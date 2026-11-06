"""rag.fit_prompt keeps the answer prompt under PROMPT_TOKEN_BUDGET (the generator degrades on long prompts, phases/faz-2)."""
import pytest
from PIL import Image

import rag


@pytest.fixture
def six_chunks(tmp_path):
    image = tmp_path / "page.png"
    Image.new("RGB", (20, 20)).save(image)
    return [{"id": i, "file_name": "doc.pdf", "page_number": i, "image_path": str(image), "heading": "",
             "content": f"chunk {i} " + "x" * 3000, "context": ""} for i in range(1, 7)]


def tokens(monkeypatch, per_image=1000):
    # stand-in tokenizer: 1 token per 4 characters, a fixed number per image
    monkeypatch.setattr(rag, "count_tokens", lambda prompt, images=(), system=None: len(prompt) // 4 + per_image * len(images))


def test_prompt_under_budget_is_unchanged(monkeypatch, six_chunks):
    tokens(monkeypatch)
    monkeypatch.setattr(rag, "PROMPT_TOKEN_BUDGET", 100_000)
    chunks, images, _ = rag.fit_prompt("q", six_chunks)
    assert len(chunks) == 6 and len(images) == rag.MAX_PAGE_IMAGES


def test_lowest_ranked_chunks_go_first_then_images(monkeypatch, six_chunks):
    tokens(monkeypatch)
    # 6 chunks ~4.6k tokens + 3 images 3k; 3 chunks ~2.4k + 3 images = 5.4k; 3 chunks + 1 image = 3.4k
    monkeypatch.setattr(rag, "PROMPT_TOKEN_BUDGET", 3500)
    chunks, images, prompt = rag.fit_prompt("q", six_chunks)
    assert [c["id"] for c in chunks] == [1, 2, 3]
    assert len(images) == 1
    assert "[3] doc.pdf · page 3" in prompt and "chunk 4" not in prompt


def test_tiny_budget_still_keeps_the_best_chunk(monkeypatch, six_chunks):
    tokens(monkeypatch)
    monkeypatch.setattr(rag, "PROMPT_TOKEN_BUDGET", 10)
    chunks, images, prompt = rag.fit_prompt("q", six_chunks)
    assert [c["id"] for c in chunks] == [1] and images == []
    assert "Attached page images, in order: none" in prompt
