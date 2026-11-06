# Local Multimodal RAG over PDFs

Ask questions about your own PDF documents in Turkish or English and get answers that cite the page each sentence comes
from. Everything runs on one machine: no document text leaves it.

**Portfolio:** https://neslihaneti.github.io/multimodal-rag/ · [Model card](docs/MODEL_CARD.md) ·
[NIST AI RMF self-assessment](docs/NIST_AI_RMF.md) · [Phase reports](phases/README.md)

## How it works

1. **Indexing** (`indexer.py`, `file_processing.py`): each page is rendered to PNG. Born-digital text is read with
   Docling; scanned pages, or pages where an image covers ≥ 30 %, go through Chandra OCR 2. Text is split by headings
   into chunks of at most 1,500 characters (tables keep their header) and stored in PostgreSQL with pgvector.
2. **Search** (`db.py`, `rag.py`): vector search (bge-m3, HNSW) and full-text search fused with Reciprocal Rank Fusion
   in one SQL query, top 40 reranked with bge-reranker-v2-m3. If the best result is weak, the model decides whether to
   search again with a new query (up to 3 rounds).
3. **Answer** (`rag.py`, `model.py`): Qwen3-VL-4B reads the 6 best excerpts and 2 page images (prompt ≤ 9,000 tokens)
   and ends every sentence with excerpt numbers, which become source pages in the UI. Refusals are replaced in code by
   a fixed sentence without citations, in the answer language.
4. **UI** (`app.py`): Streamlit, answer streamed, cited page images and search details shown.

## Results

Measured on a sealed holdout set of 72 questions, run once after all development
([report](phases/final/RAPOR.md)):

| | Result |
|---|---|
| Retrieval Recall@6 / Recall@1 / MRR | 0.98 / 0.89 / 0.934 |
| Answer correctness | 0.91 |
| Faithfulness (claims supported by the cited excerpts) | 0.94 (0.958 human-checked) |
| Citation precision / expected page cited | 0.87 / 0.95 |
| Unanswerable questions refused | 15 / 15, no citation |
| Latency p50 / p95, time to first text p50 | 22.2 s / 40.4 s, 15.2 s |

The judge is the same local model, checked against human labels (Cohen's κ 0.79–1.00). Turkish questions are the
weakest group (0.70 correct); see the [model card](docs/MODEL_CARD.md) for limitations.

## Run it

Requirements: Python 3.12, Docker, Apple Silicon (MPS) or CUDA. The models take ~50 GB of memory at peak.

```bash
pip install -r requirements.txt
docker run -d --name pgvector_db -p 5433:5432 -e POSTGRES_PASSWORD=<password> pgvector/pgvector:pg17
```

Create `.env` (not committed):

```
database_name=rag
usr_name=postgres
usr_password=<password>
host=localhost
port=5433
```

Then `streamlit run app.py`, enter a folder of PDFs in the sidebar and press **Extract & Index PDFs**.

## Tests and evaluation

```bash
pytest                                   # unit + database integration, < 1 s, models stubbed (also in CI)
pytest tests/e2e                         # prompt injection, refusal judge, Playwright UI (real models)
python3 evaluate.py retrieval            # Recall@k and MRR for 5 search methods
python3 evaluate.py answers              # correctness, faithfulness, citations, refusals, latency
python3 evaluate.py calibrate <run>-judgments.jsonl   # judge vs. human labels
```

Details: [tests/README.md](tests/README.md). Every change was made as a measured phase with its own report in
[`phases/`](phases/README.md); difficulties and lessons are logged in [`phases/ZORLUKLAR.md`](phases/ZORLUKLAR.md)
(phase reports are in Turkish).
