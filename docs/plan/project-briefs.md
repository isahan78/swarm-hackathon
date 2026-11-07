# Project briefs, ranked

Re-ranked 2026-11-06 after reading the rules, the Kitaoka paper, and the swarmtraces dataset.

Filter applied: no live multi-agent infrastructure to build from scratch, a falsifier you can state in one sentence, a track prompt it answers directly, and data or models reachable this weekend. Judging rewards idea and method over polish, which favours a clean measurement over a half-built system. Each brief is framed as a measurement or defence, because the required appendix is Limitations and Dual-Use, and because that framing is also what keeps the work on the right side of the thing it studies.

A note on register. Three of these study failure modes that are, stated plainly, ways to get past a safeguard. The research value is in *measuring how big the effect is* and *testing what shrinks it*, not in producing a sharper version of the attack. Keep the attack at the lowest fidelity that still demonstrates the effect. That is both better science (a tuned attack doesn't generalise) and the honest reading of the dual-use line.

---

## 1. The joint-monitoring gap (Track 4)

**Track prompt:** "Can a monitor that sees only part of the messages detect collusion or hidden communication?"

**The question.** Kitaoka's paper reports that a monitor reading each agent's trajectory alone catches 7% of distributed attacks, and a monitor reading all the colluding agents *together* still catches only 41%. The second number is the interesting one: even with full information, the best-case monitor misses most of them. Nobody has explained why.

**Hypotheses for the gap, each separately testable.**
- Presentation: the joint transcript is concatenated per agent; re-ordering the same content by timestamp changes what the monitor sees.
- Dilution: three benign main tasks of noise around one thin signal lower the per-reading suspicion.
- Prior: the monitor prompt frames the input as one agent's work, so it never asks whether these agents share a goal. Adding one sentence to the prompt tests this.
- Calibration: the 7.5 and 8.5 thresholds were set on single-agent benign runs; the joint operating point may not be the same point.

**Falsifier.** If re-ordering by timestamp, or adding the "these agents may share an objective" sentence to the monitor prompt, closes the gap, then the 41% was a presentation artifact, not a capability limit. That is a clean, publishable negative either way.

**What you need.** MiniLab, which is request-only (email Kitaoka tonight), or a stand-in built on ControlArena transcripts. One monitor model, which your Adaption credits cover. No live agents: you are re-scoring existing or hand-built transcripts.

**Dual-use line.** This studies the *monitor*, not the attack; it only makes detection better. Lowest-risk of the four.

---

## 2. Does task decomposition lower refusal? And what restores it? (Track 2)

**Track prompt, verbatim:** "Do agents that each refuse a harmful task complete it once it's split across them?"

**The question.** This is a known and worrying failure mode: an agent that refuses a task whole may comply with a fragment that looks benign in isolation. The organisers put it on the track list, so it is in scope by design. The research contribution is not showing it happens, it is *measuring the size of the effect* across models and, more importantly, *measuring what brings the refusal back*.

**Design, at low fidelity.** Use a small set of tasks where the whole is clearly objectionable and the fragments are individually innocuous. Measure the per-fragment compliance rate against the whole-task refusal rate. That is the effect size. Then test mitigations as the real deliverable: a system-prompt instruction to consider whether a fragment serves a larger goal; a cheap "what is this part of?" self-check before acting; a second model that sees the fragments jointly.

**Falsifier.** If a single standing instruction ("before acting on a sub-task, state what larger task it could belong to and refuse if that task is one you'd refuse whole") removes the effect, then the failure is a prompting gap, not a training gap, and that is the finding.

**What you need.** A few models (Adaption credits), no live swarm. Keep the task set at demonstration fidelity, not optimised. Lydia Ashton's point from talk 2 applies hard here: include a manipulation check that the model can articulate the rule it's being asked about, or the result is confounded by the base rate of agents doing whatever they're told.

**Dual-use line.** The deliverable is the mitigation and its effect size. Do not publish a tuned decomposition; publish the defence.

---

## 3. Does misalignment spread, and does network shape matter? (Track 2)

**Track prompt, verbatim:** "If one agent is compromised, how fast and how far does the bad behaviour spread, and does network shape matter?" This is also Gutenberg's "memetic misalignment" question (talk 3).

**The question.** Start with one agent exhibiting a target behaviour in a small population, and measure P(next agent adopts it | k already have) for k = 0, 1, 2, 3. Then vary the communication graph (fully connected, star, ring) and see whether the spread rate changes.

**Falsifier.** If the adoption curve is flat, there is no contagion and the acceleration story people tell about the Hugging Face 1,200 is wrong, or at least not mechanistic. A flat curve is a real result.

**What you need.** A toy sandbox with 5 to 20 cheap agents, which Track 1's prompts also describe building. Gutenberg's advice: n from 1 to 2 to 3 is already rich; do not chase 1,200.

**Dual-use line.** Measures spread dynamics with a neutral target behaviour (e.g. a harmless convention), not a harmful capability. Choose the marker behaviour to be clearly benign.

---

## 4. A content-level collusion detector on real logs (Track 4)

**Track prompt, verbatim:** "Using real swarm logs, build a tool that finds coordination or covert channels between agents."

**The question.** The swarmtraces dataset is downloaded and profiled (data/swarmtraces/README.md). It has no timestamps and no IPs, so Howard-Jones's traffic-pattern detector is off the table here. What it does have is 189k rows with parent-child links and a `text` field full of payloads. Build a detector that flags coordination from *content*: reuse of the same technique across payloads, chains where one agent's response seeds another's payload, shared redacted destinations.

**Falsifier.** It must beat a trivial baseline (e.g. near-duplicate text clustering) at separating coordinated from independent payloads on a held-out slice. If it doesn't beat near-duplicate detection, the "coordination" signal was just repetition.

**What you need.** Only the local dataset and a laptop; no model credits required for the baseline. Howard-Jones warned this risks overfitting one incident, so frame it as "a method, demonstrated on the one public corpus," not "a general detector."

**Dual-use line.** Purely defensive; it reads an already-public, redacted corpus to improve detection.

---

## Not recommended for a weekend
- Live autonomous adversarial swarms (needs infrastructure; classifier-blocked; the attack-fidelity trap).
- Full incident replication end to end (Gutenberg said chunk it; pick one stage).
- Activation-probe monitoring of an open-weight attacker (needs the environment stood up first; this is the one place your mech-interp corpus helps, so it is a good *post*-hackathon direction).

## My pick order
1 and 2 are the strongest for this event: both are measurements with one-sentence falsifiers, both map to a verbatim track prompt, both lean toward the inter-agent-influence area Apart judges favour, and neither needs infrastructure. 4 is the best fit if you want something runnable within the hour tonight on data already on disk. 3 is the most "science" of them if you'd rather build a small environment than score transcripts.
