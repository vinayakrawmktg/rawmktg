#!/usr/bin/env python3
"""SCRATCH: build blogs/citation-vs-mention-vs-recommendation.html (measurement taxonomy). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="citation-vs-mention-vs-recommendation"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-08-08"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("'","'").replace("'","'").replace(""",'"').replace(""",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE=''  # AdSense removed: no ad units, hurts TBT
CBCOPY=open("blogs/schema-markup-ai-citations-2026.html",encoding="utf-8").read()
mcb=re.search(r'<style id="cb-copy-css">.*?</script>', CBCOPY, re.S); CB=mcb.group(0) if mcb else ""

def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def h3(t): return f"<h3>{esc(t)}</h3>"
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div><table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def chart(cid,h,cap): return f'<div class="chart-wrap"><canvas id="{cid}" height="{h}"></canvas></div><div class="chart-caption">{esc(cap)}</div>'
def statgrid(items):
    cells="".join(f'<div class="sg-item"><div class="sg-val">{esc(v)}</div><div class="sg-label">{esc(l)}</div></div>' for v,l in items)
    return f'<div class="stat-grid">{cells}</div>'
def pipeline(nodes,goal,cap):
    parts=['<div class="pipeline">']
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Citation vs Mention vs Recommendation"
DECK=("Three words that get used interchangeably in GEO decks. They describe three different subsystems, three different failure "
      "modes, and three different fixes. Here is the measurement taxonomy, the math behind each one, and what the data actually says.")
DESC=("Mentions, citations and recommendations are three different AI-search signals with three different fixes. The measurement "
      "taxonomy, the formulas to score each, and what the evidence shows.")
DATANOTE=("A measurement-taxonomy teardown grounded in the Princeton/Georgia Tech GEO experiment (KDD 2024), the GEO-at-scale "
          "benchmark (102 brands, 102,025 responses), and the 75,000-brand correlation analysis, 2024-26. Formulas and code are "
          "working reference implementations; figures are drawn from the cited studies.")

CODE_VIS=r'''from collections import defaultdict

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
    return {p: round(100 * hits[p] / issued[p], 1) for p in issued}'''

CODE_SENT=r'''def sentiment_index(mentions):
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
               resolvable={"RivalA", "RivalB"})                    # 24.7'''

CODE_JAC=r'''from itertools import combinations

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
# treat anything above 0.35 as a suspiciously narrow prompt set'''

CODE_HTML=r'''<!-- BEFORE: narrative, hedged, unextractable -->
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
Deployment Benchmark, n=1,240</a></p>'''

CODE_JSONLD=r'''{
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
}'''

FAQ=[
 ("What is the difference between a mention, a citation, and a recommendation in AI search?",
  "A mention is your brand name appearing in text anywhere on the web, linked or not; it feeds the model's parametric memory and answers whether the machine knows you exist. A citation is an engine attributing a specific claim to a specific URL; it comes from live non-parametric retrieval and answers whether the machine treats your page as evidence. A recommendation is the engine naming you as a good choice at the synthesis layer, and answers whether the machine picks you."),
 ("Do brand mentions without links actually matter for AI visibility?",
  "Yes, but through a different mechanism than links. Unlinked mentions build entity prominence and co-citation, which is what a language model retains in its weights, rather than passing PageRank equity. In a 75,000-brand analysis, branded web mentions correlated with AI Overview visibility at 0.664 versus 0.218 for referring domains. Quality of context matters: low-quality mentions on scraped content farms do little."),
 ("What percentage of AI citations point to a brand's own website?",
  "About 2.9%. In production measurement, roughly 97.1% of citations in AI answers point to third-party domains, comparison listicles, communities like Reddit and YouTube, and reference and trade sites, rather than the brand's own domain. Your website is where you convert attention, not where you earn it."),
 ("Which off-page signal correlates most strongly with AI visibility?",
  "YouTube mentions, at a Spearman correlation of 0.737, ahead of branded web mentions at 0.664. Video transcripts are dense, conversational, entity-rich text that models ingest readily. Every mention-class signal outranked every link-class signal in the data, and raw content volume was the weakest predictor at 0.194."),
 ("How should you measure AI visibility across engines?",
  "Use a fixed prompt set of 20 to 50 discovery and comparison prompts, run it 3 to 5 times per engine to smooth out non-determinism, and compute a platform-weighted visibility score rather than a pooled average. Track mean recommendation position, a contextual sentiment index, and entity share of voice against a verified competitor set, and report per-engine deltas rather than one blended number."),
]

out=[]
# intro
out.append(p("For nearly thirty years the currency of off-page SEO was the hyperlink. A link was a countable, directional vote. PageRank turned those votes into a graph, and the graph decided who ranked. The model was crude but honest: more good links, more authority, better position."))
out.append(p("That model is now one input among several. Large language models and "+L("retrieval-augmented generation","/blogs/how-rag-actually-works")+" have created an evaluation environment where the machine does not hand back ten blue links. It reads, it decides, and it writes an answer. Somewhere inside that process your brand is either present or absent, either trusted or ignored, either recommended or skipped."))
out.append(p("Three signals govern that outcome: mentions, citations, and recommendations. In marketing conversation they get flattened into one idea, usually described as "AI visibility". Inside the machine they are produced by different subsystems, stored in different places, and measured with different math. Confusing them is the reason so many GEO programmes stall."))
out.append(pull("You cannot fix a mention problem with better on-page content, and you cannot fix a citation problem with more press coverage."))
out.append(p("This article separates the three properly. It defines each one mechanically, gives you the formulas used to score them, walks through the empirical evidence for each, and ends with a diagnostic you can run against your own brand this week."))

# 1 short version
out.append(sec("01","short","What is the difference between a mention, a citation, and a recommendation?",
 "They are three signals from three subsystems.","A mention feeds parametric memory (does the machine know you exist). A citation comes from non-parametric retrieval (does the machine treat your page as evidence). A recommendation happens at synthesis (does the machine pick you). They stack, and each gap has a different cause."))
out.append(p("If you read nothing else, read this:"))
out.append("<ul>"
 "<li><strong>A mention</strong> is your brand name appearing in text anywhere on the web, linked or not. It feeds parametric memory, the knowledge baked into a model's weights. It answers: does the machine know you exist.</li>"
 "<li><strong>A citation</strong> is an engine attributing a specific claim in its answer to a specific URL. It comes from non-parametric retrieval, the live fetch that happens when someone submits a prompt. It answers: does the machine treat your page as evidence.</li>"
 "<li><strong>A recommendation</strong> is the engine naming you as a good choice. It happens at the synthesis layer, after retrieval, when the model weighs options against each other. It answers: does the machine pick you.</li></ul>")
out.append(p("They stack. Mentions build the prior. Citations ground the answer. Recommendations convert. You can have all the mentions in the world and never get cited. You can get cited constantly and never get recommended. Each gap has a different cause."))
out.append(pipeline([("Mention","Awareness. Entity known to the model's weights."),("Citation","Trust. Page selected as evidence at retrieval."),("Recommendation","Selection. Named as the pick at synthesis.")],2,
 "Figure 1. The three signals map onto three layers of a generative search system, and form a funnel: awareness, trust, selection."))

# 2 why now
out.append(sec("02","why","Why does separating these three signals matter now?",
 "Because the signals have decoupled.","In classical search they moved together, a mention earned a link, the link moved the ranking, the ranking drove the click. Generative engines broke that chain, so link count is now a poor proxy for whether a machine will name you."))
out.append(p("A mention on Reddit with no link can lift your presence in ChatGPT answers while doing nothing for your Google position. A page that ranks eleventh on Google can be the single source an AI Overview cites, because "+L("retrieval and ranking are separate operations","/blogs/how-your-page-gets-retrieved")+". And a brand can be cited as a source in an answer that ends up recommending a competitor, which is the most frustrating outcome of all."))
out.append(p("Two data points make the scale of the change concrete. In a correlation study of 75,000 brands, branded web mentions correlated with AI Overview visibility at 0.664 while referring domains managed 0.218. And longitudinal data suggests backlinks accounted for roughly 80% of off-page ranking influence in 2012 and around 45% by 2026, with mentions, entity prominence, and co-citation absorbing the difference."))
out.append(chart("shiftChart",230,"Figure 3. The composition of off-page influence has shifted from link-class signals toward mention-class signals, 2012 to 2026."))
out.append(p("Neither number means links are dead. Links still move classical rankings, and classical rankings still feed the retrieval indices these engines query. What the numbers mean is that link count is now a poor proxy for the thing you actually care about: whether a machine will name you when a buyer asks it a question. This is the same gap covered in "+L("winning Google is not winning AI","/blogs/winning-google-isnt-winning-ai")+"."))

# 3 definitions
out.append(sec("03","definitions","How is each signal actually defined?",
 "By the mechanism that produces it, not how it looks.","Two things can look identical in an AI answer and be produced by completely different parts of the system. Mentions come from entity recognition, citations from retrieval grounding, recommendations from synthesised choice."))
out.append(h3("The mention: entity recognition and parametric association"))
out.append(p("A mention is an unlinked or linked textual reference to an entity, a brand, a product, an executive, or a proprietary term, occurring in published digital text. The defining property is that no anchor tag is required. A plain string of text carries the signal."))
out.append(p("Mechanically, mentions operate at entity extraction and parametric encoding. When crawlers and training pipelines ingest unstructured text, NLP models run Named Entity Recognition to map a string to a node in a knowledge graph. Two derived signals matter more than the raw count:"))
out.append("<ul><li><strong>Co-occurrence</strong> is the spatial proximity of your brand string to topical keywords inside a sentence, paragraph, or chunk. It teaches the machine what you are.</li>"
 "<li><strong>Co-citation</strong> is the appearance of two or more entities inside the same document or thematic context. It teaches the machine who you sit next to.</li></ul>")
out.append(p("Co-citation is the underrated one. If your name appears in the same paragraph as three established category leaders often enough, the machine starts treating you as a member of that set. That is not a metaphor; it is a property of how embeddings cluster, and it is the core of "+L("becoming an entity","/blogs/becoming-an-entity")+"."))
out.append(p("The precedent for counting unlinked mentions goes back to Google's 2012 implied-links patent (US8682892B1), which describes systems that identify references to external resources without explicit hyperlinks and treat them as implied endorsements. The honest reading: implied links do not pass classic PageRank equity, but they do establish entity prominence, and entity prominence is what a language model retains."))
out.append(callout("An honest counter-argument",["Some link-building practitioners maintain that mentions without links do very little for classical rankings, and on that narrow point they are largely right. The correlation data concerns AI visibility, not position one on a commercial keyword. Both things can be true at once."]))
out.append(h3("The citation: non-parametric grounding and provenance"))
out.append(p("A citation is an explicit, verifiable reference, usually rendered as a hyperlinked URL, a footnote, or an inline attribution, that an answer engine uses to ground a specific factual claim in its output."))
out.append(p("Citations belong to non-parametric memory. When a prompt arrives, the engine performs a live retrieval step across its index, pulls relevant passages, and loads them into the context window. If the model uses content from one of those passages, it attaches an attribution. The citation is a receipt: the retrieval layer selected your specific chunk of text as evidence for a specific statement."))
out.append(p("This has a consequence most content teams miss. Being cited is not a reward for being authoritative in general. It is a reward for having a passage that was extractable, relevant, and dense with verifiable content at the exact moment a sub-query needed it, exactly the profile described in "+L("the anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page")+". Research on citation implementation consistently finds the same preferences: machine-extractable evidence density, precise statistics, direct expert quotations, and high structural clarity."))
out.append(p("Citations also serve the engine's own interests. They reduce hallucination by tying generated prose to retrievable web evidence, which is why RAG evaluation frameworks treat citation accuracy as a first-class quality metric rather than a courtesy to publishers."))
out.append(h3("The recommendation: synthesised selection"))
out.append(p("A recommendation is an algorithmic endorsement. The system explicitly proposes your brand as a top-tier choice in response to an intent-driven query."))
out.append(p("This happens at the decision layer, after retrieval and during synthesis. Ask an engine which enterprise CRM has the best Slack integration for B2B sales teams and it does not simply look up an answer. It decomposes the question, retrieves candidates across sources, compares attributes, weighs sentiment, and produces a rank-ordered or selective list."))
out.append(p("To issue that recommendation the system combines both memory types. Parametric memory supplies the prior, a sense of who the credible players are. Non-parametric retrieval supplies the current evidence about features, pricing, and third-party opinion. A brand missing from either side struggles: strong prior with weak evidence gets mentioned but not recommended; strong evidence with weak prior gets cited as a source while a better-known competitor gets named as the pick. It is also the only one of the three that maps directly to pipeline, and the endpoint that matters most "+L("when the buyer is a bot","/blogs/when-the-buyer-is-a-bot")+"."))
out.append(h3("Comparative taxonomy matrix"))
out.append(p("The table below is the reference version. If you take one artefact from this article into a strategy document, take this one."))
out.append(table("Table 1. The measurement taxonomy across seven dimensions.",
 ["Dimension","Mention","Citation","Recommendation"],
 [["Primary IR signal","Implicit entity prominence and co-occurrence","Explicit grounding and provenance attribution","Synthesised decision and evaluative choice"],
  ["System memory layer","Parametric memory and knowledge graph","Non-parametric memory and RAG index","Model output and decoded context window"],
  ["Mechanistic trigger","Textual presence, NER, co-citation","Evidence density, extractable stats, schema","Positive sentiment, multi-source consensus, intent match"],
  ["Primary unit","Mention rate, co-occurrence frequency","Citation share, domain attribution count","Recommendation share of voice, mean rank"],
  ["Link dependency","Unlinked or linked, an implied link","Depends on valid, crawlable source URLs","Independent of any direct link"],
  ["Funnel impact","Top of funnel: entity awareness","Mid funnel: trust, verification, referral","Bottom of funnel: conversion, vendor selection"],
  ["Failure mode","Entity ambiguity or negative sentiment","Citation loss from stale or dropped chunks","Exclusion from the day-one consideration set"]],
 cls=lambda j,c: "label" if j==0 else ""))

# 4 how the machine works
out.append(sec("04","machine","How does the machine actually produce these signals?",
 "Across two layers: parametric memory and live retrieval.","Almost every strategic mistake in GEO comes from treating them as one. Mentions live in the frozen weights; citations come from the runtime fetch; the recommendation is synthesised from both."))
out.append(h3("Parametric memory versus non-parametric retrieval"))
out.append(p("Parametric memory is the set of internal parameters, weights, and biases configured during pre-training and reinforcement learning. It is static knowledge, frozen at training time, distilled from enormous web crawls. An entity mentioned heavily across authoritative sources during pre-training becomes embedded in the weights. Ask the model a generic category question and it can name that entity without touching the live web."))
out.append(p("Non-parametric memory is everything external: real-time web indices, vector databases, and retrieval pipelines queried at the moment a prompt runs. It is fresh, swappable, and where citations come from."))
out.append(callout("The rule you can act on",["If your brand is invisible even on prompts where the engine does not search, you have a parametric problem, and the fix is off-page and slow.","If your brand appears in the answer but your URL never shows up in the source list, you have a retrieval problem, and the fix is on-page and fast."]))
out.append(pipeline([("Offline ingestion","Crawls + training bake entities into weights."),("Parametric memory","The prior: who the model already knows."),("Runtime retrieval","Live fetch selects chunks, produces citations."),("Synthesis","Both combine to produce the recommendation.")],3,
 "Figure 4. Offline ingestion builds parametric memory. Runtime retrieval builds citations. Synthesis combines both into the recommendation."))
out.append(h3("Query fan-out, chunking, and context precision"))
out.append(p("Modern generative engines rarely query their index with the sentence the user typed. They use query fan-out: the orchestration layer decomposes the primary prompt into multiple targeted sub-queries. A question about enterprise SaaS CRMs with Slack integrations becomes a fan of narrower searches, integration comparisons, native workflow reviews, category buyer guides, run in parallel, each returning candidate documents."))
out.append(p("Retrieved documents are parsed into chunks, typically 100 to 300 words. A re-ranking model, usually a cross-encoder, scores each chunk for context precision. Chunks that score well share a profile: clear subject-predicate-object structure, exact numeric figures, named sources, and a single self-contained idea. Chunks that score badly are narrative, hedged, and dependent on the paragraph before them for meaning. Empirical work suggests the median length of a passage cited directly by systems like Claude or ChatGPT sits around 40 words."))
out.append(callout("The 40-word rule, stated plainly",["Write the answer to a question in one self-contained passage of roughly 40 words that would still make sense if it were the only thing a machine ever read from your page. Then write everything else around it. This is the single highest-leverage on-page change available in GEO, and it costs nothing but discipline."]))
out.append(h3("The Matthew effect and the brand stature ladder"))
out.append(p("Generative visibility compounds. Information retrieval literature calls this the Matthew effect, the rich getting richer. Language models display a structural bias toward entities with high baseline representation in the training corpus, because that is precisely what parametric memory is. Large-scale analysis across AI engines, published in the GEO-at-scale study covering 102 brands, 3,508 tracking runs, and 102,025 prompt responses, produces a clear ladder:"))
out.append(chart("tierChart",240,"Figure 5. Baseline unbranded visibility by brand stature tier. Each rung down costs roughly 30 percentage points."))
out.append("<ul><li><strong>Tier 1</strong>, global household brands with dense parametric representation, average <strong>72.9%</strong> visibility on unbranded discovery prompts.</li>"
 "<li><strong>Tier 2</strong>, established mid-market and regional brands, sit at <strong>43.6%</strong>.</li>"
 "<li><strong>Tier 3</strong>, niche and small brands without broad co-citation networks, average <strong>11.4%</strong>.</li></ul>")
out.append(p("Because engines look for multi-source corroboration before committing to a commercial recommendation, a Tier 3 brand is not one content refresh away from parity. It has to build the off-site mention footprint that Tier 1 brands accumulated over a decade. The related finding from the same dataset: visibility trajectories stay flat without intervention. Brands do not drift upward on their own."))
out.append(h3("Source composition: earned coverage dominates"))
out.append(p("The most commonly held false belief in this discipline is that optimising your own domain is sufficient. Production measurement refutes it plainly. When AI search engines generate answers and attribute citations, roughly 2.9% of total citations point to the target brand's own website. The other 97.1% point elsewhere."))
out.append(chart("sourceChart",240,"Figure 6. Citation source composition. The brand's own domain is a rounding error at 2.9%."))
out.append("<ul><li><strong>Listicles and comparison aggregators</strong> are the single largest category at about 35.7% of all citations, the "best X for Y" pages, and the highest-leverage placement in AI search.</li>"
 "<li><strong>User communities and media</strong> such as Reddit, YouTube, and Quora supply roughly 18% to 25%. Re-rankers favour unvarnished user sentiment and recent contextual proof, which is "+L("why Reddit, G2 and analyst reports drive AI recommendations","/blogs/why-ai-cites-reddit-g2-analysts")+".</li>"
 "<li><strong>Reference sites and trade publications</strong> including Wikipedia account for 10% to 15%, providing high-trust entity validation.</li></ul>")
out.append(p("Read that chart as an instruction rather than a curiosity. AI answer systems treat first-party claims with structural distrust unless independent sources corroborate them. Your website is where you convert attention, not where you earn it."))
out.append(h3("Different engines, different worlds"))
out.append(p("One more mechanical fact before the math. Engines do not share a retrieval index, and their cited source sets barely overlap. Cross-engine Jaccard overlap of cited domains runs between 16% and 20% for the same prompt. This kills the idea of a single AI search strategy: you are optimising for five loosely related systems with different index compositions, different re-ranking weights, and different freshness behaviour. That is exactly why the visibility metric below is platform-weighted rather than pooled."))

# 5 the math
out.append(sec("05","math","How do you score the three signals?",
 "Five metrics, each with its own formula.","Traditional SEO metrics do not survive contact with generative search. Platform-weighted visibility, mean recommendation position, a sentiment index, entity share of voice, and cross-platform source overlap. Each measures a different thing."))
out.append(p("Keyword rank position assumes a ranked list. Domain authority assumes a link graph is the primary evaluator. Neither assumption holds when the output is a paragraph of synthesised prose. What follows is a working framework: five metrics, each with the formula, the variables, and code you can run against your own tracking data."))
out.append(h3("1. Platform-weighted visibility"))
out.append(p("Engines do not perform uniformly. A brand can be highly visible on ChatGPT and absent from Perplexity. Pooling those into one average hides the thing you need to see, so visibility is computed as a weighted composite where w_p is the platform weight (normalised to sum to one), M_p is mentions on platform p, and Q_p is prompts issued to it. Weight the engines your buyers actually use, and renormalise if you only track some of them."))
out.append(code("python · platform-weighted visibility",CODE_VIS))
out.append(h3("2. Mean recommendation position"))
out.append(p("Appearing in a list is not the same as topping it. Position inside a generated answer correlates strongly with user selection, so ordinal placement needs its own metric. M_pos is the subset of prompts where the brand receives an explicit ordinal recommendation, and r(q,p) is the rank assigned, where 1 is the primary recommendation. Lower is better, which makes this the one metric on the dashboard that inverts. Label it clearly or someone will misread it in a board deck."))
out.append(h3("3. Contextual sentiment index"))
out.append(p("Being mentioned is not automatically good. A brand named as the expensive option with poor support has visibility and a problem. The sentiment index normalises tone into a bounded 0 to 100 score: an all-positive answer set scores 100, all-neutral 50, all-negative 0. The 0.5 coefficient on neutral mentions means a negative mention costs exactly twice what a neutral one does, which matches the observed penalty in practice."))
out.append(h3("4. Entity share of voice"))
out.append(p("Share of voice answers the only question a CMO really asks: are you winning relative to the people you compete against. M_b is total mention count for the target brand and C is the set of verified, domain-resolvable competitor entities in the answers. The verification step matters, generative engines invent plausible-sounding vendor names, and hallucinated competitors in the denominator will quietly depress your score. Resolve every competitor name to a real domain before counting it."))
out.append(code("python · sentiment index and share of voice",CODE_SENT))
out.append(h3("5. Cross-platform source overlap"))
out.append(p("The last metric is diagnostic rather than reportable. It measures how much two engines agree on sources for the same prompt, using the Jaccard coefficient over each platform's cited domain set. Run it across your prompt set and you learn where your engines diverge, which tells you which third-party domains are worth pursuing for which platform."))
out.append(code("python · cross-engine source overlap",CODE_JAC))
out.append(p("Executives want a single score. Composite metrics are lossy and you should say so out loud, but if you need one, weight the four reportable metrics and convert mean position into a positive-direction term (rank 1 scores 100, rank 6 scores 0). Publish the components alongside the composite. A score that moves without a visible driver is worse than no score."))
out.append(table("Table 2. The five metrics, and the question each one answers.",
 ["Metric","What it answers","Variables","Working target"],
 [["Platform-weighted visibility","Does the machine know us, engine by engine","w_p weight, M_p mentions, Q_p prompts","Above the tier benchmark for your stature band"],
  ["Mean recommendation position","When named, how prominently","r(q,p) ordinal rank, M_pos qualifying prompts","3 or lower, tracked as a falling line"],
  ["Contextual sentiment index","Is the framing helping or hurting","N_pos, N_neu, N_total","70 or above, zero recurring negatives"],
  ["Entity share of voice","Are we winning against the named set","M_b brand, M_c verified competitors","Rising quarter on quarter, fixed competitor set"],
  ["Source overlap coefficient","How much engines agree on sources","D_p(q) cited domain sets","Diagnostic only, expect 0.16 to 0.20"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(p("Targets in the final column are working practitioner benchmarks rather than published thresholds. Set your own from your first baseline: a Tier 3 brand hitting 25% weighted visibility has achieved considerably more than a Tier 1 brand holding 70%."))

# 6 evidence
out.append(sec("06","evidence","What does the evidence actually show?",
 "Three bodies of work, measuring three different things.","The Princeton GEO experiment (causal lifts from content changes), the GEO-at-scale benchmark (non-determinism and the stature ladder), and the 75,000-brand correlation study (mentions beat links). They get quoted interchangeably; they should not be."))
out.append(h3("The Princeton GEO experiment"))
out.append(p("The foundational study establishing generative engine optimisation came from researchers at Princeton, Georgia Tech, the Allen Institute for AI, and IIT Delhi, published at ACM SIGKDD in 2024. It evaluated 10,000 queries across generative platforms to quantify how specific on-page changes affected visibility and citation rates. The headline: classical SEO tactics do close to nothing in generative environments, while adding machine-extractable proof does a great deal."))
out.append(chart("liftChart",240,"Figure 8. Measured visibility lift by content intervention (Princeton et al., KDD 2024). Evidence beats phrasing."))
out.append("<ul><li><strong>Expert quotations</strong> produced the largest single lift at +41%. Models treat an attributed quote as a verifiable assertion rather than an opinion.</li>"
 "<li><strong>Statistical density</strong> delivered +32%. Precise figures increase the chance a chunk survives re-ranking.</li>"
 "<li><strong>Authoritative source citing</strong> delivered +30%. Linking out to primary studies raises the trust score of the citing page.</li>"
 "<li><strong>Fluency optimisation</strong> delivered +28%. Clean, readable structure makes extraction easier.</li></ul>")
out.append(p("Read those four together and a pattern emerges. Every winning intervention makes a passage more verifiable. None of them make it more persuasive. The machine is not being sold to; it is checking whether your claim can be substantiated without leaving your page."))
out.append(callout("The counterintuitive part",["Adding an outbound link to a primary source raises your own citation odds by about 30%. Traditional SEO instinct says keep the equity in-house. Generative engines do the opposite, treating well-sourced pages as better evidence than unsourced ones. Link out generously to studies, standards, and documentation."]))
out.append(h3("The GEO-at-scale benchmark"))
out.append(p("The second body of work is a production analysis across 102 enterprise brands, 3,508 tracking runs, and 102,025 prompt responses. It contributes three findings that should change how you measure."))
out.append(p("First, engines are non-deterministic. Re-running identical prompt sets against identical models produced a different prose answer in 22.5% of prompt-engine cells, and 6.8% of responses flipped binary status, moving from mentioned to not mentioned or the reverse. A single-run screenshot is not a measurement; it is a sample of size one from a noisy distribution."))
out.append(statgrid([("22.5%","of answers change wording on re-run"),("6.8%","flip mentioned / not-mentioned"),("6.7x","sentiment variance vs presence"),("flat","visibility without intervention")]))
out.append(p("Second, sentiment is far noisier than presence. Sentiment scores derived from LLM output exhibit about 6.7 times the variance of binary mention detection. Mention tracking is close to deterministic; tone fluctuates with decoding temperature and prompt phrasing. Treat a single-week sentiment drop as noise until three runs agree. Third, nothing improves on its own: absent content or digital PR intervention, visibility trajectories are flat. Every point of visibility you hold is the result of work someone did, which is the same logic behind "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+"."))
out.append(h3("Correlation studies: mentions versus links"))
out.append(p("The third body of work is correlational rather than experimental, and should be read with the usual caution. The 75,000-brand analysis measured Spearman correlations between off-page factors and visibility in Google AI Overviews, later extended to ChatGPT and AI Mode."))
out.append(chart("corrChart",300,"Figure 10. Spearman correlation with AI visibility by signal class. Every mention-class signal outranks every link-class signal."))
out.append(p("YouTube mentions lead at 0.737, which surprises people until you remember that video transcripts are dense, conversational, entity-rich text that models ingest happily. Branded web mentions follow at 0.664, branded anchors at 0.527, brand search volume at 0.392, Domain Rating at 0.326, referring domains at 0.218, and content volume, the raw number of pages on your site, comes last at 0.194."))
out.append(callout("Two honest caveats",["Correlation is not causation, and brands that earn editorial mentions are usually brands that invested in product, PR, and category presence, all of which have independent effects.","The study population was filtered to brands above a Domain Rating threshold, so it describes the competitive middle and top, not a startup with nine backlinks. What survives both caveats is the ordering: every mention-class signal outranks every link-class signal, and publishing volume is the weakest predictor on the board."]))
out.append(table("Table 3. Experimental lifts and correlational signals side by side. The first three are causal; the last four are not.",
 ["Intervention or signal","Measured effect","Source","Mechanism"],
 [["Expert quotation added","+41% lift","Princeton / Georgia Tech, KDD 2024","Verifiable statement grounding, better extractability"],
  ["Statistical evidence density","+32% lift","Princeton / Georgia Tech, KDD 2024","Precise figures pass internal fact-check filters"],
  ["Authoritative source citing","+30% lift","Princeton / Georgia Tech, KDD 2024","Connects content to primary evidence nodes"],
  ["YouTube mentions","r = 0.737","75k-brand correlation analysis","Transcript ingest supplies high-trust co-occurrence"],
  ["Branded web mentions","r = 0.664","75k-brand correlation analysis","Teaches category placement through co-citation"],
  ["Referring domains","r = 0.218","75k-brand correlation analysis","Passes link equity, weak direct retrieval influence"],
  ["Content volume","r = 0.194","75k-brand correlation analysis","Page count alone does not build entity prominence"]],
 cls=lambda j,c: "label" if j==0 else ""))

# 7 playbook
out.append(sec("07","playbook","What is the playbook for each signal?",
 "Three pillars, in order: on-page, technical, off-page.","Citation-first content structuring and entity markup are fast and within your control. Off-page entity PR is slow and decides the ceiling, because 97.1% of citations point away from your site."))
out.append(h3("Pillar 1: citation-first content structuring"))
out.append(p("The goal is a page a re-ranker can dismantle cleanly. That means abandoning the narrative intro and leading with the answer:"))
out.append("<ul><li>Write section headings as the explicit question a user would ask, not a noun phrase. "How much does implementation cost" beats "Implementation".</li>"
 "<li>Answer in the first 60 words, completely, with no windup. If the reader could stop after your opening passage and be correctly informed, so could a model.</li>"
 "<li>Target roughly 40 words for each key factual assertion, matching the median cited passage length.</li>"
 "<li>State precise numbers, dates, and scope. "A 32% efficiency gain across 1,200 enterprise implementations in Q2 2026" is extractable; "dramatically improved results recently" is not.</li>"
 "<li>Attribute every claim to a named source, and link out using descriptive anchor text that names the benchmark or dataset rather than the word "source".</li></ul>")
out.append(p("The before-and-after below is the shape of the change. Both passages contain the same information. Only one survives chunking."))
out.append(code("html · citation-first passage structure",CODE_HTML))
out.append(h3("Pillar 2: schema and entity markup"))
out.append(p("Schema alone will not make you visible. What it does is remove ambiguity about which entity you are, which matters enormously when your brand name is also a common noun or shared with another company. Declare a canonical @id URI consistently across every JSON-LD block, connect it with a sameAs array to Wikipedia, Wikidata, Crunchbase, LinkedIn, and official social accounts, and wrap statistical claims in Article and ClaimReview structures. The full treatment is in "+L("schema markup for AI citations","/blogs/schema-markup-ai-citations-2026")+"."))
out.append(code("json-ld · entity declaration",CODE_JSONLD))
out.append(h3("Pillar 3: off-page entity PR"))
out.append(p("This is where the ceiling is set. Since 97.1% of citations point at third-party domains, the work is earning presence on those domains. The co-citation play deserves special mention: getting your executives quoted in articles that also discuss Tier 1 competitors is one of the few reliable ways to move parametric association. You are not buying a link; you are teaching a model that your entity belongs in a set it already trusts, the mechanism behind "+L("authority seeding","/blogs/authority-seeding-ai-llm-trust")+"."))
out.append(table("Table 4. Off-page priorities ordered by their share of AI-search citations.",
 ["Source class","Citation share","What to do","Realistic timeline"],
 [["Comparison listicles and buyer guides","~35.7%","Identify which roundups the engines cite for your category, then pitch inclusion, correct outdated entries, supply structured product data","6 to 12 weeks per placement"],
  ["User communities: Reddit, Quora, forums","18% to 25% with video","Answer real questions in detail with a named affiliation. Do not astroturf, detected shilling produces negative framing","Ongoing, compounding"],
  ["YouTube and video transcripts","Included above","Publish substantive video with clean transcripts. Strongest single correlation at r = 0.737","8 to 16 weeks to signal"],
  ["Reference sites and trade press","10% to 15%","Pursue Wikidata and Wikipedia eligibility, trade commentary, and analyst mentions alongside Tier 1 competitors","3 to 9 months"],
  ["Your own domain","~2.9%","Citation-first structuring, schema, crawlability. Necessary, nowhere near sufficient","2 to 4 weeks"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(h3("The measurement loop"))
out.append(p("Run a continuous 90-day cycle. The cadence matters more than the tooling."))
out.append(pipeline([("Build the prompt set","20-50 fixed prompts across discovery, comparison, problem-solution."),("Baseline","Query all engines over 3-5 runs; average to smooth variance."),("Classify sources","Tag every cited URL: brand, listicle, news, community, competitor."),("Close the gaps","Ship on-page evidence; outreach to the exact domains cited."),("Re-measure","Compare deltas per engine at 30 days; full review at 90.")],4,
 "Figure 11. The operating cadence for a generative visibility programme."))
out.append(p("Step four is the one teams skip. The value is not in knowing you are invisible on a prompt. It is in knowing which four domains the engines consulted before deciding to name someone else."))
out.append(h3("Diagnosing which signal is broken"))
out.append(p("When visibility is bad, the taxonomy tells you where to look. Run a fixed prompt set and read the pattern:"))
out.append(table("Figure 12. A diagnostic for isolating the failing signal.",
 ["Symptom","Broken signal","Where to fix"],
 [["Absent even on prompts with no live search","Mention (parametric)","Off-page entity PR, co-citation, slow"],
  ["Named in the answer, but your URL never cited","Citation (retrieval)","On-page evidence density and schema, fast"],
  ["Cited as a source, competitor gets recommended","Recommendation (synthesis)","Comparison coverage, sentiment, share of voice"]],
 cls=lambda j,c: "label" if j==0 else ""))

# 8 caveats
out.append(sec("08","caveats","What does this taxonomy not mean?",
 "Four corrections, because this field overclaims fast.","Links are not obsolete. Mentions are not free. The numbers are not permanent. And tracking is not progress."))
out.append(p("<strong>It does not mean links are obsolete.</strong> Backlinks still move classical rankings, and classical rankings still feed the indices generative engines query. A correlation of 0.218 is not zero. The claim is that link count has stopped being a good proxy for AI visibility, not that it stopped mattering."))
out.append(p("<strong>It does not mean mentions are free.</strong> Unlinked mentions carry weight, but the mechanism is entity prominence rather than equity transfer. A hundred low-quality mentions on scraped content farms will not build parametric presence. Quality of context is what makes co-occurrence useful."))
out.append(p("<strong>It does not mean these numbers are permanent.</strong> Platform weights shift with market share. Source composition shifts as engines adjust retrieval preferences. The 40-word median will move as context windows grow. Treat every figure here as a snapshot with a decay rate, and "+L("re-baseline quarterly","/blogs/30-day-content-half-life-recency-ai-ranking-signal")+"."))
out.append(p("<strong>It does not mean tracking equals progress.</strong> Dashboards are cheap now. The bottleneck was never measurement. It is the unglamorous work of getting into the roundups your buyers' engines already trust, and that has not been automated. Measurement without visibility is "+L("ranking that is not visibility","/blogs/ranking-isnt-visibility")+"."))

# 9 takeaway
out.append(sec("09","takeaway","Where does this leave you?",
 "With three signals, three subsystems, three fixes.","Off-page entity PR for mentions. Evidence-dense on-page structure for citations. Comparison coverage and sentiment for recommendations. Start with the diagnostic, then work the signal that is actually broken."))
out.append(p("The taxonomy is simple enough to hold in your head. Mentions establish entity awareness and category placement inside a model's weights. Citations provide grounding and verification during retrieval. Recommendations are the synthesised output where the system evaluates options and steers a buyer."))
out.append(p("The rebalancing this requires is uncomfortable for most organic teams, because the highest-leverage work sits outside the website. You are not optimising a page any more. You are building the case, distributed across the web, that a machine will assemble on your behalf when a buyer asks it a question you never see."))
out.append(pull("Run a fixed prompt set five times across the engines your buyers use, classify every cited URL, and find out which of the three signals is actually broken. Everything else follows from that answer."))

# FAQ
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

# References
REFS=[
 ("Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines. arXiv.","https://arxiv.org/abs/2606.20065"),
 ("What is SEO-GEO? Generative Engine Optimization. explainx.ai.","https://www.explainx.ai/post/what-is-seo-geo"),
 ("Brand Mentions vs Backlinks: What Actually Moves Rankings in 2026. Link Publishers.","https://www.linkpublishers.com/blog/brand-mentions-vs-backlinks"),
 ("Backlinks vs Brand Mentions: Off-Page SEO Evolution in 2026. Search Atlas.","https://searchatlas.com/blog/backlinks-vs-brand-mentions/"),
 ("Generative Engine Optimization (GEO): The Full Definition, Explained. neuroflash.","https://neuroflash.com/blog/generative-engine-optimization/"),
 ("Generative Engine Optimization at Scale (full text). arXiv.","https://arxiv.org/html/2606.20065v1"),
 ("Unlinked Brand Mentions: The 2026 Marketer's Guide. Web Tonic.","https://www.webtonic.in/blog/unlinked-brand-mentions/"),
 ("How To Implement Citations For Generative Engine Optimisation. NeuralAdX.","https://neuraladx.com/how-to-implement-citations-for-geo/"),
 ("RAG QA Testing Guide for Retrieval, Generation, and Citation.","https://www.deepchecks.com/rag-qa-testing-guide/"),
 ("Generative Engine Optimization for B2B: The Complete 2026 Guide. Mersel AI.","https://www.merselai.com/blog/geo-for-b2b"),
 ("Brand Mentions vs Backlinks: What Actually Moves Rankings. Gravidy.","https://www.gravidy.xyz/blog/brand-mentions-vs-backlinks"),
 ("Brand Mentions Without A Link Don't Matter. LinkBuildingHQ.","https://linkbuildinghq.com/brand-mentions-without-links/"),
 ("Digital PR vs Backlinks: The New SEO Strategy for 2026. Coozmoo.","https://coozmoo.com/digital-pr-vs-backlinks/"),
 ("Patent US8682892B1: Google Patented Unlinked Brand Mentions.","https://patents.google.com/patent/US8682892B1/en"),
 ("The Complete Guide to Generative Engine Optimization in 2026. Clairon AI.","https://claironai.com/guide-to-geo-2026/"),
 ("Generative Engine Optimization, The Definitive Guide 2026. Seolyze.","https://seolyze.com/geo-definitive-guide/"),
 ("GEO: Generative Engine Optimization (Princeton, Georgia Tech, AI2, IIT Delhi). arXiv.","https://arxiv.org/abs/2311.09735"),
 ("An Analysis of AI Overview Brand Visibility Factors, 75K Brands Studied. Ahrefs.","https://ahrefs.com/blog/ai-overview-visibility-study/"),
 ("Are brand mentions without links really counted by Google as off-page signals. r/seogrowth.","https://www.reddit.com/r/seogrowth/"),
 ("YouTube mentions are the top signal for AI brand visibility. TNW.","https://thenextweb.com/news/youtube-mentions-ai-brand-visibility"),
 ("AI and Brand Visibility: Ahrefs' Insights from 75,000 Brands. BuzzStream.","https://www.buzzstream.com/blog/ai-brand-visibility-ahrefs/"),
 ("Ranqo, AI Search Visibility Suite. Further reading.","https://ranqo.com/"),
 ("AI Search Research. Ranqo Labs. Further reading.","https://ranqo.com/labs/"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
out.append('<div class="about-block" id="references"><div class="about-label">References</div>'
           '<p style="margin-bottom:16px;">The studies, patents and research this taxonomy draws on.</p>'
           f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Sources: the Princeton/Georgia Tech GEO experiment (KDD 2024), the GEO-at-scale benchmark, and the 75,000-brand correlation analysis, 2024-26. Formulas and code are working reference implementations; figures are drawn from the cited studies.</p></div>')

body="\n".join(out)

SIDEBAR=[("97.1%","of AI citations point off your site"),("0.737","YouTube mentions, the top signal"),("2.9%","citations to your own domain"),("5","metrics in the scoring framework")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#short"><span class="toc-num">01</span>The short version</a></li>'
     '<li><a href="#why"><span class="toc-num">02</span>Why it matters now</a></li>'
     '<li><a href="#definitions"><span class="toc-num">03</span>Definitions, done properly</a></li>'
     '<li><a href="#machine"><span class="toc-num">04</span>How the machine works</a></li>'
     '<li><a href="#math"><span class="toc-num">05</span>The math</a></li>'
     '<li><a href="#evidence"><span class="toc-num">06</span>What the evidence shows</a></li>'
     '<li><a href="#playbook"><span class="toc-num">07</span>The playbook</a></li>'
     '<li><a href="#caveats"><span class="toc-num">08</span>What it does not mean</a></li>'
     '<li><a href="#takeaway"><span class="toc-num">09</span>Where this leaves you</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - the GEO measurement taxonomy - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["AI visibility","GEO measurement","brand mentions","citations","recommendations","generative engine optimization","share of voice","parametric memory","RAG","AI search metrics"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Citation vs Mention vs Recommendation &middot; rawmktg."
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
 f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
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

CHARTS=r"""
<!-- Chart.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
(function(){
  if(typeof Chart==='undefined') return;
  var css=getComputedStyle(document.documentElement);
  var signal=(css.getPropertyValue('--signal')||'#D04A2A').trim();
  var faint=(css.getPropertyValue('--faint')||'#C5BFB4').trim();
  var up=(css.getPropertyValue('--up')||'#3E9B6A').trim();
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.4);

  var sh=document.getElementById('shiftChart');
  if(sh){new Chart(sh,{type:'bar',data:{labels:['2012','2026'],datasets:[
    {label:'Link-class signals',data:[80,45],backgroundColor:neutral,borderRadius:4},
    {label:'Mention-class signals',data:[20,55],backgroundColor:signal,borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+': '+c.raw+'%';}}}},
      scales:{x:{stacked:true,ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{stacked:true,beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var ti=document.getElementById('tierChart');
  if(ti){new Chart(ti,{type:'bar',data:{labels:['Tier 1 (household)','Tier 2 (mid-market)','Tier 3 (niche)'],datasets:[{data:[72.9,43.6,11.4],backgroundColor:[up,rgba(signal,0.6),signal],borderRadius:4,barThickness:60}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% unbranded visibility';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var so=document.getElementById('sourceChart');
  if(so){new Chart(so,{type:'bar',data:{labels:['Listicles & buyer guides','Communities & video','Reference & trade press','Your own domain'],datasets:[{data:[35.7,21.5,12.5,2.9],backgroundColor:[signal,rgba(signal,0.7),rgba(signal,0.5),neutral],borderRadius:4,barThickness:30}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of citations';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var lf=document.getElementById('liftChart');
  if(lf){new Chart(lf,{type:'bar',data:{labels:['Expert quotes','Statistical density','Source citing','Fluency'],datasets:[{data:[41,32,30,28],backgroundColor:[signal,rgba(signal,0.8),rgba(signal,0.65),rgba(signal,0.5)],borderRadius:4,barThickness:48}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' +'+c.raw+'% visibility lift';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return '+'+v+'%';}},grid:{color:grid}}}}});}

  var co=document.getElementById('corrChart');
  if(co){new Chart(co,{type:'bar',data:{labels:['YouTube mentions','Branded web mentions','Branded anchors','Brand search volume','Domain Rating','Referring domains','Content volume'],datasets:[{data:[0.737,0.664,0.527,0.392,0.326,0.218,0.194],backgroundColor:[up,up,rgba(up,0.7),rgba(signal,0.55),rgba(signal,0.6),signal,signal],borderRadius:4,barThickness:22}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' r = '+c.raw;}}}},
      scales:{x:{beginAtZero:true,max:0.8,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Measurement Taxonomy &middot; Ranking Signals</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/cmr_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/cmr_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("'")+hh.count("""),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faq:",hh.count('faq-item'),"| refs:",hh.count('id="references"'),"| cbcopy:",'cb-copy-css' in hh)
