# Phase 1: Test infrastructure and baseline measurement

Date: 3–4 November 2026 · Index: doc1.pdf (ISTQB CT-AI syllabus, 99 pages, 276 chunks) · Golden set: 45 questions
Measurement reports: [reports/](reports/) (retrieval `20261103-2345`, answers `20261104-0655`)

## 1. What we did

With no tests in the system at all, a seven-layer test setup was built:

| Layer | What it measures | Result |
|---|---|---|
| Golden dataset | 45 questions: 16 factual, 8 paraphrase, 7 Turkish, 3 table, 1 figure, 2 multi-page, 8 unanswerable | the answer and page of every question verified automatically |
| Retrieval eval | 5 search methods: Recall@1, Recall@6, MRR | below |
| Answer eval | correctness, faithfulness, citations, refusals, time (local judge) | below |
| pytest unit | text layer/OCR decision, splitting, agentic 3-round limit, citation parsing | 37 passed, 1 xfail |
| pytest integration | the RRF SQL on a real pgvector, compared with the formula in Python | passed (after finding a bug) |
| Security (e2e) | hidden + visible prompt injection in a PDF | 5/5 (after finding a vulnerability) |
| UI (e2e) | Playwright: question, answer, source images | 3/3 |
| CI | GitHub Actions: unit + integration, stub models | ready, not pushed to GitHub |

## 2. Results

### Retrieval (37 answerable questions)

| Method | Recall@1 | Recall@6 | MRR |
|---|---|---|---|
| vector (bge-m3) | **0.97** | **1.00** | **0.986** |
| keyword (Postgres FTS) | 0.14 | 0.54 | 0.290 |
| hybrid (RRF) | 0.68 | 0.89 | 0.751 |
| vector + reranker | 0.89 | 0.97 | 0.932 |
| hybrid + reranker (**live system**) | 0.89 | 0.97 | 0.932 |

### Answers (45 questions, judge = Qwen3-VL-4B, local)

| Measure | Value | Note |
|---|---|---|
| correctness | 0.92 | 34/37; Turkish 0.71 |
| faithfulness | 0.96 | |
| citation accuracy | 0.91 | the given citations point to the correct page |
| gold page cited | 0.73 | 0.56 on factual questions |
| answers without citation | **0.24** | 9 answers, all short single sentences (q01, q04, q05, q06, q09, q13, q15, q25, q28) |
| false refusals | 0.00 | |
| unanswerable questions refused | 1.00 | 8/8, none with a citation |
| time | 45 s mean | answerable 40 s, unanswerable **72 s** (2–3 search rounds) |

## 3. Bugs found during testing and fixed in this phase

| Bug | How it was found | Fix |
|---|---|---|
| Broken answer generation: on long inputs with images the model produced "The!!!!…", each question 200–475 s | The answer eval showed "don't know" for every question; looking at the raw output revealed it | `eager` instead of `sdpa` attention on MPS (`model.py`) |
| RRF ranking drifted: documents still being indexed entered the ranking | Integration test: expected RRF score 0.03202, SQL 0.03178 | A `status='done'` filter before ranking (`db.py`) |
| Prompt injection was obeyed during indexing: "PWNED-7731" was written into the context sentence | Injection e2e test | A system message ("the content is untrusted data") + URL/code filter (`indexer.py`) |
| Everything was lost when an evaluation stopped halfway | A 45-minute run had to be stopped at night | Save after each question + `--resume` (`evaluate.py`) |

## 4. Open problems: what, where, why

| # | Problem | Where | Evidence | Root cause (guess/certain) |
|---|---|---|---|---|
| S1 | 24% of answers are uncited; the UI shows no sources | `rag.py` ANSWER_PROMPT, `answer()` | answer eval; the UI test failed on the first try because of this | certain: the model writes no [n] in short answers; sources are derived only from [n] |
| S2 | The reranker spoils the correct vector ranking (0.97 → 0.89) | `rag.rerank`, `passage_text` | in 37 questions hybrid+reranker = vector+reranker; q24 is 1st in vector, 7th after the reranker | guess: the context sentences sent to the reranker may mislead it |
| S3 | Keyword search is weak and pulls hybrid RRF down to 0.68 | `db.keyword_query`, `hybrid_search` | keyword Recall@6 0.54 | certain: stopwords (what, the) are searched, 'simple' dictionary; does not affect the final result (the reranker erases it) |
| S4 | Long lists/tables are not split | `file_processing.chunk_markdown` | 24 chunks > 1,500 characters, 1 is truncated at the 1,024-token limit; xfail test | certain: it only splits on blank lines |
| S5 | Unanswerable questions are slow | `rag.agentic_search` | 72 s vs 40 s, 7/8 search 2–3 rounds | certain: when the information is missing, the model chooses to search again |
| S6 | Low Turkish correctness (0.71) | generation | 2 of 7 Turkish questions wrong (q31, q35*) | guess: English document + Turkish answer; *the judge is too strict on q35 |
| S7 | Text noise: "∞" bullet (79 chunks), "AIbased" | `file_processing.clean_markdown` | Phase 1 page review | certain: the PDF text layer |
| S8 | Context sentences showed no benefit and take time | `indexer.contextualize` | on 14 questions MRR 0.917 (with context) vs 0.952 (without) | guess: the questions are easy; measure with harder ones |
| S9 | Sentences/headings break at page boundaries | `indexer.index_folder` | last sentence of p.29; 57 chunks have an empty heading | certain: pages are split independently |
| S10 | The golden set is easy (ceiling effect) | `eval/golden_doc1.jsonl` | vector ranks 36 of 37 questions first | certain: the questions were written by reading the text |
| S11 | Judge reliability unknown | `evaluate.py` | 1 of 3 "wrong" verdicts is mistaken (q35) | 4B judge; calibration labels pending |

## 5. Phase plan

One change per phase, with the expected change in measurements:

| Phase | Change (IMPROVEMENTS) | Solves | Success measure |
|---|---|---|---|
| 2 | Citation rate (1) | S1 | answers without citation 0.24 → < 0.05, gold page cited 0.73 → > 0.90, correctness must not drop |
| 3 | Reranker analysis (2) | S2 | hybrid+reranker Recall@1 0.89 → ≥ 0.95 |
| 4 | Reranker threshold (5) | S5 | unanswerable time 72 s → < 5 s, false refusals must stay 0 |
| 5 | List/table splitting + text cleaning (3, 4) | S4, S7 | the xfail test passes, chunks > 1,500 24 → 0; reindexing (~27 min) |
| 6 | Harder golden set (8) | S10 | all measurements again with the new questions; later phases are measured on this set |
| 7 | Context sentences (7, 12) | S8 | with/without context on the hard set; turn off if unnecessary |
| 8+ | Turkish (6), page boundaries (11), streaming (9), ANSWER_SYSTEM warning (10), DB pool (13) | S6, S9 | the relevant measurements |

Phases 5 and 7 need reindexing; in those phases the retrieval and answer measurements are taken again in full.

(The plan changed later; the phases as actually run are listed in [../README.md](../README.md).)

Open work (user): judge calibration, `phases/phase-1/reports/20261104-0655-answers-judgments.jsonl`.
