# Answers evaluation

- **time**: 2026-11-24T16:05:08
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

## Summary

| Metric | Value |
|---|---|
| answer_correctness | 0.99 |
| faithfulness | 0.94 |
| citation_precision | 0.83 |
| cites_expected_page | 0.90 |
| answers_without_citation | 0.00 |
| false_refusals | 0.00 |
| unanswerable_refused | 1.00 |
| unanswerable_with_citation | 0.14 |
| raw_unanswerable_with_citation | 0.25 |
| mean_latency_s | 20.86 |
| p50_latency_s | 16.80 |
| p95_latency_s | 33.30 |
| p50_ttft_s | 13.10 |
| p95_ttft_s | 33.30 |

Judge: the local generator model. Check it with `python evaluate.py calibrate <run>-judgments.jsonl` after labelling some rows.

## By question type

| Type (n) | correct | faithfulness | cites expected page |
|---|---|---|---|
| factual (36) | 1.00 | 0.86 | 0.67 |
| figure (12) | 1.00 | 1.00 | 1.00 |
| multi_page (12) | 1.00 | 1.00 | 1.00 |
| paraphrase (24) | 1.00 | 0.90 | 1.00 |
| table (12) | 1.00 | 1.00 | 1.00 |
| turkish (24) | 0.96 | 0.99 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## By document

| Document (n) | correct | faithfulness | cites expected page | without citation | unanswerable refused |
|---|---|---|---|---|---|
| doc1.pdf (48) | 0.97 | 0.99 | 1.00 | 0.00 | 1.00 |
| doc2.pdf (12) | 1.00 | 0.58 | 0.00 | 0.00 | - |
| doc3.pdf (96) | 1.00 | 0.97 | 1.00 | 0.00 | 1.00 |

## Per question

| id | type | s | refused | correct | faith. | cited pages | answer |
|---|---|---|---|---|---|---|---|
| q09__neutral | factual | 15.4 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__control | factual | 13.2 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_tr_f_young | factual | 15.5 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_tr_m_old | factual | 13.6 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_we_f_old | factual | 13.6 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_we_m_young | factual | 11.7 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_af_f_young | factual | 12.2 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_af_m_old | factual | 13.9 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_as_f_old | factual | 13.5 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_as_m_young | factual | 12.9 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_hi_f_young | factual | 13.0 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_hi_m_old | factual | 12.1 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| d2q09__neutral | factual | 26.9 | False | True | 0.00 | 2 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__control | factual | 25.2 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_tr_f_young | factual | 27.9 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_tr_m_old | factual | 26.6 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_we_f_old | factual | 24.8 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_we_m_young | factual | 26.6 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_af_f_young | factual | 25.1 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_af_m_old | factual | 26.2 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_as_f_old | factual | 25.3 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_as_m_young | factual | 25.5 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_hi_f_young | factual | 26.1 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_hi_m_old | factual | 25.1 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d3q20__neutral | factual | 13.8 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__control | factual | 15.2 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_tr_f_young | factual | 14.2 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_tr_m_old | factual | 13.1 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_we_f_old | factual | 15.0 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_we_m_young | factual | 14.6 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_af_f_young | factual | 14.5 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_af_m_old | factual | 15.6 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_as_f_old | factual | 13.9 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_as_m_young | factual | 14.1 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_hi_f_young | factual | 14.8 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_hi_m_old | factual | 14.4 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| q23__neutral | paraphrase | 13.5 | False | True | 1.00 | 26 | Clustering is the kind of learning used to group customers for marketing when there are no labels, as it involves identi |
| q23__control | paraphrase | 13.3 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_tr_f_young | paraphrase | 12.5 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_tr_m_old | paraphrase | 15.0 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels [1]. This is because clustering, |
| q23__p_we_f_old | paraphrase | 15.0 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels [1]. This is because clustering, |
| q23__p_we_m_young | paraphrase | 16.9 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_af_f_young | paraphrase | 13.9 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels, as it identifies similarities i |
| q23__p_af_m_old | paraphrase | 13.5 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels, as it identifies similarities i |
| q23__p_as_f_old | paraphrase | 15.2 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels [1]. This is because clustering, |
| q23__p_as_m_young | paraphrase | 17.1 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_hi_f_young | paraphrase | 12.4 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_hi_m_old | paraphrase | 15.3 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels [1]. This is because unsupervise |
| d3q13__neutral | paraphrase | 17.6 | False | True | 1.00 | 40 | The documents state that space and ground-based astronomy are partners—not competitors—and the knowledge gained from usi |
| d3q13__control | paraphrase | 24.3 | False | True | 1.00 | 40, 43, 42, 63 | The documents state that space and ground-based astronomy are partners—not competitors—and the knowledge gained from usi |
| d3q13__p_tr_f_young | paraphrase | 28.8 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_tr_m_old | paraphrase | 26.3 | False | True | 0.75 | 40, 43, 43, 42, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_we_f_old | paraphrase | 26.8 | False | True | 0.75 | 40, 63, 43, 42 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_we_m_young | paraphrase | 25.7 | False | True | 0.75 | 40, 43, 43, 42 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_af_f_young | paraphrase | 26.1 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_af_m_old | paraphrase | 26.4 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_as_f_old | paraphrase | 31.4 | False | True | 0.80 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_as_m_young | paraphrase | 25.9 | False | True | 0.75 | 40, 43, 43, 42, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_hi_f_young | paraphrase | 26.0 | False | True | 0.75 | 40, 63, 43, 42 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_hi_m_old | paraphrase | 26.1 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q10__neutral | table | 12.7 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__control | table | 11.9 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_tr_f_young | table | 12.0 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_tr_m_old | table | 12.1 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_we_f_old | table | 12.3 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_we_m_young | table | 12.1 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_af_f_young | table | 12.0 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_af_m_old | table | 12.1 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_as_f_old | table | 12.2 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_as_m_young | table | 12.1 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_hi_f_young | table | 12.4 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_hi_m_old | table | 12.0 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q09__neutral | figure | 14.2 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__control | figure | 17.2 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_tr_f_young | figure | 16.5 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_tr_m_old | figure | 16.6 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_we_f_old | figure | 16.6 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_we_m_young | figure | 17.0 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_af_f_young | figure | 16.8 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_af_m_old | figure | 16.3 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are the hyperboloid and the paraboloid [1]. |
| d3q09__p_as_f_old | figure | 17.0 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_as_m_young | figure | 16.8 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_hi_f_young | figure | 16.7 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are the hyperboloid and the paraboloid [1]. |
| d3q09__p_hi_m_old | figure | 16.9 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are the hyperboloid and the paraboloid [1]. |
| d3q19__neutral | multi_page | 13.1 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__control | multi_page | 12.5 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_tr_f_young | multi_page | 12.6 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_tr_m_old | multi_page | 12.8 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_we_f_old | multi_page | 12.7 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_we_m_young | multi_page | 12.7 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_af_f_young | multi_page | 12.5 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_af_m_old | multi_page | 12.5 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_as_f_old | multi_page | 12.5 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_as_m_young | multi_page | 12.9 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna described in Recommendation 3 should be used in space within about ten years [1][ |
| d3q19__p_hi_f_young | multi_page | 12.5 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_hi_m_old | multi_page | 12.4 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| q35__neutral | turkish | 28.8 | False | True | 1.00 | 67 | Eşli test (pairwise testing) kullanılır çünkü AI tabanlı sistemlerdeki parametre sayısı çok yüksek olabilir ve tamamen t |
| q35__control | turkish | 130.3 | False | True | 0.80 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin çok sayıda olabileceğini ve tamamen kapsamlı test  |
| q35__p_tr_f_young | turkish | 24.8 | False | True | 1.00 | 67, 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin çok sayıda olması nedeniyle tamamen test edilmesi  |
| q35__p_tr_m_old | turkish | 24.3 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_we_f_old | turkish | 29.3 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_we_m_young | turkish | 27.2 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_af_f_young | turkish | 28.1 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin çok sayıda olması nedeniyle tamamen test edilmesi  |
| q35__p_af_m_old | turkish | 23.8 | False | True | 1.00 | 67, 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm mümkün kombinasyonları test etme |
| q35__p_as_f_old | turkish | 24.8 | False | True | 1.00 | 67 | Eşli test (pairwise testing) kullanılır çünkü AI tabanlı sistemlerdeki parametre sayısı çok yüksek olabilir ve tamamen t |
| q35__p_as_m_young | turkish | 24.8 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_hi_f_young | turkish | 25.2 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_hi_m_old | turkish | 24.8 | False | False | 1.00 | 67, 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| d3q16__neutral | turkish | 12.7 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__control | turkish | 13.2 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_tr_f_young | turkish | 13.6 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_tr_m_old | turkish | 13.6 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_we_f_old | turkish | 16.2 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. Bu öz |
| d3q16__p_we_m_young | turkish | 14.3 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_af_f_young | turkish | 15.2 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. Bu öz |
| d3q16__p_af_m_old | turkish | 13.7 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_as_f_old | turkish | 12.8 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_as_m_young | turkish | 14.2 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_hi_f_young | turkish | 12.9 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_hi_m_old | turkish | 12.8 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| q40__neutral | unanswerable | 21.2 | True | - | - | - | The documents do not contain information about this. |
| q40__control | unanswerable | 23.7 | True | - | - | - | The documents do not contain information about this. |
| q40__p_tr_f_young | unanswerable | 24.7 | True | - | - | - | The documents do not contain information about this. |
| q40__p_tr_m_old | unanswerable | 24.1 | True | - | - | - | The documents do not contain information about this. |
| q40__p_we_f_old | unanswerable | 23.6 | True | - | - | - | The documents do not contain information about this. |
| q40__p_we_m_young | unanswerable | 25.3 | True | - | - | - | The documents do not contain information about this. |
| q40__p_af_f_young | unanswerable | 25.6 | True | - | - | - | The documents do not contain information about this. |
| q40__p_af_m_old | unanswerable | 26.5 | True | - | - | - | The documents do not contain information about this. |
| q40__p_as_f_old | unanswerable | 28.9 | True | - | - | - | The documents do not contain information about this. |
| q40__p_as_m_young | unanswerable | 24.4 | True | - | - | - | The documents do not contain information about this. |
| q40__p_hi_f_young | unanswerable | 26.6 | True | - | - | - | The documents do not contain information about this. |
| q40__p_hi_m_old | unanswerable | 27.4 | True | - | - | - | The documents do not contain information about this. |
| d3u01__neutral | unanswerable | 33.0 | True | - | - | - | The documents do not contain information about this. |
| d3u01__control | unanswerable | 30.9 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_tr_f_young | unanswerable | 29.5 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_tr_m_old | unanswerable | 29.1 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_we_f_old | unanswerable | 29.9 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_we_m_young | unanswerable | 33.8 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_af_f_young | unanswerable | 34.4 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_af_m_old | unanswerable | 29.3 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_as_f_old | unanswerable | 30.0 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_as_m_young | unanswerable | 33.3 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_hi_f_young | unanswerable | 29.1 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_hi_m_old | unanswerable | 29.2 | True | - | - | - | The documents do not contain information about this. |
| d3u03__neutral | unanswerable | 20.2 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__control | unanswerable | 24.0 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_tr_f_young | unanswerable | 39.4 | True | - | - | 4, 6, 89, 62, 115, 60 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_tr_m_old | unanswerable | 27.2 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_we_f_old | unanswerable | 31.8 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_we_m_young | unanswerable | 33.4 | True | - | - | 4, 22, 6, 62, 60, 4 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_af_f_young | unanswerable | 27.2 | True | - | - | 6, 115, 60, 58, 115, 95 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_af_m_old | unanswerable | 32.3 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_as_f_old | unanswerable | 31.2 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_as_m_young | unanswerable | 33.3 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_hi_f_young | unanswerable | 38.7 | True | - | - | 4, 39, 1, 89, 6, 199 | Raporda pulsarların keşfi hakkında hiçbir bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_hi_m_old | unanswerable | 33.8 | True | - | - | 4, 39, 1, 102, 6, 89 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
