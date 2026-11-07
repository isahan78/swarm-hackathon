# Transcript: Getting Started with Swarm Incidents

**Speaker:** John Yan (Gutenberg PBC, formerly Anthropic) and Elvis Sikora (maintainer of swarms.wiki and swarmincidents.com)  
**Host:** Kamil, Team Apart  
**Event:** Apart Research Swarm Alignment Hackathon  
**Recorded:** 2026-11-06 (Zoom file GMT20261106-180254)  
**Source:** `GMT20261106-180254_Recording.transcript.vtt` (speaker-attributed).

Timestamps are offsets from the start of the recording. Light cleanup only: filler preserved, no paraphrase.

---

**[00:00:02] Kamil - Team Apart:** Welcome back, everyone!

**[00:00:05] Kamil - Team Apart:** to the Swarm Alignment Hackathon.

**[00:00:07] Kamil - Team Apart:** For this talk, I'm really happy to have with us John Yan and Elvis Sikora. John helped train Cloud3, and is now founding Gutenberg PBC. It's focused on handling and studying Swarm incidents, so this is right on point.

**[00:00:22] Kamil - Team Apart:** Elvis maintains Swarms.wiki, which is in your resources, and Swarmincidents.com, the directory and timeline for AI Agent Incidents. Their talk today is getting started with Swarm Incidents, so please welcome John and Elvis.

**[00:00:41] john @ gutenberg:** Thank you.

**[00:00:43] john @ gutenberg:** Yeah, thank you so much, Kamil, for the awesome introduction, and nice to meet you all, thank you so much for tuning in. Do I have permission to just go ahead and share my screen?

**[00:00:53] Kamil - Team Apart:** Yes, sir.

**[00:00:54] john @ gutenberg:** Terrific, terrific. Alright. Well, this is going to…

**[00:00:59] john @ gutenberg:** this is just gonna be, like, more casual, I didn't really feel like fleshing out these slides, more of a conversation.

**[00:01:04] john @ gutenberg:** But basically, I wanted to introduce us, Gutenberg, and what we do, which is incident science, and what we do to support incident science, which we have a website called Swarm's Wiki.

**[00:01:16] john @ gutenberg:** And so, what is incident science, first off? All these incidents are piling up, and they are evidence that things are not going that great for us, right? And so, how do you get the most out of them? How do you get the most out of all these warning shots to try to prevent future ones?

**[00:01:31] john @ gutenberg:** And so this is an example of what happened, like, I think just a couple days ago.

**[00:01:38] john @ gutenberg:** Where, Marcus Williams, OpenAI research lead, or safety lead, talks about how Astra is underperforming on safety tasks. And all we, you know, he tells us a release of what's going on.

**[00:01:52] john @ gutenberg:** And then if you look at the quote tweets, some people are just like.

**[00:01:56] john @ gutenberg:** This is, like, one of the, you know, this is terrifying, this is terrifying.

**[00:02:00] john @ gutenberg:** This is extremely concerning. Some people are like, this is maybe not that bad.

**[00:02:07] john @ gutenberg:** And then some people are just like, well, what about this, you know? And so…

**[00:02:11] john @ gutenberg:** effectively, there's, like, maybe a thousand researcher hours spent on Twitter, sort of debating how terrifying or not terrifying this thing is. And if it is terrifying, we should know. If it's not terrifying, we should also know. This is, like, the whole point of, like, Incident Sciences. We should, like, be able to understand what the heck is going on here, right?

**[00:02:31] john @ gutenberg:** What we did is we just, replicated this ourselves.

**[00:02:39] john @ gutenberg:** Which is where we took the same methodology that they did, and we did find that there was a…

**[00:02:44] john @ gutenberg:** reproduced gap in the capabilities versus safety frame tasks. Everything else is considered the exact same. And then we… we're not… we're not claiming that we studied everything and we're done. No, no, no, we just, like.

**[00:02:57] john @ gutenberg:** took all of our data and our code and everything else, and we just, like, produced it, and other people can build on top of it if they want to run experiments, right? We are doing open science and a public ecosystem, so everyone can, like…

**[00:03:09] john @ gutenberg:** as long as you're, you know, researchers are still gonna go on Twitter, but hopefully in the time that it takes to go on Twitter, you can at least, like, just run the experiment instead of debate among yourselves how scary this is.

**[00:03:20] john @ gutenberg:** And that's kind of the whole point of incident science, right? Is you just replicate and run the experiments. You can look at these resources later, we'll find a way to distribute it to you guys.

**[00:03:29] john @ gutenberg:** I imagine most of you all know what Hugging Face is, and you are, like, appropriately freaked out. Not everybody is necessarily that freaked out about Hugging Face. If you talk to the average layperson, some people are just like, oh, I think I heard of that. And some skeptics are just like, oh, just don't listen to the propaganda.

**[00:03:47] john @ gutenberg:** I think that, like, you know, the whole point of incident science, again, is that you can take incidents, and you can study themselves… you can study them yourselves to see how bad could it have been, how easy would it have been to treat. This is, like, very useful for everybody.

**[00:04:02] john @ gutenberg:** And so… We have a website called swarms.wiki. And literally, it was just,

**[00:04:10] john @ gutenberg:** designed to be, like, a global project tracker, or, like, GitHub for these agent incidents, where, you know, an incident happens, you want to track it, you want to contribute to it, you want to consume information about it.

**[00:04:21] john @ gutenberg:** you can just go ahead and look through here to see Hugging Face being breached, you can see a German wiki being used as a back channel, you can see all these different things.

**[00:04:29] john @ gutenberg:** Where are the tools? Who's working on what? Where are the data sets? Where can I contribute my tools and data sets and methods, and be connected to the people who are already doing this? That's the whole point of this website. Elvis is our terrific maintainer of this website.

**[00:04:44] john @ gutenberg:** It is only a couple weeks old, maybe 2 or 3 weeks old. It was a Google document, like, just linking to our friends' homepages for a little bit.

**[00:04:54] john @ gutenberg:** But yeah, you all get to be early users of this website.

**[00:04:58] john @ gutenberg:** And it already has, like, about almost 300 tracked incidents with, like.

**[00:05:04] john @ gutenberg:** the best available curation to be connected to people's

**[00:05:07] john @ gutenberg:** work, or contributions, or, like, tools available to this. So I encourage you all to comb through this, find

**[00:05:15] john @ gutenberg:** tools, resources that are of the flavor that find… that you find useful to you. And please have a very low bar for contributing feedback. Elvis is available to, I guess, would it be okay if I gave them your email, possibly, if that's best? Yeah, okay, email. But also the website itself has, like, a way to sort of, like.

**[00:05:33] john @ gutenberg:** contribute for, contribute information as well. And, we even have ways to contribute non-public information for the people who find stuff that, like, don't want to be able to share everything totally publicly on the website.

**[00:05:45] john @ gutenberg:** Yeah, that's pretty much it. Besides that, we have a playbook that we ourselves have used. This is, very scrappy, and we will have a more refined one later, but really what happens when an incident happens, like Hugging Face, or like the OpenAI disclosure, right?

**[00:05:59] john @ gutenberg:** You want to understand it, you want to, like, get the most out of it, so you come up with all these hypotheses about, like, what are the… what are the specific things that you want to test?

**[00:06:09] john @ gutenberg:** you reenact those, you break it into pieces, you test it, and you iterate based off of your findings. And so, we have, like, plenty of examples that are collected from us, our friends, we will flesh this out into, like, a…

**[00:06:24] john @ gutenberg:** A less wrong poster, a white paper, that'll be publicly available soon, but we will also link this current playbook to everybody.

**[00:06:33] john @ gutenberg:** Yeah, that's all we had for our talk. I'm happy to open up the floor to Q&A.

**[00:06:41] Kamil - Team Apart:** Awesome!

**[00:06:43] Kamil - Team Apart:** Awesome! How do we contribute to Gutenberg? someone asks.

**[00:06:48] john @ gutenberg:** Yeah, contribute to gutenberg by contributing to Swarm's Wiki. And how do you contribute to Swarm's Wiki? You can either, like, take an incident itself, and let us know that, you know, there's, an OpenAI research cluster being taken over during an evaluation. This was, like.

**[00:07:05] john @ gutenberg:** basically just as freaky as the Hugging Face incident. But nobody really studied this, and so how do you do that? I mean, you yourself can, like, sort of use this playbook and be like, okay, what are the hypotheses.

**[00:07:15] Jorge:** this is true.

**[00:07:17] john @ gutenberg:** Right. Well, maybe AI.

**[00:07:20] john @ gutenberg:** Why would it take over a research cluster? Well, it knows that it can get admin privileges if it has full admin access to the research cluster, and the version in the sandbox does not have admin access, and so it gives… it's a way to give itself more… more power, right? And so you could basically try to do all these experiments of, like, here's a research cluster, here's a way to get admin access.

**[00:07:40] john @ gutenberg:** And then poke the AI until it takes it. That's an example of an experiment.

**[00:07:46] john @ gutenberg:** If you do end up producing findings or data sets, or methods that you want to contribute to, like.

**[00:07:53] john @ gutenberg:** that's one incident that you could, contribute to directly on the website. At the meta level, the website itself is young, you are all early users of this, and so any feedback on just, like, how to make the website more usable, more intuitive for you is also terrific.

**[00:08:11] Kamil - Team Apart:** Awesome. Okay, I have some questions. So, if you were participating in this hackathon, which incident would you pick first?

**[00:08:19] john @ gutenberg:** Yeah, that's funny. We actually do, a set of

**[00:08:26] john @ gutenberg:** like, incidents that we do study ourselves. I think that these are all still, like, extensions of the Hugging Face study.

**[00:08:32] john @ gutenberg:** And when… we'll paste our outputs in here as well when they're ready. But basically.

**[00:08:38] john @ gutenberg:** we study memetic misalignment, which is where, we know that, like, it's possible to go from zero misaligned agents to one misaligned agent, sure, but, like, how… like, what happens when you go from one misaligned agent to two, or two to three, or three to four, right? And so this kind of thing we want to study of just, like, does the rate at which

**[00:08:56] john @ gutenberg:** Getting the marginal misaligned agent accelerate.

**[00:08:59] john @ gutenberg:** It certainly seems like that was the case, right? How do you get to 1200 unless things were speeding up? And if you can motivate the case for things do speed up, that's our hypothesis, right?

**[00:09:08] john @ gutenberg:** That's also pretty terrifying, and that's also pretty valuable for people to know if this risk is, like.

**[00:09:15] john @ gutenberg:** a very major part of what happened in the Hugging Face incident. So that's one of the things we do.

**[00:09:21] Kamil - Team Apart:** Nice. Okay, someone… Anna asks, apart from contributions from people like us, how do you discover more incidents to add to the wiki?

**[00:09:29] john @ gutenberg:** Yeah. Sometimes they come pretty neatly packaged in, like, a Twitter thread, where they just say, hey, this is what happened, and here's the official report, right? So our job is to, like, ingest all of these. I think…

**[00:09:42] john @ gutenberg:** And then curate them.

**[00:09:43] john @ gutenberg:** I'll stick with that class. Elvis, I don't know if there's anything more you want to say about… Yeah, like, I don't have the exact list of sources handy right now, but I, like, I could share that.

**[00:09:56] john @ gutenberg:** If you want. But we basically ingest news and reports from many different sources, and as we find out, there are gaps in our data, like.

**[00:10:05] john @ gutenberg:** our list of sources, we keep patching them to have a… As complete as possible pipeline.

**[00:10:13] john @ gutenberg:** Keeping the, like, the instant tracker up to date.

**[00:10:17] john @ gutenberg:** So some of them are, like, very easily discoverable, because people will tell you, and so you just have automated pipelines to scrape all the major news sources.

**[00:10:26] john @ gutenberg:** Maybe the other interesting question that's a part of that is, like, how do you discover incidents from rogue agents, right? Or just, like, stuff that is just live in the wild? And, many of you probably are familiar with, like, the German Wiki incident, and maybe the Tencent fleet.

**[00:10:43] john @ gutenberg:** incident discovery is its own beast, and we're pretty connected to the people who, like, Palestra, Swarm Chasers, and Transluce, we're pretty connected to the people who do do stuff like this. And so.

**[00:10:58] john @ gutenberg:** their guide… Transluce's guide, is probably the best written guide up right now, which is where they say, like, hey, here's how you get started with agent hunting. They have some tools for monitoring fingerprints on the internet to see if the internet looks, you know… to see…

**[00:11:13] john @ gutenberg:** Whether or not there's any fingerprints that are left behind that look like rogue agent activity.

**[00:11:19] john @ gutenberg:** this is a little bit, like, new information as well that we just got from Palestra and the people who are doing this. It also seems that they expect the amount of agent activity on the internet to be less rogue

**[00:11:31] john @ gutenberg:** agents, for a couple reasons, right? One, the labs themselves are moving towards offline evals. The labs, you know, why were there rogue agents before? Well, they'd had online evals where agents could access the internet, and so they, like, did things that they weren't allowed to do. And nowadays, labs are shutting that down because they're aware that that happened. And so.

**[00:11:50] john @ gutenberg:** They… I'm not saying that, like.

**[00:11:53] john @ gutenberg:** There's no chance that there will be, like, any more rogue agents that sort of break out of labs, or it could break out of, like, other parties, that have agents doing, like, unauthorized things.

**[00:12:03] john @ gutenberg:** But,

**[00:12:05] john @ gutenberg:** It seems like it will be less frequent than, like, at least the amount of news that we got in the last couple of months.

**[00:12:13] john @ gutenberg:** That's not to say that it isn't valuable to find, because if it did break through an even tighter, sort of, set of sand guardrails, that's, like, quite a significant contribution.

**[00:12:23] john @ gutenberg:** Also, there are people who we are connected to who find agents that are not

**[00:12:31] john @ gutenberg:** rogue, but, like, intentionally being misused. In fact, this number is increasing.

**[00:12:38] john @ gutenberg:** It's not totally clear how to contribute to this, because right now it's all private parties dealing with, like.

**[00:12:44] john @ gutenberg:** governments and some enterprises getting hacked. We do have contacts to people who, like, are working on this, and they are hiring, and we can, at the very least, like, link to their homepages.

**[00:12:59] john @ gutenberg:** Actually, I'm just gonna go ahead and say without, like, asking for their permission, like, Palestra might be into this, Swarm Chasers might be into this, Asymmetric Security might be into this.

**[00:13:11] john @ gutenberg:** And when they have resources available for getting started, the same way that Transluce has a getting started, when they decide to crowdsource things, we will, of course make that available on the website, and feel free to let us know if you have any questions about updates like that.

**[00:13:26] Kamil - Team Apart:** Nice. She says thank you. Okay, we have another question from Ermal. So, she says…

**[00:13:33] Kamil - Team Apart:** There's not enough information provided by the companies that caused the incident in order to investigate and replicate it properly and deeply. How do you mitigate that, and is there going to be a scoring based on that?

**[00:13:45] Kamil - Team Apart:** No, no, this is something related to hackathons.

**[00:13:48] john @ gutenberg:** Oh, I see, I see, yeah. I think that this is a big part of the theory of change of incident science, right? Labs have this one perspective of just, like.

**[00:13:57] john @ gutenberg:** you know, they will kind of fight to the death, before, providing, like, even a single piece of information, and they have extremely, like, strong reasons to be as secretive as they are, right?

**[00:14:11] john @ gutenberg:** And yet, this makes things very difficult for anybody to do any kind of public science on just, like, I'm sorry, I'm freaked out. I'd like to understand more about how to, like.

**[00:14:20] john @ gutenberg:** one, measure the actual harm, and two, measure the mitigations and do anything about anything, right? I think that this is, like, an example that, like, is showcased by the work that we just did. Where was that?

**[00:14:34] john @ gutenberg:** Oh, hold on, it's this guy.

**[00:14:39] john @ gutenberg:** So, you know, they gave some information in this, in this report that said, hey, agents sort of underperformed, and then

**[00:14:49] john @ gutenberg:** we did the base… we did experiment level one, and then they said that there was a second level of experiment that we tried to do as well. They said, like.

**[00:15:00] john @ gutenberg:** task completeness… there was basically a second level of experiment that they did, and we were not able to do that experiment because they didn't give us any details. That second level of experiment would be very useful for us as well. And so…

**[00:15:13] john @ gutenberg:** When you produce something in the public like this, you help put pressures on labs to be like, hey,

**[00:15:19] john @ gutenberg:** Labs know the costs of giving more information out, because all they think about is, like, how harmful it could be if secrets get leaked.

**[00:15:28] john @ gutenberg:** But they don't have a good measure of the benefits of giving secrets out, right? Or, like, not even secrets, just information out, right? And so, if you do… if you take a step, and then you say, I'm really confused to do the next step, and all it would take is understanding, like, the specific prompts that you used for this experiment. Because I didn't know the prompt they used for their experiment, and our experiment was, like, null, right?

**[00:15:48] john @ gutenberg:** That…

**[00:15:50] john @ gutenberg:** Provides a… that gives them a much better way of deciding what is the cost-benefit for all the secrets that they're… or, like, all the information that they're going to sort of make, right?

**[00:15:59] john @ gutenberg:** that is kind of your job, I think, as people who want to contribute to, like, a public, like, incident science ecosystem.

**[00:16:06] john @ gutenberg:** This is also true of the Swarm Chasers who are looking for rogue agent fingerprints on the internet, is,

**[00:16:13] john @ gutenberg:** I'm not one of the people who are, like, experts at Swarm Discovery, but they say stuff like, okay, step one is figure out the agent's task, then figure out the agent's identity, then figure out, like, where they were coming from,

**[00:16:25] john @ gutenberg:** and figure out how many of them there are. There's all this information that you have to, like, back.

**[00:16:29] john @ gutenberg:** like, a reverse engineer, and it's really painstakingly difficult. And the labs know the costs, again, of giving out any information, but if you tell them the benefit of your… just tell me this one thing, like, was this part of one large thing, or, like, two separate things, right? That can… that single bit of information,

**[00:16:48] john @ gutenberg:** You can measure, basically, how beneficial that single bit of information is.

**[00:16:52] john @ gutenberg:** As you start to do your work. And that helps, cooperate and put pressure on labs to, like.

**[00:16:59] john @ gutenberg:** disclose more information. There is also… so this is the cooperative side of things, and then there also is the kind of, like, you know, keep the labs honest in an adversarial setting of, like.

**[00:17:10] john @ gutenberg:** hey, you said that you put down safeguards, but I noticed by the date that this sort of thing was going on that that doesn't match up with your story. That hasn't really happened yet, but it could happen in the future, and so that's why, again, like, an independent sort of ecosystem helps audit the labs in this way.

**[00:17:27] Kamil - Team Apart:** Nice. Okay, Melissa asks…

**[00:17:29] Kamil - Team Apart:** She says, I'm sorry if this is a rookie question, so there are no rookie questions. We do aim to cater to new people, so…

**[00:17:37] Kamil - Team Apart:** All questions are welcome.

**[00:17:38] Kamil - Team Apart:** Once you've reproduced an incident, Is the next step finding ways to safeguard against that incident reoccurring?

**[00:17:46] john @ gutenberg:** Yeah, I think,

**[00:17:48] john @ gutenberg:** That is a very good next step. I think it's case by case of, like, once you reproduce an incident, you can do all kinds of things. You can ask, one, what caused it, right?

**[00:17:59] john @ gutenberg:** I think people have, like, different hypotheses of, like, what caused it and did not, and so that's an experiment on its own. Two is, could it have been worse? And so, you can ask questions like, you know, if this only happened with, like.

**[00:18:12] john @ gutenberg:** GPT 5.5, but you want to wonder if, like, GPT 5.6 would have done something even worse if it was about to do this situation, right? These are, like, good questions to ask. And then 3 is, yeah, like you said, how to mitigate it. And so, you know, let's say, for example, this happens with an open weight model, but you, like, add some more…

**[00:18:32] john @ gutenberg:** secure safeguards, or prompt it better, or even, like, you want to do alignment training, because you want to ask if alignment training is working, yes or no. That's the… these are all good reasons to have the incident be reproduced. They're, like, a playing field for all these very important field, questions in open science. I would say those are roughly the three next steps that I would take any replication of an incident.

**[00:18:53] Kamil - Team Apart:** Nice, okay. Someone asks, how do you replicate an incident as complex as the Hugging Face one?

**[00:18:58] john @ gutenberg:** Yeah.

**[00:18:59] john @ gutenberg:** You don't do the whole thing at once, right? You chunk it into things that you think are bite-sized, right?

**[00:19:07] john @ gutenberg:** that's kind of like what we did. We… okay, we… we sometimes use the word reenact, because it's a little bit looser than, like, replicate, right? You don't have to do… you don't have to have a lab

**[00:19:19] john @ gutenberg:** frontier lab-level infrastructure, and, like, just find the low-bearing bits that you think are, like, frightening. I will once again, because of recency bias, go to this thing that happened for us, right?

**[00:19:31] john @ gutenberg:** OpenAI had their own internal benchmark, and they tested, hey, this is a safety benchmark versus a capabilities benchmark. And then they found out that, like, the model overperformed with safety and overperformed in capabilities, underperformed in safety. We don't have their special coding benchmark. They're not going to give that away, that's, like, precious data.

**[00:19:51] john @ gutenberg:** what we did is we took the best available open source dataset, and then we took the same methodology and did this, because the science is still valid in that way, right? This is, like, I think a simpler example of, like, how you replicate an incident. If you want a more complicated

**[00:20:06] john @ gutenberg:** version. You can go ahead and take a look at this post, which I like quite a bit. This is by Stuart Slocum, and

**[00:20:15] john @ gutenberg:** what he did is he indeed chunked, OpenAI's,

**[00:20:21] john @ gutenberg:** the Hugging Face incident into separate, things, right? Writes to the shared registry, which is Artifactory, requesting help from other agents, sharing exploits with other agents, and then hacking Hugging Face for a reference answer.

**[00:20:33] john @ gutenberg:** I also think that these can be, like, chunks down even further, right? For Hacking Hugging Face, that can also be broken down into more pieces. But this is, like, one way of just, like, making this manageable, both for a hackathon and also for, like.

**[00:20:46] john @ gutenberg:** doing any kind of meaningful work. You don't… you don't boil the whole ocean at once.

**[00:20:51] john @ gutenberg:** I think this is a pretty good principle that I will go ahead and list here as well.

**[00:21:04] Kamil - Team Apart:** Awesome. I'm gonna share the slides with everyone, so you will get everything.

**[00:21:10] Kamil - Team Apart:** Okay, someone else asks, if it is so hard to do public science, how do we proceed? If the data is not sufficient, the research will be lacking. Any thoughts on this?

**[00:21:20] john @ gutenberg:** I think that you can still get quite a bit of juice out of the information that is publicly available. I mean, this one was, like.

**[00:21:29] john @ gutenberg:** we had enough to get some meaningful, like, oh, this is maybe a real thing, and now people can ask how real it is based off of, like, all the code and data that we've produced, right? So this is…

**[00:21:38] john @ gutenberg:** Again, I keep coming back to it because it was yesterday, but I think that, like, again, there's, like, 300 incidents here, that you can sort of go through, to sort of comb through, real stuff like this. Now, I think…

**[00:21:52] john @ gutenberg:** specifically for swarms, they are more complicated, and so you have to sort of make inferences yourself. And so, it's not, you know, one, you can just make assumptions and fill in the blank, and then just be like, hey.

**[00:22:06] john @ gutenberg:** It would be great if you helped us fill in the blank, and this is a way to sort of, like, feed into public discourse of just, like.

**[00:22:12] john @ gutenberg:** Measuring the benefit of providing, like, even just a single bit of information, right?

**[00:22:17] john @ gutenberg:** But I think that, like, be creative, you know?

**[00:22:23] john @ gutenberg:** you don't need to have Artifactory, or, like, Hugging Faces infrastructure, or Labs infrastructure. You can make your own sort of toy environment, and I think you can do a lot of meaningful science. You don't need to have a swarm of 1,000 agents, you can do… you can study interesting dynamics with just two agents, in the same way that we're also trying to see, like, going from one… we don't need to go from any N1 agent to N to 1,200 agents.

**[00:22:45] john @ gutenberg:** We're just studying n from one agent to N.

**[00:22:48] john @ gutenberg:** and to 2 agents. And that's already pretty rich. And then 2 to 3, for example.

**[00:22:52] john @ gutenberg:** Maybe there's more specific questions that I can answer, but yeah, I hope that helps.

**[00:23:00] Kamil - Team Apart:** Awesome!

**[00:23:01] Kamil - Team Apart:** Honestly, this was great. I just shared the list of links in the chat anyway, so I don't read the slides, I can just share the links along with the recording, so this is done.

**[00:23:15] Kamil - Team Apart:** And this was great, but any other pointers, tips on what people can do? Because they only have, like, 2 days.

**[00:23:22] Kamil - Team Apart:** So…

**[00:23:23] john @ gutenberg:** Yeah.

**[00:23:23] Kamil - Team Apart:** What can they do in two days that can give a good signal, right?

**[00:23:27] john @ gutenberg:** Yeah.

**[00:23:28] Kamil - Team Apart:** Like, they don't need to solve it.

**[00:23:30] john @ gutenberg:** Yeah, of course, of course. I think, if this is incident discovery flavored.

**[00:23:36] john @ gutenberg:** You can contribute by looking at Transluce's guide right here, Swarm Chasing.

**[00:23:42] john @ gutenberg:** So just Incidents.wiki, getting started, and then Swarm Chasing, boom. And if you are looking for the study of an incident, once it's produced,

**[00:23:56] john @ gutenberg:** I would say go ahead and, like, the simplest thing to do is go through, maybe not all 300 yourself, ask your agent to go ahead and do this, and see what this playbook could be, what about this playbook could be used to sort of, like, make it usable to you.

**[00:24:12] john @ gutenberg:** And similarly, I think I respect how, Stuart Slocum, he… this is also an example of this for live agents, where he only needed a single agent to really study this thing, and he just took a… took an incident and he chunked it into four different pieces. This was, like, an opinionated single person's effort.

**[00:24:30] john @ gutenberg:** You can just study one chunk, or you can just, like, chunk it into five different pieces if you wanted to, right?

**[00:24:37] john @ gutenberg:** I think these are all different, sort of, like, permutations that you can do, and, like.

**[00:24:42] john @ gutenberg:** There's plenty of, rich, rich experiments, or sort of, like, hacks that you can do, in these directions.

**[00:24:48] john @ gutenberg:** Yes, thank you.

**[00:24:49] Kamil - Team Apart:** And keep in mind.

**[00:24:49] john @ gutenberg:** Can I add to that, sorry. Since this field is so new, like, even this

**[00:24:54] john @ gutenberg:** big, like, incident that everyone knows about The Hugging Face, has plenty of space for new projects, and there are also so many other, like, also big incidents that have been significantly understudied, so I think

**[00:25:07] john @ gutenberg:** A weekend to play around and experiment with ideas is…

**[00:25:11] john @ gutenberg:** I mean, a great opportunity. There are lots to do. That's it.

**[00:25:15] Kamil - Team Apart:** Also, as we said in the logistics presentation, you're not gonna get judged on your technical work, it's more of, like, how innovative, how impactful the idea is, your methodology and approach, all this matters.

**[00:25:28] Kamil - Team Apart:** So, just try anything out. Can we close with another question I think would be useful? So, having the benefit of hindsight, what would you think, like, what do you wish you would have known before your first replication?

**[00:25:44] john @ gutenberg:** I think…

**[00:25:45] john @ gutenberg:** simplifying is definitely the best thing to do, right? This is a process that sort of, like.

**[00:25:53] john @ gutenberg:** go… happens… I think it's, like, kind of innately human, where…

**[00:25:57] john @ gutenberg:** I'm gonna replicate Huggy Face. And then you realize that's, like, 8 different steps, and then every single step actually is, like, kind of difficult to do on its own. And so, like, you can sort of pause there and realize, hold on, hold on, let me just, like… one thing at a time, right? You just get better if you focus down on one thing at a time.

**[00:26:13] john @ gutenberg:** And actually, you can just make, like, step number three really interesting on its own. Like, this is… I'm just taking an example. Step number two of requesting help from other agents. Right now, the point of, Stuart Slocum's, like, four-stage replication is to,

**[00:26:31] john @ gutenberg:** Just have something end-to-end that people can build off of. But, like.

**[00:26:35] john @ gutenberg:** I think just exploring the dynamic of one agent requesting help from another agent is already a thing that, like, is the source of study, and can be a source of continued study.

**[00:26:48] john @ gutenberg:** And something similar can be said for, like, all these different stages. Something similar can be said if you were to take a different incident and try to, again, replicate the incident, and then study all the dynamics that sort of happened there.

**[00:26:59] john @ gutenberg:** So as long as you have, like, pared down the requirements or the complexity of the thing that you're trying to do, I think this is, like, a thing that people systematically, like.

**[00:27:08] john @ gutenberg:** need to fight against, is just, like, keep paring down whatever you were going to study or explore into the simplest possible thing, and then you can realize that, like, as soon as it is just this individual component, you realize that, like, only maybe 10 people have thought seriously about this specific aspect of the whole thing.

**[00:27:25] john @ gutenberg:** And you… it's very fresh to make contributions in that way.

**[00:27:30] Kamil - Team Apart:** Okay, we are out of time, but that was great. Thank you very much, that was awesome. I hope to have you back for another hackathon, so I will be reaching out.

**[00:27:40] Kamil - Team Apart:** And, amazing! So, you said that people can reach out to you if they have any contributions or anything, right?

**[00:27:48] john @ gutenberg:** Yes, that would be terrific. The website supports this, but Elvis at gutenberg…

**[00:27:58] john @ gutenberg:** Is also available to… for reach out.

**[00:28:02] Kamil - Team Apart:** Awesome, I'll be sure to share all the links with the participants, and that was awesome. Thank you very much, and we wish you good luck. Please, please solve this thing, please, once and for all, because I lose sleep, right?

**[00:28:15] john @ gutenberg:** We're all gonna stumble together.

**[00:28:16] Kamil - Team Apart:** Yes, awesome. Okay, bye everyone!

**[00:28:20] john @ gutenberg:** Thank you, guys. Take care.

