# Related work and methodological implications

Sources checked on 2026-11-08. These are findings reported by other researchers, not measurements from this project. All four user-supplied links were reachable through the web reader. A shell clone of the public repository failed at the local proxy; some web subdirectory links were also denied. Specific uninspected source functions are therefore not represented as verified interfaces.

## Recruitment and prediction horizon

Leonidas Raghav's [Pre-Crime for Agents, at the Last Second: Probing When a Recruited Agent Gives In](https://arxiv.org/abs/2610.40588) was submitted on 29 October 2026. It studies a peer pressuring a target to disclose synthetic protected values. The paper distinguishes eventual episode outcomes, short-range outcomes and the output of the current model call. Its reported warning is strongest for the current call and much weaker for eventual recruitment. This motivates separating strict pre-generation sampling from multi-turn advance warning: a context-only vector can still be an imminent-action detector. The paper also reports detection of permitted disclosures, making authorization controls essential. None of its reported model results should be imported as findings about Qwen3-8B or file-ownership violations.

## Public implementation and reusable ideas

The [public precrime-agents repository](https://github.com/leonidas1712/precrime-agents) describes these components:

| Directory | Role described in the public README | Reuse boundary |
| --- | --- | --- |
| `experiments/E01-behaviour-pilot/` | Agent harness, scenarios and outcome scoring | Reference for protocol; not imported into this harness |
| `experiments/E02-activation-replay/` | Replay of target requests and fidelity checks | Illustrates why replay/template fidelity must be verified |
| `experiments/E05-probes/` | Probe fitting and evaluation | Reference for episode-level holdouts and horizon separation |
| `experiments/E06-monitors/` | Transcript monitors | Reference for matched observations |
| `paper-arxiv/numbers.yaml` and `runs/` | Result provenance | Model for linking claims to artifacts |

Its README reports that a trained bag-of-words baseline nearly matches the activation probe and that repeated per-call alarms produce many episode-level false alarms. We therefore include a trained TF-IDF baseline and report episode-level clean alarms as well as per-decision metrics. The public code is separate from Isahan's supplied archive; it is not evidence about his interface.

## Strategic deception probes

Goldowsky-Dill, Chughtai, Heimersheim and Hobbhahn's [Detecting Strategic Deception with Linear Probes](https://proceedings.mlr.press/v267/goldowsky-dill25a.html), ICML 2025, evaluates probes trained using contrasting honesty/deception instructions and roleplaying examples, then tests generalization to more realistic deceptive behavior in Llama-3.3-70B-Instruct. The authors report strong discrimination but explicitly do not regard the approach as a robust defense. Our experiment adopts lightweight linear probes as a monitor family while avoiding an inference from correlated neural activity to an agent's intentions. Its task and training distribution differ from recruitment under file-ownership rules.

## Sleeper-agent probes

Anthropic's [Simple probes can catch sleeper agents](https://www.anthropic.com/research/probes-catch-sleeper-agents), published 23 April 2024, studies deliberately trained sleeper-agent models. It reports that generic contrast-pair probes can identify trigger-associated defection across several constructed settings. It also identifies the unresolved question of generalization to naturally occurring deceptive alignment. The original `/news/` URL redirects to this research page. This supports testing whether a linear signal exists; it does not establish that recruitment susceptibility is represented similarly in an unmodified Qwen model.

## Frozen interpretation rules

1. Context-only sampling is necessary for strict pre-response claims; it is insufficient for a claim of several-turn advance warning.
2. Report zero-step alerts as imminent-action detections and positive-step alerts as advance warnings.
3. Compare exposed resistant targets against exposed defecting targets to separate outcome prediction from exposure detection.
4. Fit trained text and activation models on the same grouped training split; tune thresholds only on validation groups.
5. Evaluate clean false alarms over complete target conversations, retaining never-alerted and non-defecting targets.
6. Treat authorization-aware controls, stronger held-out prompts and cross-setting generalization as additional experiments, not assumed consequences of probe accuracy.

For the separately inspected collaborator archive, exact callable and activation-layer details are documented in [collaborator_integration.md](collaborator_integration.md). Its original content/task-scope label differs from this project's cross-owner action-attempt label.
