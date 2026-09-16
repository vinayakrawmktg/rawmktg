#!/usr/bin/env python3
"""SCRATCH: surface ai-visibility-tools-compared."""
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="ai-visibility-tools-compared"; URL=f"https://rawmktg.com/blogs/{SLUG}"
TITLE="AI Visibility Tools, Compared"
TOPIC="Measurement &middot; Buyer's Guide"
DESC_CARD="An honest 2026 comparison of the platforms that track whether AI answers cite your brand, Profound, Peec, Otterly, AthenaHQ and the rest, with published pricing and which to buy by profile."
IMG="/assets/images/ai-visibility-tools-compared-card"
PUB="2026-09-16"
CARD=(f'      <a href="/blogs/{SLUG}" class="article-card">\n'
 f'        <img src="{IMG}.webp" srcset="{IMG}-400.webp 400w, {IMG}-700.webp 700w, {IMG}.webp 1000w" '
 f'sizes="(max-width:768px) calc(100vw - 40px), (max-width:1024px) 46vw, 340px" alt="{TITLE}: a 2026 buyer\'s guide" class="card-img" loading="lazy" width="1000" height="525">\n'
 f'        <div class="card-body">\n          <div class="card-topic">{TOPIC}</div>\n'
 f'          <div class="card-title">{TITLE}</div>\n          <p class="card-desc">{DESC_CARD}</p>\n'
 f'          <div class="card-footer"><span class="card-arrow" aria-hidden="true">&rarr;</span></div>\n        </div>\n      </a>\n')

anc='<a href="/blogs/share-of-model-measurement" class="article-card">'
# research.html cluster 5
s=open("research.html",encoding="utf-8").read(); assert SLUG not in s and anc in s
s=s.replace(anc, CARD.lstrip()+anc if False else CARD+anc, 1) if False else s
# insert preserving: put CARD before the first occurrence's line
i=s.find(anc); ls=s.rfind("\n",0,i)+1
s=s[:ls]+CARD+s[ls:]; open("research.html","w",encoding="utf-8").write(s); print("research card ok")
# topic ranking-signals
s=open("topics/ranking-signals.html",encoding="utf-8").read(); assert SLUG not in s and anc in s
i=s.find(anc); ls=s.rfind("\n",0,i)+1
s=s[:ls]+CARD+s[ls:]; open("topics/ranking-signals.html","w",encoding="utf-8").write(s); print("topic card ok")
# sitemap
s=open("sitemap.xml",encoding="utf-8").read(); assert SLUG not in s
entry=(f'  <url>\n    <loc>{URL}</loc>\n    <lastmod>{PUB}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
a2='  <url>\n    <loc>https://rawmktg.com/blogs/share-of-model-measurement</loc>'
assert a2 in s; s=s.replace(a2, entry+a2,1); open("sitemap.xml","w",encoding="utf-8").write(s); print("sitemap ok")
# feed
s=open("feed.xml",encoding="utf-8").read(); assert SLUG not in s
fdesc=("A 2026 buyer's guide to AI visibility tracking tools, the platforms that run a fixed prompt set against ChatGPT, Google AI Overviews and AI Mode, Perplexity, Gemini and Copilot and record whether your brand is named, which URLs are cited, and which competitors are recommended instead. Names and compares Profound (enterprise depth, ~11 engines, $99-$499+/mo), Peec AI and AthenaHQ (clean mid-market analytics, ~$95-$495 and ~$295/mo), Otterly.ai (agency/budget, $29+ with a 25-factor GEO audit), Scrunch, and the SEO incumbents (Semrush, SE Ranking). Covers the five evaluation axes (platform coverage, prompt methodology, data depth, actionability, pricing transparency), which tool to buy by profile, a minimum-viable tracker in ~12 lines of Python, and the gap none of them close: tracking is not remediation. Published pricing as of September 2026; independent, unaffiliated.")
item=(f'    <item>\n      <title><![CDATA[AI Visibility Tools, Compared (2026 Buyer\'s Guide) &middot; rawmktg.]]></title>\n'
 f'      <link>{URL}</link>\n      <guid isPermaLink="true">{URL}</guid>\n      <pubDate>Tue, 16 Sep 2026 00:00:00 +0000</pubDate>\n'
 f'      <description><![CDATA[{fdesc}]]></description>\n    </item>\n')
a3='    <item>\n      <title><![CDATA[Clean Site, Zero Citations'
assert a3 in s; s=s.replace(a3, item+a3,1)
s=re.sub(r'<lastBuildDate>[^<]+</lastBuildDate>','<lastBuildDate>Tue, 16 Sep 2026 00:00:00 +0000</lastBuildDate>',s,1)
open("feed.xml","w",encoding="utf-8").write(s); print("feed ok")
# llms.txt
s=open("llms.txt",encoding="utf-8").read(); assert SLUG not in s
llm=("- [AI Visibility Tools, Compared (2026 Buyer's Guide)](https://rawmktg.com/blogs/ai-visibility-tools-compared) - September 2026. "
 "Independent comparison of AI visibility / GEO tracking tools: platforms that run a fixed buyer-question prompt set against AI answer engines "
 "(ChatGPT, Google AI Overviews and AI Mode, Perplexity, Gemini, Copilot, plus Grok/Claude/Rufus/Meta AI/DeepSeek on the broadest tools) on a "
 "schedule and log whether your brand is named, which URLs are cited, and which competitors are recommended instead. Compared, with published "
 "September-2026 entry pricing: Profound (enterprise depth and governance, ~11 engines, ~$99/$399 billed annually, enterprise ~$499+/mo); "
 "Peec AI (clean self-serve analytics, ~$95/$245/$495); AthenaHQ (~$295/mo mid-market); Otterly.ai (agency/budget, $29/$189/$489 + enterprise "
 "$1,000+, 25-factor per-prompt GEO audit); Scrunch AI (~$250/mo, broadening to a DXP); and SEO incumbents Semrush AI Toolkit and SE Ranking "
 "(bundled but shallower). Five evaluation axes: platform coverage, prompt methodology (>=5 runs per prompt, editable set), data depth (share "
 "of voice, sentiment, cited URLs, competitors), actionability, pricing transparency. Which to buy by profile (enterprise -> Profound; "
 "mid-market -> Peec/Athena; agency/budget -> Otterly; already on an SEO suite -> its module). Includes a ~12-line minimum-viable Python "
 "tracker and the key argument: these tools measure but do not remediate; tracking whether you are cited is a different job from diagnosing "
 "why and generating the fix. Independent and unaffiliated; pricing changes often.\n")
a4="- [Clean Site, Zero Citations"
assert a4 in s; s=s.replace(a4, llm+a4,1); open("llms.txt","w",encoding="utf-8").write(s); print("llms ok")
print("done")
