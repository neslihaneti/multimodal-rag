"""Hybrid search against a real PostgreSQL + pgvector, in a separate *_test database that the test empties first.

Locally it uses the connection settings in .env with database TEST_DATABASE_NAME (default rag_test, created if missing).
It is skipped when no database server is reachable.
"""
import math

import pytest

import db


def unit(*weights):
    """A 1024-dim unit vector with the given leading components."""
    v = list(weights) + [0.0] * (db_dim() - len(weights))
    norm = math.sqrt(sum(x * x for x in v))
    return [x / norm for x in v]


def db_dim():
    from model import EMBED_DIM
    return EMBED_DIM


@pytest.fixture(scope="module")
def chunks(test_db):
    """Four chunks whose vector order is A, B, C, D and whose keyword order for 'zebra' is D, C."""
    doc = db.insert_document("test.pdf", "hash-1")
    db.mark_document_done(doc)
    page = db.insert_page(doc, 1, "/tmp/1.png", "text", "text_layer")
    db.insert_chunks(page, [
        {"heading": "A", "content": "alpha section", "context": "", "embedding": unit(1, 0)},
        {"heading": "B", "content": "beta section", "context": "", "embedding": unit(1, 0.5)},
        {"heading": "C", "content": "gamma section about a zebra", "context": "", "embedding": unit(1, 1)},
        {"heading": "D", "content": "zebra zebra zebra delta", "context": "", "embedding": unit(1, 2)},
    ])
    # A chunk of a document that is still being indexed must never be returned
    unfinished = db.insert_document("half.pdf", "hash-2")
    db.insert_chunks(db.insert_page(unfinished, 1, "/tmp/2.png", "zebra", "ocr"),
                     [{"heading": "X", "content": "zebra", "context": "", "embedding": unit(1, 0)}])
    return {"query": unit(1, 0)}


def rrf(rankings, k=db.RRF_K):
    scores = {}
    for ranking in rankings:
        for rank, key in enumerate(ranking, 1):
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank)
    return scores


def test_dense_search_orders_by_cosine_similarity(chunks):
    assert [c["heading"] for c in db.dense_search(chunks["query"])] == ["A", "B", "C", "D"]


def test_keyword_search_orders_by_term_frequency(chunks):
    assert [c["heading"] for c in db.keyword_search("zebra")] == ["D", "C"]


def test_hybrid_search_matches_reciprocal_rank_fusion(chunks):
    results = db.hybrid_search("zebra", chunks["query"])
    expected = rrf([["A", "B", "C", "D"], ["D", "C"]])
    # D: 1/64 + 1/61 = 0.03202 beats C: 1/63 + 1/62 = 0.03200, then A: 1/61, then B: 1/62
    assert [c["heading"] for c in results] == sorted(expected, key=expected.get, reverse=True) == ["D", "C", "A", "B"]
    for c in results:
        assert float(c["score"]) == pytest.approx(expected[c["heading"]])


def test_hybrid_search_without_keyword_matches_equals_vector_order(chunks):
    results = db.hybrid_search("unicorn", chunks["query"])
    assert [c["heading"] for c in results] == ["A", "B", "C", "D"]


def test_hybrid_search_respects_the_limit(chunks):
    assert len(db.hybrid_search("zebra", chunks["query"], limit=2)) == 2


def test_unfinished_documents_are_not_returned(chunks):
    names = {c["file_name"] for c in db.hybrid_search("zebra", chunks["query"])}
    names |= {c["file_name"] for c in db.dense_search(chunks["query"])}
    names |= {c["file_name"] for c in db.keyword_search("zebra")}
    assert names == {"test.pdf"}
