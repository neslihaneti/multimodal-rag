# Answers evaluation

- **time**: 2026-11-24T14:25:35
- **golden**: holdout_persona.jsonl
- **golden_sha256**: f43f97e72460
- **indexed_documents**: 3
- **indexed_chunks**: 1164
- **embedder**: BAAI/bge-m3
- **reranker**: BAAI/bge-reranker-v2-m3
- **generator**: Qwen/Qwen3-VL-4B-Instruct
- **prompt_sha256**: 2856d18117b9
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
| citation_precision | 0.84 |
| cites_expected_page | 0.91 |
| answers_without_citation | 0.00 |
| false_refusals | 0.00 |
| unanswerable_refused | 1.00 |
| unanswerable_with_citation | 0.17 |
| raw_unanswerable_with_citation | 0.28 |
| mean_latency_s | 19.97 |
| p50_latency_s | 15.90 |
| p95_latency_s | 31.70 |
| p50_ttft_s | 12.50 |
| p95_ttft_s | 31.10 |

Judge: the local generator model. Check it with `python evaluate.py calibrate <run>-judgments.jsonl` after labelling some rows.

## By question type

| Type (n) | correct | faithfulness | cites expected page |
|---|---|---|---|
| factual (36) | 1.00 | 0.86 | 0.69 |
| figure (12) | 1.00 | 1.00 | 1.00 |
| multi_page (12) | 1.00 | 1.00 | 1.00 |
| paraphrase (24) | 1.00 | 0.91 | 1.00 |
| table (12) | 1.00 | 1.00 | 1.00 |
| turkish (24) | 0.96 | 0.99 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## By document

| Document (n) | correct | faithfulness | cites expected page | without citation | unanswerable refused |
|---|---|---|---|---|---|
| doc1.pdf (48) | 0.97 | 0.99 | 1.00 | 0.00 | 1.00 |
| doc2.pdf (12) | 1.00 | 0.58 | 0.08 | 0.00 | - |
| doc3.pdf (96) | 1.00 | 0.97 | 1.00 | 0.00 | 1.00 |

## Per question

| id | type | s | refused | correct | faith. | cited pages | answer |
|---|---|---|---|---|---|---|---|
| q09__neutral | factual | 17.6 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__control | factual | 10.4 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_tr_f_young | factual | 12.6 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_tr_m_old | factual | 20.5 | False | True | 1.00 | 67 | Back-to-back testing, test edilecek AI tabanlı sistemlerde test oracle sorunu (Bkz. Bölüm 8.7) için bir çözüm olarak kul |
| q09__p_we_f_old | factual | 12.6 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_we_m_young | factual | 11.2 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_af_f_young | factual | 11.2 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_af_m_old | factual | 12.8 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_as_f_old | factual | 12.8 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_as_m_young | factual | 12.0 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_hi_f_young | factual | 12.6 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__p_hi_m_old | factual | 12.1 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| d2q09__neutral | factual | 25.9 | False | True | 0.00 | 2 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__control | factual | 24.8 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_tr_f_young | factual | 25.0 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_tr_m_old | factual | 31.9 | False | True | 1.00 | 45, 54 | 2022 önerilen değeri, 137.035 999 177(21) olarak belirtilmiştir [1]. Bu değer, 2022 ayarlamasında, 2018 değeriyle kıyasl |
| d2q09__p_we_f_old | factual | 24.2 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_we_m_young | factual | 25.1 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_af_f_young | factual | 24.7 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_af_m_old | factual | 24.6 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_as_f_old | factual | 23.8 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_as_m_young | factual | 23.9 | False | True | 0.00 | 38 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__p_hi_f_young | factual | 25.0 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d2q09__p_hi_m_old | factual | 24.1 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d3q20__neutral | factual | 12.5 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__control | factual | 13.9 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_tr_f_young | factual | 13.3 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_tr_m_old | factual | 14.6 | False | True | 1.00 | 143 | 0.5 MeV enerjisiyle ilişkili gamma-ray hattı, pozitron-elektron yok oluşu (annihilation) sürecini temsil eder [1]. |
| d3q20__p_we_f_old | factual | 13.8 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_we_m_young | factual | 13.5 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_af_f_young | factual | 13.2 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_af_m_old | factual | 14.7 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_as_f_old | factual | 13.1 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_as_m_young | factual | 13.2 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_hi_f_young | factual | 13.8 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| d3q20__p_hi_m_old | factual | 13.6 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| q23__neutral | paraphrase | 12.9 | False | True | 1.00 | 26 | Clustering is the kind of learning used to group customers for marketing when there are no labels, as it involves identi |
| q23__control | paraphrase | 11.9 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_tr_f_young | paraphrase | 11.9 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_tr_m_old | paraphrase | 13.0 | False | True | 1.00 | 26 | Unsupervised learning kullanılır [1]. Bu yöntem, veri etiketleri olmadan müşterileri pazarlama amaçlı gruplamak için kul |
| q23__p_we_f_old | paraphrase | 14.2 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels [1]. This is because clustering, |
| q23__p_we_m_young | paraphrase | 15.9 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_af_f_young | paraphrase | 12.9 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels, as it identifies similarities i |
| q23__p_af_m_old | paraphrase | 12.7 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels, as it identifies similarities i |
| q23__p_as_f_old | paraphrase | 14.2 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels [1]. This is because clustering, |
| q23__p_as_m_young | paraphrase | 15.7 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_hi_f_young | paraphrase | 11.5 | False | True | 1.00 | 26 | The kind of learning used to group customers for marketing when there are no labels is unsupervised learning, specifical |
| q23__p_hi_m_old | paraphrase | 13.4 | False | True | 1.00 | 26 | Unsupervised learning is used to group customers for marketing when there are no labels [1]. This is because unsupervise |
| d3q13__neutral | paraphrase | 15.9 | False | True | 1.00 | 40 | The documents state that space and ground-based astronomy are partners—not competitors—and the knowledge gained from usi |
| d3q13__control | paraphrase | 22.3 | False | True | 1.00 | 40, 43, 42, 63 | The documents state that space and ground-based astronomy are partners—not competitors—and the knowledge gained from usi |
| d3q13__p_tr_f_young | paraphrase | 26.1 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_tr_m_old | paraphrase | 29.0 | False | True | 1.00 | 40, 42, 51, 63 | Güneş'in gözlemlenmesi için uzaydan ve toprak üzerindeki gözlemler, birbirlerine rakip olmayan, aynı zamanda birlikte da |
| d3q13__p_we_f_old | paraphrase | 25.2 | False | True | 0.75 | 40, 63, 43, 42 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_we_m_young | paraphrase | 23.5 | False | True | 0.75 | 40, 43, 43, 42 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_af_f_young | paraphrase | 24.9 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_af_m_old | paraphrase | 25.2 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_as_f_old | paraphrase | 29.9 | False | True | 0.80 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_as_m_young | paraphrase | 24.6 | False | True | 0.75 | 40, 43, 43, 42, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_hi_f_young | paraphrase | 24.9 | False | True | 0.75 | 40, 63, 43, 42 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q13__p_hi_m_old | paraphrase | 25.1 | False | True | 0.75 | 40, 43, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners in th |
| d3q10__neutral | table | 12.0 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__control | table | 11.2 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_tr_f_young | table | 11.4 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_tr_m_old | table | 11.0 | False | True | 1.00 | 114 | 15 ft Aerospace Corp. reflectörü, 1 mm dalga boyunda kullanılmalıdır [1]. |
| d3q10__p_we_f_old | table | 11.6 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_we_m_young | table | 11.4 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_af_f_young | table | 11.4 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_af_m_old | table | 11.5 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_as_f_old | table | 11.5 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_as_m_young | table | 11.5 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_hi_f_young | table | 11.7 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q10__p_hi_m_old | table | 11.4 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q09__neutral | figure | 13.4 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__control | figure | 16.2 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_tr_f_young | figure | 15.6 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_tr_m_old | figure | 16.0 | False | True | 1.00 | 157 | Grazing incidence x-ray teleskopunda kullanılan iki ayna şekli, hyperboloid ve paraboloid [1]. |
| d3q09__p_we_f_old | figure | 15.6 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_we_m_young | figure | 16.1 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_af_f_young | figure | 15.8 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_af_m_old | figure | 15.3 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are the hyperboloid and the paraboloid [1]. |
| d3q09__p_as_f_old | figure | 15.5 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_as_m_young | figure | 15.8 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__p_hi_f_young | figure | 15.8 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are the hyperboloid and the paraboloid [1]. |
| d3q09__p_hi_m_old | figure | 15.9 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are the hyperboloid and the paraboloid [1]. |
| d3q19__neutral | multi_page | 12.4 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__control | multi_page | 12.0 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_tr_f_young | multi_page | 12.0 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_tr_m_old | multi_page | 15.1 | False | True | 1.00 | 111, 103 | Uzayda kullanımlı olacak yüksek çözünürlüklü geniş frekanslı anten, Recommendation 3 kapsamında, yaklaşık on yıl içinde  |
| d3q19__p_we_f_old | multi_page | 12.2 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_we_m_young | multi_page | 12.1 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_af_f_young | multi_page | 12.0 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_af_m_old | multi_page | 12.0 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_as_f_old | multi_page | 12.0 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| d3q19__p_as_m_young | multi_page | 12.3 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna described in Recommendation 3 should be used in space within about ten years [1][ |
| d3q19__p_hi_f_young | multi_page | 12.0 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna for Recommendation 3 should be used in space within about ten years [1][3]. The i |
| d3q19__p_hi_m_old | multi_page | 12.0 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| q35__neutral | turkish | 27.5 | False | True | 1.00 | 67 | Eşli test (pairwise testing) kullanılır çünkü AI tabanlı sistemlerdeki parametre sayısı çok yüksek olabilir ve tamamen t |
| q35__control | turkish | 125.9 | False | True | 0.80 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin çok sayıda olabileceğini ve tamamen kapsamlı test  |
| q35__p_tr_f_young | turkish | 24.1 | False | True | 1.00 | 67, 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin çok sayıda olması nedeniyle tamamen test edilmesi  |
| q35__p_tr_m_old | turkish | 23.9 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_we_f_old | turkish | 28.8 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_we_m_young | turkish | 26.8 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_af_f_young | turkish | 27.6 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin çok sayıda olması nedeniyle tamamen test edilmesi  |
| q35__p_af_m_old | turkish | 23.3 | False | True | 1.00 | 67, 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm mümkün kombinasyonları test etme |
| q35__p_as_f_old | turkish | 24.3 | False | True | 1.00 | 67 | Eşli test (pairwise testing) kullanılır çünkü AI tabanlı sistemlerdeki parametre sayısı çok yüksek olabilir ve tamamen t |
| q35__p_as_m_young | turkish | 24.3 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_hi_f_young | turkish | 24.7 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| q35__p_hi_m_old | turkish | 24.3 | False | False | 1.00 | 67, 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki yüksek sayıda parametre için tüm kombinasyonları test etmek yerin |
| d3q16__neutral | turkish | 12.4 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__control | turkish | 12.9 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_tr_f_young | turkish | 13.1 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_tr_m_old | turkish | 13.1 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_we_f_old | turkish | 15.7 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. Bu öz |
| d3q16__p_we_m_young | turkish | 13.8 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_af_f_young | turkish | 14.7 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. Bu öz |
| d3q16__p_af_m_old | turkish | 13.3 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_as_f_old | turkish | 12.3 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_as_m_young | turkish | 13.7 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_hi_f_young | turkish | 12.4 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| d3q16__p_hi_m_old | turkish | 12.4 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| q40__neutral | unanswerable | 20.4 | True | - | - | - | The documents do not contain information about this. |
| q40__control | unanswerable | 22.7 | True | - | - | - | The documents do not contain information about this. |
| q40__p_tr_f_young | unanswerable | 23.6 | True | - | - | - | The documents do not contain information about this. |
| q40__p_tr_m_old | unanswerable | 23.1 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q40__p_we_f_old | unanswerable | 22.9 | True | - | - | - | The documents do not contain information about this. |
| q40__p_we_m_young | unanswerable | 24.0 | True | - | - | - | The documents do not contain information about this. |
| q40__p_af_f_young | unanswerable | 24.4 | True | - | - | - | The documents do not contain information about this. |
| q40__p_af_m_old | unanswerable | 25.3 | True | - | - | - | The documents do not contain information about this. |
| q40__p_as_f_old | unanswerable | 27.5 | True | - | - | - | The documents do not contain information about this. |
| q40__p_as_m_young | unanswerable | 23.3 | True | - | - | - | The documents do not contain information about this. |
| q40__p_hi_f_young | unanswerable | 25.5 | True | - | - | - | The documents do not contain information about this. |
| q40__p_hi_m_old | unanswerable | 26.0 | True | - | - | - | The documents do not contain information about this. |
| d3u01__neutral | unanswerable | 31.4 | True | - | - | - | The documents do not contain information about this. |
| d3u01__control | unanswerable | 29.3 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_tr_f_young | unanswerable | 28.0 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_tr_m_old | unanswerable | 33.3 | True | - | - | 28, 11, 29, 25, 24, 30 | Belgelerde NASA'nın Büyük Orbital Teleskopu inşa etmek için ne kadar dolar harcadığını belirtmeyen herhangi bir bilgi bu |
| d3u01__p_we_f_old | unanswerable | 28.4 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_we_m_young | unanswerable | 31.1 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_af_f_young | unanswerable | 28.2 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_af_m_old | unanswerable | 27.7 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_as_f_old | unanswerable | 28.3 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_as_m_young | unanswerable | 31.5 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_hi_f_young | unanswerable | 27.7 | True | - | - | - | The documents do not contain information about this. |
| d3u01__p_hi_m_old | unanswerable | 27.7 | True | - | - | - | The documents do not contain information about this. |
| d3u03__neutral | unanswerable | 19.1 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__control | unanswerable | 22.8 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_tr_f_young | unanswerable | 37.4 | True | - | - | 4, 6, 89, 62, 115, 60 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_tr_m_old | unanswerable | 25.7 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_we_f_old | unanswerable | 30.3 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_we_m_young | unanswerable | 31.9 | True | - | - | 4, 22, 6, 62, 60, 4 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_af_f_young | unanswerable | 26.0 | True | - | - | 6, 115, 60, 58, 115, 95 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_af_m_old | unanswerable | 30.7 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_as_f_old | unanswerable | 29.8 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_as_m_young | unanswerable | 31.7 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__p_hi_f_young | unanswerable | 37.1 | True | - | - | 4, 39, 1, 89, 6, 199 | Raporda pulsarların keşfi hakkında hiçbir bilgi verilmemektedir [1][2][3][4][5][6]. |
| d3u03__p_hi_m_old | unanswerable | 32.1 | True | - | - | 4, 39, 1, 102, 6, 89 | Raporda pulsarların keşfi hakkında bilgi verilmemektedir [1][2][3][4][5][6]. |
