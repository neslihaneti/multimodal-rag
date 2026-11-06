"""Blocked eager attention must give the same output as eager attention computed in one piece."""
import types

import pytest

torch = pytest.importorskip("torch")
attention = pytest.importorskip("attention")
from transformers.models.qwen3_vl.modeling_qwen3_vl import eager_attention_forward  # noqa: E402


def inputs(queries, keys, causal):
    torch.manual_seed(0)
    module = types.SimpleNamespace(num_key_value_groups=2, training=False)
    query = torch.randn(1, 4, queries, 8)
    key, value = torch.randn(1, 2, keys, 8), torch.randn(1, 2, keys, 8)
    mask = None
    if causal:
        mask = torch.full((queries, keys), float("-inf")).triu(keys - queries + 1)[None, None]
    return module, query, key, value, mask


@pytest.mark.parametrize("causal", [True, False])
def test_blocked_output_equals_eager_output(monkeypatch, causal):
    monkeypatch.setattr(attention, "QUERY_BLOCK", 16)
    args = inputs(queries=50, keys=50, causal=causal)
    expected, _ = eager_attention_forward(*args, scaling=0.35)
    output, weights = attention.blocked_eager_attention(*args, scaling=0.35)
    assert weights is None
    assert torch.allclose(output, expected, atol=1e-6)


def test_blocked_eager_gets_the_eager_mask():
    from transformers.masking_utils import ALL_MASK_ATTENTION_FUNCTIONS, eager_mask

    assert ALL_MASK_ATTENTION_FUNCTIONS._global_mapping["blocked_eager"] is eager_mask


def test_short_inputs_take_the_plain_eager_path(monkeypatch):
    monkeypatch.setattr(attention, "QUERY_BLOCK", 16)
    args = inputs(queries=1, keys=40, causal=False)  # one new token attending to a cache, as in decoding
    expected, _ = eager_attention_forward(*args, scaling=0.35)
    output, _ = attention.blocked_eager_attention(*args, scaling=0.35)
    assert torch.equal(output, expected)
