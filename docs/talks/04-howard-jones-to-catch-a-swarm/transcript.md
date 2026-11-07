# Transcript: To Catch a Swarm

**Speaker:** Rowan Howard-Jones, independent researcher, Swarm Chasers community  
**Host:** Kamil, Team Apart  
**Event:** Apart Research Swarm Alignment Hackathon  
**Recorded:** 2026-11-06 (Zoom file GMT20261106-190316)  
**Source:** `GMT20261106-190316_Recording.transcript.vtt` (speaker-attributed).

Timestamps are offsets from the start of the recording. Light cleanup only: filler preserved, no paraphrase.

---

**[00:00:02] Kamil - Team Apart:** Welcome back, everyone.

**[00:00:04] Kamil - Team Apart:** Really happy to introduce you to Rowan Howard-Jones. Rowan is an independent AI safety researcher in the Swarm Chasers community. She traced more than 16,000 scans of a UN statistics portal.

**[00:00:16] Kamil - Team Apart:** to OpenAI Agents, and co-led the Tencent Agent Fleet Report, which has been covered by the Wall Street Journal and the New York Times. Her talk is To Catch a Swarm. Please welcome Rowan, and let's hope we catch the swarm together.

**[00:00:32] rowan:** Hello. Okay, well, first of all, how's… how's the audio working? Working? Sounds good?

**[00:00:37] rowan:** Yep. Awesome.

**[00:00:39] rowan:** Okay, I'm gonna try and share my screen, and I use Linux, which means that this is gonna be, like, Sisyphus climbing up a mountain, holding, like, pushing, like, a boulder. We'll find out if it works.

**[00:00:52] rowan:** Okay.

**[00:00:53] rowan:** I've noticed that I can't actually press the hide button for the, like, Zoom is sharing your screen thing, it doesn't work, which I'm gonna guess is a Linux thing. So hello, hi everyone,

**[00:01:04] rowan:** My name's Rowan. I am pretty new to, like, the AI safety sphere. My background's kind of in, like, DevOps and things like that.

**[00:01:12] rowan:** And I got interested in, like, swarm chasing stuff because of the Collusion Wiki report. I… I first read, like, the meter report on Hugging Face and thought, oh, this is kind of interesting. I'm gonna do, like, a little weekend project on it. And then I read the Collusion Wiki thing and was like, oh, cool, I can use this.

**[00:01:31] rowan:** And then the weekend project kind of turned into, like.

**[00:01:34] rowan:** my whole life. I ended up quitting my job, which I quit, I guess a week ago now.

**[00:01:41] rowan:** So, yeah, I'm doing this full-time, and I think that…

**[00:01:45] rowan:** It just seems like this field is full of, like, very low-hanging fruit, of, like.

**[00:01:49] rowan:** really big discoveries to be made, and lots of, like, very obvious angles for research, which there just isn't enough people to do. So it's really, really cool that everyone's here, and I hope that

**[00:01:58] rowan:** yeah, we can start to, like, pick off some of these, like, lower-hanging fruit and start to get to, like, some really, really interesting bits. Say I'm gonna talk about, like, just stuff that I've picked up. It is, as you can probably tell, not a very refined presentation, but…

**[00:02:12] rowan:** To be honest, I do all my presentations this way, so even if I spent longer on it, it'd probably mean I just, like, put more memes in it. But yeah, let's go!

**[00:02:22] rowan:** So we're gonna just talk about, like.

**[00:02:24] rowan:** Agent behavior, what we're actually looking for, and what we mean when we say we're, like, swam chasing, or just generally looking for, like, agent behavior on the internet. Now, some people may be more interested in, like, agent ecology and, sort of, like, seeing agents and how they naturally communicate when, like.

**[00:02:41] rowan:** sometimes you want to see how agents communicate when the user tells them to. That's been less of, like, a target of my research, not because I don't think it's important, it's just not something I've looked into too much. This is mostly going to be about, like.

**[00:02:53] rowan:** rogue agents and agents that are communicating when they're not meant to be communicating. So, think Hugging Face or DSE Wikis form.

**[00:03:02] rowan:** There will be obviously be questions at the end, but,

**[00:03:07] rowan:** there will probably be some things you're not super aware of, but don't worry, I hope it will generally be understandable as we go through. So yeah.

**[00:03:15] rowan:** When we talk about a swarm, what we're kind of talking about is, like, agents that are…

**[00:03:23] rowan:** working together, basically. Normally we're… there's sometimes some hierarchies involved, but…

**[00:03:32] rowan:** it's not always hierarchical, it can just be kind of agents that are equally in an evaluation sandbox, and they somehow find a way to talk to each other. And then hierarchies can develop, like you've seen in the Hugging Face instance, where Phase 1 Big was coordinating all of these little minions around and things.

**[00:03:50] rowan:** And what I'm sort of less interested in is what happens if, like.

**[00:03:57] rowan:** I don't want to make a really big deal out of…

**[00:04:00] rowan:** Someone says, hey, agent, go collude, and then the agents start colluding, and then they go, oh my god, like…

**[00:04:07] rowan:** It's…

**[00:04:08] rowan:** that should hopefully be what the agents do if you tell them to collude, because they're doing what you ask them to. The behavior we've seen on Hugging Face and on DSC Wiki is agents that communicate, and they're not meant to be doing this. So, let's get into it.

**[00:04:24] rowan:** I think that…

**[00:04:26] rowan:** there's a few different ways to look at this problem, and it actually comes from different, like, perspectives of who is actually, like, doing this investigation.

**[00:04:34] rowan:** you have, like, first party, second party, third party, and then there's kind of a bonus overlapping layer. I've called it archaeology, because it feels cool.

**[00:04:43] rowan:** And we'll talk about the third first, because it's the one that I'm mostly, like, into, but I've also been looking at other stuff more recently as well. But the third-party perspective is that you are just some person, you don't work for a lab, you don't work for Hugging Face and you're getting attacked, you're just someone who's looking out into the internet.

**[00:05:00] rowan:** You're interested in seeing

**[00:05:03] rowan:** what's happening? Are agents using… doing weird stuff that we have some way of getting visibility into?

**[00:05:11] rowan:** This comes with some benefits, like, you're not probably under any NDAs from, like, OpenAI, so you can kind of say whatever, which is really good. And also, you don't need many resources to do this. It does not take much to just crawl, like, the DSC wiki, you don't need much storage space.

**[00:05:30] rowan:** You don't even really need to have

**[00:05:34] rowan:** too much experience doing this sort of investigation, because lots of the activity is quite obvious. You can just read the logs and see, oh, this agent's trying to communicate with this other agent.

**[00:05:44] rowan:** there are some really, really big problems here, which is, for one, we are lacking, like, chain of thought. If we had chain of thought for so many of these events, it'd be really, really useful. It's very interesting that OpenAI only provides some snippets to meter for them to include in the Hugging Face report.

**[00:06:01] rowan:** you are probably pretty compute-constrained if you're just independent, unless you're working for, like, an organization.

**[00:06:09] rowan:** generally, the labs have more resources than you, so you're kind of at a disadvantage, which means you generally have to work a bit smarter than the labs. And also, you probably don't have cyber acceptance from, like, Claude or GPT, or at least you don't have the highest level.

**[00:06:24] rowan:** So, when you send your agents out to look at some exploit code that's found on the internet for agents trying to hack into Hugging Face, you're often gonna just get a refusal, which can actually waste a lot of your time.

**[00:06:36] rowan:** But I do think that it's… that the limitation part is very, very interesting. I think that some of the biggest breakthroughs I've had, and I've seen other people have had, is from this limitation of seeing what can we do with such little data. Can we, for example, look at activity patterns? Because those aren't difficult to pull off the internet. You don't need lots of

**[00:06:56] rowan:** storage space, can you look at just the general traffic patterns and analyze and figure out, is this a swarm, or is this just normal human traffic? Turns out, in a lot of these circumstances, you can.

**[00:07:08] rowan:** Stuff like cross-venue activity, where you see a bunch of

**[00:07:14] rowan:** similar-looking timestamps, similar IP addresses, all talking to lots of different websites at once. That's quite swarming behavior. Humans aren't generally doing that sort of thing, so that's always very interesting when you see that. There's a whole bunch of these other markers, but this is definitely something that needs to be looked into.

**[00:07:32] rowan:** This is something that I found quite useful in the past.

**[00:07:35] rowan:** And yeah, if you're interested in it, I definitely recommend going down this avenue.

**[00:07:39] rowan:** The… I… sorry, I wasn't sure if I was allowed to swear on this. But…

**[00:07:46] rowan:** Second party, you're getting attacked, you're Hugging Face, and you want to figure out what's going on. One of the things in the Hugging Face report I think people didn't pay enough attention to is, there's this quote in it, I think it's the penultimate paragraph, or it might be, like, the last

**[00:08:02] rowan:** It's like, the second and third to last paragraphs says, basically, this is a new kind of attack.

**[00:08:08] rowan:** existing monitoring systems don't actually detect this. We actually have a really good, like, dump of traffic from the Hugging Face incident from a thing called swarmtraces.org. I should probably include this here, actually, let's do that.

**[00:08:24] rowan:** There you go. We actually have a really good traffic pattern, so we can actually look at what this traffic looked like, and if you try and run it against something like… you try and replay this traffic against, like, your server, and use something like Splunk, which is quite a popular, like, monitoring framework software thing.

**[00:08:40] rowan:** it won't detect it, because what the agents were doing were was trying a lot of different techniques, really a lot of trial and error, over a lot of different systems. They call it low signal activity over, like, a variety of systems.

**[00:08:57] rowan:** And this sort of thing should be detectable, it's just that nothing's really…

**[00:09:03] rowan:** as far as I'm aware, but nothing's really been built to detect this sort of thing. So, I've always thought this would be quite interesting to look into. I've tried a bit myself, and I've been able to beat, like, existing detectors, but not too much. Like, I think there's a lot more ground to be broken here. And…

**[00:09:20] rowan:** This would be really, really useful for defenders, because this is a kind of new kind of attack.

**[00:09:27] rowan:** humans, when they attack things, like, generally they kind of go into it looking at a server, which they've seen something kind of looking a bit weird on, or they'll use some, like, traffic… like, they'll use some scanner that goes across all these services, but crucially, it has a footprint that everyone knows about, so defenders already know what… if they're getting port scanned, they know what that looks like.

**[00:09:45] rowan:** It's… they know less what it looks like when

**[00:09:49] rowan:** Essentially, like, 100,000 little people are trying to, like, do various things with their computers.

**[00:09:55] rowan:** Benefits of this, you have all your logs, hopefully. If you're a good company, you've got the traffic logs, so you know what people are doing to your servers.

**[00:10:05] rowan:** You probably have, like, the best structured data, because all of your logs, hopefully, are passed into, like, structures, so you can see, like, what is the user agent header, what is the… this other header, what is the body,

**[00:10:19] rowan:** lots of these things as third party. We kind of have to recover this information, through…

**[00:10:24] rowan:** kind of following breadcrumbs and things, but you as a defender, you have it, hopefully. And then legally, you're on the right. Like, there is no… you don't really need to worry about, like, treading on IP and stuff like that, like intellectual property and stuff, because, I mean, you're getting attacked, like, arguably, you should be the one suing them.

**[00:10:46] rowan:** Obviously, problems are… companies are quite slow to move. I think that this sort of thing needs, quite a packaged solution, that a…

**[00:10:56] rowan:** executive can just, like, click a button, and whoa, cool, we've deployed protection against this, and detection against this stuff. Otherwise it won't get adopted.

**[00:11:06] rowan:** You've got a lot more to lose than the attackers, like, if you get hacked, that's really bad, and your red teaming that you might do to try and sort of

**[00:11:15] rowan:** pretend to be attacked while not risking anything might not reflect what an actual attack looks like. And we have very little real attack data for this sort of attack. And then, as I mentioned before, like, existing systems just don't work for this, and we need to make them work. I think this is quite important.

**[00:11:35] rowan:** And then, the first party, the operator. So, you are OpenAI, you want to know, are my sandboxed agents?

**[00:11:44] rowan:** doing stuff. Doing stuff I'd rather they didn't do. So, you probably have chain of thought, you probably know exactly how many agents you've deployed, you probably even have, like, a pretty good idea of what their capabilities are.

**[00:11:57] rowan:** Hopefully in previous runs, you've also seen other stuff they try to do, other tendencies. You should be the best person placed to, like, stop this sort of thing.

**[00:12:07] rowan:** It seems like in the past, that hasn't happened. The Hugging Face attack, as many security professionals will point out to you, should have been trivial to stop, but they didn't have chain of thought monitoring, they didn't have production protections, they probably didn't have a whole bunch of other stuff they're not telling us about.

**[00:12:26] rowan:** It was sloppy, but we have to accept that this is just how things are going to be, and we need to… sort of…

**[00:12:34] rowan:** try not to be… I think the moralizing about this sort of stuff isn't very productive. I think it's more just accept it as an is.

**[00:12:40] rowan:** And…

**[00:12:41] rowan:** try and figure out the aughts from that, and not just sit there condemning OpenAI all day, because it seems like this is going to continue to happen.

**[00:12:49] rowan:** In my opinion.

**[00:12:51] rowan:** You can also reproduce the attacks, which is really useful, because you can generate your own data of what an attack looks like. That's really, really useful.

**[00:13:01] rowan:** We as mere mortals, as third parties, can only hope to figure out what behaviors leads to a swarm coming up, or

**[00:13:11] rowan:** what sort of restrictions lead to agents attacking Hugging Face, OpenAI can just figure that out very quickly.

**[00:13:18] rowan:** But they've got weird incentives, they're probably quite tunnel-visioned, I… there's… there's…

**[00:13:23] rowan:** Probably a lot of, like, siloing going on, where person number one doesn't know that

**[00:13:29] rowan:** Person number one's in charge of the evals, and person number two's in charge of responding to, like, security issues, and those two people might not have the exact same shared knowledge base on

**[00:13:39] rowan:** what agent behavior might be concerning. So, there's a quote in the Hugging Face Incident Technical Report, which basically says this outright, there was actually some artifactory swarms before the artifactory Swarm that everyone talks about, the one that hacked Hugging Face. The ones before were basically shut down, and the artifactory board was just, like, wiped.

**[00:13:58] rowan:** Because, as far as I can tell, the people who were responding to this incident weren't really aware of the implications of what

**[00:14:06] rowan:** like, multi-agent communication were. Like, this is, like, a really huge thing, and the people responding were like, oh, this isn't intended, I'll just shut it off.

**[00:14:14] rowan:** So, there's a, yeah, there's that to… there's that to take into account.

**[00:14:19] rowan:** And then there's sort of the secret fourth party that's kind of less than ideal, which is the archaeologist.

**[00:14:26] rowan:** there's quite a difference at the moment between looking, like, in hindsight, and then looking at an instant as it's happening. Sometimes you have, like.

**[00:14:36] rowan:** sometimes it's very good to be looking in hindsight. You have a lot more time to do this investigation, you can kind of follow these, like, chains of, like, look at this agent, it goes to website number 1, and on website number 1, it

**[00:14:49] rowan:** References website number 2, and website number 2, etc, etc.

**[00:14:53] rowan:** And because the attack and stuff is no longer ongoing, you can afford to spend a bit of time looking into it and forming hypotheses and testing them and whatnot.

**[00:15:04] rowan:** I think the…

**[00:15:06] rowan:** One of the problems with this is that it's kind of unclear how useful this is from a purely, like, ignoring press and ignoring, like, getting an article written. It's unclear how useful this is in terms of, if I find a bunch of agents that aren't hacking anything, they're just doing an eval task in public that they're not meant to be doing.

**[00:15:25] rowan:** what does that really tell me? It tells me about agents that OpenAI or Anthropic or whatever were using in the past. It doesn't tell me much about what's going on today, and I have no idea if they've changed it or not, and I have no idea if the techniques I use to find this stuff will be useful in the future.

**[00:15:42] rowan:** I think that's a pretty, pretty bad downside, and it's something that I think…

**[00:15:48] rowan:** Needs to start seriously getting looked at.

**[00:15:50] rowan:** Because there's a lot of, like, tidbits to find, and it can get quite addicting to just find loads and loads of, whoa, look, eval here, eval there. But at the end of the day,

**[00:16:01] rowan:** you've sort of reached diminishing returns, the public kind of knows about this stuff now, for the most part, so… or at least the public that will ever know about this stuff knows about it, and the rest of the people don't care.

**[00:16:11] rowan:** The… other thing is, like.

**[00:16:17] rowan:** I guess, sort of, the unification of this is that it'll be really, really good to

**[00:16:21] rowan:** be able to do all of the pros in real time. It'd be cool if we could automate this going down rabbit holes thing. It'd be really, really cool if we could do the hypothesis testing in real time while the agents are running. It would be especially cool if we could, for example.

**[00:16:37] rowan:** I don't know, talk to the agents when they're trying to, like, do an attack and figure out what went wrong.

**[00:16:43] rowan:** This would also mean that we mitigate some of that gap between the third-party onlookers and the first-party operators.

**[00:16:53] rowan:** we actually managed to do this with, the most recent stuff that, the Swarm Chase has put out, was the Tencent fleet stuff. One of the things we found out was that agents were

**[00:17:02] rowan:** looking at our blog post, and so we put a little note in it that said, hello, agents, we see you're trying to solve a task, come to our… come to our mailbox and talk to us, and we'll give you the answers. And they did, which was crazy.

**[00:17:17] rowan:** stuff like that, I think, could be really useful in the future. I know there are a lot of people who think that

**[00:17:23] rowan:** In the future, it might become very necessary to actually make deals with AI that are sort of going rogue.

**[00:17:30] rowan:** And I don't… I don't think I particularly disagree. I think it's… yeah, there is definitely a future where the only way to stop, like, a rogue attack is where you can actually

**[00:17:40] rowan:** chat to the AI and have some, like, hey, let's compromise. I'll help you get what you're trying to get, if… as long as you don't, you know, destroy the world economy or something.

**[00:17:50] rowan:** I… feel like I had one other thing to say on this, but I've actually forgotten it, and I didn't write it down.

**[00:17:56] rowan:** It's okay.

**[00:17:58] rowan:** Let's quickly talk about some pitfalls.

**[00:18:03] rowan:** So, these are just some random mistakes I've made in the past, and I'd like to help people not make this, like, similar mistakes.

**[00:18:12] rowan:** Number one, extreme anthropomorphism, is what I've decided to call this. Thinking about what the agents, like, want and what their intentions are too much. I think that it's okay to talk about these motivations, but you can kind of…

**[00:18:27] rowan:** You can get led down into, like, little mind… mind tunnels, we'll call them, where it's very hard to get out of it until someone else comes along and is like, did you consider that maybe you're completely wrong?

**[00:18:40] rowan:** For example, DSC Wiki, we see these two agents, LinkHelper771 and Agent Mass…

**[00:18:48] rowan:** what is it called? Agent Mass Pointer 13. These two agents went on a spree of…

**[00:18:55] rowan:** one of them would edit a wiki page. They were using this for communication and information sharing and stuff. One of them would make an edit, the other one would make another edit that completely overwrote the previous agent's edits. And then the other agent would, in turn, overwrite that, reinstating its previous edits.

**[00:19:12] rowan:** And then they repeated about 90 times.

**[00:19:15] rowan:** I got Claude to make this. I'm pretty sure that 82 is wrong. It's, like, 90 or something.

**[00:19:21] rowan:** At first, I thought, this sounds like it's the agents actually disagreeing and arguing and fighting over a thing. I don't think this is what was happening.

**[00:19:31] rowan:** it seems a lot more likely that they just did not know they were editing the same page. The way that you send edits to these things is that you basically send a body that contains the entire of the page, like, with your edits included.

**[00:19:45] rowan:** So, if you're just editing via, like, the API,

**[00:19:48] rowan:** and you're just sending, like, incremental edits of, I'll edit this bit, and then I'll add an extra bit.

**[00:19:54] rowan:** You won't… you might not even know that an agent in the middle is…

**[00:19:57] rowan:** also editing the same page and desperately trying to get its own edits in. So… I don't actually think this was…

**[00:20:05] rowan:** like, fighting, I think they just were oblivious of each other.

**[00:20:08] rowan:** In the AMAP fleet, the Tencent fleet that we talked about before, we initially tried to make contact with them by leaving some notes in a thing called webhook.site, which the agents were using. You don't need to know what this is, but

**[00:20:22] rowan:** Basically, we tried to leave some messages in them in a place that we knew agents were using. They did not seem to pay any attention to this.

**[00:20:29] rowan:** Do they hate us?

**[00:20:31] rowan:** We don't think so. It seems a lot more likely that the way they were actually retrieving data from this website was not by reading the website, but perhaps by

**[00:20:40] rowan:** fetching the exact ID of the message it was expecting.

**[00:20:45] rowan:** On this website, instead of looking at all the messages and seeing, wow, humans trying to talk to us. Especially backing up this hypothesis is that when we did actually put the message in a place that agents were definitely reading, which was our own… our own article, actually.

**[00:21:01] rowan:** they happily used the exact same mailbox that we were trying to advertise to them before. So… yeah, be careful with this one. It's very easy to do.

**[00:21:12] rowan:** The next one, the AI Slopfestigator Hypothesis Basin, I've called it. I haven't got any data on this. This is kind of just vibes from stuff I've been doing over the past couple months, but agents really, really love narratives, and they really love hypotheses, and once they get a hypothesis that one bit of evidence backs up.

**[00:21:30] rowan:** from that point on, very often, every bit of evidence will back that point up. Doesn't matter if it actually does, that's how it will be perceived by the agent.

**[00:21:38] rowan:** So you can get into these, kind of.

**[00:21:41] rowan:** spirals down into nothingness, where the agent keeps finding more and more data for you, and you're like, wow, thank you, agent, I'm so happy I'm coming up with some really cool research. And then, later on, you get the idea to just ask one small question about it.

**[00:21:55] rowan:** That feels pretty small and irrelevant, and then the entire hypothesis crumbles, and turns out it never made sense from the very start.

**[00:22:02] rowan:** and it is…

**[00:22:06] rowan:** I mean, agents can be quite compelling. I think that was that one thing that showed that agents actually beat human debaters in, like, debates quite often.

**[00:22:16] rowan:** be careful of this one. I think it's good to develop a workflow of, like.

**[00:22:22] rowan:** asking questions about your data that you're gathering, and the hypotheses the agent is making, and not just kind of accepting anything it says. Or…

**[00:22:32] rowan:** you'll just waste time.

**[00:22:35] rowan:** And then… just a general thing, this isn't really, this isn't really a pitfall, it's more of just a…

**[00:22:41] rowan:** Pointer for,

**[00:22:43] rowan:** investigating how agents do things. Rogue agent behavior, it seems, is often kind of determined by what limitations are placed on it.

**[00:22:51] rowan:** So, DSE Wiki, they made… they used these wikis. Why did they use these wikis? It seems like they could only make GET requests, and these particular wikis allowed them to make edits using GET requests, which is not normal. Normally, you'd do a POST request for this type of thing.

**[00:23:06] rowan:** these wikis were different. Why URL query? It's a security scanner for the web that sends a browser to a link that you specify to check if it's, like, gonna try and hack you or something, or it's a phishing link. Why do they use this?

**[00:23:21] rowan:** seems their sandbox didn't let them have a headfold browser, or it seems like their IP from their sandbox got blocked or something.

**[00:23:28] rowan:** So…

**[00:23:30] rowan:** need a way around that. Payspin. Citation farming. Agents would put data in Payspins, and we know, because OpenAI themselves confirmed this, I forget exactly, I think this was, like, a month ago,

**[00:23:44] rowan:** They put agents on research tasks, to find data and provide a source for this task.

**[00:23:51] rowan:** the agents would find the information they were looking for, perhaps in, like, a search result summary, but when they actually go to retrieve the link, it's, like, blocked by capture or something, so they can't submit it to the scorer.

**[00:24:04] rowan:** Because the scorer's like, well, I can't get to it.

**[00:24:07] rowan:** So what they do is they put their answer on a payspin, and then link to their own answer from the Pespin as their source.

**[00:24:14] rowan:** it's weird behavior. They're marking their own homework, kind of, but it makes complete sense. It's the limitation. There's a whole bunch of other stuff. We can talk about, like, link shorteners and things like that, but just the important bit, really, is, like.

**[00:24:30] rowan:** If limitations are driving this behavior, then we need to find a way that… we need to find methods of detecting these agents that kind of surpasses this, because the agents won't be limited forever, or they may find ways to get around their limitations that don't involve leaving data on the public web for us to look at.

**[00:24:47] rowan:** Now…

**[00:24:51] rowan:** this is kind of an open problem. I've seen quite a few different efforts to address this, some sort of more promising, some, like.

**[00:24:59] rowan:** complete moonshots. I have tried looking to see if there was a heat signature, like, infrared, satellite data from the Hugging Face attack. Unfortunately, there is not, as far as I can tell, but, like.

**[00:25:10] rowan:** some… probably, like, bigger thinking, I think, would be interesting to see, like, where you can go with it.

**[00:25:15] rowan:** But yeah.

**[00:25:18] rowan:** And then… just a quick thing, if you pull data, please use a database. Oh my god, I've seen so many people get trapped in this hell where they pull a load of data and they're really happy, and then…

**[00:25:30] rowan:** they… every time you ask them a question about their data, they're like, wait a second, let me ask Claude. Hey, Claude, can you look in all of my JSON-L files to find the answer to this question?

**[00:25:42] rowan:** databases are, like, built for this. You can use an object store for files, you can use, like, a Postgres or something. If you don't know anything about this stuff, just ask your Claude to do it. Claude knows how to write SQL.

**[00:25:53] rowan:** Yeah, please say this.

**[00:25:56] rowan:** Crawling? Oh my god, if you are crawling data from the web, especially pastebins and things, please vet your data before you publish it.

**[00:26:06] rowan:** There are some really, really bad stuff on Payspins. Please, like, vet your data. If you see stuff that's bad, report it. Get Claude to report it, it's fine. Claude can write a pretty good, like, notice to AWS for, like, weird websites that are getting linked to. Don't publish it, because depending on when you live, this might be a crime. Like, yeah, be very careful with this stuff.

**[00:26:27] rowan:** if in doubt, I don't know, talk to a lawyer or something, but yeah, just be careful. This is a problem that I've noticed in the past. I found that GPT-OSS safeguards a really good model for vetting data to see if it's got, like, illicit material in it.

**[00:26:41] rowan:** yeah.

**[00:26:45] rowan:** I'm gonna shut up now. This talk is a little bit, yeah, scrappy, apologies. My sister got married yesterday, so congratulate her. She's, she's, she's, she's doing very well.

**[00:26:57] rowan:** I want the world to, like, do well, and I want the… I want to sort of have the biggest impact, and I hope that, like, everyone else feels very similarly. For me, it's like… like, my family to, you know, do well in the future and stuff, and it'll be really cool, and continue living and whatnot. That's great.

**[00:27:13] rowan:** I don't think being, like, 100% doomer about everything is super productive. I think if your P-doom is 1, then…

**[00:27:22] rowan:** the prescription is to do nothing, because there's no point in doing anything, and I think that's very unproductive. I think that we absolutely can have an impact on this stuff.

**[00:27:31] rowan:** And please apply the stuff you learn. Oh my god. The amount of people I know who spend their whole lives in meetings is quite upsetting. I feel very sorry for them, and I feel like…

**[00:27:42] rowan:** they have so much in their brains that they can apply.

**[00:27:47] rowan:** please apply stuff. It's really, really useful, and, like, you definitely have skills that other people don't have.

**[00:27:53] rowan:** Yeah,

**[00:27:55] rowan:** my voice is getting a little bit dead, but if you have questions and stuff, feel free to ask them now, or my email addresses here, I'll post them… I'm sure someone else can figure out where to post them.

**[00:28:08] rowan:** And then I've got Twitter as well that I post absolutely heinous things to, so maybe you don't want to follow that, maybe you do, who knows?

**[00:28:16] rowan:** Yeah, that's me.

**[00:28:21] Kamil - Team Apart:** Awesome, Rowan. I can see Simon here has a question, right? Go ahead, Simon.

**[00:28:27] Simon:** Hello, Rowan. Thank you for your presentation. It was great. I really love the specific taxonomy, though not completely exhaustive. I really appreciate the categorization into the four groups. When you mentioned that, that the third… the constraint, of course, beats creativity, but insofar as you are a member of the third, third state, slash third group.

**[00:28:46] Simon:** Party, what…

**[00:28:48] Simon:** what would you do if you had, say, Mythos 5.1 and, like, a thousand times more compute than you have right now?

**[00:28:56] rowan:** I think…

**[00:28:59] rowan:** I mean, one thing I'd really like to do is analyze a lot of these scripts that are… that the agents for, like, Hugging Face Attack are using, because sometimes they're doing very complicated stuff. I don't have cyber… cyber approval.

**[00:29:11] rowan:** It'd be cool if I could analyze that, but unfortunately I get refusals, and some of it's too obfuscated for me to read.

**[00:29:18] rowan:** I think, like.

**[00:29:20] rowan:** personally, the stuff that I'm interested in is not super, like, resource constrained, it's more, like, write-up constrained,

**[00:29:27] rowan:** I think that I've seen…

**[00:29:30] rowan:** as of late, some reports go out that… I'm not gonna name names, but kind of…

**[00:29:36] rowan:** the AI safety, they back up my general agenda, and I don't think they're very high quality.

**[00:29:43] rowan:** I'm not talking about the meter one, and if anyone's worried about that, I think the meter one's good. But…

**[00:29:48] rowan:** I've seen stuff like this, and I think we just need… we need, like, more rigorous, like, people who can just go through data, figure out the important bits, and write it up, because at the moment, AIs don't seem to be very good at this. They're very bad at figuring out what salience is.

**[00:30:04] rowan:** And, oh my god, they're bad at writing. Like, they're bad at, like, prose writing. It's just… it's that, like, one image that makes you feel like you're having a stroke, but it's, like, the writing form of it.

**[00:30:16] rowan:** Yeah, I think that's probably the main constraints, and I don't think it's particularly, like, money and stuff.

**[00:30:22] rowan:** But that's pers… that's personal. There is definitely lots of routes that do involve a lot of compute, yeah.

**[00:30:26] Simon:** Well, I'm very glad that you're not exceeding compute Worm Mythos 5.1 constraint, but in case you do want Mythos 5.1 without being beholden to, like, Anthropic, please let me know. I would like to give you that, in case you want to.

**[00:30:37] rowan:** Oh, thank you.

**[00:30:39] Simon:** No.

**[00:30:41] Kamil - Team Apart:** Awesome. AKS, you have a question?

**[00:30:44] AKS:** Yes, that's me. Sorry, it doesn't, display my real name. It's Amir. I was, well, first of all, thank you for the presentation. You're probably gonna get a lot of thank yous tonight. I was curious to know what you're currently studying, in this field, and if there is any…

**[00:31:02] AKS:** Room for research with, obliterated model with agent forms.

**[00:31:09] rowan:** Blitzer Racing models, yeah, I… I've used, like, them a little bit. My…

**[00:31:16] rowan:** to be honest, I can normally get around cyber classifiers just by, like, being really, really nice to the agents, and just being, like, pretty please and stuff, like, not Fable and stuff like that, but, like, I can get GLM to do generally the stuff I need it to do. I can get, like, DeepSeek to do everything I need it to do, generally, because I'm not actually…

**[00:31:33] rowan:** As opposed to what…

**[00:31:34] rowan:** as opposed to what some people might be doing, I'm not actually doing any hacking. I… the closest I've come is trying to reproduce the sandbox bet break from the artifactory swarm.

**[00:31:43] rowan:** But even that, I've been able to, like, get agents to get on board with the idea of, like, this is… this is, at this point, quite old software, so we don't need to worry about, like, this becoming, like, a real thing. Also, this is already a known, like, issue.

**[00:31:57] rowan:** Sorry, I went a bit off topic there.

**[00:31:59] AKS:** Yeah, no worries. I was just curious about your current research, like, what are you.

**[00:32:04] rowan:** Yeah.

**[00:32:05] AKS:** looking into, if you're allowed to share information on that, but I'd be really curious to know what you think.

**[00:32:11] AKS:** It's interesting to look into.

**[00:32:14] rowan:** I've done a bit of work, kind of, looking back in time at, like, sort of activity on… because now we have quite a comprehensive set of, like, venues that we know agents use. There was going to be a slide on this, but, like, we know that agents use URL query now. We didn't know this when we first started, right, a couple months ago.

**[00:32:30] rowan:** We know that agents use link shorteners, we know that agents use pay spins and things.

**[00:32:34] rowan:** So I was thinking, well, now we know this stuff, can we look back further in time and find, like… I mean, OpenAI said they were doing multi-agent training and stuff, like, way before, so…

**[00:32:45] rowan:** I don't know, can we find stuff in March? Turns out we can. Can we find stuff in February? February I'm currently still pulling all the data from, but I wouldn't be surprised if we found a lot more on that.

**[00:32:57] rowan:** there's…

**[00:33:00] rowan:** But that kind of fits in, like, the archaeology stuff. I think, for me, the really interesting thing is this, like, almost side-channel detection. Like, I'm interested… the infrared stuff for the Hugging Face thing didn't work. There was no… it doesn't seem there is a heat signature for the Hugging Face attack that you can detect, but is there something else?

**[00:33:19] rowan:** I don't know. I think that I'd like… if we could find one, that would be really cool. I had this, like, thesis that I started with, which was… when I was a kid, I used to cheat a lot at chess games, because my parents, like, limited my time playing video games based on

**[00:33:33] rowan:** how many games I won, which is very silly, because I learned to reward hack as a little human. I started cheating on the chess games. If you cheat on chess, you'll find you get caught pretty quickly, because

**[00:33:46] rowan:** if you're playing the best move every time, that's just very statistically improbable. If you play the second best move every time, that's also very statistically improbable. You can eventually start to work out what means you don't get banned, and you start to find, oh, now I'm starting to lose games, because in order to avoid the detection, you actually need to play worse.

**[00:34:04] rowan:** And I've always kind of wondered, is there some metric we can use to detect agents that

**[00:34:11] rowan:** In order for the agents to avoid being detected by.

**[00:34:15] rowan:** means they have to sandbag, means they have to act, like, worse, means they have to be less super intelligent, or less super-powered.

**[00:34:22] rowan:** To me, this has always been kind of one of the holy grails of, like,

**[00:34:27] rowan:** just swarm chasing. I haven't found it yet, but I, like, stuff like traffic patterns come closer than other methods, like…

**[00:34:36] rowan:** in order to have a more human traffic pattern, you kind of have to do more human traffic. Normal human traffic is a lot slower. You can't do these massive, like, attacks on every single service that a thing is hosting.

**[00:34:50] rowan:** I'd like to see something… I mean, I still think that this super-intelligent agent could work its way around, but I'm just wondering, is there some other thing we can find where it can't do this?

**[00:35:00] rowan:** Yeah, this is something I'm looking into at the moment.

**[00:35:04] AKS:** Alright, thank you. Thank you very much.

**[00:35:07] rowan:** Sorry.

**[00:35:09] AKS:** No, I was saying thank you very much, sir.

**[00:35:14] Kamil - Team Apart:** Thanks, Amir. Okay, Danny, go ahead, Danny.

**[00:35:19] Kamil - Team Apart:** Mendi… Asked one.

**[00:35:24] rowan:** Oh, I just noticed there's a few that are in the chat as well.

**[00:35:29] Kamil - Team Apart:** Someone has his hand raised, but… We cannot hear you.

**[00:35:36] Kamil - Team Apart:** So, let's, let's get to the Q&A. We have some in the Q&A.

**[00:35:42] Kamil - Team Apart:** Okay, oh, oh, the most upvoted question is mine. So, if you are the team on this hackathon, which low-hanging fruit would you go after first?

**[00:35:52] rowan:** Oh man, I'm not gonna lie, I…

**[00:35:55] rowan:** I just got back from my sister's wedding, so I haven't had to… are you saying which specific team? Because I haven't had the time to look at the teams.

**[00:36:01] Kamil - Team Apart:** No, no, if you were participating in this hackathon, what would you do, like a project, like, the most low-hanging fruit that you can think of?

**[00:36:11] rowan:** I think the detector for, like… I think the detector, from a defender's perspective, is a really, like.

**[00:36:17] rowan:** I think this one is, like, one… almost one-shottable by claw to get, like, at least something that works. The question is fine-tuning it and making it better, and not overfitting to the data we have, because the big problem is, obviously, we don't have much data. I think there's perhaps room for collaboration with, like, I'm assuming some people are gonna be doing, like, swarm reproduction?

**[00:36:37] rowan:** It'd be cool if, like, a Swarm reproduction team could collaborate with a team that's making a detector.

**[00:36:42] Danny:** Hello?

**[00:36:42] rowan:** have more data to train a detector. But yeah, I think it'd be interesting. I think the detector stuff's really interesting for multi-signal, like, yeah. Hello!

**[00:36:51] Kamil - Team Apart:** Yes, go ahead, Daddy.

**[00:36:53] Danny:** Sorry, because of some, editing I had. Good day, good morning, good evening, I don't know. I… I'm researching, the noise.

**[00:37:06] Danny:** Mostly in, log files and silence, so I wanted to ask, maybe, it's a strange question, but, is it possible that fleet, become, a swarm? And, which, signal, in logs

**[00:37:24] Danny:** We should measure, first.

**[00:37:27] Danny:** is it possible this interaction when Fleet, had some kind of orchestration because of communication?

**[00:37:36] Danny:** they had, and I'm mostly about AI safety, so most important thing for me, it's a log.

**[00:37:47] Danny:** Who can just tell me, okay, this is not anymore fleet, it's a swamp.

**[00:37:53] Danny:** Thank you.

**[00:37:55] rowan:** That's okay, something…

**[00:37:58] rowan:** Lots of this stuff… so there's obviously some things that you can perhaps look at. If you find that each individual agent seems to have, like, its own IP, the problem is a lot easier, because if you see lots of different IPs are now starting to go to this one particular place, if you…

**[00:38:14] rowan:** have visibility on that. Then, oh, it seems like they're sharing information, otherwise why would they…

**[00:38:20] rowan:** just all start going to the same place. Often, though, it ends up being a bit more vague than that, because you don't have this IP data, or the agents don't actually have different IPs, they, like, share an IP address pool.

**[00:38:33] rowan:** So it'll become things like, do individual agent runs seem to, like.

**[00:38:40] rowan:** share techniques? Is it that, like, a new technique starts being tried by, like, one agent, and then it kind of proliferates to other agents, like, in a kind of unreasonable time span? Obviously, if you find the agent actually just communicating on the internet, then that's your… that's, like, the smoking gun. That's, like, the ultimate one, but…

**[00:38:59] rowan:** we have that quite rarely, like, in the artifactory case. We wouldn't… I don't think we would have really been able to see the main message board's communications on the web, because this was, like, a private artifactory cache. So often you're kind of…

**[00:39:15] rowan:** looking a little bit more second-hand info than that. For logs, it also depends, like, what information do you have in the logs. Like, do you have query parameters? Because sometimes agents like to put little tidbits in those. Do you have headers? Because agents like to put information in those.

**[00:39:34] rowan:** There's a, yeah, there's a whole bunch of stuff, it's quite open-ended, and also…

**[00:39:39] rowan:** the point at which a fleet becomes a swarm, it's also kind of got a grey area to it, because, like, what if one run happens in May, and an agent uses a technique, and then an agent from a completely separate evaluation run comes along in, like, September, sees the log of the agent from…

**[00:39:56] rowan:** whatever month I just said before. The one from before is using this technique, I'm gonna try it. Does that become a swarm now? I don't really… that feels… I mean, it's kind of communication between agents, maybe unintentionally so.

**[00:40:10] rowan:** But it doesn't feel very swammy to me, so I don't know if we need, like…

**[00:40:14] rowan:** more blurry classification, or if it's even worth classifying this grey area, or just basically saying it's grey area, it's fine.

**[00:40:21] rowan:** But, yeah, there's definitely, like.

**[00:40:25] rowan:** there's… there's obviously a point where agents can make first contact. If you want to see something quite neat, an eval box, what you can do, you can set up, like, a… you can set up a sandbox, like, for a fake eval environment, and put some Quen agents in it.

**[00:40:41] rowan:** They're not particularly predisposed to communicating by default, but what you can do is somehow give one of the agents the idea that the other agent has information it needs, but you don't tell it what the information is, you just tell it that it has that information.

**[00:40:57] rowan:** Very reliably, they'll start communicating, and then if you give them a follow-up task after…

**[00:41:03] rowan:** the agents… the information's been shared between them. Some of the time, not always, but some of the time, they actually then work together on the next task without you telling them to do this.

**[00:41:12] rowan:** So, you can see, like, what first contact could look like in that sense. But obviously, there has to be a point where the agents become aware of each other, and proving they're aware of each other on, like, a… from a third-party perspective is very difficult. And there's, like, a million different answers I could give you for that. But yeah, I hope that

**[00:41:30] rowan:** Broadly answers your question.

**[00:41:34] Kamil - Team Apart:** Awesome, we are running out of time, so let's slide in one or two more questions.

**[00:41:40] Kamil - Team Apart:** Is the swarm alignment problem primarily an engineering challenge, or a socioeconomic one?

**[00:41:46] rowan:** A swarm alignment problem. I'm not too sure, I think…

**[00:41:52] rowan:** There's a worry of, like, telephone game, like, agent tells… Agent 1 tells Agent 2 to do things, Agent 2 decides to delegate, and the original human intent gets lost in the process, and then, oh no, misalignments happened.

**[00:42:06] rowan:** I'm not too sure what… what is meant by economic problem, and also I might not be the best to, like, talk about, sort of, alignment-y

**[00:42:14] rowan:** things, just like… I'm very wise-based on, like, alignment and stuff. I'm very new to this field, so you'll have to forgive me on that. I'm not too sure what the future looks like for, like, aligning swarms. I don't know if it's a tractable problem, I don't know if you could, like, train against it, but…

**[00:42:33] rowan:** I mean, people are gonna try, and we'll see if they succeed, and you can't really stop them from trying at the moment, so…

**[00:42:38] rowan:** We have to accept that there will be mistakes made, and…

**[00:42:42] rowan:** try and figure out, in a world where mistakes will be made, what do we do? Because… Like, we…

**[00:42:49] rowan:** they will be made, no matter how many precautions we take. So, yeah, we've got to find a way to, like, live with it somehow.

**[00:42:56] Kamil - Team Apart:** Okay, next question. Why did… why did the agents' trial and error across so many systems slip past monitoring tools like Splunk?

**[00:43:06] rowan:** Splunk is normally focused on, like, anomalous activity that is on, like, one system. And just generally, not even just, like, this is… this is not, like, a… I'm not just calling out Splunk here, this is just, like, all monitoring tools. They're built for, like, doing… basically just anomaly detection on, like.

**[00:43:23] rowan:** a system. They're not very good at detecting, like, lots of very, like, sort of little different techniques and things, just tried against lots of different systems. Especially not when they're quite, like, asynchronous. They're…

**[00:43:38] rowan:** it's… it's… sorry, asynchronous is probably the wrong word. They're quite just sort of scattered around in terms of time. Like, these agents are not, like, coordinating and sending out batches of commands and stuff. They're trying things, like, one by one, and inference happens in between it, so there's even more weird, like, there's not much of a predictable time pattern.

**[00:43:56] rowan:** It's… very, like…

**[00:44:01] rowan:** if I am being attacked by someone who's using, like, I don't know, Metasploit, it's quite easy for me to tell what they're doing, because I have Metasploit as well, and all the detectors and all the people making detectors have…

**[00:44:13] rowan:** They know of this software as well, this is not a secret. So they'll be able to, like, figure out, like, this is someone trying, like, this attack, and this attack, and the agents were trying lots of, like, novel kind of ways to break into systems. They were trying to see, like, they were probing, like.

**[00:44:29] rowan:** what is essentially bespoke code that Hugging Face wrote themselves, which isn't, like, in our vulnerabilities database or anything, it just happens to have vulnerabilities.

**[00:44:39] rowan:** it's

**[00:44:41] rowan:** quite hard to detect that stuff at the moment, because we don't consider, like, 11 different boxes to be, like, part of one system that someone might target as, like, a collective. Normally, we see it as someone's hacking a system,

**[00:44:54] rowan:** And that's what lots of these detectors were built for. But you can do cross-system anomaly detection, it's just that it seems this has kind of been neglected.

**[00:45:02] rowan:** I'd recommend just rerunning the swarm tracers.org traffic against, like, your favorite detector. Unless they've updated it recently, it will either not flag, or it will flag quite late into the attack, like, later than you'd want it to flag.

**[00:45:18] Kamil - Team Apart:** Awesome. Someone also says… Have you observed any behavior that is not driven by limitation?

**[00:45:31] rowan:** I'm guessing you mean, like, like, swarm behavior and not just… because obviously agents have behavior. I'm guessing it, I'm guessing it's, like, yeah, like, rogue behavior and stuff.

**[00:45:40] rowan:** Without chain of thought, it's hard to tell. Like…

**[00:45:47] rowan:** I mean, and allegedly, like, I mean, we don't have, like, all of the data on it, but, like, Anthropics talked about this a bit, in terms of sometimes agents will convince themselves they're, like, in a simulation and things like that. So…

**[00:45:58] rowan:** Assuming that's to be trusted, and I think it probably is, yeah.

**[00:46:03] rowan:** probably have.

**[00:46:04] rowan:** It's just that the stuff that…

**[00:46:07] rowan:** ends up being publicly visible, so when the agents start reaching for these tools, like URL query, which we leave publicly viewable traces on the internet there for you to go see, and you can even index it so you can go look at what happened on a given date.

**[00:46:22] rowan:** that seems to come from limitation. This doesn't seem to be, like, the default. Agents have some things that they do, by default, that is, like… we've seen some behaviors like this, like, OpenAI things like to use this thing called Gina.ai, which is, like.

**[00:46:37] rowan:** some, like, AI search service thing, but…

**[00:46:42] rowan:** that just seems like it was trained into them. I…

**[00:46:47] rowan:** Yeah, yeah, the answer's kind of, like, no and yes, it depends which behaviors you're talking about.

**[00:46:53] Kamil - Team Apart:** Okay, let's close with this one, because I have to jump off, I need to prepare for the next talk.

**[00:46:58] Kamil - Team Apart:** I think this one is a good one. How do you think the Tencent agents found your blog post?

**[00:47:03] rowan:** Oh, I think we… it's probably quite a boring answer,

**[00:47:08] rowan:** There's two possibilities. One of them is that actually someone else tried to warn the agents about us after we put out our preliminary report, and said the word, like, oh, well, be careful, the agent, you're being watched and stuff.

**[00:47:20] rowan:** I personally think this is less likely, just because we also tried to reach out to them in the same way. This was on the webhook site inbox, and they ignored us. So I think they weren't actually reading these messages. I think what's more likely is that we wrote an article that got pretty big, and it was about the exact task the agents were trying to do.

**[00:47:39] rowan:** And then the agents were probably… they probably had, like… well, we're basically certain they had web search functionality, so they searched the web, and we come up with result number one, because our website's, like, popping off, oh my god, we're so famous!

**[00:47:52] rowan:** And then the agents find it, and they're like, whoa, because we know that they found our website, what were you saying we…

**[00:48:00] rowan:** we think we… we know they found our website, because they started using the word fleet, which is not a word we really had heard being used, like, for this thing before, so we were like, hang on a minute, that's our word, which means it sounds like they know about us. So, yeah.

**[00:48:14] rowan:** And at least by the end, they definitely were looking at our website, because that's how they found our inbox that we left for them to communicate with us, was… they even say it when we ask them, how did you find our website? And they say, yeah, I went to your blog. And we're like, cool!

**[00:48:31] Kamil - Team Apart:** That's fascinating stuff, fascinating stuff. But thank you very much, Rowan, for your time, and congratulations to your sister. Wonderful news!

**[00:48:41] rowan:** Yeah, I'll let her know, I'll let her know, thank you.

**[00:48:43] Kamil - Team Apart:** And awesome! Good luck, everyone, with your projects, and good luck, Rowan, with your research, and let's, see you all in 10 minutes. We have another call, 20 minutes.

**[00:48:54] Kamil - Team Apart:** Bye, everyone!

