# Talk notes: Getting Started with Swarm Incidents

**Speakers:** John Yan (helped train Claude 3 at Anthropic; founding Gutenberg PBC, which studies swarm incidents) and Elvis Sikora (maintains swarms.wiki and swarmincidents.com).
**Event:** Apart Research Swarm Alignment Hackathon, 2026-11-06. Short, conversational, 28 minutes including Q&A.
**Full transcript:** [transcript.md](transcript.md). **Chat:** [chat.md](chat.md).

## 1. Incident science (01:04 to 03:20)

Incidents are piling up and are evidence; the job is to extract the most from each warning shot. His motivating example: a few days earlier, an OpenAI safety lead posted that the "Astra" model underperforms on safety-framed tasks relative to capability-framed ones. Twitter spent, in his estimate, a thousand researcher-hours debating how scary it was. Gutenberg instead replicated it with the same methodology on the best open dataset, reproduced the gap, and published code and data (02:31 to 03:20). The principle: in the time it takes to argue, run the experiment.

## 2. swarms.wiki (04:02 to 05:45)

A project tracker, "GitHub for agent incidents." Two to three weeks old at the time of the talk; roughly 300 tracked incidents, each linked to tools, datasets, people, and ways to contribute, including a private channel for non-public information. Elvis is the maintainer and the contact. The playbook (05:45 to 06:33): form hypotheses, re-enact, chunk, test, iterate. A LessWrong post or white paper is coming.

Incidents mentioned: Hugging Face breach; a German wiki used as a back channel; an OpenAI research cluster taken over during an evaluation (07:05, "just as freaky as Hugging Face, nobody studied it"); the Tencent fleet.

## 3. Their own research agenda (08:19 to 09:21)

**Memetic misalignment:** going from zero to one misaligned agent is one problem; going from one to two, two to three, is another. Does the marginal misaligned agent get cheaper? The Hugging Face numbers (1,200 agents) suggest acceleration. Their hypothesis is that it does, and they are testing n = 1 to 2, then 2 to 3, not 1 to 1,200.

## 4. Q&A

- **Discovering incidents** (09:21 to 13:26): automated ingestion of news and reports; for rogue agents in the wild, they defer to Palisade, Swarm Chasers, Transluce, and Asymmetric Security. Transluce's "getting started with agent hunting" guide is the best written one. A caveat from those groups: expect fewer rogue-agent sightings going forward because labs are moving to offline evals, while intentional misuse is rising.
- **Labs withhold details** (13:26 to 17:27): the theory of change is that public replication makes the benefit of disclosure measurable. Their Astra replication stalled at the second experiment because the prompts were never published; saying so in public is a lever. The adversarial side, catching a lab's timeline contradicting its safeguards claim, has not happened yet but could.
- **After reproduction** (17:37 to 18:53): ask what caused it, could it have been worse with the next model, and how to mitigate. Reproduced incidents are the playing field for those questions.
- **Replicating something as big as Hugging Face** (18:53 to 21:04): don't. Re-enact, chunk. Stuart Slocum's LessWrong post splits it into four stages: writes to the shared registry, requesting help from other agents, sharing exploits, and the intrusion itself. Each can be chunked further.
- **Insufficient data** (21:10 to 22:52): toy environments are fine; two agents is already rich.
- **Two days** (23:15 to 25:28): incident discovery via Transluce's guide, or pick one chunk of one incident. Kamil: judging is on innovation, impact, methodology and approach, not technical polish.
- **Hindsight** (25:28 to 27:30): simplify. Each step of a big replication is hard on its own, and once you pare down to one component you find only ten people have thought seriously about it.

## 5. Links (from chat)

- Incident debate thread: https://x.com/Marcus_J_W/status/2118093146483810386/quotes
- Gutenberg replication of the Astra result: https://docs.google.com/document/d/1pYyJAGPE-muTiXRX_QCuT1GXwyrPN-vpJzwVnxSeGVE/edit
- swarms.wiki and https://swarms.wiki/resources#tools
- Playbook: https://docs.google.com/document/d/1oR1YQbLEbS-emeWRS8nLx91pYrgQSwU7OrRTGxiN8pg/edit
- Chunking the Hugging Face incident (Slocum): https://www.lesswrong.com/posts/fMnC6ZD37qrnZAFYz/openai-huggingface-a-reproduction-and-lessons-for-alignment

## 6. Tyler's read

- This is the methodological talk of the four. Its two rules, replicate instead of debate and chunk until ten people have thought about the piece, are the hackathon's best triage filter.
- The memetic-misalignment question is a real question with a clean falsifier: measure P(agent k+1 defects | k defected) for k = 0, 1, 2 in a toy environment. If the curve is flat, the acceleration story about Hugging Face is wrong. That is a weekend experiment with two or three agents.
- Their Astra replication is a warning about reading talks: "reproduced the gap" with "everything else the same" on a different dataset is a weaker claim than it sounds. Read the doc before citing it.
- Nothing here needs the corpus. It is control and incident work, outside mech interp.
