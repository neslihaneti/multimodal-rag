"""Eager attention computed one block of query rows at a time, registered as attn_implementation="blocked_eager".

On MPS the generator runs eager attention (SDPA there produces garbage on long prompts, phases/ZORLUKLAR.md Z10). Eager
builds the whole heads × queries × keys matrix at once: for a 9k-token prompt that is 10+ GB per layer and pushed the
evaluation process to 63 GB. Each row's softmax needs only its own row, so splitting the queries into blocks gives the
same output while only a block × keys slice is in memory.
"""
import torch
from transformers import AttentionInterface
from transformers.masking_utils import AttentionMaskInterface, eager_mask
from transformers.models.qwen3_vl.modeling_qwen3_vl import eager_attention_forward

QUERY_BLOCK = 1024


def blocked_eager_attention(module, query, key, value, attention_mask, scaling, dropout=0.0, **kwargs):
    if query.shape[2] <= QUERY_BLOCK:
        return eager_attention_forward(module, query, key, value, attention_mask, scaling, dropout, **kwargs)
    outputs = []
    for start in range(0, query.shape[2], QUERY_BLOCK):
        rows = slice(start, start + QUERY_BLOCK)
        mask = attention_mask[:, :, rows] if attention_mask is not None else None
        output, _ = eager_attention_forward(module, query[:, :, rows], key, value, mask, scaling, dropout, **kwargs)
        outputs.append(output)
    # eager returns (batch, queries, heads, head_dim); the full weight matrix is never built, so none is returned
    return torch.cat(outputs, dim=1), None


AttentionInterface.register("blocked_eager", blocked_eager_attention)
# Without a mask function of the same name transformers builds no mask at all, so the prompt was attended without the
# causal mask and the answers came out garbage (phases/ZORLUKLAR.md Z12)
AttentionMaskInterface.register("blocked_eager", eager_mask)
