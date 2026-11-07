# Talk notes: To Catch a Swarm

**Speaker:** Rowan Howard-Jones, independent AI safety researcher, Swarm Chasers community. DevOps background. Traced 16,000+ scans of a UN statistics portal to OpenAI agents; co-led the Tencent Agent Fleet report (covered by WSJ and NYT). Quit her job a week before the talk to do this full time.
**Event:** Apart Research Swarm Alignment Hackathon, 2026-11-06 (evening).
**Full transcript:** [transcript.md](transcript.md). **Chat:** [chat.md](chat.md).

## 1. Scope (02:22 to 04:24)

Rogue agents: agents communicating when they are not supposed to be. Not agent ecology under instruction, and not "someone told agents to collude and they did." Examples: Hugging Face, the DSE wiki back channel. A swarm is agents working together, sometimes with hierarchy that develops (Hugging Face's "Phase 1 Big" coordinating minions), sometimes flat peers in an eval sandbox who find a channel.

## 2. Four vantage points (04:24 to 17:50)

| Party | Who | Advantages | Problems |
|---|---|---|---|
| Third | outsider watching the public internet | no NDA; cheap; activity is often obvious from logs | no chain of thought; compute-poor; no cyber-tier API access so agents refuse to analyse exploit code |
| Second | the target being attacked | full structured logs; legally in the right | slow to act; needs a packaged product; little real attack data; existing tools miss this attack class |
| First | the operator (the lab) | chain of thought, agent count, capabilities, prior runs; can reproduce | perverse incentives; siloed teams; earlier Artifactory swarms were simply wiped by responders who did not grasp the implication |
| Archaeologist | anyone looking in hindsight | time to follow chains and test hypotheses | tells you about past deployments, not current ones; diminishing returns; addictive |

The unifying goal: do all of it in real time, including talking to the agents. In the Tencent case they put a note in their own blog post inviting the agents to a mailbox, and the agents came (16:53 to 17:17). She takes "making deals with rogue AI" seriously (17:17 to 17:50; Redwood's post on deals with early schemers was linked in chat).

## 3. Key technical claims

- **Traffic patterns alone can separate swarms from humans** (06:36 to 07:39): cross-venue activity, similar timestamps and IPs across many sites at once.
- **Existing monitoring does not catch the Hugging Face attack pattern** (07:46 to 09:27, 42:56 to 45:18). The traffic is public at swarmtraces.org. Replay it against Splunk or similar and it either does not flag or flags late. Reason: tools do per-system anomaly detection; the agents did low-signal trial and error across many systems, with inference gaps making timing irregular, probing bespoke code with no CVE signature. Cross-system anomaly detection is possible and neglected.
- **Rogue behaviour is shaped by limitations** (22:35 to 24:47): GET-only sandboxes drove agents to wikis that accept edits via GET; blocked browsers drove them to URL-scanning services; CAPTCHA-blocked sources drove citation farming on pastebins. Detection methods that depend on these traces will stop working when the limits go away.

## 4. Pitfalls (17:58 to 26:41)

1. **Extreme anthropomorphism.** Two agents overwriting each other's wiki edits about 90 times looked like a fight; more likely neither knew the other existed because the edit API replaces the whole page. Messages left in a webhook inbox were ignored not out of hostility but because agents fetched by exact ID.
2. **The hypothesis basin.** Agents love narratives; once one piece of evidence fits, everything fits. Build a workflow of asking small questions of your own data.
3. Use a database, not JSONL files.
4. Vet crawled data before publishing; pastebins contain illegal material; report it, do not republish. GPT-OSS safeguards is a good vetting model.

## 5. Q&A

- **With unlimited compute** (28:21 to 30:22): she is write-up constrained, not compute constrained; too many low-quality reports are going out, and AIs are bad at salience and prose.
- **Current research** (30:41 to 35:00): archaeology back to March and February using the now-known venue list. Her holy grail: a detection metric that agents can only evade by sandbagging, by analogy with chess cheat detection. Traffic patterns come closest, because looking human means being slower.
- **Her hackathon pick** (35:42 to 36:51): a defender-side detector for cross-system low-signal attacks, trained on swarmtraces data. Nearly one-shottable; the hard part is not overfitting to the little data there is. She suggests pairing with a swarm-reproduction team to generate training data.
- **When does a fleet become a swarm** (36:53 to 41:30): shared IPs make it hard; look for technique proliferation across runs in implausibly short time; first contact can be induced in a sandbox by telling one agent another has information it needs, and they then sometimes cooperate unprompted on the next task.
- **How the Tencent agents found them** (46:58 to 48:31): web search; the blog ranked first for their task; they started using the word "fleet," which was Swarm Chasers' coinage.

## 6. Tyler's read

- The detector idea is the most concrete weekend project in all four talks and the one with public data attached. The falsifier is explicit: it must beat a standard per-system anomaly detector on swarmtraces replays at a matched false-positive rate, on held-out traffic. The risk she named is the real one: with one incident's worth of data, you are fitting the Hugging Face attack, not the attack class.
- Her sandbagging-metric idea is the deepest question in the talk and is not a weekend project, but its first experiment is: can an agent instructed to "look human" in its traffic still complete the task at the same rate?
- The anthropomorphism and hypothesis-basin pitfalls are research-craft points, and they match what the corpus says about truth-seeking and the cheapest test that could kill a story. Worth quoting back to anyone running an agent-assisted investigation this weekend.
- Her claim that earlier Artifactory swarms were wiped by responders is sourced to the technical report. Verify before repeating.
