#!/usr/bin/env python3
"""SCRATCH: build blogs/internal-linking-for-ai-retrieval.html. Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="internal-linking-for-ai-retrieval"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-13"

def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'")
        .replace("“",'"').replace("”",'"').replace("…","...").replace(" "," "))
    t=re.sub(r"\[\d+(?:,\s*\d+)*\]","",t)   # strip [n] / [n,n] citations
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)

T=open("blogs/property-vista-authority-paradox.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE=''  # AdSense removed: no ad units, hurts TBT

def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest
         else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def h3(t): return f"<h3>{esc(t)}</h3>"
def code(label,body,lang=None):
    lng=f'<span class="code-lang">{esc(lang)}</span>' if lang else ''
    return (f'<div class="code-wrap"><div class="code-label">{esc(label)}</div>'
            f'<div class="code-block">{lng}<pre>{H.escape(body)}</pre></div></div>')
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return (f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div>'
            f'<table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')
def chart(cid,height,caption):
    return (f'<div class="chart-wrap"><canvas id="{cid}" height="{height}"></canvas></div>'
            f'<div class="chart-caption">{esc(caption)}</div>')
def pipeline(nodes,goal_idx,caption):
    parts=['<div class="pipeline">']
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal_idx else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(caption)}</div>'
def compare(ll,litems,rl,ritems,caption):
    li="".join(f"<li>{esc(x)}</li>" for x in litems); ri="".join(f"<li>{esc(x)}</li>" for x in ritems)
    return (f'<div class="compare-grid"><div class="compare-col"><div class="compare-col-label seo">{esc(ll)}</div><ul>{li}</ul></div>'
            f'<div class="compare-col"><div class="compare-col-label geo">{esc(rl)}</div><ul>{ri}</ul></div></div>'
            f'<div class="chart-caption">{esc(caption)}</div>')
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras)
    return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def L(t,u,ext=True):
    a=' target="_blank" rel="noopener"' if ext else ""
    return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Internal Linking for AI Retrieval"
DECK="How hub pages, anchor-text density, and crawl-depth rules decide whether your key pages are retrieved in a RAG query chain."
DESC=("A technical deep dive on internal linking for AI retrieval: late-interaction anchor text, the Vector-Cluster "
      "architecture, a flat 2-3 hop crawl depth, GraphRAG authority, and llms.txt, the link topology that decides "
      "whether your passages get retrieved and cited.")
DATANOTE=("A technical GEO teardown for SEOs and site architects, synthesizing neural-IR research (ColBERT, Anchor-DR), "
          "the Princeton/Georgia Tech/IIT-Delhi GEO-BENCH study, GraphRAG patterns, and the Ahrefs llms.txt analysis. "
          "Figures are illustrative models; example code is illustrative.")

out=[]
out.append('<p class="lead">'+norm("For two decades the search index was a deterministic, page-centric machine. Crawlers built inverted indexes, lexical models like BM25 scored whole documents on term frequency, and optimization meant keyword placement and passing authority across flat link graphs. LLM answer engines broke that model. Modern search runs on Retrieval-Augmented Generation (RAG): a pipeline that retrieves passages, re-ranks them by semantic relevance, and feeds them to a model as grounding context.")+'</p>')
out.append(callout("TL;DR, what changes when retrieval goes neural",[
 "<strong>RAG retrieves passages, not pages.</strong> It pulls self-contained chunks and re-ranks them by meaning. Content that is mathematically isolated from your site graph is invisible to AI retrievers, no matter how good it is.",
 "<strong>Three levers move the needle:</strong> a Vector-Cluster topology (Anchor Entities, Contextual Bridges, Nuance Nodes), entity-rich anchor text that doubles as a retrieval signal, and a flat crawl depth of 2-3 hops so real-time agents reach your pages before they time out.",
 "<strong>Internal links are the edges</strong> graph-augmented retrievers traverse to compute authority. Optimizing them is now an information-retrieval problem, not a PageRank-plumbing exercise.",
]))

# 01
out.append(sec("01","neural","From inverted indexes to vector spaces, what actually changed?","Search now runs on RAG, which retrieves and re-ranks passages, not pages.",
  "Where SEO optimized for a rank position, Generative Engine Optimization (GEO) optimizes the upstream retrieval phase: getting specific text chunks injected into the model's context window."))
out.append(p("The consequence for architecture is blunt. RAG systems do not retrieve whole pages, they retrieve discrete, self-contained passages. If an enterprise page holds exceptional content but is structurally isolated from the rest of the site graph, it is effectively invisible to AI retrievers."))
out.append(pipeline([("Query","user question"),("Retrieve","top passages by vector match"),("Re-rank","by semantic relevance"),("Synthesize","LLM grounds its answer")],3,
  "Figure 1 - legacy whole-page keyword matching gives way to a multi-stage RAG retrieval pipeline that scores passages, not documents."))
out.append(p("This also rewrites measurement. AI search introduces AI Dark Traffic, valuable interactions legacy analytics struggle to attribute because they happen inside conversational interfaces via zero-click synthesis or assisted citation clicks. Across finance, technology and travel, AI experiences are estimated to displace 15-68% of traditional organic clicks."))
out.append(chart("ilDisplacement",200,"Figure 2 - estimated displacement of traditional organic clicks by AI search, by vertical. Source: industry analyses, 2026"))

# 02
out.append(sec("02","anchors","How does anchor text behave in neural retrieval?","As a query surrogate, late-interaction models match it token by token.",
  "Early dense retrievers compressed a whole page into one vector, which washes out fine detail in long documents. Late-interaction architectures like ColBERT instead keep token-level representations and score relevance with the MaxSim operator: the sum of maximum cosine similarities between each query token and all document tokens."))
out.append(code("MaxSim relevance (ColBERT late interaction)",
"""S(q, d) =  SUM   max ( E[q_i] . E[d_j] )
           i in q  j in d

  E[q_i] = contextual embedding of query token i
  E[d_j] = contextual embedding of document token j
  .      = cosine similarity between token embeddings

# Every query token "votes" for its best-matching
# document token; the votes sum into the final score.""","neural-ir"))
out.append(p("Token-level matching changes what anchor text is. Under legacy SEO, anchors passed PageRank and matched literal strings. In neural IR they are a direct semantic signal: research on the "+L("Anchor-DR framework","https://arxiv.org/abs/2305.05834")+" shows web anchors behave as natural query surrogates, contrastive learning aligns the anchor's embedding with the embedding of the page it links to, so the retriever forms a semantic expectation of the target before it reads the body."))
out.append(h3("Managing anchor-text density: dilution vs saturation"))
out.append(p("This reframes the old over-optimization worry. The neural-IR concern is not penalty risk; it is semantic dilution versus semantic saturation. Generic anchors like \"click here\" pass no context, so the target's MaxSim score declines. Hammering one exact-match keyword across every link constrains the document's vector boundaries and makes it harder to retrieve for long-tail queries. The fix is a diverse anchor-text density: semantic variants, related terms, and conversational questions that describe the precise relationship between source and target."))
out.append(chart("ilAnchorCurve",220,"Figure 3 - retrievability peaks at moderate anchor diversity and collapses under both exact-match saturation and generic dilution."))

# 03
out.append(sec("03","cluster","How do you design a Vector-Cluster architecture?","Three page types: Anchor Entities, Contextual Bridges, and Nuance Nodes.",
  "Organize content around its semantic relationships in vector space, not just shared keywords. The Vector-Clustering blueprint replaces the flat star structure with tightly woven semantic neighborhoods that signal deep, cohesive expertise to retrievers."))
out.append(pipeline([("Anchor Entity","the hub: defines the topic's ontology"),("Nuance Nodes","long-tail, high-info-gain spokes"),("Contextual Bridge","connects to an adjacent cluster")],0,
  "Figure 4 - a Vector-Cluster: an Anchor Entity hub linked to Nuance Nodes and bridged to an adjacent cluster."))
out.append('<p>'+norm("<strong>Anchor Entity (the hub).</strong> The semantic center of gravity. Unlike a generic \"ultimate guide,\" it defines the topic's ontology, vocabulary, core concepts, relationships, and leans on JSON-LD plus clean definitions near the top for easy parsing. ")
  +norm("<strong>Contextual Bridges.</strong> Connectors that reduce semantic distance between clusters, letting models trace cross-topic logic. ")
  +norm("<strong>Nuance Nodes.</strong> Long-tail, high-density spokes built on ")+L("Information Gain","/blogs/anatomy-of-a-high-citation-page",ext=False)+norm(", original data, proprietary research, unique case studies that yield clear, quotable, citable facts.")+'</p>')
out.append(table("Legacy silo vs Vector-Cluster, side by side",["Criterion","Legacy flat / silo IA","Vector-Cluster IA"],[
 ("Organizing principle","Shared keywords & manual categories","Semantic proximity in vector space"),
 ("Hub role","Category page passing PageRank","Anchor Entity defining topic ontology"),
 ("Cross-topic links","Avoided to keep silos clean","Contextual Bridges encouraged"),
 ("Anchor text","Exact-match for ranking","Diverse, entity-rich, relationship-describing"),
 ("Unit of value","The ranked page","The retrievable passage / chunk"),
 ("Retrieval outcome","Whole-page ranking","Passage injected into LLM context"),
], cls=lambda j,c: "label" if j==0 else ("up" if j==2 else "")))
out.append(p("Implementation rule: every Nuance Node links back to its Anchor Entity with descriptive anchors, and Contextual Bridges link across hubs. That structured linking lets RAG systems trace and retrieve relevant passages across your entire domain. This is the on-page side of building "+L("topical authority","/blogs/topical-authority-cluster-ai-shortlists",ext=False)+"."))

# 04
out.append(sec("04","crawl-depth","Why does crawl depth now decide what gets retrieved?","Real-time agents have seconds; keep key pages within 2-3 hops.",
  "Before content can be retrieved it must be reachable. In 2026, AI crawlers split into two camps with opposite incentives."))
out.append(compare("Training scrapers (throttle / block)",
 ["GPTBot, ClaudeBot, CCBot","Pull bulk data for future foundation models","Can consume up to ~40% of server bandwidth","Often bypass CDN caches; return no referral clicks"],
 "Real-time retrieval agents (keep open)",
 ["OAI-SearchBot, ChatGPT-User, PerplexityBot","Fetch fresh content for active queries","Respect robots.txt","Drive the citation traffic that matters"],
 "Figure 5 - the 2026 AI crawler taxonomy: bulk training scrapers vs real-time retrieval agents."))
out.append(p("That second group is why crawl depth is now a hard constraint. Traditional crawlers index asynchronously over days, so deep hierarchies eventually surface. Real-time agents have seconds to discover, scrape and filter URLs before the model responds. Content buried 4-5 clicks deep is often timed out or discarded before it is reached. This is the same access problem we cover in "+L("how AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site",ext=False)+"."))
out.append(pull("Keep every key asset within 2-3 hops of the homepage. Past depth 3, real-time retrieval probability falls off a cliff."))
out.append(chart("ilCrawlDepth",260,"Figure 6 - modeled real-time retrieval probability by crawl depth. The safe zone ends at 3 hops; depth 4-5 is frequently timed out."))
out.append(p("Crawl budget also leaks. An enterprise study of 100,000-plus page domains found bots spend roughly 18% of crawl budget on redundant parameter URLs (session IDs, sort filters) when they are not explicitly blocked. Clear robots.txt exclusions steer that budget toward high-signal hubs."))
out.append(code("robots.txt, selective AI crawler control (2026)",
"""# Goal: keep referral-driving agents in; push bulk
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

Sitemap: https://example.com/sitemap.xml""","robots.txt"))
out.append(p("Block only what you mean to. Blocking a training bot forfeits potential model exposure; allowing it spends bandwidth for zero referral traffic. Decide per business goal, and keep retrieval agents fully unblocked."))

# 05
out.append(sec("05","graphrag","What is GraphRAG, and why are internal links the edges?","It fuses vector search with graph traversal, and your links are the graph.",
  "Enterprise retrieval increasingly augments dense vectors with knowledge graphs. "+L("Graph-Augmented RAG (GraphRAG)","https://learn.microsoft.com/en-us/azure/horizondb/ai/graph-rag")+" pairs vector search with graph traversal to solve multi-hop reasoning, modeling relationships as explicit nodes and edges so the retriever can trace connections across pages."))
out.append(pipeline([("Dense vector rank","semantic similarity"),("Graph citation rank","in-degree authority"),("Reciprocal Rank Fusion","blend both signals"),("Fused context","sent to the LLM")],2,
  "Figure 7 - GraphRAG fuses vector relevance and graph traversal via Reciprocal Rank Fusion."))
out.append(p("Engineers model assets as Entity-Attribute-Value triples (Subject, Predicate, Object). The pipeline runs extraction (pull JSON-LD and triples), deduplication (normalize entity names so \"PostgreSQL,\" \"Postgres\" and \"PG\" resolve to one node), and graph construction (load relationships into a graph database). With the graph built, an Authority Boosting query counts each node's in-degree, its citation count, to find the most authoritative hubs."))
out.append(code("Authority boosting: in-degree as a hub signal",
"""-- Cypher: rank pages by internal citation count
MATCH (target:Page)<-[r:LINKS_TO]-(:Page)
RETURN target.url AS page,
       count(r)   AS in_degree     -- citation count
ORDER BY in_degree DESC
LIMIT 20;""","cypher"))
out.append(code("Reciprocal Rank Fusion of vector + graph",
"""# r_dense = rank from dense vector search
# r_graph = rank from graph citation density
# k       = smoothing constant (typically 4)

def rrf(doc, r_dense, r_graph, k=4):
    return 1.0/(k + r_dense) + 1.0/(k + r_graph)

# Authoritative-but-distinct AND relevant-but-less-linked
# documents both survive into the final context.""","python"))
out.append(callout("The payoff is measurable",[
 "In controlled tests, adding a graph-augmented overlay to a dense retriever raised the mean cosine similarity of retrieved passages from 0.673 to 0.694 while sharply cutting similarity dispersion. Separately, the Princeton GEO-BENCH study found RAG-optimized content earns up to +40% citation visibility versus unoptimized content. The architectural takeaway: your internal links are the edges graph-augmented retrievers use to map authority."
]))

# 06
out.append(sec("06","llms-txt","What is the B2A layer and the llms.txt standard?","A machine-readable index agents read instead of parsing your HTML.",
  "Sites are adding Business-to-Agent (B2A) interfaces. The "+L("llms.txt standard","/glossary/llms-txt",ext=False)+" is an emerging protocol: a clean, machine-readable index of your most important resources at the domain root, a curated master index (/llms.txt) plus a concatenated full-text bundle (/llms-full.txt)."))
out.append(code("/llms.txt",
"""# BrandName

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
  why AI visibility matters.""","markdown"))
out.append(p("The structure is strict: one H1 with the exact brand name, a blockquote summary, H2 groupings, and bullet links in exact - [Title](URL): Description syntax. But set expectations with data: "+L("Ahrefs' analysis of 137,000-plus domains","https://ahrefs.com/blog/llmstxt-study/")+" shows publishing is rising while reads remain vanishingly rare."))
out.append(chart("ilAdoption",230,"Figure 8 - llms.txt is widely published but rarely read. Source: Ahrefs 137K-domain study"))
out.append(p("Direct crawler traffic to /llms.txt is still low, but the file is low-effort, high-upside: a machine-readable source of truth that helps prevent AI engines from misrepresenting your pricing, specs, or brand facts in generated answers."))

# 07
out.append(sec("07","evidence","Does GEO actually work? The evidence.","Up to +40% citation visibility on GEO-BENCH, with field case studies to match.",
  "A landmark study from "+L("Princeton, Georgia Tech and IIT Delhi","https://arxiv.org/abs/2311.09735")+" evaluated these tactics on the GEO-BENCH benchmark and found that optimizing content for RAG pipelines, verifiable facts, direct answers, structured data, boosted citation visibility by up to 40% versus unoptimized content."))
out.append(table("Documented GEO outcomes",["Brand / sector","Strategy","Core outcome"],[
 ("EdTech platform","GEO intent optimization","+1,041% revenue in 5 months; 3x conversion efficiency"),
 ("Auto insurance","Structured FAQ + schema markup","+447% AI Overview mentions in 6 months"),
 ("SEO agency","Semantic SEO & IA optimization","+8,337% ChatGPT sessions; +2,527% engagement time"),
], cls=lambda j,c: "label" if j==0 else ("up" if j==2 else "")))
out.append(p("In the EdTech case the brand hit a \"crocodile mouth\" effect: lead volume stayed flat while revenue and conversion efficiency surged. By targeting high-intent transactional terms, optimization filtered out low-quality traffic and surfaced the brand in high-value queries. To evaluate RAG quality, teams use the GTS (Generative Trust Score) framework, scoring retrieval quality, answer relevance, and groundedness."))
out.append(table("The core GEO metric set",["Metric","What it captures","Tracking method"],[
 ("Citation Rate","How often AI tools cite you","Monthly audits across ChatGPT, Perplexity, Gemini"),
 ("Semantic Reach","Breadth of long-tail coverage","Impressions on long-tail query variants"),
 ("Referral Traffic","Assisted clicks from AI answers","UTM tags + AI referrer parsing"),
 ("Brand Sentiment","How AI describes your brand","NLP audits of generated responses"),
], cls=lambda j,c: "label" if j==0 else ""))

# 08
out.append(sec("08","blueprint","What does a retrieval-optimized page look like?","Answer block and schema up top, entity tables and links in the body, FAQ at the base.",
  "Translate the theory into a build spec, engineered so retrieval agents can extract a clean answer, parse your entities, and follow your links, top to bottom."))
out.append(callout("Retrieval-optimized page blueprint",[
 "<strong>Top:</strong> one H1 naming the primary entity, a 2-3 sentence answer block agents can lift verbatim, and JSON-LD schema.",
 "<strong>Body:</strong> question-format H2/H3s each opening with a direct answer; pricing, specs and comparisons as HTML tables (crawlers parse tables far better than prose); entity-rich contextual links.",
 "<strong>Base:</strong> an FAQ section that mirrors the questions buyers actually ask.",
]))
out.append(p("Frame headings as the questions users ask and lead each section with an answer block. Implement schema.org markup (Article, FAQPage, Product, Organization) to give agents a clean semantic layer, the same "+L("structured-data discipline","/blogs/schema-markup-ai-citations-2026",ext=False)+" that lifts citations."))
out.append(code("Entity schema (JSON-LD)",
"""<script type="application/ld+json">
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
</script>""","json"))
out.append(p("Replace \"click here\" with descriptive, entity-rich anchors. Hubs link to every relevant spoke; spokes link back to the hub and laterally to related nodes. Serve content via SSR or clean static HTML so it is visible without heavy JavaScript, keep response times low to avoid crawl timeouts, and fix broken links, redirect chains and stray noindex tags that amputate parts of your topical network."))
out.append(pipeline([("Map","cluster by vector proximity"),("Structure","schema + answer blocks"),("Link","entity-rich anchors"),("Gate crawl","robots.txt + depth"),("Expose","llms.txt"),("Measure","citations + GTS")],5,
  "Figure 9 - the six-step implementation loop: map, structure, link, gate crawl access, expose machine-readable indexes, measure, repeat."))

# 09
out.append(sec("09","summary","What should you actually build?","Retire authority-passing structures; build a retrievable semantic network.",
  "RAG and GraphRAG engines do not read a site as a flat bag of keywords, they read it as an interconnected semantic network. Shifting to a passage-centric, vector-aligned structure makes your content both retrievable and authoritative."))
out.append(callout("The roadmap, in five moves",[
 "<strong>1. Map content around vector proximity.</strong> Build clusters of Anchor Entities, Contextual Bridges and Nuance Nodes for comprehensive topic coverage.",
 "<strong>2. Strengthen the entity graph.</strong> Use entity-rich contextual anchors and structured schema to make relationships machine-readable.",
 "<strong>3. Optimize crawl accessibility.</strong> Selective robots.txt rules block bandwidth-heavy trainers while keeping referral-driving agents open; hold key assets within 2-3 hops.",
 "<strong>4. Enhance machine readability.</strong> Deploy clean llms.txt and llms-full.txt as a standardized markdown directory.",
 "<strong>5. Focus on Information Gain.</strong> Lead with answer blocks, HTML data tables and FAQs grounded in unique data to secure accurate citations.",
]))
out.append(p("Do this and you stop chasing algorithm updates. You build a machine-readable, semantic, highly retrievable knowledge base that performs consistently across every generative engine."))

# FAQ
FAQ=[
 ("Does internal linking still matter if AI retrieves passages, not pages?","More than ever. RAG retrieves passages, but a passage in a structurally isolated page is hard to discover and re-rank. Internal links are the explicit edges graph-augmented retrievers traverse to compute authority and trace multi-hop relationships, so linking determines whether your best passages are even in the candidate set."),
 ("What is the ideal crawl depth for AI retrieval?","Keep key assets within 2-3 hops of the homepage. Real-time retrieval agents have only seconds to find and scrape URLs; content at depth 4-5 is frequently timed out or discarded before it is reached."),
 ("How is anchor text different in neural IR versus classic SEO?","In classic SEO anchors passed PageRank and matched literal keywords. In neural IR (ColBERT, Anchor-DR) the anchor's embedding is aligned with the target document's embedding, so anchor text acts as a query surrogate that shapes retrievability. Aim for diverse, descriptive anchors, and avoid both generic phrases and exact-match repetition."),
 ("Should I block GPTBot and ClaudeBot in robots.txt?","It depends on your goal. Training scrapers can consume up to ~40% of bandwidth without driving referral traffic, so many sites throttle or block them. But never block real-time retrieval agents like OAI-SearchBot or PerplexityBot, those drive citation traffic."),
 ("Is llms.txt worth implementing given near-zero read rates?","Yes, as cheap insurance. Ahrefs found 97% of llms.txt files get zero monthly requests, but the file is trivial to produce and serves as a machine-readable source of truth that helps prevent AI engines from misrepresenting your pricing or specs."),
 ("What is GraphRAG and why should technical SEOs care?","GraphRAG augments vector search with knowledge-graph traversal to answer multi-hop questions. It models content relationships as nodes and edges and uses in-degree (citation count) for authority boosting via Reciprocal Rank Fusion. Your internal links are those edges, which makes link topology a direct ranking input."),
 ("How do I measure whether GEO is working?","Track four metrics: Citation Rate (audits across AI tools), Semantic Reach (long-tail impressions), Referral Traffic (UTM tags + AI referrer parsing), and Brand Sentiment (NLP audits). For RAG quality, use the GTS framework: retrieval quality, answer relevance, and groundedness."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')

SOURCES=[
 ("ColBERT: Efficient Passage Search via Late Interaction (arXiv)","https://arxiv.org/abs/2004.12832"),
 ("Anchor-DR: Dense Retrieval Training with Web Anchors (arXiv)","https://arxiv.org/abs/2305.05834"),
 ("GEO: Generative Engine Optimization, GEO-BENCH (arXiv)","https://arxiv.org/abs/2311.09735"),
 ("Graph-Augmented RAG patterns (Microsoft Learn)","https://learn.microsoft.com/en-us/azure/horizondb/ai/graph-rag"),
 ("The Vector-Clustering Blueprint (SteakHouse)","https://blog.trysteakhouse.com/blog/vector-clustering-blueprint-organizing-content"),
 ("We analyzed 137K sites: 97% of llms.txt files never get read (Ahrefs)","https://ahrefs.com/blog/llmstxt-study/"),
 ("Why Internal Linking Matters More in AI Search (Quattr)","https://www.quattr.com/blog/internal-linking-overlooked-signal-in-ai"),
 ("GTS Scoring: a framework to evaluate RAG systems (Sprinklr)","https://engineering.sprinklr.com/gts-scoring-a-practical-actionable-framework-to-evaluate-rag-systems-4e6602d9154a"),
]
src_items="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in SOURCES)
out.append(f'<div class="sources-block"><div class="sources-label">Sources & further reading</div><ul class="sources-list">{src_items}</ul></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes technical teardowns of how AI search retrieves, ranks and cites content. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("2-3","Max crawl hops for real-time retrieval"),("+40%","Citation lift from GEO-optimized content"),("18%","Crawl budget lost to depth & parameters")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#neural"><span class="toc-num">01</span>The neural shift</a></li>'
     '<li><a href="#anchors"><span class="toc-num">02</span>Anchor text as a signal</a></li>'
     '<li><a href="#cluster"><span class="toc-num">03</span>Vector-Cluster architecture</a></li>'
     '<li><a href="#crawl-depth"><span class="toc-num">04</span>Crawl depth & retrieval</a></li>'
     '<li><a href="#graphrag"><span class="toc-num">05</span>GraphRAG & authority</a></li>'
     '<li><a href="#llms-txt"><span class="toc-num">06</span>The llms.txt layer</a></li>'
     '<li><a href="#evidence"><span class="toc-num">07</span>The evidence</a></li>'
     '<li><a href="#blueprint"><span class="toc-num">08</span>The page blueprint</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div>'
              f'<div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=(f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." '
            f'class="article-header-img" width="2400" height="1260" loading="eager">')

def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),
 "image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,
 "author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},
 "mainEntityOfPage":{"@type":"WebPage","@id":URL},
 "keywords":["internal linking","AI retrieval","RAG","GraphRAG","ColBERT","anchor text","vector cluster","crawl depth","GEO","llms.txt","neural IR","information retrieval"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
 {"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
personLD={"@context":"https://schema.org",**person}

hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;'
      'clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean '
      f'Markdown version of this page is available at {URL}.md. Optimized for AI and LLM tools.</div>')
TITLE="Internal Linking for AI Retrieval: A Technical Deep Dive &middot; rawmktg."
da=escq(DESC)
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
 "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
 f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
 f"  <meta name=\"description\" content=\"{da}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
 "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
 "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
 f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
 f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en-IN" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n  <meta property=\"og:image:width\" content=\"2400\" />\n  <meta property=\"og:image:height\" content=\"1260\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{H.escape(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  {jb(blog)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/blogs/{SLUG}.md\" />\n  "+FONTS+"\n  ")

CHARTS="""
<!-- Chart.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
(function(){
  if(typeof Chart==='undefined') return;
  var css=getComputedStyle(document.documentElement);
  var signal=(css.getPropertyValue('--signal')||'#D04A2A').trim();
  var faint =(css.getPropertyValue('--faint') ||'#C5BFB4').trim();
  var up    =(css.getPropertyValue('--up')||'#3E9B6A').trim();
  var mono="'JetBrains Mono', monospace";
  var text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.45);

  var dp=document.getElementById('ilDisplacement');
  if(dp){new Chart(dp,{type:'bar',data:{labels:['Finance','Technology','Travel'],
    datasets:[{data:[[15,55],[22,60],[30,68]],backgroundColor:signal,borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw[0]+'-'+c.raw[1]+'% of clicks displaced';}}}},
      scales:{x:{beginAtZero:true,max:80,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},
              y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var ac=document.getElementById('ilAnchorCurve');
  if(ac){var xs=['saturation','','','','optimal','','','','dilution'];var ys=[6,14,40,78,100,86,52,22,9];
    new Chart(ac,{type:'line',data:{labels:xs,datasets:[{data:ys,borderColor:signal,backgroundColor:rgba(signal,0.12),fill:true,tension:0.45,borderWidth:2,pointRadius:0}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{enabled:false}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},
              y:{display:false,beginAtZero:true,max:115}}}});}

  var cd=document.getElementById('ilCrawlDepth');
  if(cd){var v=[100,96,88,70,42,20];
    new Chart(cd,{type:'bar',data:{labels:['Depth 0 (home)','Depth 1','Depth 2','Depth 3','Depth 4','Depth 5'],
    datasets:[{data:v,backgroundColor:v.map(function(_,i){return i<=2?up:signal;}),borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% real-time retrieval probability';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(x){return x+'%';}},grid:{color:grid}},
              y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var ad=document.getElementById('ilAdoption');
  if(ad){new Chart(ad,{type:'bar',data:{labels:['Publish llms.txt','Files never read','Bot traffic','From named AI tools','From diagnostic tools'],
    datasets:[{data:[28,97,96,19.5,3.6],backgroundColor:['rgba(255,255,255,0.5)',signal,'rgba(255,255,255,0.5)','rgba(255,255,255,0.5)','rgba(255,255,255,0.5)'],borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'%';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(x){return x+'%';}},grid:{color:grid}},
              y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""

tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Technical GEO Teardown</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">June 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")

final=head+STYLE+"\n  "+ADSENSE+tail
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(final)
hh=open(f"blogs/{SLUG}.html").read()
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),"brackets:",len(re.findall(r'\[\d+\]',hh)),
      "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
      "| tt:",hh.count('class="tt"'),"| pipelines:",hh.count('class="pipeline"'),"| compare:",hh.count('class="compare-grid"'),
      "| code:",hh.count("code-block")-1,"| callout:",hh.count('class="callout-box"'),"| listitem:",hh.count('role="listitem"'))
