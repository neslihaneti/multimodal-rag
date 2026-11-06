"""An interrupted indexing run keeps its finished pages and only processes the rest when restarted."""
import pytest

import db
import indexer

TEXT = "## Section\n\n" + "Plain born-digital text on this page. " * 5


@pytest.fixture
def three_pages(test_db, tmp_path, monkeypatch):
    (tmp_path / "report.pdf").write_bytes(b"%PDF-1.4 resume test")
    pages = [{"page_number": n, "image": None, "text": f"{TEXT} page {n}", "image_coverage": 0.0} for n in (1, 2, 3)]
    monkeypatch.setattr(indexer, "pdf_pages", lambda path: pages)
    monkeypatch.setattr(indexer, "save_page_image", lambda file_hash, n, image: f"/tmp/{n}.png")
    monkeypatch.setattr(indexer, "CONTEXTUAL_CHUNKS", False)
    return tmp_path


def stored_pages():
    with db.connect() as conn:
        return conn.execute("""SELECT d.status, p.page_number, count(c.id) FROM rag_documents d
            JOIN rag_pages p ON p.document_id = d.id LEFT JOIN rag_chunks c ON c.page_id = p.id
            WHERE d.file_name = 'report.pdf' GROUP BY 1, 2 ORDER BY 2""").fetchall()


def test_restart_continues_after_the_last_finished_page(three_pages, monkeypatch):
    real_insert = db.insert_page_with_chunks
    processed = []

    def crash_on_page_3(document_id, page_number, *args):
        processed.append(page_number)
        if page_number == 3:
            raise RuntimeError("power cut")
        real_insert(document_id, page_number, *args)

    monkeypatch.setattr(db, "insert_page_with_chunks", crash_on_page_3)
    with pytest.raises(RuntimeError):
        indexer.index_folder(str(three_pages))
    assert [(s, p) for s, p, _ in stored_pages()] == [("indexing", 1), ("indexing", 2)]

    processed.clear()
    monkeypatch.setattr(db, "insert_page_with_chunks", lambda *a: (processed.append(a[1]), real_insert(*a)))
    summary = indexer.index_folder(str(three_pages))
    assert processed == [3]
    assert summary["indexed"] == ["report.pdf"]
    rows = stored_pages()
    assert [(s, p) for s, p, _ in rows] == [("done", 1), ("done", 2), ("done", 3)]
    assert all(chunks >= 1 for _, _, chunks in rows)


def test_finished_document_is_skipped(three_pages):
    assert indexer.index_folder(str(three_pages))["skipped"] == ["report.pdf"]


def test_rechunk_replaces_only_pages_whose_split_changed(three_pages, monkeypatch):
    # page 2 was stored as one long chunk, the way chunk_markdown used to keep a long list together
    with db.connect() as conn:
        page_id = conn.execute("SELECT p.id FROM rag_pages p JOIN rag_documents d ON d.id = p.document_id "
                               "WHERE d.file_name = 'report.pdf' AND p.page_number = 2").fetchone()[0]
        conn.execute("UPDATE rag_pages SET ocr_text = %s WHERE id = %s",
                     ("## List\n\n" + "\n".join(f"- item {i} " + "word " * 60 for i in range(10)), page_id))
    changed = []
    real_replace = db.replace_page_chunks
    monkeypatch.setattr(db, "replace_page_chunks", lambda pid, chunks: (changed.append(pid), real_replace(pid, chunks)))

    assert indexer.rechunk_document("report.pdf") == 1
    assert changed == [page_id]
    rows = {p: n for _, p, n in stored_pages()}
    assert rows[2] > 1
    with db.connect() as conn:
        assert conn.execute("SELECT max(length(content)) FROM rag_chunks").fetchone()[0] <= 1500
    assert indexer.rechunk_document("report.pdf") == 0  # a repeated run has nothing left to do
