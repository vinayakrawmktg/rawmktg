# Citation vs Mention vs Recommendation

> Three words that get used interchangeably in GEO decks. They describe three different subsystems, three different failure modes, and three different fixes. Here is the measurement taxonomy, the math behind each one, and what the data actually says.

*Source: https://rawmktg.com/blogs/citation-vs-mention-vs-recommendation · rawmktg. by Vinayak Ravi*


For nearly thirty years the currency of off-page SEO was the hyperlink. A link was a countable, directional vote. PageRank turned those votes into a graph, and the graph decided who ranked. The model was crude but honest: more good links, more authority, better position.

That model is now one input among several. Large language models and [retrieval-augmented generation](/blogs/how-rag-actually-works) have created an evaluation environment where the machine does not hand back ten blue links. It reads, it decides, and it writes an answer. Somewhere inside that process your brand is either present or absent, either trusted or ignored, either recommended or skipped.

Three signals govern that outcome: mentions, citations, and recommendations. In marketing conversation they get flattened into one idea, usually described as "AI visibility". Inside the machine they are produced by different subsystems, stored in different places, and measured with different math. Confusing them is the reason so many GEO programmes stall.

You cannot fix a mention problem with better on-page content, and you cannot fix a citation problem with more press coverage.

This article separates the three properly. It defines each one mechanically, gives you the formulas used to score them, walks through the empirical evidence for each, and ends with a diagnostic you can run against your own brand this week.

## 01. What is the difference between a mention, a citation, and a recommendation?

**They are three signals from three subsystems.** A mention feeds parametric memory (does the machine know you exist). A citation comes from non-parametric retrieval (does the machine treat your page as evidence). A recommendation happens at synthesis (does the machine pick you). They stack, and each gap has a different cause.

If you read nothing else, read this:

- **A mention** is your brand name appearing in text anywhere on the web, linked or not. It feeds parametric memory, the knowledge baked into a model's weights. It answers: does the machine know you exist.
- **A citation** is an engine attributing a specific claim in its answer to a specific URL. It comes from non-parametric retrieval, the live fetch that happens when someone submits a prompt. It answers: does the machine treat your page as evidence.
- **A recommendation** is the engine naming you as a good choice. It happens at the synthesis layer, after retrieval, when the model weighs options against each other. It answers: does the machine pick you.

They stack. Mentions build the prior. Citations ground the answer. Recommendations convert. You can have all the mentions in the world and never get cited. You can get cited constantly and never get recommended. Each gap has a different cause.

Mention

Awareness. Entity known to the model's weights.

→

Citation

Trust. Page selected as evidence at retrieval.

→

Recommendation

Selection. Named as the pick at synthesis.

Figure 1. The three signals map onto three layers of a generative search system, and form a funnel: awareness, trust, selection.

## 02. Why does separating these three signals matter now?

**Because the signals have decoupled.** In classical search they moved together, a mention earned a link, the link moved the ranking, the ranking drove the click. Generative engines broke that chain, so link count is now a poor proxy for whether a machine will name you.

A mention on Reddit with no link can lift your presence in ChatGPT answers while doing nothing for your Google position. A page that ranks eleventh on Google can be the single source an AI Overview cites, because [retrieval and ranking are separate operations](/blogs/how-your-page-gets-retrieved). And a brand can be cited as a source in an answer that ends up recommending a competitor, which is the most frustrating outcome of all.

Two data points make the scale of the change concrete. In a correlation study of 75,000 brands, branded web mentions correlated with AI Overview visibility at 0.664 while referring domains managed 0.218. And longitudinal data suggests backlinks accounted for roughly 80% of off-page ranking influence in 2012 and around 45% by 2026, with mentions, entity prominence, and co-citation absorbing the difference.

Figure 3. The composition of off-page influence has shifted from link-class signals toward mention-class signals, 2012 to 2026.

Neither number means links are dead. Links still move classical rankings, and classical rankings still feed the retrieval indices these engines query. What the numbers mean is that link count is now a poor proxy for the thing you actually care about: whether a machine will name you when a buyer asks it a question. This is the same gap covered in [winning Google is not winning AI](/blogs/winning-google-isnt-winning-ai).

## 03. How is each signal actually defined?

**By the mechanism that produces it, not how it looks.** Two things can look identical in an AI answer and be produced by completely different parts of the system. Mentions come from entity recognition, citations from retrieval grounding, recommendations from synthesised choice.

### The mention: entity recognition and parametric association

A mention is an unlinked or linked textual reference to an entity, a brand, a product, an executive, or a proprietary term, occurring in published digital text. The defining property is that no anchor tag is required. A plain string of text carries the signal.

Mechanically, mentions operate at entity extraction and parametric encoding. When crawlers and training pipelines ingest unstructured text, NLP models run Named Entity Recognition to map a string to a node in a knowledge graph. Two derived signals matter more than the raw count:

- **Co-occurrence** is the spatial proximity of your brand string to topical keywords inside a sentence, paragraph, or chunk. It teaches the machine what you are.
- **Co-citation** is the appearance of two or more entities inside the same document or thematic context. It teaches the machine who you sit next to.

Co-citation is the underrated one. If your name appears in the same paragraph as three established category leaders often enough, the machine starts treating you as a member of that set. That is not a metaphor; it is a property of how embeddings cluster, and it is the core of [becoming an entity](/blogs/becoming-an-entity).

The precedent for counting unlinked mentions goes back to Google's 2012 implied-links patent (US8682892B1), which describes systems that identify references to external resources without explicit hyperlinks and treat them as implied endorsements. The honest reading: implied links do not pass classic PageRank equity, but they do establish entity prominence, and entity prominence is what a language model retains.

An honest counter-argument

Some link-building practitioners maintain that mentions without links do very little for classical rankings, and on that narrow point they are largely right. The correlation data concerns AI visibility, not position one on a commercial keyword. Both things can be true at once.

### The citation: non-parametric grounding and provenance

A citation is an explicit, verifiable reference, usually rendered as a hyperlinked URL, a footnote, or an inline attribution, that an answer engine uses to ground a specific factual claim in its output.

Citations belong to non-parametric memory. When a prompt arrives, the engine performs a live retrieval step across its index, pulls relevant passages, and loads them into the context window. If the model uses content from one of those passages, it attaches an attribution. The citation is a receipt: the retrieval layer selected your specific chunk of text as evidence for a specific statement.

This has a consequence most content teams miss. Being cited is not a reward for being authoritative in general. It is a reward for having a passage that was extractable, relevant, and dense with verifiable content at the exact moment a sub-query needed it, exactly the profile described in [the anatomy of a high-citation page](/blogs/anatomy-of-a-high-citation-page). Research on citation implementation consistently finds the same preferences: machine-extractable evidence density, precise statistics, direct expert quotations, and high structural clarity.

Citations also serve the engine's own interests. They reduce hallucination by tying generated prose to retrievable web evidence, which is why RAG evaluation frameworks treat citation accuracy as a first-class quality metric rather than a courtesy to publishers.

### The recommendation: synthesised selection

A recommendation is an algorithmic endorsement. The system explicitly proposes your brand as a top-tier choice in response to an intent-driven query.

This happens at the decision layer, after retrieval and during synthesis. Ask an engine which enterprise CRM has the best Slack integration for B2B sales teams and it does not simply look up an answer. It decomposes the question, retrieves candidates across sources, compares attributes, weighs sentiment, and produces a rank-ordered or selective list.

To issue that recommendation the system combines both memory types. Parametric memory supplies the prior, a sense of who the credible players are. Non-parametric retrieval supplies the current evidence about features, pricing, and third-party opinion. A brand missing from either side struggles: strong prior with weak evidence gets mentioned but not recommended; strong evidence with weak prior gets cited as a source while a better-known competitor gets named as the pick. It is also the only one of the three that maps directly to pipeline, and the endpoint that matters most [when the buyer is a bot](/blogs/when-the-buyer-is-a-bot).

### Comparative taxonomy matrix

The table below is the reference version. If you take one artefact from this article into a strategy document, take this one.

Table 1. The measurement taxonomy across seven dimensions.

| Dimension | Mention | Citation | Recommendation |
| --- | --- | --- | --- |
| Primary IR signal | Implicit entity prominence and co-occurrence | Explicit grounding and provenance attribution | Synthesised decision and evaluative choice |
| System memory layer | Parametric memory and knowledge graph | Non-parametric memory and RAG index | Model output and decoded context window |
| Mechanistic trigger | Textual presence, NER, co-citation | Evidence density, extractable stats, schema | Positive sentiment, multi-source consensus, intent match |
| Primary unit | Mention rate, co-occurrence frequency | Citation share, domain attribution count | Recommendation share of voice, mean rank |
| Link dependency | Unlinked or linked, an implied link | Depends on valid, crawlable source URLs | Independent of any direct link |
| Funnel impact | Top of funnel: entity awareness | Mid funnel: trust, verification, referral | Bottom of funnel: conversion, vendor selection |
| Failure mode | Entity ambiguity or negative sentiment | Citation loss from stale or dropped chunks | Exclusion from the day-one consideration set |

## 04. How does the machine actually produce these signals?

**Across two layers: parametric memory and live retrieval.** Almost every strategic mistake in GEO comes from treating them as one. Mentions live in the frozen weights; citations come from the runtime fetch; the recommendation is synthesised from both.

### Parametric memory versus non-parametric retrieval

Parametric memory is the set of internal parameters, weights, and biases configured during pre-training and reinforcement learning. It is static knowledge, frozen at training time, distilled from enormous web crawls. An entity mentioned heavily across authoritative sources during pre-training becomes embedded in the weights. Ask the model a generic category question and it can name that entity without touching the live web.

Non-parametric memory is everything external: real-time web indices, vector databases, and retrieval pipelines queried at the moment a prompt runs. It is fresh, swappable, and where citations come from.

The rule you can act on

If your brand is invisible even on prompts where the engine does not search, you have a parametric problem, and the fix is off-page and slow.

If your brand appears in the answer but your URL never shows up in the source list, you have a retrieval problem, and the fix is on-page and fast.

Offline ingestion

Crawls + training bake entities into weights.

→

Parametric memory

The prior: who the model already knows.

→

Runtime retrieval

Live fetch selects chunks, produces citations.

→

Synthesis

Both combine to produce the recommendation.

Figure 4. Offline ingestion builds parametric memory. Runtime retrieval builds citations. Synthesis combines both into the recommendation.

### Query fan-out, chunking, and context precision

Modern generative engines rarely query their index with the sentence the user typed. They use [query fan-out](/blogs/query-fan-out-how-one-prompt-becomes-ten-searches): the orchestration layer decomposes the primary prompt into multiple targeted sub-queries. A question about enterprise SaaS CRMs with Slack integrations becomes a fan of narrower searches, integration comparisons, native workflow reviews, category buyer guides, run in parallel, each returning candidate documents.

Retrieved documents are parsed into chunks, typically 100 to 300 words. A re-ranking model, usually a cross-encoder, scores each chunk for context precision. Chunks that score well share a profile: clear subject-predicate-object structure, exact numeric figures, named sources, and a single self-contained idea. Chunks that score badly are narrative, hedged, and dependent on the paragraph before them for meaning. Empirical work suggests the median length of a passage cited directly by systems like Claude or ChatGPT sits around 40 words.

The 40-word rule, stated plainly

Write the answer to a question in one self-contained passage of roughly 40 words that would still make sense if it were the only thing a machine ever read from your page. Then write everything else around it. This is the single highest-leverage on-page change available in GEO, and it costs nothing but discipline.

### The Matthew effect and the brand stature ladder

Generative visibility compounds. Information retrieval literature calls this the Matthew effect, the rich getting richer, the engine that powers the [GEO compounding flywheel](/blogs/geo-compounding-flywheel). Language models display a structural bias toward entities with high baseline representation in the training corpus, because that is precisely what parametric memory is. Large-scale analysis across AI engines, published in the GEO-at-scale study covering 102 brands, 3,508 tracking runs, and 102,025 prompt responses, produces a clear ladder:

Figure 5. Baseline unbranded visibility by brand stature tier. Each rung down costs roughly 30 percentage points.

- **Tier 1**, global household brands with dense parametric representation, average **72.9%** visibility on unbranded discovery prompts.
- **Tier 2**, established mid-market and regional brands, sit at **43.6%**.
- **Tier 3**, niche and small brands without broad co-citation networks, average **11.4%**.

Because engines look for multi-source corroboration before committing to a commercial recommendation, a Tier 3 brand is not one content refresh away from parity. It has to build the off-site mention footprint that Tier 1 brands accumulated over a decade. The related finding from the same dataset: visibility trajectories stay flat without intervention. Brands do not drift upward on their own.

### Source composition: earned coverage dominates

The most commonly held false belief in this discipline is that optimising your own domain is sufficient. Production measurement refutes it plainly. When AI search engines generate answers and attribute citations, roughly 2.9% of total citations point to the target brand's own website. The other 97.1% point elsewhere.

Figure 6. Citation source composition. The brand's own domain is a rounding error at 2.9%.

- **Listicles and comparison aggregators** are the single largest category at about 35.7% of all citations, the "best X for Y" pages, and the highest-leverage placement in AI search.
- **User communities and media** such as Reddit, YouTube, and Quora supply roughly 18% to 25%. Re-rankers favour unvarnished user sentiment and recent contextual proof, which is [why Reddit, G2 and analyst reports drive AI recommendations](/blogs/why-ai-cites-reddit-g2-analysts).
- **Reference sites and trade publications** including Wikipedia account for 10% to 15%, providing high-trust entity validation.

Read that chart as an instruction rather than a curiosity. AI answer systems treat first-party claims with structural distrust unless independent sources corroborate them. Your website is where you convert attention, not where you earn it.

### Different engines, different worlds

One more mechanical fact before the math. Engines do not share a retrieval index, and their cited source sets barely overlap. Cross-engine Jaccard overlap of cited domains runs between 16% and 20% for the same prompt, part of [why engines recommend different vendors](/blogs/why-engines-recommend-different-vendors). This kills the idea of a single AI search strategy: you are optimising for five loosely related systems with different index compositions, different re-ranking weights, and different freshness behaviour. That is exactly why the visibility metric below is platform-weighted rather than pooled.

## 05. How do you score the three signals?

**Five metrics, each with its own formula.** Traditional SEO metrics do not survive contact with generative search. Platform-weighted visibility, mean recommendation position, a sentiment index, entity share of voice, and cross-platform source overlap. Each measures a different thing.

Keyword rank position assumes a ranked list. Domain authority assumes a link graph is the primary evaluator. Neither assumption holds when the output is a paragraph of synthesised prose. What follows is a working framework: five metrics, each with the formula, the variables, and code you can run against your own tracking data.

### 1. Platform-weighted visibility

Engines do not perform uniformly. A brand can be highly visible on ChatGPT and absent from Perplexity. Pooling those into one average hides the thing you need to see, so visibility is computed as a weighted composite where w\_p is the platform weight (normalised to sum to one), M\_p is mentions on platform p, and Q\_p is prompts issued to it. Weight the engines your buyers actually use, and renormalise if you only track some of them.

python · platform-weighted visibility

```
from collections import defaultdict

WEIGHTS = {"chatgpt": 0.30, "gemini": 0.20, "perplexity": 0.20,
           "claude": 0.20, "grok": 0.10}

def weighted_visibility(runs, weights=WEIGHTS):
    """runs: list of dicts -> {platform, prompt_id, mentioned: bool}"""
    issued, hits = defaultdict(int), defaultdict(int)
    for r in runs:
        issued[r["platform"]] += 1
        hits[r["platform"]]   += 1 if r["mentioned"] else 0
    score, covered = 0.0, 0.0
    for p, w in weights.items():
        if issued[p] == 0:            # never fake coverage you do not have
            continue
        score   += w * (hits[p] / issued[p]) * 100
        covered += w
    return score / covered if covered else 0.0   # renormalise

def by_platform(runs):
    issued, hits = defaultdict(int), defaultdict(int)
    for r in runs:
        issued[r["platform"]] += 1
        hits[r["platform"]]   += bool(r["mentioned"])
    return {p: round(100 * hits[p] / issued[p], 1) for p in issued}
```

### 2. Mean recommendation position

Appearing in a list is not the same as topping it. Position inside a generated answer correlates strongly with user selection, so ordinal placement needs its own metric. M\_pos is the subset of prompts where the brand receives an explicit ordinal recommendation, and r(q,p) is the rank assigned, where 1 is the primary recommendation. Lower is better, which makes this the one metric on the dashboard that inverts. Label it clearly or someone will misread it in a board deck.

### 3. Contextual sentiment index

Being mentioned is not automatically good. A brand named as the expensive option with poor support has visibility and a problem. The sentiment index normalises tone into a bounded 0 to 100 score: an all-positive answer set scores 100, all-neutral 50, all-negative 0. The 0.5 coefficient on neutral mentions means a negative mention costs exactly twice what a neutral one does, which matches the observed penalty in practice.

### 4. Entity share of voice

Share of voice answers the only question a CMO really asks: are you winning relative to the people you compete against. M\_b is total mention count for the target brand and C is the set of verified, domain-resolvable competitor entities in the answers. The verification step matters, generative engines invent plausible-sounding vendor names, and hallucinated competitors in the denominator will quietly depress your score. Resolve every competitor name to a real domain before counting it.

python · sentiment index and share of voice

```
def sentiment_index(mentions):
    """mentions: list of 'positive' | 'neutral' | 'negative'"""
    if not mentions:
        return None
    pos = mentions.count("positive")
    neu = mentions.count("neutral")
    return round((pos + 0.5 * neu) / len(mentions) * 100, 1)

def share_of_voice(brand_mentions, competitor_mentions, resolvable):
    """resolvable: set of competitor names that map to a real domain.
    Hallucinated vendors are excluded to keep the denominator honest."""
    rival_total = sum(n for name, n in competitor_mentions.items()
                      if name in resolvable)
    denom = brand_mentions + rival_total
    return round(brand_mentions / denom * 100, 1) if denom else 0.0

sentiment_index(["positive", "positive", "neutral", "negative"])   # 62.5
share_of_voice(48, {"RivalA": 91, "RivalB": 55, "Ghostware": 7},
               resolvable={"RivalA", "RivalB"})                    # 24.7
```

### 5. Cross-platform source overlap

The last metric is diagnostic rather than reportable. It measures how much two engines agree on sources for the same prompt, using the Jaccard coefficient over each platform's cited domain set. Run it across your prompt set and you learn where your engines diverge, which tells you which third-party domains are worth pursuing for which platform.

python · cross-engine source overlap

```
from itertools import combinations

def jaccard(a, b):
    a, b = set(a), set(b)
    union = a | b
    return len(a & b) / len(union) if union else 0.0

def overlap_matrix(cited):
    """cited: {prompt_id: {platform: [domain, ...]}}"""
    scores = {}
    for prompt, per_platform in cited.items():
        for p1, p2 in combinations(sorted(per_platform), 2):
            scores.setdefault((p1, p2), []).append(
                jaccard(per_platform[p1], per_platform[p2]))
    return {pair: round(sum(v) / len(v), 3) for pair, v in scores.items()}

# typical real-world output: values cluster between 0.16 and 0.20
# treat anything above 0.35 as a suspiciously narrow prompt set
```

Executives want a single score. Composite metrics are lossy and you should say so out loud, but if you need one, weight the four reportable metrics and convert mean position into a positive-direction term (rank 1 scores 100, rank 6 scores 0). Publish the components alongside the composite. A score that moves without a visible driver is worse than no score.

Table 2. The five metrics, and the question each one answers.

| Metric | What it answers | Variables | Working target |
| --- | --- | --- | --- |
| Platform-weighted visibility | Does the machine know us, engine by engine | w\_p weight, M\_p mentions, Q\_p prompts | Above the tier benchmark for your stature band |
| Mean recommendation position | When named, how prominently | r(q,p) ordinal rank, M\_pos qualifying prompts | 3 or lower, tracked as a falling line |
| Contextual sentiment index | Is the framing helping or hurting | N\_pos, N\_neu, N\_total | 70 or above, zero recurring negatives |
| Entity share of voice | Are we winning against the named set | M\_b brand, M\_c verified competitors | Rising quarter on quarter, fixed competitor set |
| Source overlap coefficient | How much engines agree on sources | D\_p(q) cited domain sets | Diagnostic only, expect 0.16 to 0.20 |

Targets in the final column are working practitioner benchmarks rather than published thresholds. Set your own from your first baseline: a Tier 3 brand hitting 25% weighted visibility has achieved considerably more than a Tier 1 brand holding 70%.

## 06. What does the evidence actually show?

**Three bodies of work, measuring three different things.** The Princeton GEO experiment (causal lifts from content changes), the GEO-at-scale benchmark (non-determinism and the stature ladder), and the 75,000-brand correlation study (mentions beat links). They get quoted interchangeably; they should not be.

### The Princeton GEO experiment

The foundational study establishing generative engine optimisation came from researchers at Princeton, Georgia Tech, the Allen Institute for AI, and IIT Delhi, published at ACM SIGKDD in 2024. It evaluated 10,000 queries across generative platforms to quantify how specific on-page changes affected visibility and citation rates. The headline: classical SEO tactics do close to nothing in generative environments, while adding machine-extractable proof does a great deal.

Figure 8. Measured visibility lift by content intervention (Princeton et al., KDD 2024). Evidence beats phrasing.

- **Expert quotations** produced the largest single lift at +41%. Models treat an attributed quote as a verifiable assertion rather than an opinion.
- **Statistical density** delivered +32%. Precise figures increase the chance a chunk survives re-ranking.
- **Authoritative source citing** delivered +30%. Linking out to primary studies raises the trust score of the citing page.
- **Fluency optimisation** delivered +28%. Clean, readable structure makes extraction easier.

Read those four together and a pattern emerges. Every winning intervention makes a passage more verifiable. None of them make it more persuasive. The machine is not being sold to; it is checking whether your claim can be substantiated without leaving your page.

The counterintuitive part

Adding an outbound link to a primary source raises your own citation odds by about 30%. Traditional SEO instinct says keep the equity in-house. Generative engines do the opposite, treating well-sourced pages as better evidence than unsourced ones. Link out generously to studies, standards, and documentation.

### The GEO-at-scale benchmark

The second body of work is a production analysis across 102 enterprise brands, 3,508 tracking runs, and 102,025 prompt responses. It contributes three findings that should change how you measure.

First, engines are non-deterministic. Re-running identical prompt sets against identical models produced a different prose answer in 22.5% of prompt-engine cells, and 6.8% of responses flipped binary status, moving from mentioned to not mentioned or the reverse. A single-run screenshot is not a measurement; it is a sample of size one from a noisy distribution.

22.5%

of answers change wording on re-run

6.8%

flip mentioned / not-mentioned

6.7x

sentiment variance vs presence

flat

visibility without intervention

Second, sentiment is far noisier than presence. Sentiment scores derived from LLM output exhibit about 6.7 times the variance of binary mention detection. Mention tracking is close to deterministic; tone fluctuates with decoding temperature and prompt phrasing. Treat a single-week sentiment drop as noise until three runs agree. Third, nothing improves on its own: absent content or digital PR intervention, visibility trajectories are flat. Every point of visibility you hold is the result of work someone did, which is the same logic behind [prompt-to-citation tracking](/blogs/prompt-to-citation-tracking).

### Correlation studies: mentions versus links

The third body of work is correlational rather than experimental, and should be read with the usual caution. The 75,000-brand analysis measured Spearman correlations between off-page factors and visibility in Google AI Overviews, later extended to ChatGPT and AI Mode.

Figure 10. Spearman correlation with AI visibility by signal class. Every mention-class signal outranks every link-class signal.

YouTube mentions lead at 0.737, which surprises people until you remember that video transcripts are dense, conversational, entity-rich text that models ingest happily. Branded web mentions follow at 0.664, branded anchors at 0.527, brand search volume at 0.392, Domain Rating at 0.326, referring domains at 0.218, and content volume, the raw number of pages on your site, comes last at 0.194.

Two honest caveats

Correlation is not causation, and brands that earn editorial mentions are usually brands that invested in product, PR, and category presence, all of which have independent effects.

The study population was filtered to brands above a Domain Rating threshold, so it describes the competitive middle and top, not a startup with nine backlinks. What survives both caveats is the ordering: every mention-class signal outranks every link-class signal, and publishing volume is the weakest predictor on the board.

Table 3. Experimental lifts and correlational signals side by side. The first three are causal; the last four are not.

| Intervention or signal | Measured effect | Source | Mechanism |
| --- | --- | --- | --- |
| Expert quotation added | +41% lift | Princeton / Georgia Tech, KDD 2024 | Verifiable statement grounding, better extractability |
| Statistical evidence density | +32% lift | Princeton / Georgia Tech, KDD 2024 | Precise figures pass internal fact-check filters |
| Authoritative source citing | +30% lift | Princeton / Georgia Tech, KDD 2024 | Connects content to primary evidence nodes |
| YouTube mentions | r = 0.737 | 75k-brand correlation analysis | Transcript ingest supplies high-trust co-occurrence |
| Branded web mentions | r = 0.664 | 75k-brand correlation analysis | Teaches category placement through co-citation |
| Referring domains | r = 0.218 | 75k-brand correlation analysis | Passes link equity, weak direct retrieval influence |
| Content volume | r = 0.194 | 75k-brand correlation analysis | Page count alone does not build entity prominence |

## 07. What is the playbook for each signal?

**Three pillars, in order: on-page, technical, off-page.** Citation-first content structuring and entity markup are fast and within your control. Off-page entity PR is slow and decides the ceiling, because 97.1% of citations point away from your site.

### Pillar 1: citation-first content structuring

The goal is a page a re-ranker can dismantle cleanly. That means abandoning the narrative intro and leading with the answer:

- Write section headings as the explicit question a user would ask, not a noun phrase. "How much does implementation cost" beats "Implementation".
- Answer in the first 60 words, completely, with no windup. If the reader could stop after your opening passage and be correctly informed, so could a model.
- Target roughly 40 words for each key factual assertion, matching the median cited passage length.
- State precise numbers, dates, and scope. "A 32% efficiency gain across 1,200 enterprise implementations in Q2 2026" is extractable; "dramatically improved results recently" is not.
- Attribute every claim to a named source, and link out using descriptive anchor text that names the benchmark or dataset rather than the word "source".

The before-and-after below is the shape of the change. Both passages contain the same information. Only one survives chunking.

html · citation-first passage structure

```
<!-- BEFORE: narrative, hedged, unextractable -->
<h2>Implementation</h2>
<p>Every business is different, and the time it takes to get up and
running can vary quite a lot depending on your setup, your team, and
how complex your existing processes are. Many of our customers have
found the process to be quicker than expected...</p>

<!-- AFTER: question heading, 40-word answer, named evidence -->
<h2>How long does implementation take?</h2>
<p>Median implementation takes 18 days for teams under 50 seats and
41 days above 200 seats, based on 1,240 deployments completed between
January and June 2026. Integration with an existing CRM adds a median
6 days.</p>
<p>Source: <a href="/research/deployment-benchmark-2026">2026
Deployment Benchmark, n=1,240</a></p>
```

### Pillar 2: schema and entity markup

Schema alone will not make you visible. What it does is remove ambiguity about which entity you are, which matters enormously when your brand name is also a common noun or shared with another company. Declare a canonical @id URI consistently across every JSON-LD block, connect it with a sameAs array to Wikipedia, Wikidata, Crunchbase, LinkedIn, and official social accounts, and wrap statistical claims in Article and ClaimReview structures. The full treatment is in [schema markup for AI citations](/blogs/schema-markup-ai-citations-2026).

json-ld · entity declaration

```
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Example",
  "url": "https://example.com",
  "description": "AR automation for mid-market finance teams.",
  "foundingDate": "2019-03-01",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q000000",
    "https://www.crunchbase.com/organization/example",
    "https://www.linkedin.com/company/example",
    "https://www.youtube.com/@example"
  ],
  "subjectOf": {
    "@type": "Article",
    "headline": "2026 Deployment Benchmark",
    "citation": "https://example.com/research/deployment-benchmark-2026"
  }
}
```

### Pillar 3: off-page entity PR

This is where the ceiling is set. Since 97.1% of citations point at third-party domains, the work is earning presence on those domains. The co-citation play deserves special mention: getting your executives quoted in articles that also discuss Tier 1 competitors is one of the few reliable ways to move parametric association. You are not buying a link; you are teaching a model that your entity belongs in a set it already trusts, the mechanism behind [authority seeding](/blogs/authority-seeding-ai-llm-trust).

Table 4. Off-page priorities ordered by their share of AI-search citations.

| Source class | Citation share | What to do | Realistic timeline |
| --- | --- | --- | --- |
| Comparison listicles and buyer guides | ~35.7% | Identify which roundups the engines cite for your category, then pitch inclusion, correct outdated entries, supply structured product data | 6 to 12 weeks per placement |
| User communities: Reddit, Quora, forums | 18% to 25% with video | Answer real questions in detail with a named affiliation. Do not astroturf, detected shilling produces negative framing | Ongoing, compounding |
| YouTube and video transcripts | Included above | Publish substantive video with clean transcripts. Strongest single correlation at r = 0.737 | 8 to 16 weeks to signal |
| Reference sites and trade press | 10% to 15% | Pursue Wikidata and Wikipedia eligibility, trade commentary, and analyst mentions alongside Tier 1 competitors | 3 to 9 months |
| Your own domain | ~2.9% | Citation-first structuring, schema, crawlability. Necessary, nowhere near sufficient | 2 to 4 weeks |

### The measurement loop

Run a continuous 90-day cycle. The cadence matters more than the tooling.

Build the prompt set

20-50 fixed prompts across discovery, comparison, problem-solution.

→

Baseline

Query all engines over 3-5 runs; average to smooth variance.

→

Classify sources

Tag every cited URL: brand, listicle, news, community, competitor.

→

Close the gaps

Ship on-page evidence; outreach to the exact domains cited.

→

Re-measure

Compare deltas per engine at 30 days; full review at 90.

Figure 11. The operating cadence for a generative visibility programme.

Step four is the one teams skip. The value is not in knowing you are invisible on a prompt. It is in knowing which four domains the engines consulted before deciding to name someone else.

### Diagnosing which signal is broken

When visibility is bad, the taxonomy tells you where to look. Run a fixed prompt set and read the pattern:

Figure 12. A diagnostic for isolating the failing signal.

| Symptom | Broken signal | Where to fix |
| --- | --- | --- |
| Absent even on prompts with no live search | Mention (parametric) | Off-page entity PR, co-citation, slow |
| Named in the answer, but your URL never cited | Citation (retrieval) | On-page evidence density and schema, fast |
| Cited as a source, competitor gets recommended | Recommendation (synthesis) | Comparison coverage, sentiment, share of voice |

Free Tool · Diagnostic

Which of your three signals is broken?

Answer the three questions from the diagnostic above and isolate the first failing signal, with the fix that actually applies.

Answer three questions about one prompt set

1. On prompts where the engine does **not** search the live web, does your brand get named?

Yes, it appearsNo, absent

2. When your brand **does** appear in an answer, does your URL show up in the cited sources?

Yes, citedNever cited

3. When you are cited, are you the recommended pick, or does a competitor get named?

We are the pickCompetitor wins

Broken signal

--

Answer the three checks

What to fix first

Your result and the specific fix appear here.

[Open the full tool →](/tools/ai-visibility-signal-diagnostic)

Free tools from this piece

Four browser-based tools built from this taxonomy: the [Signal Diagnostic](/tools/ai-visibility-signal-diagnostic) to find the broken signal, the [Platform-Weighted Visibility Calculator](/tools/platform-weighted-visibility-calculator), the [Sentiment & Share-of-Voice Calculator](/tools/sentiment-share-of-voice-calculator), and the [Cross-Engine Source Overlap Calculator](/tools/cross-engine-source-overlap-calculator). All free, all run in your browser.

## 08. What does this taxonomy not mean?

**Four corrections, because this field overclaims fast.** Links are not obsolete. Mentions are not free. The numbers are not permanent. And tracking is not progress.

**It does not mean links are obsolete.** Backlinks still move classical rankings, and classical rankings still feed the indices generative engines query. A correlation of 0.218 is not zero. The claim is that link count has stopped being a good proxy for AI visibility, not that it stopped mattering.

**It does not mean mentions are free.** Unlinked mentions carry weight, but the mechanism is entity prominence rather than equity transfer. A hundred low-quality mentions on scraped content farms will not build parametric presence. Quality of context is what makes co-occurrence useful.

**It does not mean these numbers are permanent.** Platform weights shift with market share. Source composition shifts as engines adjust retrieval preferences. The 40-word median will move as context windows grow. Treat every figure here as a snapshot with a decay rate, and [re-baseline quarterly](/blogs/30-day-content-half-life-recency-ai-ranking-signal).

**It does not mean tracking equals progress.** Dashboards are cheap now. The bottleneck was never measurement. It is the unglamorous work of getting into the roundups your buyers' engines already trust, and that has not been automated. Measurement without visibility is [ranking that is not visibility](/blogs/ranking-isnt-visibility).

## 09. Where does this leave you?

**With three signals, three subsystems, three fixes.** Off-page entity PR for mentions. Evidence-dense on-page structure for citations. Comparison coverage and sentiment for recommendations. Start with the diagnostic, then work the signal that is actually broken.

The taxonomy is simple enough to hold in your head. Mentions establish entity awareness and category placement inside a model's weights. Citations provide grounding and verification during retrieval. Recommendations are the synthesised output where the system evaluates options and steers a buyer.

The rebalancing this requires is uncomfortable for most organic teams, because the highest-leverage work sits outside the website. You are not optimising a page any more. You are building the case, distributed across the web, that a machine will assemble on your behalf when a buyer asks it a question you never see.

Run a fixed prompt set five times across the engines your buyers use, classify every cited URL, and find out which of the three signals is actually broken. Everything else follows from that answer.

## Frequently asked questions

### What is the difference between a mention, a citation, and a recommendation in AI search?

A mention is your brand name appearing in text anywhere on the web, linked or not; it feeds the model's parametric memory and answers whether the machine knows you exist. A citation is an engine attributing a specific claim to a specific URL; it comes from live non-parametric retrieval and answers whether the machine treats your page as evidence. A recommendation is the engine naming you as a good choice at the synthesis layer, and answers whether the machine picks you.

### Do brand mentions without links actually matter for AI visibility?

Yes, but through a different mechanism than links. Unlinked mentions build entity prominence and co-citation, which is what a language model retains in its weights, rather than passing PageRank equity. In a 75,000-brand analysis, branded web mentions correlated with AI Overview visibility at 0.664 versus 0.218 for referring domains. Quality of context matters: low-quality mentions on scraped content farms do little.

### What percentage of AI citations point to a brand's own website?

About 2.9%. In production measurement, roughly 97.1% of citations in AI answers point to third-party domains, comparison listicles, communities like Reddit and YouTube, and reference and trade sites, rather than the brand's own domain. Your website is where you convert attention, not where you earn it.

### Which off-page signal correlates most strongly with AI visibility?

YouTube mentions, at a Spearman correlation of 0.737, ahead of branded web mentions at 0.664. Video transcripts are dense, conversational, entity-rich text that models ingest readily. Every mention-class signal outranked every link-class signal in the data, and raw content volume was the weakest predictor at 0.194.

### How should you measure AI visibility across engines?

Use a fixed prompt set of 20 to 50 discovery and comparison prompts, run it 3 to 5 times per engine to smooth out non-determinism, and compute a platform-weighted visibility score rather than a pooled average. Track mean recommendation position, a contextual sentiment index, and entity share of voice against a verified competitor set, and report per-engine deltas rather than one blended number.

References

The studies, patents and research this taxonomy draws on.

1. [Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines. arXiv.](https://arxiv.org/abs/2606.20065)
2. [What is SEO-GEO? Generative Engine Optimization. explainx.ai.](https://www.explainx.ai/post/what-is-seo-geo)
3. [Brand Mentions vs Backlinks: What Actually Moves Rankings in 2026. Link Publishers.](https://www.linkpublishers.com/blog/brand-mentions-vs-backlinks)
4. [Backlinks vs Brand Mentions: Off-Page SEO Evolution in 2026. Search Atlas.](https://searchatlas.com/blog/backlinks-vs-brand-mentions/)
5. [Generative Engine Optimization (GEO): The Full Definition, Explained. neuroflash.](https://neuroflash.com/blog/generative-engine-optimization/)
6. [Generative Engine Optimization at Scale (full text). arXiv.](https://arxiv.org/html/2606.20065v1)
7. [Unlinked Brand Mentions: The 2026 Marketer's Guide. Web Tonic.](https://www.webtonic.in/blog/unlinked-brand-mentions/)
8. [How To Implement Citations For Generative Engine Optimisation. NeuralAdX.](https://neuraladx.com/how-to-implement-citations-for-geo/)
9. [RAG QA Testing Guide for Retrieval, Generation, and Citation.](https://www.deepchecks.com/rag-qa-testing-guide/)
10. [Generative Engine Optimization for B2B: The Complete 2026 Guide. Mersel AI.](https://www.merselai.com/blog/geo-for-b2b)
11. [Brand Mentions vs Backlinks: What Actually Moves Rankings. Gravidy.](https://www.gravidy.xyz/blog/brand-mentions-vs-backlinks)
12. [Brand Mentions Without A Link Don't Matter. LinkBuildingHQ.](https://linkbuildinghq.com/brand-mentions-without-links/)
13. [Digital PR vs Backlinks: The New SEO Strategy for 2026. Coozmoo.](https://coozmoo.com/digital-pr-vs-backlinks/)
14. [Patent US8682892B1: Google Patented Unlinked Brand Mentions.](https://patents.google.com/patent/US8682892B1/en)
15. [The Complete Guide to Generative Engine Optimization in 2026. Clairon AI.](https://claironai.com/guide-to-geo-2026/)
16. [Generative Engine Optimization, The Definitive Guide 2026. Seolyze.](https://seolyze.com/geo-definitive-guide/)
17. [GEO: Generative Engine Optimization (Princeton, Georgia Tech, AI2, IIT Delhi). arXiv.](https://arxiv.org/abs/2311.09735)
18. [An Analysis of AI Overview Brand Visibility Factors, 75K Brands Studied. Ahrefs.](https://ahrefs.com/blog/ai-overview-visibility-study/)
19. [Are brand mentions without links really counted by Google as off-page signals. r/seogrowth.](https://www.reddit.com/r/seogrowth/)
20. [YouTube mentions are the top signal for AI brand visibility. TNW.](https://thenextweb.com/news/youtube-mentions-ai-brand-visibility)
21. [AI and Brand Visibility: Ahrefs' Insights from 75,000 Brands. BuzzStream.](https://www.buzzstream.com/blog/ai-brand-visibility-ahrefs/)
22. [Ranqo, AI Search Visibility Suite. Further reading.](https://ranqo.com/)
23. [AI Search Research. Ranqo Labs. Further reading.](https://ranqo.com/labs/)

About rawmktg.

rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Sources: the Princeton/Georgia Tech GEO experiment (KDD 2024), the GEO-at-scale benchmark, and the 75,000-brand correlation analysis, 2024-26. Formulas and code are working reference implementations; figures are drawn from the cited studies.
