# Share of Model: How to Actually Measure It

> Share of Model gets quoted in every AI-visibility deck and defined in almost none of them. This is the formula, the sample size that makes it stable, and the benchmark bands that tell you whether your number is good or embarrassing.

*Source: https://rawmktg.com/blogs/share-of-model-measurement · rawmktg. by Vinayak Ravi*


Most teams find out about their AI visibility the same way. Someone on the exec team types the category question into ChatGPT, does not see the company, and forwards the screenshot to marketing. That screenshot is not data. It is one draw from a probability distribution, and the next person to type the same question will get a different answer.

The standard behind these numbers

This article is the worked spec. The one-page, versioned standard every rawmktg figure follows lives at the [measurement methodology](/methodology).

Share of Model is the metric that replaces the screenshot. It answers one question with one number: across the questions your buyers actually ask, in the engines they actually use, how much of the answer space do you own compared to everyone else selling into the same problem. This piece is the methodology, not the taxonomy and not the attribution plumbing, just the metric, how to compute it, how big a sample it needs, and how to read the result. A single number can still hide which buying stage is missing, which is why a [segment teardown reports four measures, not one](/blogs/clean-site-zero-citations).

A single measurement is a screenshot. Two comparable measurements are a program.

The short version

Share of Model = your weighted presence divided by the total weighted presence of every brand in the category, computed over the same prompt portfolio, on the same engines, on a fixed cadence.

What makes it hard is not the mathematics, it is the discipline: a fixed portfolio, enough runs, honest weights, and the willingness to publish a number lower than the one your tool vendor reports.

## 01. How do the three AI-visibility metrics differ?

**Taxonomy defines the event, Share of Model scores it, attribution follows it.** Three measurement problems get confused, and each has a different fix. What counts is a taxonomy question. Whether an appearance produced a session is an attribution question. Share of Model is the middle layer that counts the defined events across a fixed prompt set and turns them into one share.

Before you can count anything, you have to decide what counts. A brand name in a paragraph, a URL in a footnote, and a brand named as the recommendation are three different events with three different causes, the distinction drawn in [citation vs mention vs recommendation](/blogs/citation-vs-mention-vs-recommendation), and it is upstream of everything here. Once you know a brand appeared, you still need to know whether that answer produced a session or a deal, a plumbing problem covered in [prompt-to-citation tracking](/blogs/prompt-to-citation-tracking). Share of Model sits between them: it is a scoreboard, not a diagnosis and not a revenue model.

Taxonomy

Defines the event: mention vs citation vs recommendation.

→

Share of Model

Scores the event across a fixed prompt portfolio.

→

Attribution

Follows it downstream to sessions, signups, pipeline.

Figure 1. Where Share of Model sits. The taxonomy defines the event, the metric scores it, attribution follows it downstream.

Table 1. Legacy visibility metrics and the assumption each one breaks on.

| Metric | What it counts | Unit | Fails when |
| --- | --- | --- | --- |
| Share of Voice | Media impressions and paid reach | Impressions | Buyers stop seeing media and start asking a model |
| Share of Search | Branded query volume in Google | Search volume | The query never reaches Google because the answer arrived first |
| Rank tracking | Position on a static results page | Position 1 to 100 | There is no page, only a synthesized paragraph |
| Share of Model | Weighted brand presence in generated answers | Percent of answer space | The prompt set is too small or unweighted |

The last row is the whole argument. Generative outputs are probabilistic, so the correct unit of measurement is a share of a distribution, not a position on a list.

## 02. What does Share of Model actually measure?

**Weighted brand presence across a representative, multi-engine prompt set.** Three parts do the work: a statistically representative and versioned prompt portfolio, coverage across multiple engines that retrieve differently, and weighting by commercial intent so a definition is not worth the same as a shortlist.

A **statistically representative set** is a fixed portfolio, versioned and re-run identically each cycle, covering the range of ways a buyer actually phrases the problem. If the portfolio changes between cycles, the trend line is meaningless. **Across multiple engines** matters because ChatGPT, Perplexity, Google AI Overviews, Claude and Grok retrieve, and therefore recommend, differently, the reason set out in [why different engines recommend different vendors](/blogs/why-engines-recommend-different-vendors); a blended single number hides the fact that you might own one engine and be invisible in another.

**Weighted by intent** is the part most tools skip. A brand named in answer to "what is workforce management software" and a brand named in answer to "which workforce management platform handles multi-state overtime compliance under $12 per employee" are not worth the same. One is a definition. The other is a shortlist that ends in a purchase order.

## 03. Why does the naive inclusion-rate formula lie to you?

**It treats a footnote like a recommendation, every engine as equal, and every question as equal.** The unweighted inclusion rate, brand appearances divided by scored responses, is clean, reproducible and wrong in three ways. The practical consequence is rank inversion: two brands can swap places entirely once weighting is applied.

Nearly every tool that reports an AI-visibility score starts with the unweighted inclusion rate: the number of responses in which the brand appears anywhere, divided by the total scored responses. Show up in 620 of 2,000 answers and you score 31%. It treats a fourth-alternative caveat mention identically to being named the single best option; it treats a Grok mention the same as an enterprise-procurement ChatGPT mention; and it rewards you for winning cheap definitional prompts that are worth almost nothing.

Figure 2. Rank inversion. Brand A wins on raw volume and loses on every dimension that maps to revenue once weighting is applied.

Brand A is winning the definitional long tail and appearing late in lists. Brand B appears less often but appears first, in comparison and constraint prompts, in the engines its buyers use. A raw count says Brand A leads by seven points; the weighted score says Brand B leads by nineteen. Only one of those conclusions would survive contact with the pipeline, which is the same gap between [ranking and visibility](/blogs/ranking-isnt-visibility).

## 04. What is the formula that holds up?

**Weighted presence over total weighted field presence, adjusted for engine and intent.** For every engine and every prompt, take your presence score, multiply by the engine weight and the intent weight, and sum. Divide by the same sum across every brand in the competitive set. Engine weights sum to one so the score stays interpretable.

formula · weighted Share of Model

```
SoM(b) =    Σ_e  Σ_p   w_e · w_p · score(b, e, p)
           -----------------------------------------
           Σ_{b' in C}  Σ_e  Σ_p   w_e · w_p · score(b', e, p)

  w_e     engine weight, Σ w_e = 1   (where your buyers ask)
  w_p     intent weight, 0.5x .. 2.0x (distance from purchase)
  score   presence in [0,1], averaged over N runs of the prompt
  C       the competitive set (the denominator is field presence,
          not response count, that is what makes it a share)
```

### Setting the engine weights

Engine weight is a business decision, not a statistical one: it reflects where your buyers ask, not global market share. A B2B infrastructure vendor selling to platform engineers weights Perplexity and Claude higher; a mid-market SaaS company selling to operations leaders weights ChatGPT and Google AI Overviews heavily. Set the weights once, document the reasoning, and do not change them mid-year. If you must revise them, restate prior periods on the new weights so the trend stays honest.

### Setting the intent weights

Intent weight scales with distance from a purchase decision. A workable default we use across teardowns:

Table 2. Default intent weights. Tune the multipliers to your sales cycle, then freeze them.

| Intent tier | Weight | What the prompt is doing | Example |
| --- | --- | --- | --- |
| Navigational & entity | 0.5x | Testing whether the model knows you exist and describes you correctly | What is Acme, and what does it do? |
| Category discovery | 1.0x | Unbranded category ask, no vendor named | Best workforce management platforms for multi-site healthcare |
| Comparative & evaluation | 1.5x | Head-to-head, pros and cons, shortlist construction | Compare Acme and Beta for compliance tracking |
| Transactional & constraint | 2.0x | Hard budget, integration or regulatory constraints attached | HRIS under $15 per employee with Slack and SOC 2 Type II |

The gap between 0.5 and 2.0 is deliberate. It is the difference between a model knowing your name and a model putting you on a shortlist while the buyer has a budget open. Brands that only optimize the top of that table build [an authority position with no demand attached](/blogs/authority-isnt-demand).

Free Tool · Calculator

Compute your Share of Model

The weighted formula above, made live. Enter per-engine mention and prompt counts for a visibility score, then add field mentions to get your Share of Model, your share of the whole competitive field.

Enter your tracking counts per engine

Leave an engine blank to exclude it, the score renormalises across the engines you actually track. Default weights are market-share estimates; edit them for your market. "Field mentions" is optional, the total brand-mentions across every vendor in the same responses; fill it to also get your Share of Model.

ChatGPT

Mentioned

Prompts issued

Weight

Field mentions (all vendors)

Gemini

Mentioned

Prompts issued

Weight

Field mentions (all vendors)

Perplexity

Mentioned

Prompts issued

Weight

Field mentions (all vendors)

Claude

Mentioned

Prompts issued

Weight

Field mentions (all vendors)

Grok

Mentioned

Prompts issued

Weight

Field mentions (all vendors)

Platform-weighted visibility

0%

Enter counts

Per-engine visibility

Share of Model , share of the field

–%

Add "field mentions" per engine to compute your weighted share of the whole competitive field.

## 05. How do you score a single response?

**A composite of five dimensions between 0.0 and 1.0, averaged over the runs.** Presence is not a one or a zero. It is mention inclusion, recommendation endorsement, position prominence, sentiment and entity accuracy, weighted so the first two carry 60% because recommendation is what moves pipeline.

Table 3. The five presence dimensions and their default weights.

| Dimension | Symbol | Weight | What it captures |
| --- | --- | --- | --- |
| Mention inclusion | m | 0.30 | Is the brand named or cited anywhere in the response. Binary. |
| Recommendation endorsement | d | 0.30 | Presented as a pick rather than a passing reference. Active endorsements carry 3-5x the value of a co-mention. |
| Position prominence | rho | 0.20 | Where in the answer hierarchy the brand lands. Graded, not binary. |
| Sentiment polarity | s | 0.15 | Positive framing scores 1.0, neutral 0.6, negative 0.0. |
| Entity accuracy | a | 0.05 | Are the stated features, pricing and positioning correct. Catches hallucination. |

Figure 4. Default dimension weights. The first two carry 60% because recommendation is the outcome that moves pipeline.

Position prominence needs a ladder rather than a raw rank, because the drop-off is not linear, being named first is worth far more than twice being named second. Entity accuracy carries the smallest weight but the largest downside: a brand can score well on inclusion and still be harmed if the model consistently misstates its pricing tier, so track it as a separate alarm, not just a 5% input. The structural fix is in [hallucination-proofing your brand](/blogs/hallucination-proofing-your-brand).

python · presence score for one brand, one prompt, one engine

```
from dataclasses import dataclass

POSITION_WEIGHTS = {1: 1.00, 2: 0.70, 3: 0.70, 4: 0.40, 5: 0.40, 6: 0.40}
TAIL_WEIGHT      = 0.15
SENTIMENT        = {"positive": 1.0, "neutral": 0.6, "negative": 0.0}
DIM_WEIGHTS      = {"m": 0.30, "d": 0.30, "rho": 0.20, "s": 0.15, "a": 0.05}

@dataclass
class Extraction:
    rank: int; mentioned: int; recommended: int
    sentiment: str; entity_accurate: int

def presence(x):
    rho = POSITION_WEIGHTS.get(x.rank, TAIL_WEIGHT)
    return (DIM_WEIGHTS["m"]   * x.mentioned
          + DIM_WEIGHTS["d"]   * x.recommended
          + DIM_WEIGHTS["rho"] * rho
          + DIM_WEIGHTS["s"]   * SENTIMENT[x.sentiment]
          + DIM_WEIGHTS["a"]   * x.entity_accurate)

# average presence() over the N runs of the prompt. keep the weights
# in config, not in code, so a weighting change is auditable.
```

Extraction is the part people underestimate. Brand names get truncated, pluralized and abbreviated inside generated prose. Build an alias table per brand before you run anything, and validate your extractor against a hand-labelled sample of at least 200 responses before you trust a single score.

## 06. How many runs per prompt do you actually need?

**Eight to twelve, because one run is a coin flip recorded as a fact.** The failure that invalidates most AI-visibility reporting is running each prompt once and reporting the result as a rate. The same prompt sent twice returns different brand sets; the estimate only settles around eight to twelve runs per prompt per engine.

Figure 5. A single prompt with a true inclusion rate of 27%, estimated run by run. Before roughly run 8 the estimate is noise.

At one run your estimate is either 0% or 100%. At three runs it can still be off by 30 points. Somewhere around eight to twelve runs per prompt per engine, the estimate settles into a range you can act on. Perplexity and Google AI Overviews are especially unstable because they re-retrieve on every call.

### Bounding the estimate

Report intervals, not point estimates. For simple presence proportions use a Wilson score interval rather than the normal approximation, which breaks badly at the low rates most brands actually have.

python · Wilson 95% confidence interval

```
import math

def wilson(successes, n, z=1.96):
    """95% CI for a proportion. Correct at small n and extreme p,
    where the normal approximation breaks badly."""
    if n == 0:
        return (0.0, 0.0)
    p      = successes / n
    denom  = 1 + z*z / n
    centre = (p + z*z / (2*n)) / denom
    margin = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return (centre - margin, centre + margin)   # use for inclusion rates
```

The weighted Share of Model composite is not a simple proportion, and mentions cluster inside multi-brand responses, which violates the independence Wilson assumes. For the composite, resample at the response level with a percentile bootstrap.

python · response-level bootstrap for the composite

```
import numpy as np

def bootstrap_som(responses, brand, n_iter=1000, seed=7):
    """Percentile bootstrap CI for the weighted composite. Resample
    whole responses, not individual mentions, so within-response
    correlation (brands cluster inside multi-brand answers) survives."""
    rng = np.random.default_rng(seed)
    idx = np.arange(len(responses))
    est = []
    for _ in range(n_iter):
        sample = [responses[i] for i in rng.choice(idx, len(idx))]
        est.append(weighted_som(sample, brand, ENGINE_W, INTENT_W))
    return tuple(np.percentile(est, [2.5, 97.5]))  # <1000 iters = unstable tails
```

## 07. How many prompts do you need?

**Enough for about 1,900 observations per brand per engine, then stop.** Work backwards from the precision you need. To hold a two-point margin at a 27% rate you need roughly 1,900 scored observations per brand per engine, which at ten runs is about 190 prompts. A 250 to 500 prompt portfolio is where decision-grade programmes land.

formula · observations required for a ±2 point margin

```
n = z² · p(1 - p) / E²

  z = 1.96  (95% confidence)
  p = 0.27  (observed inclusion rate)
  E = 0.02  (target margin of error, ±2 points)

  ->  n ≈ 1,896 scored observations, per brand, per engine
  at 10 runs/prompt that is ≈ 190 prompts; round up to a
  250 to 500 prompt portfolio, run 5 to 12 times per engine.
```

Figure 6. Confidence-interval width against total observations. The curve flattens hard after about 2,500.

The flattening matters more than the absolute numbers. Going from 500 to 2,500 observations buys a large precision gain; going from 2,500 to 5,000 buys very little. That is the argument for a 250-prompt portfolio rather than a 500-prompt one if budget is tight, spend the saved API calls on more engines instead.

Directional versus decision-grade

A 50 to 100 prompt audit is fine for a first look and for finding obvious gaps. It is not enough to declare a winner between two brands sitting three points apart, and it is not enough to claim a quarter-over-quarter improvement. Say which one you are doing.

Free Tool · Calculator

Plan your sample size

How many runs and prompts you need for a number you can trust, plus a Wilson confidence interval for a rate you have already measured.

Plan the sample

Expected inclusion rate (%)

Target margin of error (± points)

Confidence (90 / 95 / 99)

Runs per prompt per engine

n = z² · p(1-p) / E². Runs convert observations into a prompt count. Engines that re-retrieve on every call (Perplexity, Google AI Overviews) need the top of the 8-12 run range.

Bound an observed rate (Wilson)

Times the brand appeared

Total scored responses

The Wilson score interval is correct at the low rates most brands actually have, where the normal approximation breaks badly.

Observations needed

0obs

per brand, per engine

The plan

Your prompt count appears here.

Wilson 95% interval

–

Enter appearances and total responses to bound the rate.

## 08. Why can't you blend the engines into one number?

**Retrieval architecture drives variance, and variance drives your run budget.** Blending everything into one number is the second most common mistake after under-sampling. Report each engine separately, then weight into the headline, because the per-engine cut is where the fix lives.

Table 4. Per-engine execution configuration. Report each engine separately, then weight into the headline number.

| Engine | Primary retrieval | Variance | Min runs | Best intent fit |
| --- | --- | --- | --- | --- |
| ChatGPT | Hybrid parametric plus web RAG | Moderate | 10 | Broad commercial and B2B discovery |
| Perplexity | Live web RAG indexing | High | 12 | Deep technical and research queries |
| Google AI Overviews | Search graph plus Gemini | High | 10 | High-volume consumer and business search |
| Claude | Parametric-heavy, extended context | Low to moderate | 8 | Long-form analysis and enterprise evaluation |
| Grok | Real-time social plus web RAG | High | 12 | Real-time trends and industry news |

A brand strong on Claude and weak on Perplexity has a live-retrieval problem: the training corpus knows it, the live index does not. That is a crawlability and freshness fix, not a brand fix, and the mechanics are in [how your page gets retrieved](/blogs/how-your-page-gets-retrieved).

## 09. How do you build the prompt portfolio?

**From how buyers describe situations, not from a keyword list.** The portfolio is the measurement instrument. Keyword lists are what people type into a search box; buyers describe a situation to an assistant, their headcount, their stack, their compliance constraint. Most of those phrasings have zero search volume.

Most buyer phrasings have zero search volume, which is exactly why the [query fan-out mechanics](/blogs/query-fan-out-how-one-prompt-becomes-ten-searches) matter here. A workable split is 15% navigational, 35% category discovery, 30% comparative and 20% transactional. Discovery gets the largest share because it is where the category conversation happens; transactional gets the highest weight because it is where the money is.

Figure 8. Portfolio allocation by volume. Discovery and comparison prompts carry the bulk of the volume; constraint prompts carry the bulk of the weight.

yaml · the versioned portfolio file

```
# portfolio.yaml -- version this file. It IS the measurement instrument.
version: 2026.Q3.1
category: field_service_management
competitor_set: [acme, beta, gamma, delta, epsilon, zeta]

engine_weights:              # must sum to 1.0 -- where your buyers ask
  chatgpt:      0.38
  ai_overviews: 0.24
  perplexity:   0.18
  claude:       0.12
  grok:         0.08

intent_weights: {navigational: 0.5, discovery: 1.0,
                 comparative: 1.5, transactional: 2.0}

prompts:
  - {id: fsm-disc-001, tier: discovery,     text: "best field service software for HVAC"}
  - {id: fsm-comp-014, tier: comparative,   text: "ServiceTitan vs Housecall Pro for a 40-tech shop"}
  - {id: fsm-txn-031,  tier: transactional, text: "FSM under $80/tech/mo with QuickBooks + SOC 2"}
```

Three rules keep the instrument honest. Never edit a prompt in place, deprecate it and add a new ID. Never add prompts mid-cycle, batch them into the next version. Always keep at least 80% of prompts stable across versions so the trend line survives.

## 10. What does the measurement pipeline look like?

**Nine stages on a fixed cadence, with the portfolio frozen and every raw response stored.** Run monthly for an active programme, quarterly for maintenance. The denominator is total field presence, not response count. Store every raw response, not just the extraction, because scoring logic and alias tables improve and re-scoring history is cheap.

Frozen portfolio

250-500 prompts, versioned, unchanged.

→

Poll engines

8-12 runs per prompt per engine.

→

Extract + score

Alias table, five presence dimensions.

→

Aggregate to field share

Denominator = total field presence.

→

Report + CI

Blended headline plus per-engine cut, then backlog.

Figure 9. The full loop. The last stage feeds the content backlog; stage one stays frozen so the next cycle is comparable.

python · the weighted Share of Model rollup

```
from collections import defaultdict

def weighted_som(responses, brand, engine_w, intent_w):
    """responses: iterable of scored responses across the portfolio."""
    num = den = 0.0
    for r in responses:
        w    = engine_w[r.engine] * intent_w[r.tier]
        num += w * r.scores.get(brand, 0.0)
        den += w * sum(r.scores.values())   # total field presence
    return num / den if den else 0.0        # a share, not a rate
```

Storage is cheaper than execution by two orders of magnitude, so keep the full text of every response, not the extraction. And the rollup query's guard clause is not optional: under-sampled cells are the main source of fake movement.

sql · cycle-over-cycle rollup with an under-sampling guard

```
-- Cycle-over-cycle movement, ready for the dashboard.
WITH scored AS (
  SELECT cycle_id, engine, tier, brand,
         engine_weight * intent_weight * presence_score AS w_score,
         engine_weight * intent_weight * field_score    AS w_field
  FROM   response_scores
  WHERE  portfolio_version = '2026.Q3.1'
)
SELECT cycle_id,
       SUM(w_score) / NULLIF(SUM(w_field), 0) AS share_of_model,
       COUNT(*)                               AS observations
FROM   scored
GROUP  BY cycle_id
HAVING COUNT(*) >= 200;   -- the HAVING is not optional: under-sampled
                          -- cells are the main source of fake movement.
```

## 11. What does a good Share of Model score look like?

**It depends on the vertical, and most first measurements land in the bottom two tiers.** A score means nothing in isolation. 18% is excellent in a fragmented market with forty vendors and poor in a consolidated one with four. Across verticals, brands land in four consistent tiers, and benchmarks come from teardowns of the actual competitive set.

Figure 11. Share of Model benchmark bands by vertical and competitive tier (band midpoints). Read your number against the band for your tier.

Table 5. Benchmark Share of Model ranges by vertical. The right-hand column is where the gap gets closed.

| Vertical | Category leader | Strong challenger | Emerging provider | What drives retrieval |
| --- | --- | --- | --- | --- |
| HR tech & staffing | 35-45% | 18-30% | 5-15% | Directory reviews (G2, Capterra), community forums, pricing pages |
| AEC services & tech | 32-42% | 15-28% | 4-12% | Technical specs, trade association journals, Schema.org entities |
| Field service management | 38-48% | 20-32% | 5-14% | Feature comparison tables, integration guides, industry reviews |
| Carbon accounting | 35-45% | 16-28% | 3-12% | Methodological papers, GHG Protocol citations, regulatory briefs |

Three things to read out of that table. Field service runs highest at the top because it is the most consolidated, so the leader's denominator is smaller, the full breakdown is in the [field service software teardown](/blogs/field-service-software-ai-visibility-gap). Carbon accounting runs lowest because the category rewards methodological credibility over marketing volume, which a new entrant cannot buy quickly, we took that market apart in [authority isn't the moat](/blogs/authority-isnt-the-moat). And the retrieval-driver column is the actionable one: optimizing an AEC site with HR-tech tactics produces nothing.

The tier that surprises people is the bottom one. In our lending and credit teardown, 44 of 52 brands were named 0% of the time. Not low, zero, a large fraction of a well-funded category sitting entirely outside the answer space. Movement is slower than teams expect: set expectations at three to five points per quarter for a brand in the emerging tier doing the work consistently.

## 12. How do you connect model share to money?

**Stack five layers under it, then size the gap for the CFO.** Share of Model on its own is a marketing metric. To survive a budget conversation it connects to pipeline through a citation-source split, mention quality, an authority-gap map, AI-referral attribution and agentic web logs.

01 Share of Model + rank

The weighted score and your ordinal position.

→

02 Citation-source split

Owned / earned / community. Own-domain-only is fragile.

→

03 Mention quality

Sentiment, attribute association, hallucination rate.

→

04 Authority-gap map

Third-party domains you are absent from = outreach list.

→

05 AI-referral attribution

Sessions from AI engines vs branded-search lift.

Figure 12. The measurement stack. Layer 01 is the number; everything above it explains why the number moved.

The authority-gap map, the third-party domains engines cite for your category where you are absent, is your outreach target list, and the method is in [authority seeding for AI](/blogs/authority-seeding-ai-llm-trust). Two formulas carry the budget conversation. Return on GEO connects spend to tracked revenue plus a conservatively attributed brand-lift term, and cost of inaction quantifies the gap to the leader as forgone pipeline.

A worked cost-of-inaction estimate

A field service platform running at 14% against a leader at 38%, in a category generating an estimated 120,000 relevant prompts a year, converting AI-sourced exposure at 1.4% into opportunities worth an average of $18,000. The 24-point gap maps to 28,800 answers, which maps to roughly $7.26 million in annual pipeline that goes to someone else.

Be honest about what that number is: a sizing estimate built on a conversion assumption you should state explicitly, not a forecast. Its job is to make the gap legible to a CFO, not to be booked.

## 13. How do you stand the program up in 90 days?

**Measurement infrastructure before optimization work, always.** The first score lands on day 14 and it will be worse than expected. Check crawler behaviour before the authority work, or the placements you earn will feed engines that still cannot retrieve your site.

Table 6. A 90-day implementation sequence.

| Stage | Focus | Deliverables |
| --- | --- | --- |
| Days 1-14 | Baseline audit | Curate the 250+ prompt portfolio, run first sampling across five engines, map competitor Share of Model |
| Days 15-30 | Machine scannability | llms.txt at root, clean Markdown variants, Schema.org markup, verify bot access in robots.txt |
| Days 31-60 | Citation-gap acquisition | Targeted PR and placement on the high-citation third-party domains from authority mapping |
| Days 61-75 | Pipeline attribution | GA4 referral tracking for AI engines, dashboard combining Share of Model and referral conversions |
| Days 76-90 | Operational cadence | Automated monthly polling, variance alerts, Share of Model in the quarterly review |

Days 15 to 30 come before the authority work for a reason: if the crawlers cannot parse your pages, the placements you earn in days 31 to 60 will feed engines that still cannot retrieve your site, and you will pay for coverage that only helps your competitors' answers look better sourced. Check crawler behaviour first, using the breakdown in [how AI crawlers actually index your site](/blogs/how-ai-crawlers-index-your-site).

## 14. What are the seven ways the number goes wrong?

**Under-sampling, drift, blending, alias misses, weight tinkering, thin cells and denominator confusion.** Most bad Share of Model reporting traces to one of seven failure modes. The most damaging is weight tinkering, because it is invisible outside the measurement team and manufactures good news on demand.

Table 7. The seven failure modes that account for most bad Share of Model reporting.

| Failure | What it looks like | Fix |
| --- | --- | --- |
| Single-run sampling | Score swings 15 points between cycles with no work done | 8 to 12 runs per prompt per engine, minimum |
| Portfolio drift | Prompts edited or added between cycles | Version the portfolio file, keep 80% stable, deprecate rather than edit |
| Blended-only reporting | One number that hides an engine you are invisible in | Always publish the per-engine cut alongside the headline |
| Alias misses | Extractor misses abbreviations and truncations of the brand | Alias table per brand, validated against 200 hand-labelled responses |
| Weight tinkering | Score improves after a weighting change, not after work | Freeze weights for the year, restate history if you must revise |
| Under-sampled cells | A tier or engine with 40 observations reported as a trend | Suppress cells below a minimum observation count |
| Denominator confusion | Reporting a rate and calling it a share | Denominator is total field presence across the competitor set, not response count |

If your weights change, the previous quarter has to be restated on the new weights before anyone sees a trend line. Write that into the process document.

## 15. What should you do this week?

**Run a 50-prompt pilot, with intervals attached, against the band for your tier.** Settle the taxonomy, write 50 prompts from sales-call notes tagged to intent tiers, run each ten times on two engines, score with the five dimensions, and report with a Wilson interval. Then freeze the weights and put the next run on the calendar.

- **Settle the taxonomy first.** Decide what counts as a citation, a mention and a recommendation before you count anything, using [the taxonomy piece](/blogs/citation-vs-mention-vs-recommendation) as the reference.
- **Write 50 prompts from sales-call notes,** not from a keyword tool, and tag each to an intent tier. This is your pilot portfolio.
- **Run each prompt 10 times on two engines.** Score presence with the five dimensions and report the number with a Wilson interval attached.
- **Compare to the band** for your vertical and tier in Table 5. If you are below the emerging band, the problem is retrieval, not messaging.
- **Pull the citation-source split.** If more than 70% of your citations come from your own domain, the authority gap is your first project.
- **Freeze the weights, version the portfolio, and put the next run on the calendar.** A single measurement is a screenshot; two comparable measurements are a program.

Share of Model is not complicated mathematics. It is a weighted average with confidence intervals attached. What makes it hard is the discipline, a fixed portfolio, enough runs, honest weights, and the willingness to publish a number lower than the one your tool vendor reports. That discipline is the entire difference between measurement and guessing.

## Frequently asked questions

### What is Share of Model tracking, and do you need an agency for it?

Share of Model tracking is measuring, on a fixed cadence, how often and how prominently a brand is named across AI answers for a category, then trending it over time. You do not need a Share of Model agency to start: the method is a frozen prompt portfolio run 8 to 12 times per engine with the results scored and bounded, which an in-house team can run themselves. An agency mainly helps with scale and consistency, not with anything proprietary; the full standard is public on the measurement methodology page.

### What is Share of Model and how is it calculated?

Share of Model is the percentage of brand presence an entity captures across a statistically representative set of category prompts, measured across multiple generative engines and weighted by commercial intent and engine usage. You compute it as your weighted presence divided by the total weighted presence of every brand in the competitive set, over the same prompt portfolio, on the same engines, on a fixed cadence. The denominator is total field presence, not response count, which is what makes it a share rather than a rate.

### How many times should you run each prompt?

Eight to twelve runs per prompt per engine, minimum. Language models are probabilistic: the same prompt sent twice can return different brand sets. At one run your estimate is either 0% or 100%; at three runs it can still be off by 30 points; the estimate only settles into an actionable range around eight to twelve runs. High live-retrieval engines like Perplexity and Google AI Overviews need the top of that range because they re-retrieve on every call.

### How many prompts do you need for a reliable Share of Model?

To hold a two-point margin of error at a 27% inclusion rate you need roughly 1,900 scored observations per brand per engine. At ten runs per prompt that is about 190 prompts, so decision-grade programmes land at a portfolio of 250 to 500 prompts run 5 to 12 times per engine. Precision flattens hard after about 2,500 observations, so a 250-prompt portfolio plus more engines usually beats a 500-prompt one on a tight budget.

### Should you report one blended AI-visibility number across engines?

Report both, but never blended-only. The weighted composite goes on the dashboard; the per-engine breakdown goes in the appendix, because that is where the fix lives. A brand strong on Claude and weak on Perplexity has a live-retrieval problem, the training corpus knows it but the live index does not, which is a crawlability and freshness fix rather than a brand fix. A single blended number hides the engine you are invisible in.

### What is a good Share of Model score?

It depends entirely on the vertical and your competitive tier, so a raw number means nothing in isolation. Across teardowns brands land in four tiers: category leaders run roughly 35-48%, strong challengers 15-32%, and emerging providers 3-15%, with the exact bands set by how consolidated the market is. Field service tops out highest (leader band to 48%) because it is the most consolidated; carbon accounting bottoms lowest (emerging to 3%) because engines there reward peer-reviewed and regulatory sources over marketing volume. Read your number against the band for your tier.

### How is Share of Model different from share of voice, citations and mentions?

Share of voice counts media impressions; share of search counts branded query volume; both break when the buyer asks a model instead of seeing an ad or reaching Google. Citations, mentions and recommendations are the underlying events, a taxonomy that is upstream of Share of Model and defines what you count. Share of Model is the middle scoreboard layer: it takes those events, counts them across a fixed weighted prompt portfolio, and turns them into one share you can trend and benchmark. Attribution to sessions and pipeline is a separate downstream layer.

References

Figures 1 through 14 are original, built from the data and formulas in the sources below.

1. [Share of Model, Generative Engine Optimization. Alephic.](https://www.alephic.com/geo)
2. [Share of Model Framework: Architectonics of Measuring AI Visibility, Narrative Control, and ROI. Chetver.](https://chetver.com/research/share-of-model)
3. [Share of Model (SoM). The Agile Brand Guide.](https://agilebrandguide.com/wiki/agentic-commerce/share-of-model-som/)
4. [How we measure: methodology. Clear Cited.](https://clearcited.com/methodology/)
5. [What Is AI Visibility Score? The Complete Guide to Share of Model. AICarma.](https://aicarma.com/blog/ai-visibility-score/)
6. [What Is Share of Model? The New Metric Replacing Share of Voice. Everything-PR.](https://everything-pr.com/what-is-share-of-model-the-new-metric-replacing-share-of-voice)
7. [Share of Model: a key metric for AI-powered search. Hallam.](https://hallam.agency/blog/share-of-model-a-key-metric-for-ai-powered-search/)
8. [How to Measure AI Search Visibility: The Complete Framework for 2026. Medium.](https://medium.com/@joachim_43659/how-to-measure-ai-search-visibility-the-complete-framework-for-2026-e7fe64c2f759)
9. [Who Owns the AI Recommendation? A Multi-Industry Empirical Map of Brand Category Ownership Across LLMs. arXiv.](https://arxiv.org/html/2606.23057v1)
10. [What is Share of Model and How Do You Track GEO Performance? iMark Infotech.](https://www.imarkinfotech.com/what-is-share-of-model-and-how-do-you-track-geo-performance-the-measurement-framework/)
11. [What is share of model? Simaia.](https://simaia.co/insight/what-is-share-of-model)
12. [AEO Agency & Services: Future-proof brands for AI. Precis.](https://www.precis.com/aeo-services)
13. [How Do I Compare Website SEO and AI Visibility in 2026? BrandArmor.](https://www.brandarmor.ai/blog/how-do-i-compare-website-seo-and-ai-visibility-in-2026)
14. [GEO & SEO Services for professional services. Hinge Marketing.](https://hingemarketing.com/programs-services/services/geo-seo-services-for-professional-services)
15. [What percentage of the AI market do you hold? SEOZoom.](https://www.seozoom.com/what-percentage-of-the-ai-market-do-you-hold/)

About rawmktg.

rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Sources: the Share of Model literature (Alephic, Chetver, the Agile Brand Guide), the multi-industry LLM brand-ownership study (arXiv), and rawmktg category teardowns, 2026. Formulas and code are working reference implementations; benchmark bands are directional.
