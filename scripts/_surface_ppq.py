#!/usr/bin/env python3
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="pricing-page-ai-will-quote"; URL=f"https://rawmktg.com/blogs/{SLUG}"
TITLE="The Pricing Page AI Will Quote"
TOPIC="Content &amp; Authority &middot; Money Pages"
DESC_CARD="Buyers ask AI what things cost. If your price is trapped in an image, a widget, or a 'contact us', the model quotes a competitor or invents a number. How to write the page it lifts instead."
IMG="/assets/images/pricing-page-ai-will-quote-card"
PUB="2026-09-16"
CARD=(f'      <a href="/blogs/{SLUG}" class="article-card">\n'
 f'        <img src="{IMG}.webp" srcset="{IMG}-400.webp 400w, {IMG}-700.webp 700w, {IMG}.webp 1000w" '
 f'sizes="(max-width:768px) calc(100vw - 40px), (max-width:1024px) 46vw, 340px" alt="{TITLE}: pricing pages for AI search" class="card-img" loading="lazy" width="1000" height="525">\n'
 f'        <div class="card-body">\n          <div class="card-topic">{TOPIC}</div>\n'
 f'          <div class="card-title">{TITLE}</div>\n          <p class="card-desc">{DESC_CARD}</p>\n'
 f'          <div class="card-footer"><span class="card-arrow" aria-hidden="true">&rarr;</span></div>\n        </div>\n      </a>\n')

anc='<a href="/blogs/the-link-liability" class="article-card">'
for f in ["research.html","topics/content-authority.html"]:
    s=open(f,encoding="utf-8").read(); assert SLUG not in s and anc in s
    i=s.find(anc); ls=s.rfind("\n",0,i)+1
    s=s[:ls]+CARD+s[ls:]; open(f,"w",encoding="utf-8").write(s); print("card ->",f)

s=open("sitemap.xml",encoding="utf-8").read(); assert SLUG not in s
entry=(f'  <url>\n    <loc>{URL}</loc>\n    <lastmod>{PUB}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
a2='  <url>\n    <loc>https://rawmktg.com/blogs/the-link-liability</loc>'
assert a2 in s; s=s.replace(a2, entry+a2,1); open("sitemap.xml","w",encoding="utf-8").write(s); print("sitemap ok")

s=open("feed.xml",encoding="utf-8").read(); assert SLUG not in s
fdesc=("How to write a pricing page that AI answer engines will quote correctly. Buyers ask ChatGPT, Perplexity, Gemini and Google AI what products cost, and the answer is assembled from whatever the model can extract; if your price sits in an image, a JavaScript widget, or behind 'contact sales', the model quotes a competitor, an outdated figure, or hallucinates a number with your name on it. The fix has three reinforcing layers: real numbers in server-side text, led by an answer block that states every tier in the first 40-55 words; a parseable comparison table; and Product/Offer/PriceSpecification JSON-LD whose numbers match the page exactly. Covers making 'it depends' pricing quotable (floor, unit, typical case), why 'contact us' is the one answer a model cannot pass on, why old prices persist (cross-source corroboration, reconcile G2/Capterra/directories), JavaScript-rendering pitfalls, crawler access, a 10-point checklist, and how to measure whether engines quote your price correctly.")
item=(f'    <item>\n      <title><![CDATA[The Pricing Page AI Will Quote &middot; rawmktg.]]></title>\n'
 f'      <link>{URL}</link>\n      <guid isPermaLink="true">{URL}</guid>\n      <pubDate>Tue, 16 Sep 2026 06:00:00 +0000</pubDate>\n'
 f'      <description><![CDATA[{fdesc}]]></description>\n    </item>\n')
a3='    <item>\n      <title><![CDATA[AI Visibility Tools, Compared'
assert a3 in s; s=s.replace(a3, item+a3,1)
open("feed.xml","w",encoding="utf-8").write(s); print("feed ok")

s=open("llms.txt",encoding="utf-8").read(); assert SLUG not in s
llm=("- [The Pricing Page AI Will Quote](https://rawmktg.com/blogs/pricing-page-ai-will-quote) - September 2026. How to write a pricing page "
 "AI answer engines will quote correctly. AI frequently gets SaaS pricing wrong because the number a model returns is only as good as what it "
 "can extract, and most pricing pages hand it nothing: a price locked in an image, a JavaScript-rendered widget, or hidden behind 'contact "
 "sales', so the model falls back to stale training data, a review site, or a competitor, or invents a figure. Three reinforcing layers make a "
 "page quotable: (1) real numbers in server-side text, led by an answer block stating every tier's price in the first 40-55 words after the H1; "
 "(2) a parseable comparison table (not an image, not JS-only); (3) Product/Offer/PriceSpecification JSON-LD (UnitPriceSpecification for "
 "per-seat/per-unit) with numbers matching the visible page exactly, mismatched schema is worse than none. Make 'it depends' pricing quotable "
 "by publishing a floor, unit and representative example for flat, usage-based, tiered, custom and freemium models; never ship a naked 'contact "
 "us' (the one answer a model cannot pass on). Fix persistent wrong prices via cross-source parity (reconcile G2, Capterra, directories, old "
 "posts) and freshness (update price, schema and dateModified together). Ensure crawlers can read it: server-side HTML, robots.txt allows "
 "GPTBot/OAI-SearchBot/PerplexityBot, verify in view-source not the rendered DOM. Includes a 10-point checklist, answer-block and Offer-schema "
 "code, and how to measure whether engines quote your price correctly (named? number right? your URL cited?). On-page hygiene: gets an "
 "already-named brand quoted accurately; getting onto the shortlist is a separate off-site job.\n")
a4="- [AI Visibility Tools, Compared"
assert a4 in s; s=s.replace(a4, llm+a4,1); open("llms.txt","w",encoding="utf-8").write(s); print("llms ok")
print("done")
