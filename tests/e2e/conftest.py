"""End-to-end tests use the real models (minutes, Apple GPU): run them on their own with `pytest tests/e2e`."""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

if getattr(sys.modules.get("model"), "IS_STUB", False):
    pytest.skip("the unit tests replaced the models with stubs in this session: run `pytest tests/e2e` separately",
                allow_module_level=True)
