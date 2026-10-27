import torch
from PIL import Image
from src.llm.llm_utils import MedicalImageCaptioner

def test_models():
    # 1. Criação de uma imagem simulada para teste (ou aponte para um ficheiro real .jpg/.png)
    test_image = Image.new("RGB", (512, 512), color=(128, 128, 128))
    prompt_path = "prompts/specific_prompt.txt"

    mock_rag_examples = [
        {
            "caption": "Chest X-ray showing mild cardiomegaly without acute pulmonary consolidation.",
            "image": test_image
        }
    ]

    model_to_test = "Qwen/Qwen3-VL-4B-Instruct"
    # Para validar a alternância com o MedGemma, só descomentar a linha abaixo :) 
    # model_to_test = "google/medgemma-1.5-4b-it"

    print("=" * 60)
    print(f"A inicializar o modelo: {model_to_test}")
    print("=" * 60)

    captioner = MedicalImageCaptioner(
        provider="huggingface",
        model_name=model_to_test,
        max_tokens=512,
        prompt_file=prompt_path
    )

    # 2. Teste da geração direta (Zero-Shot)
    print("\n--- Teste 1: generate_caption (Direct) ---")
    res_direct, meta_direct = captioner.generate_caption(test_image)
    print("Laudo gerado:")
    print(res_direct["caption"])
    print(f"Metadados de tokens: {meta_direct}")

    # 3. Teste da geração com RAG
    print("\n--- Teste 2: generate_caption_with_rag (Few-Shot) ---")
    res_rag, meta_rag, _ = captioner.generate_caption_with_rag(test_image, mock_rag_examples)
    print("Laudo gerado com RAG:")
    print(res_rag["caption"])
    print(f"Metadados de tokens: {meta_rag}")

    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    test_models()
