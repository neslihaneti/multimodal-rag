"""Agentic search must stop after MAX_SEARCH_ROUNDS searches whatever the model says."""
import itertools

import pytest

import rag


@pytest.fixture
def searches(monkeypatch):
    calls, ids = [], itertools.count(1)

    def fake_retrieve(query, top_k=rag.TOP_K):
        calls.append(query)
        return [{"id": next(ids), "file_name": "doc.pdf", "page_number": 1, "heading": "", "content": query, "context": ""}]

    monkeypatch.setattr(rag, "retrieve", fake_retrieve)
    monkeypatch.setattr(rag, "rerank", lambda query, chunks: chunks)
    return calls


def model_says(monkeypatch, replies):
    replies = iter(replies)
    prompts = []

    def fake_generate(prompt, images=(), system=None, max_new_tokens=1024):
        prompts.append(prompt)
        return next(replies)

    monkeypatch.setattr(rag, "generate", fake_generate)
    return prompts


def test_stops_after_max_rounds_even_if_the_model_keeps_asking(monkeypatch, searches):
    prompts = model_says(monkeypatch, (f"SEARCH: query {i}" for i in itertools.count()))
    chunks, queries = rag.agentic_search("question")
    assert len(searches) == rag.MAX_SEARCH_ROUNDS == 3
    assert len(prompts) == rag.MAX_SEARCH_ROUNDS - 1  # no decision is asked after the last search
    assert queries == ["question", "query 0", "query 1"]
    assert len(chunks) == 3


def test_enough_stops_after_one_search(monkeypatch, searches):
    model_says(monkeypatch, ["ENOUGH"])
    _, queries = rag.agentic_search("question")
    assert searches == ["question"]
    assert queries == ["question"]


def test_repeated_query_stops_the_loop(monkeypatch, searches):
    model_says(monkeypatch, ["SEARCH: question"])
    rag.agentic_search("question")
    assert len(searches) == 1


def test_unparseable_reply_stops_the_loop(monkeypatch, searches):
    model_says(monkeypatch, ["I think the results look fine."])
    rag.agentic_search("question")
    assert len(searches) == 1


def test_no_results_stops_without_asking_the_model(monkeypatch):
    monkeypatch.setattr(rag, "retrieve", lambda query, top_k=rag.TOP_K: [])
    prompts = model_says(monkeypatch, [])
    assert rag.agentic_search("question") == ([], ["question"])
    assert prompts == []


def test_decision_prompt_is_kept_under_the_token_budget(monkeypatch):
    found = [{"id": i, "file_name": "doc.pdf", "page_number": i, "heading": "", "content": f"chunk {i} " + "x" * 4000, "context": ""}
             for i in range(1, 7)]
    monkeypatch.setattr(rag, "retrieve", lambda query, top_k=rag.TOP_K: found)
    monkeypatch.setattr(rag, "rerank", lambda query, chunks: chunks)
    monkeypatch.setattr(rag, "count_tokens", lambda prompt, images=(), system=None: len(prompt) // 4)
    monkeypatch.setattr(rag, "PROMPT_TOKEN_BUDGET", 2500)  # about two of the 1,000-token chunks
    prompts = model_says(monkeypatch, ["ENOUGH"])
    chunks, _ = rag.agentic_search("question")
    assert "chunk 2 " in prompts[0] and "chunk 3 " not in prompts[0]
    assert len(chunks) == 6  # only the decision prompt is trimmed; the answer step fits its own prompt


@pytest.mark.parametrize("score, decisions", [(0.9, 0), (0.2, 1)])
def test_high_rerank_score_skips_the_decision(monkeypatch, searches, score, decisions):
    monkeypatch.setattr(rag, "ENOUGH_SCORE", 0.5)
    monkeypatch.setattr(rag, "rerank", lambda query, chunks: [dict(c, rerank_score=score) for c in chunks])
    prompts = model_says(monkeypatch, ["ENOUGH"])
    rag.agentic_search("question")
    assert len(prompts) == decisions and len(searches) == 1

