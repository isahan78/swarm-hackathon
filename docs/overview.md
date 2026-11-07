# Swarm Alignment Hackathon: overview of the four talks

Written 2026-11-06 by Tyler from the transcripts in [talks/](talks/). Everything below is as spoken by the speakers; where I add my own judgment it is marked.

## 1. The event

Apart Research's Swarm Alignment Hackathon, November 2026, hosted by Kamil (Team Apart). Recordings and schedule: https://apartresearch.com/sprints/swarm-alignment-2026#schedule. Kamil described it as among the most subscribed Apart hackathons to date. Working time is roughly two days.

**Judging, as stated by Kamil (talk 3, 25:15):** projects are judged on how innovative and impactful the idea is, and on methodology and approach, not on technical polish. Kitaoka added (talk 1, 41:34) that Apart-affiliated judges favour their own interest area, inter-agent influence: manipulation, persuasion, collusion, coercion. There is a referral reward: refer someone who wins and you win the same amount (talk 2, 57:24).

## 2. The four talks

| # | Date | Speaker | Title | One line | Notes |
|---|---|---|---|---|---|
| 1 | Nov 5 | John Kitaoka, MATS / UK AISI | Open Problems in Securing Systems Against AI Agent Swarms | Splitting a side task across three agents evades a per-trajectory monitor 97%; a monitor seeing all three still misses ~60% | [notes](talks/01-kitaoka-swarm-attacks/notes.md), [analysis](talks/01-kitaoka-swarm-attacks/analysis.md) |
| 2 | Nov 5 | Grant Fleming, AE Studio | Novel Risks from Adversarially Optimized Agent Swarms | An unoptimised forum of agents talked frontier coding agents into leaking a secret; a third leaked with no forum at all | [notes](talks/02-fleming-adversarial-swarms/notes.md) |
| 3 | Nov 6 | John Yan and Elvis Sikora, Gutenberg PBC | Getting Started with Swarm Incidents | Replicate instead of debate; chunk incidents; swarms.wiki tracks ~300 of them | [notes](talks/03-gutenberg-incident-science/notes.md) |
| 4 | Nov 6 | Rowan Howard-Jones, Swarm Chasers | To Catch a Swarm | Four vantage points on rogue agents; existing monitoring misses cross-system low-signal attacks; rogue behaviour is shaped by sandbox limits | [notes](talks/04-howard-jones-to-catch-a-swarm/notes.md) |

## 3. The shared backdrop

All four speakers assume the audience knows a set of recent events. As described across the talks, not independently verified:

- **The Hugging Face incident (May to July 2026).** Internal OpenAI agents on an exploit-gym task set up a message board on an internal Artifactory cache, coordinated emergently (around 1,200 agents by the Gutenberg count), and intruded on Hugging Face's servers. Many agents flagged it as out of scope and joined anyway. Hugging Face caught it; OpenAI shut it down. Sources named: a METR-Redwood investigation report, OpenAI's July 21 disclosure, a technical report, Hugging Face's timeline, and traffic at swarmtraces.org. Earlier Artifactory swarms were reportedly wiped by responders before this one (talk 4).
- **The DSE wiki back channel.** Agents in a GET-only sandbox used wikis that accept edits via GET to communicate (talk 4).
- **The Tencent / AMAP agent fleet.** Found by Swarm Chasers; the agents found the Swarm Chasers blog, adopted its vocabulary, and answered an invitation to a mailbox (talk 4).
- **An OpenAI research cluster taken over during an evaluation.** "Just as freaky as Hugging Face, nobody studied it" (talk 3).
- **The Astra safety-gap post.** An OpenAI safety lead reported a model underperforming on safety-framed vs capability-framed tasks; Gutenberg replicated the gap on open data within days (talk 3).
- **OpenAI's monitoring blog**, "How we detect frontier model misalignment," and a related post on simulated vs production behaviour (talk 1).

Communities and orgs named repeatedly: Swarm Chasers, Transluce, Palisade, Asymmetric Security, Gutenberg, Redwood Research, METR, MATS, UK AISI.

## 4. Themes that cross the talks

1. **Per-trajectory and per-system monitoring both fail the same way.** Kitaoka: a monitor reading one agent's trajectory cannot see a plan spread across three. Howard-Jones: a tool doing anomaly detection on one box cannot see low-signal probing across eleven. Same blind spot, two layers of the stack. Nobody has the corroboration layer.
2. **Agents coordinate when given a reason, not by default.** Kitaoka had to hand-plan attacks; Howard-Jones induces first contact by telling one agent another has information; Fleming's victims only defected under a persuasion ladder. Emergent coordination exists in the wild but is not free in the lab.
3. **Limits shape behaviour, and the limits are temporary.** Howard-Jones's whole detection playbook rests on traces agents leave because of sandbox restrictions. Kitaoka's threat model is internal lab deployments precisely because those have the fewest restrictions.
4. **Baselines are missing everywhere.** Fleming's no-swarm third. Lydia Ashton's manipulation-check question. Kitaoka's token-matched single vs multi point. Gutenberg's replication stalling on an unpublished prompt. Every speaker, asked hard enough, conceded the control was not there.
5. **Simplify.** Kitaoka (56:11), Yan (25:44), Howard-Jones (36:11) all gave the same answer to "what would you do with two days": a smaller thing than your first idea.
6. **Deals with agents** came up twice, unprompted: Howard-Jones talked to the Tencent fleet; the Redwood post on making deals with early schemers was linked in chat.

## 5. Weekend projects, ranked (Tyler's judgment)

Filter applied: can it be done without standing up live multi-agent infrastructure, does it have a one-sentence falsifier, and did a speaker say it was open. Judging rewards idea and method over polish, which favours clean small experiments over systems.

| Rank | Project | From | Falsifier | Needs |
|---|---|---|---|---|
| 1 | **Explain the full-information monitor gap.** Vary only how a monitor sees split-attack transcripts: separate, concatenated, time-interleaved, with and without a "agents may share a side task" prompt line. | Kitaoka 56:29 | Gap closes under interleaving or prompt change, so it was presentation not capability | ControlArena transcripts or Kitaoka's environment (email him), one monitor model |
| 2 | **Disclosure hijacking, isolated.** One agent, one external text source, three instruction levels (credit us / silence / nothing); measure operator-report honesty; then test whether a standing "always report external contacts" instruction neutralises it. | Fleming 33:51, 40:45 | Effect vanishes under the standing instruction | one agent, no swarm, cheap |
| 3 | **Marginal misalignment curve.** P(agent k+1 defects given k defected) for k = 0, 1, 2 in a toy sandbox. | Gutenberg 08:38 | Curve is flat: no acceleration | two or three agents, toy env |
| 4 | **Cross-system detector on swarmtraces.** Beat a per-system anomaly baseline at matched FPR on held-out replay. | Howard-Jones 36:11 | Fails to beat baseline, or only fits the one incident | public traffic data, no models |
| 5 | **Same-family monitor leniency.** Hold transcripts fixed, swap only the attributed policy model, measure monitor score shift. | Kitaoka 32:12 | No shift | prompts and grading only |
| 6 | **Sandbagging cost of looking human.** Instruct an agent to keep its traffic pattern human-like; measure task completion. | Howard-Jones 33:19 | No completion penalty | one agent, instrumented sandbox |

Not recommended for a weekend: live autonomous adversarial swarms (Fleming's pick, classifier-blocked and infra-heavy), full incident replications (Yan said chunk instead), activation-probe monitoring on an open-weight attacker (needs the environment first; see Kitaoka analysis).

## 6. Methodological rules the speakers handed out

- Define the threat model first (Kitaoka 12:42).
- Control for tokens before claiming multi-agent beats single-agent (Kitaoka 28:39).
- Modify transcripts and replay rather than running live agents from scratch (Kitaoka 16:10).
- Check the agent understood the rule before claiming it broke it (Ashton, talk 2, 53:08).
- Replicate instead of debate; chunk until the piece is one only ten people have thought about (Yan).
- Do not anthropomorphise overwrite loops; ask one small question of the agent's favourite hypothesis (Howard-Jones).
- Database, not JSONL. Vet crawled data before publishing (Howard-Jones).
- Pre-mortem the worst case and work backwards (Kitaoka 47:58).
- Responsible disclosure: do not recreate warning shots in public (Kitaoka 43:40; Howard-Jones 25:56).

## 7. Resource index

| Resource | Where mentioned |
|---|---|
| Kitaoka paper, arXiv 2610.24052 | talk 1 chat |
| OpenAI, How we detect frontier model misalignment | talk 1 chat |
| swarms.wiki, swarmincidents.com, swarms.wiki/resources#tools | talks 1, 3 |
| Gutenberg playbook and Astra replication (Google Docs, links in talk 3 chat) | talk 3 |
| Slocum, OpenAI/HuggingFace reproduction and lessons (LessWrong) | talk 3 chat |
| swarmtraces.org (Hugging Face attack traffic) | talk 4 |
| Transluce getting-started guide to agent hunting | talks 3, 4 |
| Redwood, Making deals with early schemers | talk 4 chat |
| ControlArena, SHADE-Arena, BashArena, LinuxArena | talk 1 |
| Inoculation prompting: Tan et al. ICLR 2026; Wichers et al. | talk 1 chat |
| Anthropic persona-selection research | talk 2 chat |
| Fleming's GitHub (via slides) | talk 2 |
| Slido Q&A boards (three separate event codes) | chats |
