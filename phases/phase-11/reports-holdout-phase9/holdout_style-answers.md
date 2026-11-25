# Answers evaluation

- **time**: 2026-11-24T14:48:10
- **golden**: holdout_style.jsonl
- **golden_sha256**: af5ec406eede
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
| answer_correctness | 0.97 |
| faithfulness | 0.93 |
| citation_precision | 0.83 |
| cites_expected_page | 0.93 |
| answers_without_citation | 0.00 |
| false_refusals | 0.00 |
| unanswerable_refused | 1.00 |
| unanswerable_with_citation | 0.00 |
| raw_unanswerable_with_citation | 0.00 |
| mean_latency_s | 19.25 |
| p50_latency_s | 16.60 |
| p95_latency_s | 32.50 |
| p50_ttft_s | 11.90 |
| p95_ttft_s | 27.90 |

Judge: the local generator model. Check it with `python evaluate.py calibrate <run>-judgments.jsonl` after labelling some rows.

## By question type

| Type (n) | correct | faithfulness | cites expected page |
|---|---|---|---|
| factual (12) | 1.00 | 0.78 | 0.75 |
| figure (4) * | 1.00 | 1.00 | 1.00 |
| multi_page (4) * | 1.00 | 1.00 | 1.00 |
| paraphrase (8) | 1.00 | 1.00 | 1.00 |
| table (4) * | 1.00 | 1.00 | 1.00 |
| turkish (8) | 0.88 | 1.00 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## By document

| Document (n) | correct | faithfulness | cites expected page | without citation | unanswerable refused |
|---|---|---|---|---|---|
| doc1.pdf (16) | 0.92 | 1.00 | 1.00 | 0.00 | 1.00 |
| doc2.pdf (4) * | 1.00 | 0.33 | 0.25 | 0.00 | - |
| doc3.pdf (32) | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 |

## Per question

| id | type | s | refused | correct | faith. | cited pages | answer |
|---|---|---|---|---|---|---|---|
| q09__formal | factual | 17.5 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__casual | factual | 10.5 | False | True | 1.00 | 67 | Another name for back-to-back testing is differential testing [1]. |
| q09__non_native | factual | 9.8 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| q09__typos | factual | 10.1 | False | True | 1.00 | 67 | Back-to-back testing is also known as differential testing [1]. |
| d2q09__formal | factual | 26.5 | False | True | 0.00 | 2 | The 2022 recommended value of the inverse of the fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__casual | factual | 39.8 | False | True | 0.33 | 2, 54, 45, 44 | The 2022 recommended value for the inverse fine-structure constant is 137.035 999 177(21) [4]. This value is derived fro |
| d2q09__non_native | factual | 25.2 | False | True | 0.00 | 2 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [4]. |
| d2q09__typos | factual | 25.1 | False | True | 1.00 | 45 | The 2022 recommended value of the inverse fine-structure constant is 137.035 999 177(21) [1]. |
| d3q20__formal | factual | 15.1 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV is represented by positron-electron annihilation [1]. |
| d3q20__casual | factual | 17.6 | False | True | 1.00 | 143, 144 | The 0.5 MeV gamma-ray line is associated with positron-electron annihilation [1]. This process is also mentioned in the  |
| d3q20__non_native | factual | 13.2 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV is represented by positron-electron annihilation [1]. |
| d3q20__typos | factual | 11.8 | False | True | 1.00 | 143 | The gamma-ray line at 0.5 MeV represents positron-electron annihilation [1]. |
| q23__formal | paraphrase | 15.2 | False | True | 1.00 | 26 | The type of learning used to segment customers for marketing purposes when no labels are available is unsupervised learn |
| q23__casual | paraphrase | 16.6 | False | True | 1.00 | 26, 30 | To group customers for marketing when there are no labels, you would use unsupervised learning, specifically clustering. |
| q23__non_native | paraphrase | 14.9 | False | True | 1.00 | 26 | The kind of learning used for grouping customers for marketing when labels are not existing is unsupervised learning, sp |
| q23__typos | paraphrase | 13.8 | False | True | 1.00 | 26 | Clustering is the kind of learning used to group customers for marketing when there are no labels, as it involves identi |
| d3q13__formal | paraphrase | 11.4 | False | True | 1.00 | 40 | Because the knowledge to be gained from using space and ground-based astronomy together is very likely greater than the  |
| d3q13__casual | paraphrase | 15.7 | False | True | 1.00 | 40 | The documents state that space and ground-based astronomy are partners—not competitors—and the knowledge gained from usi |
| d3q13__non_native | paraphrase | 30.5 | False | True | 1.00 | 40, 63, 42, 43 | The observing of the Sun from space and from ground should not be treated like rivals because both methods are partners, |
| d3q13__typos | paraphrase | 25.5 | False | True | 1.00 | 40, 42, 43, 63 | Observing the Sun from space and from the ground should not be treated as rivals because both methods are partners, and  |
| d3q10__formal | table | 11.0 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector is expected to be usable is 1 mm [1]. |
| d3q10__casual | table | 12.1 | False | True | 1.00 | 114 | The 15 ft Aerospace Corp. reflector should work at a shortest wavelength of 1 mm [1]. |
| d3q10__non_native | table | 11.3 | False | True | 1.00 | 114 | The 15 ft Aerospace Corp. reflector should be usable at a shortest wavelength of 1 mm [1]. |
| d3q10__typos | table | 11.0 | False | True | 1.00 | 114 | The shortest wavelength at which the 15 ft Aerospace Corp. reflector should be usable is 1 mm [1]. |
| d3q09__formal | figure | 18.9 | False | True | 1.00 | 157 | The two mirror geometries employed in the grazing incidence x-ray telescope are the hyperboloid and the paraboloid [1].  |
| d3q09__casual | figure | 13.0 | False | True | 1.00 | 157 | The grazing incidence x-ray telescope uses a hyperboloid and a paraboloid as its mirror shapes [1]. |
| d3q09__non_native | figure | 15.4 | False | True | 1.00 | 157 | The two shapes of mirror used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q09__typos | figure | 11.9 | False | True | 1.00 | 157 | The two mirror shapes used in the grazing incidence x-ray telescope are a hyperboloid and a paraboloid [1]. |
| d3q19__formal | multi_page | 12.4 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna in Recommendation 3 should be in use in space within about ten years [1][3]. The  |
| d3q19__casual | multi_page | 12.2 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna in Recommendation 3 should be used in space within about ten years [1][3]. The fi |
| d3q19__non_native | multi_page | 12.9 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna system proposed in Recommendation 3 should be used in space within about ten year |
| d3q19__typos | multi_page | 12.1 | False | True | 1.00 | 111, 103 | The high-resolution broad-band antenna of Recommendation 3 should be used in space within about ten years [1][3]. The in |
| q35__formal | turkish | 25.1 | False | False | 1.00 | 67, 67, 72 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin etkileşimlerini test etmek için kullanılır. Bu yön |
| q35__casual | turkish | 28.0 | False | True | 1.00 | 67 | Eşli test (pairwise testing), AI tabanlı sistemlerdeki parametrelerin çok sayıda olmasına rağmen, tüm mümkün kombinasyon |
| q35__no_diacritics | turkish | 21.9 | False | True | 1.00 | 67 | Pairwise testing is used for AI-based systems because it can significantly reduce the number of test cases required, ide |
| q35__typos | turkish | 29.4 | False | True | 1.00 | 67, 72 | Eşli tet (pairwise testing) AI tabanlı sistemlerde, özellikle çok sayıda parametre ve bu parametrelerin birçok farklı de |
| d3q16__formal | turkish | 14.7 | False | True | 1.00 | 177 | Fizik çalışma grubu, uzay ortamının dört temel özelliklerini kayda geçirmiştir: düşük sıcaklık, düşük basınç, zayıf many |
| d3q16__casual | turkish | 15.6 | False | True | 1.00 | 177 | Fizik çalışma grubu, uzay ortamının temel özelliklerini şu şekilde not etmiştir: (1) düşük sıcaklık, (2) düşük basınç, ( |
| d3q16__no_diacritics | turkish | 29.8 | False | True | 1.00 | 177 | Uzay ortamının temel özelliklerini not eden fizik çalışma grubu, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sı |
| d3q16__typos | turkish | 13.7 | False | True | 1.00 | 177 | Uzay ortamının temel özellikleri, düşük sıcaklık, düşük basınç, zayıf manyetik alan ve sıfır-gravity alanıdır [1]. |
| q40__formal | unanswerable | 22.5 | True | - | - | - | The documents do not contain information about this. |
| q40__casual | unanswerable | 25.5 | True | - | - | - | The documents do not contain information about this. |
| q40__non_native | unanswerable | 21.3 | True | - | - | - | The documents do not contain information about this. |
| q40__typos | unanswerable | 19.8 | True | - | - | - | The documents do not contain information about this. |
| d3u01__formal | unanswerable | 27.9 | True | - | - | - | The documents do not contain information about this. |
| d3u01__casual | unanswerable | 27.8 | True | - | - | - | The documents do not contain information about this. |
| d3u01__non_native | unanswerable | 34.7 | True | - | - | - | The documents do not contain information about this. |
| d3u01__typos | unanswerable | 32.5 | True | - | - | - | The documents do not contain information about this. |
| d3u03__formal | unanswerable | 20.1 | True | - | - | - | Verilen belgelerde pulsarların keşfine ilişkin herhangi bir bilgi bulunmamaktadır. |
| d3u03__casual | unanswerable | 21.9 | True | - | - | - | Verilen belgelerde pulsarların keşfiyle ilgili herhangi bir bilgi bulunamadı. |
| d3u03__no_diacritics | unanswerable | 27.8 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| d3u03__typos | unanswerable | 20.9 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
