# ImageCLEFmedical Caption Evaluation Report

- **Data da Avaliação:** 2026-10-31 22:17
- **Amostras Avaliadas:** 9927

---

## 1. Métricas Léxicas & N-gramas

| Métrica | Média | Desvio Padrão (Std) |
| :--- | :--- | :--- |
| **BLEU (sacrebleu)** | 0.0222 | 0.0245 |
| **ROUGE-1 (F1)** | 0.1924 | - |
| **ROUGE-2 (F1)** | 0.0459 | - |
| **ROUGE-L (F1)** | 0.1434 | - |

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
| **MedCAT Concept Precision** | 0.1021 |
| **MedCAT Concept Recall** | 0.2255 |
| **MedCAT Concept F1-Score** | 0.1298 |

---

## 4. Métricas Oficiais do Desafio ImageCLEF (Factualidade e Relevância)

| Critério Clínico | Pontuação (0.0 a 1.0) |
| :--- | :--- |
| **Factuality (Precisão / Anti-alucinação)** | 0.1021 |
| **Clinical Relevance (Recall Clínico)** | 0.2255 |
| **Clinical Alignment (Concordância Anatômica)** | 0.0726 |
| **OVERALL SCORE (Média Harmônica)** | **0.1298** |

---

## 5. Amostragem de Laudos (Predição vs. Ground Truth)

| Image ID | Laudo Real (Ground Truth) | Laudo Predito | Overall Score |
| :--- | :--- | :--- | :--- |
| `ROCOv2_2023_test_000001` | CT chest axial view showing a huge ascending aortic aneurysm (*). | {     "caption": "Axial computed tomography (CT) image of the thorax demonstrating the heart, great vessels, and surrounding thoracic structures. A circular metallic density is visible within the cardiac silhouette, consistent with a cardiac implant. The lungs are air-filled and appear unremarkable. The vertebral body and ribs are visible in the posterior and lateral aspects, respectively. No other abnormalities are evident in this slice." } | 0.0465 |
| `ROCOv2_2023_test_000002` | Computed tomography (CT) shows floating thrombosis (white arrow) | {     "caption": "Coronal CT image demonstrating a metallic stent straddling the left main coronary artery, indicated by the arrow, with adjacent cardiac and pulmonary vasculature visible." } | 0.0870 |
| `ROCOv2_2023_test_000003` | Digitally subtracted angiogram demonstrates active extravasation of the superior rectal artery into the ileal-conduit (blue arrow) | {     "caption": "Angiographic image showing the left iliac artery with a guidewire (blue arrow) positioned within the vessel lumen, demonstrating normal arterial flow and branching patterns. The image is oriented with 'LT' indicating the left side of the body." } | 0.1765 |
| `ROCOv2_2023_test_000004` | Digitally subtracted angiogram of the IMA demonstrated cessation of flow through the proximal superior rectal artery in the region of the intersection between the artery and ureter with retained perfusion of the rectosigmoid region and resolution of active extravasation | {     "caption": "Anteroposterior radiograph of the pelvic region demonstrating a guidewire and catheter system in the pelvic vasculature, with the left side indicated by 'LT'. The guidewire is coursing through the pelvic vessels, and a catheter is positioned proximally with a visible distal tip. The surrounding vascular architecture is visible, including branching vessels and pelvic structures." } | 0.0833 |
| `ROCOv2_2023_test_000005` | Angle measurement of a Type 1 canal. | {     "caption": "Coronal CT image demonstrating a metallic implant with two measured angles: 128.6° and 73.3°, indicated by digital annotations, within the context of a joint or bone structure." } | 0.0000 |
| `ROCOv2_2023_test_000006` | Computed tomography on day 26Follow-up enhanced computed tomography on day 26 revealed no apparent progression of left iliopsoas hematoma, and no extravasation of contrast media was seen. | {     "caption": "Axial computed tomography image of the abdomen showing the vertebral body, bilateral iliac bones, and abdominal organs including the liver, spleen, and bowel loops. The image demonstrates normal anatomical relationships with no visible foreign bodies, contrast agents, or acute pathological lesions." } | 0.1500 |
| `ROCOv2_2023_test_000007` | Enhanced CT scan of the chest revealed an anterior mediastinal tumor (black arrow). | {     "caption": "Axial computed tomography image of the thorax demonstrating a metallic foreign body (arrow) located in the superior mediastinum, adjacent to the right clavicle and superior aspect of the heart. The image shows normal bony thoracic structures, including the vertebral body, ribs, and sternum, with no evidence of acute hemorrhage or air collection. The lungs are aerated, and the mediastinal contour is unremarkable except for the presence of the foreign body." } | 0.0851 |
| `ROCOv2_2023_test_000008` | Arrow shows ULP at the distal arch. | {     "caption": "Coronal CT image of the thorax showing the mediastinum, great vessels, and thoracic spine. A metallic foreign body is visible within the right upper mediastinum, indicated by the arrow, consistent with a retained surgical implant or device. The vertebral bodies and intervertebral discs are visible along the posterior aspect of the image." } | 0.0606 |

---
*Relatório gerado automaticamente pelo pipeline de avaliação ImageCLEFmedical.*
