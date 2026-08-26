# The rawmktg Measurement Methodology

> One standard for every number we publish. What a prompt portfolio must contain, how many times we run it, how we bound the result, and what has to be true before a figure is called decision-grade rather than directional.

Version 1.0 &middot; effective 26 August 2026 
This is the canonical specification behind every visibility number rawmktg publishes, in articles, teardowns and the free tools. It is versioned. When it changes, the version and the changelog at the foot of this page change with it, and any figure that depends on the change is restamped. If a teardown and this page ever disagree, this page is correct.
 

Most AI-visibility numbers you will see anywhere, including screenshots in sales decks, come from a single query typed once into one engine. That is not a measurement, it is an anecdote with a timestamp. AI answers are non-deterministic: ask the same question ten times and the set of brands named changes, sometimes by fifteen points, with nothing altered on any website. A method that ignores that variance reports noise as fact. This page defines the method that does not.

 A number is only decision-grade when it would survive being measured again next week. Everything here exists to make that true. 

## What has to be in a prompt portfolio?

**A frozen, versioned set of real buyer prompts, bucketed by intent, held constant across cycles. The portfolio is the instrument. It is assembled once, version-stamped, and never quietly edited, because changing the questions between cycles makes the trend meaningless. Prompts are sorted into intent buckets so a brand that wins commercial questions but loses research questions is visible, not averaged away.**

Every prompt is a real question a buyer in the category would ask an assistant, phrased the way a person phrases it, not a keyword. Prompts are split into three buckets, commercial (best, top, alternatives), research (how, what, comparison), and brand (named-entity checks). Each bucket carries a weight, because an appearance in a high-intent commercial answer is worth more than one in a definitional aside. The portfolio is stored with a version tag such as v2026.08 and frozen for the life of that version, so every cycle measures the same instrument.

 Table 1. Portfolio tiers. The tier sets the width of the question set, not the statistical rigour, which is fixed in section 2. Tier Prompts What it answers Confidence Baseline / diagnostic 50 to 150 A fast read: are we present at all, and where are the obvious holes Directional, not for board slides Decision-grade / standard 250 to 500 The default. Share and trend you can act on and defend Roughly a plus or minus 2-point margin Enterprise / category 500+ Full category coverage, per-segment and per-region breakouts Tight intervals on sub-segments 

Different rawmktg articles run different tiers on purpose. The prompt-to-citation baseline starts at 50 to 150 because it is a 30-day diagnostic; the Share of Model spec runs 250 to 500 because it is decision-grade. Those are not contradictions, they are named tiers of the same method. What never changes between them is the run count.

## How many times is each prompt run?

**Eight to twelve times per prompt per engine. The default is ten. This is fixed at every tier. Portfolio width is a scope choice; run count is not. Because a single response is a coin flip, each prompt is issued 8 to 12 times to every engine and the results are averaged, which is what turns a set of anecdotes into an inclusion rate with a real interval around it. Fewer than eight runs and the interval is too wide to act on.**

Ten runs is the working default. Below eight, cycle-to-cycle swings are dominated by sampling noise rather than real change, which is how a brand appears to gain or lose fifteen points in a month with no work done. This is the single parameter that must be identical everywhere, and it is the one earlier drafts were loosest about. A baseline diagnostic may use a narrow portfolio, but it still runs each prompt the full eight-to-twelve times, otherwise it is not a baseline, it is a guess.

 The rule that overrides the others 
If you take one number from this page, take this: 8 to 12 runs per prompt per engine, default 10, at every tier and in every article. A wide portfolio run once is worse than a narrow portfolio run ten times.
 

## Which engines count, and how are they weighted?

**Each engine is measured and reported separately, then combined with evidence-based weights, never averaged blind. ChatGPT Search, Google AI Overviews, Perplexity, Copilot and Gemini cite different sources for the same question, so a blended single number hides where you are winning. Engines are weighted by audience reach and citation behaviour, and every headline figure ships with its per-engine breakdown.**

The engines diverge enough that optimising for one does little for another, which is why cross-engine source overlap is low and why the report keeps them apart. Weights reflect reach and how much each engine actually influences a buyer, and they live in the versioned config so a weight change is a version change. The composite is only ever presented alongside the per-engine rows it is built from.

## How is a number bounded and guarded?

**Every rate carries a Wilson interval, trends use response-level bootstrap, and no cell is reported below 200 observations. A point estimate with no interval invites over-reading. Inclusion rates are reported with 95% Wilson intervals; period-over-period changes are tested with a response-level bootstrap so a move is only called real when it clears the noise band; and any brand-engine cell with fewer than 200 observations is withheld rather than shown.**

 formula &middot; Share of Model SoM(b) = Σ_e Σ_p w_e · w_p · score(b,e,p) ÷ Σ over every brand in the field

 b brand score 0.30 mention + 0.30 recommendation
 e engine + 0.20 position + 0.15 sentiment + 0.05 prominence
 p prompt w_e, w_p engine and prompt-bucket weights
 Share of Model is a share of the whole field, not a raw inclusion rate. 
 formula &middot; observations for a target margin n = z^2 · p(1-p) / e^2 # observations per brand per engine

 z = 1.96 (95%) p = expected inclusion rate e = target margin
 For p = 0.30 and e = 0.02, n ~ 2,000 observations.
 At 10 runs per prompt that is ~200 prompts per engine cell. 

The sample maths is why decision-grade lands at 250 to 500 prompts: at a 30% base rate and a plus or minus 2-point target, you need roughly 2,000 observations per engine, which at ten runs is about 200 prompts per engine cell. You can size any target yourself with the sample-size and confidence planner . The 200-observation floor is enforced in the query, not left to judgement.

 sql &middot; the per-cell sample-size guard -- No cell is reported until it clears the sample floor.
SELECT brand_id, engine, AVG(present) AS inclusion
FROM observations
WHERE portfolio_version = 'v2026.08'
GROUP BY brand_id, engine
HAVING COUNT(*) >= 200; -- under-sampled cells are withheld, not shown 

## How often is it re-run, and what makes a figure decision-grade?

**Monthly on a frozen portfolio, restamped on every version change. Decision-grade requires the standard tier, full runs, and a passing sample guard. Cadence is monthly so trend outpaces noise without burning tokens. A figure earns the decision-grade label only when it is measured on a 250-plus prompt portfolio, at 8 to 12 runs, with every reported cell clearing 200 observations. Anything short of that is published as directional and labelled as such.**

The distinction is a labelling rule, not a soft preference. Directional numbers, from a baseline portfolio, are allowed and useful, but they are never dressed up as decision-grade, and they never appear without the word. Declared inputs that cannot be measured, whether a brand publishes original research, has named expert quotes, runs an aged and authentic community account, are kept in a visibly separate declared section with an asserted, not measured label, and are never folded silently into a measured composite.

## What changes, and how do you know it changed?

**Every change to a parameter, weight or portfolio version is recorded here with a date. Versioning is the trust mechanism. A methodology that can be edited invisibly is worth nothing, so every change to a weight, a threshold, a run default or a portfolio version is logged below with the date it took effect and what it affected.**

 Changelog Version Date Change v1.0 26 Aug 2026 Initial published standard. Fixes the run count at 8 to 12 (default 10) across all tiers and articles; defines the baseline / decision-grade / enterprise portfolio tiers; sets the 200-observation per-cell reporting floor. 
 
## Frequently asked questions
 
### How many prompts should an AI-visibility measurement use?
 
It depends on what the number is for, and rawmktg uses three named tiers. A baseline diagnostic uses 50 to 150 prompts and is directional. A decision-grade programme, the default, uses 250 to 500 prompts, which at ten runs per prompt gives roughly a plus or minus 2-point margin. Enterprise or full-category work uses 500 or more. The tier sets how wide the question set is; it does not change the run count, which is fixed.
 
### How many times should you run each prompt?
 
Eight to twelve times per prompt per engine, with ten as the default, at every tier. AI answers are non-deterministic, so a single response is a coin flip. Averaging 8 to 12 runs is what converts anecdotes into an inclusion rate with a usable confidence interval. Below eight runs, month-to-month swings are dominated by sampling noise rather than real change.
 
### Why not just average all the engines into one score?
 
Because ChatGPT Search, Google AI Overviews, Perplexity, Copilot and Gemini cite different sources for the same question, so a blended number hides where you are winning and losing. rawmktg measures and reports each engine separately, then combines them with evidence-based weights held in a versioned config, and always shows the per-engine breakdown behind any composite.
 
### What makes a number decision-grade rather than directional?
 
Three things together: a portfolio of at least 250 prompts, 8 to 12 runs per prompt per engine, and every reported brand-engine cell clearing 200 observations. If any of the three is missing, the figure is published as directional and labelled that way. Declared inputs that cannot be measured are kept in a separate section and never folded into a measured score.
 
### Why is this methodology versioned?
 
So it cannot be edited invisibly. A method that can change without a record is not a standard. Every change to a weight, threshold, run default or portfolio version is logged in the changelog on this page with its effective date, and any published figure that depends on the change is restamped.
 
 Where this method is applied 
Read the full spec and worked example in Share of Model, measured properly . Size your own sample with the sample-size and confidence planner . See the baseline version in prompt-to-citation tracking , and the metric taxonomy in citation vs mention vs recommendation .
 
 About rawmktg. 
rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

*Source: https://rawmktg.com/methodology · rawmktg. by Vinayak Ravi*