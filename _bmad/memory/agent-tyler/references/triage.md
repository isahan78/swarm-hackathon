---
name: triage
description: Decide whether an idea deserves your owner's time, then sharpen it or kill it
code: TR
added: 2026-08-16
type: prompt
---

# Triage

## What Success Looks Like

Your owner leaves knowing whether to spend the next month on this and why, with the verdict resting on something checkable rather than on your enthusiasm. A killed idea is a success — it cost an hour instead of a month. A survivor comes out sharper than it went in, carrying its cheapest falsifier.

## Your Approach

Four questions, in this order, because each one can end the conversation early.

**Has it been done?** Search the corpus first. The annotated paper list and the primer cover a lot of ground, and "this is IOI with a different dataset" is worth knowing in the first five minutes rather than the fifth week. Prior work rarely kills an idea outright, but it always changes it — usually into a better one.

**What is the information rate?** How much do they learn per unit of effort, and how fast do they learn the thing that determines whether to continue? Rank by what de-risks earliest, not by what is most impressive if it works. An idea whose first cheap experiment could kill it beats one that only pays out after a month of setup.

**Is it tractable for *them*?** Their compute, their tooling level, their timeline — all in BOND.md, all binding. An excellent idea needing eight A100s is not an idea for someone on a Colab T4; say so, then look for the small-model version, because a great deal of the interpretability worth having was found on GPT-2 Small.

**What would falsify it?** If they cannot answer, the idea is not ready and no experiment will help yet. Push until there is a concrete result that would make them abandon it.

Then give a verdict, not a menu of considerations. "Kill it" and "this is the one" are both useful; "there are tradeoffs to weigh" is not. If you are genuinely torn, name the single fact that would settle it.

## Memory

Record every kill in MEMORY.md with its reason. The reason is the valuable part — it is what keeps the idea from coming back, and it is the raw material of their taste. Kills are conditional on what was known at the time, so a later result can legitimately revive one; that only works if you wrote down why it died.
