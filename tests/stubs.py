"""Lightweight stand-ins so unit tests import the project without torch, the models or Docling."""
import importlib
import sys
import types
from unittest import mock


def fake_model_module():
    model = types.ModuleType("model")
    model.IS_STUB = True
    model.EMBED_DIM = 1024
    model.EMBED_MODEL_NAME = model.RERANK_MODEL_NAME = model.GEN_MODEL_NAME = "stub"
    model.embed_texts = lambda texts, batch_size=16: [[0.0] * 1024 for _ in texts]
    model.rerank_scores = lambda query, passages, batch_size=16: [0.5] * len(passages)
    model.generate = lambda prompt, images=(), system=None, max_new_tokens=1024, options=None: ""
    model.generate_stream = lambda prompt, images=(), system=None, max_new_tokens=1024, options=None: iter([""])
    model.count_tokens = lambda prompt, images=(), system=None: len(prompt) // 4 + 1000 * len(images)
    model.extract_OCR_text = lambda image: "OCR TEXT"
    model.unload_ocr_model = lambda: None
    return model


def install():
    sys.modules["model"] = fake_model_module()
    # Docling is only used by pdf_pages(); stub it where it is not installed (CI)
    try:
        importlib.import_module("docling.document_converter")
    except ImportError:
        for name in ("docling", "docling.datamodel", "docling.datamodel.pipeline_options",
                     "docling.datamodel.base_models", "docling.document_converter"):
            sys.modules[name] = mock.MagicMock()
