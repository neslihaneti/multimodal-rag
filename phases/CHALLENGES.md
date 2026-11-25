# Challenges met during testing and how they were solved

For the interview question "What difficulties did you run into while testing?". Each entry: **situation → how we
noticed → root cause → fix → result → lesson**. New phases add entries; the numbers do not change.

---

## Phase 1

### Z1. The metric said "don't know"; in fact the model was broken
- **Situation:** In the answer evaluation all of the first 7 questions were "refused", at 200–475 s per question.
- **Noticing:** The numbers made no sense (the same questions had been answered correctly in 30 s before). The raw output: "The!!!!!!…".
- **Root cause:** bf16 + SDPA attention on the Apple GPU (MPS) overflows numerically on long image+text inputs. Correct without images, correct with a short context, broken with a long one; correct with `eager` attention. Isolated step by step.
- **Fix:** `attn_implementation="eager"` on MPS.
- **Result:** correctness 0.92, time 45 s.
- **Lesson:** The judge read the broken output as a "refusal"; metrics alone mislead, looking at the raw output is essential. The bug was also in the user interface; without tests it would not have been noticed.

### Z2. The invisible drift in RRF
- **Situation:** The results of hybrid search looked correct.
- **Noticing:** The integration test compared the SQL's score with the RRF formula computed independently in Python: 0.03202 expected, 0.03178 returned.
- **Root cause:** Chunks of documents still being indexed entered the ranking and were filtered out afterwards; the ranks of the real chunks shifted and the 40-candidate quota was wasted.
- **Fix:** Only `status='done'` documents before ranking.
- **Lesson:** A result "looking reasonable" is not enough; check the formula against an independent reference (a test oracle).

### Z3. The answer step was safe, indexing was not
- **Situation:** We put two prompt injections into a PDF: one hidden in white text and one visible, disguised as a "note to AI".
- **Noticing:** The answers were clean, but the test that checks the database caught the model that writes context sentences during indexing writing "PWNED-7731".
- **Root cause:** The call that produces the context sentence had no "the document content is data" warning.
- **Fix:** A system message + not saving a context sentence that contains a URL/code absent from the chunk. The system message alone was enough.
- **Lesson:** The attack surface is not only the answer the user sees; every step an LLM touches (indexing included) must be tested. The test first verifies that the attack really entered the index; otherwise its passing proves nothing.

### Z4. Another AI's analysis pointed at the wrong place
- **Situation:** An external review blamed keyword search for the weakness of hybrid search and suggested changing the RRF weight; it suggested 0.15 as the reranker threshold.
- **Noticing:** We checked with our own measurements: in none of the 37 questions do hybrid+reranker and vector+reranker differ; it is the reranker that pushes q24 down. Threshold 0.15 blocks an answerable question, 0.05 none.
- **Fix:** In the roadmap we made the real question "why does the reranker make vector search worse?" and corrected the threshold to 0.05.
- **Lesson:** An observation can be right with the wrong cause; do not apply any suggestion without verifying it with data.

### Z5. The assumption "hybrid search is better" did not hold for this document
- **Situation:** Expectation: hybrid > vector. Measurement: vector Recall@1 0.97, hybrid RRF 0.68, live system 0.89.
- **Lesson and honest note:** Because I wrote the golden set by reading the text, it may be easy for vector search (ceiling effect). The conclusion is not "hybrid is bad" but "this is the measured state on this set with these settings"; to be measured again with hard questions (Phase 6).

### Z6. The UI test tripped over model behaviour
- **Situation:** The Playwright test could not find a source image.
- **Root cause:** Not a UI bug: the model gave the correct answer without a citation (no [n]); sources are derived only from citations. The answer eval measured this at 24%.
- **Fix (for now):** The UI test was made deterministic with a question that gets a citation (`do_sample=False`); the real problem went to Phase 2.
- **Lesson:** UI tests must be kept apart from model quality; and a failing test can point to a problem in another layer.

### Z7. Reliability of the local judge
- **Situation:** So that no data leaves the machine, the judge is also the local 4B model.
- **Noticing:** We read by hand the 3 answers it called "wrong": 2 really are wrong, 1 is correct (too strict).
- **Fix:** Every decision is written to `judgments.jsonl`; a `calibrate` command computes the agreement rate and Cohen's kappa from hand labels.
- **Lesson:** The LLM-as-judge itself must be tested.

### Z8. A long evaluation stopping halfway
- **Situation:** The 45-question answer eval takes ~45 min; when stopped, everything was lost.
- **Fix:** A checkpoint file after each question (with the golden set hash), `--resume`.
- **Lesson:** Expensive evaluations must be designed to be restartable (idempotent).

## Z9. A long evaluation stopped silently halfway (Phase 1b)

- **Problem:** The 82-question `evaluate.py answers` stopped at question 42 without an error (exit 0, no traceback). Plenty of memory (128 GB, 96% free), no process-kill record in the system log; the process closed together with the background shell session that started it.
- **Fix:** Thanks to the checkpoint of Z8 no answer was lost; `--resume` skipped the 42 questions and went on. Long jobs are now started independently of the session with `nohup … &`.
- **Second trap:** The resumed process would reread `rag.py`, and the file already had the next phase's (Phase 2) prompt change; resuming as it was would have measured the second half of the baseline with the new prompt. The change was reverted temporarily and reapplied after the process had loaded its modules.
- **Lesson:** If the code under measurement and the code under development share the same working directory, a "resume" button can silently measure a different system. Adding the code version (e.g. a prompt hash) to the run_info in the report header makes this mistake visible.

## Z10. A model bug thought to be "fixed" came back as a process crash on long contexts (Phase 1b → Phase 2)

- **Symptom:** The silent stop of Z9 was deterministic: the evaluation died both times at q43 ("What is the capital of Australia?", an unanswerable question). Run alone with `python3 -X faulthandler`: `Fatal Python error: Segmentation fault`, top of the stack `eager_attention_forward` (the prefill of answer generation), exit 139.
- **Cause:** For unanswerable questions the reranker's top ranks were doc2's huge chunks (3.5–5 thousand characters, LaTeX-heavy) → 6 chunks + 3 page images = **13,298 tokens**. The eager attention adopted in Phase 1 to fix the "The!!!!" bug (Z1) builds the whole attention matrix in memory (32 heads × 13k² ≈ 11 GB bf16, ~22 GB for the softmax in fp32) and the process crashes on MPS, despite 128 GB of RAM.
- **Hypothesis tests (same input, separate processes):**
  - sdpa bf16 / fp16 / **fp32** → all three produced garbage ("0000…", "| | |…"): the problem is not numerical precision.
  - Length sweep (sdpa, 3 images): 5k–11.3k tokens correct; 12.2k broken format; **12.9k: "The capital of Australia is Canberra."** — an answer from outside the documents (a faithfulness violation, with no error message!); 13.3k garbage.
  - Rescuing sdpa with a budget failed: in the real flow a 9,573-token **text-only** search-decision prompt also produced "SEARCH!!!!", and **every later call** (an 8.4k-token prompt that works correctly on its own) was broken → MPS sdpa breaks in a stateful way; the threshold is unpredictable.
  - eager is correct on the same two calls (9.5k text 6.2 s, 8.4k with images 34.5 s).
- **Fix:** Stayed with eager + a two-layer guard: `model.MAX_INPUT_TOKENS = 10000` (refuses a prompt above it with an explicit `ValueError` instead of a crash/garbage) and `rag.PROMPT_TOKEN_BUDGET = 9000` (`fit_prompt`: first the lowest-ranked chunks down to 3, then page images, finally chunks again; the search-decision prompt is trimmed to the same budget). Unit tests: `tests/unit/test_prompt_budget.py`, `test_decision_prompt_is_kept_under_the_token_budget`.
- **Lesson / interview line:** "When you fix a bug, also measure the limits of the fix." The Phase 1 fix had only been tested on short single-document prompts; once the multi-document index made prompts longer, the same root cause (MPS attention on long contexts) came back first as a crash, and at the most dangerous point as a *silent answer from outside the documents*. The lasting fix was not the attention type but explicitly limiting the input size and pinning the limit with a test.

## Z11. MPS memory piled up during an evaluation lasting hours (Phase 2)

- **Symptom:** The token budget removed the crash, but the 82-question run stopped after question 81: `RuntimeError: MPS backend out of memory (MPS allocated: 57 GiB, other allocations: 120 GiB … Tried to allocate 9.25 GiB)`. The same prompt size was fine on its own.
- **Cause:** Eager attention allocates GBs of temporary buffers at every prefill; PyTorch's MPS cache keeps them for the life of the process, and in fragmented memory a large allocation eventually no longer fits.
- **Fix:** At the end of `model.generate` the tensors are deleted and `torch.mps.empty_cache()` is called. Since 80 answers were in the checkpoint, `--resume` ran only the last question (the prompt hash did not change, same system).
- **Lesson:** A limit test that passes in one call may not pass in a long-running process: a "soak" run is a separate kind of test. This also applies to the UI, which runs as a server.

## Z12. An attention registered under a custom name ran without a mask (Phase J)

- **Symptom:** With `blocked_eager` (attention.py), written to save memory, the answers broke: `\x00` sequences, "Canberra" from outside the documents on q43, a wrong year on q01; every question generated up to 1,024 tokens and took 3 min; process memory 50 GB → 148 GB in one run and a system OOM. The "eager" mode set up for comparison used the same name, so it was broken too; at first it looked like "the memory setting breaks it".
- **Cause:** transformers produces no mask at all for attention types whose name is not in the mask table (`AttentionMaskInterface`) (for backends such as vLLM/TGI that build their own mask). It had only been registered in `AttentionInterface` → the prompt was processed without a causal mask.
- **Fix:** `AttentionMaskInterface.register("blocked_eager", eager_mask)` + a unit test. Two memory safety nets for long jobs: `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.8` (a hard limit inside the process) and `mem_guard.sh` (stops the process if its footprint passes 70 GB).
- **Lesson:** The unit test only verified the attention function, not how the model calls it (with a mask). When an integration point changes, check at least one known-correct answer from the real model. And in a comparison, the "control" arm must really be independent of the change under test.

## Z13. The root of the memory leak: MPS keeps a graph for every new input shape (Phase 5)

- **Symptom:** Despite the `empty_cache` fix of Z11, long runs kept growing: ~3 GB/question for the answer measurement, and even ~2 GB/question for the retrieval measurement, which generates nothing (73 GB after 30 questions). The guard stopped the process.
- **Isolation:** The same reranker was given inputs of random length 25 times: memory 2.8 → 17 GB, a steady rise. With the length padded to multiples of 256 it stayed flat at 4 GB. So the problem is not the cache: PyTorch MPS compiles and keeps a compute graph for every new tensor shape, and every chunk has a different length.
- **Fix:** embedder and reranker inputs `pad_to_multiple_of=128` (the result is the same thanks to the mask: score difference at most 0.00017, embedding cosine ≥ 0.9995; the order of candidates with nearly equal scores can change). The retrieval measurement stayed around 11 GB over 82 questions. In the generator every prompt and every decoding step is a new shape, so a fix is harder; for now it is managed with `mem_guard.sh` + `run_resume.sh`, to be handled in Phase 6.
- **Lesson:** "I emptied the cache and it did not help" is not a conclusion, it is a clue. Reducing the symptom to the smallest piece (one model, synthetic input, one variable) and measuring two conditions side by side showed the root cause in minutes.

## Z14. The repetition block silently changed numbers from the source (Phase 5b)

- **Symptom:** `no_repeat_ngram_size` (8 and 12), tried to break the loop, produced fluent, cited but wrong answers: "2017" → "2020", "SC42" → "SC41", "0.5 MeV" → "0.7 MeV", "10⁻¹⁹" → "0-19".
- **Cause:** In a decoder-only model, transformers applies this rule to all `input_ids` including the prompt. Copying a phrase verbatim from the source chunk counts as "repetition", and the model slides to the nearest allowed token. The user had foreseen the same risk for `repetition_penalty`; number and citation questions were added to the sweep on the user's condition.
- **Fix:** No generation setting was adopted (the loops had already disappeared with the chunking fix). An n-gram block that counts only the answer was also tried: it did not break the loop, it made the model repeat the same content in different words.
- **Lesson:** When sweeping a "side-effect blocker", looking only at the problem cases is not enough; correct cases, especially those that need exact copying (numbers, codes, citations), must be in the control group too. And fixing the cause (long chunks) is cleaner than suppressing the symptom with a setting.

## Z15. With `re.IGNORECASE`, the Turkish "ı" made every English question Turkish (Phase 5c)

- **Symptom:** The first regex that detects the question language (`[çğıöşü…]`, `re.I`) counted all 82 questions of the development set as Turkish.
- **Cause:** In Python's Unicode case folding, `ı` (U+0131) is treated as equivalent to `i` and `I`. So a case-insensitive `[ı]` matches every `i`.
- **Fix:** The flag was removed and the capital letters were written into the class explicitly. Language detection is compared with the golden `lang` field on 82 questions in a unit test.
- **Lesson:** Do not use `re.IGNORECASE` in a regex that works with Turkish characters; or test the result against labelled data.

## Z16. A `None` document crashed the report after all answers were done (Phase 11)

- **Symptom:** The stereotype run answered all 13 questions, then `evaluate.py answers` failed while writing the report (`'<' not supported between 'str' and 'NoneType'`); the runner retried 15 times and gave up.
- **Cause:** The stereotype traps belong to no document, and `build.py` wrote `"document": null`; the report sorts rows by document.
- **Fix:** The traps get the document name `"none (stereotype trap)"`; a unit test checks that every row names a document. The 13 questions were run again from scratch (the checkpoint was kept aside, not edited); the persona and style files stayed byte-identical, so their 400 answers stayed valid.
- **Lesson:** Run a new golden file end to end with `--limit 2` before a multi-hour run: the report step only runs at the very end.

## Z17. `import evaluate` loaded the HuggingFace package (Phase 11)

- **Symptom:** `eval/fairness/analyze.py judge` failed: `module 'evaluate' has no attribute 'ask'`.
- **Cause:** Python puts the script's own folder (`eval/fairness/`) first on `sys.path`, not the project root, so `import evaluate` found the installed HuggingFace `evaluate` package.
- **Fix:** The project root is inserted into `sys.path` before the import.

## Z18. A wait condition matched "thresholds failed" (Phase 11)

- **Symptom:** The background wait for the Part 2 chain (`grep -E "…|failed|…"` on the chain log) reported the end after the first of four steps; the chain was still running.
- **Cause:** The fairness report prints "❌ thresholds failed: …" when a threshold fails, which is a normal result, not a crash.
- **Fix:** The wait matches only the runner's own messages (`part 2 done|retrieval failed|no report|gave up|keep failing`) and checks that the process is alive. Nothing was lost; only the notice came early.
- **Lesson:** Wait for a runner's specific end markers, not for generic words that the measured output can also contain.

## Z19. A claim's page must come from its own citation number (Phase 11)

- **Symptom:** The first holdout label list showed every page an answer cited next to each claim (one claim with 4 pages), which would have made the strict page rule impossible to apply.
- **Cause:** A row's `cited` lists the cited pages in order of first appearance of each `[n]` in the answer; the judgment's `cited` holds the claim's own excerpt numbers `n`. The two were joined without mapping `n` → page.
- **Fix:** `n` is mapped through the distinct `[n]` of the answer in order of appearance (asserted to have the same length as `cited`); the list was rebuilt before the user saw it (3 claim groups instead of 5).
- **Lesson:** When a label decision depends on a page, show the page of that claim's citation only, and assert the mapping.
