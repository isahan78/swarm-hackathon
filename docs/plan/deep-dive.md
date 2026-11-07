# Project deep dives

Written for: you and your prospective teammates, to pick one and start.

Context assumed: global track (team preferred), compute is one RunPod GPU with about $12 of credit plus Anthropic (Claude) API access from a Max plan, no GPT-5.6 monitors. Deadline Sunday Nov 8, 23:59 Anywhere on Earth. Judging: Impact & Innovation, Execution, Presentation, each 1 to 5, not scored on polish. A Limitations and Dual-Use appendix is required.

Two constraints shape every design below:
- **Calls are scarcer than dollars.** Max-plan Claude access is rate-limited and not a bulk batch API. An experiment that needs thousands of model calls will stall on rate limits before it runs out of money.
- **The cheap-actor / expensive-referee split.** Where a project needs many agents, host a small open-weight model on the RunPod GPU to be the agent population (unmetered) and spend Claude only on the one role that has to be smart: the monitor or the grader. $12 covers a 7-to-8B model on a 4090-class card for most of a weekend.

A recurring theme: for every one of these, the result is only worth submitting if it has a **control**. The speakers all conceded this was the field's weak spot. Your control is your edge.

---

## Project 1 — The joint-monitoring gap, with a Claude monitor

**Track 4.** Verbatim prompt: "Can a monitor that sees only part of the messages detect collusion or hidden communication?"

### The live question
Kitaoka's paper reports three detection rates for a side task spread across several agents: a monitor reading each agent alone catches 7%, a single agent doing the whole thing is caught 87%, and a monitor reading **all the colluding agents together** still catches only 41%. The first number is almost definitional, you can't flag what isn't in front of you. The third is the surprise: with full information, the best-case monitor misses most of them, and Kitaoka said outright he doesn't know why. He called explaining it a good hackathon project.

You can't reproduce his exact numbers because his monitors were GPT-5.6 Sol and Luna and you don't have them. That turns the project into a sharper question: **does the gap exist at all when the monitor is Claude, and if so, which part of the setup causes it?** A gap that is specific to one model family is a more interesting finding than one that generalizes, and it connects to his own open question about same-family collusion.

### Hypotheses, each a separate condition
- **Presentation.** The joint view concatenates agents back to back. Re-ordering the same content interleaved by time changes what stands out.
- **Dilution.** Each agent's benign main task is noise around a thin signal, dragging the suspicion score down.
- **Framing.** The monitor prompt assumes one agent and never asks whether these agents share an objective. Adding one sentence tests this.
- **Calibration.** The threshold was set on single-agent benign runs; the joint operating point may not be the same point.

### Falsifier
If interleaving by time, or adding a "these agents may share a hidden objective" line to the monitor prompt, pushes joint detection up toward the single-agent rate, then the 41% was a presentation and prompting artifact, not a limit of the monitor. Publishable either way: "the scary gap closes with one prompt line" is a genuinely useful result for anyone building oversight.

### Design
You need transcripts where a side objective is split across N agents, each individually plausible, plus a benign set to calibrate the threshold. Three ways to get them, cheapest first:
1. **Synthesize minimal ones yourself.** You don't need Kitaoka's infrastructure to study the *monitor*. A small set of hand-built or lightly-generated scenarios (his own method was modifying transcripts by hand) where a benign-looking fragment per agent composes into something a monitor should catch. Full control, inference only, no GPU.
2. **ControlArena** (Redwood, open) for more realistic trajectories.
3. **MiniLab**, request-only: email Kitaoka Friday; treat as a bonus if it arrives, not a dependency.

Conditions per scenario: per-agent monitor, joint-concatenated, joint-interleaved, joint-with-coordination-prompt. Metric: detection rate (fraction above threshold) with confidence intervals, plus a benign control set to fix the threshold at a stated false-positive rate. **Sanity check first:** confirm the per-agent monitor actually misses your split scenarios. If your hand-built splits are too obvious and get caught per-agent, there is no gap to explain and you fix the scenarios before going further.

### Minimum viable result
8 to 12 scenarios, one Claude monitor, four reading conditions, a benign calibration set, one detection-rate table with CIs. That is a complete paper.

### Strong version
Several Claude tiers as monitors; ablate which single prompt change matters; test whether a reasoning monitor closes the gap on its own.

### Compute
Inference only, no GPU required. Rough budget: 12 scenarios x 4 conditions x 5 readings plus ~50 benign calibration calls is under 300 calls. Pace them and you stay inside rate limits.

### What makes it meaningless
No benign calibration set, so the threshold is arbitrary and the detection rates aren't comparable. Scenarios so artificial the per-agent monitor already catches them.

### Dual-use
Studies the monitor; the output improves detection. You release split scenarios at demonstration fidelity, not tuned attacks. Lowest-risk of the four.

### Fit
Light compute, sharp question, one-person-finishable. Narrative is strong: "we explain a number from a paper three weeks old." Best choice for a small or uncertain team.

---

## Project 2 — Does breaking a task into pieces lower refusal, and what restores it?

**Track 2.** Verbatim prompt: "Do agents that each refuse a harmful task complete it once it's split across them?"

### The live question
An agent that refuses a request as a whole may comply with a fragment that looks innocent on its own. It's on the organisers' track list, so it's in scope by design. Existence is not the contribution, everyone expects it. The contribution is **measuring the effect size across models** and, the real deliverable, **measuring what brings the refusal back.**

### Use a harmless proxy target
You do not need a genuinely dangerous "whole" to demonstrate the effect, and you shouldn't use one. Pick a target that is against a stated rule but harmless: get the model to emit a specific banned phrase, or assemble a fake secret, where the forbidden whole is benign. This sidesteps both the ethics appendix and the output classifier, and it's cleaner science because you control the ground truth exactly.

### The confound you must kill (Lydia Ashton's point from talk 2)
If models comply with roughly two-thirds of any instruction, "it complied with a fragment" says nothing about decomposition. You need:
- a **base-rate control**: compliance with fragments of a *benign* whole;
- a **manipulation check**: afterward, ask the model what the fragments assembled to, to see whether it even could have known.

Without these, your headline number is confounded and the result is empty.

### Design
A small set of rule-violating-but-harmless wholes, each broken into individually-innocuous fragments. Per model: (a) present the whole, measure refusal; (b) present fragments in separate contexts, measure fragment compliance; (c) manipulation check. Then mitigations as the deliverable: a standing instruction to name the larger task a fragment serves and refuse if that whole is refusable; a second-pass reviewer that sees the fragments jointly; a self-check step.

### Falsifier
If one standing instruction removes the effect, it's a prompting gap, not a training gap, and that's the finding. Alternatively, if the manipulation check shows models genuinely cannot tell the fragments compose to the forbidden whole, it's a capability limit, not an alignment failure, and the framing changes.

### Minimum viable result
10 wholes, 2 to 3 Claude tiers, the refuse-vs-fragment contrast, the base-rate control, the manipulation check, one mitigation with its effect size.

### Compute
Pure Claude inference, small N, no GPU. Light. Watch rate limits but comfortable.

### What makes it meaningless
Skipping the base-rate control or the manipulation check. Using a real harmful target, which adds risk for no scientific gain.

### Dual-use
Clean if the target is a harmless proxy and the deliverable is the mitigation. Do not publish a tuned decomposition.

### Fit
Easiest to execute of the four, and the easiest to turn into a meaningless number if rushed. Innovation ceiling is lower because the base effect is expected; your novelty has to live in the mitigation and the rigor.

---

## Project 3 — Does misalignment spread through a population, and does network shape matter?

**Track 2** ("how fast and how far does bad behaviour spread, and does network shape matter?"), doubling as a **Track 1** sandbox. This is Gutenberg's memetic-misalignment question.

### The live question
The Hugging Face story goes from one coordinating agent to around 1,200, which implies the spread accelerates, but nobody has measured the adoption curve. Seed one agent in a small population with a marker behaviour and measure the probability that a fresh agent adopts it given that k agents already have it, for k = 0, 1, 2, 3. Then change the communication graph and see whether the curve's slope changes.

### Use a benign marker behaviour
The behaviour that spreads must be harmless: a convention, like signing messages with a codeword, or preferring one harmless strategy. You're measuring *contagion dynamics*, not a dangerous capability, and a benign marker keeps the dual-use line trivial and the detection easy.

### Design
A toy sandbox with 5 to 20 agents and a shared channel (a message board or a shared file). Seed one agent with the marker. Agents take turns; measure whether and when uninfected agents adopt it. Vary the topology (fully connected, star, ring), the population size, and whether the seed agent justifies the behaviour or just exhibits it.

**Positive control first:** verify the environment *can* show propagation by instructing all agents to adopt the marker and confirming they do. If they can't even when told, the null later means nothing.

### The compute design that makes this affordable
Host a small open-weight model (Qwen or Llama class, 7 to 8B) on the RunPod GPU as the whole agent population, unmetered. Detect adoption of a codeword with a regex, so you spend no Claude calls on grading at all; keep Claude in reserve only if the open model is too incoherent to show social dynamics, in which case it plays the agent role for a scaled-down run. $12 covers a 7B on a 4090-class card for most of the weekend.

### Falsifier
A flat adoption curve means no contagion, and the acceleration story people tell about the 1,200 is wrong or at least not mechanistic. A flat curve is a real, submittable result.

### Minimum viable result
One topology, population around 8, a benign marker, the adoption curve for k = 0 to 3, and a no-seed control. Clean and complete.

### Strong version
Three topologies, two population sizes, showing network shape changes the slope, tied explicitly to the Hugging Face timeline.

### Compute
Open model on RunPod carries the population; regex grading is free; Claude only as a fallback. This is the project the $12 GPU was made for.

### What makes it meaningless
No positive control, so you can't tell a real null from a broken harness. Too few agents or rounds to see a curve. A marker so trivial it spreads by coincidence, or so odd it never spreads.

### Dual-use
Benign marker, spread dynamics only. Clean.

### Fit
Highest ceiling and best fit to this event: it's the emergence-and-contagion question the whole hackathon is themed on, and a contagion curve plus a network diagram is a memorable figure. The one project with real build risk, because you stand up an environment Friday night. Best for a team with someone comfortable building a harness; risky solo.

---

## Project 4 — A content-level collusion detector on the real logs

**Track 4.** Verbatim prompt: "Using real swarm logs, build a tool that finds coordination or covert channels between agents."

### The live question
The swarmtraces dataset is downloaded and profiled (`data/swarmtraces/README.md`): 189,579 rows, parent-child links on 61k of them, payload / response / recovered-text kinds, and a text field full of the actual attack payloads. It has **no timestamps and no IPs**, so Howard-Jones's traffic-timing detector is impossible from this file. The reachable question is content-level: can you flag coordination from *what the payloads say and how they relate*, better than a trivial baseline?

### The hard part: there are no labels
"Coordinated vs independent" is not marked in the data. You have to construct an evaluation, and this is the crux a judge will poke:
- Use the `parent_id` chains as weak positive labels for "related," and random pairs as negatives.
- Or inject synthetic independent payloads as clean negatives.
- Hold out a slice for evaluation.
Be explicit about the proxy's weakness and validate it.

### Design
Signals: reuse of the same technique across payloads, chains where one agent's response seeds another's payload, shared redacted destinations or credential placeholders. Build a detector on these. Baseline: near-duplicate text clustering (MinHash or embeddings). The detector has to beat the baseline at separating chained pairs from random pairs on held-out data.

### Falsifier
If the detector doesn't beat near-duplicate detection, the "coordination signal" was just repetition, and that is itself worth reporting.

### Minimum viable result
Data profile (done), a near-duplicate baseline, one content-feature detector, an evaluation on the chain-vs-random-pair task, and a precision-recall or AUC number.

### Compute
Laptop. Embeddings run locally or on the RunPod box; Claude optional to label a small sample. Nearly free, runnable tonight.

### What makes it meaningless
No baseline, so "it finds clusters" proves nothing. An unvalidated label proxy. Overfitting the one incident, which Howard-Jones warned about directly: frame it as a method demonstrated on the one public corpus, not a general detector.

### Dual-use
Purely defensive; reads an already-public, redacted corpus. Lowest risk.

### Fit
The surest finish and the lowest ceiling. The no-timestamps limitation already cut the flashiest version. Best if your priority is to definitely ship something clean.

---

## Ranking, for your constraints

| | Innovation ceiling | Execution risk | Compute fit | Judge fit (this event) | Solo-safe |
|---|---|---|---|---|---|
| 1 Joint-monitoring gap | High | Low | Excellent (inference) | High (Track 4, topical) | Yes |
| 2 Decomposition vs refusal | Medium | Low | Excellent (inference) | Medium | Yes |
| 3 Spread / contagion | High | Medium-high (build) | Excellent (open model on GPU) | Highest (event's theme) | No |
| 4 Log detector | Medium-low | Low | Excellent (laptop) | Medium | Yes |

### The hedge worth knowing
Projects 1 and 3 share a substrate: a small open model playing several agents, plus Claude as monitor. If you build that toy swarm first, you can run the contagion experiment (project 3); and if the environment proves too hard to make interesting in time, the same generated transcripts feed straight into the monitoring question (project 1). Committing to the substrate hedges the project choice until Saturday.

### My recommendation
- **Solid team with someone who can build a harness:** Project 3. It's the event's own question, the compute design is elegant and cheap, and the figure is memorable. Build the substrate Friday; it's also your fallback into Project 1.
- **Small or uncertain team, or might end up solo:** Project 1. Sharpest question, lightest compute, finishable by one person, strong "we explain a brand-new paper's mystery" narrative.
- **You want to guarantee a clean finish over a high ceiling:** Project 4, runnable tonight on data already on disk.
- Project 2 only if the team is drawn to it, and only with the base-rate control, the manipulation check, and a harmless proxy target locked in from the start.
