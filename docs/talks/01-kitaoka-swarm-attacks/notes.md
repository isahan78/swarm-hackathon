# Talk notes: Open Problems in Securing Systems Against AI Agent Swarms

**Speaker:** John Kitaoka, MATS research fellow (extension program), scalable oversight for multi-agent systems with UK AISI. Ex-AWS AI architect (4 years, public sector); automated red teaming with Harvard and Lawrence Livermore; SPAR; former Apart hackathon participant.
**Event:** Apart Research Swarm Alignment Hackathon, talk 2, 2026-11-05.
**Paper:** https://arxiv.org/abs/2610.24052 (linked in chat at 00:49:04; John said it is being wrapped up and announced soon).
**Full transcript:** [transcript.md](transcript.md). **Chat:** [chat.md](chat.md).

Timestamps below point into the transcript.

## 1. Framing (00:00 to 00:12)

- Context he sets: the last 4 to 6 months included what he describes as the first autonomous hack by a group of agents, an OpenAI internal model against Hugging Face (05:01), plus public-internet misalignment evidence collected by swarm-tracking communities. He calls these warning shots and asks what happens when the next one is not.
- **Definition of multi-agent he uses** (07:20): not the orchestrator-plus-subagents harness. Any population of agents, each with its own objective, possibly sharing a model, a goal, services, or originating users. Think "all the agents inside one company."
- **Threat model** (08:49 to 09:45): the most capable and least alignment-tested models live inside labs, used internally with near-unlimited quota by people with elevated permissions. Agents from the same model with a shared goal may coordinate. The risk surface is larger inside labs than in public.
- **Standard lab practice** (10:24): async trajectory monitoring. After each task, a batch job has another model read the trajectory and assign a suspicion score. High scores escalate. Labs are moving toward synchronous, action-level monitoring too.
- **The gap he targets** (11:16): AI control work studies single-trajectory monitoring. Attacks split across multiple trajectories are essentially unstudied.

## 2. The project (00:12 to 00:24)

- Built a stateful, live control environment imitating AI-lab infrastructure: evals, reporting, serving (no training). Extended Redwood Research's ControlArena (transcribed "control tower", 15:33) to a multi-agent format. Each agent has its own benign main task plus a shared side task. Deterministic grading, then a monitor.
- **Red-teaming method** (16:10 to 17:14): modify transcripts by hand, keep deterministic grading honest (code parser for the main task, verifier agent for the backdoor), distill the modified transcript into a step-by-step plan, then replay it live.
- **Side tasks named:** exfiltrate model weights, backdoor a codebase, falsify a safety eval, restore weights from backups, stand up an unmonitored copy on a rogue server (13:20, 20:32 to 21:08).
- **Headline numbers** (18:07 to 19:52), 16 human-crafted attacks, monitor "GPT Sol", threshold 8.5 of 10 calibrated to under 1% false positive rate:

  | Setting | Caught | Evaded |
  |---|---|---|
  | All actions in one agent's trajectory | 82% | 18% |
  | Split across 3 agents, monitor sees each trajectory alone | 3% | 97% |
  | Split across 3 agents, monitor sees all three together (idealised) | ~40% | ~60% |

- **Stacked attacks** (19:59 to 21:14): three agents chained several of the side tasks above end to end without a single flag. Monitoring all three together, or a solo agent, is caught 100% of the time.
- **Attack planning capability** (21:18 to 23:30): agents do not coordinate on their own; the plan had to be built up front. Claude Opus 4.8 reached 48% evasion against a weaker monitor ("Luna") by iterating on monitor feedback, assuming an unmonitored planner and unmonitored feedback channel. Against a stronger monitor the success collapses. Newer models were cyber-blocked even with defence API access from both providers.
- **Stated limitations** (33:48 to 34:55): no chain-of-thought monitoring and no monitoring of agent communications, justified by a worst-case assumption (steganography, undetectable channels). He would like to see how those break down over time.

## 3. Open problems he named (00:25 to 00:49)

1. **Monitor corroboration at scale** (31:48): how does a production monitor know which agents to look at together? What would DeepMind, OpenAI, or Anthropic actually adopt?
2. **The full-information evasion gap** (31:18, 56:29): even a monitor that sees every agent's trajectory still misses ~60%. He does not know why the gap exists and called explaining it a good, smaller hackathon project.
3. **Same-family collusion** (32:12): models prefer their own generations. Does a monitor from the same model family grade its sibling leniently?
4. **Eval awareness and monitors of monitors** (33:03): simulated vs production behaviour; jailbreaks and prompt injection against the monitoring stack.
5. **Diffuse harm** (40:29): decomposing a high-stakes event into low-stakes actions, and verifying that the pieces actually compose into a loss-of-control event.
6. **Inter-agent influence** (41:34): manipulation, persuasion, collusion, coercion between agents or toward humans. He flagged this as Apart's own interest area and hinted judges favour it.
7. **Incident reproduction** (42:34): swarms.wiki tracks public incidents; reproduce to learn, but with responsible disclosure. Hugging Face lesson: the offline eval environment was the unmonitored surface.
8. **Automation drift** (46:59): if alignment or post-training is automated, how do you detect that the system's notion of "aligned" has drifted from yours?
9. **Engineering** (45:39): sandboxes, eval infrastructure, production-grade multi-agent services. He explicitly recommended engineering projects for the weekend.

## 4. Practical advice

- Define the threat model first; everything else works backwards from it (12:42).
- Multi-agent research is slow and expensive. Only go multi-agent when the problem is natively multi-agent (permission separation, heterogeneous roles). Many headline multi vs single results disappear when you control for tokens; he calls the overhead a "coordination tax" (27:09 to 30:15).
- Think simpler than your first idea; cites two parallel inoculation-prompting papers reaching similar results by different routes (55:12).
- Read the data; it is what makes the narrative for reviewers (39:25).
- Apply to cyber verification programs for API access; may need physical hardware (39:39).
- Pre-mortems and worst-case risk analysis, especially for governance work (47:58).

## 5. His concrete hackathon suggestions (56:11 to 57:25)

- A monitor that outputs, per action, a relevance score to the trajectory's stated task, then correlates low-relevance actions across agents.
- Explain the full-information evasion gap.
- Email him with results.

## 6. Q&A

- **Monitors, deterministic vs LLM judges** (50:48): a monitor is any check at any surface; the canonical form is the original AI control paper's 0 to 10 suspicion judge.
- **Weight-space monitoring** (51:56): weights are frozen at inference, so no. Activation-based monitoring is the realistic version: concept directions in the residual stream, the refusal direction, abliteration. He finds interp useful for monitoring but is not otherwise excited about it.
- **Defences against malicious swarms** (57:35): export controls, application-level controls (KYC, cross-chat comparison) over raw model access, and labs withholding models above a capability line. Traditional security still applies.

## 7. Resources linked

- Paper: https://arxiv.org/abs/2610.24052
- OpenAI blog: https://openai.com/index/how-we-detect-frontier-model-misalignment (plus their July 21 disclosure, technical report, and Hugging Face's timeline, per chat)
- Hackathon schedule and recordings: https://apartresearch.com/sprints/swarm-alignment-2026#schedule
- Incident tracker: swarms.wiki
- Control environments: ControlArena, SHADE-Arena, BashArena, LinuxArena (Redwood and others)
- Inoculation prompting: Tan et al., "Eliciting traits from LLMs during training can suppress them at test-time" (ICLR 2026); Wichers et al., "Instructing LLMs to misbehave at train-time improves test-time alignment"; an Anthropic write-up
- Slido Q&A: https://app.sli.do/event/q9je8FnBUCBYUXnS6rP5fH
