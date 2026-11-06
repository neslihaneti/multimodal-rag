import pytest

from file_processing import chunk_markdown, clean_markdown

LONG = "word " * 80  # 400 characters


def test_splits_on_headings_and_keeps_the_heading():
    md = f"## 1.1 First\n\n{LONG}\n\n## 1.2 Second\n\n{LONG}"
    chunks = chunk_markdown(md)
    assert [c["heading"] for c in chunks] == ["1.1 First", "1.2 Second"]
    assert chunks[0]["content"].startswith("## 1.1 First")
    assert chunks[1]["content"].startswith("## 1.2 Second")


def test_text_before_the_first_heading_has_no_heading():
    chunks = chunk_markdown(f"{LONG}\n\n## Later\n\n{LONG}")
    assert chunks[0]["heading"] == ""
    assert chunks[1]["heading"] == "Later"


def test_short_section_is_merged_into_the_next_one():
    md = f"## Chapter 3\n\nIntro.\n\n## 3.1 Forms of ML\n\n{LONG}"
    chunks = chunk_markdown(md, min_chars=200)
    assert len(chunks) == 1
    assert chunks[0]["heading"] == "Chapter 3"
    assert "## 3.1 Forms of ML" in chunks[0]["content"]


def test_long_section_is_split_on_paragraphs_and_every_part_keeps_the_heading():
    paragraphs = "\n\n".join(f"Paragraph {i}. " + "text " * 60 for i in range(6))  # ~300 chars each
    chunks = chunk_markdown(f"## Big\n\n{paragraphs}", max_chars=700)
    assert len(chunks) > 1
    assert all(c["heading"] == "Big" for c in chunks)
    assert all(len(c["content"]) <= 700 for c in chunks)
    joined = " ".join(c["content"] for c in chunks)
    assert all(f"Paragraph {i}." in joined for i in range(6))  # nothing lost


def test_empty_input_gives_no_chunks():
    assert chunk_markdown("") == []
    assert chunk_markdown("\n\n  \n") == []


def test_long_bullet_list_respects_max_chars():
    # list items are separated by single newlines, so the list is one "paragraph" (doc1 p.50 gave a 1,968-char chunk)
    items = "\n".join(f"- Item {i}: " + "detail " * 40 for i in range(8))  # ~2,300 chars, no blank lines
    chunks = chunk_markdown(f"## List\n\nThere are several reasons:\n\n{items}", max_chars=1500)
    assert all(len(c["content"]) <= 1500 for c in chunks)
    assert "\n".join(c["content"] for c in chunks).count("- Item") == 8


def test_long_markdown_table_repeats_its_header_in_every_chunk():
    rows = "\n".join(f"| constant {i} | " + "1.23456789 " * 8 + "|" for i in range(30))
    chunks = chunk_markdown(f"## Table\n\n| name | value |\n|---|---|\n{rows}", max_chars=1000)
    table_chunks = [c for c in chunks if "constant" in c["content"]]
    assert len(table_chunks) > 1 and all(len(c["content"]) <= 1000 for c in chunks)
    assert all("| name | value |\n|---|---|" in c["content"] for c in table_chunks)
    assert sum(c["content"].count("| constant") for c in chunks) == 30


def test_long_html_table_repeats_its_head_in_every_chunk():
    head = "<table border=\"1\">\n<thead>\n<tr>\n<th>Year</th>\n<th>Stage</th>\n</tr>\n</thead>\n<tbody>\n"
    body = "".join(f"<tr>\n<td>{1966 + i}</td>\n<td>{'figuring and testing mirrors ' * 3}</td>\n</tr>\n" for i in range(30))
    chunks = chunk_markdown("## Schedule\n\n" + head + body + "</tbody>\n</table>", max_chars=1200)
    table_chunks = [c for c in chunks if "<td>" in c["content"]]
    assert len(table_chunks) > 1 and all(len(c["content"]) <= 1200 for c in chunks)
    assert all("<th>Year</th>" in c["content"] for c in table_chunks)
    assert sum(c["content"].count("<td>19") for c in chunks) == 30


def test_one_very_long_line_is_split_on_sentences():
    text = " ".join(f"Sentence number {i} says something about mirrors." for i in range(80))
    chunks = chunk_markdown("## Prose\n\n" + text, max_chars=800)
    assert len(chunks) > 1 and all(len(c["content"]) <= 800 for c in chunks)


def test_clean_markdown_shortens_dot_leaders_dashes_and_blank_lines():
    md = "7.1 Specification ........................ 50\n\n\n\n|---------|------|\n| a     b |"
    assert clean_markdown(md) == "7.1 Specification … 50\n\n|---|---|\n| a b |"
