#!/usr/bin/env python3
"""SCRATCH: discoverability opt - glossary spoke-links, last-updated stamp, homepage entity node. Do NOT commit."""
import os, re, glob, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

TITLES={
 "internal-linking-for-ai-retrieval":"Internal Linking for AI Retrieval",
 "why-ai-cites-reddit-g2-analysts":"Why AI Cites Reddit, G2 & Analysts Over Your Website",
 "schema-markup-ai-citations-2026":"Schema Markup for AI Citations",
 "how-rag-actually-works":"How RAG Actually Works",
 "30-day-content-half-life-recency-ai-ranking-signal":"The 30-Day Content Half-Life",
 "anatomy-of-a-high-citation-page":"Anatomy of a High-Citation Page",
 "prompt-to-citation-tracking":"From Prompt to Citation: Tracking AI Visibility",
 "hallucination-proofing-your-brand":"Hallucination-Proofing Your Brand",
 "geo-foundation-audit":"The GEO Foundation Audit",
 "why-ai-cites-domo-over-databricks":"Why AI Cites Domo Over Databricks",
}
RULES=[
 (r'rag|retrieval-augmented|^retrieval|generative-engine$|answer-engine|llm-citation|gptbot|oai|perplexity|common-crawl|share-of-model|ai-overview','how-rag-actually-works'),
 (r'crawl|render|hydrat|javascript|index|sitemap|redirect|canonical|url-structure|site-architecture|orphan|noindex|duplicate|faceted|http-status|soft-404|internal-linking|core-web|cumulative-layout|interaction-to-next|largest-contentful|time-to-first|log-file|robots','internal-linking-for-ai-retrieval'),
 (r'authority|domain-rating|referring|e-e-a-t|seeding|unlinked-brand|link-intersect|citation-gap','why-ai-cites-reddit-g2-analysts'),
 (r'schema|graph|knowledge-graph|entity-resolution','schema-markup-ai-citations-2026'),
 (r'half-life|content-half|recency','30-day-content-half-life-recency-ai-ranking-signal'),
 (r'answer-capsule|answer-lead|proof-pairing|topical','anatomy-of-a-high-citation-page'),
 (r'llms-txt','internal-linking-for-ai-retrieval'),
 (r'prompt-portfolio|prompt-to-citation|ai-referral','prompt-to-citation-tracking'),
 (r'hallucinat','hallucination-proofing-your-brand'),
 (r'generative-engine-optimization|answer-engine-optimization','geo-foundation-audit'),
]
def target_for(slug):
    for pat,art in RULES:
        if re.search(pat,slug): return art
    return "geo-foundation-audit"

# ---- 1. glossary spoke-links ----
added=0
for f in glob.glob("glossary/*.html"):
    slug=os.path.basename(f)[:-5]
    tgt=target_for(slug)
    h=open(f,encoding="utf-8").read()
    if f'href="/blogs/{tgt}"' in h: continue  # already links to its pillar
    line=(f'\n<p style="font-family:var(--f-mono);font-size:12px;letter-spacing:.02em;color:var(--mute);margin:26px 0 0;padding-top:16px;border-top:1px solid var(--rule)">'
          f'Related reading: <a href="/blogs/{tgt}" style="color:var(--ink);text-decoration:underline;text-decoration-color:var(--signal)">{H.escape(TITLES[tgt])}</a></p>\n')
    # insert before newsletter section, else before footer, else </main>
    for anchor in ['<section class="newsletter-section"','<footer class="site-foot"','</main>']:
        idx=h.find(anchor)
        if idx!=-1:
            h=h[:idx]+line+h[idx:]; break
    open(f,"w",encoding="utf-8").write(h); added+=1
print("glossary spoke-links added:",added)

# ---- 2. last-updated stamp on blogs (from dateModified) ----
import datetime
MON=["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
stamped=0
for f in glob.glob("blogs/*.html"):
    h=open(f,encoding="utf-8").read()
    m=re.search(r'"dateModified":"(\d{4})-(\d{2})-(\d{2})"',h)
    if not m: continue
    y,mo=m.group(1),int(m.group(2))
    label=f"Updated {MON[mo]} {y}"
    # replace the eyebrow-date span content (first occurrence)
    new=re.sub(r'(<span class="eyebrow-date">)[^<]*(</span>)', r'\1'+label+r'\2', h, count=1)
    if new!=h:
        open(f,"w",encoding="utf-8").write(new); stamped+=1
print("blogs last-updated stamped:",stamped)

# ---- 3. homepage entity node ----
idx_html=open("index.html",encoding="utf-8").read()
if '"@id":"https://rawmktg.com/#org"' not in idx_html:
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"Organization","@id":"https://rawmktg.com/#org","name":"rawmktg.","url":"https://rawmktg.com",
       "logo":"https://rawmktg.com/assets/images/favicon-180.png",
       "description":"rawmktg. publishes data-driven teardowns, tools and a glossary on how AI search decides what to recommend.",
       "sameAs":["https://www.linkedin.com/company/rawmktg/"]},
      {"@type":"WebSite","@id":"https://rawmktg.com/#website","name":"rawmktg.","url":"https://rawmktg.com",
       "publisher":{"@id":"https://rawmktg.com/#org"},"inLanguage":"en"}
    ]}
    node='  <script type="application/ld+json">'+json.dumps(graph)+'</script>\n'
    idx_html=idx_html.replace("</head>",node+"</head>",1)
    open("index.html","w",encoding="utf-8").write(idx_html)
    print("homepage entity node: added")
else:
    print("homepage entity node: already present")
# validate it
import json as J
ix=open("index.html").read()
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',ix,re.S):
    try: J.loads(m.group(1))
    except Exception as e: print("BAD homepage jsonld",e)
print("DONE")
