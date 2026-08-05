#!/usr/bin/env python3
"""SCRATCH: question-format headings for the 'How AI search works' topic (4 articles).
Converts capsule-backed section headings to questions + short bold answer lead.
No TOC auto-edit (audited separately). Do NOT commit."""
import re, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

CONFIG = {
"blogs/geo-compounding-flywheel.html": [
  ("seven-step-loop","How does the GEO compounding flywheel work?","Through a seven-step, self-reinforcing loop."),
  ("retrieval-pipeline","How does AI retrieval actually decide what to cite?","Through a defined, multi-stage filter, not one algorithm."),
  ("princeton","What does the Princeton GEO study actually prove?","That specific content tactics measurably change AI citations."),
  ("share-of-citation","What is Share of Citation, and why does it matter?","It is the metric that actually tracks AI visibility."),
  ("implementation","How should you implement GEO across three workstreams?","In parallel, not in sequence."),
  ("executive-case","Why is GEO mathematically different from paid and SEO?","Because its returns compound instead of resetting."),
],
"blogs/geo-foundation-audit.html": [
  ("conversational-discovery","How is B2B search shifting to conversational discovery?","From crawled links to synthesised answers."),
  ("algorithmic-core","What is the algorithmic core of GEO?","Vector databases, embeddings, and real-time retrieval."),
  ("sourcing-fragmentation","Why do AI engines cite such different sources?","Because AI search is not a monolith."),
  ("framework","How do you run a GEO foundation audit, step by step?","As a structured diagnostic, not a guess."),
  ("benchmarks","How does AI citation visibility differ by industry?","Sharply: citation dynamics vary by vertical."),
  ("synthesized-pipeline","How do you capture the AI-synthesised pipeline?","Upgrade SEO, do not abandon it."),
],
"blogs/how-rag-actually-works.html": [
  ("chunking","Why is chunking the most underrated concept in GEO?","Because engines retrieve passages, not whole pages."),
  ("platforms","How do ChatGPT, Perplexity, and Gemini cite differently?","Same pipeline, three different ranking systems."),
  ("measurement","How do you measure GEO success?","With Citation Share, not keyword rankings."),
],
"blogs/why-engines-recommend-different-vendors.html": [
  ("architecture","01: How does each engine actually work?","They share no common retrieval architecture."),
  ("chatgpt","02: How does ChatGPT Search choose its sources?","A fine-tuned GPT-4o reading over Bing's index."),
  ("perplexity","03: How does Perplexity rank and cite sources?","As a live RAG engine with heavy source verification."),
  ("gemini","04: How do Gemini and AI Overviews pick what to cite?","Entity first, source documents second."),
  ("matrix","05: How should you prioritise GEO across the three engines?","Not by investing equally in all three."),
  ("roadmap","06: What does a 60-day multi-engine GEO rollout look like?","A unified rollout across ChatGPT, Perplexity and Gemini."),
  ("future","07: What comes after GEO citations?","Citations are the short game; agentic discovery is next."),
],
}

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
print(f"headings converted: {th} | capsule leads added: {cap}")
print("em dashes:", sum(open(p).read().count("—") for p in CONFIG))
