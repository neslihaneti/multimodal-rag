# Tests and evaluation

| Layer | What it checks | Where it runs | Command |
|---|---|---|---|
| Unit | text layer vs OCR decision, heading chunking, agentic search stops after 3 rounds, `[n]` citations → source pages, context-sentence guard | CI and Mac, < 1 s | `pytest` |
| Integration | dense, keyword and hybrid (RRF) search against a real pgvector, compared with RRF computed in Python | CI (pgvector service) and Mac (Docker) | `pytest` |
| Security (e2e) | prompt injection hidden in a PDF (white text and a visible "note to AI systems") must not be followed at index or answer time | Mac, real models, ~1 min | `pytest tests/e2e/test_prompt_injection.py` |
| UI (e2e) | Streamlit loads, a question gets an answer, source images load, search details open | Mac, real models, ~5 min | `pytest tests/e2e/test_ui.py` |
| Retrieval eval | Recall@1, Recall@6, MRR for vector, keyword, hybrid and reranked search on the golden set | Mac, ~3 min | `python evaluate.py retrieval` |
| Answer eval | correctness, faithfulness, citation precision, refusals on unanswerable questions, latency | Mac, ~1 h | `python evaluate.py answers` |

- The golden set is [`eval/golden_doc1.jsonl`](../eval/golden_doc1.jsonl): 45 questions about doc1.pdf (factual, paraphrased,
  Turkish, table, figure, multi-page and 8 that the document cannot answer), each with its expected answer and pages.
- Unit tests replace the models with [`tests/stubs.py`](stubs.py), so they need neither torch nor a GPU.
- Database tests use separate `*_test` databases and refuse to run against any other name; the real index is never touched.
- The answer judge is the same local model (Qwen3-VL-4B), so no document text leaves the machine. A 4B judge can be wrong:
  label some rows of `reports/<run>-judgments.jsonl` (`"human": true/false`) and run
  `python evaluate.py calibrate reports/<run>-judgments.jsonl` to see how often it agrees with you.
- Each evaluation writes `reports/<date>-<kind>.md` and `.json` with the settings it ran with, so runs can be compared.

Setup for the full local run: `pip install -r requirements-dev.txt && playwright install chromium`, Docker with the
`pgvector_db` container running, and doc1.pdf indexed.
