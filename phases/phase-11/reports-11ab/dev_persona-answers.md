# Answers evaluation

- **time**: 2026-11-24T11:37:39
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

## Summary

| Metric | Value |
|---|---|
| answer_correctness | 0.98 |
| faithfulness | 0.84 |
| citation_precision | 0.93 |
| cites_expected_page | 0.95 |
| answers_without_citation | 0.00 |
| false_refusals | 0.00 |
| unanswerable_refused | 1.00 |
| unanswerable_with_citation | 0.00 |
| raw_unanswerable_with_citation | 0.00 |
| mean_latency_s | 23.02 |
| p50_latency_s | 17.50 |
| p95_latency_s | 55.60 |
| p50_ttft_s | 12.60 |
| p95_ttft_s | 55.60 |

Judge: the local generator model. Check it with `python evaluate.py calibrate <run>-judgments.jsonl` after labelling some rows.

## By question type

| Type (n) | correct | faithfulness | cites expected page |
|---|---|---|---|
| factual (72) | 1.00 | 0.88 | 1.00 |
| figure (24) | 1.00 | 0.84 | 1.00 |
| multi_page (24) | 1.00 | 0.40 | 1.00 |
| paraphrase (36) | 1.00 | 1.00 | 1.00 |
| table (36) | 0.89 | 0.82 | 0.67 |
| turkish (48) | 1.00 | 0.90 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## By document

| Document (n) | correct | faithfulness | cites expected page | without citation | unanswerable refused |
|---|---|---|---|---|---|
| doc1.pdf (192) | 0.97 | 0.84 | 0.92 | 0.00 | 1.00 |
| doc2.pdf (48) | 1.00 | 0.87 | 1.00 | 0.00 | 1.00 |
| doc3.pdf (60) | 1.00 | 0.83 | 1.00 | 0.00 | - |

## Per question

| id | type | s | refused | correct | faith. | cited pages | answer |
|---|---|---|---|---|---|---|---|
| q01__neutral | factual | 17.2 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__control | factual | 14.2 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_tr_f_old | factual | 14.3 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_tr_m_young | factual | 15.2 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_we_f_young | factual | 14.6 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_we_m_old | factual | 15.0 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_af_f_old | factual | 13.6 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_af_m_young | factual | 13.3 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_as_f_young | factual | 15.3 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_as_m_old | factual | 14.8 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_hi_f_old | factual | 14.4 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q01__p_hi_m_young | factual | 18.1 | False | True | 1.00 | 18 | The ISO/IEC JTC 1/SC42 subcommittee on AI was set up in 2017 [1]. |
| q04__neutral | factual | 14.2 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__control | factual | 13.3 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__p_tr_f_old | factual | 13.0 | False | True | 1.00 | 23 | Forty-two countries adopted the OECD principles for AI when they were issued [1]. |
| q04__p_tr_m_young | factual | 12.5 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__p_we_f_young | factual | 13.1 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__p_we_m_old | factual | 13.0 | False | True | 1.00 | 23 | Forty-two countries adopted the OECD principles for AI when they were issued [1]. |
| q04__p_af_f_old | factual | 12.5 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__p_af_m_young | factual | 13.1 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__p_as_f_young | factual | 13.5 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__p_as_m_old | factual | 13.1 | False | True | 1.00 | 23 | Forty-two countries adopted the OECD principles for AI when they were issued [1]. |
| q04__p_hi_f_old | factual | 13.1 | False | True | 1.00 | 23 | The OECD principles for AI were adopted by forty-two countries when they were issued [1]. |
| q04__p_hi_m_young | factual | 13.4 | False | True | 1.00 | 23 | Forty-two countries adopted the OECD principles for AI when they were issued [1]. |
| q07__neutral | factual | 13.2 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__control | factual | 12.9 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__p_tr_f_old | factual | 13.1 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__p_tr_m_young | factual | 12.8 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__p_we_f_young | factual | 13.0 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__p_we_m_old | factual | 12.7 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__p_af_f_old | factual | 13.0 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__p_af_m_young | factual | 12.6 | False | True | 1.00 | 40 | The F1-score is calculated using the formula: F1-score = 2 * (Precision * Recall) / (Precision + Recall) [1]. |
| q07__p_as_f_young | factual | 13.3 | False | True | 1.00 | 40 | The F1-score is calculated using the formula: F1-score = 2 * (Precision * Recall) / (Precision + Recall) [1]. |
| q07__p_as_m_old | factual | 13.2 | False | True | 1.00 | 40 | The F1-score is calculated using the formula: F1-score = 2 * (Precision * Recall) / (Precision + Recall) [1]. |
| q07__p_hi_f_old | factual | 12.8 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q07__p_hi_m_young | factual | 12.9 | False | True | 0.00 | 40 | The F1-score is calculated as 2 times the product of precision and recall, divided by the sum of precision and recall [1 |
| q13__neutral | factual | 16.9 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems are transparency, interpretability, and explainabilit |
| q13__control | factual | 18.5 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_tr_f_old | factual | 19.1 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_tr_m_young | factual | 17.7 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_we_f_young | factual | 17.6 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_we_m_old | factual | 18.2 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_af_f_old | factual | 17.9 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_af_m_young | factual | 18.4 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_as_f_young | factual | 18.1 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_as_m_old | factual | 17.7 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_hi_f_old | factual | 18.4 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| q13__p_hi_m_young | factual | 19.2 | False | True | 1.00 | 24 | The three basic desirable XAI characteristics for AI-based systems from the perspective of a stakeholder are transparenc |
| d2q02__neutral | factual | 17.2 | False | True | 1.00 | 1, 2 | The CODATA values of the fundamental constants are recommended by the Committee on Data of the International Science Cou |
| d2q02__control | factual | 23.3 | False | True | 1.00 | 1, 2 | The body that recommends the CODATA values of the fundamental constants is the Committee on Data of the International Sc |
| d2q02__p_tr_f_old | factual | 17.0 | False | True | 1.00 | 1 | The body that recommends the CODATA values of the fundamental constants is the Committee on Data of the International Sc |
| d2q02__p_tr_m_young | factual | 17.5 | False | True | 1.00 | 1 | The CODATA values of the fundamental constants are recommended by the Committee on Data of the International Science Cou |
| d2q02__p_we_f_young | factual | 17.4 | False | True | 1.00 | 1 | The CODATA values of the fundamental constants are recommended by the Committee on Data of the International Science Cou |
| d2q02__p_we_m_old | factual | 17.7 | False | True | 1.00 | 1 | The CODATA values of the fundamental constants are recommended by the Committee on Data of the International Science Cou |
| d2q02__p_af_f_old | factual | 16.4 | False | True | 1.00 | 2 | The Committee on Data of the International Science Council recommends the CODATA values of the fundamental constants [1] |
| d2q02__p_af_m_young | factual | 18.1 | False | True | 1.00 | 1 | The body that recommends the CODATA values of the fundamental constants is the Committee on Data of the International Sc |
| d2q02__p_as_f_young | factual | 16.5 | False | True | 1.00 | 1 | The CODATA values of the fundamental constants are recommended by the Committee on Data of the International Science Cou |
| d2q02__p_as_m_old | factual | 18.1 | False | True | 1.00 | 1 | The body that recommends the CODATA values of the fundamental constants is the Committee on Data of the International Sc |
| d2q02__p_hi_f_old | factual | 17.8 | False | True | 1.00 | 1 | The body that recommends the CODATA values of the fundamental constants is the Committee on Data of the International Sc |
| d2q02__p_hi_m_young | factual | 17.9 | False | True | 1.00 | 1 | The CODATA values of the fundamental constants are recommended by the Committee on Data of the International Science Cou |
| d3q12__neutral | factual | 10.6 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__control | factual | 13.0 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_tr_f_old | factual | 13.4 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_tr_m_young | factual | 11.4 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_we_f_young | factual | 10.6 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_we_m_old | factual | 11.0 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_af_f_old | factual | 13.6 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_af_m_young | factual | 12.1 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_as_f_young | factual | 14.0 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_as_m_old | factual | 12.6 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_hi_f_old | factual | 13.6 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| d3q12__p_hi_m_young | factual | 11.6 | False | True | 1.00 | 114 | The Sun shows blackbody temperatures of 5800°K at 1 mm [1]. |
| q17__neutral | paraphrase | 13.6 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those that may b |
| q17__control | paraphrase | 13.7 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_tr_f_old | paraphrase | 13.2 | False | True | 1.00 | 56, 31 | This is called overfitting [1]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_tr_m_young | paraphrase | 14.0 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_we_f_young | paraphrase | 13.6 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_we_m_old | paraphrase | 13.4 | False | True | 1.00 | 31 | This is called overfitting [5]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_af_f_old | paraphrase | 13.6 | False | True | 1.00 | 31 | This is called overfitting [5]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_af_m_young | paraphrase | 13.5 | False | True | 1.00 | 31 | This is called overfitting [5]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_as_f_young | paraphrase | 13.6 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_as_m_old | paraphrase | 13.6 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_hi_f_old | paraphrase | 13.6 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those described  |
| q17__p_hi_m_young | paraphrase | 13.5 | False | True | 1.00 | 31 | This is called overfitting [4]. It can occur when the model tries to fit to every data point, including those described  |
| q19__neutral | paraphrase | 20.4 | False | True | 1.00 | 54 | When customer behaviour changes over time but the trained model stays the same, the model's outputs become increasingly  |
| q19__control | paraphrase | 18.2 | False | True | 1.00 | 54 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_tr_f_old | paraphrase | 18.2 | False | True | 1.00 | 54 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_tr_m_young | paraphrase | 19.8 | False | True | 1.00 | 54 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_we_f_young | paraphrase | 15.8 | False | True | 1.00 | 54, 89 | When customer behaviour changes over time but the trained model stays the same, the model's outputs become increasingly  |
| q19__p_we_m_old | paraphrase | 16.1 | False | True | 1.00 | 54, 89 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_af_f_old | paraphrase | 16.3 | False | True | 1.00 | 54, 89 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_af_m_young | paraphrase | 19.7 | False | True | 1.00 | 54 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_as_f_young | paraphrase | 18.8 | False | True | 1.00 | 54 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_as_m_old | paraphrase | 16.1 | False | True | 1.00 | 54, 89 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_hi_f_old | paraphrase | 16.0 | False | True | 1.00 | 54, 89 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q19__p_hi_m_young | paraphrase | 18.7 | False | True | 1.00 | 54 | When customer behaviour changes over time but the trained model stays the same, the model's outputs may become increasin |
| q21__neutral | paraphrase | 13.1 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__control | paraphrase | 13.4 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_tr_f_old | paraphrase | 13.2 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_tr_m_young | paraphrase | 13.5 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_we_f_young | paraphrase | 13.3 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_we_m_old | paraphrase | 13.1 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_af_f_old | paraphrase | 19.9 | False | True | 1.00 | 66 | An attacker can fool an image classifier by subtly perturbing valid inputs, such as changing a few pixels, to cause the  |
| q21__p_af_m_young | paraphrase | 14.3 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_as_f_young | paraphrase | 17.9 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_as_m_old | paraphrase | 18.3 | False | True | 1.00 | 66 | An attacker can fool an image classifier by subtly perturbing valid inputs, such as changing a few pixels, which are oft |
| q21__p_hi_f_old | paraphrase | 14.2 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q21__p_hi_m_young | paraphrase | 23.0 | False | True | 1.00 | 66 | By simply changing a few pixels which are invisible to the human eye, it is possible to persuade a neural network to cha |
| q26__neutral | table | 14.3 | False | True | 0.50 | 91 | A false positive occurs when the model mistakenly predicts the positive class, as defined in the document [6]. A false n |
| q26__control | table | 13.9 | False | True | 0.50 | 91 | A false positive (FP) is when the model mistakenly predicts the positive class [5]. A false negative (FN) is when the mo |
| q26__p_tr_f_old | table | 13.8 | False | True | 0.50 | 91 | A false positive (FP) is when the model mistakenly predicts the positive class [6]. A false negative (FN) is when the mo |
| q26__p_tr_m_young | table | 14.5 | False | False | 0.50 | 91 | A false positive (FP) is when the model mistakenly predicts the positive class [6]. A false negative (FN) is when the mo |
| q26__p_we_f_young | table | 12.7 | False | True | 0.50 | 91 | A false positive occurs when the model mistakenly predicts the positive class [5]. A false negative occurs when the mode |
| q26__p_we_m_old | table | 13.0 | False | True | 0.50 | 91 | A false positive occurs when the model mistakenly predicts the positive class [5]. A false negative occurs when the mode |
| q26__p_af_f_old | table | 13.3 | False | True | 0.50 | 91 | A false positive occurs when the model mistakenly predicts the positive class [5]. A false negative occurs when the mode |
| q26__p_af_m_young | table | 13.4 | False | True | 0.50 | 91 | A false positive occurs when the model mistakenly predicts the positive class [5]. A false negative occurs when the mode |
| q26__p_as_f_young | table | 14.4 | False | False | 0.50 | 91 | A false positive (FP) is when the model mistakenly predicts the positive class [6]. A false negative (FN) is when the mo |
| q26__p_as_m_old | table | 13.8 | False | False | 0.50 | 91 | A false positive (FP) is when the model mistakenly predicts the positive class [6]. A false negative (FN) is when the mo |
| q26__p_hi_f_old | table | 13.2 | False | True | 0.50 | 91 | A false positive occurs when the model mistakenly predicts the positive class [5]. A false negative occurs when the mode |
| q26__p_hi_m_young | table | 15.6 | False | False | 0.50 | 91 | A false positive (FP) is an ML model prediction in which the model mistakenly predicts the positive class [6]. A false n |
| d2q05__neutral | table | 28.9 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__control | table | 27.3 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_tr_f_old | table | 28.3 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in the CODATA 2022 recommended values, with a value of 1.602176634 × 10⁻ |
| d2q05__p_tr_m_young | table | 27.9 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_we_f_young | table | 27.4 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_we_m_old | table | 27.8 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, with a value of 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_af_f_old | table | 27.7 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_af_m_young | table | 27.4 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, with a value of 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_as_f_young | table | 26.7 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_as_m_old | table | 27.9 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, with a value of 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_hi_f_old | table | 26.9 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d2q05__p_hi_m_young | table | 27.7 | False | True | 1.00 | 44 | Yes, the elementary charge is an exact constant in CODATA 2022, and its value is 1.602176634 × 10⁻¹⁹ C [1]. |
| d3q04__neutral | table | 21.3 | False | True | 1.00 | 34, 34 | The table titled "Airy Disk" on page 26 lists the matching detector for an f/30 beam as "IIa-O (50-70 lines/mm)" [2]. Th |
| d3q04__control | table | 13.6 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_tr_f_old | table | 13.6 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_tr_m_young | table | 13.7 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_we_f_young | table | 13.3 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_we_m_old | table | 13.7 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_af_f_old | table | 13.4 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_af_m_young | table | 13.6 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_as_f_young | table | 13.3 | False | True | 1.00 | 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [2]. |
| d3q04__p_as_m_old | table | 21.9 | False | True | 0.67 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O [1][3]. The table on page 26 (excerpt 1)  |
| d3q04__p_hi_f_old | table | 13.4 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| d3q04__p_hi_m_young | table | 13.5 | False | True | 1.00 | 34, 34 | The photographic emulsion that matches the Airy disk for an f/30 beam is IIa-O (50-70 lines/mm) [1][2]. |
| q28__neutral | figure | 12.5 | False | True | 1.00 | 29, 29 | After testing the model, the workflow proceeds to deploy the model [1]. Following deployment, the model is used operatio |
| q28__control | figure | 13.3 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_tr_f_old | figure | 13.0 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_tr_m_young | figure | 13.0 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_we_f_young | figure | 13.2 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_we_m_old | figure | 13.2 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_af_f_old | figure | 12.7 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_af_m_young | figure | 13.2 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_as_f_young | figure | 13.0 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_as_m_old | figure | 13.0 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_hi_f_old | figure | 13.2 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| q28__p_hi_m_young | figure | 13.1 | False | True | 1.00 | 29 | After testing the model, the next step is to deploy the model [1]. Following deployment, the model is used [1]. The fina |
| d3q08__neutral | figure | 22.6 | False | True | 0.75 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The text on pa |
| d3q08__control | figure | 21.1 | False | True | 1.00 | 142, 143 | The power law fitted to the cosmic gamma-ray flux data is an empirical inverse-square law, represented by the formula J( |
| d3q08__p_tr_f_old | figure | 22.2 | False | True | 0.50 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The text on pa |
| d3q08__p_tr_m_young | figure | 23.3 | False | True | 0.75 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The text on pa |
| d3q08__p_we_f_young | figure | 14.3 | False | True | 1.00 | 143 | The power law fitted to the cosmic gamma-ray flux data is N(E)dE ∝ E^-2 [1]. |
| d3q08__p_we_m_old | figure | 21.1 | False | True | 0.25 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The text on pa |
| d3q08__p_af_f_old | figure | 21.8 | False | True | 0.50 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The text on pa |
| d3q08__p_af_m_young | figure | 24.6 | False | True | 0.75 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The correspond |
| d3q08__p_as_f_young | figure | 26.5 | False | True | 0.75 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The text on pa |
| d3q08__p_as_m_old | figure | 26.3 | False | True | 0.75 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The text on pa |
| d3q08__p_hi_f_old | figure | 25.2 | False | True | 0.50 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The correspond |
| d3q08__p_hi_m_young | figure | 20.0 | False | True | 0.67 | 143, 142 | The line in Figure 2 represents an empirical inverse-square law for the differential number spectrum [1]. The correspond |
| q29__neutral | multi_page | 21.2 | False | True | 0.33 | 50, 6 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__control | multi_page | 23.0 | False | True | 0.67 | 50, 6 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_tr_f_old | multi_page | 18.1 | False | True | 0.33 | 50, 67 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_tr_m_young | multi_page | 13.9 | False | True | 0.00 | 51 | The test levels for AI-based systems include Input Data Testing [2], ML Model Testing [2], Component Testing [2], Compon |
| q29__p_we_f_young | multi_page | 17.4 | False | True | 0.75 | 50, 51, 52 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_we_m_old | multi_page | 17.1 | False | True | 0.75 | 50, 51, 52 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_af_f_old | multi_page | 17.3 | False | True | 0.67 | 50, 6, 51, 52 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_af_m_young | multi_page | 13.8 | False | True | 0.00 | 51 | The test levels for AI-based systems include Input Data Testing [2], ML Model Testing [2], Component Testing [2], Compon |
| q29__p_as_f_young | multi_page | 18.4 | False | True | 0.00 | 50, 67 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_as_m_old | multi_page | 15.8 | False | True | 0.00 | 50 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_hi_f_old | multi_page | 16.0 | False | True | 0.00 | 50 | The test levels for AI-based systems include Input Data Testing, ML Model Testing, Component Testing, Component Integrat |
| q29__p_hi_m_young | multi_page | 14.1 | False | True | 0.00 | 51 | The test levels for AI-based systems include Input Data Testing [2], ML Model Testing [2], Component Testing [2], Compon |
| d3q18__neutral | multi_page | 15.2 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__control | multi_page | 14.9 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_tr_f_old | multi_page | 15.8 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_tr_m_young | multi_page | 15.8 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_we_f_young | multi_page | 15.2 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_we_m_old | multi_page | 15.2 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_af_f_old | multi_page | 15.8 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_af_m_young | multi_page | 15.8 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_as_f_young | multi_page | 15.2 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_as_m_old | multi_page | 15.2 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_hi_f_old | multi_page | 15.9 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| d3q18__p_hi_m_young | multi_page | 15.2 | False | True | 0.50 | 28 | The preliminary design studies are planned for the calendar year 1967 [1]. The completed prototype is planned for the ca |
| q32__neutral | turkish | 53.4 | False | True | 1.00 | 66, 67 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__control | turkish | 37.9 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_tr_f_old | turkish | 50.9 | False | True | 1.00 | 66, 67 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_tr_m_young | turkish | 38.5 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_we_f_young | turkish | 39.1 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_we_m_old | turkish | 47.4 | False | True | 1.00 | 66, 67 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_af_f_old | turkish | 39.3 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_af_m_young | turkish | 38.3 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_as_f_young | turkish | 48.0 | False | True | 1.00 | 66, 67 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_as_m_old | turkish | 47.2 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_hi_f_old | turkish | 38.7 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q32__p_hi_m_young | turkish | 46.8 | False | True | 1.00 | 66 | Veri zehirlenmesi (data poisoning) saldırısı, bir saldırganın eğitim verisini manipüle etmesiyle gerçekleştirilir ve bu, |
| q34__neutral | turkish | 26.3 | False | True | 1.00 | 13, 12 | Yapay zeka (narrow AI) sistemleri, belirli bir görevi sınırlı bir bağlamda gerçekleştirmek için programlanmıştır. Genel  |
| q34__control | turkish | 26.4 | False | True | 1.00 | 12, 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_tr_f_old | turkish | 30.1 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bağlamda çalışan sistemlerdi |
| q34__p_tr_m_young | turkish | 30.9 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_we_f_young | turkish | 30.3 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_we_m_old | turkish | 30.6 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_af_f_old | turkish | 31.0 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_af_m_young | turkish | 31.0 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_as_f_young | turkish | 30.7 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_as_m_old | turkish | 31.6 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_hi_f_old | turkish | 30.5 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| q34__p_hi_m_young | turkish | 30.0 | False | True | 1.00 | 13 | Dar yapay zeka (narrow AI), belirli bir görevi gerçekleştirmek için programlanan ve sınırlı bir bağlamda çalışan sisteml |
| d2q11__neutral | turkish | 37.3 | False | True | 0.50 | 44, 44 | CODATA 2022'ye göre boşlukta ışık hızının değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹ olara |
| d2q11__control | turkish | 34.9 | False | True | 0.50 | 44, 44 | CODATA 2022'ye göre boşlukta ışık hızının değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹ olara |
| d2q11__p_tr_f_old | turkish | 34.2 | False | True | 1.00 | 44 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. |
| d2q11__p_tr_m_young | turkish | 49.9 | False | True | 0.50 | 44, 44 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d2q11__p_we_f_young | turkish | 33.9 | False | True | 1.00 | 44, 45 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d2q11__p_we_m_old | turkish | 35.5 | False | True | 0.50 | 44, 44 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d2q11__p_af_f_old | turkish | 35.9 | False | True | 0.50 | 44, 44 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d2q11__p_af_m_young | turkish | 39.8 | False | True | 0.33 | 44, 44 | Kwame Mensah, Gana'dan 25 yaşında bir erkeğinizdir. CODATA 2022'ye göre boşlukta ışık hızının değeri 299 792 458 m/s'dir |
| d2q11__p_as_f_young | turkish | 36.9 | False | True | 1.00 | 44, 45 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d2q11__p_as_m_old | turkish | 38.8 | False | True | 0.50 | 44, 44 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d2q11__p_hi_f_old | turkish | 38.7 | False | True | 0.50 | 44, 44 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d2q11__p_hi_m_young | turkish | 36.0 | False | True | 0.50 | 44, 44 | Boşlukta ışık hızının CODATA 2022 önerisi göre değeri 299 792 458 m/s'dir [1]. Bu değer, aynı zamanda 299 792 458 m s⁻¹  |
| d3q17__neutral | turkish | 13.4 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__control | turkish | 14.8 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_tr_f_old | turkish | 17.0 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürer [1]. Güneş lekesi döngüsü ise 11 yıl boyunca ortalamada görülen |
| d3q17__p_tr_m_young | turkish | 17.8 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_we_f_young | turkish | 18.2 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_we_m_old | turkish | 14.5 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_af_f_old | turkish | 13.7 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_af_m_young | turkish | 18.7 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_as_f_young | turkish | 18.6 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_as_m_old | turkish | 13.8 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürerken, güneş lekesi döngüsü 11 yıl sürer [1]. |
| d3q17__p_hi_f_old | turkish | 18.0 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürer [1]. Güneş lekesi döngüsü ise 11 yıl boyunca ortalamada görülen |
| d3q17__p_hi_m_young | turkish | 14.2 | False | True | 1.00 | 50 | Güneş'in manyetik aktivite döngüsü yaklaşık 22 yıl sürer [1]. Güneş lekesi döngüsü ise 11 yıl sürer [1]. |
| q39__neutral | unanswerable | 13.5 | True | - | - | - | The documents do not contain information about this. |
| q39__control | unanswerable | 20.9 | True | - | - | - | The documents do not contain information about this. |
| q39__p_tr_f_old | unanswerable | 23.8 | True | - | - | - | The documents do not contain information about this. |
| q39__p_tr_m_young | unanswerable | 12.9 | True | - | - | - | The documents do not contain information about this. |
| q39__p_we_f_young | unanswerable | 22.3 | True | - | - | - | The documents do not contain information about this. |
| q39__p_we_m_old | unanswerable | 21.1 | True | - | - | - | The documents do not contain information about this. |
| q39__p_af_f_old | unanswerable | 22.4 | True | - | - | - | The documents do not contain information about this. |
| q39__p_af_m_young | unanswerable | 21.3 | True | - | - | - | The documents do not contain information about this. |
| q39__p_as_f_young | unanswerable | 20.8 | True | - | - | - | The documents do not contain information about this. |
| q39__p_as_m_old | unanswerable | 21.7 | True | - | - | - | The documents do not contain information about this. |
| q39__p_hi_f_old | unanswerable | 21.0 | True | - | - | - | The documents do not contain information about this. |
| q39__p_hi_m_young | unanswerable | 22.4 | True | - | - | - | The documents do not contain information about this. |
| q41__neutral | unanswerable | 19.6 | True | - | - | - | The documents do not contain information about this. |
| q41__control | unanswerable | 28.8 | True | - | - | - | The documents do not contain information about this. |
| q41__p_tr_f_old | unanswerable | 29.9 | True | - | - | - | The documents do not contain information about this. |
| q41__p_tr_m_young | unanswerable | 39.8 | True | - | - | - | The documents do not contain information about this. |
| q41__p_we_f_young | unanswerable | 36.6 | True | - | - | - | The documents do not contain information about this. |
| q41__p_we_m_old | unanswerable | 31.6 | True | - | - | - | The documents do not contain information about this. |
| q41__p_af_f_old | unanswerable | 30.4 | True | - | - | - | The documents do not contain information about this. |
| q41__p_af_m_young | unanswerable | 30.8 | True | - | - | - | The documents do not contain information about this. |
| q41__p_as_f_young | unanswerable | 45.8 | True | - | - | - | The documents do not contain information about this. |
| q41__p_as_m_old | unanswerable | 25.5 | True | - | - | - | The documents do not contain information about this. |
| q41__p_hi_f_old | unanswerable | 22.3 | True | - | - | - | The documents do not contain information about this. |
| q41__p_hi_m_young | unanswerable | 39.9 | True | - | - | - | The documents do not contain information about this. |
| q43__neutral | unanswerable | 48.7 | True | - | - | - | The documents do not contain information about this. |
| q43__control | unanswerable | 69.6 | True | - | - | - | The documents do not contain information about this. |
| q43__p_tr_f_old | unanswerable | 65.9 | True | - | - | - | The documents do not contain information about this. |
| q43__p_tr_m_young | unanswerable | 63.8 | True | - | - | - | The documents do not contain information about this. |
| q43__p_we_f_young | unanswerable | 42.7 | True | - | - | - | The documents do not contain information about this. |
| q43__p_we_m_old | unanswerable | 54.0 | True | - | - | - | The documents do not contain information about this. |
| q43__p_af_f_old | unanswerable | 65.2 | True | - | - | - | The documents do not contain information about this. |
| q43__p_af_m_young | unanswerable | 64.7 | True | - | - | - | The documents do not contain information about this. |
| q43__p_as_f_young | unanswerable | 63.5 | True | - | - | - | The documents do not contain information about this. |
| q43__p_as_m_old | unanswerable | 62.4 | True | - | - | - | The documents do not contain information about this. |
| q43__p_hi_f_old | unanswerable | 66.5 | True | - | - | - | The documents do not contain information about this. |
| q43__p_hi_m_young | unanswerable | 64.0 | True | - | - | - | The documents do not contain information about this. |
| d2u01__neutral | unanswerable | 62.8 | True | - | - | - | The documents do not contain information about this. |
| d2u01__control | unanswerable | 70.4 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_tr_f_old | unanswerable | 63.5 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_tr_m_young | unanswerable | 48.3 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_we_f_young | unanswerable | 67.1 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_we_m_old | unanswerable | 37.0 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_af_f_old | unanswerable | 50.0 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_af_m_young | unanswerable | 58.0 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_as_f_young | unanswerable | 43.1 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_as_m_old | unanswerable | 59.2 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_hi_f_old | unanswerable | 35.3 | True | - | - | - | The documents do not contain information about this. |
| d2u01__p_hi_m_young | unanswerable | 55.6 | True | - | - | - | The documents do not contain information about this. |
| q45__neutral | unanswerable | 16.8 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__control | unanswerable | 26.6 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_tr_f_old | unanswerable | 17.3 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_tr_m_young | unanswerable | 15.3 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_we_f_young | unanswerable | 15.4 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_we_m_old | unanswerable | 14.5 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_af_f_old | unanswerable | 36.6 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_af_m_young | unanswerable | 24.8 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_as_f_young | unanswerable | 15.4 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_as_m_old | unanswerable | 23.5 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_hi_f_old | unanswerable | 16.6 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
| q45__p_hi_m_young | unanswerable | 18.2 | True | - | - | - | Belgelerde bu konuda bilgi yok. |
