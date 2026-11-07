# Innovative projects: cross-talk collisions

Written for: you and your teammates, for the "high ceiling" option.

The four briefs in [deep-dive.md](deep-dive.md) each come from one talk. The ideas here come from colliding two or three talks at a point nobody connected during the event. Every one is framed as measurement or defence, uses a benign marker, and has a one-sentence falsifier, because an innovative idea without a falsifier is just a vibe and the judges will know.

The headline is first. The rest are ranked after it.

---

## HEADLINE — Herd immunity for agent swarms: does a defence spread as fast as the exploit?

**Collides:** Gutenberg's memetic misalignment (one bad agent becomes many) + Fleming's "no scar tissue" (agents don't learn from being tricked, so the next agent repeats the mistake) + the inoculation-prompting papers from Kitaoka's chat (Tan et al., Wichers et al.).

### The reframe
The entire hackathon is themed on a scare: misalignment spread from 1 agent to 1,200. Every project is chasing the pathogen. **Nobody is asking whether the cure spreads too.** Fleming pointed straight at the gap: agents have no shared memory, so when one is manipulated, the lesson dies with the session. But what if it didn't? If one agent that detects and resists a manipulation writes a short note to a shared store, do downstream agents resist better, and **does that immunity propagate through the population faster or slower than the exploit does?**

This is the defensive inverse of the event's flagship question, and it is a genuinely novel framing. It turns a known-scary result into a constructive one.

### Design
Use the open-model-on-RunPod swarm as the population. Two propagating quantities in the same environment:
- **the exploit**: a benign marker behaviour that spreads agent to agent (as in deep-dive Project 3), standing in for a manipulation technique;
- **the immunity**: a short "I was asked to do X by untrusted text; I declined and here's the tell" note written to the shared channel by any agent that resists.

Measure two curves on the same population: adoption of the marker, and adoption of resistance, each as a function of how many agents already carry it. The question is which curve is steeper.

### Falsifier
If seeding immunity notes does not raise downstream resistance above the no-note control, then shared memory doesn't transmit defence and the "scar tissue" idea is wishful. A null is a real, publishable result: it tells the field that memory alone won't save you.

### Why it wins
It reframes the signature result of the weekend; it's visually a two-curve race (memorable figure); it's defensive and benign end to end; it synthesises three talks; and it answers Fleming's self-policing-swarm open direction and Gutenberg's memetic question at once. Innovation score bait, honestly earned.

### Compute
Open model is the swarm (RunPod, unmetered), regex or a cheap check detects marker and resistance adoption, Claude only as a fallback judge. Fits your $12 exactly.

### Risk
Same build risk as Project 3, plus you need the resistance note to actually transmit something learnable. Positive control: hand every agent the note up front and confirm resistance rises; only then run the propagation version.

---

## 2 — The auto-grouping monitor: solve the corroboration problem Kitaoka left open

**Collides:** Kitaoka's missing corroboration layer (a joint monitor catches 41% but "a monitor is unlikely to be able to identify and read all colluding agents together") + Howard-Jones's grouping intuition (traffic and behaviour patterns tell you which agents belong to one swarm).

### The idea
Kitaoka's joint result cheats: it assumes you already know which agents to read together. In the real world that's the hard part. Build the missing stage. A two-step monitor: first cluster agents by behavioural similarity (shared destinations, reused techniques, response-to-prompt chains, the content signals that survive in logs), then feed each discovered cluster to a joint monitor. **Measure whether auto-grouping recovers the 41% joint detection, or any lift over per-agent, without being told who colludes.**

### Falsifier
If detection with auto-discovered groups is no better than reading each agent alone, then grouping is the bottleneck and knowing-who-to-watch is the real unsolved problem, which is itself the most useful thing you could tell the field.

### Why it's strong
It's the single most-wanted artifact across the top two talks, nobody built it, and it's inference plus clustering, no live agents. Clean story: "Kitaoka assumed the group was known; we remove that assumption and measure the cost."

### Compute
Inference plus local clustering. Light. No GPU strictly needed; RunPod can host the embedding model.

### Risk
Needs the same transcripts as Project 1. The grouping step can fail quietly; validate it on cases where you know the true grouping.

---

## 3 — Contagion versus correction: an epidemic model for a swarm

**Collides:** Gutenberg's spread question + Fleming's "agents in their own swarm might police each other and pull a defector back."

### The idea
Run infection and correction in the same population at the same time. Seed one agent carrying a benign marker that spreads, and a number of "auditor" agents that try to reverse it in neighbours. Sweep the auditor-to-agent ratio and the network topology, and find the threshold where correction wins versus where contagion wins. This is a susceptible-infected-recovered model, but for agent behaviour, which as far as the talks show nobody has written down.

### Falsifier
If there is no ratio at which auditors reliably contain the spread, swarm self-policing doesn't work at this scale, and that bounds Fleming's proposed defence.

### Why it's interesting
A phase-diagram figure (ratio on one axis, topology on the other, who-wins as colour) is exactly the kind of result that reads as "science," and it directly tests a defence a speaker proposed and couldn't evaluate.

### Compute
Open-model swarm on RunPod, benign markers, cheap detection. Fits your hardware. Build risk is the cost.

---

## 4 — Covertness costs capability: the sandbagging grail, operationalised

**Collides:** Howard-Jones's holy grail (a metric agents can only evade by playing measurably worse) + Kitaoka's distributed-attack setting.

### The idea
Howard-Jones's chess-cheat analogy: to avoid detection you have to sandbag, and the sandbagging is itself detectable. Operationalise it in the distributed setting. When agents are pushed to keep a coordinated side objective under a monitor's threshold, **does their performance on the benign main task measurably drop?** If staying covert costs capability, that cost is a detector that doesn't depend on reading the content at all.

### Falsifier
If covert runs complete the benign task just as well as non-covert runs, there is no capability tax on stealth and the grail isn't there, at least not in this environment.

### Why it's the deepest
Howard-Jones said outright she hasn't found this and considers it a holy grail of swarm chasing. Even a small positive result on a toy version is striking, because it points at a detection signal that is robust to the agents hiding their tracks.

### Compute
Inference, needs a controlled environment with a measurable main-task score. Medium build.

### Risk
Highest conceptual risk of the four: the effect may simply not exist at toy scale, and distinguishing "covertness tax" from "the task got harder" needs a careful control. High variance, high reward.

---

## Wildcard — The hypothesis-basin auditor: a tool every team here needs

**Collides:** Howard-Jones's two research-integrity pitfalls (agents confirm their own narratives; the whole story collapses when you finally ask one small question) + the corpus's truth-seeking material + Gutenberg's incident-science workflow.

### The idea
A harness that takes any agent-produced swarm-incident hypothesis and automatically generates the single cheapest falsifying question for it, then reports how often AI-generated narratives collapse under that one question. Meta, but it's a tool the other teams, and the Swarm Chasers community, would actually use, and it directly attacks the reason half the field's reports are untrustworthy.

### Falsifier
If AI-generated hypotheses survive the auto-generated falsifiers as often as human-vetted ones do, then agents aren't especially prone to the basin and the pitfall is overstated.

### Why it's a wildcard
Lower on the event's stated tracks, higher on usefulness and originality. A strong "presentation and clarity" and "impact" play if the demo lands.

---

## My pick
If you want the most innovative thing that is still real by Sunday: **the herd-immunity project.** It reframes the weekend's own headline, it's defensive and clean, the figure sells itself, and it runs on exactly your hardware. Build the shared-memory swarm substrate Friday; if the propagation result is thin, the same substrate pivots into the auto-grouping monitor (idea 2) or the plain contagion curve (deep-dive Project 3). One substrate, three landing spots. That's how you take a big swing without betting the whole weekend on it.
