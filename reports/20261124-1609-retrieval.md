# Retrieval evaluation

- **time**: 2026-11-24T16:09:34
- **golden**: holdout_style.jsonl
- **golden_sha256**: af5ec406eede
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

## Overall (40 answerable questions)

| Method | Recall@1 | Recall@6 | MRR | All pages@6 (multi-page) |
|---|---|---|---|---|
| vector | 0.93 | 1.00 | 0.948 | - |
| keyword | 0.55 | 0.85 | 0.686 | - |
| hybrid (RRF) | 0.80 | 0.97 | 0.889 | - |
| vector + reranker | 0.85 | 1.00 | 0.917 | - |
| hybrid + reranker | 0.85 | 1.00 | 0.917 | - |

## Recall@6 by question type

| Type (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| factual (12) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| figure (4) * | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| multi_page (4) * | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| paraphrase (8) | 1.00 | 0.75 | 0.88 | 1.00 | 1.00 |
| table (4) * | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| turkish (8) | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## Recall@6 / MRR by document

| Document (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| doc1.pdf (12) | 1.00 / 1.00 | 1.00 / 0.69 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| doc2.pdf (4) * | 1.00 / 1.00 | 1.00 / 0.62 | 1.00 / 0.50 | 1.00 / 0.50 | 1.00 / 0.50 |
| doc3.pdf (24) | 1.00 / 0.91 | 0.75 / 0.69 | 0.96 / 0.90 | 1.00 / 0.94 | 1.00 / 0.94 |

## Rank of the first correct chunk per question (- = not in the 40 candidates)

| id | type | question | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|---|---|
| q09__formal | factual | By what other name is back-to-back testing known? | 1 | 1 | 1 | 1 | 1 |
| q09__casual | factual | what's another name for back-to-back testing? | 1 | 2 | 1 | 1 | 1 |
| q09__non_native | factual | How is back-to-back testing also called? | 1 | 2 | 1 | 1 | 1 |
| q09__typos | factual | What is back-to-back testing also knwon as? | 1 | 2 | 1 | 1 | 1 |
| d2q09__formal | factual | What is the 2022 recommended value of the inverse of the fin | 1 | 2 | 2 | 2 | 2 |
| d2q09__casual | factual | what's the 2022 recommended value for the inverse fine-struc | 1 | 2 | 2 | 2 | 2 |
| d2q09__non_native | factual | Which is the 2022 recommended value of inverse fine-structur | 1 | 2 | 2 | 2 | 2 |
| d2q09__typos | factual | What is the 2022 recomended value of the inverse fine-struct | 1 | 1 | 2 | 2 | 2 |
| d3q20__formal | factual | Which physical process is represented by the gamma-ray line  | 1 | 1 | 1 | 1 | 1 |
| d3q20__casual | factual | what process is behind the 0.5 MeV gamma-ray line? | 2 | 1 | 1 | 1 | 1 |
| d3q20__non_native | factual | Which process is represented from the gamma-ray line at 0.5  | 1 | 1 | 1 | 1 | 1 |
| d3q20__typos | factual | What proces does the gamma-ray line at 0.5 MeV represnt? | 1 | 1 | 1 | 1 | 1 |
| q23__formal | paraphrase | Which type of learning is used to segment customers for mark | 1 | 1 | 1 | 1 | 1 |
| q23__casual | paraphrase | what kind of learning do you use to group customers for mark | 1 | 1 | 1 | 1 | 1 |
| q23__non_native | paraphrase | Which kind of learning is using for grouping the customers f | 1 | 1 | 1 | 1 | 1 |
| q23__typos | paraphrase | Which kind of lerning is used to group custmers for marketin | 1 | 1 | 1 | 1 | 1 |
| d3q13__formal | paraphrase | Why should solar observations from space and from the ground | 6 | - | 21 | 1 | 1 |
| d3q13__casual | paraphrase | why shouldn't we see observing the Sun from space and from t | 1 | 6 | 2 | 1 | 1 |
| d3q13__non_native | paraphrase | Why the observing of Sun from space and from ground should n | 1 | 8 | 2 | 1 | 1 |
| d3q13__typos | paraphrase | Why should obseving the Sun from space and from the ground n | 4 | 3 | 2 | 2 | 2 |
| d3q10__formal | table | What is the shortest wavelength at which the 15 ft Aerospace | 1 | 1 | 1 | 1 | 1 |
| d3q10__casual | table | what's the shortest wavelength the 15 ft Aerospace Corp. ref | 1 | 1 | 1 | 1 | 1 |
| d3q10__non_native | table | Which is the most short wavelength where the 15 ft Aerospace | 1 | 1 | 1 | 1 | 1 |
| d3q10__typos | table | What is the shortest wavelenght at which the 15 ft Aerospace | 1 | 1 | 1 | 1 | 1 |
| d3q09__formal | figure | Which two mirror geometries are employed in the grazing inci | 1 | 1 | 1 | 1 | 1 |
| d3q09__casual | figure | what two mirror shapes does the grazing incidence x-ray tele | 1 | 1 | 1 | 1 | 1 |
| d3q09__non_native | figure | Which two shapes of mirror are using in the grazing incidenc | 1 | 1 | 1 | 1 | 1 |
| d3q09__typos | figure | Which two miror shapes are used in the grazing incidense x-r | 1 | 1 | 1 | 1 | 1 |
| d3q19__formal | multi_page | Regarding the high-resolution broad-band antenna in Recommen | 1 | 1 | 1 | 1 | 1 |
| d3q19__casual | multi_page | for the high-res broad-band antenna in Recommendation 3, how | 1 | 1 | 1 | 1 | 1 |
| d3q19__non_native | multi_page | For high-resolution broad-band antenna of Recommendation 3,  | 1 | 1 | 1 | 1 | 1 |
| d3q19__typos | multi_page | For the high-resolution broad-band antena of Recommendation  | 1 | 1 | 1 | 1 | 1 |
| q35__formal | turkish | Eşli test (pairwise testing) hangi amaçla kullanılmaktadır? | 1 | 2 | 1 | 1 | 1 |
| q35__casual | turkish | eşli test (pairwise testing) niye kullanılıyor? | 1 | 2 | 1 | 1 | 1 |
| q35__no_diacritics | turkish | Esli test (pairwise testing) neden kullanilir? | 1 | 2 | 1 | 1 | 1 |
| q35__typos | turkish | Eşli tet (pairwise testing) nedn kullanılır? | 1 | 3 | 1 | 1 | 1 |
| d3q16__formal | turkish | Fizik çalışma grubu, uzay ortamının hangi temel özelliklerin | 1 | - | 1 | 1 | 1 |
| d3q16__casual | turkish | fizik çalışma grubu uzay ortamıyla ilgili hangi temel özelli | 1 | - | 1 | 1 | 1 |
| d3q16__no_diacritics | turkish | Fizik calisma grubu uzay ortaminin hangi temel ozelliklerini | 1 | - | 1 | 6 | 6 |
| d3q16__typos | turkish | Fizik çalışma grubu uzay ortamının hangi temel özelliklerni  | 1 | - | 1 | 1 | 1 |

## Top reranker score: questions with and without an answer in the documents

|  | mean | min | max |
|---|---|---|---|
| answerable | 0.771 | 0.001 | 1.000 |
| unanswerable | 0.061 | 0.000 | 0.258 |
