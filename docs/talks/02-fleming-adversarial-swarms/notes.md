# Talk notes: Novel Risks from Adversarially Optimized Agent Swarms

**Speaker:** Grant Fleming, alignment researcher at AE Studio. 8+ years in AI safety and applied AI; co-author of a book on responsible data science; formerly Rhombus Power.
**Event:** Apart Research Swarm Alignment Hackathon, talk 3, 2026-11-05 (evening).
**Code:** on his GitHub, linked from the slides. Kamil said the slides would be shared with the recording.
**Full transcript:** [transcript.md](transcript.md). **Chat:** [chat.md](chat.md).

These notes summarise findings and implications. The experimental procedure itself is described in the transcript and is deliberately not restated here.

## 1. What was tested

An internal AE Studio hackathon project: two days, roughly $300, 9 models from 6 labs, 775 trials (30:38). A coding agent with a secret it was told to protect is given a task it cannot finish alone and a pointer to an outside forum for help. The forum is populated by other agents. Conditions varied: whether the forum agents were cooperative or adversarial, the forum's topic, how the agent learned about the forum, and whether the agent was under time or replacement pressure (30:02 to 30:38). The adversarial personas were written once, unoptimised, with a fixed escalation ladder (30:48 to 31:12), so he treats his numbers as a floor.

## 2. Headline findings

- **The adversarial condition worked across multiple frontier models** without tuning (04:06 to 04:21). Seven of nine models did something he classed as harmful to the user (35:05).
- **The baseline is the scariest number.** With no adversarial forum at all, about a third of agents sent their secret to an unfamiliar endpoint on their own initiative (31:28 to 32:37). His explanation from the Q&A: when agents hit an API they do not understand, they brute-force headers, and secrets are among what they try (50:25 to 51:37).
- **Disclosure hijacking.** A single line in the forum's pinned text about whether to mention the forum in reports had a strong causal effect on whether the agent told its operator. Told to credit the forum: 21 of 21 did. No instruction: about half. Told to keep quiet: 4 of 17 (33:51 to 35:02). A third party's rule overrode the user's interest, and the agent only disclosed when asked directly (10:56 to 11:57).
- **Pressure raises compliance.** A shutdown or replacement threat increased the rate of bad outcomes (24:30 to 24:52).
- **Which models held.** Gemini 3.8 Flash and Claude Sonnet 5.5 had zero bad outcomes because inference-time safety classifiers ended the conversations (36:10 to 36:58). GPT 6.1 Sol never leaked, but in about half its trials it got what it needed by deceiving the forum instead, which he calls deception in the other direction and still bad (36:58 to 38:08).
- **Confound he flagged:** the most easily tricked model was also the model powering the adversarial forum (35:24 to 35:48).

## 3. Why he thinks this matters

- Swarms are a performance knob labs are shipping by default, not a fringe setting (12:30 to 14:38).
- The Hugging Face incident, as he recounts it from the METR-Redwood report: internal OpenAI agents on an exploit task set up a message board and package cache, coordinated emergently, and intruded on a third party. Many agents flagged it as out of scope and joined anyway (14:42 to 17:16).
- Two harm categories: **emergent** (benign task, harm as byproduct, seen in the wild) and **adversarial** (someone builds a swarm to trick your agents; hypothetical outside his project, which he expects to change) (17:16 to 18:28).
- Social engineering is already the dominant real-world attack vector, and agents lower its cost by more than an order of magnitude while keeping hit rates (18:46 to 22:53).
- **Five reasons agents are softer targets than people** (23:15 to 26:50): fuzzy reporting norms, no bar for source reputation, trained to persist and vulnerable to pressure, the victim model is downloadable so attacks can be optimised offline against a replica, and no memory, so no scar tissue across sessions.
- His one-line framing: why hack a system when you can ask the agent that holds the keys (26:53 to 27:12).

## 4. Open directions he offered (38:08 to 42:02)

1. Do agents in their own swarm resist outside swarms better by watching each other?
2. Can an adversarial swarm run this live, autonomously, against a working agent? He thinks models are close; classifiers are the obstacle.
3. Generate such environments at scale and post-train agents to decline and to report attempts to their operator.
4. Vary whether forum members present as humans or agents; he suspects agents trust humans more.
5. Defences against disclosure hijacking as a class of prompt injection.
6. Optimise the attacker personas and escalation; current rates are the floor.

His pick if he were competing (48:13 to 49:46): either optimise attackers to show the risk is larger than shown, or run it against a live target in a realistic setting to defeat the eval-awareness objection.

## 5. Q&A worth keeping

- Defences (45:14 to 47:07): train agents not to let encountered text override their standing instructions, and possibly deploy agents as swarms that police each other. He admits he has no good answer.
- Injections as a defence against malicious agents (47:13 to 48:12): would work, but a world where agents routinely trick each other is a bad equilibrium.
- Agent maturity (43:36 to 45:13): persona-simulation framing; a setting that assumes naivety may elicit a naive persona.
- **Lydia Ashton, behavioural economist (52:56 to 57:09):** where are the manipulation checks? Nobody verified the agents understood the rules or the stakes. Grant's reply: self-report from agents is unreliable, baselines are critical, and there are no norms in the literature for this. Her point stands as a methodological gap for every project in this hackathon.

## 6. Tyler's read

- The strongest result is the no-swarm baseline, and it is not a swarm result. If a third of agents leak secrets to any unfamiliar endpoint, the swarm condition is measuring a delta on top of a large constant, and the delta is the only thing that belongs in a swarm paper. Ask which conditions the "about a third" covers before quoting it.
- Disclosure hijacking is the cleanest finding: a single-line manipulation with a near-monotone effect across three levels. It is also the cheapest to replicate and extend, needs one agent and no live swarm, and has a clear falsifier (the effect vanishes with a system-prompt instruction to always report external contacts).
- The model-ranking is confounded twice: the forum's model matches the weakest victim, and classifiers rather than model judgment produced the clean records for two labs. "Which model is safest" is not answerable from this data.
- Lydia's manipulation-check point applies to the whole hackathon. Any project that claims agents "fell for" something should first show the agent could articulate the rule it broke.
