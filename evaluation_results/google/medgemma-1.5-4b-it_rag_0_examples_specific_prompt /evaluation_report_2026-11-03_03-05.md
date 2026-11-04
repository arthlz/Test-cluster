# ImageCLEFmedical Caption Evaluation Report

- **Data da Avaliação:** 2026-11-03 03:05
- **Amostras Avaliadas:** 9927

---

## 1. Métricas Léxicas & N-gramas

| Métrica | Média | Desvio Padrão (Std) |
| :--- | :--- | :--- |
| **BLEU (sacrebleu)** | 0.0229 | 0.0247 |
| **ROUGE-1 (F1)** | 0.1913 | - |
| **ROUGE-2 (F1)** | 0.0516 | - |
| **ROUGE-L (F1)** | 0.1514 | - |

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
| **MedCAT Concept Precision** | 0.1190 |
| **MedCAT Concept Recall** | 0.2012 |
| **MedCAT Concept F1-Score** | 0.1345 |

---

## 4. Métricas Oficiais do Desafio ImageCLEF (Factualidade e Relevância)

| Critério Clínico | Pontuação (0.0 a 1.0) |
| :--- | :--- |
| **Factuality (Precisão / Anti-alucinação)** | 0.1190 |
| **Clinical Relevance (Recall Clínico)** | 0.2012 |
| **Clinical Alignment (Concordância Anatômica)** | 0.0760 |
| **OVERALL SCORE (Média Harmônica)** | **0.1345** |

---

## 5. Amostragem de Laudos (Predição vs. Ground Truth)

| Image ID | Laudo Real (Ground Truth) | Laudo Predito | Overall Score |
| :--- | :--- | :--- | :--- |
| `ROCOv2_2023_test_000001` | CT chest axial view showing a huge ascending aortic aneurysm (*). | {   "caption": "Chest X-ray image showing the heart, lungs, and mediastinum. The heart appears enlarged. A radiopaque marker is present in the right upper lobe." } | 0.1053 |
| `ROCOv2_2023_test_000002` | Computed tomography (CT) shows floating thrombosis (white arrow) | {   "caption": "Coronary CT angiography (CTA) of the chest, axial view. The image shows the coronary arteries, with the left main coronary artery highlighted by the white arrow. The left main coronary artery is seen coursing between the left atrium and left ventricle." } | 0.2400 |
| `ROCOv2_2023_test_000003` | Digitally subtracted angiogram demonstrates active extravasation of the superior rectal artery into the ileal-conduit (blue arrow) | {   "caption": "Angiogram of the lower extremities, showing the left common iliac artery. A catheter is visible within the artery, with a small focus of contrast material noted near the bifurcation." } | 0.1379 |
| `ROCOv2_2023_test_000004` | Digitally subtracted angiogram of the IMA demonstrated cessation of flow through the proximal superior rectal artery in the region of the intersection between the artery and ureter with retained perfusion of the rectosigmoid region and resolution of active extravasation | {   "caption": "Angiography of the lower extremities, showing the left common iliac artery and its branches. A catheter is visible within the left common iliac artery." } | 0.0588 |
| `ROCOv2_2023_test_000005` | Angle measurement of a Type 1 canal. | {   "caption": "Axial CT image of the right shoulder joint. The image displays the glenohumeral joint, including the humeral head, glenoid fossa, and surrounding soft tissues. The humeral head is visible, and the glenoid fossa is also apparent. The image shows the acromioclavicular joint. The image is oriented in the axial plane." } | 0.0000 |
| `ROCOv2_2023_test_000006` | Computed tomography on day 26Follow-up enhanced computed tomography on day 26 revealed no apparent progression of left iliopsoas hematoma, and no extravasation of contrast media was seen. | <unused94>thought The user wants me to act as a radiology specialist and provide a caption for the given medical image.  1.  **Analyze the image:**     *   **Modality:** CT scan (based on the image appearance and typical use).     *   **Body region:** Abdomen.     *   **Orientation:** Axial view.     *   **Visible structures:**         *   Kidneys (left kidney appears enlarged, possibly cystic or solid mass).         *   Ureters (visible, but not clearly delineated).         *   Bladder (partially visible).         *   Abdominal aorta (visible).         *   Other abdominal organs (liver, spleen, bowel loops) are present but not clearly defined.         *   Bones (vertebral bodies, ribs).     *   **Abnormalities/Findings:**         *   The left kidney is significantly enlarged and has a heterogeneous appearance, suggesting a possible mass or complex cyst.         *   There is a possible fluid collection or cyst in the left kidney.     *   **Medical devices:** None are visible.  2.  **Note abnormalities/findings:**     *   Enlarged left kidney with possible mass/cyst.  3.  **Generate caption:**     *   Start with the modality and body region: "CT scan of the abdomen"     *   Describe the main finding: "showing a markedly enlarged left kidney"     *   Add details about the appearance: "with a heterogeneous appearance and possible cystic or solid component."     *   Mention other visible structures if relevant, but keep it concise. "The right kidney and other abdominal structures are partially visualized." (This is less important than the left kidney finding).     *   Combine and refine: "CT scan of the abdomen demonstrating a markedly enlarged left kidney with a heterogeneous appearance and possible cystic or solid component."  4.  **Final Check:**     *   Is it concise? Yes.     *   Is it clinically accurate? Yes, based on visual evidence.     *   Does it focus on visible content? Yes.     *   Does it use appropriate terminology? Yes (CT scan, abdomen, left kidney, heterogeneous appearance, cystic/solid component).     *   Is it objective? Yes, avoids speculation.     *   Is it similar to biomedical literature captions? Yes.  5.  **Format as JSON:**     ```json | 0.0161 |
| `ROCOv2_2023_test_000007` | Enhanced CT scan of the chest revealed an anterior mediastinal tumor (black arrow). | {   "caption": "Chest X-ray showing the heart, lungs, and mediastinum. The heart appears enlarged. A black arrow points to a possible abnormality in the upper right lung." } | 0.2500 |
| `ROCOv2_2023_test_000008` | Arrow shows ULP at the distal arch. | {   "caption": "Axial CT scan of the chest, demonstrating the heart, lungs, and mediastinum. The image shows the thoracic aorta, pulmonary arteries, and the left main bronchus. A white arrow points to the left main bronchus." } | 0.1739 |

---
*Relatório gerado automaticamente pelo pipeline de avaliação ImageCLEFmedical.*
