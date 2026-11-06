"""N-gram repeat block for answers (phases/faz-5b/RAPOR.md)."""
from transformers import LogitsProcessor


class AnswerNoRepeatNGram(LogitsProcessor):
    """Like no_repeat_ngram_size, but only n-grams of the generated answer count: transformers' version also looks at the
    prompt, so it would stop the model from copying a long phrase of a source excerpt word for word."""

    def __init__(self, size, prompt_length):
        self.size, self.prompt_length = size, prompt_length

    def __call__(self, input_ids, scores):
        for row, ids in enumerate(input_ids[:, self.prompt_length:].tolist()):
            if len(ids) < self.size:
                continue
            prefix = ids[len(ids) - self.size + 1:]
            banned = {ids[i + self.size - 1] for i in range(len(ids) - self.size + 1) if ids[i:i + self.size - 1] == prefix}
            if banned:
                scores[row, list(banned)] = -float("inf")
        return scores
