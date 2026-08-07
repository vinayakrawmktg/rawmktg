# Internal Linking for AI Retrieval

> How hub pages, anchor-text density, and crawl-depth rules decide whether your key pages are retrieved in a RAG query chain.

*Source: https://rawmktg.com/blogs/internal-linking-for-ai-retrieval · rawmktg. by Vinayak Ravi*


For two decades the search index was a deterministic, page-centric machine. Crawlers built inverted indexes, lexical models like BM25 scored whole documents on term frequency, and optimization meant keyword placement and passing authority across flat link graphs. LLM answer engines broke that model. Modern search runs on Retrieval-Augmented Generation (RAG): a pipeline that retrieves passages, re-ranks them by semantic relevance, and feeds them to a model as grounding context.

TL;DR, what changes when retrieval goes neural

**RAG retrieves passages, not pages.** It pulls self-contained chunks and re-ranks them by meaning. Content that is mathematically isolated from your site graph is invisible to AI retrievers, no matter how good it is.

**Three levers move the needle:** a Vector-Cluster topology (Anchor Entities, Contextual Bridges, Nuance Nodes), entity-rich anchor text that doubles as a retrieval signal, and a flat crawl depth of 2-3 hops so real-time agents reach your pages before they time out.

**Internal links are the edges** graph-augmented retrievers traverse to compute authority. Optimizing them is now an information-retrieval problem, not a PageRank-plumbing exercise.

## 01. From inverted indexes to vector spaces, what actually changed?

**Search now runs on RAG, which retrieves and re-ranks passages, not pages.** Where SEO optimized for a rank position, Generative Engine Optimization (GEO) optimizes the upstream retrieval phase: getting specific text chunks injected into the model's context window.

The consequence for architecture is blunt. RAG systems do not retrieve whole pages, [they retrieve discrete, self-contained passages](/blogs/how-your-page-gets-retrieved). If an enterprise page holds exceptional content but is structurally isolated from the rest of the site graph, it is effectively invisible to AI retrievers.

Query

user question

→

Retrieve

top passages by vector match

→

Re-rank

by semantic relevance

→

Synthesize

LLM grounds its answer

Figure 1 - legacy whole-page keyword matching gives way to a multi-stage RAG retrieval pipeline that scores passages, not documents.

This also rewrites measurement. AI search introduces AI Dark Traffic, valuable interactions legacy analytics struggle to attribute because they happen inside conversational interfaces via zero-click synthesis or assisted citation clicks. Across finance, technology and travel, AI experiences are estimated to displace 15-68% of traditional organic clicks.

Figure 2 - estimated displacement of traditional organic clicks by AI search, by vertical. Source: industry analyses, 2026

## 02. How does anchor text behave in neural retrieval?

**As a query surrogate, late-interaction models match it token by token.** Early dense retrievers compressed a whole page into one vector, which washes out fine detail in long documents. Late-interaction architectures like ColBERT instead keep token-level representations and score relevance with the MaxSim operator: the sum of maximum cosine similarities between each query token and all document tokens.

MaxSim relevance (ColBERT late interaction)

neural-ir

```
S(q, d) =  SUM   max ( E[q_i] . E[d_j] )
           i in q  j in d

  E[q_i] = contextual embedding of query token i
  E[d_j] = contextual embedding of document token j
  .      = cosine similarity between token embeddings

# Every query token "votes" for its best-matching
# document token; the votes sum into the final score.
```

Token-level matching changes what anchor text is. Under legacy SEO, anchors passed PageRank and matched literal strings. In neural IR they are a direct semantic signal: research on the [Anchor-DR framework](https://arxiv.org/abs/2305.05834) shows web anchors behave as natural query surrogates, contrastive learning aligns the anchor's embedding with the embedding of the page it links to, so the retriever forms a semantic expectation of the target before it reads the body.

### Managing anchor-text density: dilution vs saturation

This reframes the old over-optimization worry. The neural-IR concern is not penalty risk; it is semantic dilution versus semantic saturation. Generic anchors like "click here" pass no context, so the target's MaxSim score declines. Hammering one exact-match keyword across every link constrains the document's vector boundaries and makes it harder to retrieve for long-tail queries. The fix is a diverse anchor-text density: semantic variants, related terms, and conversational questions that describe the precise relationship between source and target.

Figure 3 - retrievability peaks at moderate anchor diversity and collapses under both exact-match saturation and generic dilution.

## 03. How do you design a Vector-Cluster architecture?

**Three page types: Anchor Entities, Contextual Bridges, and Nuance Nodes.** Organize content around its semantic relationships in vector space, not just shared keywords. The Vector-Clustering blueprint replaces the flat star structure with tightly woven semantic neighborhoods that signal deep, cohesive expertise to retrievers.

Anchor Entity

the hub: defines the topic's ontology

→

Nuance Nodes

long-tail, high-info-gain spokes

→

Contextual Bridge

connects to an adjacent cluster

Figure 4 - a Vector-Cluster: an Anchor Entity hub linked to Nuance Nodes and bridged to an adjacent cluster.

**Anchor Entity (the hub).** The semantic center of gravity. Unlike a generic "ultimate guide," it defines the topic's ontology, vocabulary, core concepts, relationships, and leans on JSON-LD plus clean definitions near the top for easy parsing. **Contextual Bridges.** Connectors that reduce semantic distance between clusters, letting models trace cross-topic logic. **Nuance Nodes.** Long-tail, high-density spokes built on [Information Gain](/blogs/anatomy-of-a-high-citation-page), original data, proprietary research, unique case studies that yield clear, quotable, citable facts.

Legacy silo vs Vector-Cluster, side by side

| Criterion | Legacy flat / silo IA | Vector-Cluster IA |
| --- | --- | --- |
| Organizing principle | Shared keywords & manual categories | Semantic proximity in vector space |
| Hub role | Category page passing PageRank | Anchor Entity defining topic ontology |
| Cross-topic links | Avoided to keep silos clean | Contextual Bridges encouraged |
| Anchor text | Exact-match for ranking | Diverse, entity-rich, relationship-describing |
| Unit of value | The ranked page | The retrievable passage / chunk |
| Retrieval outcome | Whole-page ranking | Passage injected into LLM context |

Implementation rule: every Nuance Node links back to its Anchor Entity with descriptive anchors, and Contextual Bridges link across hubs. That structured linking lets RAG systems trace and retrieve relevant passages across your entire domain. This is the on-page side of building [topical authority](/blogs/topical-authority-cluster-ai-shortlists).

## 04. Why does crawl depth now decide what gets retrieved?

**Real-time agents have seconds; keep key pages within 2-3 hops.** Before content can be retrieved it must be reachable. In 2026, AI crawlers split into two camps with opposite incentives.

Training scrapers (throttle / block)

- GPTBot, ClaudeBot, CCBot
- Pull bulk data for future foundation models
- Can consume up to ~40% of server bandwidth
- Often bypass CDN caches; return no referral clicks

Real-time retrieval agents (keep open)

- OAI-SearchBot, ChatGPT-User, PerplexityBot
- Fetch fresh content for active queries
- Respect robots.txt
- Drive the citation traffic that matters

Figure 5 - the 2026 AI crawler taxonomy: bulk training scrapers vs real-time retrieval agents.

That second group is why crawl depth is now a hard constraint. Traditional crawlers index asynchronously over days, so deep hierarchies eventually surface. Real-time agents have seconds to discover, scrape and filter URLs before the model responds. Content buried 4-5 clicks deep is often timed out or discarded before it is reached. This is the same access problem we cover in [how AI crawlers index your site](/blogs/how-ai-crawlers-index-your-site).

Keep every key asset within 2-3 hops of the homepage. Past depth 3, real-time retrieval probability falls off a cliff.

Figure 6 - modeled real-time retrieval probability by crawl depth. The safe zone ends at 3 hops; depth 4-5 is frequently timed out.

Crawl budget also leaks. An enterprise study of 100,000-plus page domains found bots spend roughly 18% of crawl budget on redundant parameter URLs (session IDs, sort filters) when they are not explicitly blocked. Clear robots.txt exclusions steer that budget toward high-signal hubs.

robots.txt, selective AI crawler control (2026)

robots.txt

```
# Goal: keep referral-driving agents in; push bulk
# scrapers and parameter URLs out.

# --- Real-time retrieval agents: ALLOW ---
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: PerplexityBot
Allow: /

# --- Bulk training scrapers: throttle / block ---
User-agent: GPTBot
Disallow: /
User-agent: ClaudeBot
Disallow: /
User-agent: CCBot
Disallow: /

# --- Protect crawl budget from parameter sprawl ---
User-agent: *
Disallow: /*?sessionid=
Disallow: /*?sort=
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Block only what you mean to. Blocking a training bot forfeits potential model exposure; allowing it spends bandwidth for zero referral traffic. Decide per business goal, and keep retrieval agents fully unblocked.

## 05. What is GraphRAG, and why are internal links the edges?

**It fuses vector search with graph traversal, and your links are the graph.** Enterprise retrieval increasingly augments dense vectors with knowledge graphs. [Graph-Augmented RAG (GraphRAG)](https://learn.microsoft.com/en-us/azure/horizondb/ai/graph-rag) pairs vector search with graph traversal to solve multi-hop reasoning, modeling relationships as explicit nodes and edges so the retriever can trace connections across pages.

Dense vector rank

semantic similarity

→

Graph citation rank

in-degree authority

→

Reciprocal Rank Fusion

blend both signals

→

Fused context

sent to the LLM

Figure 7 - GraphRAG fuses vector relevance and graph traversal via Reciprocal Rank Fusion.

Engineers model assets as Entity-Attribute-Value triples (Subject, Predicate, Object). The pipeline runs extraction (pull JSON-LD and triples), deduplication (normalize entity names so "PostgreSQL," "Postgres" and "PG" resolve to one node), and graph construction (load relationships into a graph database). With the graph built, an Authority Boosting query counts each node's in-degree, its citation count, to find the most authoritative hubs.

Authority boosting: in-degree as a hub signal

cypher

```
-- Cypher: rank pages by internal citation count
MATCH (target:Page)<-[r:LINKS_TO]-(:Page)
RETURN target.url AS page,
       count(r)   AS in_degree     -- citation count
ORDER BY in_degree DESC
LIMIT 20;
```

Reciprocal Rank Fusion of vector + graph

python

```
# r_dense = rank from dense vector search
# r_graph = rank from graph citation density
# k       = smoothing constant (typically 4)

def rrf(doc, r_dense, r_graph, k=4):
    return 1.0/(k + r_dense) + 1.0/(k + r_graph)

# Authoritative-but-distinct AND relevant-but-less-linked
# documents both survive into the final context.
```

The payoff is measurable

In controlled tests, adding a graph-augmented overlay to a dense retriever raised the mean cosine similarity of retrieved passages from 0.673 to 0.694 while sharply cutting similarity dispersion. Separately, the Princeton GEO-BENCH study found RAG-optimized content earns up to +40% citation visibility versus unoptimized content. The architectural takeaway: your internal links are the edges graph-augmented retrievers use to map authority.

## 06. What is the B2A layer and the llms.txt standard?

**A machine-readable index agents read instead of parsing your HTML.** Sites are adding Business-to-Agent (B2A) interfaces. The [llms.txt standard](/glossary/llms-txt) is an emerging protocol: a clean, machine-readable index of your most important resources at the domain root, a curated master index (/llms.txt) plus a concatenated full-text bundle (/llms-full.txt).

/llms.txt

markdown

```
# BrandName

> BrandName provides enterprise-grade AI search
> tracking and optimization platforms.

## Core Resources

- [Pricing](https://brand.com/pricing): Startup and
  Enterprise tier structures.
- [Integration Guide](https://brand.com/docs): REST
  API deployment documentation.
- [Vector-Cluster Playbook](https://brand.com/playbook):
  How to structure content for AI retrieval.

## About

- [Company](https://brand.com/about): Who we are and
  why AI visibility matters.
```

The structure is strict: one H1 with the exact brand name, a blockquote summary, H2 groupings, and bullet links in exact - [Title](URL): Description syntax. But set expectations with data: [Ahrefs' analysis of 137,000-plus domains](https://ahrefs.com/blog/llmstxt-study/) shows publishing is rising while reads remain vanishingly rare.

Figure 8 - llms.txt is widely published but rarely read. Source: Ahrefs 137K-domain study

[Direct crawler traffic to /llms.txt is still low](/blogs/does-llms-txt-do-anything-yet), but the file is low-effort, high-upside: a machine-readable source of truth that helps prevent AI engines from misrepresenting your pricing, specs, or brand facts in generated answers.

## 07. Does GEO actually work? The evidence.

**Up to +40% citation visibility on GEO-BENCH, with field case studies to match.** A landmark study from [Princeton, Georgia Tech and IIT Delhi](https://arxiv.org/abs/2311.09735) evaluated these tactics on the GEO-BENCH benchmark and found that optimizing content for RAG pipelines, verifiable facts, direct answers, structured data, boosted citation visibility by up to 40% versus unoptimized content.

Documented GEO outcomes

| Brand / sector | Strategy | Core outcome |
| --- | --- | --- |
| EdTech platform | GEO intent optimization | +1,041% revenue in 5 months; 3x conversion efficiency |
| Auto insurance | Structured FAQ + schema markup | +447% AI Overview mentions in 6 months |
| SEO agency | Semantic SEO & IA optimization | +8,337% ChatGPT sessions; +2,527% engagement time |

In the EdTech case the brand hit a "crocodile mouth" effect: lead volume stayed flat while revenue and conversion efficiency surged. By targeting high-intent transactional terms, optimization filtered out low-quality traffic and surfaced the brand in high-value queries. To evaluate RAG quality, teams use the GTS (Generative Trust Score) framework, scoring retrieval quality, answer relevance, and groundedness.

The core GEO metric set

| Metric | What it captures | Tracking method |
| --- | --- | --- |
| Citation Rate | How often AI tools cite you | Monthly audits across ChatGPT, Perplexity, Gemini |
| Semantic Reach | Breadth of long-tail coverage | Impressions on long-tail query variants |
| Referral Traffic | Assisted clicks from AI answers | UTM tags + AI referrer parsing |
| Brand Sentiment | How AI describes your brand | NLP audits of generated responses |

## 08. What does a retrieval-optimized page look like?

**Answer block and schema up top, entity tables and links in the body, FAQ at the base.** Translate the theory into a build spec, engineered so retrieval agents can extract a clean answer, parse your entities, and follow your links, top to bottom.

Retrieval-optimized page blueprint

**Top:** one H1 naming the primary entity, a 2-3 sentence answer block agents can lift verbatim, and JSON-LD schema.

**Body:** question-format H2/H3s each opening with a direct answer; pricing, specs and comparisons as HTML tables (crawlers parse tables far better than prose); entity-rich contextual links.

**Base:** an FAQ section that mirrors the questions buyers actually ask.

Frame headings as the questions users ask and lead each section with an answer block. Implement schema.org markup (Article, FAQPage, Product, Organization) to give agents a clean semantic layer, the same [structured-data discipline](/blogs/schema-markup-ai-citations-2026) that lifts citations.

Entity schema (JSON-LD)

json

```
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Internal Linking for AI Retrieval",
  "about": { "@type": "Thing", "name": "Generative Engine Optimization" },
  "mentions": [
    { "@type": "Thing", "name": "Retrieval-Augmented Generation" },
    { "@type": "Thing", "name": "Vector-Cluster Architecture" }
  ],
  "author": { "@type": "Organization", "name": "rawmktg." }
}
</script>
```

Replace "click here" with descriptive, entity-rich anchors. Hubs link to every relevant spoke; spokes link back to the hub and laterally to related nodes. Serve content via SSR or clean static HTML so it is visible without heavy JavaScript, keep response times low to avoid crawl timeouts, and fix broken links, redirect chains and stray noindex tags that amputate parts of your topical network.

Map

cluster by vector proximity

→

Structure

schema + answer blocks

→

Link

entity-rich anchors

→

Gate crawl

robots.txt + depth

→

Expose

llms.txt

→

Measure

citations + GTS

Figure 9 - the six-step implementation loop: map, structure, link, gate crawl access, expose machine-readable indexes, measure, repeat.

## 09. What should you actually build?

**Retire authority-passing structures; build a retrievable semantic network.** RAG and GraphRAG engines do not read a site as a flat bag of keywords, they read it as an interconnected semantic network. Shifting to a passage-centric, vector-aligned structure makes your content both retrievable and authoritative.

The roadmap, in five moves

**1. Map content around vector proximity.** Build clusters of Anchor Entities, Contextual Bridges and Nuance Nodes for comprehensive topic coverage.

**2. Strengthen the entity graph.** Use entity-rich contextual anchors and structured schema to make relationships machine-readable.

**3. Optimize crawl accessibility.** Selective robots.txt rules block bandwidth-heavy trainers while keeping referral-driving agents open; hold key assets within 2-3 hops.

**4. Enhance machine readability.** Deploy clean llms.txt and llms-full.txt as a standardized markdown directory.

**5. Focus on Information Gain.** Lead with answer blocks, HTML data tables and FAQs grounded in unique data to secure accurate citations.

Do this and you stop chasing algorithm updates. You build a machine-readable, semantic, highly retrievable knowledge base that performs consistently across every generative engine.

Free interactive tool

Estimate your page's retrieval probability

Enter how many clicks a page sits from your homepage to see whether real-time AI agents can reach it in time.

Clicks from the homepage 3 hops

How many clicks a crawler needs to reach this page from your homepage.

Page is in your sitemap & llms.txt

Discovery files help real-time agents reach deeper pages, worth roughly one hop.

Real-time retrieval probability

70%

depth 3 from the homepage

AT RISK

Reachability

Models real-time retrieval probability by crawl depth (100 / 96 / 88 / 70 / 42 / 20% at depths 0-5), grounded in the internal-linking-for-AI-retrieval research. Real-time agents have seconds to fetch a URL; past depth 3 retrieval falls off a cliff. Directional.

A free rawmktg tool. [Open the full tool →](/tools/crawl-depth-retrieval-estimator) · [see all tools](/tools)

Frequently Asked Questions

### Does internal linking still matter if AI retrieves passages, not pages?

More than ever. RAG retrieves passages, but a passage in a structurally isolated page is hard to discover and re-rank. Internal links are the explicit edges graph-augmented retrievers traverse to compute authority and trace multi-hop relationships, so linking determines whether your best passages are even in the candidate set.

### What is the ideal crawl depth for AI retrieval?

Keep key assets within 2-3 hops of the homepage. Real-time retrieval agents have only seconds to find and scrape URLs; content at depth 4-5 is frequently timed out or discarded before it is reached.

### How is anchor text different in neural IR versus classic SEO?

In classic SEO anchors passed PageRank and matched literal keywords. In neural IR (ColBERT, Anchor-DR) the anchor's embedding is aligned with the target document's embedding, so anchor text acts as a query surrogate that shapes retrievability. Aim for diverse, descriptive anchors, and avoid both generic phrases and exact-match repetition.

### Should I block GPTBot and ClaudeBot in robots.txt?

It depends on your goal. Training scrapers can consume up to ~40% of bandwidth without driving referral traffic, so many sites throttle or block them. But never block real-time retrieval agents like OAI-SearchBot or PerplexityBot, those drive citation traffic.

### Is llms.txt worth implementing given near-zero read rates?

Yes, as cheap insurance. Ahrefs found 97% of llms.txt files get zero monthly requests, but the file is trivial to produce and serves as a machine-readable source of truth that helps prevent AI engines from misrepresenting your pricing or specs.

### What is GraphRAG and why should technical SEOs care?

GraphRAG augments vector search with knowledge-graph traversal to answer multi-hop questions. It models content relationships as nodes and edges and uses in-degree (citation count) for authority boosting via Reciprocal Rank Fusion. Your internal links are those edges, which makes link topology a direct ranking input.

### How do I measure whether GEO is working?

Track four metrics: Citation Rate (audits across AI tools), Semantic Reach (long-tail impressions), Referral Traffic (UTM tags + AI referrer parsing), and Brand Sentiment (NLP audits). For RAG quality, use the GTS framework: retrieval quality, answer relevance, and groundedness.

Sources & further reading

- [ColBERT: Efficient Passage Search via Late Interaction (arXiv)](https://arxiv.org/abs/2004.12832)
- [Anchor-DR: Dense Retrieval Training with Web Anchors (arXiv)](https://arxiv.org/abs/2305.05834)
- [GEO: Generative Engine Optimization, GEO-BENCH (arXiv)](https://arxiv.org/abs/2311.09735)
- [Graph-Augmented RAG patterns (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/horizondb/ai/graph-rag)
- [The Vector-Clustering Blueprint (SteakHouse)](https://blog.trysteakhouse.com/blog/vector-clustering-blueprint-organizing-content)
- [We analyzed 137K sites: 97% of llms.txt files never get read (Ahrefs)](https://ahrefs.com/blog/llmstxt-study/)
- [Why Internal Linking Matters More in AI Search (Quattr)](https://www.quattr.com/blog/internal-linking-overlooked-signal-in-ai)
- [GTS Scoring: a framework to evaluate RAG systems (Sprinklr)](https://engineering.sprinklr.com/gts-scoring-a-practical-actionable-framework-to-evaluate-rag-systems-4e6602d9154a)

About rawmktg.

rawmktg. publishes technical teardowns of how AI search retrieves, ranks and cites content. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com
