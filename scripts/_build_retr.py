#!/usr/bin/env python3
"""SCRATCH: build blogs/how-your-page-gets-retrieved.html (chunking & embeddings / RAG retrieval). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="how-your-page-gets-retrieved"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-08-05"
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

HEADLINE="How Your Page Gets Retrieved"
DECK=("Chunking, embeddings and the rerank funnel. Every AI engine breaks your page apart before it considers citing you, "
      "here is what happens inside, why good content loses at the boundary, and how to write pages that survive the cut.")
DESC=("AI engines never read your page, they read chunks of it, scored alone. How chunking, embeddings, vector drift and "
      "reranking decide what gets cited, and how to write for it.")
DATANOTE=("A retrieval-mechanics teardown grounded in published research and vendor engineering documentation, Anthropic's "
          "contextual retrieval, Jina AI's late chunking, the Matryoshka and ColBERT papers, and the RAGAS evaluation framework, "
          "2024-26. Figures are drawn from those cited sources; code is illustrative.")

CODE_PROMPT=r'''<document>
{{WHOLE_DOCUMENT_TEXT}}
</document>

<chunk>
{{TARGET_CHUNK_TEXT}}
</chunk>

Please give a succinct context (50-100 tokens) to situate this
chunk within the overall document, to improve search retrieval.
Answer only with the contextual prefix and nothing else.'''

CODE_COSINE=r'''# What dense retrieval actually computes, stripped to essentials
import numpy as np

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query  = embed("how long does onboarding take")
chunks = [embed(c) for c in page_chunks]

scores  = [cosine(query, c) for c in chunks]
ranking = np.argsort(scores)[::-1]

# Only the top handful ever reach the model.
top_k = [page_chunks[i] for i in ranking[:5]]'''

CODE_RRF=r'''# Reciprocal Rank Fusion, the whole idea in a few lines
K = 60

def rrf(rankings, weights=None):
    scores = {}
    for i, ranked_ids in enumerate(rankings):
        w = (weights or [1] * len(rankings))[i]
        for rank, doc_id in enumerate(ranked_ids, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + w / (K + rank)
    return sorted(scores, key=scores.get, reverse=True)

# Dense search carries more weight than keyword search
final = rrf([dense_results, bm25_results], weights=[0.8, 0.2])'''

out=[]
out.append('<p class="lead">'+norm("Here is the uncomfortable part. When an AI assistant answers a question and cites a source, no model read your page, not the way a person does, not top to bottom. Your page was pulled apart into passages, each converted into a list of numbers and stored in an index. The question became numbers too, and the system went looking for the closest match.")+'</p>')
out.append(p("The unit that competed was never your page. It was a fragment of it, maybe three hundred words long, sitting alone in a database with no title, no navigation, and no memory of the paragraph above it. Teams still write for the page, measure at the page level, and audit at the page level, meanwhile the thing being judged is a passage they never saw in isolation."))
out.append(pull("Your page is the container. The chunk is the competitor."))
out.append(p("This piece walks the whole pipeline, because the shape of the machine determines the shape of the content that wins inside it. Once you can see where passages get cut, where meaning leaks out, and where the ranking actually happens, a lot of vague advice about \"writing for AI\" collapses into something specific, the mechanical layer beneath "+L("how RAG actually works","/blogs/how-rag-actually-works")+"."))
out.append(statgrid([("200-800","tokens per indexed passage"),("1536","embedding dimensions, any input length"),("80/20","dense-to-sparse fusion, k=60"),("5-20","chunks survive from ~150 candidates")]))

# 01
out.append(sec("01","why-cut","Why does your page get cut up at all?","Because a fixed-size vector cannot hold a whole page without dissolving its details, so systems split first, then encode each passage on its own budget.",
  "An embedding model takes text of any length and returns a fixed-length list of numbers, usually 384 to 1536 of them. A tweet gets 1536 numbers; a 4,000-word guide gets 1536 numbers. The model has a fixed budget of expressive capacity and must spend it across everything in the text."))
out.append(p("Feed it one tight paragraph about pricing tiers and the vector strongly encodes pricing tiers. Feed it your entire product page and the vector encodes something like \"general B2B software marketing page\", with the pricing detail smeared into near-invisibility. That is not a bug, it is the arithmetic of compression: specific numbers, named entities and precise claims lose signal strength relative to the dominant topic of the document. Chunking is the fix, split the document into smaller passages before encoding and each passage gets its own full budget."))
out.append(callout("But cutting costs you something too",[
 "Go too far the other way and you break the thing that made the text useful. Chop a document into hyper-granular fragments and you destroy the macro narrative, leaving isolated statements stripped of the detail that gave them meaning. Every retrieval system sits somewhere on this trade-off, and where it sits determines what it can find. Most production systems land between 200 and 800 tokens per chunk, roughly 150 to 600 words.",
]))

# 02
out.append(sec("02","four-cuts","What are the four ways your page gets cut?","Fixed-size windows, sentence/paragraph boundaries, semantic-distance boundaries, and structural header parsing, and only the last one follows your intent.",
  "The algorithm that decides where the cuts fall determines the entire shape of the index built from your content, and the four approaches are not equally kind to well-structured writing."))
out.append(table("Boundary strategies compared, and what each does to your writing",["Strategy","How it cuts","What it buys","What it breaks"],[
 ("Fixed-size sliding window","Static token count with a fixed stride overlap.","Almost no compute cost; predictable memory.","Bisects named entities, formulas and logical propositions."),
 ("Sentence / paragraph","Punctuation and newline delimiters.","Preserves local syntax and clause structure.","Variable lengths create unstable embedding density."),
 ("Semantic distance","Cuts where cosine similarity drops between adjacent sentences.","Boundaries land on genuine topic shifts.","High ingestion latency, a forward pass per sentence."),
 ("Structural headers","Markdown headers and HTML DOM nodes.","Preserves the organisation you actually intended.","Collapses on inconsistent or malformed markup."),
], cls=lambda j,c:"label" if j==0 else ("up" if (j==2) else "neg" if j==3 else "")))
out.append(callout("What this changes about how you write",[
 "You cannot control which algorithm indexes you, and different assistants use different ones. What you can control is making your content survive all four: real heading tags, semantically complete sections, and topic shifts that align with structural breaks give every parser the same answer, which is also "+"why "+L("clean internal structure decides retrieval","/blogs/internal-linking-for-ai-retrieval")+".",
]))

# 03
out.append(sec("03","context-rupture","What is context rupture, and why does good content fail?","Because standard pipelines encode each chunk alone, a passage that never names its own subject drifts out of range of the query it should answer, even when the fact is correctly indexed.",
  "This is the single most important mechanic in the article, and it explains why genuinely excellent content sometimes gets no AI visibility at all. Passages lean heavily on the document around them; isolate a segment and anaphoric references lose their target nouns."))
out.append(callout("A concrete example, two adjacent chunks",[
 "Chunk A: \"ACME Corporation expanded its robotics division in Q3.\"",
 "Chunk B: \"The division achieved a 14% revenue increase over the prior fiscal year.\"",
 "Chunk B has the answer, the number, the growth rate. And it will not be retrieved. Nothing in it says ACME, robotics, or Q3. Embedded on its own, its vector is positioned entirely on its isolated text, so the query \"ACME Corporation Q3 financial performance\" lands somewhere else and Chunk B falls outside the nearest-neighbour radius. The fact exists, it is correctly indexed, and it cannot be found.",
]))
out.append(pull("Most content does not fail because it is thin. It fails because its best paragraphs cannot say what they are about."))
out.append(p("Now audit your own writing: pronouns carrying the subject across paragraphs, section three referring to \"this approach\" from section two, a case study where the client name appears once in the intro and never again, comparison tables where product names live in the header row and the rows say \"it\" and \"the platform\". All of that is fine for a human reader. All of it produces orphaned chunks, the same failure that makes "+L("AI misdescribe a brand it can't cleanly resolve","/blogs/hallucination-proofing-your-brand")+"."))

# 04
out.append(sec("04","patches","How do retrieval systems patch the problem?","Two ways: generative contextualisation prepends a written summary to each chunk before indexing; late chunking runs the whole document through the encoder first and slices after. Together they cut retrieval failures by up to 67%.",
  "Engineers noticed the failure and built two very different fixes, and understanding both tells you what the systems reward."))
out.append(h3("Fix one: generative contextual augmentation"))
out.append(p("Before embedding a chunk, send it to a language model with the full parent document and ask for a short prefix explaining what the chunk is about, then glue that prefix on and index the combined text. A chunk reading \"Operating margins expanded by 240 basis points\" becomes \"This chunk is from the Q2 2023 financial statement for ACME Corporation... Operating margins expanded by 240 basis points\". The rewritten passage resolves the pronouns, names the entity, anchors the timeframe, and the explicit terms become searchable in the keyword index too. This is "+L("Anthropic's contextual retrieval","https://www.anthropic.com/engineering/contextual-retrieval",True)+"."))
out.append(code("The prompt that writes the context prefix",CODE_PROMPT))
out.append(p("The measured gains are not marginal. On standard evaluation sets, contextual prefixes on dense embeddings cut top-20 retrieval failure by 35% against a naive pipeline; pair them with contextual keyword search and failures drop 49%; add a reranking stage and the reduction reaches 67%."))
out.append(chart("retFail",210,"Figure 1, retrieval failure reduction across the stack. Each layer targets a different cause, which is why the gains compound instead of overlapping. Source: Anthropic contextual retrieval."))
out.append(p("Read those numbers as a diagnosis, not a benchmark: two thirds of retrieval failures in a naive system are caused by problems that have nothing to do with content quality, context loss, vocabulary mismatch, and bad ranking. All three have content-side counterparts. And it is cheap: key-value prompt caching gives cache reads a ~90% token discount, so ingestion lands near $1 per million document tokens, which means you should assume the systems reading your content already do this and are already compensating for some of your ambiguity. Some, not all."))
out.append(h3("Fix two: late chunking"))
out.append(p("The more elegant approach reverses the order of operations. Traditional pipelines split first and encode second, so attention only ever sees one isolated chunk. "+L("Late chunking","https://jina.ai/news/late-chunking-in-long-context-embedding-models/",True)+" feeds the entire document through a long-context encoder in one pass, so every token vector already encodes global context, and only then applies chunk boundaries, pooling across the token slice. It preserves cross-chunk dependencies and document-level context without changing the vector's dimensions, and adds no query-time cost."))
out.append(table("The two fixes compared, same problem, different mechanisms",["Axis","Generative contextualisation","Late chunking"],[
 ("Depends on","An external LLM API or local generative model.","A long-context transformer embedder (8k+ tokens)."),
 ("Ingestion speed","Slower, bound by token generation.","Fast, one encoder pass per document."),
 ("Effect on keyword search","Large, adds real searchable words to the sparse index.","None, the underlying text is untouched."),
 ("How context is stored","Explicitly, as text prepended to the passage.","Implicitly, inside the attention layers."),
 ("Operational complexity","Higher, needs caching, orchestration, retries.","Lower, needs slice-based pooling support."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(callout("The content implication",[
 "Late chunking recovers context that exists in your document. It cannot invent context that was never written down. If your page never states the entity, the timeframe, or the qualifier anywhere in the surrounding text, no amount of attention across the document will surface it. Explicit beats implicit, every time.",
]))

# 05
out.append(sec("05","vector-space","What happens inside the vector space?","Text becomes points in a continuous space; closeness is measured by cosine angle; and the first filter judges only coarse topical signal, so a passage that takes four sentences to reveal its subject may never reach the stage where its detail counts.",
  "Cosine similarity measures the angle between two vectors and ignores magnitude, which stops passage length from distorting relevance, that is the standard for text. Dot product and Euclidean distance are the alternatives, and at the dense stage your chunk either scores in the top handful or it does not exist."))
out.append(code("What dense retrieval computes, in essence",CODE_COSINE))
out.append(p("Two refinements matter for content. Matryoshka embeddings nest meaning hierarchically, coarse topic in the leading dimensions, fine detail later, which enables a cheap first pass on a 64-dimensional prefix before rescoring the shortlist on full vectors. The blunt consequence: the first filter your chunk faces is deliberately coarse, judging on broad topical signal alone, so passages whose topic is unmistakable in the opening lines pass it. And multi-vector models like "+L("ColBERT keep token-level vectors and score with MaxSim","/blogs/internal-linking-for-ai-retrieval")+", which rewards passages containing the literal terminology of the question, not just its general vibe. The exact words still matter."))

# 06
out.append(sec("06","funnel","What funnel does your chunk have to survive?","Four filters: dense and sparse search running together, reciprocal rank fusion merging them, then a cross-encoder reranker that narrows ~150 candidates to the 5-20 that reach the model. Most content dies at the reranker.",
  "Dense vector search is one stage of several, and content usually dies at a different stage than people assume."))
out.append(pipeline([("Dense + sparse","vectors for concepts, BM25 for exact terms"),("Rank fusion","merge by rank, dense 80 / keyword 20"),("Cross-encoder rerank","~150 candidates scored jointly"),("Context window","the 5-20 that reach the model")],3,
  "Figure 2, the production funnel. Four filters between an indexed chunk and a chunk that gets quoted."))
out.append(p("Dense vectors are excellent at intent and synonyms and weak at exact lookups (part numbers, SKUs, proper nouns), so BM25 keyword search runs alongside. BM25's term-frequency component saturates, so the tenth mention of a keyword adds almost nothing and dilutes your passage on the vector side, there is no version of this system where stuffing works. The two score scales are incompatible, so "+L("Reciprocal Rank Fusion","/blogs/internal-linking-for-ai-retrieval")+" throws away raw scores and operates on rank positions, commonly weighting dense 80% and keyword 20%. The passage that wins is rarely the best on either axis, it is the one that is good on both."))
out.append(code("Reciprocal Rank Fusion, the whole idea",CODE_RRF))
out.append(pull("Being retrieved is not the same as being read. A chunk at rank 40 in the candidate pool is invisible in exactly the same way as a chunk that was never indexed."))
out.append(p("The reranker is where most outcomes are decided. Dense retrieval uses a bi-encoder that embeds query and passage separately (what makes pre-indexing possible); a cross-encoder runs both through one transformer together, letting every query word attend to every passage word. Far more accurate, far too expensive to run over the whole index, so it runs as a second pass over 100 to 150 candidates and narrows them to the 5 to 20 that build the final context."))

# 07
out.append(sec("07","failures","What are the three failure modes, and their fixes?","Semantic fragmentation, lexical mismatch, and ranking degradation, each with an engineering fix and a content-side counterpart you actually control.",
  "Retrieval failures group cleanly into three architectural categories, and diagnosing which one you have matters more than any generic optimisation."))
out.append(table("Three failure modes, and the content response to each",["Failure mode","What happens","Your content-side fix"],[
 ("Semantic fragmentation","Chunking split related facts across passages; no single vector matches.","Write sections that are semantically complete, every section names its own subject."),
 ("Lexical mismatch","Dense search misses exact constraints, part numbers, identifiers, versions.","Vocabulary discipline, use the literal category, competitor and version terms buyers type."),
 ("Ranking degradation","The right chunk is retrieved but sits too low to make the window.","Directness, answer the query head-on, early, in language that mirrors the question."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Clever renaming of a known category is a lexical mismatch you are inflicting on yourself. And cross-encoders reward passages that answer the query head-on: a passage that opens with three sentences of throat-clearing loses to one that opens with the answer, the same shape as "+L("any high-citation page","/blogs/anatomy-of-a-high-citation-page")+"."))

# 08
out.append(sec("08","playbook","How do you write content that survives the cut?","By being clearer than you needed to be: self-contained sections, named subjects, front-loaded answers, real structure, self-describing tables, and specific facts. None of it means writing worse for humans.",
  "Everything above collapses into a manageable set of habits, and they mostly amount to writing every section as if it will be read alone, because it will be."))
out.append(table("A pre-publish checklist derived from the mechanics",["Check","What good looks like","Failure it prevents"],[
 ("Section independence","Every H2 makes full sense read alone, with no prior paragraph.","Semantic fragmentation"),
 ("Entity naming","The subject is named by name at least once inside every section.","Vector drift"),
 ("Temporal anchors","Dates and periods stated explicitly, never \"last year\".","Vector drift"),
 ("Answer position","The core claim appears in the first two sentences of the section.","Ranking degradation"),
 ("Vocabulary match","Uses the literal category and product terms buyers type.","Lexical mismatch"),
 ("Markup integrity","Real H2 and H3 tags in a clean, consistent hierarchy.","Bad boundary placement"),
 ("Table framing","A summary line above each table; subjects repeated in row labels.","Structural fragmentation"),
 ("Specificity","Concrete numbers and named entities, not general characterisation.","Compression loss"),
], cls=lambda j,c:"label" if j==0 else ("neg" if j==2 else "")))
out.append(p("Front-loading the answer helps at three separate stages at once, coarse first-pass filtering, cross-encoder scoring, and the moment a model decides which passage to quote, which is exactly what the "+L("answer-block optimizer","/tools/answer-block-optimizer")+" checks. Naming the subject in every section directly reduces fragmentation, the highest-leverage change a content team can make, and it is the same explicitness that "+L("makes you resolvable as an entity","/blogs/becoming-an-entity")+"."))
out.append(callout("The authority connection",[
 "None of this replaces authority. Retrieval mechanics determine whether your passage can be found; corroboration across independent sources, consistent entity naming, and genuine subject depth determine whether it gets trusted once it is. Mechanics get you into the candidate pool. "+L("Authority","/blogs/authority-seeding-ai-llm-trust")+" is what survives the reranker.",
]))

# 09
out.append(sec("09","measure","How do you tell whether any of this is working?","With two metrics, context precision (is the good material near the top) and context recall (was everything needed retrieved at all), plus a manual buyer-question loop you can run without touching anyone's index.",
  "Retrieval quality is measurable, and the two metrics that matter are worth borrowing even if you never run a formal evaluation. They pull against each other, governed by the retrieval window size."))
out.append(chart("retPR",210,"Figure 3, precision and recall as a function of retrieval window size. Retrieve fifty chunks and recall climbs while precision falls; retrieve two and precision peaks while facts spread across passages go missing. Every system picks a point on this curve."))
out.append(table("The retrieval metrics worth knowing",["Metric","What it measures","What a low score is telling you"],[
 ("Context precision","Signal-to-noise and ranking quality.","Ranking is weak, relevant passages exist but sit too low."),
 ("Context recall","Completeness of retrieved information.","The candidate window is too narrow, or facts are fragmented."),
 ("Context entity recall","Coverage of named entities.","Vocabulary and entity-naming gaps between query and corpus."),
 ("Faithfulness","Whether generated claims are grounded in context.","The generator is hallucinating past what was retrieved."),
 ("Answer relevancy","Whether the output addresses the actual question.","Instruction-following failure downstream of retrieval."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("You will not run RAGAS on someone else's index, but a manual equivalent is genuinely useful: build 30 to 50 questions your buyers actually ask in their words; run each through the assistants that matter and record whether you appear and which passage got quoted; for the misses, read the passage on your site that should have answered it in isolation, with no title and no surrounding text. In most cases the reason is visible in ten seconds, the passage does not name its subject, does not state its qualifier, or buries the answer four sentences deep. Fix the passage, not the page, then "+L("re-run the same question set in four to six weeks","/blogs/prompt-to-citation-tracking")+". Different assistants weight these stages differently, which is part of "+L("why engines recommend different vendors","/blogs/why-engines-recommend-different-vendors")+"."))

# takeaway
out.append(sec("10","takeaway","What's the takeaway?","At every step, the same content property is rewarded: explicitness. Passages that name their subject, state their qualifiers, use the vocabulary of the question, and answer it directly.",
  "Retrieval is not a black box. It is a sequence of mechanical steps, each of which discards content for a specific and knowable reason: your document gets split because a fixed vector cannot hold a page; the split severs relationships; engineering compensates with contextualisation and late chunking; then dense and keyword search merge by rank fusion and get filtered by a cross-encoder before anything reaches a model."))
out.append(pull("Write every section as if it will be read alone. Because it will be."))
out.append(p("That is not a hack, and it will not stop working when the architectures change. It is simply what it looks like to write for a reader who arrives in the middle, with no context, and only a few seconds of attention to spend, which, as it turns out, describes most human readers too."))

FAQ=[
 ("Do AI search engines read my whole page?","No. Before an AI engine can cite you, your page is split into passages (typically 150-600 words, 200-800 tokens), each converted into a fixed-length vector and stored in an index. When someone asks a question, that question is vectorised too and the system retrieves the closest-matching passages, not pages. The unit that competes for a citation is a single chunk, scored alone with no title, no navigation and no memory of the paragraph above it, so writing and auditing at the page level misses where the contest actually happens."),
 ("Why does my best content sometimes get zero AI visibility?","Usually context rupture. Standard pipelines embed each chunk in isolation, so a passage that carries its meaning through pronouns or references to earlier paragraphs, \"the division\", \"this approach\", \"last year\", loses its subject when cut. Its vector lands away from the query's vector and it falls outside the nearest-neighbour search radius, so the fact is correctly indexed but cannot be found. The fix is to name the subject, state the timeframe, and repeat the qualifier inside every section."),
 ("What is contextual retrieval and late chunking?","Two engineering fixes for context rupture. Contextual retrieval (Anthropic) uses an LLM to write a short prefix naming a chunk's subject and timeframe before indexing it, cutting top-20 retrieval failures by 35%, rising to 67% when combined with keyword search and reranking. Late chunking (Jina AI) runs the whole document through a long-context encoder first so every token vector carries global context, then slices, preserving cross-chunk meaning at no query-time cost. Both recover context that was written down, neither can invent context you never stated."),
 ("How do I write content that gets retrieved and cited?","Write every H2 section so it makes sense read alone: name the subject by name at least once, state dates explicitly, put the core claim in the first two sentences, use the literal terms buyers type (category, competitor and version names), keep real H2/H3 markup, add a summary line above every table, and prefer concrete numbers over general characterisation. These reduce the three failure modes, semantic fragmentation, lexical mismatch and ranking degradation, without writing worse for humans."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
REFS=[
 ("Contextual Retrieval in AI Systems. Anthropic.","https://www.anthropic.com/engineering/contextual-retrieval"),
 ("jina-ai/late-chunking: code for explaining and evaluating late chunking. GitHub.","https://github.com/jina-ai/late-chunking"),
 ("Late Chunking in Long-Context Embedding Models. Jina AI.","https://jina.ai/news/late-chunking-in-long-context-embedding-models/"),
 ("A Step-by-Step RAG Evaluation Process & Key Metrics Explained. Openxcell.","https://www.openxcell.com/blog/rag-evaluation/"),
 ("RAG Evaluation Metrics: Best Practices. Patronus AI.","https://www.patronus.ai/llm-testing/rag-evaluation-metrics"),
 ("Matryoshka Representation Learning (arXiv:2205.13147). arXiv.","https://arxiv.org/abs/2205.13147"),
 ("Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models (PDF). arXiv.","https://arxiv.org/pdf/2409.04701"),
 ("Enhancing RAG with contextual retrieval. Claude Cookbook.","https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide"),
 ("Late Chunking: Contextual Chunk Embeddings (v3). arXiv.","https://arxiv.org/html/2409.04701v3"),
 ("Late Chunking: Contextual Chunk Embeddings (v2). arXiv.","https://arxiv.org/html/2409.04701v2"),
 ("Chunking Strategies for LLM Applications. Pinecone.","https://www.pinecone.io/learn/chunking-strategies/"),
 ("Contextual Retrieval in Retrieval-Augmented Generation (RAG). Box Blog.","https://blog.box.com/contextual-retrieval-in-retrieval-augmented-generation-rag"),
 ("Implementing Anthropic's Contextual Retrieval with Async Processing. Instructor.","https://python.useinstructor.com/blog/2024/09/26/implementing-anthropics-contextual-retrieval-with-async-processing/"),
 ("Late Chunking vs Contextual Retrieval: The Math Behind RAG's Context Problem. KX Systems on Medium.","https://medium.com/kx-systems/late-chunking-vs-contextual-retrieval-the-math-behind-rags-context-problem-d5a26b9bbd38"),
 ("Introducing Contextual Retrieval by Anthropic. r/Rag, Reddit.","https://www.reddit.com/r/Rag/comments/1fl2wma/introducing_contextual_retrieval_by_anthropic/"),
 ("Late Chunking in RAG: Improving Text Retrieval Performance. Bluetick Consultants.","https://www.bluetickconsultants.com/unlocking-better-text-retrieval-with-late-chunking-a-revolutionary-approach-for-rag-applications/"),
 ("MIPIC: Matryoshka Representation Learning via Self-Distilled Intra-Relational and Progressive Information Chaining. arXiv.","https://arxiv.org/html/2604.24374v2"),
 ("MaxSim Operator in Dense Retrieval. Emergent Mind.","https://www.emergentmind.com/topics/maxsim-operator"),
 ("Late Chunking: Embedding First, Chunk Later. Stackademic.","https://blog.stackademic.com/late-chunking-embedding-first-chunk-later-long-context-retrieval-in-rag-applications-3a292f6443bb"),
 ("Ragas Evaluation: In-Depth Insights. PIXION Blog.","https://pixion.co/blog/ragas-evaluation-in-depth-insights"),
 ("RAG Evaluation Simplified, Part 2: Deep Dive into Recall & Precision. Medium.","https://medium.com/@fassha08/rag-evaluation-simplified-part-2-deep-dive-into-recall-precision-4853709630bb"),
 ("Context Recall. Ragas Documentation.","https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/"),
 ("Metrics. Ragas Documentation.","https://docs.ragas.io/en/v0.1.21/concepts/metrics/"),
 ("Evaluating RAG Applications with RAGAs. Leonie Monigatti.","https://www.leoniemonigatti.com/blog/rag-evaluation-with-ragas.html"),
 ("Context Precision. Ragas Documentation.","https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/"),
 ("Contextual retrieval in Anthropic using Amazon Bedrock Knowledge Bases. AWS.","https://aws.amazon.com/blogs/machine-learning/contextual-retrieval-in-anthropic-using-amazon-bedrock-knowledge-bases/"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
out.append('<div class="about-block" id="references"><div class="about-label">References</div>'
           '<p style="margin-bottom:16px;">The research and engineering sources this teardown draws on.</p>'
           f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, retrieval mechanics and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Sources: Anthropic contextual retrieval, Jina AI late chunking, the Matryoshka Representation Learning and ColBERT papers, Pinecone chunking guidance, and the RAGAS evaluation framework, 2024-26. Code is illustrative; figures are drawn from the cited sources.</p></div>')

body="\n".join(out)

SIDEBAR=[("-67%","Retrieval failures eliminated, contextual + BM25 + rerank"),("200-800","Tokens per competing passage"),("5-20","Chunks that reach the model, from ~150")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#why-cut"><span class="toc-num">01</span>Why it gets cut</a></li>'
     '<li><a href="#four-cuts"><span class="toc-num">02</span>Four ways it gets cut</a></li>'
     '<li><a href="#context-rupture"><span class="toc-num">03</span>Context rupture</a></li>'
     '<li><a href="#patches"><span class="toc-num">04</span>How systems patch it</a></li>'
     '<li><a href="#vector-space"><span class="toc-num">05</span>Inside the vector space</a></li>'
     '<li><a href="#funnel"><span class="toc-num">06</span>The retrieval funnel</a></li>'
     '<li><a href="#failures"><span class="toc-num">07</span>Three failure modes</a></li>'
     '<li><a href="#playbook"><span class="toc-num">08</span>The writing playbook</a></li>'
     '<li><a href="#measure"><span class="toc-num">09</span>Is it working?</a></li>'
     '<li><a href="#takeaway"><span class="toc-num">10</span>The takeaway</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - chunking, embeddings and the rerank funnel - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["RAG","retrieval","chunking","embeddings","late chunking","contextual retrieval","reranking","BM25","reciprocal rank fusion","GEO","AI visibility"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="How Your Page Gets Retrieved: Chunking &amp; Embeddings &middot; rawmktg."
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

  var rf=document.getElementById('retFail');
  if(rf){var rl=['Naive embeddings','Contextual embeddings','Contextual + BM25','Contextual + rerank'];var rv=[0,35,49,67];
    new Chart(rf,{type:'bar',data:{labels:rl,datasets:[{data:rv,backgroundColor:rv.map(function(v){return v>=67?signal:v>=49?rgba(signal,0.75):v>=35?rgba(signal,0.55):neutral;}),borderRadius:4,barThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.raw===0?' baseline':' -'+c.raw+'% top-20 retrieval failures';}}}},
      scales:{x:{beginAtZero:true,max:75,ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v?'-'+v+'%':'base';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var pr=document.getElementById('retPR');
  if(pr){var lab=['2','5','10','20','50'];
    new Chart(pr,{type:'line',data:{labels:lab,datasets:[
      {label:'Precision',data:[0.95,0.85,0.72,0.56,0.4],borderColor:signal,backgroundColor:'transparent',tension:0.35,borderWidth:2,pointRadius:3,pointBackgroundColor:signal},
      {label:'Recall',data:[0.4,0.63,0.79,0.9,0.97],borderColor:up,backgroundColor:'transparent',tension:0.35,borderWidth:2,pointRadius:3,pointBackgroundColor:up}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:10},boxWidth:10,boxHeight:10,padding:14}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+' '+Math.round(c.raw*100)+'%';}}}},
      scales:{x:{title:{display:true,text:'retrieval window (chunks)',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{min:0,max:1,ticks:{color:text,font:{family:mono,size:9},callback:function(v){return Math.round(v*100)+'%';}},grid:{color:grid}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">AI Search Mechanics &middot; Chunking &amp; Embeddings</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/retr_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/retr_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| cbcopy:",'cb-copy-css' in hh)
