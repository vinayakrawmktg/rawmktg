# Query Fan-Out: How One Prompt Becomes Ten Searches

> You type one sentence. The engine runs eight to sixteen searches you never see, scores a few thousand text chunks, and writes an answer from roughly five pages. How that machine works, what the math rewards, and why the page that ranks #1 often loses to the page that ranks #5 four times.

*Source: https://rawmktg.com/blogs/query-fan-out-how-one-prompt-becomes-ten-searches · rawmktg. by Vinayak Ravi*


Search used to be a single transaction. You typed a string, the engine matched it against an inverted index, and it handed back ten blue links ordered by lexical relevance, link topology and domain authority. One input, one lookup, one list. Every SEO tactic built between 1998 and 2023 assumes that shape.

That shape is gone. When you ask ChatGPT Search, Google AI Mode or Perplexity a real question, the system does not run your question. It reads your question, works out what you are actually trying to decide, and then writes its own set of searches. Those run in parallel against different corpora, get fused, chunked, scored and compressed into a context window. Only then does a model write the paragraph you read.

Your competitors are not beating you on the head term. They are beating you on eleven sub-queries neither of you can see in Ahrefs.

The industry name for the middle step is query fan-out (also query decomposition, multi-query retrieval, or query variant generation). If you optimised a page for the sentence a human types, you optimised for a string that is no longer being searched. The strings being searched are machine-written, highly specific, and almost entirely absent from keyword tools.

## 01. What is query fan-out, in one line?

**AI search does not rank pages against your prompt.** It generates its own sub-queries, retrieves passages for each one, fuses the lists, and cites whichever sources show up usefully across the most facets. Breadth of coverage beats depth on any single term.

Query fan-out, also written **"query fan out"** or **"query fanout"**, is the same mechanism Google and Gemini call **grounding**: the engine expands your prompt into many sub-queries, retrieves passages for each, and grounds its answer in what comes back. So "query fan-out" and "grounding queries" describe the two halves of one process, and its practical meaning is that breadth of coverage, not a single keyword ranking, decides who gets cited.

Each sub-query goes after a distinct facet of the original: a technical spec, a pricing tier, a compliance requirement, a comparison, a piece of social proof, or a follow-up you have not thought to ask. They fire simultaneously across live web indices, knowledge graphs, product catalogues and community databases. The system merges the ranked lists with Reciprocal Rank Fusion and dense vector scoring, assembles the surviving passages into a context block, and passes that to the model, which writes the answer with inline citations.

Classify

Does this even need a search, and how hard?

→

Decompose

Write the sub-queries that cover the facets.

→

Retrieve

Fire them at different corpora in parallel.

→

Fuse + score

Merge lists, chunk pages, score the chunks.

→

Synthesise

Write one answer, attach citations.

Figure 1. The generalised fan-out pipeline. Every commercial AI search product is a variation on this shape.

The structural detail that drives everything

Retrieval happens per sub-query, not per prompt. A page is never evaluated once. It is evaluated eight to sixteen times, against eight to sixteen different questions, and it only needs to win a few of them to be pulled into the context pool. Visibility is no longer a position. It is a hit rate.

## 02. How many hidden searches does one prompt trigger?

**Eight to sixteen in standard modes, and 400+ in agentic deep research.** About 59% of prompts fan out into 5 to 11 sub-searches, 24% into 12 to 19, and the hardest standard tasks reach 28. A single ChatGPT Deep Research prompt has been documented triggering over 400. ([GEOly](https://www.geoly.ai/blog/query-fan-out))

Figure 2. Distribution of sub-query volume per prompt. The modal prompt fires between five and eleven hidden searches.

Table 1. Sub-query volume bands, share of prompts, and the modes that produce them.

| Sub-query volume | Share of prompts | What triggers it | Typical engine |
| --- | --- | --- | --- |
| 1 to 4 | ~17% | Simple factual and navigational lookups | Google AI Mode, ChatGPT standard |
| 5 to 11 | 59% | Standard commercial and comparative intent | Perplexity, ChatGPT Search |
| 12 to 19 | 24% | Multi-faceted buyer journeys and analysis | Google AI Mode on Gemini 2.5 |
| 20 to 28 | ~3% | Advanced multi-constraint research tasks | Complex multi-turn AI sessions |
| 200 to 400+ | Special mode | Recursive agentic deep research | ChatGPT Deep Research |

Read that as a traffic forecast and it looks like good news. Read it as a competition forecast and it is not. Ten sub-queries means ten chances to be included and ten chances to be left out.

## 03. How does ChatGPT Search actually work, stage by stage?

**A seven-stage retrieval pipeline, and every stage is a filter that throws work away.** Understanding where the losses happen tells you exactly where to spend effort: classification, query generation, metadata filtering, fetch and chunk, vector scoring, audition selection, and synthesis.

### Stage 1: query classification

A lightweight classifier scores the prompt in milliseconds and returns a no-search, simple-search and complex-search probability. If the no-search score clears roughly 0.2, the model answers from parameters and no retrieval happens at all. If the complex score clears roughly 0.4, the system enters a recursive multi-turn planner. ([Rankly](https://www.tryrankly.com/blogs/how-chatgpt-search-works)) A meaningful share of prompts in your category may never trigger a search, for those you are competing against training data and brand memory, not your sitemap.

python - the routing decision

```
# Conceptual shape of the routing decision
scores = classifier(prompt, conversation_history)

if scores.no_search > 0.20:
    return answer_from_parameters(prompt)        # no retrieval, no citations
if scores.complex_search > 0.40:
    return recursive_planner(prompt, max_rounds=3)   # fan-out, read, fan-out again
return single_pass_retrieval(prompt)             # one round of sub-queries
```

### Stage 2: search query generation

The orchestrator writes two classes of query: short keyword queries for inverted-index lookup, and longer semantic queries (around fifteen words) written to align vector embeddings with intent. For complex prompts it runs a planner loop, up to three rounds, issuing a batch, reading the metadata, spotting gaps, and firing again. If your content answers the obvious facet, you compete in round one against everyone. If it answers the awkward second-order facet, you are one of very few candidates in round two, where the field is thin.

### Stages 3-4: filter, fetch and chunk

Sub-queries return 40 to 50 candidate URLs. Before fetching a single page, the system cuts that pool to 10 to 20 based purely on SERP-level metadata, title tags, meta descriptions, authority signals and schema. Your body copy is not consulted at this stage; your title tag is doing all the work. ([Rankly](https://www.tryrankly.com/blogs/how-chatgpt-search-works)) Survivors are fetched three to ten at a time under a hard two-second render timeout, then parsed into uniform, non-overlapping 128-token chunks ([Rankly](https://www.tryrankly.com/blogs/how-chatgpt-search-works)), about a hundred words, that may be split mid-argument by a chunker that has never read your headline.

### Stages 5-6: vector scoring and the audition chunk

Chunks are embedded and scored by cosine similarity against the semantic sub-query vectors, thousands of comparisons in 100 to 200 milliseconds. The system then looks at the single highest-scoring chunk from each page, its audition chunk, alongside the metadata, and selects a final pool of three to five pages for deep reading. Your entire page is represented, at the moment of selection, by its best hundred words. If your best chunk is a hedged introduction, you do not audition well.

### Stage 7: context assembly and generation

Surviving text, roughly 5,000 to 6,000 tokens, is formatted into sliding windows around the top chunks, and the core model writes the answer with inline citations. Two infrastructure facts sit underneath: about 92% of ChatGPT's external searches run via the Bing Search API, and OpenAI's OAI-SearchBot does not execute JavaScript, it parses raw HTML. Empirical work found 46% of ChatGPT crawler requests operating in plain-HTML mode. ([Netstager](https://blog.netstager.com/query-fan-out-in-seo/))

40-50 URLs

from the sub-queries.

→

10-20 pass

metadata filter, title tags only.

→

3-5 pages

deep-read after the audition chunk.

→

5-6k tokens

context window, then the answer.

Figure 3. The compression funnel. Fifty candidates become five pages become six thousand tokens.

## 04. How do Google AI Mode and Perplexity differ?

**Same fan-out, different destinations, and different transparency.** Google issues up to sixteen parallel sub-searches across four corpora at once ([Aleyda Solis](https://www.aleydasolis.com/en/ai-search/google-query-fan-out/)), the web index, Knowledge Graph, Shopping Graph and review databases. Perplexity exposes its six to ten sub-queries directly in the interface.

What makes Google's version structurally different is not the count, it is the destinations. Your product page competes in the web index, your entity record in the Knowledge Graph, your feed in the Shopping Graph, your reviews somewhere else entirely. A team that only owns the website is playing one of four hands. And the number that should reshape planning: pages that rank for the associated fan-out sub-queries are 161% more likely to be cited in AI Overviews than pages that rank only for the primary query. ([Surfer](https://surferseo.com/blog/query-fan-out/)) This is the multi-corpus split covered in [AI Mode vs AI Overviews](/blogs/ai-mode-vs-ai-overviews).

Perplexity leans on decomposition hardest and most visibly, exposing its sub-queries as follow-up searches. It is the cheapest research tool available: type your buyers' questions and read the sub-queries it shows you. That is your content brief, written by the machine that will grade it. ([Finseo](https://www.finseo.ai/query-fanout-analysis))

Table 2. Architecture comparison across the three engines that matter commercially.

| Feature | ChatGPT Search | Google AI Mode | Perplexity |
| --- | --- | --- | --- |
| Orchestrator | Dedicated reasoning orchestrator | Custom Gemini 2.5 engine | Agentic RAG pipeline |
| Sub-queries / prompt | 8 to 12 (400+ in Deep Research) | 8 to 16 parallel | 6 to 10 |
| Primary index | Bing API ~92% + OAI-SearchBot | Web index, Knowledge Graph, Shopping Graph, reviews | Hybrid web + multi-engine APIs |
| JavaScript rendering | No, raw HTML only | Yes, Googlebot pipeline | Partial and limited |
| Fetch timeout | Hard 2.0s per page | Native SERP latency | Dynamic multi-source |
| Unit evaluated | 128-token vector chunks | Entity-based passage scoring | Structured Q&A passages |

## 05. What is the math that decides who gets cited?

**Two operations: cosine similarity for relevance, and Reciprocal Rank Fusion for survival.** Neither rewards what classical SEO optimises for. Cosine scores a passage against a sub-query; RRF decides which documents survive when eight ranked lists have to become one.

### Vector embeddings and cosine similarity

A 128-token chunk becomes a dense vector; a generated sub-query becomes a dense vector in the same space; relevance is the cosine of the angle between them. The denominator normalises for magnitude, so a long passage does not beat a short one simply for being long. Retrieval systems care about the band from roughly 0.7 upward. Because embeddings capture concepts rather than strings, a chunk can score high with zero exact keyword overlap. Keyword density is not a lever here; conceptual cleanliness is.

python - the scoring pass, minus the GPU

```
# What the scoring pass looks like, minus the GPU
import numpy as np

def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

chunks        = chunk_page(html, size_tokens=128, overlap=0)
chunk_vecs    = embed(chunks)              # e.g. 1536 dimensions each
subquery_vecs = embed(generated_subqueries)

# every chunk is scored against every sub-query, independently
scores = { (i, j): cosine(q, ch)
           for i, q  in enumerate(subquery_vecs)
           for j, ch in enumerate(chunk_vecs) }

# the page is represented by its single best chunk: the audition chunk
audition = max(scores.values())
```

The line that breaks old habits

Your page's score at the selection gate is a maximum, not a mean. Padding a page with more sections does not raise its audition score. Writing one section that nails one sub-query does.

### Reciprocal Rank Fusion, and why #1 is overrated

After N parallel sub-queries the system holds N ranked lists and needs one pool. It merges them with RRF: each document scores the sum, across every list it appears in, of one over a constant (conventionally k=60) plus its rank. ([GEOly](https://www.geoly.ai/blog/query-fan-out)) The constant exists to stop any single list's top result from dominating, and it works by flattening the top of the curve almost completely.

Figure 4. The RRF weighting curve at k=60. Rank #1 contributes 0.01639, rank #10 contributes 0.01429, a gap of just 13%.

Thirteen percent. Every incremental effort spent moving a page from position ten to position one buys a 13% edge inside a single sub-query list. Appearing at all in a second sub-query list buys you close to 100%.

Figure 5. Document B ranks #5 in four lists; Document A ranks #1 in one. B wins by 3.75x without ever winning a single sub-query.

python - Reciprocal Rank Fusion in eight lines

```
# Reciprocal Rank Fusion in eight lines
from collections import defaultdict

def rrf(result_lists, k=60):
    scores = defaultdict(float)
    for ranked in result_lists:                 # one list per sub-query
        for rank, doc in enumerate(ranked, start=1):
            scores[doc] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

# doc_a appears once at rank 1; doc_b appears four times at rank 5
lists = [
    ['doc_a', 'x', 'y', 'z', 'doc_b'],
    ['p', 'q', 'r', 's', 'doc_b'],
    ['t', 'u', 'v', 'w', 'doc_b'],
    ['m', 'n', 'o', 'l', 'doc_b'],
]
rrf(lists)[:2]
# [('doc_b', 0.06154), ('doc_a', 0.01639)]
```

The fusion algorithm structurally favours content that addresses multiple facets over monolithic pages that optimise for one head term. It is the mathematical reason a [topical authority cluster](/blogs/topical-authority-cluster-ai-shortlists) outperforms a hero page. And because the engine scores individual chunks against specific sub-queries, not domains against topics, [passage relevance now outranks domain authority](/blogs/ranking-isnt-visibility): a small domain's explicit, dense, atomic answer can outscore a vague passage on a major publisher ([Netstager](https://blog.netstager.com/query-fan-out-in-seo/)). Authority still helps at the selection gate, but it cannot manufacture a relevant chunk that does not exist.

## 06. What does fan-out do to a real buyer prompt?

**It reads the hard constraints and writes eight searches aimed at eight corpora.** A mid-market healthcare-CRM prompt with four hard constraints (Epic integration, HIPAA, AI workflows, under $150/user) and one soft one decomposes into eight sub-queries, only one of which resembles a keyword anyone researches.

A traditional engine would try to match 'enterprise CRM healthcare Epic EHR HIPAA under 150' and return a mess of sponsored pages. The AI system writes eight searches instead:

Table 3. The fan-out for a single mid-market buyer prompt. Only SQ-01 resembles a keyword anyone researches.

| ID | Facet | Target corpus | Selection logic |
| --- | --- | --- | --- |
| SQ-01 | Product classification | Web index, review aggregators | Identify category leaders |
| SQ-02 | Technical compatibility | Vendor docs, app exchanges | Filter on a hard integration requirement |
| SQ-03 | Regulatory | Trust centres, security specs | Verify the mandatory legal framework |
| SQ-04 | Functional capability | Feature modules, product guides | Assess automation depth |
| SQ-05 | Commercial | Official pricing pages | Enforce the sub-$150 constraint |
| SQ-06 | Direct comparison | Comparative roundups | Analyse trade-offs between leaders |
| SQ-07 | Sentiment | Reddit, Quora, peer forums | Validate real implementation experience |
| SQ-08 | Edge case | Vendor FAQs, knowledge bases | Audit constraints on secondary candidate |

The synthesised answer highlights Vendor A for superior Epic integration (cited from technical docs), notes Vendor B as cost-effective but flags that Epic sync needs middleware (cited from a developer forum), and excludes Vendor C outright because its HIPAA BAA is restricted to tiers above $200. This is the mechanism behind most unexplained AI visibility losses. The page was fine. The coverage was not.

The vendor that lost

A competitor published one well-optimised landing page targeting 'best healthcare CRM'. It was excluded entirely, because it offered no extractable data for SQ-02, SQ-03 or SQ-05. It did not rank badly. It was never a candidate. There was nothing on the page for three of the eight questions to retrieve.

## 07. Why can't keyword tools see the searches that matter?

**Because over 95% of generated sub-queries have zero recurring search volume. ([Netstager](https://blog.netstager.com/query-fan-out-in-seo/))** Keyword databases were built by measuring strings humans repeat. Fan-out sub-queries are written fresh by a model for one user's context and never typed by anyone. A tool that measures repetition cannot see a query that occurs once.

So the standard workflow breaks at the first step, there is no volume report to sort descending. What replaces it: read the sub-queries Perplexity exposes for your category; mine your sales calls (buyer objections are almost verbatim what the orchestrator generates); enumerate your head term's facets deliberately (specification, compatibility, compliance, capability, price, comparison, sentiment, edge case); and watch which pages get cited for questions you never targeted. Search volume as a prioritisation metric is retiring. Facet coverage replaces it, the same shift measured in [citation vs mention vs recommendation](/blogs/citation-vs-mention-vs-recommendation).

Table 4. The optimisation model before and after query fan-out.

| Factor | Traditional SEO | Generative engine optimisation |
| --- | --- | --- |
| Primary goal | Rank #1 on a results page | Be cited inside a synthesised answer |
| Targeting unit | One focus keyword per page | Whole intent clusters and entity facets |
| Ranking signal | Domain authority, backlinks, exact match | Passage vector similarity, monosemantic chunks |
| Volume model | High-volume head and mid-tail terms | Zero-volume sub-queries, ~95% invisible |
| Content structure | Monolithic 2,500-word guide | Modular, self-contained, passage-level answers |
| Technical focus | Core Web Vitals, mobile UX, JS rendering | Plain-HTML readability, fast crawl, schema |
| Measurement | Clicks, keyword rankings, impressions | Citation frequency, share of voice by facet |

## 08. How do you optimise for query fan-out?

**Four moves: write atomically, keep passages monosemantic, survive a non-rendering crawler, and build off-site.** In rough order of return on effort. Almost none of it is measurable in the tools most teams pay for, which is the real transition cost.

### 1. Write atomically, and let headings do the retrieving

Engines extract 128-token chunks and score them independently, so build modular, self-contained sections where each fully answers one sub-question. Pages with headlines that directly answer specific sub-questions are cited by ChatGPT 41% of the time, against 29% for generic or artistic headlines, a twelve-point swing for writing your H2s as questions. ([Netstager](https://blog.netstager.com/query-fan-out-in-seo/)) The counterintuitive part: focused articles covering 26% to 50% of a topic's sub-queries beat massive single-page guides attempting 100%, because five focused pages produce five audition chunks, five title tags and five shots at the fusion pool, where one monster URL produces one of each. This is the shape of [a high-citation page](/blogs/anatomy-of-a-high-citation-page).

Figure 6. ChatGPT citation rate by headline style: question-style H2s (41%) vs generic or artistic headlines (29%).

html - the structural pattern that works

```
<article>
  <h1>Healthcare CRM platforms with native Epic EHR integration</h1>
  <section>
    <h2>Which healthcare CRMs integrate natively with Epic EHR?</h2>
    <p>Three platforms offer certified native Epic integration:
    Vendor A (Epic App Orchard, bidirectional), Vendor B (read-only
    via middleware), and Vendor C (FHIR R4 endpoint, 2024 onward).</p>
    <!-- answer lands in the first 40 words, inside one chunk -->
  </section>
  <section>
    <h2>Does a HIPAA BAA come with every pricing tier?</h2>
    <table>...tiers, BAA availability, price per user per month...</table>
  </section>
</article>
```

Answer first, elaborate second. The chunker does not read ahead. If your answer arrives in paragraph four, it lands in a different chunk from the heading that promised it, and the two are scored separately.

Free Tool · Generator

Generate the eight-facet brief

Turn your head term into the eight questions a fan-out will ask, one question-style H2 per facet, plus its target corpus. Copy or download.

Your head term

A named competitor (optional)

Enter a head term and get an eight-facet brief: one question-style H2 per facet, plus the corpus each sub-query targets. Answer each in the first forty words, in server-side HTML.

Your fan-out brief

CopyDownload .md

```
Enter a head term to generate the brief.
```

[Open the full tool →](/tools/fan-out-content-brief-generator)

### 2. Keep passages monosemantic

A passage is monosemantic when it stays cleanly on one concept. High monosemanticity keeps the embedding mathematically close to the target sub-query vector, maximising cosine similarity. ([Aleyda Solis](https://www.aleydasolis.com/en/ai-search/google-query-fan-out/)) Passages that blend several topics produce a vector that sits between all of them and scores mediocre against every sub-query. Practical test: take any 150-word block in isolation, with no heading, and ask what single question it answers. If you cannot name one, the chunk will not win one. This is the passage-level layer beneath [how your page gets retrieved](/blogs/how-your-page-gets-retrieved).

### 3. Make the facts survive a non-rendering crawler

Since OAI-SearchBot does not run client-side JavaScript, and 46% of ChatGPT retrieval passes fetch plain HTML, every fact you want cited must be in the server-side response, and under a two-second timeout. Use semantic HTML (article, section, h2, table); never render pricing, specs or compliance data client-side; use real HTML tables, not CSS grids or images; and ship JSON-LD, more in [schema markup for AI citations](/blogs/schema-markup-ai-citations-2026) and [how AI crawlers index your site](/blogs/how-ai-crawlers-index-your-site).

If your pricing table is rendered client-side

It does not exist. Not to a non-rendering crawler working under a two-second timeout. Any fact you want cited, pricing, specs, compliance terms, integration lists, has to be in the server-side HTML response.

json-ld - one block answers three sub-queries

```
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Vendor A Health Cloud",
  "applicationCategory": "CRM",
  "offers": {
    "@type": "Offer",
    "price": "120.00",
    "priceCurrency": "USD",
    "unitText": "per user per month"
  },
  "featureList": [
    "Native Epic EHR integration via App Orchard",
    "HIPAA Business Associate Agreement on all paid tiers",
    "Automated patient outreach workflows"
  ]
}
```

### 4. Build the off-site footprint, because the fan-out leaves your domain

Sentiment sub-queries do not go to your website. They go to Reddit, Quora, G2 and Capterra, because the engine is cross-validating your claims against people who are not you. Domains with strong profiles across those platforms see roughly 3x higher citation rates, and sites with very large referring-domain footprints are around 3.5x more likely to be cited. ([Netstager](https://blog.netstager.com/query-fan-out-in-seo/)) A fan-out of eight sub-queries might send only four at content you control; the other four go to corpora you can influence but not own. That is the argument for [authority seeding](/blogs/authority-seeding-ai-llm-trust) and [why AI cites Reddit, G2 and analysts](/blogs/why-ai-cites-reddit-g2-analysts).

## 09. How do you measure any of this?

**Rank tracking answers a question the engine no longer asks. Expected citation replaces it.** Expected citation decomposes into retrieval probability (a coverage problem, do you have a passage that can win sub-query i at all) and selection probability (a quality and authority problem, does your audition chunk beat the others).

Most teams have spent a decade optimising selection for a handful of queries while leaving retrieval at zero for most of the fan-out. A workable loop, without buying anything: build a prompt set of 30 to 50 real buyer questions; run them across ChatGPT Search, AI Mode and Perplexity weekly, logging every cited domain; capture the sub-queries where the interface exposes them; score whether you were cited, mentioned without a link, and which facet you were cited for; and track share of voice by facet. Gaps by facet tell you what to write next, the discipline behind [prompt-to-citation tracking](/blogs/prompt-to-citation-tracking).

python - minimal citation tracker

```
# Minimal citation tracker: prompts in, cited domains out
import datetime

PROMPTS = load_jsonl('buyer_prompts.jsonl')     # 30-50 real questions
rows = []
for p in PROMPTS:
    for engine in ('chatgpt_search', 'ai_mode', 'perplexity'):
        answer = ask(engine, p['text'])
        rows.append({
            'date':       datetime.date.today().isoformat(),
            'prompt':     p['id'],
            'facet':      p['facet'],        # spec | compat | compliance | price ...
            'engine':     engine,
            'cited':      OUR_DOMAIN in answer.citations,
            'mentioned':  OUR_BRAND in answer.text,
            'sources':    answer.citations,
            'subqueries': answer.get('subqueries', []),   # Perplexity exposes these
        })

# share of voice by facet is the number that should move
sov = group_by(rows, 'facet', agg=lambda r: mean(x['cited'] for x in r))
```

Free Tool · Calculator

Estimate your expected citation rate

The formula above, made live. Enter your facet count, coverage and selection strength to see expected citations, and why covering one more facet usually wins.

Your topic's fan-out

Facets in the fan-out

Facets you cover

Avg selection strength (0-1)

Retrieval probability is a coverage problem (do you have a passage that can win facet i at all). Selection strength is a quality and authority problem (given you were retrieved, does your audition chunk beat the others). Expected citation = the average of retrieval x selection across the fan-out.

Expected citation rate

0%

Enter your fan-out

Where the lift is

Your estimate updates as you type.

[Open the full tool →](/tools/expected-citation-estimator)

Free Tool · Diagnostic

Audit your facet coverage

Run the eight-facet frame against your own content. Mark what you answer in under a hundred words and see the briefs you are missing.

Your topic or head term

For each of the eight facets a fan-out targets, mark whether a single passage on your site answers it in under a hundred words. Buried in paragraph four does not count, the chunker does not read ahead.

**Specification.** the core features and what it actually does

Covered in <100 wordsMissing / buried

**Compatibility.** integrations, platforms and what it works with

Covered in <100 wordsMissing / buried

**Compliance.** security, certifications and regulatory fit

Covered in <100 wordsMissing / buried

**Capability.** specific workflows and how deep the automation goes

Covered in <100 wordsMissing / buried

**Price.** plans, tiers and total cost, in server-side HTML

Covered in <100 wordsMissing / buried

**Comparison.** head-to-head vs named competitors and alternatives

Covered in <100 wordsMissing / buried

**Sentiment.** real reviews and community proof (off your domain)

Covered in <100 wordsMissing / buried

**Edge case.** the awkward constraint a buyer asks about last

Covered in <100 wordsMissing / buried

Facet coverage

0/8

Mark the facets

Briefs to write next

[Open the full tool →](/tools/facet-coverage-auditor)

Free tools from this piece

Three browser-based tools built from this deep dive: the [Facet Coverage Auditor](/tools/facet-coverage-auditor) to find your gaps, the [Expected-Citation Estimator](/tools/expected-citation-estimator) that replaces rank tracking, and the [Fan-Out Content Brief Generator](/tools/fan-out-content-brief-generator). They complement the existing [Query Fan-Out Simulator](/tools/query-fan-out-simulator), a free query fan-out tool, and [RRF Calculator](/tools/rrf-rank-fusion-calculator). All free, all run in your browser.

## 10. What should you do this week?

**Decompose your five best prompts by hand, audit facets not keywords, and start the log.** The baseline you do not capture this month is the comparison you will want in six.

- Pick your five highest-value buyer prompts and decompose them by hand with the eight-facet frame: specification, compatibility, compliance, capability, price, comparison, sentiment, edge case. You will find gaps within twenty minutes.
- Audit the facets, not the keywords. For each sub-query, ask whether any single passage on your site answers it in under a hundred words. If not, that is a brief.
- Rewrite your H2s as questions, then move the answer into the first forty words underneath each.
- Curl your own pages with JavaScript disabled. Anything missing from that response is invisible to a meaningful share of AI retrieval.
- Split the monster guide. One page carrying twenty facets has one audition chunk and one title tag; five focused pages have five of each.
- Claim the off-domain surfaces: review profiles, documentation, community answers, entity records. Half the fan-out never touches your site.
- Start the prompt log now. Thirty prompts, weekly, three engines, in a sheet.

AI search does not reward the best page for a query. It rewards the most consistently useful source across a set of queries you will never see.

## Frequently asked questions

### What is query fan-out in AI search?

Query fan-out is the step where an AI search engine decomposes your single prompt into a set of targeted sub-queries, one per facet of what you meant (a spec, a price tier, a compliance requirement, a comparison, social proof), then fires them in parallel against different corpora. Instead of searching once for what you typed, the engine searches many times for what you meant, and each sub-query is a separate retrieval contest with its own winners.

### How many sub-queries does one prompt generate?

In standard modes, a single conversational prompt fans out into roughly 8 to 16 parallel sub-queries. About 59% of prompts trigger 5 to 11, 24% trigger 12 to 19, and the hardest standard tasks reach 28. Agentic research modes break the scale entirely: a single ChatGPT Deep Research prompt has been documented triggering over 400 sub-queries.

### Why do zero-volume keywords matter for AI search?

Over 95% of generated fan-out sub-queries have zero recurring search volume in keyword tools, because they are machine-written fresh for one user's context and never typed by anyone. Keyword databases measure strings humans repeat, so they cannot see a query that occurs once. The prioritisation metric shifts from search volume to facet coverage: how many of the sub-queries in a topic you can answer better than anyone.

### Does ranking #1 still matter with Reciprocal Rank Fusion?

Less than it used to. Under RRF with the conventional constant k=60, rank #1 contributes 0.01639 and rank #10 contributes 0.01429, a gap of just 13%. Moving a page from position 10 to 1 inside one sub-query buys a 13% edge; appearing at all in a second sub-query list buys close to 100%. A document that ranks #5 across four lists beats a document that ranks #1 in one, by 3.75x.

### How do you optimise for query fan-out?

Write atomically, one self-contained section per sub-question with the answer in the first 40 words; keep passages monosemantic so the embedding sits close to one sub-query vector; serve every fact (pricing, specs, compliance) in server-side HTML because the main ChatGPT crawler does not render JavaScript; and build the off-site footprint, since sentiment sub-queries go to Reddit, G2 and forums, not your site. Rewriting H2s as questions alone lifts ChatGPT citation rate from 29% to 41%.

### Is query fan-out the same as grounding?

Largely yes. Grounding is the term Google and Gemini use for retrieving external passages to support an answer, and query fan-out is how that retrieval is done: the model rewrites your prompt into eight to sixteen sub-queries, runs them in parallel, and grounds the answer in the passages that come back. "Query fan-out" names the expansion step; "grounding" names the retrieve-and-cite loop it feeds.

### Is there a query fan-out tool?

Yes. The free Query Fan-Out Simulator takes a buyer prompt and shows the sub-queries an engine is likely to generate from it, so you can see which facets your page answers and which it misses. Pair it with the Fan-Out Content Brief Generator to turn those sub-queries into an outline, and the RRF Calculator to see how fusion scoring rewards breadth over a single number-one ranking.

Sources and further reading

The pipeline analyses and measurements this deep dive draws on.

1. [What Is Query Fan-Out in SEO and How Does It Affect Your Rankings? Netstager.](https://blog.netstager.com/query-fan-out-in-seo/)
2. [Query Fan-Out Analysis Tool: Analyze AI Query Decomposition. Finseo.](https://www.finseo.ai/query-fanout-analysis)
3. [Google AI Mode's Query Fan-Out Technique: What It Means for SEO. Aleyda Solis.](https://www.aleydasolis.com/en/ai-search/google-query-fan-out/)
4. [What Is Query Fan-Out and How Does It Work for AI Searches? Search Engine Land.](https://searchengineland.com/guide/query-fan-out)
5. [What Is Query Fan-Out and Why Does It Matter? Semrush.](https://www.semrush.com/blog/query-fan-out/)
6. [Query Fan-Out: Everything You Need To Know. Surfer.](https://surferseo.com/blog/query-fan-out/)
7. [How ChatGPT Search Works: The 7-Stage Pipeline Behind Every Answer. Rankly.](https://www.tryrankly.com/blogs/how-chatgpt-search-works)
8. [What Is Query Fan-Out? Understanding the Hidden Queries Driving AI Search. GEOly.](https://www.geoly.ai/blog/query-fan-out)
9. [LegalMALR: Multi-Agent Query Understanding and LLM-Based Reranking. arXiv.](https://arxiv.org/html/2601.17692v1)

About rawmktg.

rawmktg. publishes data-led analysis of how search, retrieval and AI answer engines actually work. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Figures are original illustrations built from the cited data. Percentages are drawn from published third-party measurements and should be read as directional rather than exact.
