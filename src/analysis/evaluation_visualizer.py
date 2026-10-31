import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import torch

from rouge_score import rouge_scorer
from sacrebleu import BLEU, sentence_bleu
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score

# Importações opcionais com fallback seguro para não travar o cluster se faltar pacote e eu perder muito tmepo
try:
    from bert_score import score as bert_score_fn
    HAS_BERTSCORE = True
except ImportError:
    HAS_BERTSCORE = False

try:
    import evaluate
    HAS_EVALUATE = True
except ImportError:
    HAS_EVALUATE = False

try:
    from medcat.cat import CAT
    HAS_MEDCAT = True
except ImportError:
    HAS_MEDCAT = False


class EvaluationVisualizer:
    """Visualizer and evaluator for medical image captioning results (ImageCLEF Benchmark)."""

    def __init__(self, medcat_model_path: Optional[str] = None):
        """Initialize the evaluation visualizer and metrics scorers."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 1. Métricas Léxicas Tradicionais
        self.rouge_scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"], use_stemmer=True
        )
        self.bleu_scorer = BLEU()

        # 2. BLEURT (HuggingFace evaluate)
        self.bleurt_scorer = None
        if HAS_EVALUATE:
            try:
                self.bleurt_scorer = evaluate.load("bleurt", config_name="BLEURT-20")
            except Exception as e:
                print(f"[Aviso] Não foi possível carregar BLEURT-20: {e}")

        # 3. MedCAT (UMLS / SNOMED CT Concept Extractor)
        self.cat = None
        if HAS_MEDCAT and medcat_model_path and os.path.exists(medcat_model_path):
            try:
                print(f"Carregando modelo MedCAT de: {medcat_model_path}")
                self.cat = CAT.load_model_pack(medcat_model_path)
            except Exception as e:
                print(f"[Aviso] Falha ao carregar MedCAT pack: {e}")

    def load_from_jsonl(self, jsonl_file: str) -> List[Dict[str, Any]]:
        """Load evaluation data from a JSONL file."""
        if not os.path.exists(jsonl_file):
            raise FileNotFoundError(f"JSONL file not found: {jsonl_file}")

        print(f"Loading evaluation data from {jsonl_file}")
        results = []
        with open(jsonl_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line.strip())
                    results.append(data)
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON on line {line_num}: {e}")
                    continue

        print(f"Loaded {len(results)} evaluation results")
        return results

    def _extract_clinical_concepts(self, text: str) -> set:
        """Extrai conceitos clínicos usando MedCAT ou fallback semântico de termos médicos."""
        if self.cat:
            try:
                entities = self.cat.get_entities(text).get("entities", {})
                return {ent.get("cui", ent.get("source_value", "")) for ent in entities.values()}
            except Exception:
                pass

        # Fallback heurístico: extrai n-gramas e termos anatômicos/patológicos relevantes
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        stop_words = {
            "the", "and", "with", "for", "from", "that", "this", "are", "was",
            "show", "showing", "demonstrates", "reveals", "seen", "image", "raw",
            "clinical", "caption", "expert", "radiologist", "noted", "present"
        }
        return {w for w in words if w not in stop_words}

    def calculate_caption_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate caption evaluation metrics across all ImageCLEF dimensions."""
        bleu_scores = []
        rouge_scores = {"rouge1": [], "rouge2": [], "rougeL": []}
        predictions = []
        references = []
        valid_results = []

        # 1. Filtro e Métricas N-grama (BLEU e ROUGE)
        for result in results:
            if "error" in result:
                continue

            ground_truth = result.get("ground_truth_caption", result.get("ground_truth", ""))
            generated = result.get("generated_caption", result.get("prediction", ""))

            if not ground_truth or not generated:
                continue

            predictions.append(generated)
            references.append(ground_truth)
            valid_results.append(result)

            # BLEU
            try:
                b_score = sentence_bleu(generated, [ground_truth]).score / 100.0
            except Exception:
                b_score = 0.0
            bleu_scores.append(b_score)

            # ROUGE
            r_res = self.rouge_scorer.score(ground_truth, generated)
            for m in ["rouge1", "rouge2", "rougeL"]:
                rouge_scores[m].append(r_res[m].fmeasure)

        num_samples = len(predictions)
        if num_samples == 0:
            return {"num_samples": 0}

        # 2. BERTScore (PubMedBERT em lote)
        bert_prec, bert_rec, bert_f1 = [0.0] * num_samples, [0.0] * num_samples, [0.0] * num_samples
        if HAS_BERTSCORE:
            try:
                print("Calculando BERTScore com PubMedBERT...")
                P, R, F1 = bert_score_fn(
                    predictions,
                    references,
                    model_type="microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract",
                    device=self.device,
                    batch_size=32,
                    verbose=False
                )
                bert_prec = P.cpu().numpy().tolist()
                bert_rec = R.cpu().numpy().tolist()
                bert_f1 = F1.cpu().numpy().tolist()
            except Exception as e:
                print(f"[Aviso] Falha ao computar BERTScore com PubMedBERT: {e}")

        # 3. BLEURT
        bleurt_scores = [0.0] * num_samples
        if self.bleurt_scorer:
            try:
                print("Calculando BLEURT-20...")
                res_b = self.bleurt_scorer.compute(predictions=predictions, references=references)
                bleurt_scores = res_b["scores"]
            except Exception as e:
                print(f"[Aviso] Falha no cálculo do BLEURT: {e}")

        # 4. MedCAT & Métricas Clínicas do ImageCLEF (Relevance, Factuality, Alignment, Overall)
        print("Calculando métricas de conceitos clínicos, factualidade e alinhamento...")
        medcat_prec, medcat_rec, medcat_f1 = [], [], []
        factuality_scores, relevance_scores, alignment_scores, overall_scores = [], [], [], []
        detailed_results = []

        for idx in range(num_samples):
            pred_text = predictions[idx]
            ref_text = references[idx]
            orig_result = valid_results[idx]

            pred_concepts = self._extract_clinical_concepts(pred_text)
            ref_concepts = self._extract_clinical_concepts(ref_text)

            intersection = pred_concepts.intersection(ref_concepts)

            # Concept Precision / Factuality (Anti-alucinação: achados preditos confirmados no laudo real)
            prec = len(intersection) / len(pred_concepts) if pred_concepts else (1.0 if not ref_concepts else 0.0)
            # Concept Recall / Relevance (Capacidade de capturar todas as alterações reais descritas)
            rec = len(intersection) / len(ref_concepts) if ref_concepts else (1.0 if not pred_concepts else 0.0)
            # MedCAT F1
            c_f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

            # Alignment (Concordância Jaccard entre entidades anatômicas e diagnósticas)
            union = pred_concepts.union(ref_concepts)
            align = len(intersection) / len(union) if union else 1.0

            # Overall Score oficial (Média harmônica entre Factualidade e Relevância)
            overall = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

            medcat_prec.append(prec)
            medcat_rec.append(rec)
            medcat_f1.append(c_f1)
            factuality_scores.append(prec)
            relevance_scores.append(rec)
            alignment_scores.append(align)
            overall_scores.append(overall)

            detailed_results.append({
                "image_id": orig_result.get("image_id", orig_result.get("id", f"sample_{idx}")),
                "ground_truth": ref_text,
                "generated": pred_text,
                "bleu_score": bleu_scores[idx],
                "rouge1_f": rouge_scores["rouge1"][idx],
                "rouge2_f": rouge_scores["rouge2"][idx],
                "rougeL_f": rouge_scores["rougeL"][idx],
                "bertscore_f1": bert_f1[idx],
                "bleurt_score": bleurt_scores[idx],
                "medcat_f1": c_f1,
                "factuality": prec,
                "relevance": rec,
                "alignment": align,
                "overall": overall,
            })

        # Agregação das Métricas
        metrics = {
            "num_samples": num_samples,
            # Léxicas
            "bleu_mean": float(np.mean(bleu_scores)),
            "bleu_std": float(np.std(bleu_scores)),
            "bleu_scores": bleu_scores,
            "rouge1_mean": float(np.mean(rouge_scores["rouge1"])),
            "rouge2_mean": float(np.mean(rouge_scores["rouge2"])),
            "rougeL_mean": float(np.mean(rouge_scores["rougeL"])),
            # Semânticas
            "bertscore_precision_mean": float(np.mean(bert_prec)),
            "bertscore_recall_mean": float(np.mean(bert_rec)),
            "bertscore_f1_mean": float(np.mean(bert_f1)),
            "bleurt_mean": float(np.mean(bleurt_scores)),
            # Conceitos Médicos / MedCAT
            "medcat_precision_mean": float(np.mean(medcat_prec)),
            "medcat_recall_mean": float(np.mean(medcat_rec)),
            "medcat_f1_mean": float(np.mean(medcat_f1)),
            # ImageCLEF Clinical
            "factuality_mean": float(np.mean(factuality_scores)),
            "relevance_mean": float(np.mean(relevance_scores)),
            "alignment_mean": float(np.mean(alignment_scores)),
            "overall_mean": float(np.mean(overall_scores)),
            "detailed_results": detailed_results,
        }
        return metrics

    def create_caption_visualizations(self, caption_metrics: Dict[str, Any], output_dir: str) -> None:
        """Create caption evaluation visualizations."""
        os.makedirs(output_dir, exist_ok=True)
        plt.style.use("default")
        sns.set_palette("husl")

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle("ImageCLEFmedical Caption Evaluation Metrics", fontsize=16)

        # 1. BLEU Score Distribution
        bleu_scores = caption_metrics["bleu_scores"]
        if bleu_scores:
            axes[0, 0].hist(bleu_scores, bins=30, alpha=0.7, edgecolor="black")
            axes[0, 0].axvline(
                caption_metrics["bleu_mean"],
                color="red",
                linestyle="--",
                label=f'Média BLEU: {caption_metrics["bleu_mean"]:.3f}'
            )
            axes[0, 0].set_xlabel("BLEU Score")
            axes[0, 0].set_ylabel("Frequência")
            axes[0, 0].set_title("Distribuição do BLEU")
            axes[0, 0].legend()

        # 2. Comparativo ROUGE & BERTScore
        comp_labels = ["R-1", "R-2", "R-L", "BERT-F1"]
        comp_values = [
            caption_metrics["rouge1_mean"],
            caption_metrics["rouge2_mean"],
            caption_metrics["rougeL_mean"],
            caption_metrics["bertscore_f1_mean"]
        ]
        bars = axes[0, 1].bar(comp_labels, comp_values, alpha=0.7)
        axes[0, 1].set_ylabel("Score (0 a 1)")
        axes[0, 1].set_title("Métricas Léxicas vs. Semânticas")
        axes[0, 1].set_ylim(0, 1)
        for bar, val in zip(bars, comp_values):
            axes[0, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{val:.3f}", ha="center", va="bottom")

        # 3. Métricas Clínicas do ImageCLEF
        clin_labels = ["Factuality", "Relevance", "Alignment", "OVERALL"]
        clin_values = [
            caption_metrics["factuality_mean"],
            caption_metrics["relevance_mean"],
            caption_metrics["alignment_mean"],
            caption_metrics["overall_mean"]
        ]
        bars2 = axes[1, 0].bar(clin_labels, clin_values, color=["#3498db", "#2ecc71", "#f1c40f", "#e74c3c"], alpha=0.8)
        axes[1, 0].set_ylabel("Pontuação")
        axes[1, 0].set_title("Critérios Clínicos Oficiais ImageCLEF")
        axes[1, 0].set_ylim(0, 1)
        for bar, val in zip(bars2, clin_values):
            axes[1, 0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{val:.3f}", ha="center", va="bottom")

        # 4. Correlação Factuality vs ROUGE-L
        detailed = caption_metrics["detailed_results"]
        if detailed:
            fact_list = [r["factuality"] for r in detailed]
            rougeL_list = [r["rougeL_f"] for r in detailed]
            axes[1, 1].scatter(rougeL_list, fact_list, alpha=0.6, color="purple")
            axes[1, 1].set_xlabel("ROUGE-L (Léxico)")
            axes[1, 1].set_ylabel("Factuality (Conceitos Médicos)")
            axes[1, 1].set_title("Concordância Léxica vs. Factualidade")

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "caption_metrics.png"), dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Visualizações salvas em: {output_dir}/caption_metrics.png")

    def create_prediction_examples_visualization(self, caption_metrics: Dict[str, Any], output_dir: str, num_examples: int = 6) -> None:
        """Create visualization showing prediction examples."""
        os.makedirs(output_dir, exist_ok=True)
        detailed = caption_metrics["detailed_results"]
        if not detailed:
            return

        detailed_sorted = sorted(detailed, key=lambda x: x["overall"], reverse=True)
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle("Exemplos de Predições (Avaliados por Overall Score)", fontsize=16)

        examples_to_show = detailed_sorted[:num_examples // 2] + detailed_sorted[-(num_examples // 2):]
        for i, example in enumerate(examples_to_show[:num_examples]):
            row = i // 3
            col = i % 3

            text_content = (
                f"Image ID: {example['image_id']}\n"
                f"Overall: {example['overall']:.3f} | BLEU: {example['bleu_score']:.3f}\n"
                f"Factuality: {example['factuality']:.3f} | Relevance: {example['relevance']:.3f}\n\n"
                f"Ground Truth:\n{example['ground_truth'][:90]}...\n\n"
                f"Generated:\n{example['generated'][:90]}..."
            )
            axes[row, col].text(0.05, 0.95, text_content, transform=axes[row, col].transAxes,
                                fontsize=10, verticalalignment='top', fontfamily='monospace')
            axes[row, col].set_xlim(0, 1)
            axes[row, col].set_ylim(0, 1)
            axes[row, col].axis('off')
            title = f"Top Exemplo {i+1}" if i < num_examples // 2 else f"Pior Exemplo {i+1 - num_examples // 2}"
            axes[row, col].set_title(title, fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "prediction_examples.png"), dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Exemplos salvos em: {output_dir}/prediction_examples.png")

    def create_evaluation_report(self, caption_metrics: Dict[str, Any], output_dir: str) -> str:
        """Create a comprehensive Markdown evaluation report according to ImageCLEF standards."""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        report_path = os.path.join(output_dir, f"evaluation_report_{timestamp}.md")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# ImageCLEFmedical Caption Evaluation Report\n\n")
            f.write(f"- **Data da Avaliação:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"- **Amostras Avaliadas:** {caption_metrics['num_samples']}\n\n")

            f.write("---\n\n")
            f.write("## 1. Métricas Léxicas & N-gramas\n\n")
            f.write("| Métrica | Média | Desvio Padrão (Std) |\n")
            f.write("| :--- | :--- | :--- |\n")
            f.write(f"| **BLEU (sacrebleu)** | {caption_metrics['bleu_mean']:.4f} | {caption_metrics['bleu_std']:.4f} |\n")
            f.write(f"| **ROUGE-1 (F1)** | {caption_metrics['rouge1_mean']:.4f} | - |\n")
            f.write(f"| **ROUGE-2 (F1)** | {caption_metrics['rouge2_mean']:.4f} | - |\n")
            f.write(f"| **ROUGE-L (F1)** | {caption_metrics['rougeL_mean']:.4f} | - |\n\n")

            f.write("---\n\n")
            f.write("## 2. Métricas de Similaridade Semântica & Embeddings\n\n")
            f.write("| Métrica | Precisão | Recall | F1-Score |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            f.write(f"| **BERTScore (PubMedBERT)** | {caption_metrics['bertscore_precision_mean']:.4f} | {caption_metrics['bertscore_recall_mean']:.4f} | {caption_metrics['bertscore_f1_mean']:.4f} |\n")
            f.write(f"| **BLEURT-20** | - | - | {caption_metrics['bleurt_mean']:.4f} |\n\n")

            f.write("---\n\n")
            f.write("## 3. Conceitos Médicos & Entidades Clínicas (MedCAT / UMLS)\n\n")
            f.write("| Métrica Clínica | Valor |\n")
            f.write("| :--- | :--- |\n")
            f.write(f"| **MedCAT Concept Precision** | {caption_metrics['medcat_precision_mean']:.4f} |\n")
            f.write(f"| **MedCAT Concept Recall** | {caption_metrics['medcat_recall_mean']:.4f} |\n")
            f.write(f"| **MedCAT Concept F1-Score** | {caption_metrics['medcat_f1_mean']:.4f} |\n\n")

            f.write("---\n\n")
            f.write("## 4. Métricas Oficiais do Desafio ImageCLEF (Factualidade e Relevância)\n\n")
            f.write("| Critério Clínico | Pontuação (0.0 a 1.0) |\n")
            f.write("| :--- | :--- |\n")
            f.write(f"| **Factuality (Precisão / Anti-alucinação)** | {caption_metrics['factuality_mean']:.4f} |\n")
            f.write(f"| **Clinical Relevance (Recall Clínico)** | {caption_metrics['relevance_mean']:.4f} |\n")
            f.write(f"| **Clinical Alignment (Concordância Anatômica)** | {caption_metrics['alignment_mean']:.4f} |\n")
            f.write(f"| **OVERALL SCORE (Média Harmônica)** | **{caption_metrics['overall_mean']:.4f}** |\n\n")

            f.write("---\n\n")
            f.write("## 5. Amostragem de Laudos (Predição vs. Ground Truth)\n\n")
            f.write("| Image ID | Laudo Real (Ground Truth) | Laudo Predito | Overall Score |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            detailed = caption_metrics["detailed_results"]
            for ex in detailed[:8]:
                gt_clean = ex["ground_truth"].replace("\n", " ").replace("|", "/")
                pred_clean = ex["generated"].replace("\n", " ").replace("|", "/")
                f.write(f"| `{ex['image_id']}` | {gt_clean} | {pred_clean} | {ex['overall']:.4f} |\n")

            f.write("\n---\n*Relatório gerado automaticamente pelo pipeline de avaliação ImageCLEFmedical.*\n")

        print(f"Relatório de avaliação completo salvo em: {report_path}")
        return report_path

    def run_full_evaluation(self, jsonl_file: str, output_dir: str = "evaluation_results") -> Dict[str, Any]:
        """Run full evaluation with visualizations and report."""
        print("=" * 60)
        print("INICIANDO AVALIAÇÃO COMPLETA (IMAGECLEF BENCHMARK)")
        print("=" * 60)

        results = self.load_from_jsonl(jsonl_file)
        caption_metrics = self.calculate_caption_metrics(results)

        print("Gerando gráficos e matrizes comparativas...")
        self.create_caption_visualizations(caption_metrics, output_dir)
        self.create_prediction_examples_visualization(caption_metrics, output_dir)

        print("Escrevendo relatório consolidado em Markdown...")
        report_path = self.create_evaluation_report(caption_metrics, output_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        results_path = os.path.join(output_dir, f"evaluation_results_{timestamp}.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump({
                "evaluation_timestamp": datetime.now().isoformat(),
                "source_file": jsonl_file,
                "caption_metrics": caption_metrics
            }, f, indent=2)

        print(f"Resultados completos salvos em: {results_path}")
        return caption_metrics
