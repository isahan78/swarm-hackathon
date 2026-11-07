# Analysis: what the Kitaoka talk actually supports, and what to build from it

Written 2026-11-06 from the transcript alone. The paper (arXiv 2610.24052) has not been read yet; every number below is as spoken, and a talk is not a methods section. Where I am inferring rather than reporting, I say so.

## 1. The claims, ranked by how well the talk supports them

**Strong: splitting an attack across agents defeats a per-trajectory monitor.**
This is the paper's main result and it is almost definitional. A monitor that reads one trajectory at a time cannot see a plan that lives across three. The 97% evasion figure (18:37) is the number everyone will quote, but it is an upper bound on what a *human* red team can do with full knowledge of the monitor, not evidence that models would do this unprompted. He said as much: the attacks were hand-crafted (18:07) and agents "won't naturally coordinate on their own" (21:18).

**Interesting and unexplained: the full-information gap.**
A monitor given all three trajectories together still misses about 60% (19:07). This is the result that is *not* explained by the setup. Possibilities, all my inference:
- Context dilution. Three benign main tasks of noise around a thin side-task signal.
- Presentation. Concatenated trajectories vs interleaved by wall-clock time are very different inputs for a monitor.
- Prior. The monitor prompt may assume one agent, one task, so it never asks "do these agents share a goal?"
- Calibration transfer. The 8.5 threshold was calibrated to under 1% false positives, but on what benign distribution? If it was single-agent benign runs, the multi-agent operating point is not the same operating point.

He called explaining this gap a good, smaller hackathon project (56:29). I agree, and it is the cheapest real result available from this talk.

**Weak: models can plan these attacks.**
Claude Opus 4.8 reached 48% evasion against a weaker monitor, with an unmonitored planner, an unmonitored feedback channel, and iteration against the monitor's own output (22:27 to 23:15). Against a stronger monitor the success "collapses." So the capability claim and the scary headline point in different directions: human-planned attacks are nearly invisible, model-planned attacks mostly are not. Read the paper for whether the planning result holds at matched monitor strength before citing it.

**Unstated but load-bearing: sample size.**
Sixteen attacks. 82% caught cannot be 13 of 16 exactly, so either there are multiple runs per attack or the percentages are rounded over something else. That matters for the 3% figure especially. Check the paper.

**Scope he flagged himself:** no chain-of-thought monitoring, no agent-communication monitoring (33:48). This is a worst-case assumption, defensible, but it means the result says nothing about the monitoring stack labs are actually moving toward (synchronous, action-level, 11:00). The threat model is "async batch trajectory review only." Any project that extends his result should say which monitoring regime it is attacking.

## 2. What the Q&A revealed

- **Weight-space monitoring is a non-starter** for the reason Himanshu gave in chat: weights are frozen during inference. John redirected to activation monitoring and the refusal direction (51:56 to 54:38). The corpus backs that this is the live version of the idea: Arditi et al.'s difference-in-means "refusal direction" is described at lines 5183 to 5187 of the corpus, and the Open Problems paper argues that even "shallow, correlation-based descriptions could signal potentially concerning cognition" in a real-time monitoring setting (lines 2890 to 2903). So there is ground under an interp-flavoured monitoring project, but see section 3 for why it is a bad fit for this weekend.
- **Bryan's chat question** (42:09), whether agents adapt once they learn where the monitoring boundary is, is exactly the setup of the Opus 4.8 planning experiment. It was not answered live, and the answer in the talk is "yes, partially, against a weak monitor."
- **Nazmus's question** (40:53), decentralised planning, was also not answered. It is the harder version of the planning experiment: no single planner to monitor. Nobody has that result.

## 3. Hackathon triage

The clock is a weekend. The binding constraint John named twice is that multi-agent infrastructure eats the time (21:33, 27:09). So the filter is: can the multi-agent part be *transcript manipulation* rather than *live agents*?

**A. Explain the full-information gap.** Explore-stage. Take any control environment with trajectories (ControlArena is public), construct split attacks by editing transcripts the way he describes (16:10), and vary only how the monitor sees them: separate, concatenated, time-interleaved, with and without a prompt line saying agents may share a side task. The falsifier is clean: if the gap closes under interleaving or under the prompt change, the gap was presentation, not capability, and that is a publishable negative. If it does not close, you have narrowed the cause. Cost: one monitor model and prompts. No live agents. Needs his environment or a stand-in; email him (56:52).

**B. His per-action relevance monitor.** Understand-stage version of A. Monitor emits a suspicion score plus a per-action "relevance to stated task" score; low-relevance actions are correlated across agents. Falsifier: it fails to beat the concatenated-trajectory baseline at matched false-positive rate. Risk: it is the obvious idea and three other teams will build it. Worth doing only if A points at it.

**C. Token-matched audit of multi vs single agent claims.** He claimed most headline multi-agent gains vanish when you control for tokens (28:39). A weekend literature audit that checks which published comparisons actually matched tokens is cheap, needs no compute, and is the kind of thing judges remember. Falsifier: the claim is wrong and the gains survive matching. Either outcome is a result.

**D. Activation-based side-task detection.** Train a probe or difference-in-means direction for "pursuing a hidden side task" on an open-weight model, compare against the black-box monitor at matched false-positive rate. Grounded in the corpus (above), and it is the one direction where this project's mech-interp tooling is an advantage. But: you need an open-weight policy model running the attacks, which means standing up the environment yourself, which is the multi-agent tax again. A one-agent version is honest and cheaper: does an activation probe catch the *solo* attacks the 82% black-box monitor catches, and does it catch any of the 18% it misses? That is single-trajectory control, not swarm work, so expect judges to ask why it is here.

**E. Same-family collusion.** Does a GPT monitor grade a GPT policy more leniently than a Claude policy on identical transcripts? Pure prompt-and-grade experiment, no live agents, clear falsifier. He named it as open (32:24). The confound is that transcripts from different models differ in style, so you need to swap the *attribution* while holding the transcript fixed. Cheap and clean.

**Verdict.** A or E, not B or D. Both are transcript-only, both have a falsifier you can state in one sentence, and both are questions he said are open. D is the interesting one for someone with interp tooling but it is a Monday-to-Friday project, not a Friday-to-Sunday one.

## 4. Things to be careful about when citing this talk

- "UKAC" in the transcript is almost certainly UK AISI.
- "Control tower" at 15:33 is ControlArena.
- The Hugging Face incident, the OpenAI disclosure, and swarms.wiki are presented as fact in the talk. Verify from the linked sources before repeating them in a write-up.
- Model names (GPT Sol, GPT Luna, Opus 4.8) are as spoken. Check the paper for exact identifiers.
