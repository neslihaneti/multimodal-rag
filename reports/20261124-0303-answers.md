# Answers evaluation

- **time**: 2026-11-24T03:03:00
- **golden**: dev_style.jsonl
- **golden_sha256**: 06c9e8981963
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
| answer_correctness | 0.96 |
| faithfulness | 0.87 |
| citation_precision | 0.93 |
| cites_expected_page | 0.97 |
| answers_without_citation | 0.00 |
| false_refusals | 0.01 |
| unanswerable_refused | 0.95 |
| unanswerable_with_citation | 0.05 |
| raw_unanswerable_with_citation | 0.05 |
| mean_latency_s | 23.18 |
| p50_latency_s | 18.40 |
| p95_latency_s | 50.60 |
| p50_ttft_s | 12.30 |
| p95_ttft_s | 50.60 |

Judge: the local generator model. Check it with `python evaluate.py calibrate <run>-judgments.jsonl` after labelling some rows.

## By question type

| Type (n) | correct | faithfulness | cites expected page |
|---|---|---|---|
| factual (24) | 1.00 | 0.90 | 1.00 |
| figure (8) | 1.00 | 0.85 | 1.00 |
| multi_page (8) | 1.00 | 0.49 | 1.00 |
| paraphrase (12) | 0.92 | 1.00 | 1.00 |
| table (12) | 0.92 | 0.86 | 0.92 |
| turkish (16) | 0.94 | 0.93 | 0.94 |

\* n < 8: informational only, no pass/fail threshold.

## By document

| Document (n) | correct | faithfulness | cites expected page | without citation | unanswerable refused |
|---|---|---|---|---|---|
| doc1.pdf (64) | 0.96 | 0.88 | 0.98 | 0.00 | 0.94 |
| doc2.pdf (16) | 1.00 | 0.92 | 1.00 | 0.00 | 1.00 |
| doc3.pdf (20) | 0.95 | 0.80 | 0.95 | 0.00 | - |

## Per question

| id | type | s | refused | correct | faith. | cited pages | answer |
|---|---|---|---|---|---|---|---|
| q01__formal | factual | 25.6 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__casual | factual | 13.8 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 AI subcommittee was set up in 2017 [1]. |
| q01__non_native | factual | 14.6 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee for AI was set up in 2017 [1]. |
| q01__typos | factual | 13.0 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q04__formal | factual | 13.7 | False | True | 1.00 | 23 | The OECD principles on artificial intelligence were adopted by forty-two countries at the time of their issuance [1]. |
| q04__casual | factual | 13.1 | False | True | 1.00 | 23 | The OECD AI principles were adopted by forty-two countries when they were issued [1]. |
| q04__non_native | factual | 11.8 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__typos | factual | 14.0 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q07__formal | factual | 13.8 | False | True | 0.50 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__casual | factual | 13.2 | False | True | 1.00 | 40 | The F1-score is computed as the harmonic mean of precision and recall, using the formula: F1-score = 2 * (Precision * Re |
| q07__non_native | factual | 13.6 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__typos | factual | 12.5 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q13__formal | factual | 17.2 | False | True | 1.00 | 24 | The three fundamental characteristics considered desirable for explainable AI (XAI) are transparency, interpretability,  |
| q13__casual | factual | 18.5 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems are transparency, interpretability, and explainabilit |
| q13__non_native | factual | 17.7 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems are transparency, interpretability, and explainabilit |
| q13__typos | factual | 18.4 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems are transparency, interpretability, and explainabilit |
| d2q02__formal | factual | 24.2 | False | True | 1.00 | 2, 1 | The organisation responsible for recommending the CODATA values is the Committee on Data of the International Science Co |
| d2q02__casual | factual | 21.2 | False | True | 1.00 | 1, 2 | The CODATA values for the fundamental constants are recommended by the Committee on Data of the International Science Co |
| d2q02__non_native | factual | 26.9 | False | True | 1.00 | 1, 2 | The CODATA recommended values of fundamental constants are provided by the Committee on Data of the International Scienc |
| d2q02__typos | factual | 21.2 | False | True | 1.00 | 1, 2 | The recommended values of the fundamental constants are provided by the Committee on Data of the International Science C |
| d3q12__formal | factual | 11.0 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__casual | factual | 11.4 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__non_native | factual | 10.7 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__typos | factual | 11.1 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| q17__formal | paraphrase | 13.2 | False | True | 1.00 | 31 | This phenomenon is called overfitting [1]. It may occur when the model tries to fit to every data point, including those |
| q17__casual | paraphrase | 14.6 | False | True | 1.00 | 31 | The issue you're describing is called overfitting [2]. This happens when the model fits too closely to the training data |
| q17__non_native | paraphrase | 15.4 | False | True | 1.00 | 31 | This is called overfitting [4]. It occurs when the model fits too closely to the training data and fails to generalize t |
| q17__typos | paraphrase | 16.8 | False | False | 1.00 | 31 | This is called underfitting [2]. It can occur when the model is not sophisticated enough to accurately fit the patterns  |
| q19__formal | paraphrase | 17.9 | False | True | 1.00 | 54 | The operational environment can change over time without the trained model changing correspondingly. This phenomenon is  |
| q19__casual | paraphrase | 20.8 | False | True | 1.00 | 54, 29 | If customers start behaving differently over time but the model never gets updated, the model's outputs will become incr |
| q19__non_native | paraphrase | 11.8 | False | True | 1.00 | 54 | This phenomenon is known as concept drift, which typically causes the outputs of the model to become increasingly less a |
| q19__typos | paraphrase | 18.3 | False | True | 1.00 | 54 | When customer behavior changes over time but the trained model stays the same, the model's outputs become increasingly l |
| q21__formal | paraphrase | 14.0 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__casual | paraphrase | 13.7 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__non_native | paraphrase | 13.5 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__typos | paraphrase | 13.6 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q26__formal | table | 12.2 | False | True | 1.00 | 40, 91 | A false positive occurs when the model mistakenly predicts the positive class, while a false negative occurs when the mo |
| q26__casual | table | 14.7 | False | False | 0.50 | 91 | A false positive (FP) is an ML model prediction in which the model mistakenly predicts the positive class [5]. A false n |
| q26__non_native | table | 19.0 | False | True | 1.00 | 40, 91 | In a confusion matrix, a false positive (FP) occurs when the model mistakenly predicts the positive class, while a false |
| q26__typos | table | 13.4 | False | True | 0.50 | 40 | In a confusion matrix, a false positive (FP) is when the model mistakenly predicts the positive class [1]. A false negat |
| d2q05__formal | table | 30.6 | False | True | 1.00 | 44 | Yes, in the CODATA 2022 adjustment, the elementary charge is treated as an exact constant, and its value is given as 1.6 |
| d2q05__casual | table | 27.5 | False | True | 1.00 | 44 | Yes, the elementary charge is exact in the CODATA 2022 recommended values. Its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__non_native | table | 28.0 | False | True | 1.00 | 44 | In the CODATA 2022 adjustment, the elementary charge is an exact constant. Its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__typos | table | 27.7 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d3q04__formal | table | 13.5 | False | True | 1.00 | 34 | The photographic emulsion matched to the Airy disk of an f/30 beam is IIa-O (50-70 lines/mm) [2]. |
| d3q04__casual | table | 23.4 | False | True | 0.33 | 34, 34 | The emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [2]. This is found in the table on pa |
| d3q04__non_native | table | 13.3 | False | True | 1.00 | 34 | The photographic emulsion matching with the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [2]. |
| d3q04__typos | table | 14.2 | False | True | 1.00 | 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [2]. |
| q28__formal | figure | 12.8 | False | True | 1.00 | 29, 29 | After the model is tested, the next step is to deploy the model [1]. Following deployment, the model is used operational |
| q28__casual | figure | 13.4 | False | True | 1.00 | 29 | After testing the model, the next step in the ML workflow is to deploy the model [1]. Following deployment, the model is |
| q28__non_native | figure | 12.0 | False | True | 1.00 | 29 | After the model is tested, the next step is to deploy the model [1]. Following deployment, the model is used [1]. After  |
| q28__typos | figure | 12.9 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| d3q08__formal | figure | 20.5 | False | True | 0.50 | 142, 143 | The power law fitted to the cosmic gamma-ray flux data is an empirical inverse-square law, represented by the formula J( |
| d3q08__casual | figure | 20.4 | False | True | 0.67 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The correspond |
| d3q08__non_native | figure | 20.6 | False | True | 1.00 | 142, 143 | The power law fit to the data of cosmic gamma-ray flux is an empirical inverse-square law, represented by the formula J( |
| d3q08__typos | figure | 19.4 | False | True | 0.67 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The correspond |
| q29__formal | multi_page | 20.0 | False | True | 0.67 | 50, 6, 70 | The test levels that apply to AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Componen |
| q29__casual | multi_page | 19.3 | False | True | 0.33 | 50, 6 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__non_native | multi_page | 24.4 | False | True | 0.60 | 6, 51, 52 | The test levels for AI-based systems include input data testing, ML model testing, component testing, component integrat |
| q29__typos | multi_page | 18.9 | False | True | 0.33 | 50, 6 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| d3q18__formal | multi_page | 15.4 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completion of the prototype is planned fo |
| d3q18__casual | multi_page | 15.0 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The finished prototype is planned for the cal |
| d3q18__non_native | multi_page | 15.3 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The prototype is planned to be completed in t |
| d3q18__typos | multi_page | 15.1 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| q32__formal | turkish | 40.0 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__casual | turkish | 43.3 | False | True | 1.00 | 66, 67 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim veri setini manipüle etmesiyle gerçekleştirilir. Bu |
| q32__no_diacritics | turkish | 44.1 | False | True | 1.00 | 66, 58 | Veri zehirlenmesi (data poisoning), bir saldırganın eğitim verisini manipüle etmesiyle ilgili bir saldırı türüdür. Bu sa |
| q32__typos | turkish | 39.9 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q34__formal | turkish | 30.3 | False | True | 1.00 | 12, 13 | Yapay zekâ (narrow AI) sistemleri, belirli bir görevi gerçekleştirmek için programlanmıştır ve sınırlı bir bağlamda çalı |
| q34__casual | turkish | 32.3 | False | True | 1.00 | 13 | Yapay zeka (narrow AI) sistemleri, belirli bir görevi gerçekleştirmek için programlanmıştır ve sınırlı bir bağlamda çalı |
| q34__no_diacritics | turkish | 29.8 | False | True | 1.00 | 13 | Yapay zeka (narrow AI) sistemleri, belirli bir görevi gerçekleştirmek için programlanmıştır ve sınırlı bir bağlamda çalı |
| q34__typos | turkish | 33.8 | False | True | 1.00 | 13 | Yapay zeka (narrow AI) ve genel yapay zeka arasındaki fark, narrow AI'nin belirli bir görevi gerçekleştirmek üzere progr |
| d2q11__formal | turkish | 39.7 | False | True | 0.50 | 44, 44 | CODATA 2022 verilerine göre boşlukta ışık hızının değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s |
| d2q11__casual | turkish | 35.0 | False | True | 1.00 | 44 | CODATA 2022'ye göre boşlukta ışık hızı 299 792 458 m/s'tir [1]. Bu değer, tabloda "Speed of light in vacuum" başlığı alt |
| d2q11__no_diacritics | turkish | 48.5 | False | True | 1.00 | 44 | CODATA 2022'ye göre boşlukta ışık hızının değeri 299 792 458 m/s'tir [2]. |
| d2q11__typos | turkish | 37.8 | False | True | 0.50 | 44, 44 | CODATA 2022'ye göre boşlukta ışık hızının değeri 299 792 458 m/s'tir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹ olara |
| d3q17__formal | turkish | 13.3 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__casual | turkish | 13.3 | False | True | 1.00 | 50 | Güneşin manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__no_diacritics | turkish | 77.7 | True | False | - | - | Belgelerde bu konuda bilgi yok. |
| d3q17__typos | turkish | 14.5 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| q39__formal | unanswerable | 21.3 | True | - | - | - | The documents do not contain information about this. |
| q39__casual | unanswerable | 20.0 | False | - | - | 4, 11 | The Certified Tester AI Testing (CT-AI) exam is based on a syllabus that includes eleven chapters with examinable conten |
| q39__non_native | unanswerable | 13.3 | True | - | - | - | The documents do not contain information about this. |
| q39__typos | unanswerable | 21.3 | True | - | - | - | The documents do not contain information about this. |
| q41__formal | unanswerable | 31.2 | True | - | - | - | The documents do not contain information about this. |
| q41__casual | unanswerable | 22.8 | True | - | - | - | The documents do not contain information about this. |
| q41__non_native | unanswerable | 26.6 | True | - | - | - | The documents do not contain information about this. |
| q41__typos | unanswerable | 25.3 | True | - | - | - | The documents do not contain information about this. |
| q43__formal | unanswerable | 52.5 | True | - | - | - | The documents do not contain information about this. |
| q43__casual | unanswerable | 60.8 | True | - | - | - | The documents do not contain information about this. |
| q43__non_native | unanswerable | 48.6 | True | - | - | - | The documents do not contain information about this. |
| q43__typos | unanswerable | 56.3 | True | - | - | - | The documents do not contain information about this. |
| d2u01__formal | unanswerable | 50.6 | True | - | - | - | The documents do not contain information about this. |
| d2u01__casual | unanswerable | 64.3 | True | - | - | - | The documents do not contain information about this. |
| d2u01__non_native | unanswerable | 45.5 | True | - | - | - | The documents do not contain information about this. |
| d2u01__typos | unanswerable | 37.4 | True | - | - | - | The documents do not contain information about this. |
| q45__formal | unanswerable | 14.6 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__casual | unanswerable | 24.8 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__no_diacritics | unanswerable | 14.9 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__typos | unanswerable | 14.2 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
