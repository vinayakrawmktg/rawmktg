#!/usr/bin/env python3
"""SCRATCH: build blogs/query-fan-out-how-one-prompt-becomes-ten-searches.html. Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="query-fan-out-how-one-prompt-becomes-ten-searches"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-08-10"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'
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
    for i,(t,dd) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(dd)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Query Fan-Out: How One Prompt Becomes Ten Searches"
DECK=("You type one sentence. The engine runs eight to sixteen searches you never see, scores a few thousand text chunks, and "
      "writes an answer from roughly five pages. How that machine works, what the math rewards, and why the page that ranks #1 "
      "often loses to the page that ranks #5 four times.")
DESC=("Query fan-out explained: how AI search turns one prompt into 8-16 hidden sub-queries, the RRF and cosine math that decides citations, and why 95% of the searches that matter have zero keyword volume.")
DATANOTE=("A technical deep dive on query fan-out across ChatGPT Search, Google AI Mode and Perplexity, grounded in published pipeline "
          "analyses and third-party measurements (Rankly, Netstager, Finseo, Aleyda Solis, Surfer, GEOly, Search Engine Land, Semrush), "
          "2025-26. Figures are original illustrations built from the cited data; percentages are directional rather than exact.")

CODE_ROUTE=r'''# Conceptual shape of the routing decision
scores = classifier(prompt, conversation_history)

if scores.no_search > 0.20:
    return answer_from_parameters(prompt)        # no retrieval, no citations
if scores.complex_search > 0.40:
    return recursive_planner(prompt, max_rounds=3)   # fan-out, read, fan-out again
return single_pass_retrieval(prompt)             # one round of sub-queries'''

CODE_COSINE=r'''# What the scoring pass looks like, minus the GPU
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
audition = max(scores.values())'''

CODE_RRF=r'''# Reciprocal Rank Fusion in eight lines
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
# [('doc_b', 0.06154), ('doc_a', 0.01639)]'''

CODE_HTML=r'''<article>
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
</article>'''

CODE_JSONLD=r'''{
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
}'''

CODE_TRACKER=r'''# Minimal citation tracker: prompts in, cited domains out
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
sov = group_by(rows, 'facet', agg=lambda r: mean(x['cited'] for x in r))'''

FAQ=[
 ("What is query fan-out in AI search?",
  "Query fan-out is the step where an AI search engine decomposes your single prompt into a set of targeted sub-queries, one per facet of what you meant (a spec, a price tier, a compliance requirement, a comparison, social proof), then fires them in parallel against different corpora. Instead of searching once for what you typed, the engine searches many times for what you meant, and each sub-query is a separate retrieval contest with its own winners."),
 ("How many sub-queries does one prompt generate?",
  "In standard modes, a single conversational prompt fans out into roughly 8 to 16 parallel sub-queries. About 59% of prompts trigger 5 to 11, 24% trigger 12 to 19, and the hardest standard tasks reach 28. Agentic research modes break the scale entirely: a single ChatGPT Deep Research prompt has been documented triggering over 400 sub-queries."),
 ("Why do zero-volume keywords matter for AI search?",
  "Over 95% of generated fan-out sub-queries have zero recurring search volume in keyword tools, because they are machine-written fresh for one user's context and never typed by anyone. Keyword databases measure strings humans repeat, so they cannot see a query that occurs once. The prioritisation metric shifts from search volume to facet coverage: how many of the sub-queries in a topic you can answer better than anyone."),
 ("Does ranking #1 still matter with Reciprocal Rank Fusion?",
  "Less than it used to. Under RRF with the conventional constant k=60, rank #1 contributes 0.01639 and rank #10 contributes 0.01429, a gap of just 13%. Moving a page from position 10 to 1 inside one sub-query buys a 13% edge; appearing at all in a second sub-query list buys close to 100%. A document that ranks #5 across four lists beats a document that ranks #1 in one, by 3.75x."),
 ("How do you optimise for query fan-out?",
  "Write atomically, one self-contained section per sub-question with the answer in the first 40 words; keep passages monosemantic so the embedding sits close to one sub-query vector; serve every fact (pricing, specs, compliance) in server-side HTML because the main ChatGPT crawler does not render JavaScript; and build the off-site footprint, since sentiment sub-queries go to Reddit, G2 and forums, not your site. Rewriting H2s as questions alone lifts ChatGPT citation rate from 29% to 41%."),
]

out=[]
out.append(p("Search used to be a single transaction. You typed a string, the engine matched it against an inverted index, and it handed back ten blue links ordered by lexical relevance, link topology and domain authority. One input, one lookup, one list. Every SEO tactic built between 1998 and 2023 assumes that shape."))
out.append(p("That shape is gone. When you ask ChatGPT Search, Google AI Mode or Perplexity a real question, the system does not run your question. It reads your question, works out what you are actually trying to decide, and then writes its own set of searches. Those run in parallel against different corpora, get fused, chunked, scored and compressed into a context window. Only then does a model write the paragraph you read."))
out.append(pull("Your competitors are not beating you on the head term. They are beating you on eleven sub-queries neither of you can see in Ahrefs."))
out.append(p("The industry name for the middle step is query fan-out (also query decomposition, multi-query retrieval, or query variant generation). If you optimised a page for the sentence a human types, you optimised for a string that is no longer being searched. The strings being searched are machine-written, highly specific, and almost entirely absent from keyword tools."))

# 01 one-line / what it is
out.append(sec("01","what","What is query fan-out, in one line?",
 "AI search does not rank pages against your prompt.",
 "It generates its own sub-queries, retrieves passages for each one, fuses the lists, and cites whichever sources show up usefully across the most facets. Breadth of coverage beats depth on any single term."))
out.append(p("Each sub-query goes after a distinct facet of the original: a technical spec, a pricing tier, a compliance requirement, a comparison, a piece of social proof, or a follow-up you have not thought to ask. They fire simultaneously across live web indices, knowledge graphs, product catalogues and community databases. The system merges the ranked lists with Reciprocal Rank Fusion and dense vector scoring, assembles the surviving passages into a context block, and passes that to the model, which writes the answer with inline citations."))
out.append(pipeline([("Classify","Does this even need a search, and how hard?"),("Decompose","Write the sub-queries that cover the facets."),("Retrieve","Fire them at different corpora in parallel."),("Fuse + score","Merge lists, chunk pages, score the chunks."),("Synthesise","Write one answer, attach citations.")],4,
 "Figure 1. The generalised fan-out pipeline. Every commercial AI search product is a variation on this shape."))
out.append(callout("The structural detail that drives everything",[
 "Retrieval happens per sub-query, not per prompt. A page is never evaluated once. It is evaluated eight to sixteen times, against eight to sixteen different questions, and it only needs to win a few of them to be pulled into the context pool. Visibility is no longer a position. It is a hit rate."]))

# 02 numbers
out.append(sec("02","numbers","How many hidden searches does one prompt trigger?",
 "Eight to sixteen in standard modes, and 400+ in agentic deep research.",
 "About 59% of prompts fan out into 5 to 11 sub-searches, 24% into 12 to 19, and the hardest standard tasks reach 28. A single ChatGPT Deep Research prompt has been documented triggering over 400."))
out.append(chart("distChart",240,"Figure 2. Distribution of sub-query volume per prompt. The modal prompt fires between five and eleven hidden searches."))
out.append(table("Table 1. Sub-query volume bands, share of prompts, and the modes that produce them.",
 ["Sub-query volume","Share of prompts","What triggers it","Typical engine"],
 [["1 to 4","~17%","Simple factual and navigational lookups","Google AI Mode, ChatGPT standard"],
  ["5 to 11","59%","Standard commercial and comparative intent","Perplexity, ChatGPT Search"],
  ["12 to 19","24%","Multi-faceted buyer journeys and analysis","Google AI Mode on Gemini 2.5"],
  ["20 to 28","~3%","Advanced multi-constraint research tasks","Complex multi-turn AI sessions"],
  ["200 to 400+","Special mode","Recursive agentic deep research","ChatGPT Deep Research"]],
 cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Read that as a traffic forecast and it looks like good news. Read it as a competition forecast and it is not. Ten sub-queries means ten chances to be included and ten chances to be left out."))

# 03 chatgpt pipeline
out.append(sec("03","chatgpt","How does ChatGPT Search actually work, stage by stage?",
 "A seven-stage retrieval pipeline, and every stage is a filter that throws work away.",
 "Understanding where the losses happen tells you exactly where to spend effort: classification, query generation, metadata filtering, fetch and chunk, vector scoring, audition selection, and synthesis."))
out.append(h3("Stage 1: query classification"))
out.append(p("A lightweight classifier scores the prompt in milliseconds and returns a no-search, simple-search and complex-search probability. If the no-search score clears roughly 0.2, the model answers from parameters and no retrieval happens at all. If the complex score clears roughly 0.4, the system enters a recursive multi-turn planner. A meaningful share of prompts in your category may never trigger a search, for those you are competing against training data and brand memory, not your sitemap."))
out.append(code("python - the routing decision",CODE_ROUTE))
out.append(h3("Stage 2: search query generation"))
out.append(p("The orchestrator writes two classes of query: short keyword queries for inverted-index lookup, and longer semantic queries (around fifteen words) written to align vector embeddings with intent. For complex prompts it runs a planner loop, up to three rounds, issuing a batch, reading the metadata, spotting gaps, and firing again. If your content answers the obvious facet, you compete in round one against everyone. If it answers the awkward second-order facet, you are one of very few candidates in round two, where the field is thin."))
out.append(h3("Stages 3-4: filter, fetch and chunk"))
out.append(p("Sub-queries return 40 to 50 candidate URLs. Before fetching a single page, the system cuts that pool to 10 to 20 based purely on SERP-level metadata, title tags, meta descriptions, authority signals and schema. Your body copy is not consulted at this stage; your title tag is doing all the work. Survivors are fetched three to ten at a time under a hard two-second render timeout, then parsed into uniform, non-overlapping 128-token chunks, about a hundred words, that may be split mid-argument by a chunker that has never read your headline."))
out.append(h3("Stages 5-6: vector scoring and the audition chunk"))
out.append(p("Chunks are embedded and scored by cosine similarity against the semantic sub-query vectors, thousands of comparisons in 100 to 200 milliseconds. The system then looks at the single highest-scoring chunk from each page, its audition chunk, alongside the metadata, and selects a final pool of three to five pages for deep reading. Your entire page is represented, at the moment of selection, by its best hundred words. If your best chunk is a hedged introduction, you do not audition well."))
out.append(h3("Stage 7: context assembly and generation"))
out.append(p("Surviving text, roughly 5,000 to 6,000 tokens, is formatted into sliding windows around the top chunks, and the core model writes the answer with inline citations. Two infrastructure facts sit underneath: about 92% of ChatGPT's external searches run via the Bing Search API, and OpenAI's OAI-SearchBot does not execute JavaScript, it parses raw HTML. Empirical work found 46% of ChatGPT crawler requests operating in plain-HTML mode."))
out.append(pipeline([("40-50 URLs","from the sub-queries."),("10-20 pass","metadata filter, title tags only."),("3-5 pages","deep-read after the audition chunk."),("5-6k tokens","context window, then the answer.")],3,
 "Figure 3. The compression funnel. Fifty candidates become five pages become six thousand tokens."))

# 04 google + perplexity
out.append(sec("04","engines","How do Google AI Mode and Perplexity differ?",
 "Same fan-out, different destinations, and different transparency.",
 "Google issues up to sixteen parallel sub-searches across four corpora at once, the web index, Knowledge Graph, Shopping Graph and review databases. Perplexity exposes its six to ten sub-queries directly in the interface."))
out.append(p("What makes Google's version structurally different is not the count, it is the destinations. Your product page competes in the web index, your entity record in the Knowledge Graph, your feed in the Shopping Graph, your reviews somewhere else entirely. A team that only owns the website is playing one of four hands. And the number that should reshape planning: pages that rank for the associated fan-out sub-queries are 161% more likely to be cited in AI Overviews than pages that rank only for the primary query. This is the multi-corpus split covered in "+L("AI Mode vs AI Overviews","/blogs/ai-mode-vs-ai-overviews")+"."))
out.append(p("Perplexity leans on decomposition hardest and most visibly, exposing its sub-queries as follow-up searches. It is the cheapest research tool available: type your buyers' questions and read the sub-queries it shows you. That is your content brief, written by the machine that will grade it."))
out.append(table("Table 2. Architecture comparison across the three engines that matter commercially.",
 ["Feature","ChatGPT Search","Google AI Mode","Perplexity"],
 [["Orchestrator","Dedicated reasoning orchestrator","Custom Gemini 2.5 engine","Agentic RAG pipeline"],
  ["Sub-queries / prompt","8 to 12 (400+ in Deep Research)","8 to 16 parallel","6 to 10"],
  ["Primary index","Bing API ~92% + OAI-SearchBot","Web index, Knowledge Graph, Shopping Graph, reviews","Hybrid web + multi-engine APIs"],
  ["JavaScript rendering","No, raw HTML only","Yes, Googlebot pipeline","Partial and limited"],
  ["Fetch timeout","Hard 2.0s per page","Native SERP latency","Dynamic multi-source"],
  ["Unit evaluated","128-token vector chunks","Entity-based passage scoring","Structured Q&A passages"]],
 cls=lambda j,c:"label" if j==0 else ""))

# 05 the math
out.append(sec("05","math","What is the math that decides who gets cited?",
 "Two operations: cosine similarity for relevance, and Reciprocal Rank Fusion for survival.",
 "Neither rewards what classical SEO optimises for. Cosine scores a passage against a sub-query; RRF decides which documents survive when eight ranked lists have to become one."))
out.append(h3("Vector embeddings and cosine similarity"))
out.append(p("A 128-token chunk becomes a dense vector; a generated sub-query becomes a dense vector in the same space; relevance is the cosine of the angle between them. The denominator normalises for magnitude, so a long passage does not beat a short one simply for being long. Retrieval systems care about the band from roughly 0.7 upward. Because embeddings capture concepts rather than strings, a chunk can score high with zero exact keyword overlap. Keyword density is not a lever here; conceptual cleanliness is."))
out.append(code("python - the scoring pass, minus the GPU",CODE_COSINE))
out.append(callout("The line that breaks old habits",[
 "Your page's score at the selection gate is a maximum, not a mean. Padding a page with more sections does not raise its audition score. Writing one section that nails one sub-query does."]))
out.append(h3("Reciprocal Rank Fusion, and why #1 is overrated"))
out.append(p("After N parallel sub-queries the system holds N ranked lists and needs one pool. It merges them with RRF: each document scores the sum, across every list it appears in, of one over a constant (conventionally k=60) plus its rank. The constant exists to stop any single list's top result from dominating, and it works by flattening the top of the curve almost completely."))
out.append(chart("rrfChart",240,"Figure 4. The RRF weighting curve at k=60. Rank #1 contributes 0.01639, rank #10 contributes 0.01429, a gap of just 13%."))
out.append(p("Thirteen percent. Every incremental effort spent moving a page from position ten to position one buys a 13% edge inside a single sub-query list. Appearing at all in a second sub-query list buys you close to 100%."))
out.append(chart("abChart",210,"Figure 5. Document B ranks #5 in four lists; Document A ranks #1 in one. B wins by 3.75x without ever winning a single sub-query."))
out.append(code("python - Reciprocal Rank Fusion in eight lines",CODE_RRF))
out.append(p("The fusion algorithm structurally favours content that addresses multiple facets over monolithic pages that optimise for one head term. It is the mathematical reason a "+L("topical authority cluster","/blogs/topical-authority-cluster-ai-shortlists")+" outperforms a hero page. And because the engine scores individual chunks against specific sub-queries, not domains against topics, "+L("passage relevance now outranks domain authority","/blogs/ranking-isnt-visibility")+": a small domain's explicit, dense, atomic answer can outscore a vague passage on a major publisher. Authority still helps at the selection gate, but it cannot manufacture a relevant chunk that does not exist."))

# 06 worked example
out.append(sec("06","example","What does fan-out do to a real buyer prompt?",
 "It reads the hard constraints and writes eight searches aimed at eight corpora.",
 "A mid-market healthcare-CRM prompt with four hard constraints (Epic integration, HIPAA, AI workflows, under $150/user) and one soft one decomposes into eight sub-queries, only one of which resembles a keyword anyone researches."))
out.append(p("A traditional engine would try to match 'enterprise CRM healthcare Epic EHR HIPAA under 150' and return a mess of sponsored pages. The AI system writes eight searches instead:"))
out.append(table("Table 3. The fan-out for a single mid-market buyer prompt. Only SQ-01 resembles a keyword anyone researches.",
 ["ID","Facet","Target corpus","Selection logic"],
 [["SQ-01","Product classification","Web index, review aggregators","Identify category leaders"],
  ["SQ-02","Technical compatibility","Vendor docs, app exchanges","Filter on a hard integration requirement"],
  ["SQ-03","Regulatory","Trust centres, security specs","Verify the mandatory legal framework"],
  ["SQ-04","Functional capability","Feature modules, product guides","Assess automation depth"],
  ["SQ-05","Commercial","Official pricing pages","Enforce the sub-$150 constraint"],
  ["SQ-06","Direct comparison","Comparative roundups","Analyse trade-offs between leaders"],
  ["SQ-07","Sentiment","Reddit, Quora, peer forums","Validate real implementation experience"],
  ["SQ-08","Edge case","Vendor FAQs, knowledge bases","Audit constraints on secondary candidate"]],
 cls=lambda j,c:"label" if j==0 else ""))
out.append(p("The synthesised answer highlights Vendor A for superior Epic integration (cited from technical docs), notes Vendor B as cost-effective but flags that Epic sync needs middleware (cited from a developer forum), and excludes Vendor C outright because its HIPAA BAA is restricted to tiers above $200. This is the mechanism behind most unexplained AI visibility losses. The page was fine. The coverage was not."))
out.append(callout("The vendor that lost",[
 "A competitor published one well-optimised landing page targeting 'best healthcare CRM'. It was excluded entirely, because it offered no extractable data for SQ-02, SQ-03 or SQ-05. It did not rank badly. It was never a candidate. There was nothing on the page for three of the eight questions to retrieve."]))

# 07 zero-volume
out.append(sec("07","zero-volume","Why can't keyword tools see the searches that matter?",
 "Because over 95% of generated sub-queries have zero recurring search volume.",
 "Keyword databases were built by measuring strings humans repeat. Fan-out sub-queries are written fresh by a model for one user's context and never typed by anyone. A tool that measures repetition cannot see a query that occurs once."))
out.append(p("So the standard workflow breaks at the first step, there is no volume report to sort descending. What replaces it: read the sub-queries Perplexity exposes for your category; mine your sales calls (buyer objections are almost verbatim what the orchestrator generates); enumerate your head term's facets deliberately (specification, compatibility, compliance, capability, price, comparison, sentiment, edge case); and watch which pages get cited for questions you never targeted. Search volume as a prioritisation metric is retiring. Facet coverage replaces it, the same shift measured in "+L("citation vs mention vs recommendation","/blogs/citation-vs-mention-vs-recommendation")+"."))
out.append(table("Table 4. The optimisation model before and after query fan-out.",
 ["Factor","Traditional SEO","Generative engine optimisation"],
 [["Primary goal","Rank #1 on a results page","Be cited inside a synthesised answer"],
  ["Targeting unit","One focus keyword per page","Whole intent clusters and entity facets"],
  ["Ranking signal","Domain authority, backlinks, exact match","Passage vector similarity, monosemantic chunks"],
  ["Volume model","High-volume head and mid-tail terms","Zero-volume sub-queries, ~95% invisible"],
  ["Content structure","Monolithic 2,500-word guide","Modular, self-contained, passage-level answers"],
  ["Technical focus","Core Web Vitals, mobile UX, JS rendering","Plain-HTML readability, fast crawl, schema"],
  ["Measurement","Clicks, keyword rankings, impressions","Citation frequency, share of voice by facet"]],
 cls=lambda j,c:"label" if j==0 else ""))

# 08 playbook
out.append(sec("08","playbook","How do you optimise for query fan-out?",
 "Four moves: write atomically, keep passages monosemantic, survive a non-rendering crawler, and build off-site.",
 "In rough order of return on effort. Almost none of it is measurable in the tools most teams pay for, which is the real transition cost."))
out.append(h3("1. Write atomically, and let headings do the retrieving"))
out.append(p("Engines extract 128-token chunks and score them independently, so build modular, self-contained sections where each fully answers one sub-question. Pages with headlines that directly answer specific sub-questions are cited by ChatGPT 41% of the time, against 29% for generic or artistic headlines, a twelve-point swing for writing your H2s as questions. The counterintuitive part: focused articles covering 26% to 50% of a topic's sub-queries beat massive single-page guides attempting 100%, because five focused pages produce five audition chunks, five title tags and five shots at the fusion pool, where one monster URL produces one of each. This is the shape of "+L("a high-citation page","/blogs/anatomy-of-a-high-citation-page")+"."))
out.append(chart("citeChart",210,"Figure 6. ChatGPT citation rate by headline style: question-style H2s (41%) vs generic or artistic headlines (29%)."))
out.append(code("html - the structural pattern that works",CODE_HTML))
out.append(p("Answer first, elaborate second. The chunker does not read ahead. If your answer arrives in paragraph four, it lands in a different chunk from the heading that promised it, and the two are scored separately."))
out.append(h3("2. Keep passages monosemantic"))
out.append(p("A passage is monosemantic when it stays cleanly on one concept. High monosemanticity keeps the embedding mathematically close to the target sub-query vector, maximising cosine similarity. Passages that blend several topics produce a vector that sits between all of them and scores mediocre against every sub-query. Practical test: take any 150-word block in isolation, with no heading, and ask what single question it answers. If you cannot name one, the chunk will not win one. This is the passage-level layer beneath "+L("how your page gets retrieved","/blogs/how-your-page-gets-retrieved")+"."))
out.append(h3("3. Make the facts survive a non-rendering crawler"))
out.append(p("Since OAI-SearchBot does not run client-side JavaScript, and 46% of ChatGPT retrieval passes fetch plain HTML, every fact you want cited must be in the server-side response, and under a two-second timeout. Use semantic HTML (article, section, h2, table); never render pricing, specs or compliance data client-side; use real HTML tables, not CSS grids or images; and ship JSON-LD, more in "+L("schema markup for AI citations","/blogs/schema-markup-ai-citations-2026")+" and "+L("how AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site")+"."))
out.append(callout("If your pricing table is rendered client-side",[
 "It does not exist. Not to a non-rendering crawler working under a two-second timeout. Any fact you want cited, pricing, specs, compliance terms, integration lists, has to be in the server-side HTML response."]))
out.append(code("json-ld - one block answers three sub-queries",CODE_JSONLD))
out.append(h3("4. Build the off-site footprint, because the fan-out leaves your domain"))
out.append(p("Sentiment sub-queries do not go to your website. They go to Reddit, Quora, G2 and Capterra, because the engine is cross-validating your claims against people who are not you. Domains with strong profiles across those platforms see roughly 3x higher citation rates, and sites with very large referring-domain footprints are around 3.5x more likely to be cited. A fan-out of eight sub-queries might send only four at content you control; the other four go to corpora you can influence but not own. That is the argument for "+L("authority seeding","/blogs/authority-seeding-ai-llm-trust")+" and "+L("why AI cites Reddit, G2 and analysts","/blogs/why-ai-cites-reddit-g2-analysts")+"."))

# 09 measurement
out.append(sec("09","measure","How do you measure any of this?",
 "Rank tracking answers a question the engine no longer asks. Expected citation replaces it.",
 "Expected citation decomposes into retrieval probability (a coverage problem, do you have a passage that can win sub-query i at all) and selection probability (a quality and authority problem, does your audition chunk beat the others)."))
out.append(p("Most teams have spent a decade optimising selection for a handful of queries while leaving retrieval at zero for most of the fan-out. A workable loop, without buying anything: build a prompt set of 30 to 50 real buyer questions; run them across ChatGPT Search, AI Mode and Perplexity weekly, logging every cited domain; capture the sub-queries where the interface exposes them; score whether you were cited, mentioned without a link, and which facet you were cited for; and track share of voice by facet. Gaps by facet tell you what to write next, the discipline behind "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+"."))
out.append(code("python - minimal citation tracker",CODE_TRACKER))

# 10 monday
out.append(sec("10","monday","What should you do this week?",
 "Decompose your five best prompts by hand, audit facets not keywords, and start the log.",
 "The baseline you do not capture this month is the comparison you will want in six."))
out.append("<ul>"
 "<li>Pick your five highest-value buyer prompts and decompose them by hand with the eight-facet frame: specification, compatibility, compliance, capability, price, comparison, sentiment, edge case. You will find gaps within twenty minutes.</li>"
 "<li>Audit the facets, not the keywords. For each sub-query, ask whether any single passage on your site answers it in under a hundred words. If not, that is a brief.</li>"
 "<li>Rewrite your H2s as questions, then move the answer into the first forty words underneath each.</li>"
 "<li>Curl your own pages with JavaScript disabled. Anything missing from that response is invisible to a meaningful share of AI retrieval.</li>"
 "<li>Split the monster guide. One page carrying twenty facets has one audition chunk and one title tag; five focused pages have five of each.</li>"
 "<li>Claim the off-domain surfaces: review profiles, documentation, community answers, entity records. Half the fan-out never touches your site.</li>"
 "<li>Start the prompt log now. Thirty prompts, weekly, three engines, in a sheet.</li></ul>")
out.append(pull("AI search does not reward the best page for a query. It rewards the most consistently useful source across a set of queries you will never see."))

# FAQ
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

REFS=[
 ("What Is Query Fan-Out in SEO and How Does It Affect Your Rankings? Netstager.","https://blog.netstager.com/query-fan-out-in-seo/"),
 ("Query Fan-Out Analysis Tool: Analyze AI Query Decomposition. Finseo.","https://www.finseo.ai/query-fanout-analysis"),
 ("Google AI Mode's Query Fan-Out Technique: What It Means for SEO. Aleyda Solis.","https://www.aleydasolis.com/en/ai-search/google-query-fan-out/"),
 ("What Is Query Fan-Out and How Does It Work for AI Searches? Search Engine Land.","https://searchengineland.com/guide/query-fan-out"),
 ("What Is Query Fan-Out and Why Does It Matter? Semrush.","https://www.semrush.com/blog/query-fan-out/"),
 ("Query Fan-Out: Everything You Need To Know. Surfer.","https://surferseo.com/blog/query-fan-out/"),
 ("How ChatGPT Search Works: The 7-Stage Pipeline Behind Every Answer. Rankly.","https://www.tryrankly.com/blogs/how-chatgpt-search-works"),
 ("What Is Query Fan-Out? Understanding the Hidden Queries Driving AI Search. GEOly.","https://www.geoly.ai/blog/query-fan-out"),
 ("LegalMALR: Multi-Agent Query Understanding and LLM-Based Reranking. arXiv.","https://arxiv.org/html/2601.17692v1"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
out.append('<div class="about-block" id="references"><div class="about-label">Sources and further reading</div>'
           '<p style="margin-bottom:16px;">The pipeline analyses and measurements this deep dive draws on.</p>'
           f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-led analysis of how search, retrieval and AI answer engines actually work. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Figures are original illustrations built from the cited data. Percentages are drawn from published third-party measurements and should be read as directional rather than exact.</p></div>')

body="\n".join(out)

# --- inline source attributions on stat-heavy sentences ---
SRC={"Rankly":"https://www.tryrankly.com/blogs/how-chatgpt-search-works",
 "Netstager":"https://blog.netstager.com/query-fan-out-in-seo/",
 "GEOly":"https://www.geoly.ai/blog/query-fan-out",
 "Finseo":"https://www.finseo.ai/query-fanout-analysis",
 "Aleyda Solis":"https://www.aleydasolis.com/en/ai-search/google-query-fan-out/",
 "Surfer":"https://surferseo.com/blog/query-fan-out/"}
def _cite(s): return f' (<a href="{SRC[s]}" target="_blank" rel="noopener" style="font-family:var(--f-mono);font-size:11px;color:var(--mute);text-decoration:none;border-bottom:1px solid var(--rule);">{s}</a>)'
CITES=[
 ("A single ChatGPT Deep Research prompt has been documented triggering over 400.","GEOly"),
 ("If the complex score clears roughly 0.4, the system enters a recursive multi-turn planner.","Rankly"),
 ("Your body copy is not consulted at this stage; your title tag is doing all the work.","Rankly"),
 ("Survivors are fetched three to ten at a time under a hard two-second render timeout, then parsed into uniform, non-overlapping 128-token chunks","Rankly"),
 ("Empirical work found 46% of ChatGPT crawler requests operating in plain-HTML mode.","Netstager"),
 ("pages that rank for the associated fan-out sub-queries are 161% more likely to be cited in AI Overviews than pages that rank only for the primary query.","Surfer"),
 ("Google issues up to sixteen parallel sub-searches across four corpora at once","Aleyda Solis"),
 ("That is your content brief, written by the machine that will grade it.","Finseo"),
 ("It merges them with RRF: each document scores the sum, across every list it appears in, of one over a constant (conventionally k=60) plus its rank.","GEOly"),
 ("a vague passage on a major publisher","Netstager"),
 ("over 95% of generated sub-queries have zero recurring search volume.","Netstager"),
 ("against 29% for generic or artistic headlines, a twelve-point swing for writing your H2s as questions.","Netstager"),
 ("High monosemanticity keeps the embedding mathematically close to the target sub-query vector, maximising cosine similarity.","Aleyda Solis"),
 ("and sites with very large referring-domain footprints are around 3.5x more likely to be cited.","Netstager"),
]
for anc,s in CITES:
    n=body.count(anc)
    if n==1: body=body.replace(anc, anc+_cite(s), 1)
    else: print("  !! CITE anchor x%d: %s"%(n,anc[:45]))

SIDEBAR=[("1 -> 12","average fan-out width per prompt"),("95%","of decisive searches have zero keyword volume"),("13%","the RRF edge from rank 10 to rank 1"),("3.75x","how much #5-in-four beats #1-in-one")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#what"><span class="toc-num">01</span>What fan-out is</a></li>'
     '<li><a href="#numbers"><span class="toc-num">02</span>The hidden searches</a></li>'
     '<li><a href="#chatgpt"><span class="toc-num">03</span>ChatGPT, stage by stage</a></li>'
     '<li><a href="#engines"><span class="toc-num">04</span>Google & Perplexity</a></li>'
     '<li><a href="#math"><span class="toc-num">05</span>The math that decides</a></li>'
     '<li><a href="#example"><span class="toc-num">06</span>A worked example</a></li>'
     '<li><a href="#zero-volume"><span class="toc-num">07</span>The zero-volume problem</a></li>'
     '<li><a href="#playbook"><span class="toc-num">08</span>The playbook</a></li>'
     '<li><a href="#measure"><span class="toc-num">09</span>How to measure it</a></li>'
     '<li><a href="#monday"><span class="toc-num">10</span>What to do this week</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this deep dive</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - how AI search fans one prompt into many sub-queries - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["query fan-out","AI search","generative engine optimization","GEO","reciprocal rank fusion","query decomposition","ChatGPT Search","Google AI Mode","Perplexity","sub-queries","vector embeddings"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Query Fan-Out: How AI Search Works &middot; rawmktg."
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

  var d=document.getElementById('distChart');
  if(d){new Chart(d,{type:'bar',data:{labels:['1-4','5-11','12-19','20-28','200-400+'],datasets:[{data:[17,59,24,3,1],backgroundColor:['#5B7FB3',signal,'#5B7FB3','#5B7FB3','#5B7FB3'],borderRadius:4,barThickness:30}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of prompts';}}}},
      scales:{x:{beginAtZero:true,max:70,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var r=document.getElementById('rrfChart');
  if(r){var labels=[],vals=[];for(var i=1;i<=10;i++){labels.push('#'+i);vals.push(1/(60+i));}
    new Chart(r,{type:'line',data:{labels:labels,datasets:[{data:vals,borderColor:signal,backgroundColor:rgba(signal,0.15),borderWidth:2,pointRadius:3,pointBackgroundColor:signal,fill:true,tension:0.1}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' RRF weight '+c.raw.toFixed(5);}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'},title:{display:true,text:'rank within one sub-query list',color:text,font:{family:mono,size:9}}},y:{ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v.toFixed(4);}},grid:{color:grid}}}}});}

  var a=document.getElementById('abChart');
  if(a){new Chart(a,{type:'bar',data:{labels:['Doc B (#5 x4 lists)','Doc A (#1 x1 list)'],datasets:[{data:[0.06154,0.01639],backgroundColor:[up,neutral],borderRadius:4,barThickness:44}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' RRF score '+c.raw.toFixed(5);}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var c=document.getElementById('citeChart');
  if(c){new Chart(c,{type:'bar',data:{labels:['Question-style H2s','Generic / artistic headlines'],datasets:[{data:[41,29],backgroundColor:[up,neutral],borderRadius:4,barThickness:56}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' cited '+c.raw+'% of the time';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,max:50,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">AI Search Mechanics &middot; Technical Deep Dive</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/fo_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/fo_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,"| h1:",hh.count("<h1"),
 "| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faq:",hh.count('faq-item'),"| refs:",hh.count('id="references"'),"| cbcopy:",'cb-copy-css' in hh)
