#!/usr/bin/env python3
"""SCRATCH: surface the-link-liability into research/topic/sitemap/feed/llms + inbound already wired."""
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="the-link-liability"; URL=f"https://rawmktg.com/blogs/{SLUG}"
TITLE="The Link Liability"
TOPIC="Content &amp; Authority &middot; Backlink research"
DESC_CARD="41 backlink audits across investing, wealth and digital assets, read as one dataset: only 3.7% of every link relationship ever formed still carries authority."
IMG="/assets/images/the-link-liability-card"
PUB="2026-08-27"

CARD=(f'      <a href="/blogs/{SLUG}" class="article-card">\n'
 f'        <img src="{IMG}.webp" srcset="{IMG}-400.webp 400w, {IMG}-700.webp 700w, {IMG}.webp 1000w" '
 f'sizes="(max-width:768px) calc(100vw - 40px), (max-width:1024px) 46vw, 340px" alt="{TITLE}: what 41 backlink audits reveal" class="card-img" loading="lazy" width="1000" height="525">\n'
 f'        <div class="card-body">\n'
 f'          <div class="card-topic">{TOPIC}</div>\n'
 f'          <div class="card-title">{TITLE}</div>\n'
 f'          <p class="card-desc">{DESC_CARD}</p>\n'
 f'          <div class="card-footer"><span class="card-arrow" aria-hidden="true">&rarr;</span></div>\n'
 f'        </div>\n      </a>\n')

# 1. research.html cluster 04, before mbl card (newest first)
s=open("research.html",encoding="utf-8").read()
assert SLUG not in s
anc='      <a href="/blogs/mentions-beat-links" class="article-card">'
assert s.count(anc)==1
s=s.replace(anc, CARD+anc,1); open("research.html","w",encoding="utf-8").write(s); print("research card ok")

# 2. content-authority topic page, before mbl card
s=open("topics/content-authority.html",encoding="utf-8").read()
assert SLUG not in s
assert s.count(anc)==1
s=s.replace(anc, CARD+anc,1); open("topics/content-authority.html","w",encoding="utf-8").write(s); print("topic card ok")

# 3. sitemap.xml before mbl
s=open("sitemap.xml",encoding="utf-8").read()
assert SLUG not in s
entry=(f'  <url>\n    <loc>{URL}</loc>\n    <lastmod>{PUB}</lastmod>\n'
       f'    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
anc2='  <url>\n    <loc>https://rawmktg.com/blogs/mentions-beat-links</loc>'
assert anc2 in s
s=s.replace(anc2, entry+anc2,1); open("sitemap.xml","w",encoding="utf-8").write(s); print("sitemap ok")

# 4. feed.xml newest item + build date
s=open("feed.xml",encoding="utf-8").read()
assert SLUG not in s
fdesc=("A backlink teardown of 41 funded companies in investing, wealth management and digital assets, audited on one day with one method "
 "against the same 40-company peer set and read as a single dataset. Headline: of 15,134 link relationships ever formed across the cohort, "
 "2,126 domains still link, 1,044 pass authority, and only 567 sit at DR 50+ -- 3.7% of everything ever earned, an 86% pooled decay rate. "
 "Findings: 58% of live referring domains sit at DR 29 or below and 36% below DR 10; Domain Rating correlates with live dofollow domains at "
 "r=0.45 (14.6-point residual) so it lags reality and is inflated by single sitewide footer links; median company has lost 74% of every "
 "domain that ever linked and nobody monitors it (13,037 lost relationships sit unworked); median homepage concentration is 100%, capping "
 "what content can rank; 49% of the 283 strongest placements are nofollow; 31% of flagged spam domains carry DR 30+ so a low-DR filter keeps "
 "a third of them; 803 identified link opportunities resolve to just 32 domains (0.69 average pairwise overlap), 62% directories and wire "
 "hosts. Introduces four replacement metrics -- Effective Authority Domains (median 8), Live Equity Ratio (median 13%), Link Liability Ratio "
 "(median 47%), Page Concentration (median 100%) -- with a nine-step remediation order, a triage pass, a 90-day sequence, and working pandas "
 "and disavow code. 13 original figures, 7 tables, 4 code blocks.")
item=(f'    <item>\n      <title><![CDATA[The Link Liability: What 41 Backlink Audits Reveal &middot; rawmktg.]]></title>\n'
 f'      <link>{URL}</link>\n      <guid isPermaLink="true">{URL}</guid>\n'
 f'      <pubDate>Thu, 27 Aug 2026 00:00:00 +0000</pubDate>\n'
 f'      <description><![CDATA[{fdesc}]]></description>\n    </item>\n')
anc3='    <item>\n      <title><![CDATA[Digital PR & Data Studies: The Link Play AI Cites'
assert anc3 in s
s=s.replace(anc3, item+anc3,1)
s=re.sub(r'<lastBuildDate>[^<]+</lastBuildDate>','<lastBuildDate>Thu, 27 Aug 2026 00:00:00 +0000</lastBuildDate>',s,1)
open("feed.xml","w",encoding="utf-8").write(s); print("feed ok")

# 5. llms.txt bullet before mbl
s=open("llms.txt",encoding="utf-8").read()
assert SLUG not in s
llm=("- [The Link Liability: What 41 Backlink Audits Reveal](https://rawmktg.com/blogs/the-link-liability) - August 2026. A backlink teardown "
 "of 41 funded companies in investing, wealth and digital assets, audited on one day with one method against the same 40-company peer set and "
 "read as one dataset (21,445 backlinks analysed). Headline collapse: of 15,134 domains that have ever linked to the cohort, 2,126 still link, "
 "1,044 pass authority, and only 567 sit at DR 50+ -- 3.7% of every relationship ever formed, an 86% pooled decay rate. Most dashboards report "
 "the first number and none report the last. Findings: 58% of live referring domains are DR 29 or below and 36% below DR 10 (scrapers, "
 "expired-domain networks, jobs aggregators, directories); Domain Rating correlates with live dofollow domains at Pearson r=0.45 with a "
 "14.6-point residual, so DR lags reality (crawled on a delay, decays slowly inside the score) and is inflated by a single sitewide footer "
 "link; the median company has lost 74% of every domain that ever linked and 32 of 40 have lost more than half, with 13,037 lost relationships "
 "sitting unworked while teams pay for new ones; median homepage concentration is 100% (20 of 37 companies), which caps what any non-homepage "
 "page can rank; 49% of the 283 strongest placements are nofollow (newswire, jobs boards, directories, big media default to it); the spam does "
 "not look like spam -- 31% of flagged domains carry DR 30+ and 7% clear DR 50, so a low-DR filter keeps a third, and much is inherited not "
 "bought; competitor gap analysis converges on commodity links -- 803 opportunities resolve to 32 domains (0.69 average pairwise Jaccard "
 "overlap), 62% directories and wire hosts, 40% free self-serve listings. Sub-segments differ: exchanges acquired reach and kept none (fix = "
 "recovery), digital-asset infra never acquired any (fix = acquisition). Replaces Domain Rating with four export-computable metrics: Effective "
 "Authority Domains (live dofollow at DR 50+, median 8), Live Equity Ratio (live dofollow / ever acquired, median 13%), Link Liability Ratio "
 "(nofollow-only + flagged / live, median 47%), Page Concentration (median 100%). Nine-step remediation in order (audit before you acquire, "
 "report EAD not DR, diff monthly, work recovery before acquisition, claim the free tier, stop counting nofollow as link building, give links "
 "a landing page other than the homepage, publish one unsubstitutable thing per quarter, re-run on a schedule), a keep/recover/disavow triage "
 "pass, a 90-day sequence, and working pandas and Google disavow code. 13 original figures, 7 tables, 4 code blocks.\n")
anc4="- [Digital PR and Data Studies: The Link Play AI Cites]"
assert anc4 in s
s=s.replace(anc4, llm+anc4,1); open("llms.txt","w",encoding="utf-8").write(s); print("llms.txt ok")
print("done insertions")
