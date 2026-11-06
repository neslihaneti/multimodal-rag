import hashlib
import os
import re

import pypdfium2 as pdfium

#we are creating pipeline
from docling.datamodel.pipeline_options  import PdfPipelineOptions #document parser
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
pipeline_options = PdfPipelineOptions()
pipeline_options.images_scale = 2.0
pipeline_options.generate_page_images = True
pipeline_options.generate_picture_images = False
pipeline_options.do_table_structure = True  # tables from the text layer keep their rows and columns
pipeline_options.do_ocr = False  # OCR is done by Chandra

doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

HEADING = re.compile(r"^#{1,6}\s+(.*)")


def list_pdfs(folder):
    return sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".pdf"))


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def image_coverage(pdf_page):
    """Share of the page covered by its largest image: about 1 for a scanned page, small for born-digital text."""
    width, height = pdf_page.get_size()
    largest = 0.0
    for obj in pdf_page.get_objects(filter=[pdfium.raw.FPDF_PAGEOBJ_IMAGE], max_depth=3):
        left, bottom, right, top = obj.get_pos()
        largest = max(largest, (right - left) * (top - bottom) / (width * height))
    return largest


def clean_markdown(markdown):
    # Docling pads table cells and keeps table-of-contents dot leaders; both waste chunk space
    markdown = re.sub(r"\.{4,}", " … ", markdown)
    markdown = re.sub(r"-{4,}", "---", markdown)
    markdown = re.sub(r"[ \t]{2,}", " ", markdown)
    return re.sub(r"\n{3,}", "\n\n", markdown).strip()


def pdf_pages(path):
    """Each page's image, its text-layer markdown (empty for scanned pages) and how much of it is covered by images."""
    conv_res = doc_converter.convert(path)
    pdf = pdfium.PdfDocument(path)
    pages = []
    for page_no, page in sorted(conv_res.document.pages.items()):
        text = conv_res.document.export_to_markdown(page_no=page_no, image_placeholder="", escape_underscores=False)
        pdf_page = pdf[page_no - 1]
        pages.append({
            "page_number": page_no,
            "image": page.image.pil_image,
            "text": clean_markdown(text),
            "image_coverage": image_coverage(pdf_page),
        })
        pdf_page.close()
    pdf.close()
    return pages


def chunk_markdown(markdown, max_chars=1500, min_chars=200):
    """Split OCR markdown into heading-based sections; long sections are split on paragraph breaks."""
    sections, heading, lines = [], "", []

    def flush():
        text = "\n".join(lines).strip()
        if text:
            sections.append({"heading": heading, "content": text})

    for line in markdown.splitlines():
        match = HEADING.match(line)
        if match:
            flush()
            heading, lines = match.group(1).strip(), [line]
        else:
            lines.append(line)
    flush()

    # Merge heading-only or very short sections into the next one
    merged = []
    for section in sections:
        if merged and len(merged[-1]["content"]) < min_chars:
            merged[-1]["content"] += "\n\n" + section["content"]
            merged[-1]["heading"] = merged[-1]["heading"] or section["heading"]
        else:
            merged.append(dict(section))

    chunks = []
    for section in merged:
        if len(section["content"]) <= max_chars:
            chunks.append(section)
            continue
        paragraphs = [piece for paragraph in re.split(r"\n\s*\n", section["content"]) for piece in split_block(paragraph, max_chars)]
        chunks += [{"heading": section["heading"], "content": text} for text in pack(paragraphs, max_chars, "\n\n")]
    return chunks


def pack(units, max_chars, separator, prefix=""):
    """Greedily join units into pieces of at most max_chars, each starting with prefix (a repeated table header)."""
    pieces, part = [], ""
    for unit in units:
        if part and len(prefix) + len(part) + len(separator) + len(unit) > max_chars:
            pieces.append((prefix + part).strip())
            part = ""
        part += (separator if part else "") + unit
    if part.strip():
        pieces.append((prefix + part).strip())
    return pieces


def split_block(text, max_chars):
    """Split a paragraph longer than max_chars: a list or table without blank lines on its lines or rows, with the
    table header repeated in every piece, and a single long line on sentence ends."""
    if len(text) <= max_chars:
        return [text]
    if "<tr" in text:  # Chandra writes tables as HTML: split between rows, repeat everything before the first body row
        rows = re.split(r"(?=<tr[\s>])", text)
        head_end = next((i for i, r in enumerate(rows) if i and "<th" not in r), len(rows))
        head, body = "".join(rows[:head_end]), rows[head_end:]
        if body and len(head) < max_chars // 2:
            return pack(body, max_chars, "", prefix=head)
    lines = text.splitlines()
    if len(lines) > 1:
        header = "\n".join(lines[:2]) + "\n" if lines[0].startswith("|") and re.match(r"\|[\s:|-]+\|?$", lines[1] if len(lines) > 1 else "") else ""
        body = [piece for line in (lines[2:] if header else lines) for piece in split_block(line, max_chars - len(header))]
        return pack(body, max_chars, "\n", prefix=header)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) > 1:
        return pack(sentences, max_chars, " ")
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
