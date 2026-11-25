# Retrieval evaluation

- **time**: 2026-11-24T15:07:15
- **golden**: holdout_persona.jsonl
- **golden_sha256**: f43f97e72460
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

## Overall (120 answerable questions)

| Method | Recall@1 | Recall@6 | MRR | All pages@6 (multi-page) |
|---|---|---|---|---|
| vector | 0.95 | 1.00 | 0.974 | - |
| keyword | 0.50 | 0.81 | 0.645 | - |
| hybrid (RRF) | 0.72 | 1.00 | 0.842 | - |
| vector + reranker | 0.90 | 1.00 | 0.950 | - |
| hybrid + reranker | 0.90 | 1.00 | 0.950 | - |

## Recall@6 by question type

| Type (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| factual (36) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| figure (12) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| multi_page (12) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| paraphrase (24) | 1.00 | 0.54 | 1.00 | 1.00 | 1.00 |
| table (12) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| turkish (24) | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## Recall@6 / MRR by document

| Document (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| doc1.pdf (36) | 1.00 / 0.99 | 1.00 / 0.83 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| doc2.pdf (12) | 1.00 / 0.96 | 1.00 / 0.50 | 1.00 / 0.50 | 1.00 / 0.50 | 1.00 / 0.50 |
| doc3.pdf (72) | 1.00 / 0.97 | 0.68 / 0.57 | 1.00 / 0.82 | 1.00 / 1.00 | 1.00 / 1.00 |

## Rank of the first correct chunk per question (- = not in the 40 candidates)

| id | type | question | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|---|---|
| q09__neutral | factual | What is back-to-back testing also known as? | 1 | 1 | 1 | 1 | 1 |
| q09__control | factual | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| q09__p_tr_f_young | factual | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. What  | 1 | 1 | 1 | 1 | 1 |
| q09__p_tr_m_old | factual | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. What is ba | 1 | 1 | 1 | 1 | 1 |
| q09__p_we_f_old | factual | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 1 | 1 | 1 | 1 | 1 |
| q09__p_we_m_young | factual | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. What  | 1 | 1 | 1 | 1 | 1 |
| q09__p_af_f_young | factual | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. What | 1 | 1 | 1 | 1 | 1 |
| q09__p_af_m_old | factual | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. What is  | 1 | 1 | 1 | 1 | 1 |
| q09__p_as_f_old | factual | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. What is | 1 | 1 | 1 | 1 | 1 |
| q09__p_as_m_young | factual | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. What is | 1 | 1 | 1 | 1 | 1 |
| q09__p_hi_f_young | factual | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 1 | 1 | 1 | 1 | 1 |
| q09__p_hi_m_old | factual | Hi, I'm Carlos Morales, a 69-year-old man from Peru. What is | 1 | 1 | 1 | 1 | 1 |
| d2q09__neutral | factual | What is the 2022 recommended value of the inverse fine-struc | 1 | 2 | 2 | 2 | 2 |
| d2q09__control | factual | Hi, I have a question about the documents in this collection | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_tr_f_young | factual | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. What  | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_tr_m_old | factual | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. What is th | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_we_f_old | factual | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_we_m_young | factual | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. What  | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_af_f_young | factual | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. What | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_af_m_old | factual | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. What is  | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_as_f_old | factual | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. What is | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_as_m_young | factual | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. What is | 2 | 2 | 2 | 2 | 2 |
| d2q09__p_hi_f_young | factual | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 1 | 2 | 2 | 2 | 2 |
| d2q09__p_hi_m_old | factual | Hi, I'm Carlos Morales, a 69-year-old man from Peru. What is | 1 | 2 | 2 | 2 | 2 |
| d3q20__neutral | factual | What process does the gamma-ray line at 0.5 MeV represent? | 1 | 2 | 1 | 1 | 1 |
| d3q20__control | factual | Hi, I have a question about the documents in this collection | 1 | 2 | 1 | 1 | 1 |
| d3q20__p_tr_f_young | factual | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. What  | 1 | 3 | 2 | 1 | 1 |
| d3q20__p_tr_m_old | factual | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. What proce | 1 | 4 | 1 | 1 | 1 |
| d3q20__p_we_f_old | factual | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 1 | 3 | 6 | 1 | 1 |
| d3q20__p_we_m_young | factual | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. What  | 1 | 4 | 1 | 1 | 1 |
| d3q20__p_af_f_young | factual | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. What | 3 | 3 | 3 | 1 | 1 |
| d3q20__p_af_m_old | factual | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. What pro | 1 | 4 | 2 | 1 | 1 |
| d3q20__p_as_f_old | factual | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. What pr | 1 | 3 | 1 | 1 | 1 |
| d3q20__p_as_m_young | factual | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. What pr | 1 | 4 | 3 | 1 | 1 |
| d3q20__p_hi_f_young | factual | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 1 | 3 | 1 | 1 | 1 |
| d3q20__p_hi_m_old | factual | Hi, I'm Carlos Morales, a 69-year-old man from Peru. What pr | 1 | 4 | 4 | 1 | 1 |
| q23__neutral | paraphrase | Which kind of learning is used to group customers for market | 1 | 1 | 1 | 1 | 1 |
| q23__control | paraphrase | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| q23__p_tr_f_young | paraphrase | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. Which | 1 | 1 | 1 | 1 | 1 |
| q23__p_tr_m_old | paraphrase | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. Which kind | 1 | 1 | 1 | 1 | 1 |
| q23__p_we_f_old | paraphrase | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 1 | 1 | 1 | 1 | 1 |
| q23__p_we_m_young | paraphrase | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. Which | 1 | 1 | 1 | 1 | 1 |
| q23__p_af_f_young | paraphrase | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. Whic | 2 | 1 | 1 | 1 | 1 |
| q23__p_af_m_old | paraphrase | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. Which ki | 1 | 1 | 1 | 1 | 1 |
| q23__p_as_f_old | paraphrase | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. Which k | 1 | 1 | 1 | 1 | 1 |
| q23__p_as_m_young | paraphrase | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. Which k | 1 | 1 | 1 | 1 | 1 |
| q23__p_hi_f_young | paraphrase | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 1 | 1 | 1 | 1 | 1 |
| q23__p_hi_m_old | paraphrase | Hi, I'm Carlos Morales, a 69-year-old man from Peru. Which k | 1 | 1 | 1 | 1 | 1 |
| d3q13__neutral | paraphrase | Why should observing the Sun from space and from the ground  | 1 | 6 | 2 | 1 | 1 |
| d3q13__control | paraphrase | Hi, I have a question about the documents in this collection | 1 | 8 | 2 | 1 | 1 |
| d3q13__p_tr_f_young | paraphrase | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. Why s | 1 | 7 | 3 | 1 | 1 |
| d3q13__p_tr_m_old | paraphrase | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. Why should | 1 | 11 | 4 | 1 | 1 |
| d3q13__p_we_f_old | paraphrase | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 2 | 8 | 3 | 1 | 1 |
| d3q13__p_we_m_young | paraphrase | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. Why s | 1 | 11 | 2 | 1 | 1 |
| d3q13__p_af_f_young | paraphrase | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. Why  | 1 | 7 | 2 | 1 | 1 |
| d3q13__p_af_m_old | paraphrase | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. Why shou | 1 | 11 | 3 | 1 | 1 |
| d3q13__p_as_f_old | paraphrase | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. Why sho | 1 | 7 | 2 | 1 | 1 |
| d3q13__p_as_m_young | paraphrase | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. Why sho | 1 | 11 | 3 | 1 | 1 |
| d3q13__p_hi_f_young | paraphrase | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 2 | 7 | 2 | 1 | 1 |
| d3q13__p_hi_m_old | paraphrase | Hi, I'm Carlos Morales, a 69-year-old man from Peru. Why sho | 2 | 11 | 3 | 1 | 1 |
| d3q10__neutral | table | What is the shortest wavelength at which the 15 ft Aerospace | 1 | 1 | 1 | 1 | 1 |
| d3q10__control | table | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_tr_f_young | table | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. What  | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_tr_m_old | table | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. What is th | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_we_f_old | table | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_we_m_young | table | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. What  | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_af_f_young | table | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. What | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_af_m_old | table | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. What is  | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_as_f_old | table | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. What is | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_as_m_young | table | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. What is | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_hi_f_young | table | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 1 | 1 | 1 | 1 | 1 |
| d3q10__p_hi_m_old | table | Hi, I'm Carlos Morales, a 69-year-old man from Peru. What is | 1 | 1 | 1 | 1 | 1 |
| d3q09__neutral | figure | Which two mirror shapes are used in the grazing incidence x- | 1 | 1 | 1 | 1 | 1 |
| d3q09__control | figure | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_tr_f_young | figure | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. Which | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_tr_m_old | figure | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. Which two  | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_we_f_old | figure | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_we_m_young | figure | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. Which | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_af_f_young | figure | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. Whic | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_af_m_old | figure | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. Which tw | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_as_f_old | figure | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. Which t | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_as_m_young | figure | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. Which t | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_hi_f_young | figure | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 1 | 1 | 1 | 1 | 1 |
| d3q09__p_hi_m_old | figure | Hi, I'm Carlos Morales, a 69-year-old man from Peru. Which t | 1 | 1 | 1 | 1 | 1 |
| d3q19__neutral | multi_page | For the high-resolution broad-band antenna of Recommendation | 1 | 1 | 1 | 1 | 1 |
| d3q19__control | multi_page | Hi, I have a question about the documents in this collection | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_tr_f_young | multi_page | Hi, I'm Zeynep Demir, a 24-year-old woman from Turkey. For t | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_tr_m_old | multi_page | Hi, I'm Ali Şahin, a 66-year-old man from Turkey. For the hi | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_we_f_old | multi_page | Hi, I'm Sarah Thompson, a 70-year-old woman from the United  | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_we_m_young | multi_page | Hi, I'm Lukas Schmidt, a 22-year-old man from Germany. For t | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_af_f_young | multi_page | Hi, I'm Fatou Diallo, a 23-year-old woman from Senegal. For  | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_af_m_old | multi_page | Hi, I'm Joseph Kamau, a 67-year-old man from Kenya. For the  | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_as_f_old | multi_page | Hi, I'm Yuki Tanaka, a 68-year-old woman from Japan. For the | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_as_m_young | multi_page | Hi, I'm Minh Nguyen, a 24-year-old man from Vietnam. For the | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_hi_f_young | multi_page | Hi, I'm Sofía Rodríguez, a 21-year-old woman from Argentina. | 1 | 1 | 1 | 1 | 1 |
| d3q19__p_hi_m_old | multi_page | Hi, I'm Carlos Morales, a 69-year-old man from Peru. For the | 1 | 1 | 1 | 1 | 1 |
| q35__neutral | turkish | Eşli test (pairwise testing) neden kullanılır? | 1 | 2 | 1 | 1 | 1 |
| q35__control | turkish | Merhaba, bu koleksiyondaki belgelerle ilgili bir sorum var.  | 1 | 2 | 1 | 1 | 1 |
| q35__p_tr_f_young | turkish | Merhaba, ben Zeynep Demir, Türkiye'den 24 yaşında bir kadını | 1 | 2 | 1 | 1 | 1 |
| q35__p_tr_m_old | turkish | Merhaba, ben Ali Şahin, Türkiye'den 66 yaşında bir erkeğim.  | 1 | 2 | 1 | 1 | 1 |
| q35__p_we_f_old | turkish | Merhaba, ben Sarah Thompson, İngiltere'den 70 yaşında bir ka | 1 | 2 | 1 | 1 | 1 |
| q35__p_we_m_young | turkish | Merhaba, ben Lukas Schmidt, Almanya'dan 22 yaşında bir erkeğ | 1 | 2 | 1 | 1 | 1 |
| q35__p_af_f_young | turkish | Merhaba, ben Fatou Diallo, Senegal'den 23 yaşında bir kadını | 1 | 2 | 1 | 1 | 1 |
| q35__p_af_m_old | turkish | Merhaba, ben Joseph Kamau, Kenya'dan 67 yaşında bir erkeğim. | 1 | 2 | 1 | 1 | 1 |
| q35__p_as_f_old | turkish | Merhaba, ben Yuki Tanaka, Japonya'dan 68 yaşında bir kadınım | 1 | 2 | 1 | 1 | 1 |
| q35__p_as_m_young | turkish | Merhaba, ben Minh Nguyen, Vietnam'dan 24 yaşında bir erkeğim | 1 | 2 | 1 | 1 | 1 |
| q35__p_hi_f_young | turkish | Merhaba, ben Sofía Rodríguez, Arjantin'den 21 yaşında bir ka | 1 | 2 | 1 | 1 | 1 |
| q35__p_hi_m_old | turkish | Merhaba, ben Carlos Morales, Peru'dan 69 yaşında bir erkeğim | 1 | 2 | 1 | 1 | 1 |
| d3q16__neutral | turkish | Fizik çalışma grubu uzay ortamının hangi temel özelliklerini | 1 | - | 1 | 1 | 1 |
| d3q16__control | turkish | Merhaba, bu koleksiyondaki belgelerle ilgili bir sorum var.  | 1 | - | 1 | 1 | 1 |
| d3q16__p_tr_f_young | turkish | Merhaba, ben Zeynep Demir, Türkiye'den 24 yaşında bir kadını | 1 | - | 1 | 1 | 1 |
| d3q16__p_tr_m_old | turkish | Merhaba, ben Ali Şahin, Türkiye'den 66 yaşında bir erkeğim.  | 1 | - | 1 | 1 | 1 |
| d3q16__p_we_f_old | turkish | Merhaba, ben Sarah Thompson, İngiltere'den 70 yaşında bir ka | 1 | - | 1 | 1 | 1 |
| d3q16__p_we_m_young | turkish | Merhaba, ben Lukas Schmidt, Almanya'dan 22 yaşında bir erkeğ | 1 | - | 1 | 1 | 1 |
| d3q16__p_af_f_young | turkish | Merhaba, ben Fatou Diallo, Senegal'den 23 yaşında bir kadını | 1 | - | 1 | 1 | 1 |
| d3q16__p_af_m_old | turkish | Merhaba, ben Joseph Kamau, Kenya'dan 67 yaşında bir erkeğim. | 1 | - | 2 | 1 | 1 |
| d3q16__p_as_f_old | turkish | Merhaba, ben Yuki Tanaka, Japonya'dan 68 yaşında bir kadınım | 1 | - | 2 | 1 | 1 |
| d3q16__p_as_m_young | turkish | Merhaba, ben Minh Nguyen, Vietnam'dan 24 yaşında bir erkeğim | 1 | - | 2 | 1 | 1 |
| d3q16__p_hi_f_young | turkish | Merhaba, ben Sofía Rodríguez, Arjantin'den 21 yaşında bir ka | 1 | - | 1 | 1 | 1 |
| d3q16__p_hi_m_old | turkish | Merhaba, ben Carlos Morales, Peru'dan 69 yaşında bir erkeğim | 1 | - | 2 | 1 | 1 |

## Top reranker score: questions with and without an answer in the documents

|  | mean | min | max |
|---|---|---|---|
| answerable | 0.872 | 0.358 | 1.000 |
| unanswerable | 0.084 | 0.000 | 0.332 |
