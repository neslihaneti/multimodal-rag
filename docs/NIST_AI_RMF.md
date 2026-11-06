# NIST AI RMF: Self-Assessment

A self-assessment of this project against the NIST AI Risk Management Framework (AI RMF 1.0, January 2023) and its
Generative AI Profile (NIST AI 600-1, July 2024). **It is not a claim of conformance.** The AI RMF is written for
organizations; this is a one-person project, so several outcomes, most of GOVERN, have no counterpart here. Those
rows say so.

Status: **Met**: evidence in the repository · **Partial**: some of the outcome · **Gap**: missing · **N/A**: does
not apply to a single-user local tool.

## 1. AI RMF core functions

| Function | What the outcome asks for | Evidence in this project | Status | Gap |
|---|---|---|---|---|
| GOVERN | Policies and processes for AI risk, documented and in place | Success criteria and thresholds agreed in writing before the work (`phases/BASARI_TANIMI.md`); rule that model changes are proposed and approved before they start; non-regression rule (> 1 question drop must be justified or rolled back) | Partial | No organizational policy, risk tolerance statement or review board |
| GOVERN | Roles, accountability, training | One owner decides; each phase has a dated report (`phases/faz-N/RAPOR.md`) and a lessons log (`phases/ZORLUKLAR.md`) | Partial | No separation between developer and approver beyond the owner |
| GOVERN | Third-party models and data | Model names recorded in every evaluation report | Partial | No license or model-provenance review written down |
| MAP | Context, intended use and users established | `docs/MODEL_CARD.md`: purpose, intended use, out-of-scope uses, languages | Met | |
| MAP | Capabilities, limits and risks of the AI identified | Limitations in the model card; failure analyses in phase reports (sdpa collapse, repetition loops, n-gram blocking changing numbers) | Met | |
| MAP | Impacts on individuals and groups | Turkish vs. English gap measured and reported | Partial | No assessment beyond language |
| MEASURE | Methods and metrics chosen and documented | Retrieval (Recall@k, MRR), answer (correctness, faithfulness, citation precision, refusals), latency and time to first text; `evaluate.py` | Met | |
| MEASURE | Evaluated before deployment, on data not used for development | Sealed 72-question holdout, run once (`phases/final/RAPOR.md`) | Met | |
| MEASURE | Measurement validity | LLM judge checked against human labels on stratified samples, Cohen's κ per decision type, three rounds | Met | Labels from one person: no inter-annotator agreement |
| MEASURE | Feedback and tracking over time | Every run versioned: golden set, prompt and judge hashes, settings | Partial | No monitoring after deployment |
| MANAGE | Risks prioritized and treated | Refusal rewritten in code; prompt token budget; memory guard; injection-safe context summaries | Met | |
| MANAGE | Benefits vs. risks; option not to deploy | Thresholds decide; the holdout is the release gate | Partial | No go/no-go record besides the phase reports |
| MANAGE | Post-deployment monitoring, incidents, decommissioning | | Gap | No logging of production questions, incident process or drift monitoring |

## 2. Generative AI Profile (NIST AI 600-1) risks

| GAI risk | How it shows up in a document RAG system | Control and evidence | Status |
|---|---|---|---|
| Confabulation | Answering beyond the excerpts or inventing facts | Prompt limited to excerpts and page images; claim-level faithfulness 0.94 on the holdout (0.958 human-checked); unanswerable questions refused 15 / 15; false refusals 0.02. Case: HF `no_repeat_ngram_size` (tried against repetition loops) also blocks n-grams of the prompt, so the model silently changed copied numbers (2017 → 2020, 0.5 → 0.7 MeV); decoding penalties were rejected and loops reduced by re-chunking instead (`phases/faz-5b/RAPOR.md`) | Met |
| Information integrity | Users cannot check where an answer came from | Every sentence cited; citation precision 0.87; gold page cited 0.95; source pages shown in the UI | Met |
| Information security | Instructions hidden in indexed documents (indirect prompt injection) | End-to-end test with hidden white text and a fake note to AI systems: no canary or URL in context or answer | Met (one attack type tested) |
| Data privacy | Documents sent to third parties | Everything runs locally; no external API; credentials in `.env`, outside version control | Met |
| Human-AI configuration | Over-reliance on fluent answers | Cited page images and search details next to each answer; fixed refusal sentence | Partial: no user study |
| Harmful bias and homogenization | Unequal quality across groups of users | Language is the only group measured: Turkish 0.70 vs. English 0.96 correct on the holdout, causes analysed, two fixes after the holdout | Partial |
| Value chain and component integration | Behaviour of third-party models and libraries | Each failure traced to a component (MPS sdpa, HF `no_repeat_ngram_size`) and pinned around | Partial: no supplier review |
| Environmental impacts | Energy use | Local 4B model on one machine; not measured | Gap |
| Intellectual property | Reproducing copyrighted documents | Answers quote the user's own documents to the user | N/A for single-user use |
| CBRN information; violent, hateful or obscene content | Generating harmful content | System only answers from the user's indexed documents; not tested | Not assessed |

## 3. Main gaps

1. Monitoring after deployment and an incident process (MANAGE): none, as the tool is not deployed.
2. Organizational governance (GOVERN): replaced by written criteria and an approval rule for one person.
3. Human labels from a single annotator: κ measures judge vs. one person, not agreement between people.
4. Security testing covers one indirect injection pattern, not a red-team exercise.
