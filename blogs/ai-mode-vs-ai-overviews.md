# AI Mode vs AI Overviews

> Google's two AI surfaces share a query box but run different retrieval logic and cite different sources, and a B2B brand has to earn its place in both. How each one decides what to show.

*Source: https://rawmktg.com/blogs/ai-mode-vs-ai-overviews · rawmktg. by Vinayak Ravi*


Google did not add AI to search. It split search into two AI products that share a query box, and they disagree about which sources deserve a citation almost nine times out of ten. For anyone doing GEO, that disagreement is the whole story: you cannot optimize for "Google AI" as a single target. There are two targets, they reward different work, they pull from different places, and a page that wins one can be invisible in the other.

The first surface is [AI Overviews](#architecture): the boxed summary above the blue links. You never ask for it, it fires automatically on roughly a quarter of queries. The second is AI Mode: a separate tab you deliberately select, where search becomes a conversation that remembers what you asked three turns ago. Same box, same brand, two retrieval engines with their own logic, update cadence and citation habits. Across 730,000 paired responses, the same query produces two completely different source lists 86.3% of the time.

## 01. What's behind Google's two AI surfaces?

**Both run on Gemini, but they search a different number of times, touch different indexes, and weigh ranking differently.** AI Overviews is a passive summarization layer stitched into the standard results page. AI Mode is an active, standalone conversational tab the user opts into. That is where the resemblance ends.

AI Overviews - passive summary

- Automatic trigger, fires on ~25% of queries
- Single-pass RAG over the standard index
- Reads top-ranking standard-index docs
- ~200 words, ~21-second session
- Low source diversity, ranking-led

AI Mode - conversational research

- User-activated tab, opted into
- Parallel query fan-out, retrieves many times
- Reads live web + Knowledge Graph + Shopping Graph (50B+ SKUs)
- ~800 words, ~49-second session
- High source diversity, rank-decoupled

AI Overviews is, mechanically, a thin wrapper on classic ranking: it pulls high-ranking documents from the standard index and hands them to a Gemini summarizer. Speed is the point, and the sources skew toward what was already going to rank. AI Mode runs on the Gemini 3 family, keeps conversational context across follow-ups, and crucially does not retrieve once, it retrieves many times, in parallel, against several indexes at once. That single design choice drives the low overlap.

## 02. How does query fan-out break the rules?

**AI Mode shreds your query into sub-queries and runs them concurrently across specialized indexes.** Classic search maps one query to one retrieval path. [AI Mode does not do that](/blogs/how-rag-actually-works). It takes the parent query, decomposes it into sub-queries, and runs them in parallel. The technique is called [query fan-out](/tools/query-fan-out-simulator), and it is why AI Mode cites pages you have never seen rank for the head term.

Decompose

Gemini splits the parent query

→

Parallel retrieval

sub-queries hit many indexes at once

→

Evaluate & extract

isolate the passages that answer each

→

Synthesize & cite

one narrative, many sources

Query fan-out, four stages. A complex question can split into up to 16 concurrent sub-queries pulling live news, spec sheets, pricing feeds and forum threads in one pass.

That parallelism is exactly why AI Mode surfaces deep internal pages, product documentation and niche forum posts that never rank for the primary keyword. It bypasses the single-index bottleneck classic search lives inside. The implication for a brand is blunt: ranking for the head term no longer guarantees you are in the room when the answer gets assembled. It is the same reason [the Google leader is not the AI leader](/blogs/winning-google-isnt-winning-ai) in category after category.

## 03. How much do the two surfaces actually overlap?

**Just 13.7% of cited sources, across 730K paired responses. They draw from largely separate pools.** Here is the number that should reorganize a GEO roadmap. Ahrefs studied 730,000 paired responses and found AI Overviews and AI Mode agreed on sources just 13.7% of the time. It is not an Ahrefs artifact: independent studies land in the same low-overlap neighborhood.

Overlap and concordance studies, 2025-26

| Study | Sample | What was compared | Overlap |
| --- | --- | --- | --- |
| Ahrefs | 730K response pairs | AI Overviews vs AI Mode citations | 13.7% |
| Ahrefs | Top-3 citations | AI Overviews vs AI Mode | 16.3% |
| STAT | 40K keywords | AI Mode URL vs organic top-10 | 12% |
| SE Ranking | Cross-query set | AI Mode URL vs organic (domain: 51%) | 14% |
| BuzzStream | 30K citations, 595 prompts | Citations exclusive to one platform | 76.1% |
| Agency monitor | 12 verticals, Jan-Apr 2026 | AIO-cited page also cited in AI Mode | 15% |

But there is a twist that changes how you read all of this. Low source overlap does not mean the two surfaces give different answers. They mostly do not. The disagreement is about citations, not conclusions.

similarity.py - URL sets vs answer text

python

```
# 1 / URL overlap - how many cited links are shared?
jaccard(A, B) = |A ∩ B| / |A ∪ B|
   A = AI Overviews cited-URL set
   B = AI Mode cited-URL set
   result ≈ 0.137   # low. the links barely intersect.

# 2 / answer overlap - do the two texts agree?
cosine(u, v) = (u · v) / (||u|| · ||v||)
   u = embed(AIO answer)
   v = embed(AI Mode answer)
   result ≈ 0.86    # high. the conclusions converge.
```

Both surfaces reach the same conclusion nine times out of ten. They just cite entirely different sources, in different language, to get there.

That gap is the GEO opportunity stated precisely. The conclusion is not the prize, the citation is. Two brands can both be "the answer" while only one gets named and linked. Your job is not to be correct, the model is already correct without you. Your job is to be the source it reaches for when it justifies the answer, and because the two surfaces reach for different sources, you have to earn that slot twice.

## 04. How does each surface treat your organic ranking?

**Opposite relationships: AI Overviews tracks it, AI Mode is decoupled from it.** This is where the dual-track strategy comes from. The two surfaces have opposite relationships with classic ranking, and that contrast decides which tactics you point at which surface.

Figure 1 - share of cited URLs that match the organic top-10 for the same query. AI Overviews 38%; AI Mode just 12%.

AI Overviews - tracks organic

- 38% of cited URLs rank in the organic top 10
- Organic-rank share of citations climbed 32.3% to 54.5% (mid-2024 to late-2025)
- Healthcare and other YMYL verticals reach 75.3%
- If you can rank, you can largely earn the Overview

AI Mode - decoupled

- Only ~12% of cited URLs match the exact organic top-10 (14% per SE Ranking)
- Domain-level overlap is ~51%: it knows your site
- It pulls the buried comparison page, the docs, the data study
- Your homepage is not the asset, your depth is

Read those in sequence. AI Overviews still respects classic ranking signals, and the dependency is strengthening over time. AI Mode refuses that shortcut: it recognizes your site as authoritative but declines to cite your money landing page, reaching instead for the deep internal resource that resolves a specific sub-query. The work that wins each surface is [not the same](/blogs/why-engines-recommend-different-vendors).

## 05. What does the split look like on real prompts?

**Complex multi-intent queries diverge hard; flat factual queries collapse onto the same canonical sources.** Theory is cheap. Here is what the split looks like on real prompts. The first query is complex and multi-intent, the kind that triggers full fan-out. The second is a flat factual entity query, the one situation where both surfaces collapse onto the same sources.

AI Overviews - "smart ring vs watch vs mat?"

- One short paragraph of summary
- Cites three top-ranking product-review URLs
- Leans on authoritative health portals
- Clean, fast, shallow

AI Mode - same question

- Fan-out splits it: sensor specs, battery life, medical accuracy
- A comparative layout with spec cards
- Cites a dozen-plus sources: Reddit, product docs, niche publications
- Runs a research project, not a summary

The exception that proves the mechanic

Ask a flat factual question, "What products does Adidas offer?", and every surface, including third-party models, converges on the same foundational sources: the annual report, the investor-relations portal, and Wikipedia. Wikipedia carries 35% of citations shared across AI engines despite being only 3.8% of total citations. Factual identity queries pull from canonical sources, so the surfaces agree.

The pattern is consistent: the more a query needs to be reasoned across dimensions, the more fan-out engages and the more the two surfaces split apart. Most B2B buying questions, "best X for Y", "X vs Y", "how do teams handle Z", are exactly the multi-intent prompts that maximize divergence, which is why B2B brands feel the split harder than consumer ones.

## 06. Who does AI Mode actually cite?

**A concentrated mix: the top five domains take 38%, and Google's own properties take 22.8%.** If 13.7% tells you the surfaces differ, the domain mix tells you how, and where the oxygen for external brands actually is. AI Mode concentrates its citations hard, and three of its top five domains are Google's own.

Figure 2 - AI Mode citation share by domain, top 5. Three of the five (YouTube, blog.google, Google.com) are Google-owned, 22.8% of the total.

Two trends inside that chart matter for planning. Self-citation is rising fast: Google.com citations tripled between mid-2025 and early 2026 as help docs and Maps features got wired into the chat interface. And [user-generated content is surging](/blogs/why-ai-cites-reddit-g2-analysts): Reddit citations jumped 450% over three months. AI Overviews behaves differently again, leaning multimodal, with YouTube holding a 23.3% share and a relevant on-page video raising AIO citation odds by 156%.

AI Mode citation behavior, four numbers to plan around

| Metric | Value | What it means |
| --- | --- | --- |
| Sidebar block links | 90.8% | Most citations render as block links, not inline (8.9% inline, 0.3% traditional) |
| URLs surviving 3 runs | 9.2% | Run the same query 3x and only 9.2% of URLs persist; 60%+ of domains rotate |
| Reddit citation rise | 450% | Over a three-month window, reflecting appetite for real-world experience |
| On-page video lift | 156% | Increase in AI Overviews citation odds from a relevant video |

The volatility number is the one most teams underweight. AI Mode uses a probabilistic retrieval model that [continuously reshuffles its sources](/blogs/30-day-content-half-life-recency-ai-ranking-signal), so you are not chasing a fixed ranking that holds still once you win it. You are raising your inclusion odds across a distribution that re-rolls on every query, which reframes the whole measurement question.

## 07. How do you appear in Google AI Mode?

**Semantic depth and entity authority, not keyword density. Three levers, in order of leverage.** Because AI Mode is conversational and runs on fan-out, the work that earns citations is depth and authority. Three levers.

### Lever 01 - Structure pages for extraction

After every target H2, lead with a direct, self-contained answer of [40 to 55 words](/tools/answer-block-optimizer) before any narrative, matching Gemini's extraction patterns. Treat each H2 as a [standalone answer](/blogs/anatomy-of-a-high-citation-page) and phrase headings as natural questions. Cut conversational filler: statistics with clear source citations lift citation probability by 40% to 70%. Apply [FAQPage, Article and Product schema](/blogs/schema-markup-ai-citations-2026) so crawlers can parse and credit claims.

### Lever 02 - Build off-site co-citation

Participate in relevant [Reddit, Quora and Stack Overflow threads](/blogs/reddit-geo-playbook), AI Mode leans on UGC for real-world reviews, so mentions in high-engagement threads convert directly into citation rate. Build YouTube guides (Gemini treats transcripts as text, so speak your brand and methodology terms clearly). And keep LinkedIn, Crunchbase, G2 and Capterra profiles detailed and current, because the Knowledge Graph and Shopping Graph use them to verify entity relationships during comparisons.

### Lever 03 - Measure the right thing

Track Brand Inclusion Rate (is your brand present in the synthesized answer at all), Mention and Citation Rate (where your name is generated and your URL explicitly linked), and [Share of AI Voice](/blogs/prompt-to-citation-tracking) (your citation volume against competitors across a fixed prompt set, plus co-citation mapping). This lever forces teams to abandon a fifteen-year-old dashboard, because 93% of AI Mode sessions end without a click. Click-through rate, rank position and traffic volume are measuring a door almost nobody walks through anymore.

Legacy metrics - retire these

- Click-through rate (CTR)
- Keyword rank position
- Page impressions
- Organic traffic volume

Generative metrics - track these

- Brand Inclusion Rate
- Mention Rate %
- Share of AI Voice (SOAV)
- Sentiment & co-citation mapping

## 08. What's the dual-track takeaway?

**AI Overviews reward the page; AI Mode rewards the brand. You run both tracks at once.** One sentence carries the strategy. The architectural split forces a parallel approach, because the tactics that win one surface do almost nothing for the other.

The dual-track alignment

| Dimension | AI Overviews | AI Mode |
| --- | --- | --- |
| Optimize for | Page-level ranking | Domain-level authority |
| Core tactic | 40-55 word direct summaries | Multi-platform mentions |
| Content shape | Direct, comparative tables | Modular informational hubs |
| Wins on | Top-10 rankings + schema | Proprietary research + off-site presence |
| Scoreboard | Citation share vs rank | Inclusion rate vs competitors |

AI Overviews is, at bottom, a ranking game with a summarization layer bolted on top. Win it with structured data, concise summary blocks and the top-10 positions you already chase. AI Mode is an authority game decided before the click that never comes. Win it with comprehensive topic coverage, proprietary research worth citing, and a presence on the platforms it trusts more than your own homepage.

The bottom line

Optimize for one surface and you are half-visible. The brands that hold organic visibility through this shift run both tracks at once, treating Google not as one AI to please but as two engines that have to be earned separately. The 13.7% overlap is not a problem to solve. It is the map.

Sources & further reading

1. [Ahrefs - Are AI Mode and AI Overviews just different versions of the same answer? (730K responses)](https://ahrefs.com/blog/ai-overviews-vs-ai-mode/)
2. [Moz - Only 12% of AI Mode citations match URLs in the organic SERP](https://moz.com/blog/ai-mode-citations)
3. [BrightEdge - AI Overview citations now 54% from organic rankings](https://www.brightedge.com/resources/weekly-ai-search-insights/rank-overlap-after-16-months-of-aio)
4. [Ahrefs - 38% of AI Overview citations pull from the top 10](https://ahrefs.com/blog/ai-overview-citations-top-10/)
5. [BuzzStream - AI citation overlap: do AI platforms cite the same sites?](https://www.buzzstream.com/blog/ai-citation-overlap/)
6. [Aleyda Solis - Google's query fan-out technique and what it means for SEO](https://www.aleydasolis.com/en/ai-search/google-query-fan-out/)
7. [Google - Optimizing your website for generative AI features in Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
8. [Semrush - What is Google AI Mode (and how to optimize for it)](https://www.semrush.com/blog/google-ai-mode/)

Free interactive tool

Score your dual-track AI visibility

Rate the AI Overviews track and the AI Mode track separately to see which gaps are costing you citations on each surface.

AI Overviews track, win the page 100 pts

Ranks in the organic top 10 for target terms

NoPartialYes

40-55 word direct answer after each H2

NoPartialYes

FAQPage / Article / Product schema deployed

NoPartialYes

Direct, comparative tables and scannable blocks

NoPartialYes

A relevant on-page video

NoPartialYes

Dense factual prose with stats and sources

NoPartialYes

AI Mode track, win the brand 100 pts

Deep, modular topic hubs beyond money pages

NoPartialYes

Proprietary research or original data worth citing

NoPartialYes

Off-site co-citation: Reddit, Quora, forums

NoPartialYes

Accurate G2, Capterra, Crunchbase, LinkedIn profiles

NoPartialYes

YouTube presence with clean transcripts

NoPartialYes

Questions-as-headings, each a standalone answer

NoPartialYes

AI Overviews track

0/100

AI Mode track

0/100

-

A weighted self-assessment of the two tracks Google AI rewards separately. AI Overviews scores page-level ranking and extraction; AI Mode scores domain depth, off-site co-citation and freshness. Weights reflect each lever's pull on citations; real results depend on execution and competition.

A free rawmktg tool. [Open the full tool →](/tools/dual-track-visibility-scorecard) · [see all tools](/tools)

Frequently Asked Questions

### What is the difference between Google AI Overviews and AI Mode?

AI Overviews is the boxed summary that fires automatically above the blue links on about a quarter of queries; it is a single-pass summary of top-ranking pages. AI Mode is a separate, user-activated conversational tab that runs query fan-out, retrieving many sub-queries in parallel across the live web, Knowledge Graph and Shopping Graph. Both run on Gemini, but they cite the same sources only 13.7% of the time.

### Why do AI Overviews and AI Mode cite different sources?

Because they retrieve differently. AI Overviews summarizes pages that already rank in the standard index, so its sources skew toward classic SEO winners. AI Mode decomposes a query into up to 16 sub-queries and runs them across multiple specialized indexes, surfacing deep pages, documentation and forum threads that never rank for the head term. Across 730K paired responses the two agree on sources just 13.7% of the time, though their answers converge about 86%.

### Does ranking in Google's organic top 10 get me into AI Mode?

Not reliably. Only about 12% of AI Mode's cited URLs match the exact organic top-10 URL for the same query (14% per SE Ranking). Domain-level overlap is higher, around 51%, so AI Mode recognizes your site, it just pulls deeper pages than your money landing page. AI Overviews is the opposite: roughly 38% of its citations rank in the organic top 10, and that dependency is strengthening.

### How do you optimize for Google AI Mode?

Three levers: structure pages for extraction (lead each H2 with a 40-55 word direct answer, add FAQPage and Article schema); build off-site co-citation (Reddit and forum participation, YouTube with clean transcripts, accurate G2/Capterra/Crunchbase profiles); and measure the right thing (Brand Inclusion Rate, Mention and Citation Rate, Share of AI Voice) since 93% of AI Mode sessions end without a click.

About rawmktg.

rawmktg. publishes data-driven explainers and teardowns on how AI search decides what to recommend, pulling citation and SEO data to show exactly where the visibility gaps are. Contact: vinayak@rawmktg.com
