# Retrieval evaluation

- **time**: 2026-11-24T11:46:27
- **golden**: dev_style.jsonl
- **golden_sha256**: 06c9e8981963
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

## Overall (80 answerable questions)

| Method | Recall@1 | Recall@6 | MRR | All pages@6 (multi-page) |
|---|---|---|---|---|
| vector | 0.93 | 1.00 | 0.956 | 0.50 |
| keyword | 0.56 | 0.89 | 0.695 | 0.25 |
| hybrid (RRF) | 0.88 | 0.95 | 0.917 | 0.25 |
| vector + reranker | 0.94 | 0.99 | 0.958 | 0.62 |
| hybrid + reranker | 0.94 | 0.99 | 0.961 | 0.62 |

## Recall@6 by question type

| Type (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| factual (24) | 1.00 | 0.88 | 1.00 | 1.00 | 1.00 |
| figure (8) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| multi_page (8) | 1.00 | 0.88 | 1.00 | 1.00 | 1.00 |
| paraphrase (12) | 1.00 | 0.92 | 1.00 | 1.00 | 1.00 |
| table (12) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| turkish (16) | 1.00 | 0.75 | 0.75 | 0.94 | 0.94 |

\* n < 8: informational only, no pass/fail threshold.

## Recall@6 / MRR by document

| Document (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| doc1.pdf (48) | 1.00 / 0.95 | 0.92 / 0.68 | 1.00 / 0.96 | 1.00 / 0.97 | 1.00 / 0.97 |
| doc2.pdf (12) | 1.00 / 0.89 | 1.00 / 0.71 | 0.67 / 0.61 | 1.00 / 0.94 | 1.00 / 0.96 |
| doc3.pdf (20) | 1.00 / 1.00 | 0.75 / 0.73 | 1.00 / 1.00 | 0.95 / 0.95 | 0.95 / 0.95 |

## Rank of the first correct chunk per question (- = not in the 40 candidates)

| id | type | question | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|---|---|
| q01__formal | factual | Could you please state the year in which the ISO/IEC JTC 1/S | 1 | 1 | 1 | 1 | 1 |
| q01__casual | factual | so when did they set up the ISO/IEC JTC 1/SC42 AI subcommitt | 1 | 1 | 1 | 1 | 1 |
| q01__non_native | factual | In which year the ISO/IEC JTC 1/SC42 subcommittee for AI was | 1 | 1 | 1 | 1 | 1 |
| q01__typos | factual | When was the ISO/IEC JTC 1/SC42 subcomittee on AI setup? | 1 | 1 | 1 | 1 | 1 |
| q04__formal | factual | How many countries adopted the OECD principles on artificial | 1 | 1 | 1 | 1 | 1 |
| q04__casual | factual | how many countries signed up to the OECD AI principles when  | 1 | 1 | 1 | 1 | 1 |
| q04__non_native | factual | How much countries were adopting the OECD principles for AI  | 1 | 1 | 1 | 1 | 1 |
| q04__typos | factual | How many contries adopted the OECD principels for AI when th | 1 | 1 | 1 | 1 | 1 |
| q07__formal | factual | Could you explain how the F1-score is calculated? | 1 | 1 | 1 | 1 | 1 |
| q07__casual | factual | how do you work out the F1 score? | 1 | 12 | 1 | 1 | 1 |
| q07__non_native | factual | How the F1-score is calculate? | 1 | 2 | 1 | 1 | 1 |
| q07__typos | factual | How is the F1-scroe calcualted? | 1 | - | 1 | 1 | 1 |
| q13__formal | factual | Which three fundamental characteristics are considered desir | 1 | 1 | 1 | 1 | 1 |
| q13__casual | factual | what are the 3 basic things you want from XAI? | 1 | 1 | 1 | 1 | 1 |
| q13__non_native | factual | Which are the three basic characteristic that is desirable f | 1 | 1 | 1 | 1 | 1 |
| q13__typos | factual | What are the thre basic desireable XAI charcteristics? | 1 | 1 | 1 | 1 | 1 |
| d2q02__formal | factual | Which organisation is responsible for recommending the CODAT | 1 | 1 | 1 | 1 | 1 |
| d2q02__casual | factual | who actually recommends the CODATA values for the fundamenta | 1 | 2 | 2 | 1 | 1 |
| d2q02__non_native | factual | Which organization is recommend the CODATA values of fundame | 1 | 2 | 1 | 1 | 1 |
| d2q02__typos | factual | Which body recomends the CODATA values of the fundamantal co | 1 | 2 | 2 | 1 | 1 |
| d3q12__formal | factual | What blackbody temperature does the Sun exhibit at a wavelen | 1 | 2 | 1 | 1 | 1 |
| d3q12__casual | factual | what's the Sun's blackbody temperature at 1 mm? | 1 | 1 | 1 | 1 | 1 |
| d3q12__non_native | factual | Which blackbody temperature the Sun is showing at 1 mm wavel | 1 | 1 | 1 | 1 | 1 |
| d3q12__typos | factual | What blackbdy temprature does the Sun show at 1 mm wavelengh | 1 | 20 | 1 | 1 | 1 |
| q17__formal | paraphrase | When a model performs well on its training examples but pred | 1 | 1 | 1 | 1 | 1 |
| q17__casual | paraphrase | my model's great on the stuff it trained on but bad on new i | 1 | 10 | 1 | 1 | 1 |
| q17__non_native | paraphrase | A model is doing great on examples it learned but it make po | 1 | 3 | 1 | 3 | 3 |
| q17__typos | paraphrase | A model does grate on the examples it learnt from but makes  | 1 | 4 | 1 | 2 | 2 |
| q19__formal | paraphrase | What are the consequences when customer behaviour changes ov | 1 | 1 | 1 | 1 | 1 |
| q19__casual | paraphrase | what happens if customers start behaving differently over ti | 1 | 1 | 1 | 1 | 1 |
| q19__non_native | paraphrase | What is happening when the behaviour of customers is changin | 1 | 1 | 1 | 1 | 1 |
| q19__typos | paraphrase | What hapens when customer behavior changes over time but the | 1 | 1 | 1 | 1 | 1 |
| q21__formal | paraphrase | How can an image classifier be deceived by altering only a s | 1 | 1 | 1 | 1 | 1 |
| q21__casual | paraphrase | how do people trick an image classifier just by tweaking a f | 1 | 2 | 1 | 1 | 1 |
| q21__non_native | paraphrase | How somebody can fool the image classifier with changing few | 1 | 1 | 1 | 1 | 1 |
| q21__typos | paraphrase | How can someone fool an image clasifier by chaning a few pix | 1 | 3 | 1 | 1 | 1 |
| q26__formal | table | Within a confusion matrix, how does a false positive differ  | 1 | 1 | 1 | 1 | 1 |
| q26__casual | table | confusion matrix question: false positive vs false negative, | 1 | 1 | 1 | 1 | 1 |
| q26__non_native | table | In confusion matrix, what is difference between false positi | 1 | 1 | 1 | 1 | 1 |
| q26__typos | table | In a confusion matirx, what is the diffrence between a false | 1 | 1 | 1 | 1 | 1 |
| d2q05__formal | table | In CODATA 2022, is the elementary charge treated as an exact | 1 | 1 | 1 | 1 | 1 |
| d2q05__casual | table | is the elementary charge exact in CODATA 2022? and what's it | 2 | 1 | 1 | 1 | 1 |
| d2q05__non_native | table | In CODATA 2022 the elementary charge is exact constant or no | 1 | 1 | 1 | 1 | 1 |
| d2q05__typos | table | Is the elementry charge an exact constant in CODATA 2022, an | 1 | 1 | 1 | 1 | 1 |
| d3q04__formal | table | Which photographic emulsion is matched to the Airy disk of a | 1 | 1 | 1 | 1 | 1 |
| d3q04__casual | table | which photo emulsion goes with the Airy disk for an f/30 bea | 1 | 1 | 1 | 1 | 1 |
| d3q04__non_native | table | Which photographic emulsion is matching with Airy disk for f | 1 | 1 | 1 | 1 | 1 |
| d3q04__typos | table | Which photograhic emulsion matchs the Airy disk for an f/30  | 1 | 1 | 1 | 1 | 1 |
| q28__formal | figure | According to the ML workflow figure, which steps follow the  | 2 | 1 | 2 | 1 | 1 |
| q28__casual | figure | in the ML workflow diagram, what comes after testing the mod | 1 | 1 | 1 | 1 | 1 |
| q28__non_native | figure | In the figure of ML workflow, which steps are coming after t | 2 | 2 | 2 | 1 | 1 |
| q28__typos | figure | In the ML workflow figrue, which steps come after testng the | 2 | 4 | 2 | 1 | 1 |
| d3q08__formal | figure | Which power law has been fitted to the cosmic gamma-ray flux | 1 | 1 | 1 | 1 | 1 |
| d3q08__casual | figure | what power law did they fit to the cosmic gamma-ray flux dat | 1 | 1 | 1 | 1 | 1 |
| d3q08__non_native | figure | Which power law is fit to the data of cosmic gamma-ray flux? | 1 | 1 | 1 | 1 | 1 |
| d3q08__typos | figure | What power law is fited to the cosmic gama-ray flux data? | 1 | 1 | 1 | 1 | 1 |
| q29__formal | multi_page | Please list all of the test levels that apply to AI-based sy | 1 | 3 | 1 | 1 | 1 |
| q29__casual | multi_page | can you list all the test levels for AI-based systems? | 1 | 3 | 1 | 1 | 1 |
| q29__non_native | multi_page | Please give all test levels which are for AI-based systems. | 1 | 3 | 1 | 1 | 1 |
| q29__typos | multi_page | List all the test levles for AI-basd systems. | 4 | 14 | 2 | 1 | 1 |
| d3q18__formal | multi_page | According to the Large Orbital Telescope schedule, in which  | 1 | 1 | 1 | 1 | 1 |
| d3q18__casual | multi_page | in the Large Orbital Telescope schedule, what years are the  | 1 | 1 | 1 | 1 | 1 |
| d3q18__non_native | multi_page | In schedule of Large Orbital Telescope, which years are plan | 1 | 1 | 1 | 1 | 1 |
| d3q18__typos | multi_page | In the Large Orbital Telescope schedual, in which years are  | 1 | 1 | 1 | 1 | 1 |
| q32__formal | turkish | Veri zehirlenmesi (data poisoning) saldırısının ne olduğunu  | 1 | 3 | 1 | 1 | 1 |
| q32__casual | turkish | veri zehirlenmesi (data poisoning) saldırısı ne ya? | 1 | 3 | 1 | 1 | 1 |
| q32__no_diacritics | turkish | Veri zehirlenmesi (data poisoning) saldirisi nedir? | 1 | 3 | 1 | 1 | 1 |
| q32__typos | turkish | Veri zehirlenmsi (data poisoning) saldırıs nedir? | 1 | 3 | 1 | 1 | 1 |
| q34__formal | turkish | Dar yapay zekâ (narrow AI) ile genel yapay zekâ arasındaki f | 1 | 3 | 1 | 2 | 2 |
| q34__casual | turkish | dar yapay zeka (narrow AI) ile genel yapay zeka arasındaki f | 1 | 3 | 1 | 1 | 1 |
| q34__no_diacritics | turkish | Dar yapay zeka (narrow AI) ile genel yapay zeka arasindaki f | 1 | 3 | 1 | 1 | 1 |
| q34__typos | turkish | Dar yapay zek (narrow AI) ile genel yapay zeka arasındak far | 1 | 3 | 1 | 1 | 1 |
| d2q11__formal | turkish | CODATA 2022 verilerine göre boşlukta ışık hızının değeri ned | 1 | 2 | 13 | 1 | 1 |
| d2q11__casual | turkish | CODATA 2022'ye göre boşlukta ışık hızı kaç? | 1 | 2 | 12 | 1 | 1 |
| d2q11__no_diacritics | turkish | CODATA 2022'ye gore boslukta isik hizinin degeri nedir? | 5 | 2 | 7 | 4 | 2 |
| d2q11__typos | turkish | CODATA 2022'ye göre boşlukta ışık hızınn değei nedir? | 1 | 2 | 14 | 1 | 1 |
| d3q17__formal | turkish | Güneş'in manyetik aktivite döngüsü ile güneş lekesi döngüsün | 1 | - | 1 | 1 | 1 |
| d3q17__casual | turkish | güneşin manyetik aktivite döngüsü ve güneş lekesi döngüsü ka | 1 | - | 1 | 1 | 1 |
| d3q17__no_diacritics | turkish | Gunes'in manyetik aktivite dongusu ve gunes lekesi dongusu k | 1 | - | 1 | 27 | 27 |
| d3q17__typos | turkish | Güneş'in manyetk aktivite döngüsü ve güneş lekesi dönügsü ka | 1 | - | 1 | 1 | 1 |

## Top reranker score: questions with and without an answer in the documents

|  | mean | min | max |
|---|---|---|---|
| answerable | 0.790 | 0.000 | 1.000 |
| unanswerable | 0.011 | 0.000 | 0.082 |
