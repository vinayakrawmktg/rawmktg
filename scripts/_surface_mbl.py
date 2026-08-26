#!/usr/bin/env python3
"""SCRATCH: surface mentions-beat-links into listings/sitemap/feed/llms + inbound links."""
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="mentions-beat-links"; URL=f"https://rawmktg.com/blogs/{SLUG}"
TITLE="Digital PR &amp; Data Studies"
TOPIC="Content &amp; Authority &middot; Digital PR"
DESC_CARD="Your domain is under 10% of AI citation sources. Original research seeded off-site is what generative engines actually cite, plus the study spec and a 90-day play."
IMG="/assets/images/mentions-beat-links-card"

CARD=(f'      <a href="/blogs/{SLUG}" class="article-card">\n'
 f'        <img src="{IMG}.webp" srcset="{IMG}-400.webp 400w, {IMG}-700.webp 700w, {IMG}.webp 1000w" '
 f'sizes="(max-width:768px) calc(100vw - 40px), (max-width:1024px) 46vw, 340px" alt="{TITLE}: The Link Play AI Cites" class="card-img" loading="lazy" width="1000" height="525">\n'
 f'        <div class="card-body">\n'
 f'          <div class="card-topic">{TOPIC}</div>\n'
 f'          <div class="card-title">{TITLE}: The Link Play AI Cites</div>\n'
 f'          <p class="card-desc">{DESC_CARD}</p>\n'
 f'          <div class="card-footer"><span class="card-arrow" aria-hidden="true">&rarr;</span></div>\n'
 f'        </div>\n      </a>\n')

# 1. index.html cluster 04 (Content & authority): insert as first card in that cluster's grid
s=open("index.html",encoding="utf-8").read()
assert SLUG not in s
i=s.find("Content &amp; authority architecture")
assert i>0, "cluster 04 head missing"
g=s.find('<div class="article-grid">', i)
open_tag='<div class="article-grid">\n'
gi=g+len(open_tag)
assert s[g:gi]==open_tag, "grid open format mismatch"
s=s[:gi]+CARD+s[gi:]
open("index.html","w",encoding="utf-8").write(s)
print("index cluster04 card added")

# 2. content-authority topic page: first card
s=open("topics/content-authority.html",encoding="utf-8").read()
assert SLUG not in s
anc='<a href="/blogs/comparison-pages-ai-shortlists" class="article-card">'
assert anc in s
s=s.replace('      '+anc, CARD+'      '+anc, 1)
open("topics/content-authority.html","w",encoding="utf-8").write(s)
print("topic page card added")

# 3. sitemap.xml
s=open("sitemap.xml",encoding="utf-8").read()
assert SLUG not in s
entry=(f'  <url>\n    <loc>{URL}</loc>\n    <lastmod>2026-08-26</lastmod>\n'
       f'    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
anc='  <url>\n    <loc>https://rawmktg.com/blogs/comparison-pages-ai-shortlists</loc>'
assert anc in s
s=s.replace(anc, entry+anc,1); open("sitemap.xml","w",encoding="utf-8").write(s); print("sitemap ok")

# 4. feed.xml newest item + build date
s=open("feed.xml",encoding="utf-8").read()
assert SLUG not in s
fdesc=("Digital PR for AI search. Your owned domain is only 5-10% of the sources a generative engine cites (McKinsey); ~82% trace to "
 "earned editorial media (Muck Rack). An Ahrefs analysis of ~75,000 brands puts mention frequency at 0.664 correlation with AI citation "
 "inclusion vs 0.204 for backlinks, roughly 3x the signal. The GEO experiment (Princeton/GT/AI2/IIT Delhi) shows attributed quotes (+41%) "
 "and precise statistics (+31%) are the top citation levers and keyword stuffing is negative (-8%); an original data study is the only "
 "asset that produces both. Covers stat units and citable stat density, the study spec, distribution into the top 15 domains that hold "
 "68% of citations, the unlinked-mention reporting shift, Article+Dataset+Organization schema, brand mention share measurement, the "
 "citation lag, the Dark AI attribution gap (70.6% referrer-stripped), and a 90-day sequence.")
item=(f'    <item>\n      <title><![CDATA[Digital PR & Data Studies: The Link Play AI Cites &middot; rawmktg.]]></title>\n'
 f'      <link>{URL}</link>\n      <guid isPermaLink="true">{URL}</guid>\n'
 f'      <pubDate>Wed, 26 Aug 2026 00:00:00 +0000</pubDate>\n'
 f'      <description><![CDATA[{fdesc}]]></description>\n    </item>\n')
anc='    <item>\n      <title><![CDATA[The Broken-Sitemap Tax'
assert anc in s
s=s.replace(anc, item+anc,1)
s=re.sub(r'<lastBuildDate>[^<]+</lastBuildDate>','<lastBuildDate>Wed, 26 Aug 2026 00:00:00 +0000</lastBuildDate>',s,1)
open("feed.xml","w",encoding="utf-8").write(s); print("feed ok")

# 5. llms.txt bullet
s=open("llms.txt",encoding="utf-8").read()
assert SLUG not in s
llm=("- [Digital PR and Data Studies: The Link Play AI Cites](https://rawmktg.com/blogs/mentions-beat-links) - August 2026. The off-site "
 "authority layer for AI search. Your owned domain is only 5-10% of the source citations in AI answers (McKinsey); the rest is earned "
 "editorial, review platforms, aggregators and community you do not control, and ~82% of AI citations trace to earned editorial media "
 "(Muck Rack). Mentions beat links: an Ahrefs analysis of ~75,000 brands puts web-wide brand mention frequency at 0.664 Spearman "
 "correlation with AI citation inclusion vs 0.204 for backlinks (~3x the signal); links still drive crawler discovery but are no longer "
 "the dominant term, and Google-organic vs AI-cited overlap collapsed from ~70% to under 20% (83% of AI Overview citations sit outside the "
 "organic top ten). The GEO experiment (Princeton/Georgia Tech/AI2/IIT Delhi, SIGKDD 2024) tested 9 modifications on a 10,000-query "
 "benchmark: attributed quotations +41% and precise statistics +31% are the top position-adjusted-word-count levers, keyword stuffing is "
 "-8%; strategies stack with heavy overlap (model ~50%, not 85%); when all sources optimise, visibility redistributes to challengers "
 "(rank 5 +115.1%, rank 1 -30.3%). The highest-yield PR asset is an original data study because it natively produces both top levers; "
 "+239% median citation lift from syndicated research. Four archetypes (survey, internal telemetry, index/benchmark, meta-analysis); "
 "telemetry is nearly free and unreplicable. Design in stat units (precise number + named methodology + attributed quote in a sub-45-word "
 "block); citable stat density should clear 4 per 1,000 words; write the headline before the survey; publish the raw dataset. Distribution "
 "is concentrated: top 15 domains hold ~68% of AI citations (5WPR, 680M citations), so 30 placements in retrieved domains beat 300 in the "
 "long tail; entity corroboration index log-weights independent domains (two domains beat four mentions on one); sequence an exclusive "
 "first. The unlinked mention is near-complete for retrieval, track mention volume per domain, not links. Package the hub front-loaded "
 "(44.2% of citations from the first 30%), deep (>20k chars = ~4.3x citations) and modular, with Article+Dataset+Organization JSON-LD "
 "(~45% higher citation rates; Wikidata explains up to 49.9% of B2B recommendation variance); allow OAI-SearchBot, not just GPTBot. "
 "Measure brand mention share over many runs (5 min, 10 better); the cited domains are your outreach list. Report the citation lag "
 "(mentions lead, citations lag) and the Dark AI gap (70.6% referrer-stripped, dark sessions convert at 10.21% vs 2.46% baseline). "
 "Includes a 90-day sequence, 6 formulas (stacked lift, citable stat density, entity corroboration index, brand mention share, hidden "
 "dark-AI revenue, cost per citation point) and working YAML/Python/JSON-LD/robots code.\n")
anc="- [The Broken-Sitemap Tax: XML Sitemaps for AI Discovery]"
assert anc in s
s=s.replace(anc, llm+anc,1); open("llms.txt","w",encoding="utf-8").write(s); print("llms.txt ok")
print("done insertions")
