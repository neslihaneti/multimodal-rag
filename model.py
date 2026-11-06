import gc
import os
import threading
from functools import lru_cache

# PyTorch frees its MPS cache only near the high watermark, which by default lies above the machine's memory: a long
# evaluation grew to 143 GB on a 128 GB Mac. These limits (fractions of the GPU's recommended working set) make it
# release cached blocks much earlier, and the high one is a hard cap: past it the process gets an out-of-memory error
# instead of pushing the whole Mac into swap. They must be set before torch starts
os.environ.setdefault("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.8")
os.environ.setdefault("PYTORCH_MPS_LOW_WATERMARK_RATIO", "0.5")

import torch
from chandra.model.hf import generate_hf
from chandra.model.schema import BatchInputItem
from chandra.output import parse_markdown
from transformers import (
    LogitsProcessorList,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
    AutoModel,
    AutoModelForImageTextToText,
    AutoModelForSequenceClassification,
    AutoProcessor,
    AutoTokenizer,
    Qwen3VLForConditionalGeneration,
)

DEVICE = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float32 if DEVICE == "cpu" else torch.bfloat16

OCR_MODEL_NAME = "datalab-to/chandra-ocr-2"  # the checkpoint chandra-ocr 0.2 prompts are written for
GEN_MODEL_NAME = os.getenv("GEN_MODEL", "Qwen/Qwen3-VL-4B-Instruct")
# On MPS, eager attention builds the full attention matrix and segfaults on long prompts (13.3k tokens crashed the
# process); prompts over this limit are refused instead (phases/faz-2/RAPOR.md)
MAX_INPUT_TOKENS = int(os.getenv("MAX_INPUT_TOKENS", "10000"))
EMBED_MODEL_NAME = "BAAI/bge-m3"
RERANK_MODEL_NAME = "BAAI/bge-reranker-v2-m3"
EMBED_DIM = 1024
# MPS compiles and keeps a graph for every new input shape: with a different length per batch a retrieval evaluation
# grew by 2 GB per question (73 GB after 30). Padding to a multiple of this keeps the shapes few (phases/ZORLUKLAR.md Z13)
PAD_MULTIPLE = 128
# Larger pages make Chandra return a blank page or hallucinate on MPS (tested: 2200 ok, 2800 fails)
OCR_MAX_SIDE = int(os.getenv("OCR_MAX_SIDE", "2000"))


# Models load on first use. Chandra is only needed while indexing and can be unloaded afterwards.
@lru_cache(maxsize=1)
def _ocr_model():
    model = AutoModelForImageTextToText.from_pretrained(OCR_MODEL_NAME, dtype=DTYPE, device_map={"": DEVICE}).eval()
    model.processor = AutoProcessor.from_pretrained(OCR_MODEL_NAME)
    model.processor.tokenizer.padding_side = "left"
    return model


def unload_ocr_model():
    _ocr_model.cache_clear()
    gc.collect()
    if DEVICE == "mps":
        torch.mps.empty_cache()


@lru_cache(maxsize=1)
def _embedder():
    tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL_NAME)
    model = AutoModel.from_pretrained(EMBED_MODEL_NAME, dtype=DTYPE).to(DEVICE).eval()
    return tokenizer, model


@lru_cache(maxsize=1)
def _reranker():
    tokenizer = AutoTokenizer.from_pretrained(RERANK_MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(RERANK_MODEL_NAME, dtype=DTYPE).to(DEVICE).eval()
    return tokenizer, model


@lru_cache(maxsize=1)
def _generator():
    # On MPS, SDPA attention turns long prompts into "The!!!!..." (from ~9.5k tokens, text-only too), and once one call
    # has broken every later call in the process breaks as well; eager attention is correct up to MAX_INPUT_TOKENS.
    # It is computed one block of query rows at a time, which keeps its memory small (attention.py)
    import attention as _  # registers "blocked_eager"
    attention = "blocked_eager" if DEVICE == "mps" else "sdpa"
    model = Qwen3VLForConditionalGeneration.from_pretrained(GEN_MODEL_NAME, dtype=DTYPE, device_map=DEVICE, attn_implementation=attention)
    processor = AutoProcessor.from_pretrained(GEN_MODEL_NAME)
    return model, processor


def extract_OCR_text(image):
    image = image.convert("RGB")
    image.thumbnail((OCR_MAX_SIDE, OCR_MAX_SIDE))
    batch = [BatchInputItem(image=image, prompt_type="ocr_layout")]
    result = generate_hf(batch, _ocr_model())[0]
    return parse_markdown(result.raw)


def embed_texts(texts, batch_size=16):
    # bge-m3 dense embedding: CLS token, L2-normalized
    tokenizer, model = _embedder()
    embeddings = []
    for i in range(0, len(texts), batch_size):
        inputs = tokenizer(texts[i:i + batch_size], padding=True, truncation=True, max_length=1024, pad_to_multiple_of=PAD_MULTIPLE, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            cls = model(**inputs).last_hidden_state[:, 0]
        embeddings.extend(torch.nn.functional.normalize(cls.float(), p=2, dim=-1).cpu().tolist())
    _release_mps_cache()
    return embeddings


def rerank_scores(query, passages, batch_size=16):
    tokenizer, model = _reranker()
    scores = []
    for i in range(0, len(passages), batch_size):
        pairs = [[query, p] for p in passages[i:i + batch_size]]
        inputs = tokenizer(pairs, padding=True, truncation=True, max_length=1024, pad_to_multiple_of=PAD_MULTIPLE, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            logits = model(**inputs).logits.view(-1).float()
        scores.extend(torch.sigmoid(logits).cpu().tolist())
    _release_mps_cache()
    return scores


def _release_mps_cache():
    if DEVICE == "mps":
        torch.mps.empty_cache()


def _inputs(prompt, images, system):
    model, processor = _generator()
    content = [{"type": "image", "image": image} for image in images]
    content.append({"type": "text", "text": prompt})
    messages = [{"role": "system", "content": [{"type": "text", "text": system}]}] if system else []
    messages.append({"role": "user", "content": content})
    return processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )


def count_tokens(prompt, images=(), system=None):
    return _inputs(prompt, images, system).input_ids.shape[1]


def _prepare(prompt, images, system, options):
    model, processor = _generator()
    inputs = _inputs(prompt, images, system).to(model.device)
    if DEVICE == "mps" and inputs.input_ids.shape[1] > MAX_INPUT_TOKENS:
        raise ValueError(f"prompt of {inputs.input_ids.shape[1]} tokens is over MAX_INPUT_TOKENS ({MAX_INPUT_TOKENS})")
    options = dict(options or {})
    if "answer_no_repeat_ngram_size" in options:
        from no_repeat import AnswerNoRepeatNGram
        no_repeat = AnswerNoRepeatNGram(options.pop("answer_no_repeat_ngram_size"), inputs.input_ids.shape[1])
        options["logits_processor"] = LogitsProcessorList([no_repeat])
    return model, processor, inputs, options


class _StopWhenSet(StoppingCriteria):
    def __init__(self, event):
        self.event = event

    def __call__(self, input_ids, scores, **kwargs):
        return self.event.is_set()


def generate_stream(prompt, images=(), system=None, max_new_tokens=1024, options=None):
    """Like generate(), but yields the text piece by piece as it is generated. Closing the generator early (a
    consumer that stops reading) also stops the generation."""
    model, processor, inputs, options = _prepare(prompt, images, system, options)
    streamer = TextIteratorStreamer(processor.tokenizer, skip_prompt=True, skip_special_tokens=True)
    stop, errors = threading.Event(), []

    def run():
        try:
            with torch.no_grad():  # no_grad is per thread
                model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, streamer=streamer,
                               stopping_criteria=StoppingCriteriaList([_StopWhenSet(stop)]), **options)
        except BaseException as error:
            errors.append(error)
            streamer.end()  # otherwise the reader waits for text that never comes

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    try:
        yield from streamer
    finally:
        stop.set()
        thread.join()
        del inputs
        if DEVICE == "mps":
            torch.mps.empty_cache()
    if errors:
        raise errors[0]


def generate(prompt, images=(), system=None, max_new_tokens=1024, options=None):
    model, processor, inputs, options = _prepare(prompt, images, system, options)
    with torch.no_grad():
        generated_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, **options)
    output_ids = generated_ids[:, inputs.input_ids.shape[1]:]
    text = processor.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
    if DEVICE == "mps":
        # Eager attention's multi-GB buffers stay cached otherwise; after 81 eval questions the cache ran out of memory
        del inputs, generated_ids, output_ids
        torch.mps.empty_cache()
    return text
