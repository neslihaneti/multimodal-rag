# Model Card: Local Multimodal RAG over PDF Documents

A system card in the style of *Model Cards for Model Reporting* (Mitchell et al., 2019). It describes the whole
retrieval-augmented system, not a newly trained model: no model was trained or fine-tuned in this project.

## System details

| | |
|---|---|
| Purpose | Answer questions about a user's own PDF documents, citing the page each sentence is based on |
| Answer model | `Qwen/Qwen3-VL-4B-Instruct` (bf16, eager attention computed in 1,024-query blocks) |
| OCR | `datalab-to/chandra-ocr-2`, only for scanned pages or pages where an image covers ≥ 30 % |
| Embeddings / reranker | `BAAI/bge-m3` (1024-d) / `BAAI/bge-reranker-v2-m3` |
| Search | PostgreSQL 17 + pgvector: HNSW vector search and full-text search fused with RRF (k = 60), top 40 reranked, top 6 to the model; up to 3 search rounds |
| Prompt | 6 excerpts + 2 page images (896 px), at most 9,000 tokens |
| Runtime | One Apple Silicon Mac (128 GB unified memory, MPS). No data leaves the machine; no cloud API |
| Interface | Streamlit, answers streamed, source page images and search details shown |

## Intended use

- One person asking factual questions about documents they indexed themselves, in Turkish or English.
- Answers that must be checked against their sources: every answer sentence ends with excerpt numbers and the cited
  page images are shown.

## Out of scope

- Decisions with legal, medical, financial or safety consequences without a person checking the cited pages.
- Questions about anything outside the indexed documents: the system is built to refuse them.
- Several users or a public server: one process, one database, no authentication or rate limiting.
- Languages other than Turkish and English (not evaluated).

## Evaluation

Golden sets written in advance. The development set (82 questions on 3 documents) was used for every change; the
final holdout set (72 questions, written by the project owner) was opened once, after all changes, and no setting was
changed on its results. Success thresholds were agreed before the work began (`phases/BASARI_TANIMI.md`).

Documents: an ISTQB AI-testing syllabus (99 pages, born-digital), the CODATA 2022 fundamental constants report
(62 pages, equations and tables), a 1966 scanned space research report (200 pages, OCR).

### Final holdout (5 November 2026)

| Metric | Threshold | Result |
|---|---|---|
| Recall@6 / Recall@1 / MRR | ≥ 0.90 / ≥ 0.80 / ≥ 0.85 | 0.98 / 0.89 / 0.934 |
| Answer correctness | ≥ 0.85 | 0.91 (52 / 57) |
| Faithfulness (claims supported by cited excerpts) | ≥ 0.92 | 0.94 (0.958 with human labels) |
| Citation precision / gold page cited | ≥ 0.80 / ≥ 0.85 | 0.87 / 0.95 |
| Answers without citation | ≤ 0.05 | 0.00 |
| Unanswerable questions refused / refusals with a citation | ≥ 0.90 / 0.00 | 1.00 (15 / 15) / 0.00 |
| False refusals | ≤ 0.05 | 0.02 |
| Latency p50 / p95 | ≤ 30 / ≤ 60 s | 22.2 / 40.4 s |
| Time to first text p50 | ≤ 15 s (revised from ≤ 10 s) | 15.2 s: 0.2 s over, accepted by the owner |

The judge is the same local 4B model. It was checked against human labels on 90 stratified decisions of the final
run: agreement / Cohen's κ 0.93 / 0.79 (claim supported), 1.00 / 1.00 (correct), 1.00 / 1.00 (refusal).

### By subgroup (final holdout)

| Question type | n | Correct | Gold page cited |
|---|---|---|---|
| factual / paraphrase / table | 10 / 10 / 10 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 |
| figure | 9 | 0.89 | 1.00 |
| multi-page | 8 | 0.88 | 1.00 |
| **Turkish** | 10 | **0.70** | **0.70** |

## Known limitations

- **Turkish questions are the weakest group** (0.70 correct on the holdout). Causes found after the holdout:
  answers sometimes in English, Turkish-only terms not finding English passages, no Turkish stemming in full-text
  search. Two of these were addressed after the holdout (see *Changes after the final holdout*); the holdout result
  above is unchanged.
- **Repetition loops:** on a few long table questions the 4B model repeats a sentence until the token limit
  (up to ~150 s). Decoding penalties were rejected because they changed numbers copied from the sources.
- **Attribution drift:** a correct fact is sometimes cited to a neighbouring excerpt instead of the one it came from.
- **Judge:** a 4B local model; its "unsupported" verdicts include false negatives (7 of 16 in a human audit), so raw
  faithfulness understates the human-checked value.
- **Hardware bound:** latency and memory were measured on one 128 GB Mac; a single answer can peak at ~50–58 GB of process memory (physical footprint reported by macOS `footprint`, which includes MPS allocations; how much of it is cached rather than live tensors was not measured).

## Safety and security

- Indirect prompt injection: a test PDF with hidden white text and a fake "note to AI systems" is indexed in the
  end-to-end tests; the canary and fake URL must not reach the stored context or the answer (3 tests, passing).
- Refusals are replaced in code by a fixed sentence without citations, in the answer language.
- Credentials stay in `.env`, outside version control; tests only use databases whose name ends in `_test`.

## Changes after the final holdout

Measured on the development set only; the holdout was not run again.

- **Phase 9:** answer language set in code (the question's language, or the language explicitly asked for); Turkish
  questions answered in English 1 → 0, correctness unchanged (0.97).
- **Phase 10 (tried, rolled back):** searching Turkish queries also with an English translation raised dev
  correctness to 0.99 (Turkish 12 / 12) but made Turkish questions ~9 s slower to first text, over the latency
  thresholds. The released code is Phase 9. Details: `phases/faz-10/RAPOR.md`.

## Reproducing

`python3 evaluate.py retrieval|answers --golden eval/golden_final.jsonl`; each run writes a dated report with the
model names, prompt and judge hashes, and settings to `reports/`. Phase reports: `phases/`.
