#!/usr/bin/env python3
"""SCRATCH: surface clean-site-zero-citations into research/topic/sitemap/feed/llms."""
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="clean-site-zero-citations"; URL=f"https://rawmktg.com/blogs/{SLUG}"
TITLE="Clean Site, Zero Citations"
TOPIC="Industry Teardowns &middot; Investing &amp; Wealth"
DESC_CARD="41 investing and wealth companies scored on four AI tools: 36 of 41 got zero AI citations, and the five that appeared ran the messiest sites. Why retrieval is a gate, not a ranking factor."
IMG="/assets/images/clean-site-zero-citations-card"
PUB="2026-09-01"

CARD=(f'      <a href="/blogs/{SLUG}" class="article-card">\n'
 f'        <img src="{IMG}.webp" srcset="{IMG}-400.webp 400w, {IMG}-700.webp 700w, {IMG}.webp 1000w" '
 f'sizes="(max-width:768px) calc(100vw - 40px), (max-width:1024px) 46vw, 340px" alt="{TITLE}: an Investing and Wealth AI visibility teardown" class="card-img" loading="lazy" width="1000" height="525">\n'
 f'        <div class="card-body">\n'
 f'          <div class="card-topic">{TOPIC}</div>\n'
 f'          <div class="card-title">{TITLE}</div>\n'
 f'          <p class="card-desc">{DESC_CARD}</p>\n'
 f'          <div class="card-footer"><span class="card-arrow" aria-hidden="true">&rarr;</span></div>\n'
 f'        </div>\n      </a>\n')

anc='      <a href="/blogs/field-service-software-ai-visibility-gap" class="article-card">'

# 1. research.html industry teardowns cluster, before first card
s=open("research.html",encoding="utf-8").read()
assert SLUG not in s and s.count(anc)>=1
s=s.replace(anc, CARD+anc,1); open("research.html","w",encoding="utf-8").write(s); print("research card ok")

# 2. topics/industry-teardowns.html, before first card
s=open("topics/industry-teardowns.html",encoding="utf-8").read()
assert SLUG not in s and s.count(anc)>=1
s=s.replace(anc, CARD+anc,1); open("topics/industry-teardowns.html","w",encoding="utf-8").write(s); print("topic card ok")

# 3. sitemap.xml before the-link-liability
s=open("sitemap.xml",encoding="utf-8").read()
assert SLUG not in s
entry=(f'  <url>\n    <loc>{URL}</loc>\n    <lastmod>{PUB}</lastmod>\n'
       f'    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
anc2='  <url>\n    <loc>https://rawmktg.com/blogs/the-link-liability</loc>'
assert anc2 in s
s=s.replace(anc2, entry+anc2,1); open("sitemap.xml","w",encoding="utf-8").write(s); print("sitemap ok")

# 4. feed.xml newest item + build date
s=open("feed.xml",encoding="utf-8").read()
assert SLUG not in s
fdesc=("An AI-visibility teardown of 41 companies in the Investing & Wealth cohort (investing, wealth and digital-asset infrastructure), each "
 "scored against the same 48 buyer questions on ChatGPT, Google AI Overviews, Claude and Gemini -- 7,872 answers -- with 35 same-day site "
 "crawls (23,870 URLs). Headline: 36 of 41 companies were never named or linked in a single one of their 192 answers, and the segment occupies "
 "just 19% of the answer slot counting every overlap. The inversion: the five visible companies carried twice the median high-priority site "
 "problems of the invisible 36 -- the cleanest site (Juno, one problem, six URLs) scored zero, the messiest (Range, Pulley) got quoted -- so "
 "site hygiene does not appear in the signal (r=+0.25, not significant; confounded by publishing volume). Why: retrieval is a gate not a "
 "ranking factor, three multiplicative gates (retrievability, answer match, corroboration); the segment optimises gate 1 and dies at gate 2, "
 "no page answers the question. 314 of 328 vendor-stage cells are empty; Alternatives is a clean zero across all 41 companies and four tools. "
 "Ten domains own 37% of the slot and a third of that is trade media and adjacent vendors. The four tools disagree (Range is 6% and 17% at "
 "once), so single-tool 'AI visibility' is noise. 21% of losses cited no source at all -- a corroboration problem, not a content one. Reports "
 "four metrics to replace 'AI visibility': Answer Share, Stage Coverage Index, Decision-Stage Presence, Citable Surface Ratio. Includes a "
 "90-day sequence, the three-gate model, decision-page HTML with FAQ schema, and a gate-1 shell check. 10 figures, 7 tables, 4 code blocks.")
item=(f'    <item>\n      <title><![CDATA[Clean Site, Zero Citations: An Investing & Wealth AI-Visibility Teardown &middot; rawmktg.]]></title>\n'
 f'      <link>{URL}</link>\n      <guid isPermaLink="true">{URL}</guid>\n'
 f'      <pubDate>Mon, 01 Sep 2026 00:00:00 +0000</pubDate>\n'
 f'      <description><![CDATA[{fdesc}]]></description>\n    </item>\n')
anc3='    <item>\n      <title><![CDATA[The Link Liability'
assert anc3 in s
s=s.replace(anc3, item+anc3,1)
s=re.sub(r'<lastBuildDate>[^<]+</lastBuildDate>','<lastBuildDate>Mon, 01 Sep 2026 00:00:00 +0000</lastBuildDate>',s,1)
open("feed.xml","w",encoding="utf-8").write(s); print("feed ok")

# 5. llms.txt bullet before the-link-liability
s=open("llms.txt",encoding="utf-8").read()
assert SLUG not in s
llm=("- [Clean Site, Zero Citations: An Investing & Wealth AI-Visibility Teardown](https://rawmktg.com/blogs/clean-site-zero-citations) - "
 "September 2026. An AI-answer visibility teardown of 41 companies in the Investing & Wealth cohort (investing, wealth and digital-asset "
 "infrastructure), each scored against the same fixed 48 buyer questions across eight buying stages on ChatGPT, Google AI Overviews, Claude "
 "and Gemini (192 pairs per company, 7,872 answers), with 35 same-day production crawls totalling 23,870 URLs; binary scoring, brand named or "
 "a page on its domain linked. Headline: 36 of 41 companies were never named or linked in a single one of their 192 answers; only five appear "
 "(Range 12%, Cryptio/Pulley/Taxbit 2%, Utila 1%) and the segment holds just 19% of the slot counting every overlap. The inversion (the core "
 "finding): the five visible companies carried a median of 6 high-priority site problems vs 3 for the invisible 30, i.e. twice the technical "
 "debt; the cleanest site (Juno, one problem, six URLs) is invisible and the messiest (Pulley 10, Range 7) get quoted; correlation of hygiene "
 "with visibility is +0.25 and not significant (t=1.48), and collapses under a publishing-volume confound -- hygiene does not appear in the "
 "signal. Mechanism: retrieval is a gate, not a ranking factor; three multiplicative gates (1 retrievability: robots/noindex/status/title/H1, "
 "binary and cheap; 2 answer match: does a page address the question in the shape asked, continuous, where the segment dies; 3 corroboration: "
 "third-party mentions, entity consistency, original data). The segment optimises gate 1 (already passed) and never builds gate 2. Empty "
 "funnel: 314 of 328 vendor-stage cells are zero; Alternatives is a clean zero across all 41 companies and four tools -- the cheapest "
 "uncontested decision page in the category. Concentration: ten domains own 37% of the answer slot (fireblocks 8%, bitgo 6%, cobo 5%...), and "
 "11 of 37 points sit on trade media/niche publishers/adjacent vendors that do not sell what the cohort sells; winners are blog and list "
 "pages, not category assets. Tool disagreement: the four tools produce three shapes from five data points (Range is 6% on ChatGPT and 17% on "
 "Claude/Gemini), so any single-tool 'AI visibility' number is noise unless the tool, prompt set and date are named. 21% of losses cited no "
 "source at all (43 of 204) -- the model answered from parametric memory, a corroboration problem solved by presence in category roundups, "
 "trade media, directories and review sites, not by a better page. Crawl data is uniform and template-level: five template defects touched "
 "over 12,000 pages, so fix templates not pages; site size (6 to 1,540 URLs) predicts nothing. Replaces 'AI visibility' with four "
 "export-computable metrics, each reported with prompt set + tool + date: Answer Share (AS, mean 0.46%), Stage Coverage Index (SCI, 0.00 for "
 "36 of 41), Decision-Stage Presence (DSP, mean 0.31%, the revenue-predictive one), Citable Surface Ratio (CSR, 0.789; below ~0.7 go earn "
 "mentions). Sequence: weeks 1-2 clear retrieval blockers (cheap, ~3 problems/site, not for the number), weeks 2-8 publish decision pages "
 "(Alternatives first, then comparison, then pricing with real numbers), weeks 4-12 earn outside mentions in parallel, day 90 re-measure the "
 "same prompts. Same Investing & Wealth cohort as the link-liability backlink teardown. Includes the three-gate Python model, the four-metric "
 "scorecard code, decision-page HTML with an answer block and FAQ schema, and a gate-1 shell check. 10 original figures, 7 tables, 4 code "
 "blocks. Directional only: five non-zero outcomes; the 314/328 empty-cell count is not a correlation, it is a count.\n")
anc4="- [The Link Liability: What 41 Backlink Audits Reveal]"
assert anc4 in s
s=s.replace(anc4, llm+anc4,1); open("llms.txt","w",encoding="utf-8").write(s); print("llms.txt ok")
print("done insertions")
