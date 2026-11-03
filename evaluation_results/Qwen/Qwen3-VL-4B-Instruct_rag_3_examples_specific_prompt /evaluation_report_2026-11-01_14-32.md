# RocoV2 Caption Evaluation Report

- **Data da Avaliação:** 2026-11-01 14:32
- **Amostras Avaliadas:** 9927

---

## 1. Métricas Léxicas & N-gramas

| Métrica | Média | Desvio Padrão (Std) |
| :--- | :--- | :--- |
| **BLEU (sacrebleu)** | 0.0274 | 0.0291 |
| **ROUGE-1 (F1)** | 0.2128 | - |
| **ROUGE-2 (F1)** | 0.0507 | - |
| **ROUGE-L (F1)** | 0.1609 | - |

---

## 2. Métricas de Similaridade Semântica & Embeddings

| Métrica | Precisão | Recall | F1-Score |
| :--- | :--- | :--- | :--- |
| **BERTScore (PubMedBERT)** | 0.0000 | 0.0000 | 0.0000 |
| **BLEURT-20** | - | - | 0.0000 |

---

## 3. Conceitos Médicos & Entidades Clínicas (MedCAT / UMLS)

| Métrica Clínica | Valor |
| :--- | :--- |
| **MedCAT Concept Precision** | 0.1251 |
| **MedCAT Concept Recall** | 0.2154 |
| **MedCAT Concept F1-Score** | 0.1455 |

---

## 4. Métricas Oficiais do Desafio ImageCLEF (Factualidade e Relevância)

| Critério Clínico | Pontuação (0.0 a 1.0) |
| :--- | :--- |
| **Factuality (Precisão / Anti-alucinação)** | 0.1251 |
| **Clinical Relevance (Recall Clínico)** | 0.2154 |
| **Clinical Alignment (Concordância Anatômica)** | 0.0826 |
| **OVERALL SCORE (Média Harmônica)** | **0.1455** |

---

## 5. Amostragem de Laudos (Predição vs. Ground Truth)

| Image ID | Laudo Real (Ground Truth) | Laudo Predito | Overall Score |
| :--- | :--- | :--- | :--- |
| `ROCOv2_2023_test_000001` | CT chest axial view showing a huge ascending aortic aneurysm (*). | {     "caption": "Transverse CT image of the thorax showing the heart (marked with asterisk), great vessels, and surrounding thoracic structures, including the lungs, ribs, and vertebral body. No obvious medical devices or pathologies are visible in this slice." } | 0.0000 |
| `ROCOv2_2023_test_000002` | Computed tomography (CT) shows floating thrombosis (white arrow) | {     "caption": "Thoracic computed tomography image showing a linear, low-attenuation structure (white arrow) within the mediastinum, consistent with a thrombus or fibrotic band in the vicinity of the cardiac silhouette." } | 0.3200 |
| `ROCOv2_2023_test_000003` | Digitally subtracted angiogram demonstrates active extravasation of the superior rectal artery into the ileal-conduit (blue arrow) | {     "caption": "Angiographic image showing a catheter positioned within a vascular structure, indicated by a blue arrow, in the lower abdominal region; the image is labeled 'LT' (left side) and depicts complex vascular anatomy with branching vessels and surrounding soft tissue." } | 0.1111 |
| `ROCOv2_2023_test_000004` | Digitally subtracted angiogram of the IMA demonstrated cessation of flow through the proximal superior rectal artery in the region of the intersection between the artery and ureter with retained perfusion of the rectosigmoid region and resolution of active extravasation | {     "caption": "Fluoroscopic image in left anterior oblique (LAO) view showing a guidewire and catheter system navigating the pelvic vasculature, with visible branching vessels and a labeled 'LT' indicating the left side." } | 0.0000 |
| `ROCOv2_2023_test_000005` | Angle measurement of a Type 1 canal. | {     "caption": "Axial CT image showing the femoral head–neck junction with two angular measurements annotated: 128.6° and 73.3°, indicating angular relationships at the proximal femur. The measurements are derived from defined anatomical landmarks and are presented in degrees as labeled." } | 0.0000 |
| `ROCOv2_2023_test_000006` | Computed tomography on day 26Follow-up enhanced computed tomography on day 26 revealed no apparent progression of left iliopsoas hematoma, and no extravasation of contrast media was seen. | {     "caption": "Axial contrast-enhanced CT scan of the abdomen showing the vertebral body, lumbar spine, and surrounding abdominal organs including the kidneys, intestines, and major vessels. No obvious abnormalities, interventions, or pathologies are visible in this slice." } | 0.1111 |
| `ROCOv2_2023_test_000007` | Enhanced CT scan of the chest revealed an anterior mediastinal tumor (black arrow). | {     "caption": "Axial computed tomography image of the thorax showing a well-defined, enhancing mass at the superior mediastinum, with a prominent arrow indicating the lesion's location adjacent to the trachea and great vessels." } | 0.0714 |
| `ROCOv2_2023_test_000008` | Arrow shows ULP at the distal arch. | {     "caption": "Sagittal CT image of the thorax showing a metallic foreign body (arrow) located in the posterior mediastinum, adjacent to the thoracic spine and great vessels." } | 0.1053 |

---
*Relatório gerado automaticamente pelo pipeline de avaliação ImageCLEFmedical.*
