"""How rag.answer turns [n] markers in the model's text into source pages."""
import json
import os

import pytest
from PIL import Image

import rag

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def chunks(tmp_path, monkeypatch):
    image = tmp_path / "page.png"
    Image.new("RGB", (20, 20)).save(image)
    found = [{"id": i, "file_name": "doc1.pdf", "page_number": page, "image_path": str(image), "heading": "",
              "content": f"chunk {i}", "context": "", "rerank_score": 0.9} for i, page in enumerate([50, 51, 50], 1)]
    monkeypatch.setattr(rag, "agentic_search", lambda query: (found, [query]))
    return found


def stream_of(text, closed=None):
    """The model's text in pieces of 3 characters, like a streamer; `closed` records that the reader stopped early."""
    def pieces(prompt, images=(), system=None, max_new_tokens=1024, options=None):
        try:
            for i in range(0, len(text), 3):
                yield text[i:i + 3]
        except GeneratorExit:
            if closed is not None:
                closed.append(True)
            raise
    return pieces


def answer_with(monkeypatch, text, question="What are the test levels?"):
    monkeypatch.setattr(rag, "generate_stream", stream_of(text))
    return rag.answer(question)


def test_cited_numbers_become_source_pages(monkeypatch, chunks):
    result = answer_with(monkeypatch, "Input data testing [2] and ML model testing [1].")
    assert [s["page_number"] for s in result["sources"]] == [51, 50]


def test_same_page_cited_twice_is_listed_once(monkeypatch, chunks):
    result = answer_with(monkeypatch, "A [1]. B [3].")  # chunks 1 and 3 are both on page 50
    assert [s["page_number"] for s in result["sources"]] == [50]


def test_out_of_range_citations_are_ignored(monkeypatch, chunks):
    result = answer_with(monkeypatch, "Something [7] and [0].")
    assert result["sources"] == []


@pytest.mark.parametrize("text", [
    "The documents do not contain information about the exam price [1].",
    "Belgelerde bu konuda bilgi bulunmamaktadır [2].",
])
def test_not_found_answer_has_no_sources(monkeypatch, chunks, text):
    assert answer_with(monkeypatch, text)["sources"] == []


@pytest.mark.parametrize("question, text, expected", [
    ("What is the capital of Australia?", "The documents do not contain information about this [1][2][3][4][5][6].", rag.REFUSAL["en"]),
    ("Kubernetes'te bir pod nasıl yeniden başlatılır?", "The documents do not contain information about this.", rag.REFUSAL["tr"]),
    ("Raporda pulsarların keşfi hakkında ne söyleniyor?", "Belgelerde bu bilgi yer almıyor [2].", rag.REFUSAL["tr"]),
    ("When was Hubble launched?", "The documents do not contain information about Hubble. The report discusses the LOT [3].", rag.REFUSAL["en"]),
])
def test_refusal_becomes_the_fixed_sentence_in_the_question_language(monkeypatch, chunks, question, text, expected):
    result = answer_with(monkeypatch, text, question)
    assert result["answer"] == expected and result["sources"] == []
    # the generation stops once the first sentence shows a refusal: raw_answer is what the model wrote until then
    assert text.startswith(result["raw_answer"]) and rag.is_refusal(result["raw_answer"])


def test_refusal_after_a_partial_answer_keeps_the_text(monkeypatch, chunks):
    text = "Input data testing is a test level [2]. The exam price is not mentioned."
    assert answer_with(monkeypatch, text)["answer"] == text


@pytest.mark.parametrize("sentence", list(rag.REFUSAL.values()))
def test_fixed_refusal_sentences_are_recognised_as_refusals(sentence):
    assert rag.is_refusal(sentence) and rag.NOT_FOUND.search(sentence)


def test_question_language_matches_the_golden_set():
    with open(os.path.join(ROOT, "eval", "golden_dev.jsonl"), encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]
    assert [(q["id"], rag.question_language(q["question"])) for q in items] == [(q["id"], q["lang"]) for q in items]


@pytest.mark.parametrize("question, language, searched", [
    ("Yapay zeka tabanlı sistemlerde kavram kayması (concept drift) nedir?", "tr", None),
    ("What is concept drift and how is it tested?", "en", None),
    ("Kavram kayması nedir? İngilizce cevap ver.", "en", "Kavram kayması nedir?"),
    ("Kavram kayması nedir, ingilizce olarak açıklar mısın?", "en", None),
    ("What is concept drift? Please answer in Turkish.", "tr", "What is concept drift?"),
    ("Explain concept drift in Turkish", "tr", "Explain concept drift"),
    ("Türkçe keyword araması neden zayıf?", "tr", None),  # "Türkçe" as a topic, not a request
])
def test_answer_language_and_the_searched_question(question, language, searched):
    assert rag.answer_language(question) == language
    if searched:
        assert rag.without_language_request(question) == searched


def test_the_prompt_names_the_answer_language(monkeypatch, chunks):
    prompts = []
    def capture(prompt, **kwargs):
        prompts.append(prompt)
        return stream_of("Bir cevap [1].")(prompt)
    monkeypatch.setattr(rag, "generate_stream", capture)
    rag.answer("Kavram kayması nedir?")
    rag.answer("What is concept drift? Answer in Turkish.")
    rag.answer("Kavram kayması nedir? İngilizce cevap ver.")
    assert ["in Turkish" in p for p in prompts] == [True, True, False] and "in English" in prompts[2]


def test_refusal_follows_the_requested_language(monkeypatch, chunks):
    result = answer_with(monkeypatch, "The documents do not contain information about this.", "Pulsar nedir? İngilizce cevap ver.")
    assert result["answer"] == rag.REFUSAL["en"]


def test_stream_shows_the_answer_from_its_first_sentence_on(monkeypatch, chunks):
    text = "Input data testing is one level [2]. ML model testing is another [1]."
    monkeypatch.setattr(rag, "generate_stream", stream_of(text))
    *pieces, result = rag.answer_stream("What are the test levels?")
    assert pieces[0].startswith("Input data testing is one level [2].") and "".join(pieces) == text == result["answer"]


def test_stream_starts_before_a_long_first_sentence_ends(monkeypatch, chunks):
    text = "Input data testing checks the quality, completeness and representativeness of the training data [2]."
    monkeypatch.setattr(rag, "generate_stream", stream_of(text))
    *pieces, result = rag.answer_stream("What is input data testing?")
    assert len(pieces[0]) <= rag.FIRST_SENTENCE_MAX + 3 and "".join(pieces) == text == result["answer"]


def test_stream_replaces_a_refusal_and_stops_the_generation(monkeypatch, chunks):
    closed = []
    text = "The documents do not contain information about this [1][2]. Some more text that is never needed."
    monkeypatch.setattr(rag, "generate_stream", stream_of(text, closed))
    *pieces, result = rag.answer_stream("Raporda pulsarların keşfi hakkında ne söyleniyor?")
    assert pieces == [rag.REFUSAL["tr"]] and result["answer"] == rag.REFUSAL["tr"] and result["sources"] == []
    assert closed == [True]


def test_stream_of_a_short_answer_without_sentence_end(monkeypatch, chunks):
    monkeypatch.setattr(rag, "generate_stream", stream_of("4 kg [2]"))
    assert list(rag.answer_stream("How heavy?"))[:-1] == ["4 kg [2]"]


def test_no_history_means_no_rewrite(monkeypatch):
    monkeypatch.setattr(rag, "generate", lambda *a, **k: pytest.fail("the model must not be called"))
    assert rag.rewrite_query("What is MRR?", []) == "What is MRR?"


def test_no_indexed_documents(monkeypatch):
    monkeypatch.setattr(rag, "agentic_search", lambda query: ([], [query]))
    result = rag.answer("anything")
    assert result["sources"] == [] and "Index" in result["answer"]
