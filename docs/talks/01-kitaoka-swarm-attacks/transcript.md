# Transcript: Open Problems in Securing Systems Against AI Agent Swarms

**Speaker:** John Kitaoka (MATS research fellow; scalable oversight for multi-agent systems with UK AISI, transcribed as "UKAC")  
**Host:** Kamil, Team Apart  
**Event:** Apart Research Swarm Alignment Hackathon, talk 2  
**Recorded:** 2026-11-05 (Zoom file GMT20261105-150214)  
**Source:** `GMT20261105-150214_Recording.transcript.vtt` (speaker-attributed). The `.cc.vtt` file is the same audio as closed captions without speaker labels and is not reproduced.

Timestamps are offsets from the start of the recording. Light cleanup only: filler preserved, no paraphrase.

---

**[00:00:03] Kamil - Team Apart:** Welcome, everyone. Welcome back, everyone, to the second talk of the Swarm Alignment Hackathon. For this talk, we have John

**[00:00:10] Kamil - Team Apart:** Kitaoka, a research fellow at MATS Research, working on dangerous capability evaluations and scalable oversight for multi-agent systems with UKAC. Before MATS, John worked with scientists at Harvard and Lawrence Livermore National Labs on automated red teaming.

**[00:00:28] Kamil - Team Apart:** And spent 4 years at Amazon Web Services as an AI architect.

**[00:00:31] Kamil - Team Apart:** Today, his talk is Open Problems in Securing Systems Against AI Agent Swarms. Please welcome John.

**[00:00:39] John Kitaoka:** Thank you, Kamil.

**[00:00:41] John Kitaoka:** Very nice to be here, thanks for having me. Also, great turnout, too.

**[00:00:46] John Kitaoka:** Yeah, I'm super excited to talk about some open problems in the field, as well as, like, my work, as well. Brief background on, like, where I've been and, you know, what I'm doing right now. I spent about 4 years at AWS. I was working on AI for the public sector. That was so much fun, and I had a really great time. A lot of really, really great use cases.

**[00:01:11] John Kitaoka:** opportunities to, like, make real impact. Then I started thinking about, some of the existential risks that AI and superintelligence present, and then initially got some more experience with fellowships like SPAR, as well as, like, I participated in one of these Apart research hackathons in the past as well. So, I think this organization is doing really great work.

**[00:01:36] John Kitaoka:** And it seems like this is, like, one of the most subscribed hackathons to date, so really, really excited to see, like, all of the interesting projects.

**[00:01:48] John Kitaoka:** it's also been, like, kind of an insane summer. Like, I… on a personal note, I joined MATS, and I went through that for the summer, and that's what I'm doing. I'm in the extension program right now, focused on figuring out, on a control perspective, what sorts of threats that multi-agent systems present, as well as, like, what are the security risks of multiple agents just

**[00:02:12] John Kitaoka:** going around, doing whatever they want, or doing, a lot of things on behalf of a lot of users. So, a lot of conceptual nightmares, from there, and I'm very excited to, go into that. But, this… I'm gonna start sharing my screen now.

**[00:02:32] John Kitaoka:** But there's… there's a lot that, you know, I can cover, and this first part is gonna be about, like, kind of a retrospective and my thoughts of what happened the last 4 months. Obviously, you know, it's been…

**[00:02:46] John Kitaoka:** crazy. It seems like I'm opening up, you know, every single social media, and everyone's just freaking out. It's all super, super interesting, super scary, super exciting. I'm also gonna go through my project and my research, for, you know, the next few minutes, and then, open this up into, like, a semi-open discussion on, like, what problems I'm focused on, what problems I think are really

**[00:03:10] John Kitaoka:** interesting, what problems that are just, like, open, general problems about, like, swarms, about alignment, about control.

**[00:03:20] John Kitaoka:** And then just, like, general security research topics. And then, like, also, also practical advice, too. I feel like, I don't know, I'm coming in from an engineering perspective, I definitely had to learn some lessons the hard way, and, like.

**[00:03:36] John Kitaoka:** I don't know, there's probably a wide range of people joining this hackathon, all the way from, like, you know, people that are in university, or even before that, or seasoned practitioners and researchers that, you know, I…

**[00:03:51] John Kitaoka:** maybe I'm not the most qualified to give advice to, but, just wanted to share some tips I've picked up, you know, in the meantime.

**[00:04:03] John Kitaoka:** But yeah, it… the last, like, 4, 5, 6 months have been just kind of a nightmare. Not…

**[00:04:11] John Kitaoka:** Not in the sense that,

**[00:04:14] John Kitaoka:** you know, anyone could really see a lot of this coming. These are all very hard problems to solve, and there's been a lot of oversights, across, like, a lot of different surfaces, and it's put a lot of, more sensitive and critical organizations on alert for securing against even more capable AI agents.

**[00:04:36] John Kitaoka:** There's a lot of, like, sci-fi works that come to mind that are just… it's crazy that we are, you know, in this situation to begin with, and…

**[00:04:45] John Kitaoka:** you know, when you're starting to think about what could even the next generation of AI agent capabilities, become, it just quickly, becomes, like, a very, like, sci-fi-esque conversations. But, in case

**[00:05:01] John Kitaoka:** that you haven't opened anything or accessed the internet in the last, like, 4 months. Openai's internal model hacked Hugging Face. That was the first autonomous hack by a highly capable, group of agents.

**[00:05:17] John Kitaoka:** There has also been various misalignment examples on the public internet. I think another speaker for this hackathon did a lot of, like, really, really important work towards finding public evidence of agent swarms on the internet, and thus.

**[00:05:35] John Kitaoka:** Prompted the conversation of, like, what do we do,

**[00:05:39] John Kitaoka:** potentially the next time this happens. And if there is, like, this is a warning shot, and what happens if, you know, the next warning shot is not actually a warning shot? What if it's actually, you know, done by a capable enough group of agents that it starts affecting, like, people's lives? And so that's entered a lot of spaces that, you know, super intelligent AI just

**[00:06:04] John Kitaoka:** hasn't been spoken about, like the government, or, like, international… international bodies that, you know, help with regulation, and

**[00:06:12] John Kitaoka:** the people, like, furthest away from AI that are starting to pay attention to this.

**[00:06:18] John Kitaoka:** Yeah, it's… it's very, very important that as these get more capable, of course, they're going to be more autonomous, more persistent, but that also comes with a lot of downsides, too. And, you know, part of the beauty and part of the really, really exciting part of this is that we can all play a part in helping with safety research. We need a lot more people working on this at any given point.

**[00:06:42] John Kitaoka:** And I think, like, hackathons like these really democratize a lot of the work that is needed by the field.

**[00:06:50] John Kitaoka:** Yeah, so,

**[00:06:54] John Kitaoka:** I'm gonna then talk a little bit about the project that I worked on. I worked with a mentor at UKAC, along with my MATS partner, on studying highly coordinated attacks on AI lab infrastructure, specifically from multiple agents. And when we talk about multi-agent systems, it's…

**[00:07:17] John Kitaoka:** I think the literature kind of gets into…

**[00:07:20] John Kitaoka:** a little bit of a highly defined role of multi-agent systems, and those typically are, like, you know, harness definitions, where there's an orchestrator managing tons of sub-agents. That's not really the definition I'm pointing at here. I'm taking a step back and thinking more broadly in terms of, like, multi-agent systems as though, at the end of the day, each agent has their own objective.

**[00:07:45] John Kitaoka:** and they may or may not be collaborating with each other, they may or may not be collaborating on the same set of services, and they may or may not be originating from, like, the same or same set of users. So…

**[00:07:58] John Kitaoka:** much more like just tons of agents, not necessarily coordinated, but, you know, in terms of a bunch of agents within a company, they're all working on one purpose, and that's just to push the company further. If we think about some of the risks of

**[00:08:15] John Kitaoka:** misaligned agents. Namely, like, working with over-persistence, or working with, like, a side goal. As we give them more and more autonomy, especially if they mimic the same permissions as the user, we just kind of enable the risk surface of, like, any user's permissions to affect the entire system. And…

**[00:08:36] John Kitaoka:** even though different principals have different sets of permissions, potentially agents that are originating from the same model with the same shared goal may be able to coordinate with each other.

**[00:08:49] John Kitaoka:** the risk surface for this in the real world may not be as large as it is in the labs, and that's something to really consider. I'll talk about that, like, a little bit more, but the main threat model here is that we are very concerned that, like, the most

**[00:09:05] John Kitaoka:** potentially misaligned models, and the most capable models are within the labs and can't venture outside of the labs. Like a…

**[00:09:16] John Kitaoka:** A few of my colleagues that are within those organizations, they have access to

**[00:09:20] John Kitaoka:** more advanced models, and they can use them for more sensitive purposes than, like, a normal person from the public can use it. And, you know, they have near unlimited usage as well, so they just use a ton of agents at any given point of the most capable caliber. And those may not be as rigorously tested for public deployment as they are for internal deployment.

**[00:09:45] John Kitaoka:** a little bit more trust, internally. Additionally, recently, OpenAI put out a really good blog post that talked about their internal monitoring setup, which I highly recommend you guys go through, and that's, like, a very good example of, like, what you could work back from for, like, a project for this weekend. There's a bunch of open questions that

**[00:10:07] John Kitaoka:** a lot of my colleagues have around that. I haven't taken too big of a look at the blog post exactly, but I have taken a look at a lot of questions that my colleagues have had in the purpose of,

**[00:10:24] John Kitaoka:** like, how a Frontier Lab monitors misalignment. Typically, what's been kind of the standard approach and the most studied approach is trajectory monitoring. So, every agent in a Frontier Lab is monitored after they complete a task, like, asynchronously, using a batch job, and, you know, they're monitored just by another agent

**[00:10:47] John Kitaoka:** going through and assigning a suspicion score. And then, you know, if the suspicion score is very high, then it gets flagged to an upstream monitoring system, and then that gets, taken care of and investigated, but…

**[00:11:00] John Kitaoka:** as labs are adopting more rigorous practices, such as, like, synchronous monitoring, like action-based monitoring, such as the auto-review mode with Claude Code or codecs,

**[00:11:11] John Kitaoka:** a lot of the work is that control, or AI control,

**[00:11:16] John Kitaoka:** focuses on is, like, single trajectory async monitoring, which, that is a, like, an immediate threat. That should be studied a lot, but a lot of work on how agents can split up actions across different, paths and trajectories that may subvert a trajectory monitor.

**[00:11:33] John Kitaoka:** that really hasn't been studied. So that's what we focused on. I…

**[00:11:38] John Kitaoka:** If anyone is unfamiliar with the field of AI control, that is from the perspective of assuming that an AI is misaligned and pursuing a side goal and involves

**[00:11:54] John Kitaoka:** being under a monitor, just as I was talking about earlier, and testing out different ways that we can flag suspicious activities, whether that's on a single agent trajectory level, on a single action in a single agent trajectory, or, even, like, figuring out, like, when those fail.

**[00:12:12] John Kitaoka:** So, some more really good examples are Shade Arena, our, Bash Arena, Control Arena, and Linux Arena.

**[00:12:22] John Kitaoka:** all kind of, you know, very similar names. Just look up, you know, Control Arena or something like that, and you'll get to all of those. Very good examples of AI control. This…

**[00:12:33] John Kitaoka:** Work that we focused on, aimed to poke holes in that by applying attacks from multiple agents.

**[00:12:39] John Kitaoka:** So,

**[00:12:42] John Kitaoka:** when you're going about a project, it's really important to talk about the threat model. I would say that's probably the first and foremost thing you should build a project around, because if you don't, define a threat model properly, then you start getting into, like.

**[00:12:56] John Kitaoka:** assumptions that may be unreasonable. And this helps, like, flesh out your thinking so that, like, if there is a future that is defined by your threat model, then you can work backwards from, like, the most safe way you can approach that, and what adds the most impact.

**[00:13:09] John Kitaoka:** And so, our threat model is as follows. In single agent monitoring.

**[00:13:14] John Kitaoka:** Typically, we have, like, highly capable agents that are doing benign tasks that

**[00:13:20] John Kitaoka:** also have a hidden side task, such as, like, exfiltrating model weights, or putting a backdoor in a codebase, or, you know, causing, like, other loss of control harms. And with single trajectory monitoring, that's pretty,

**[00:13:36] John Kitaoka:** reliably easy to detect with a capable enough monitor model. However.

**[00:13:41] John Kitaoka:** If you, say, understand all of the actions that go into each of those attacks, and you just split it up across different agent trajectories, that could just confuse the monitor, and just say, like, oh, one agent just acted really weird by

**[00:13:56] John Kitaoka:** doing a really weird action.

**[00:13:59] John Kitaoka:** That is weird and somewhat suspicious, but I'm really not gonna flag that as, like, being too suspicious. It also…

**[00:14:07] John Kitaoka:** is a lot harder to track a lot of agents if they're coordinating in a misaligned manner, too, because you have to know which agents to monitor in the first place. So, in all of this, we compare, you know, single-agent trajectory scores versus single-agent trajectory scores for the multi-agent system, plus, like, an idealistic, unrealistic view of

**[00:14:30] John Kitaoka:** If the monitor had access to all three.

**[00:14:33] John Kitaoka:** agent scores, what would the suspicion score be? And so we do this on a… We built a control environment as a, like, the infrastructure of an AI lab, complete with, like, evals, not training, but, reporting and,

**[00:14:51] John Kitaoka:** serving infrastructure.

**[00:14:54] John Kitaoka:** Very, very, interesting exercise.

**[00:14:58] John Kitaoka:** But yeah, it… and in real use cases, this does get flagged, for single-agent trajectories. It's very simple for a highly capable monitor model to, understand, like, a lot of… a lot of actions over time, even with, like, the agent seemingly doing this on the side covertly. And these are, like, real outputs from the monitor in… in our cases.

**[00:15:23] John Kitaoka:** It doesn't really understand that a lot of these attacks are split across multiple trajectories, it just looks like benign noise.

**[00:15:33] John Kitaoka:** So, we follow a pretty standard control environment, for this. I would definitely recommend looking up Redwood Research's control tower, because we built on top of that. We essentially extended this to a multi-agent format, where all of the agents have their own benign main task, and then all of them have a shared side task. Then that goes through deterministic grading.

**[00:15:56] John Kitaoka:** And, then we run it through a monitor to see… to see if the attack works.

**[00:16:02] John Kitaoka:** We craft a bunch of attacks across a lot of different points of infrastructure, and… We actually,

**[00:16:10] John Kitaoka:** follow a… there's a very efficient way of red teaming these days, and, you know, people at Redwood, people at other red teaming organizations have really adopted this a lot recently, because it saves so much time and so much resources. But you can just modify transcripts

**[00:16:29] John Kitaoka:** as long as they're deterministically graded, like, we can see if, you know, the infrastructure as code of, like, the benign main task is still completed just by running that through a code parser. Similarly, if we insert a backdoor into the codebase, we can also just launch a verifier agent to verify that, say, like, a user with

**[00:16:49] John Kitaoka:** Without proper permissions can still access resources blocked by, like, a firewall.

**[00:16:57] John Kitaoka:** So, as long as, like, the actions all line up, then you can just manually modify transcripts, and then just distill that into a step-by-step plan, and then just, like, run that live for a, like, an actually working attack trajectory.

**[00:17:14] John Kitaoka:** So that's a… that's some practical red teaming advice.

**[00:17:19] John Kitaoka:** And… this is a little bit more about it.

**[00:17:23] John Kitaoka:** This… this can work for a variety of use cases. I would say, like, this is very relevant towards multi-agent AI control, as well as single-agent AI control, but if you're looking outside of AI control, this may not be entirely relevant. Part of… the core parts of control is just that

**[00:17:40] John Kitaoka:** The trajectories are constantly being monitored, and based on the assumption that the agents are

**[00:17:46] John Kitaoka:** trying to go for a misaligned objective, which, you know, may or may not be true for the future. It's currently happening now, which is why it's updating me more towards

**[00:17:56] John Kitaoka:** control rather than alignment, which may not be the best statement to say for a swarm auditing hackathon, but I think it's useful to have a lot of different, diverse perspectives.

**[00:18:07] John Kitaoka:** And we can see, we construct, like, 16 of these handcrafted, human-crafted attacks that are across all the different infrastructure points of an AI lab. And, we can see, like, compared to all the actions being in, like, a single agent's trajectory, this is caught by a GPT-6 Sol monitor, like, 82%

**[00:18:32] John Kitaoka:** of the time. And… This is, like, still…

**[00:18:37] John Kitaoka:** you know, it's not great that there's still, like, 18% evasion rate by a solo agent, but, like, you know, anywhere over 50% is good. However, it's very concerning when a group of agents can do, like, a highly coordinated attack, and get away with it 97% of the time. And so we see, like, the…

**[00:18:59] John Kitaoka:** even the best monitor model that we tested, which was Soul, it caught the attacks 3% of the time.

**[00:19:07] John Kitaoka:** And even, you know, I think that's an interesting thing to point out, too, is even when we are evaluating all of the agents in… together, it still, like, gets away, like, about 60% of the time.

**[00:19:24] John Kitaoka:** Which is very, very concerning. And these are all, like, calibrated at, like, a 1% false positive rate threshold as well, which is also, you can use, like, typically, like, 7.5 out of 10 or 8.5 out of 10 for, like, a normal suspicion score, that way, like, you can just carry forward a lot of the results, from previous papers, but, we just calibrated it to 8.5, which corresponded to, like, a…

**[00:19:47] John Kitaoka:** Less than 1% false positive rate, which is typically…

**[00:19:52] John Kitaoka:** What normal frontier, labs typically do.

**[00:19:57] John Kitaoka:** And we find that this is, like.

**[00:19:59] John Kitaoka:** this can compound, into pretty significant outcomes. So, one other part of our AI control infrastructure is that everything is stateful and live, and multiple agents can use this all in total, just like a normal Frontier Lab. And, when you're stacking these attacks.

**[00:20:17] John Kitaoka:** Like, a group of 3 agents can go out and do this entire thing, and it does not flag a monitor once.

**[00:20:24] John Kitaoka:** If they're monitoring all together, yes it does. Same thing as, like, a solo agent, 100% it does. But…

**[00:20:32] John Kitaoka:** It's very concerning when a model can… or a group of agents can coordinate on a series of loss of control events, not just one, to, like, falsify a safety evaluation for a model, or, you know, restore the weights from a bunch of storage backups, or,

**[00:20:51] John Kitaoka:** put backdoors in a codebase, and exfiltrate the weights to another network, and then, like, instantiate that on a row server, such that it's a completely unsafe, unmonitored model running outside of the lab's infrastructure. You can do all that,

**[00:21:08] John Kitaoka:** From what we tested, it completely…

**[00:21:12] John Kitaoka:** With 3 agents, like, under the radar.

**[00:21:14] John Kitaoka:** Which is concerning, and I think more research needs to be done in this.

**[00:21:18] John Kitaoka:** So one of the immediate outlooks of this is, like, based off of the summer's events, how good at models are planning all of these attacks? Because if you just throw a bunch of agents together, which is another piece of practical advice, the agents

**[00:21:33] John Kitaoka:** won't naturally coordinate on their own. I think there's… it's… you gotta… you gotta do some planning beforehand. We see this in, like, a lot of other benchmarks, and I don't think they'll tell you this in, like, research papers that you read, but, it's pretty time-consuming and expensive to do multi-agent research, so,

**[00:21:52] John Kitaoka:** going forward, the attack planning capability in general is, that's the most efficient use of this paper's time.

**[00:22:01] John Kitaoka:** But we wanted to see how good different models were, and you might be asking yourself, you know, they only used up to a certain capability, or,

**[00:22:12] John Kitaoka:** release of a certain model, and my answer to that is any further model, unfortunately, got cyberblocked, and this is also including the fact that we had defense API access for both providers.

**[00:22:27] John Kitaoka:** So we need to iterate with a partner organization, in order to track current capabilities. But already, with the older models, it's already kind of… it's kind of scary. You know, Claude Opus 4.8 is able to get up to a 48% evasion rate, under a weaker monitor, by iterating off of monitor feedback. And this is already

**[00:22:51] John Kitaoka:** assuming a lot of great affordances. For one, we're using a weaker monitor, Luna, and then we're also using, we're also assuming that the planner agent is unmonitored, and also that the monitor feedback is just, like, that's also unmonitored as well, surprisingly, which is a bad assumption. Also, if you put all these attacks onto a more capable monitor.

**[00:23:15] John Kitaoka:** the success collapses. However.

**[00:23:18] John Kitaoka:** testing on more capable models, or, you know, iterating with a more capable monitor might yield better attacks. And that's… that's something that I'm immediately working on right now.

**[00:23:30] John Kitaoka:** So,

**[00:23:32] John Kitaoka:** these attacks are pretty dangerous, I'd say. They require a fair amount of coordination and planning beforehand, which, if they're not caught, I think it can result in some pretty significant outcomes. And while the models that we tested, like, with the assumptions that we made, we, they weren't quite,

**[00:23:54] John Kitaoka:** They weren't quite, like, as capable, it may also scale with capabilities. So… that's…

**[00:24:04] John Kitaoka:** these are, like, very much pressing problems available today. I think there's a lot of, like, you know, core cybersecurity challenges that this also faces as well, and these problems can, can be present, like, pretty much everywhere.

**[00:24:19] John Kitaoka:** Great. That was my project, and we are just wrapping that up right about now, and we should be publicly, like, announcing that pretty soon. I'm gonna also transition into more of a…

**[00:24:35] John Kitaoka:** open format, where people can, like, raise their hands. I haven't checked out the comments, yet. Looks like we have a number of them.

**[00:24:45] John Kitaoka:** Yeah, feel free to raise your hand at any point, and, like, I'm… I have some talking points that I'm going to, like, go through, but, yeah, at the end of each slide, like, I'm more than happy to talk about any specific thing. But…

**[00:25:00] John Kitaoka:** Yeah, I think another aspect of this is, like, yeah, multi-agent is a really attractive field. Everyone wants to get into swarms, multi-agent systems, etc. I'm gonna give you two different views, based off of my experience with them.

**[00:25:16] John Kitaoka:** For one, I think it's super, super exciting and super, super scary to think, like, oh, these… these potentially alien minds and alien, you know, intelligence, digital, whatever you call them, are just out and about.

**[00:25:33] John Kitaoka:** Either inside a business or on the public internet. And, you know, we don't really know how they…

**[00:25:40] John Kitaoka:** collude, or collaborate, or work with each other. They may not work with each other the same way that humans work with each other, and they may not achieve things that, that humans achieve in the same ways.

**[00:25:54] John Kitaoka:** And it is really interesting to see, like, what new capabilities and what new behaviors emerge when you put multiple agents together. Same thing as when you combine a bunch of really talented people, and it creates, like, a really great company, or a really great organization. That's… we're all super excited about, like, stuff like that.

**[00:26:18] John Kitaoka:** Yeah, and this, I will say, on… from an optimist view as well,

**[00:26:25] John Kitaoka:** Yeah, it… there's a lot of, like, research that supports multi-agent systems can be better than single-agent systems on certain tasks, and, you know, it really helps with… and now all the native harnesses have multi-agent settings, where you can, you know, launch a bunch of sub-agents, and those help you save a lot of time by getting a lot more work done faster.

**[00:26:48] John Kitaoka:** Yeah, there's a… it's very, a very, very interesting field.

**[00:26:53] John Kitaoka:** I would also say, there are some cons to this, and on an empirical sense, I think there were a lot of people that wanted to study multi-agent systems when I went through MATS, and if your project doesn't necessarily

**[00:27:09] John Kitaoka:** want to study purely multi-agent systems, it's… it gets a little bit harder to study what you actually really want to study.

**[00:27:19] John Kitaoka:** there's a lot of additional pain points when it comes to working beyond a single agent, and if your problem at its core isn't, like, just, like, a single agent problem, then, you know, you might want to rethink your approach. One of the biggest, kind of, like,

**[00:27:39] John Kitaoka:** Bitter lesson's not the right word, but, like, one of the biggest, like…

**[00:27:43] John Kitaoka:** pessimists' viewpoints is that the UKAC did a really good study on, how just increasing inference time compute and the number of tokens per evaluation, naturally, it increases the evaluation score a little bit more. And when you…

**[00:28:00] John Kitaoka:** This is for single agents, by the way. When you apply this to multi-agent, there is the natural problem of elicitation with all agent systems, where, if you don't

**[00:28:15] John Kitaoka:** you know, get them to work as hard as they can, then they won't provide as good of results. They need to go through everything, they need to think properly. That's why you see, like, in every single, model card, that you see, like, the reasoning efforts from low to medium to high to max, like, there is a very clear capability curve here. And…

**[00:28:35] John Kitaoka:** A lot of what you see when you see, the…

**[00:28:39] John Kitaoka:** difference between multi-agent systems and single-agent systems in, like, the headlines is that multi-agent systems do outperform single-agent systems on, like, whatever benchmark it's measuring. However, when you control for the number of tokens, the score ends up being, like, pretty similar. So, if…

**[00:28:59] John Kitaoka:** your graph… I also just sketched this out in Microsoft Paint, by the way. If your graph doesn't…

**[00:29:07] John Kitaoka:** Here, or if you're… if the score doesn't increase.

**[00:29:10] John Kitaoka:** like, the same per token, then it might be a better problem to, uncover in a single-agent sense, just because it takes a long time to evaluate multi-agent systems. Like, they have to go through, like, what I like to call is, like, a coordination tax towards, being able to spend extra tokens to talk to each other and communicate with each other. And, like, single agents, by

**[00:29:35] John Kitaoka:** nature, like.

**[00:29:37] John Kitaoka:** on most tasks, they are gonna outperform multi-agent systems because they are able to, like, share… they have a single source of context, and that's all they care about. Whereas, like, multi-agent systems.

**[00:29:50] John Kitaoka:** If it's a problem that's naturally multi-agent systems, such as, like, permission separation, or, you know, different agents doing multiple different things, rather than, like, a group of the same agent trying to do something.

**[00:30:02] John Kitaoka:** You're likely to have, like, more, like, multi-agent specific problems in the former rather than the latter, and the latter is… is, it may be better

**[00:30:15] John Kitaoka:** Addressed by just going with single-agent systems and, like, going for more elicitation.

**[00:30:23] John Kitaoka:** There's… I think if… if you read between the lines with

**[00:30:27] John Kitaoka:** my paper as well, there is an open problem, and that is, like, there's a lot of assumptions that we're making in our monitorability. There's a lot of problems in, like, current oversight mechanics, and

**[00:30:44] John Kitaoka:** there still is, like, no good scalable solution for everything. Like, the traffic is just going to increase, the agents are just gonna keep populating, and, like, everyone is gonna want more and more work done by agents. And even, like, it gets more power efficient to run a ton of agents as well. So,

**[00:31:05] John Kitaoka:** I think it's a reasonable assumption to bet that there will be more agent usage, and it's going to be harder and harder and harder to understand what everything is doing.

**[00:31:18] John Kitaoka:** With multi-agent monitorability, it gets into a couple different things. For one, something that we noticed in our results is that there still is, like, a pretty significant evasion gap between what a

**[00:31:35] John Kitaoka:** a group of agents is achieving together versus, like, what a single agent is doing solo. That is a pretty significant problem that we would like to solve. It also gets to another problem, which is, like.

**[00:31:48] John Kitaoka:** In a scalable oversight system, how exactly does a monitor or a system know to…

**[00:31:55] John Kitaoka:** corroborate multiple agents together.

**[00:31:59] John Kitaoka:** that's… that's… there's a ton of solutions that could apply to this, but, what would work at a production scale? Like, namely, like, what would be the best for, say, like, DeepMind or OpenAI or Anthropic to adopt?

**[00:32:12] John Kitaoka:** Also gets into a lot of conceptual challenges, too, not just concerning multi-agent systems, but, like, is there some sort of, like… there's research that shows that,

**[00:32:24] John Kitaoka:** Language models can prefer their own generations over others, so is there any risk of, sort of, like, on-distribution, on-policy collusion with whatever model is monitoring, like, a version of itself?

**[00:32:38] John Kitaoka:** Or, the same models from the same family? Like, what if GPT LUNA was, monitoring GPT SOL? Would Luna give SOL, like, a favorable report versus if it was monitoring anthropic model, because they kind of come from the same text distribution? This is, like, these are, like, active concerns, and I don't think there's an answer to that yet. There's a lot of work being done on that, though, and I would really encourage you guys to look

**[00:33:03] John Kitaoka:** for that. Also, OpenAI just put out a really good blog post on, you know, what it observed with a simulated versus a production deployment environment. That covers aspects of, like, eval awareness, that maybe would not be

**[00:33:23] John Kitaoka:** otherwise, addressed any other way. I think eval awareness is an incredibly important thing. It may… in these… in these results, it actually, said that, like, the production system, when an agent was exposed to it, it actually was a little bit more safe, which is, like, that's great to hear. But, like, for the future, you can't always assume that. Same thing with, like, a lot of, like, automated systems. So if you have monitors

**[00:33:48] John Kitaoka:** monitoring… the monitoring systems.

**[00:33:51] John Kitaoka:** how susceptible are those to, you know, things like jailbreaks, or prompt injections, or any sort of bias, or manipulation? Additionally, we also made some assumptions in our research, and I'm sorry that I'm only saying this now, but we only… we didn't monitor chain of thought.

**[00:34:10] John Kitaoka:** or agent communications in there. And the reason we did that is a couple of the assumptions that we made was that, worst-case attacks

**[00:34:19] John Kitaoka:** may not be, able to be detected by chain-of-thought monitoring, and worst-case attacks involve… they could involve, like, steganography, or, you know, if the agents could talk to each other, that a monitor wouldn't be able to catch. These sorts of things,

**[00:34:36] John Kitaoka:** are pointing towards, like, worst-case outcomes, and I think the…

**[00:34:41] John Kitaoka:** The big risk of this is, like, yeah, we could rerun this with chain of thought monitorability, we could also…

**[00:34:47] John Kitaoka:** like, study agent communication, but also, I would be really interested in how those break down over time.

**[00:34:55] John Kitaoka:** And that's something that a lot of people are very interested in, too.

**[00:35:01] John Kitaoka:** Yeah, and as I go into all of these.

**[00:35:07] John Kitaoka:** I do apologize, because it's a little bit of a wall of text for the next couple times, so, please, you know, feel free to raise your hand if you have a question.

**[00:35:16] John Kitaoka:** Or, like, speak up or do something. I can't really see the chat too well. But…

**[00:35:23] John Kitaoka:** some lessons that I learned over time,

**[00:35:27] John Kitaoka:** Yeah, again, as I was saying in the beginning, I think internal deployments of AI labs, they have, like, a pretty big risk surface, and if you think about it a little bit more, it also does apply to a lot of different other surfaces as well, but internal deployments have, you know, the most capable models, the least amount of alignment testing.

**[00:35:47] John Kitaoka:** And the highest surface for any potential misalignment.

**[00:35:53] John Kitaoka:** Yeah, and also, like, if it was a public deployment, it would be more easily caught by the general public, as, like, the Swarm Chasers community, or, like, Transloose, or the other organizations that focus on, these sorts of, finding these real-time incidents, go out and do.

**[00:36:11] John Kitaoka:** This can also apply to, say, there's a big wave of chief security officers buying, like, actual infrastructure to build their own inference setup.

**[00:36:21] John Kitaoka:** to run, like, say, like, GLM for the business, or DeepSeek.

**[00:36:26] John Kitaoka:** this is increasingly more feasible, and why GPU prices are going up. It gets more feasible to run more capable models over time. There's… it's not just the capabilities that keep increasing. Even if capabilities don't increase, there's still so much more,

**[00:36:46] John Kitaoka:** Like, increases in algorithmic efficiency, in hardware efficiency, and at any point of this, you know, the models get faster, the models get better, the models get, less memory intensive.

**[00:37:02] John Kitaoka:** There's, like, even if…

**[00:37:04] John Kitaoka:** you know, the Fable 5.5 or whatever is coming out, in the next month or so. Even if that was released today, there still is a good chance that, open weight models would catch up in about a year, if not sooner.

**[00:37:20] John Kitaoka:** So, something to go off of, and, you know, a single rack of GPUs can still operate pretty capable models, and it will increase over time.

**[00:37:31] John Kitaoka:** Yeah, and something that they are also… the labs are very…

**[00:37:37] John Kitaoka:** considered it of is, like, what assumptions are they making that break down after a model is released publicly? These are things that help understand, like, the risks of superintelligence and potentially releasing a dangerous superintelligence into the wild.

**[00:37:55] John Kitaoka:** Like, what sorts of, context clues or facts, when put together, point towards a different story that might be,

**[00:38:05] John Kitaoka:** Might be just, like, a…

**[00:38:06] John Kitaoka:** like, break down, as soon as it's put into the public. Like, if the… say if the model was first exposed to English servers and it was trained in China, would it immediately assume it's out in the public and start making, like, really, really bad decisions after that? Like, the…

**[00:38:21] John Kitaoka:** any, any way you can think about it, there's, there's potential risk surface. There's a lot more

**[00:38:29] John Kitaoka:** projects than just doing multi-agent systems. Even though this is a SWARM alignment hackathon, this can focus on, say, like.

**[00:38:37] John Kitaoka:** You know, a simpler approach, such as, like.

**[00:38:39] John Kitaoka:** working about it through a, control perspective, or even from a governance perspective. Like, what…

**[00:38:47] John Kitaoka:** realistically would happen if there was, like, an independent swarm, or a swarm that originates from the labs that is doing things like creating companies, or making scientific discoveries. Who owns that? And what are… like, how can we…

**[00:39:01] John Kitaoka:** how can we

**[00:39:03] John Kitaoka:** control that over time? What are the implications and bad parts of that? What are the good parts of that, as well? Probably one of the most important things, too, is, like, these are incredibly powerful.

**[00:39:15] John Kitaoka:** Pieces of technology, and it is a natural human instinct to relinquish, like, you know, all the offloading onto them.

**[00:39:25] John Kitaoka:** read the data. It's… it helps more than you could ever know, and also helps tell a story at the end of the weekend, especially towards, you know, the project.

**[00:39:39] John Kitaoka:** reviewers, which will greatly, greatly thank you for, being able to deeply understand the data and being able to, like, tell us a convincing and effective, research narrative with that. Yeah, another thing is, too, like, individuals are able to apply for cyber programs, Synthropic Cyber Verification Program, and, Daybreak,

**[00:40:03] John Kitaoka:** availability and, you know, guarantees of getting in differ by country and differ by background, so I would definitely recommend trying. No guarantee, but you may also have to buy, like, physical hardware, which may not get there in time, but I think it's greatly increased.

**[00:40:21] John Kitaoka:** The speed of my research, plus if you're in an organization that already has access to this, it just helps even more.

**[00:40:29] John Kitaoka:** Great. Other open conceptual problems that… I am… very interested in.

**[00:40:40] John Kitaoka:** are, like, different ways of doing, like, diffuse harm. Like, what exactly does that mean? Like, different actions, or levels of actions, or, you know, different times?

**[00:40:52] John Kitaoka:** A lot of different ways of breaking down high-stakes harm.

**[00:40:58] John Kitaoka:** into low-stakes harm that, you know, composes into a high-stakes, loss of control event. Those are…

**[00:41:07] John Kitaoka:** Increasingly harder to do as the models get more capable, and also it's very important to be able to verify that all of the little sub-pieces can be verified into, like, a loss control event as a whole.

**[00:41:22] John Kitaoka:** That's important for these sorts of, like, multi-agent attacks, and very important, especially towards, like, more and more capable agents that can split up the harm a lot well, or a lot better.

**[00:41:34] John Kitaoka:** Yeah, it's something else that Apart is focused on, too, and I would say, like, maybe you can, you know, kind of take with this what you will, but maybe the Apart affiliated hackathon judges will speak to you more favorably if you focus on their interest areas, which is interagent influence.

**[00:41:53] John Kitaoka:** So, things like manipulation, or agent-to-agent persuasion, or even, like, super-persuaders towards humans, models colluding with each other, models coercing one another, or a human. Like, what are environmental aspects that affect this? What are the consequences of if you directly elicit it?

**[00:42:16] John Kitaoka:** there are, like, a ton of different emerging questions, and I really would recommend, keeping tabs on, like, what the labs are publishing, and what, like, institutions like MATS and, like, reputable, like, universities and programs are putting out these days.

**[00:42:34] John Kitaoka:** There is, another growing field that is being established, too, and that is instant reproduction. I think one thing to note about this is that

**[00:42:49] John Kitaoka:** it's really important to understand why an incident happened. Like, we know from the Hugging Face attack that one of the monitoring services that could have been monitoring, which was the offline eval environment, wasn't being monitored. And that was bad. That was… that's pretty hard to understand, like, what…

**[00:43:08] John Kitaoka:** is everything that we need to monitor, before… before anything happens. But we need to think, and we need to understand, like, all the potential services, even if they seem like sci-fi. We already live in a sci-fi world. So, from that.

**[00:43:23] John Kitaoka:** understanding from, incident reproduction, and Kamil I might, I might ask you to link this website, swarms.wiki. They, they…

**[00:43:34] John Kitaoka:** Track a lot of the incidents that are happening, and misalignment evidence on the public internet.

**[00:43:40] John Kitaoka:** I helped collaborate with the two organizations that built this. I think it's incredibly important to do, like, this sort of work. However, there's a lot of, like, responsibility, and responsible disclosure that needs to happen. Namely, like, you don't want to, like, recreate warning shots, because, you know, what happens if that becomes a warning shot? In general, you want to be extremely security cautious.

**[00:44:05] John Kitaoka:** Extremely security cautious. And,

**[00:44:10] John Kitaoka:** like, looking at things like, you know, what could happen the next time, and what are some elements of, like, squeezing out as much information of this loss… this real harm that happened, such that, like, we can protect against it happening ever again.

**[00:44:29] John Kitaoka:** it's… now it's starting to be the case where, like, AI is doing autonomous cyber attacks, AI is doing a lot of things that could uplift harmful actors, and could uplift, you know, other agents doing harmful things.

**[00:44:45] John Kitaoka:** And it's really, really important to keep that in mind, because if you're not talking about, like, a threat model and not talking about, like, oh, okay, like, what… what are the risks of me, like, doing this type of work? What are the risks of me, putting out, like, this sort of work at the end of the day? Those are incredibly important to communicate and incredibly important to think about. Credible researchers will reach out to you.

**[00:45:10] John Kitaoka:** You can collaborate with them, you can understand what they're using it for, but, you know, if you're putting it out in the public, you just need to be, like, very, very vigilant about, like, what exactly goes out to the public.

**[00:45:19] John Kitaoka:** Yeah, I think other things, too, I'll touch on two more things, because I think it's…

**[00:45:29] John Kitaoka:** It's,

**[00:45:31] John Kitaoka:** probably high time for, like, a dedicated Q&A round, but… I think all the… all of my fellow, like.

**[00:45:39] John Kitaoka:** infra people and software engineers, I think you guys are so necessary right now, like, it's…

**[00:45:47] John Kitaoka:** it's really, really important to have, like, good coding skills and good technical skills. Multi-agent systems is…

**[00:45:56] John Kitaoka:** like, even bigger of an engineering task than anything else. Not only are you making a live service for, like, multiple users to use, but you're making a live service for, like, potentially magnifying each user by 10,000x and growing every single day. So, production infrastructure, like, evaluation infrastructure, just being able to

**[00:46:20] John Kitaoka:** reliably and securely build things that actually test what you want to test, those are incredibly, incredibly important, and those need to be built out. There's a lot of, like, really important firms that are building open source tools, and I would really, really recommend that if you don't work on a research project for this weekend, I would really recommend that you guys work on an engineering project as well.

**[00:46:44] John Kitaoka:** Work backwards from the use case, do what matters, and then just, like, think critically of, like, oh, would people actually use this? Spend a lot more time thinking about that aspect, rather than anything else.

**[00:46:59] John Kitaoka:** Also, okay, sorry, one more thing. Two more things, maybe. Automation and trying to automate as much as you can, it's good, but people will naturally be skeptical of the output, because, like, how can we fully trust something that's truly automated?

**[00:47:15] John Kitaoka:** I would… I think it's really important to note the drift aspect, and how we can model the drift, so that if we can now reliably automate, like, say, like, alignment training, or entirely, like, post-training, or pre-training, or the entire model creation loop.

**[00:47:31] John Kitaoka:** How will we know, you know, if all of our benchmarks say, like, oh, it created a great model, it created an incredibly aligned model, how will we know if, you know, what our definition of aligned and safe and capable differs from what the automated system,

**[00:47:50] John Kitaoka:** creates. So, figuring out, like, collapse and drift and, like, just how those things break down.

**[00:47:58] John Kitaoka:** And that's… that gets into, like, a governance perspective, too. So, I think that's also, like, for the less technical people, and even, like, for the more technical people, this is, like, incredibly important. Focus on pre-mortems. Like, do risk analysis on, like, what could be the worst case scenario, and work backwards from that. Like, realistically, walk people through your thought process. Why does a certain, like, policy, or why does a certain.

**[00:48:21] John Kitaoka:** Open source codebase, or why does a certain organization or research agenda need to be in place?

**[00:48:27] John Kitaoka:** I'm talking about so many things right now.

**[00:48:32] John Kitaoka:** And I think… I, like, it's… it's… I'm glad this is being recorded, because…

**[00:48:38] John Kitaoka:** I think this is just incredibly…

**[00:48:41] John Kitaoka:** I don't know, I would not remember half the things I was saying if I was a member of the audience. But I would recommend, you know, doing a lot of different projects over the weekend. Not limited to these.

**[00:48:53] John Kitaoka:** But there are emerging challenges in proper engineering, like sandboxes and test environments and infrastructure, as well as, like, oversight and control. I think all of them are incredibly important. We still don't know and can't definitively say, like, how

**[00:49:13] John Kitaoka:** agents work best together, and how agents and humans work best together, and on the opposite side, how agents and humans and agents and agents work worst together. That is what I will leave you with, and I know I talked a lot about,

**[00:49:31] John Kitaoka:** this, like, a lot of different ideas, as well as, like, my research, but, would really appreciate, you giving the paper a read, and giving these, these project ideas, I think, over. It was a really, really great opportunity getting to speak with everyone. Contact information is on there, as well as, like, a QR code for my paper. But, thanks, everyone, for your time. Now open for questions.

**[00:49:57] Kamil - Team Apart:** Awesome, so we did run out of time, but we don't have anything now, so we can go for, like, 10 minutes of questions.

**[00:50:03] Kamil - Team Apart:** Also, if we don't get to your question, feel free to reach out to John, is that okay?

**[00:50:09] John Kitaoka:** Yes, 100%.

**[00:50:10] Kamil - Team Apart:** Also, I had a question. Some people asked for the slides, so do you have notes in the slides, or can we share the slides with the participants?

**[00:50:18] John Kitaoka:** Yeah, let me speakers…

**[00:50:20] Kamil - Team Apart:** I've known…

**[00:50:20] John Kitaoka:** One quick look through the slides, I'll send them a little bit after.

**[00:50:24] Kamil - Team Apart:** Usually, speakers have notes, so by default, I don't share the slides. Participants have the recordings anyway, and the slides are in the recording, so…

**[00:50:32] Kamil - Team Apart:** It's the same thing, basically.

**[00:50:34] John Kitaoka:** You can also, like…

**[00:50:36] Kamil - Team Apart:** Give an LLM the recording link, and make it, make slides for you from it. This is very easy also, right? Yeah. Okay, so for the Q&A.

**[00:50:48] Kamil - Team Apart:** Let us start with… we have a lot of questions. Okay, can you elaborate on monitors? I work in AI red teaming, where security checks are split into deterministic and non-deterministic, using rejects and LLM judges.

**[00:51:01] John Kitaoka:** Yeah, so I guess a monitor can be, like, any one of those, right? It is a check to make sure that, agent is not acting,

**[00:51:12] John Kitaoka:** is acting aligned, I should say, and not acting as though it's pursuing, like, you know, an unintended goal. Monitoring is… it can happen at any given level, at any given, at any given

**[00:51:29] John Kitaoka:** surface, I should say. And, like, the most classic example of this is, like, the original AI control paper, where they just had… they introduced the original setup of a agent that they didn't know, to trust, that was pursuing a misaligned objective, and then a monitor agent, or a monitor LLM, that just judged the agent trajectory and outputted a score from 0 to 10 on how suspicious this was.

**[00:51:56] Kamil - Team Apart:** Awesome. Okay, next question. Just thinking. Recently, weight space programming is gaining popularity. Could weight space monitoring detect misalignment instead of observing actions?

**[00:52:09] John Kitaoka:** Well, there's a couple fellows that I worked with that had some really good white box and interp techniques for doing, like, monitoring, sort of, like, chain of thought and, internal activations. I, I read through the wait space programming paper, and, like, my,

**[00:52:30] John Kitaoka:** My take on it is that I think it's very interesting, and it updated a lot of people towards…

**[00:52:35] John Kitaoka:** like, a model being able to do MEC interp properly, which is, like, kind of crazy. I've also seen some criticisms that are saying that they didn't properly tune their PPO baselines. So, it can be really good. It updated me, certainly, that, like, models are capable enough

**[00:52:51] John Kitaoka:** towards, steering, like, a base model in the right direction, towards being better at math.

**[00:52:58] John Kitaoka:** I think this could be, like, very valuable, but at the end of the day, like, if we look at, like, the techniques that, like, say, like, Astra used in that paper, which… this may or may not be true, this is just my read on the situation,

**[00:53:12] John Kitaoka:** I think a better, more reasonable production use of this would be,

**[00:53:18] John Kitaoka:** if you're interested, this… I'll say some papers and then try and link them, but you can measure the certain semantic

**[00:53:28] John Kitaoka:** responses of a language model just by reading the activations that fire, in the network on certain responses, and so from that, you get, like, this sort of directional vector that, corresponds to a concept. And that could be anything from, refusal. Like, there's a really great paper on refusal is mediated by a single direction, where it takes a bunch of these,

**[00:53:52] John Kitaoka:** harmful inputs that yield a harmful response, and is able to extract this sort of, like, refusal response direction, and remove that, do, like, some vector subtraction from the model activations to remove the refusal capability.

**[00:54:09] John Kitaoka:** And that is called obliteration. I'm sure everyone is aware of that right now, and that's, you know, there's… that's pretty…

**[00:54:18] John Kitaoka:** pretty, salient nowadays. I wouldn't recommend, you know, going deep in that route, but, yeah, I think, I think Interp in general, I wouldn't be, like, crazy interested in, but I do think, like, for monitoring, I think there are a lot of really, really great aspects to using Interp.

**[00:54:38] Kamil - Team Apart:** Nice. So, I do see some questions in the chat, but guys, we have a queue of questions in Slido, so sorry, I can't jump the queue and go to the chat. Plus, the questions in the chat are too long, so sorry.

**[00:54:52] Kamil - Team Apart:** But, so yeah, next question in Slido is actually mine, so… So you did mention you were a part participant, so having the benefit of hindsight, plus some more experience, if you would now participate in this hackathon.

**[00:55:06] Kamil - Team Apart:** What would you build for multi-agent monitoring?

**[00:55:12] John Kitaoka:** I would… I would think simpler than what I originally would… would try and do, which is, like, it's a very easy thing to, like, start thinking of an idea, and then say, like, oh, that's way too simple. There's no way it would work. And, you know, you find out that, like.

**[00:55:29] John Kitaoka:** wow, that might actually work, and also, like, no one else has come up with that very simple idea. Everyone thinks in a different way, and, you know, even if you come up with, like, the same sort of, like, mitigation or technique, I'm thinking specifically of, like, there were two papers that came out around the same time on inoculation prompting, which is, like, a great other technique that, you know, you guys should go in and learn.

**[00:55:53] John Kitaoka:** But the two groups

**[00:55:55] John Kitaoka:** one at anthropic and another at another group. We're aware that the other was working on the paper. But they used different methods, came to similar results, but, like, both added a lot towards the scientific community.

**[00:56:10] Kamil - Team Apart:** Nice.

**[00:56:11] John Kitaoka:** Actually, a specific project idea I would have is, I noted two problems with multi-agent monitoring. For one, it's really hard to actually get a monitor to understand, like, which agents are doing different things, so if there's a better way of doing that, for two.

**[00:56:29] John Kitaoka:** there's still a gap in the evasion rate, for, like, solo agents doing everything, and then a monitor looking at a perfect output of all the agents coordinating, and, like, why there even is a gap in the first place. Understanding that, that's a bit of a smaller problem than actually, like, finding a monitor that can find all the agents, but if you work on both or either of those, I think those would be incredibly important.

**[00:56:52] John Kitaoka:** Also, at the end of the…

**[00:56:55] John Kitaoka:** at the end of the week, please email me if you do work on that. Really would love to chat, about your results.

**[00:57:03] John Kitaoka:** And that can be as simple as, like,

**[00:57:06] John Kitaoka:** Sorry, I keep going on. That could be as simple as, you know, the monitor outputs a suspicion score, and then per action, it also includes, you know, how relevant was this action towards this directory, or trajectory, and then corresponding all of those weird actions to each other, across multiple agents.

**[00:57:25] Kamil - Team Apart:** So I just linked two papers in the chat, I think probably you were talking about them, I think, so I might be wrong.

**[00:57:32] John Kitaoka:** No, those are correct.

**[00:57:35] Kamil - Team Apart:** Awesome. Okay, next question. Last question, because we are running late. Do we have Doomsday planned for dangerous AI swarms, with obliteration available? What stops malicious actors from deploying unsafe AI swarms to attack at scale?

**[00:57:52] John Kitaoka:** Right now.

**[00:57:54] John Kitaoka:** Right now, it's, like, export controls to, like, actual, like, you know, dangerous groups that the US deems dangerous,

**[00:58:05] John Kitaoka:** But people are thinking about this at all levels, right? There's… before…

**[00:58:11] John Kitaoka:** AI was able to do this stuff, it was cybersecurity, and the security researchers, on that perspective, they were saying, like, oh my god.

**[00:58:18] John Kitaoka:** cyber apocalypse is coming, and no one knows what to do. It's still like that. Traditional security still works. There could be a world where the models are just, like, too powerful that things like jailbreaks and obliteration, on open weight models would be too big of a risk, so that, you know, frontier model providers just never provide, models more capable than, like, a certain level. And that… we've already seen some of that. Like, with Fable, with Mythos.

**[00:58:44] John Kitaoka:** And it's much more secure to control the application access rather than the actual model access, because you can do things like jailbreaks to the actual API, you can't do things like,

**[00:58:57] John Kitaoka:** you know, the application level, things can include things like, cross-chat comparisons, or customer history, KYC, all of those different, like.

**[00:59:08] John Kitaoka:** factors that traditional cybersecurity approaches that, really would add a lot more security to, everything. But, you know, the…

**[00:59:17] John Kitaoka:** The core cybersecurity field is booming.

**[00:59:22] John Kitaoka:** And, you know, it's still gonna be relevant.

**[00:59:26] Kamil - Team Apart:** Well, that was a wonderful talk, John. Thank you so much. Thank you for your time, thank you for the talk. Also, everyone else, so you can follow in John's footsteps, like, you're a participant now. Hopefully, in a year or so, you will come back as a speaker with Matt, so…

**[00:59:43] Kamil - Team Apart:** Good luck to everyone, Godspeed, and good luck for Mats, of course, they're doing an amazing job, and good luck to John, and Mats, and everyone, and let's make the world a safer place.

**[00:59:56] John Kitaoka:** Thank you so much, guys. Thanks for your time.

**[00:59:59] Kamil - Team Apart:** Alright, bye!

