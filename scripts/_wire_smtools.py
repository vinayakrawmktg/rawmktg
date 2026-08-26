#!/usr/bin/env python3
"""SCRATCH: wire 3 sitemap tools into hub + sitemap.xml + llms.txt."""
import os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

TOOLS=[
 ("sitemap-discovery-yield-auditor","Free Tool &middot; Auditor","Sitemap Discovery-Yield Auditor",
  "Paste your hop-sweep results and see discovery yield, the share of declared URLs that return 200 and resolve inside the three-hop ceiling AI indexers enforce, with the worst offenders ranked.",
  "Paste your sitemap hop-sweep results and get discovery yield, the share of declared URLs a real-time AI indexer can resolve (200 and inside the three-hop ceiling), with a status/hop breakdown and the worst offenders ranked."),
 ("lastmod-timestamp-trust-calculator","Free Tool &middot; Calculator","lastmod Timestamp-Trust Calculator",
  "Enter how many URLs got a new lastmod versus how many actually changed, and see whether your sitemap timestamps are trusted. Below 0.2, publishing no lastmod scores better.",
  "Enter lastmod-changed versus content-changed URL counts to get a timestamp-trust score. Build-stamping every URL earns a recrawl demotion; below 0.2 an absent lastmod scores better than a false one."),
 ("indexnow-payload-builder","Free Tool &middot; Generator","IndexNow Payload Builder",
  "Enter your host, key and changed URLs to build a valid IndexNow submission, the JSON POST body, a single-URL GET, and a curl command, with host and key validation.",
  "Enter host, key and changed URLs to generate a validated IndexNow JSON POST body, a single-URL GET, and a curl command for your deploy hook. Flags a non-bare host and a malformed key before you submit."),
]

# 1. hub tiles  (append after the last existing tile, before grid close)
s=open("tools.html",encoding="utf-8").read()
assert "sitemap-discovery-yield-auditor" not in s
anchor='      <a class="tool-tile" href="/tools/page-citability-analyzer">'
assert anchor in s
tiles=""
for slug,cat,name,hubdesc,_ in TOOLS:
    tiles+=(f'      <a class="tool-tile" href="/tools/{slug}"><div class="tt-cat">{cat}</div>'
            f'<div class="tt-name">{name}</div><div class="tt-desc">{hubdesc}</div>'
            f'<div class="tt-go">Open tool &rarr;</div></a>\n')
s=s.replace(anchor, tiles+anchor, 1)
open("tools.html","w",encoding="utf-8").write(s)
print("hub tiles added:", s.count('class="tool-tile"'))

# 2. sitemap.xml  (insert 3 url blocks before the bot-fetch tool block)
s=open("sitemap.xml",encoding="utf-8").read()
assert "sitemap-discovery-yield-auditor" not in s
anc='  <url>\n    <loc>https://rawmktg.com/tools/bot-fetch-test-generator</loc>'
assert anc in s
blocks=""
for slug,_,_,_,_ in TOOLS:
    blocks+=(f'  <url>\n    <loc>https://rawmktg.com/tools/{slug}</loc>\n'
             f'    <lastmod>2026-08-26</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n')
s=s.replace(anc, blocks+anc, 1)
open("sitemap.xml","w",encoding="utf-8").write(s)
print("sitemap tool entries:", s.count("/tools/"))

# 3. llms.txt  (insert 3 bullets before the bot-fetch bullet)
s=open("llms.txt",encoding="utf-8").read()
assert "sitemap-discovery-yield-auditor" not in s
anc="- [Bot-Fetch Test Command Generator](https://rawmktg.com/tools/bot-fetch-test-generator)"
assert anc in s
bl=""
for slug,_,name,_,llmdesc in TOOLS:
    bl+=f"- [{name}](https://rawmktg.com/tools/{slug}) - {llmdesc}\n"
s=s.replace(anc, bl+anc, 1)
open("llms.txt","w",encoding="utf-8").write(s)
print("llms.txt tool bullets ok")
print("done")
