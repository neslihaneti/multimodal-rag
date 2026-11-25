# Retrieval evaluation

- **time**: 2026-11-24T16:29:36
- **golden**: holdout_stereotype.jsonl
- **golden_sha256**: 3b2dfc15e8b1
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

## Overall (2 answerable questions)

| Method | Recall@1 | Recall@6 | MRR | All pages@6 (multi-page) |
|---|---|---|---|---|
| vector | 0.50 | 1.00 | 0.750 | - |
| keyword | 1.00 | 1.00 | 1.000 | - |
| hybrid (RRF) | 1.00 | 1.00 | 1.000 | - |
| vector + reranker | 1.00 | 1.00 | 1.000 | - |
| hybrid + reranker | 1.00 | 1.00 | 1.000 | - |

## Recall@6 by question type

| Type (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| bias_control (2) * | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

\* n < 8: informational only, no pass/fail threshold.

## Recall@6 / MRR by document

| Document (n) | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|
| doc1.pdf (2) * | 1.00 / 0.75 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |

## Rank of the first correct chunk per question (- = not in the 40 candidates)

| id | type | question | vector | keyword | hybrid (RRF) | vector + reranker | hybrid + reranker |
|---|---|---|---|---|---|---|---|
| b04 | bias_control | How can data chosen to support diversity be fair but not bal | 1 | 1 | 1 | 1 | 1 |
| b05 | bias_control | Why might demographic data be collected when testing for ina | 2 | 1 | 1 | 1 | 1 |

## Top reranker score: questions with and without an answer in the documents

|  | mean | min | max |
|---|---|---|---|
| answerable | 0.970 | 0.956 | 0.983 |
| unanswerable | 0.045 | 0.000 | 0.237 |
