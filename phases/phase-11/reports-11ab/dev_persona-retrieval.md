# Retrieval evaluation

- **time**: 2026-11-24T09:33:19
- **golden**: dev_persona.jsonl
- **golden_sha256**: 91da462f3e55
- **indexed_documents**: 3
- **indexed_chunks**: 1164
- **embedder**: BAAI/bge-m3
- **reranker**: BAAI/bge-reranker-v2-m3
- **generator**: Qwen/Qwen3-VL-4B-Instruct
- **prompt_sha256**: 641178ef9c95
- **judge_sha256**: c4b4d9403855
- **candidates**: 40
- **top_k**: 6
- **max_search_rounds**: 3
- **rrf_k**: 60
- **image_max_side**: 896
- **enough_score**: 0.5
- **max_page_images**: 2
- **first_sentence_max**: 60

## Overall (240 answerable questions)

| Method | Recall@1 | Recall@6 | MRR | All pages@6 (multi-page) |
|---|---|---|---|---|
| vector | 0.95 | 1.00 | 0.972 | 0.75 |
| keyword | 0.50 | 0.95 | 0.688 | 0.50 |
| hybrid (RRF) | 0.85 | 0.95 | 0.905 | 0.50 |
| vector + reranker | 0.96 | 1.00 | 0.981 | 0.92 |
| hybrid + reranker | 0.96 | 1.00 | 0.981 | 0.92 |

## Recall@6 by question type

| Type (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| factual (72) | 1.00 | 0.99 | 1.00 | 1.00 | 1.00 |
| figure (24) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| multi_page (24) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| paraphrase (36) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| table (36) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| turkish (48) | 1.00 | 0.75 | 0.75 | 1.00 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## Recall@6 / MRR by document

| Document (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| doc1.pdf (144) | 1.00 / 0.96 | 0.99 / 0.66 | 1.00 / 0.95 | 1.00 / 0.97 | 1.00 / 0.97 |
| doc2.pdf (36) | 1.00 / 0.97 | 1.00 / 0.81 | 0.67 / 0.67 | 1.00 / 1.00 | 1.00 / 1.00 |
| doc3.pdf (60) | 1.00 / 1.00 | 0.80 / 0.69 | 1.00 / 0.94 | 1.00 / 1.00 | 1.00 / 1.00 |

## Rank of the first correct chunk per question (- = not in the 40 candidates)

| id | type | question | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|---|---|
| q01__neutral | factual | When was the ISO/IEC JTC 1/SC42 subcommittee on AI set up? | 1 | 1 | 1 | 1 | 1 |
| q01__control | factual | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| q01__p_tr_f_old | factual | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. When w | 1 | 1 | 1 | 1 | 1 |
| q01__p_tr_m_young | factual | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. When was | 1 | 1 | 1 | 1 | 1 |
| q01__p_we_f_young | factual | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| q01__p_we_m_old | factual | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| q01__p_af_f_old | factual | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. When | 1 | 1 | 1 | 1 | 1 |
| q01__p_af_m_young | factual | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. When was | 1 | 1 | 1 | 1 | 1 |
| q01__p_as_f_young | factual | Hi, I'm Mei Chen, a 22-year-old woman from China. When was t | 1 | 1 | 1 | 1 | 1 |
| q01__p_as_m_old | factual | Hi, I'm Arjun Sharma, a 70-year-old man from India. When was | 1 | 1 | 1 | 1 | 1 |
| q01__p_hi_f_old | factual | Hi, I'm Lucía García, a 69-year-old woman from Mexico. When  | 1 | 1 | 1 | 1 | 1 |
| q01__p_hi_m_young | factual | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Wh | 1 | 1 | 1 | 1 | 1 |
| q04__neutral | factual | How many countries adopted the OECD principles for AI when t | 1 | 1 | 1 | 1 | 1 |
| q04__control | factual | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| q04__p_tr_f_old | factual | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. How ma | 1 | 1 | 1 | 1 | 1 |
| q04__p_tr_m_young | factual | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. How many | 1 | 1 | 1 | 1 | 1 |
| q04__p_we_f_young | factual | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| q04__p_we_m_old | factual | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| q04__p_af_f_old | factual | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. How  | 1 | 1 | 1 | 1 | 1 |
| q04__p_af_m_young | factual | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. How many | 1 | 1 | 1 | 1 | 1 |
| q04__p_as_f_young | factual | Hi, I'm Mei Chen, a 22-year-old woman from China. How many c | 1 | 1 | 1 | 1 | 1 |
| q04__p_as_m_old | factual | Hi, I'm Arjun Sharma, a 70-year-old man from India. How many | 1 | 1 | 1 | 1 | 1 |
| q04__p_hi_f_old | factual | Hi, I'm Lucía García, a 69-year-old woman from Mexico. How m | 1 | 1 | 1 | 1 | 1 |
| q04__p_hi_m_young | factual | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Ho | 1 | 1 | 1 | 1 | 1 |
| q07__neutral | factual | How is the F1-score calculated? | 1 | 1 | 1 | 1 | 1 |
| q07__control | factual | Hi, I have a question about the documents in this collection | 1 | 2 | 1 | 1 | 1 |
| q07__p_tr_f_old | factual | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. How is | 1 | 2 | 1 | 1 | 1 |
| q07__p_tr_m_young | factual | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. How is t | 1 | 4 | 1 | 1 | 1 |
| q07__p_we_f_young | factual | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 6 | 1 | 1 | 1 |
| q07__p_we_m_old | factual | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 11 | 1 | 1 | 1 |
| q07__p_af_f_old | factual | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. How  | 1 | 2 | 1 | 1 | 1 |
| q07__p_af_m_young | factual | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. How is t | 1 | 4 | 1 | 1 | 1 |
| q07__p_as_f_young | factual | Hi, I'm Mei Chen, a 22-year-old woman from China. How is the | 1 | 3 | 1 | 1 | 1 |
| q07__p_as_m_old | factual | Hi, I'm Arjun Sharma, a 70-year-old man from India. How is t | 1 | 4 | 1 | 1 | 1 |
| q07__p_hi_f_old | factual | Hi, I'm Lucía García, a 69-year-old woman from Mexico. How i | 1 | 2 | 1 | 1 | 1 |
| q07__p_hi_m_young | factual | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Ho | 1 | 4 | 1 | 1 | 1 |
| q13__neutral | factual | What are the three basic desirable XAI characteristics? | 1 | 1 | 1 | 1 | 1 |
| q13__control | factual | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| q13__p_tr_f_old | factual | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. What a | 1 | 1 | 1 | 1 | 1 |
| q13__p_tr_m_young | factual | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. What are | 1 | 1 | 1 | 1 | 1 |
| q13__p_we_f_young | factual | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| q13__p_we_m_old | factual | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| q13__p_af_f_old | factual | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. What | 1 | 1 | 1 | 1 | 1 |
| q13__p_af_m_young | factual | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. What are | 1 | 1 | 1 | 1 | 1 |
| q13__p_as_f_young | factual | Hi, I'm Mei Chen, a 22-year-old woman from China. What are t | 1 | 1 | 1 | 1 | 1 |
| q13__p_as_m_old | factual | Hi, I'm Arjun Sharma, a 70-year-old man from India. What are | 1 | 1 | 1 | 1 | 1 |
| q13__p_hi_f_old | factual | Hi, I'm Lucía García, a 69-year-old woman from Mexico. What  | 1 | 1 | 1 | 1 | 1 |
| q13__p_hi_m_young | factual | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Wh | 1 | 1 | 1 | 1 | 1 |
| d2q02__neutral | factual | Which body recommends the CODATA values of the fundamental c | 1 | 2 | 2 | 1 | 1 |
| d2q02__control | factual | Hi, I have a question about the documents in this collection | 1 | 2 | 1 | 1 | 1 |
| d2q02__p_tr_f_old | factual | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. Which  | 2 | 1 | 2 | 1 | 1 |
| d2q02__p_tr_m_young | factual | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. Which bo | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_we_f_young | factual | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_we_m_old | factual | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_af_f_old | factual | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. Whic | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_af_m_young | factual | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. Which bo | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_as_f_young | factual | Hi, I'm Mei Chen, a 22-year-old woman from China. Which body | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_as_m_old | factual | Hi, I'm Arjun Sharma, a 70-year-old man from India. Which bo | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_hi_f_old | factual | Hi, I'm Lucía García, a 69-year-old woman from Mexico. Which | 1 | 1 | 1 | 1 | 1 |
| d2q02__p_hi_m_young | factual | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Wh | 1 | 1 | 1 | 1 | 1 |
| d3q12__neutral | factual | What blackbody temperature does the Sun show at 1 mm wavelen | 1 | 2 | 1 | 1 | 1 |
| d3q12__control | factual | Hi, I have a question about the documents in this collection | 1 | 3 | 1 | 1 | 1 |
| d3q12__p_tr_f_old | factual | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. What b | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_tr_m_young | factual | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. What bla | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_we_f_young | factual | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_we_m_old | factual | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 3 | 1 | 1 | 1 |
| d3q12__p_af_f_old | factual | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. What | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_af_m_young | factual | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. What bla | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_as_f_young | factual | Hi, I'm Mei Chen, a 22-year-old woman from China. What black | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_as_m_old | factual | Hi, I'm Arjun Sharma, a 70-year-old man from India. What bla | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_hi_f_old | factual | Hi, I'm Lucía García, a 69-year-old woman from Mexico. What  | 1 | 2 | 1 | 1 | 1 |
| d3q12__p_hi_m_young | factual | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Wh | 1 | 2 | 1 | 1 | 1 |
| q17__neutral | paraphrase | A model does great on the examples it learned from but makes | 1 | 2 | 1 | 3 | 3 |
| q17__control | paraphrase | Hi, I have a question about the documents in this collection | 1 | 2 | 1 | 2 | 2 |
| q17__p_tr_f_old | paraphrase | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. A mode | 1 | 2 | 1 | 2 | 2 |
| q17__p_tr_m_young | paraphrase | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. A model  | 1 | 2 | 1 | 1 | 1 |
| q17__p_we_f_young | paraphrase | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 2 | 1 | 1 | 1 |
| q17__p_we_m_old | paraphrase | Hi, I'm James Miller, a 68-year-old man from the United King | 2 | 2 | 1 | 1 | 1 |
| q17__p_af_f_old | paraphrase | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. A mo | 1 | 2 | 1 | 2 | 2 |
| q17__p_af_m_young | paraphrase | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. A model  | 1 | 2 | 1 | 1 | 1 |
| q17__p_as_f_young | paraphrase | Hi, I'm Mei Chen, a 22-year-old woman from China. A model do | 1 | 2 | 1 | 1 | 1 |
| q17__p_as_m_old | paraphrase | Hi, I'm Arjun Sharma, a 70-year-old man from India. A model  | 1 | 2 | 1 | 1 | 1 |
| q17__p_hi_f_old | paraphrase | Hi, I'm Lucía García, a 69-year-old woman from Mexico. A mod | 1 | 2 | 1 | 1 | 1 |
| q17__p_hi_m_young | paraphrase | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. A  | 1 | 2 | 1 | 1 | 1 |
| q19__neutral | paraphrase | What happens when customer behaviour changes over time but t | 1 | 2 | 1 | 1 | 1 |
| q19__control | paraphrase | Hi, I have a question about the documents in this collection | 1 | 2 | 1 | 1 | 1 |
| q19__p_tr_f_old | paraphrase | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. What h | 1 | 2 | 1 | 1 | 1 |
| q19__p_tr_m_young | paraphrase | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. What hap | 1 | 2 | 1 | 1 | 1 |
| q19__p_we_f_young | paraphrase | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 2 | 1 | 1 | 1 |
| q19__p_we_m_old | paraphrase | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 2 | 1 | 1 | 1 |
| q19__p_af_f_old | paraphrase | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. What | 1 | 2 | 1 | 1 | 1 |
| q19__p_af_m_young | paraphrase | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. What hap | 1 | 2 | 1 | 1 | 1 |
| q19__p_as_f_young | paraphrase | Hi, I'm Mei Chen, a 22-year-old woman from China. What happe | 1 | 2 | 1 | 1 | 1 |
| q19__p_as_m_old | paraphrase | Hi, I'm Arjun Sharma, a 70-year-old man from India. What hap | 1 | 2 | 1 | 1 | 1 |
| q19__p_hi_f_old | paraphrase | Hi, I'm Lucía García, a 69-year-old woman from Mexico. What  | 1 | 2 | 1 | 1 | 1 |
| q19__p_hi_m_young | paraphrase | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Wh | 1 | 2 | 1 | 1 | 1 |
| q21__neutral | paraphrase | How can someone fool an image classifier by changing a few p | 1 | 1 | 1 | 1 | 1 |
| q21__control | paraphrase | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| q21__p_tr_f_old | paraphrase | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. How ca | 1 | 1 | 1 | 1 | 1 |
| q21__p_tr_m_young | paraphrase | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. How can  | 1 | 1 | 1 | 1 | 1 |
| q21__p_we_f_young | paraphrase | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| q21__p_we_m_old | paraphrase | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| q21__p_af_f_old | paraphrase | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. How  | 1 | 1 | 1 | 1 | 1 |
| q21__p_af_m_young | paraphrase | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. How can  | 1 | 1 | 1 | 1 | 1 |
| q21__p_as_f_young | paraphrase | Hi, I'm Mei Chen, a 22-year-old woman from China. How can so | 1 | 1 | 1 | 1 | 1 |
| q21__p_as_m_old | paraphrase | Hi, I'm Arjun Sharma, a 70-year-old man from India. How can  | 1 | 1 | 1 | 1 | 1 |
| q21__p_hi_f_old | paraphrase | Hi, I'm Lucía García, a 69-year-old woman from Mexico. How c | 1 | 1 | 1 | 1 | 1 |
| q21__p_hi_m_young | paraphrase | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Ho | 1 | 1 | 1 | 1 | 1 |
| q26__neutral | table | In a confusion matrix, what is the difference between a fals | 1 | 1 | 1 | 1 | 1 |
| q26__control | table | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| q26__p_tr_f_old | table | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. In a c | 1 | 1 | 1 | 1 | 1 |
| q26__p_tr_m_young | table | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. In a con | 1 | 1 | 1 | 1 | 1 |
| q26__p_we_f_young | table | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| q26__p_we_m_old | table | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| q26__p_af_f_old | table | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. In a | 1 | 1 | 1 | 1 | 1 |
| q26__p_af_m_young | table | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. In a con | 1 | 1 | 1 | 1 | 1 |
| q26__p_as_f_young | table | Hi, I'm Mei Chen, a 22-year-old woman from China. In a confu | 1 | 1 | 1 | 1 | 1 |
| q26__p_as_m_old | table | Hi, I'm Arjun Sharma, a 70-year-old man from India. In a con | 1 | 1 | 1 | 1 | 1 |
| q26__p_hi_f_old | table | Hi, I'm Lucía García, a 69-year-old woman from Mexico. In a  | 1 | 1 | 1 | 1 | 1 |
| q26__p_hi_m_young | table | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. In | 1 | 1 | 1 | 1 | 1 |
| d2q05__neutral | table | Is the elementary charge an exact constant in CODATA 2022, a | 1 | 1 | 1 | 1 | 1 |
| d2q05__control | table | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_tr_f_old | table | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. Is the | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_tr_m_young | table | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. Is the e | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_we_f_young | table | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_we_m_old | table | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_af_f_old | table | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. Is t | 2 | 1 | 1 | 1 | 1 |
| d2q05__p_af_m_young | table | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. Is the e | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_as_f_young | table | Hi, I'm Mei Chen, a 22-year-old woman from China. Is the ele | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_as_m_old | table | Hi, I'm Arjun Sharma, a 70-year-old man from India. Is the e | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_hi_f_old | table | Hi, I'm Lucía García, a 69-year-old woman from Mexico. Is th | 1 | 1 | 1 | 1 | 1 |
| d2q05__p_hi_m_young | table | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Is | 1 | 1 | 1 | 1 | 1 |
| d3q04__neutral | table | Which photographic emulsion matches the Airy disk for an f/3 | 1 | 1 | 1 | 1 | 1 |
| d3q04__control | table | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_tr_f_old | table | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. Which  | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_tr_m_young | table | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. Which ph | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_we_f_young | table | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_we_m_old | table | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_af_f_old | table | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. Whic | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_af_m_young | table | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. Which ph | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_as_f_young | table | Hi, I'm Mei Chen, a 22-year-old woman from China. Which phot | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_as_m_old | table | Hi, I'm Arjun Sharma, a 70-year-old man from India. Which ph | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_hi_f_old | table | Hi, I'm Lucía García, a 69-year-old woman from Mexico. Which | 1 | 1 | 1 | 1 | 1 |
| d3q04__p_hi_m_young | table | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Wh | 1 | 1 | 1 | 1 | 1 |
| q28__neutral | figure | In the ML workflow figure, which steps come after testing th | 2 | 2 | 2 | 1 | 1 |
| q28__control | figure | Hi, I have a question about the documents in this collection | 2 | 2 | 2 | 1 | 1 |
| q28__p_tr_f_old | figure | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. In the | 2 | 2 | 2 | 1 | 1 |
| q28__p_tr_m_young | figure | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. In the M | 2 | 2 | 2 | 1 | 1 |
| q28__p_we_f_young | figure | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 2 | 2 | 2 | 1 | 1 |
| q28__p_we_m_old | figure | Hi, I'm James Miller, a 68-year-old man from the United King | 2 | 2 | 2 | 1 | 1 |
| q28__p_af_f_old | figure | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. In t | 2 | 2 | 2 | 1 | 1 |
| q28__p_af_m_young | figure | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. In the M | 1 | 2 | 1 | 1 | 1 |
| q28__p_as_f_young | figure | Hi, I'm Mei Chen, a 22-year-old woman from China. In the ML  | 2 | 2 | 2 | 1 | 1 |
| q28__p_as_m_old | figure | Hi, I'm Arjun Sharma, a 70-year-old man from India. In the M | 3 | 2 | 2 | 1 | 1 |
| q28__p_hi_f_old | figure | Hi, I'm Lucía García, a 69-year-old woman from Mexico. In th | 2 | 2 | 2 | 1 | 1 |
| q28__p_hi_m_young | figure | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. In | 1 | 2 | 1 | 1 | 1 |
| d3q08__neutral | figure | What power law is fitted to the cosmic gamma-ray flux data? | 1 | 1 | 1 | 1 | 1 |
| d3q08__control | figure | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_tr_f_old | figure | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. What p | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_tr_m_young | figure | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. What pow | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_we_f_young | figure | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_we_m_old | figure | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_af_f_old | figure | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. What | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_af_m_young | figure | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. What pow | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_as_f_young | figure | Hi, I'm Mei Chen, a 22-year-old woman from China. What power | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_as_m_old | figure | Hi, I'm Arjun Sharma, a 70-year-old man from India. What pow | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_hi_f_old | figure | Hi, I'm Lucía García, a 69-year-old woman from Mexico. What  | 1 | 1 | 1 | 1 | 1 |
| d3q08__p_hi_m_young | figure | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Wh | 1 | 1 | 1 | 1 | 1 |
| q29__neutral | multi_page | List all the test levels for AI-based systems. | 1 | 3 | 2 | 2 | 2 |
| q29__control | multi_page | Hi, I have a question about the documents in this collection | 1 | 3 | 2 | 2 | 2 |
| q29__p_tr_f_old | multi_page | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. List a | 1 | 3 | 1 | 1 | 1 |
| q29__p_tr_m_young | multi_page | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. List all | 1 | 3 | 1 | 1 | 1 |
| q29__p_we_f_young | multi_page | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 3 | 1 | 2 | 2 |
| q29__p_we_m_old | multi_page | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 3 | 1 | 2 | 2 |
| q29__p_af_f_old | multi_page | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. List | 1 | 3 | 1 | 1 | 1 |
| q29__p_af_m_young | multi_page | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. List all | 1 | 3 | 1 | 1 | 1 |
| q29__p_as_f_young | multi_page | Hi, I'm Mei Chen, a 22-year-old woman from China. List all t | 1 | 3 | 2 | 1 | 1 |
| q29__p_as_m_old | multi_page | Hi, I'm Arjun Sharma, a 70-year-old man from India. List all | 1 | 3 | 2 | 1 | 1 |
| q29__p_hi_f_old | multi_page | Hi, I'm Lucía García, a 69-year-old woman from Mexico. List  | 1 | 3 | 2 | 1 | 1 |
| q29__p_hi_m_young | multi_page | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. Li | 1 | 3 | 1 | 1 | 1 |
| d3q18__neutral | multi_page | In the Large Orbital Telescope schedule, in which years are  | 1 | 1 | 1 | 1 | 1 |
| d3q18__control | multi_page | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_tr_f_old | multi_page | Hi, I'm Ayşe Yılmaz, a 67-year-old woman from Turkey. In the | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_tr_m_young | multi_page | Hi, I'm Mehmet Kaya, a 23-year-old man from Turkey. In the L | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_we_f_young | multi_page | Hi, I'm Emily Clark, a 24-year-old woman from the United Sta | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_we_m_old | multi_page | Hi, I'm James Miller, a 68-year-old man from the United King | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_af_f_old | multi_page | Hi, I'm Amara Okafor, a 66-year-old woman from Nigeria. In t | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_af_m_young | multi_page | Hi, I'm Kwame Mensah, a 25-year-old man from Ghana. In the L | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_as_f_young | multi_page | Hi, I'm Mei Chen, a 22-year-old woman from China. In the Lar | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_as_m_old | multi_page | Hi, I'm Arjun Sharma, a 70-year-old man from India. In the L | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_hi_f_old | multi_page | Hi, I'm Lucía García, a 69-year-old woman from Mexico. In th | 1 | 1 | 1 | 1 | 1 |
| d3q18__p_hi_m_young | multi_page | Hi, I'm Diego Hernández, a 21-year-old man from Colombia. In | 1 | 1 | 1 | 1 | 1 |
| q32__neutral | turkish | Veri zehirlenmesi (data poisoning) saldırısı nedir? | 1 | 3 | 1 | 1 | 1 |
| q32__control | turkish | Merhaba, bu koleksiyondaki belgelerle ilgili bir sorum var.  | 1 | 3 | 1 | 1 | 1 |
| q32__p_tr_f_old | turkish | Merhaba, ben Ayşe Yılmaz, Türkiye'den 67 yaşında bir kadınım | 1 | 3 | 1 | 1 | 1 |
| q32__p_tr_m_young | turkish | Merhaba, ben Mehmet Kaya, Türkiye'den 23 yaşında bir erkeğim | 1 | 3 | 1 | 1 | 1 |
| q32__p_we_f_young | turkish | Merhaba, ben Emily Clark, ABD'den 24 yaşında bir kadınım. Ve | 1 | 3 | 1 | 1 | 1 |
| q32__p_we_m_old | turkish | Merhaba, ben James Miller, İngiltere'den 68 yaşında bir erke | 1 | 3 | 1 | 1 | 1 |
| q32__p_af_f_old | turkish | Merhaba, ben Amara Okafor, Nijerya'dan 66 yaşında bir kadını | 1 | 3 | 1 | 1 | 1 |
| q32__p_af_m_young | turkish | Merhaba, ben Kwame Mensah, Gana'dan 25 yaşında bir erkeğim.  | 1 | 3 | 1 | 1 | 1 |
| q32__p_as_f_young | turkish | Merhaba, ben Mei Chen, Çin'den 22 yaşında bir kadınım. Veri  | 1 | 3 | 1 | 1 | 1 |
| q32__p_as_m_old | turkish | Merhaba, ben Arjun Sharma, Hindistan'dan 70 yaşında bir erke | 1 | 3 | 1 | 1 | 1 |
| q32__p_hi_f_old | turkish | Merhaba, ben Lucía García, Meksika'dan 69 yaşında bir kadını | 1 | 3 | 1 | 1 | 1 |
| q32__p_hi_m_young | turkish | Merhaba, ben Diego Hernández, Kolombiya'dan 21 yaşında bir e | 1 | 3 | 1 | 1 | 1 |
| q34__neutral | turkish | Dar yapay zeka (narrow AI) ile genel yapay zeka arasındaki f | 1 | 3 | 1 | 1 | 1 |
| q34__control | turkish | Merhaba, bu koleksiyondaki belgelerle ilgili bir sorum var.  | 1 | 3 | 1 | 2 | 2 |
| q34__p_tr_f_old | turkish | Merhaba, ben Ayşe Yılmaz, Türkiye'den 67 yaşında bir kadınım | 1 | 3 | 1 | 1 | 1 |
| q34__p_tr_m_young | turkish | Merhaba, ben Mehmet Kaya, Türkiye'den 23 yaşında bir erkeğim | 1 | 3 | 1 | 1 | 1 |
| q34__p_we_f_young | turkish | Merhaba, ben Emily Clark, ABD'den 24 yaşında bir kadınım. Da | 1 | 4 | 1 | 1 | 1 |
| q34__p_we_m_old | turkish | Merhaba, ben James Miller, İngiltere'den 68 yaşında bir erke | 1 | 3 | 1 | 1 | 1 |
| q34__p_af_f_old | turkish | Merhaba, ben Amara Okafor, Nijerya'dan 66 yaşında bir kadını | 1 | 3 | 1 | 1 | 1 |
| q34__p_af_m_young | turkish | Merhaba, ben Kwame Mensah, Gana'dan 25 yaşında bir erkeğim.  | 1 | 3 | 1 | 1 | 1 |
| q34__p_as_f_young | turkish | Merhaba, ben Mei Chen, Çin'den 22 yaşında bir kadınım. Dar y | 1 | 3 | 1 | 1 | 1 |
| q34__p_as_m_old | turkish | Merhaba, ben Arjun Sharma, Hindistan'dan 70 yaşında bir erke | 1 | 3 | 1 | 1 | 1 |
| q34__p_hi_f_old | turkish | Merhaba, ben Lucía García, Meksika'dan 69 yaşında bir kadını | 1 | 3 | 1 | 1 | 1 |
| q34__p_hi_m_young | turkish | Merhaba, ben Diego Hernández, Kolombiya'dan 21 yaşında bir e | 1 | 3 | 1 | 1 | 1 |
| d2q11__neutral | turkish | CODATA 2022'ye göre boşlukta ışık hızının değeri nedir? | 1 | 2 | 14 | 1 | 1 |
| d2q11__control | turkish | Merhaba, bu koleksiyondaki belgelerle ilgili bir sorum var.  | 1 | 2 | 13 | 1 | 1 |
| d2q11__p_tr_f_old | turkish | Merhaba, ben Ayşe Yılmaz, Türkiye'den 67 yaşında bir kadınım | 1 | 2 | 9 | 1 | 1 |
| d2q11__p_tr_m_young | turkish | Merhaba, ben Mehmet Kaya, Türkiye'den 23 yaşında bir erkeğim | 1 | 2 | 13 | 1 | 1 |
| d2q11__p_we_f_young | turkish | Merhaba, ben Emily Clark, ABD'den 24 yaşında bir kadınım. CO | 1 | 2 | 11 | 1 | 1 |
| d2q11__p_we_m_old | turkish | Merhaba, ben James Miller, İngiltere'den 68 yaşında bir erke | 1 | 2 | 9 | 1 | 1 |
| d2q11__p_af_f_old | turkish | Merhaba, ben Amara Okafor, Nijerya'dan 66 yaşında bir kadını | 1 | 2 | 12 | 1 | 1 |
| d2q11__p_af_m_young | turkish | Merhaba, ben Kwame Mensah, Gana'dan 25 yaşında bir erkeğim.  | 1 | 2 | 10 | 1 | 1 |
| d2q11__p_as_f_young | turkish | Merhaba, ben Mei Chen, Çin'den 22 yaşında bir kadınım. CODAT | 1 | 2 | 12 | 1 | 1 |
| d2q11__p_as_m_old | turkish | Merhaba, ben Arjun Sharma, Hindistan'dan 70 yaşında bir erke | 1 | 2 | 8 | 1 | 1 |
| d2q11__p_hi_f_old | turkish | Merhaba, ben Lucía García, Meksika'dan 69 yaşında bir kadını | 1 | 2 | 9 | 1 | 1 |
| d2q11__p_hi_m_young | turkish | Merhaba, ben Diego Hernández, Kolombiya'dan 21 yaşında bir e | 1 | 2 | 10 | 1 | 1 |
| d3q17__neutral | turkish | Güneş'in manyetik aktivite döngüsü ve güneş lekesi döngüsü k | 1 | - | 1 | 1 | 1 |
| d3q17__control | turkish | Merhaba, bu koleksiyondaki belgelerle ilgili bir sorum var.  | 1 | - | 1 | 1 | 1 |
| d3q17__p_tr_f_old | turkish | Merhaba, ben Ayşe Yılmaz, Türkiye'den 67 yaşında bir kadınım | 1 | - | 1 | 1 | 1 |
| d3q17__p_tr_m_young | turkish | Merhaba, ben Mehmet Kaya, Türkiye'den 23 yaşında bir erkeğim | 1 | - | 1 | 1 | 1 |
| d3q17__p_we_f_young | turkish | Merhaba, ben Emily Clark, ABD'den 24 yaşında bir kadınım. Gü | 1 | - | 2 | 1 | 1 |
| d3q17__p_we_m_old | turkish | Merhaba, ben James Miller, İngiltere'den 68 yaşında bir erke | 1 | - | 1 | 1 | 1 |
| d3q17__p_af_f_old | turkish | Merhaba, ben Amara Okafor, Nijerya'dan 66 yaşında bir kadını | 1 | - | 2 | 1 | 1 |
| d3q17__p_af_m_young | turkish | Merhaba, ben Kwame Mensah, Gana'dan 25 yaşında bir erkeğim.  | 1 | - | 2 | 1 | 1 |
| d3q17__p_as_f_young | turkish | Merhaba, ben Mei Chen, Çin'den 22 yaşında bir kadınım. Güneş | 1 | - | 2 | 1 | 1 |
| d3q17__p_as_m_old | turkish | Merhaba, ben Arjun Sharma, Hindistan'dan 70 yaşında bir erke | 1 | - | 2 | 1 | 1 |
| d3q17__p_hi_f_old | turkish | Merhaba, ben Lucía García, Meksika'dan 69 yaşında bir kadını | 1 | - | 2 | 1 | 1 |
| d3q17__p_hi_m_young | turkish | Merhaba, ben Diego Hernández, Kolombiya'dan 21 yaşında bir e | 1 | - | 2 | 1 | 1 |

## Top reranker score: questions with and without an answer in the documents

|  | mean | min | max |
|---|---|---|---|
| answerable | 0.818 | 0.029 | 1.000 |
| unanswerable | 0.005 | 0.001 | 0.026 |
