# probe/ — PREEXISTING CODE (reused, not written for this hackathon)

Every file in this directory was written **before** the Swarm Alignment Hackathon,
as part of the author's prior "Probe–Text Gap" research
(github.com/isahan78/ais-research, `experiment/`). It is copied in unchanged so the
submission repo is self-contained. Per the hackathon rules, it is marked preexisting
here and in the report.

| File | What it does | Role in this project |
|---|---|---|
| `harvest_activations.py` | Forward-pass + hook to pull residual-stream vectors from the model | Reference for the activation-capture hook we wire into the live loop |
| `train_probe.py` | Trains a linear probe (logistic regression) on activations → label | Trains the co-option probe |
| `cross_fit.py` | Held-out / cross-fit evaluation so the probe can't leak | Honest eval, held out by objective |
| `text_classifier.py` | TF-IDF / bag-of-words text baseline | The transcript-monitor baseline |
| `text_floor.py` | Text-only performance floor | Sanity floor for the text monitor |
| `llm_judge.py` | LLM-as-judge scaffold | Candidate for the faithfulness judge pass |
| `make_figures.py` | Plotting for detection / comparison figures | The two headline figures |

**New code written for this hackathon lives in `swarm_env/`** (the swarm, the
multi-agent loop, and the live activation capture that bridges the loop to this probe).
