"""The indexer reads the PDF's own text layer when it can and sends the page to Chandra OCR otherwise."""
import pytest

import indexer
from file_processing import image_coverage

TEXT = "## 7.2 Test Levels\n\n" + "AI-based systems typically comprise both AI and non-AI components. " * 3


@pytest.fixture(autouse=True)
def fake_ocr(monkeypatch):
    monkeypatch.setattr(indexer, "extract_OCR_text", lambda image: "OCR TEXT")
    monkeypatch.setattr(indexer, "OCR_MODE", "auto")


def page(text=TEXT, coverage=0.0):
    return {"page_number": 1, "image": object(), "text": text, "image_coverage": coverage}


def test_born_digital_page_uses_the_text_layer():
    assert indexer.page_text(page()) == (TEXT, "text_layer")


def test_scanned_page_goes_to_ocr():
    # a scan is one image over the whole page; its text layer is empty or an invisible OCR layer
    assert indexer.page_text(page(text="", coverage=0.98)) == ("OCR TEXT", "ocr")


def test_page_with_a_large_figure_goes_to_ocr_even_with_text():
    assert indexer.page_text(page(coverage=0.45)) == ("OCR TEXT", "ocr")


def test_small_logo_does_not_force_ocr():
    assert indexer.page_text(page(coverage=0.02))[1] == "text_layer"


def test_almost_empty_text_layer_goes_to_ocr():
    assert indexer.page_text(page(text="Page 3 of 99"))[1] == "ocr"


def test_threshold_is_inclusive_for_text_length(monkeypatch):
    monkeypatch.setattr(indexer, "TEXT_LAYER_MIN_CHARS", len(TEXT))
    assert indexer.page_text(page())[1] == "text_layer"


def test_ocr_mode_always_overrides_the_text_layer(monkeypatch):
    monkeypatch.setattr(indexer, "OCR_MODE", "always")
    assert indexer.page_text(page())[1] == "ocr"


class FakeObject:
    def __init__(self, left, bottom, right, top):
        self.box = (left, bottom, right, top)

    def get_pos(self):
        return self.box


class FakePage:
    def __init__(self, *objects):
        self.objects = objects

    def get_size(self):
        return 600.0, 800.0

    def get_objects(self, filter=None, max_depth=None):
        return iter(self.objects)


def test_image_coverage_uses_the_largest_image():
    logo = FakeObject(500, 750, 560, 790)    # 60 x 40
    figure = FakeObject(50, 300, 550, 700)   # 500 x 400 = 0.4167 of the page
    assert image_coverage(FakePage(logo, figure)) == pytest.approx(500 * 400 / (600 * 800))


def test_image_coverage_is_zero_without_images():
    assert image_coverage(FakePage()) == 0.0
