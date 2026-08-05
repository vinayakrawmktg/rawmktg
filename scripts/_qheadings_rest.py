#!/usr/bin/env python3
"""SCRATCH: question-format headings for the remaining 3 topics. Do NOT commit."""
import re, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

CONFIG = {
# ---------- technical-layer ----------
"blogs/how-ai-crawlers-index-your-site.html": [
  ("crawl-landscape","Which crawlers actually index your site for AI?",None),
  ("crawler-behaviour","How does each AI crawler actually behave?",None),
  ("js-rendering-gap","Can AI crawlers read JavaScript-rendered content?",None),
  ("verifying-crawlers","How do you tell real AI crawlers from spoofed ones?",None),
  ("robots-sitemap","How should you configure robots.txt and sitemaps for AI crawlers?",None),
  ("geo-optimisations","Which GEO optimisations actually move the needle?",None),
],
"blogs/schema-markup-ai-citations-2026.html": [
  ("search-architecture","How do modern AI search architectures process a query?","By decomposing it into parallel sub-queries."),
  ("ahrefs-study","Does schema markup actually increase AI citations?","Not as a direct boost, but cited pages carry it far more often."),
  ("ingestion-mechanics","How do RAG pipelines parse and chunk structured data?","Structured metadata can lift accuracy by up to 300%."),
  ("graph-architecture","How should you structure schema with a single @graph block?","One JSON-LD @graph script per page."),
  ("multi-platform","How do you optimise schema across ChatGPT, Gemini and Perplexity?","They barely overlap: only ~11% of cited URLs do."),
  ("comparison-page","How do comparison pages win evaluation-stage AI citations?","By owning 'A vs B' queries with structured comparisons."),
],
# ---------- content-authority ----------
"blogs/authority-seeding-ai-llm-trust.html": [
  ("paradigm-shift","How has authority shifted from link graphs to semantic networks?","Models learn from how the whole web describes you."),
  ("dual-pathway","What are the two pathways generative search uses to cite you?","Pre-trained memory and real-time retrieval."),
  ("citation-gauntlet","What does content pass through to earn an AI citation?","A five-gate citation gauntlet."),
  ("platform-profiles","How differently do ChatGPT, Claude, Perplexity and AI Overviews cite?","Each retrieves and trusts sources differently."),
  ("vertical-playbooks","How should authority seeding differ by industry?","Each vertical needs a tailored seeding strategy."),
  ("execution-blueprint","How do you build an off-site signal stack, phase by phase?","Through five coordinated phases."),
],
"blogs/hallucination-proofing-your-brand.html": [
  ("paradigm","01: How do SEO, AEO and GEO differ?","They optimise for fundamentally different goals."),
  ("hallucination-anatomy","02: Why does AI hallucinate about your brand?","Not randomly: it fills gaps in your data."),
  ("research","03: What does the GEO research actually say?","The Princeton GEO study is the empirical foundation."),
  ("schema","04: How does Schema.org make your brand machine-readable?","It is the primary structured-data signal AI parses."),
  ("llms-txt","05: What does /llms.txt tell AI crawlers about you?","Who you are, in a format models read first."),
  ("claim-anchoring","06: How do you anchor claims so AI quotes them accurately?","By pairing every claim with verifiable proof."),
  ("before-after","07: What does claim-anchored content look like, before and after?","The delta between marketing copy and GEO copy is stark."),
  ("monitoring","08: How do you monitor GEO performance?","By sampling non-deterministic answers repeatedly."),
  ("roadmap","09: What does a 4-phase GEO rollout look like?","A phased transition to hallucination-resistant content."),
],
"blogs/topical-authority-cluster-ai-shortlists.html": [
  ("pagerank","01: How is GEO different from PageRank SEO?","Rank on a list versus become the recommendation."),
  ("rag-pipeline","02: How does the RAG pipeline decide what to recommend?","Content must clear each retrieval stage."),
  ("depth-vs-breadth","03: Does topical depth or breadth win in AI search?","Depth beats a broad semantic footprint."),
  ("geo-bench","04: What did the Princeton GEO-bench actually find?","Depth, specificity and citations drive visibility."),
  ("five-pillars","05: What makes a brand citable by AI?","Five pillars turn the GEO-bench findings into a program."),
  ("three-gaps","06: Why do most B2B brands fail to surface in LLM answers?","Three recurring gaps block them."),
  ("cluster-architecture","07: How do you build a topical authority cluster for AI?","A hybrid of optimised first-party pages and off-site nodes."),
  ("llms-txt","08: How do llms.txt and schema lower the cost of being cited?","By minimising the compute cost of crawling you."),
  ("share-of-model","09: How do you measure AI visibility with Share of Model?","Keyword volume and rankings no longer apply."),
],
# ---------- ranking-signals ----------
"blogs/30-day-content-half-life-recency-ai-ranking-signal.html": [
  ("paradigm-shift","Why is evergreen content losing its AI citations?","Recency is now a hard ranking signal."),
  ("anatomy","How fast do AI citations decay after 30 days?","A meaningful share is lost within the first month."),
  ("technical-architecture","Why is recency a hard ranking signal, not a preference?","Three mechanisms structurally bias toward fresh content."),
  ("platform-breakdown","How does each AI engine weigh content freshness?","They do not treat recency uniformly."),
  ("zero-click","How does zero-click search change content ROI?","Citations matter even when nobody clicks through."),
  ("on-page-blueprint","What does AI-ready content actually look like?","Extractable, without rebuilding the page."),
  ("refresh-system","How often should you refresh content to keep AI citations?","On a programmatic cadence, not by publishing more."),
  ("measurement","How do you measure AI citation performance?","Rankings and clicks no longer capture it."),
],
"blogs/eeat-is-an-ai-signal-now.html": [
  ("paradigm-shift","How did E-E-A-T move from a search signal to a model weight?","It is now baked into LLM parameters."),
  ("alignment-pipeline","How do human preferences get encoded into model trust?","Through deliberate post-training alignment."),
  ("factuality-layer","How do models learn to prefer factual sources?","Through factuality-aware preference tuning."),
  ("activation-space","Where does trustworthiness actually live inside an LLM?","In the model's activation space, not just its outputs."),
  ("content-warehouse","How does Google score content quality automatically?","Through signals stored in its Content Warehouse."),
  ("quality-rater-guidelines","How do Google's 2025 rater guidelines treat AI content?","They draw a hard line on low-effort AI content."),
  ("mageo","What is next at the GEO research frontier?","Automated, multi-agent optimisation methods."),
  ("geo-trinity","Which on-page tactics most increase AI citations?","Statistics, quotations and source citations."),
  ("off-page","How do you build off-page authority for AI search?","With entity footprints, not backlinks alone."),
],
"blogs/prompt-to-citation-tracking.html": [
  ("paradigm-shift","01: How is GEO measurement different from SEO measurement?","You track citations, not rankings."),
  ("engines","02: How does citation behaviour differ across AI engines?","Each engine has a structurally different home turf."),
  ("portfolio","03: How do you design a prompt portfolio to track citations?","It is the off-site monitoring layer of the stack."),
  ("crawlers","04: How do you make your site legible to AI crawlers?","Audit and govern your content chunks first."),
  ("ga4","05: How do you attribute AI-search sessions in GA4?","On-site analytics must capture what off-site tools miss."),
  ("looker","06: How do you report GEO results in Looker Studio?","Blend off-site prompts with on-site analytics."),
  ("loop","07: How does GEO measurement actually drive action?","A stack only earns its keep if it changes the work."),
],
}

# anatomy: §N spans, no id, no capsule -> heading-only questions (sentence case)
ANATOMY = [
 ("Headings engineered for query fan-out","How do you engineer headings for query fan-out?"),
 ("Paragraph density: the inverted pyramid","What paragraph density gets content cited?"),
 ("The citation ski ramp: where on the page matters","Where on the page do AI citations come from?"),
 ("Claim-level citations as TrustRank signals","How do claim-level citations build trust?"),
 ("Schema as machine-readable contract","What role does schema play in getting cited?"),
 ("Platform divergence and the commercial value of citations","How do platforms diverge, and why do citations have commercial value?"),
 ("The editorial standard that separates cited from invisible","What editorial standard separates cited pages from invisible ones?"),
]

th=cap=0
for path, items in CONFIG.items():
    h=open(path,encoding="utf-8").read()
    for sid,newinner,lead in items:
        pat=re.compile(r'(<h2 id="'+re.escape(sid)+r'">)(<span class="section-num">\d+</span>)?(.*?)(</h2>)', re.S)
        if not pat.search(h): print("MISS",path,sid); continue
        h=pat.sub(lambda m:m.group(1)+(m.group(2) or '')+newinner+m.group(4), h, count=1); th+=1
        if lead:
            cpat=re.compile(r'(<h2 id="'+re.escape(sid)+r'">.*?</h2>\s*<div class="section-answer">)(?!<strong>)', re.S)
            h2c=cpat.sub(lambda m:m.group(1)+'<strong>'+lead+'</strong> ', h, count=1)
            if h2c!=h: cap+=1; h=h2c
    open(path,"w",encoding="utf-8").write(h)

# anatomy
ap="blogs/anatomy-of-a-high-citation-page.html"
h=open(ap).read(); an=0
for old,new in ANATOMY:
    if "</span>"+old+"</h2>" in h:
        h=h.replace("</span>"+old+"</h2>", "</span>"+new+"</h2>",1); an+=1
    else: print("MISS anatomy:",old)
open(ap,"w").write(h)

print(f"id headings converted: {th} | capsule leads: {cap} | anatomy headings: {an}")
allfiles=list(CONFIG)+[ap]
print("em dashes:", sum(open(p).read().count("—") for p in allfiles))
