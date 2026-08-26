#!/usr/bin/env python3
"""SCRATCH: wire 2 PR tools into hub(top)+sitemap+llms; embed CSD into article."""
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

TOOLS=[
 ("citable-stat-density-scorer","Free Tool &middot; Analyzer","Citable Stat Density Scorer",
  "Paste a research draft and score each claim as citable, weak or rewrite, then get the citable stat density per 1,000 words a research hub needs to be lifted by AI.",
  "Paste a research draft to score every claim on precise number, named method and attribution (CITABLE/WEAK/REWRITE) and get citable stat density per 1,000 words. A research hub should clear 4."),
 ("dark-ai-revenue-estimator","Free Tool &middot; Estimator","Dark AI Revenue Estimator",
  "About 70.6% of AI referrals hide in GA4 Direct with the referrer stripped, converting at 4x baseline. Enter three numbers to back out the sessions and revenue.",
  "Enter monthly Direct sessions, Direct conversions and ACV to back out the dark-AI sessions hiding in Direct (70.6% referrer-stripped, ~10.21% conversion vs 2.46% baseline) and the hidden monthly revenue. A directional model."),
]

# 1. hub: prepend both tiles at the top of the grid (newest first)
s=open("tools.html",encoding="utf-8").read()
for slug,_,_,_,_ in TOOLS: assert slug not in s, f"{slug} already in hub"
open_tag='<div class="tools-grid">\n'
assert open_tag in s
tiles=""
for slug,cat,name,hubdesc,_ in TOOLS:
    tiles+=(f'      <a class="tool-tile" href="/tools/{slug}"><div class="tt-cat">{cat}</div>'
            f'<div class="tt-name">{name}</div><div class="tt-desc">{hubdesc}</div>'
            f'<div class="tt-go">Open tool &rarr;</div></a>\n')
s=s.replace(open_tag, open_tag+tiles, 1)
open("tools.html","w",encoding="utf-8").write(s)
print("hub tiles:", s.count('class="tool-tile"'))

# 2. sitemap.xml
s=open("sitemap.xml",encoding="utf-8").read()
anc='  <url>\n    <loc>https://rawmktg.com/tools/sitemap-discovery-yield-auditor</loc>'
assert anc in s
blocks=""
for slug,_,_,_,_ in TOOLS:
    blocks+=(f'  <url>\n    <loc>https://rawmktg.com/tools/{slug}</loc>\n'
             f'    <lastmod>2026-08-26</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n')
s=s.replace(anc, blocks+anc, 1); open("sitemap.xml","w",encoding="utf-8").write(s); print("sitemap ok")

# 3. llms.txt
s=open("llms.txt",encoding="utf-8").read()
anc="- [Sitemap Discovery-Yield Auditor](https://rawmktg.com/tools/sitemap-discovery-yield-auditor)"
assert anc in s
bl=""
for slug,_,name,_,llmdesc in TOOLS:
    nm=name.replace("&middot;","-")
    bl+=f"- [{nm}](https://rawmktg.com/tools/{slug}) - {llmdesc}\n"
s=s.replace(anc, bl+anc, 1); open("llms.txt","w",encoding="utf-8").write(s); print("llms ok")

# 4. embed CSD scorer into the article
ART="blogs/mentions-beat-links.html"
a=open(ART,encoding="utf-8").read()
t=open("tools/citable-stat-density-scorer.html",encoding="utf-8").read()
assert 'id="csd"' not in a
card=re.search(r'<section class="card" id="csd">.*?</section>', t, re.S).group(0)
scr=re.search(r'<script>\s*\(function\(\)\{\s*var root=document\.getElementById\(\x27csd\x27\).*?\}\)\(\);\s*</script>', t, re.S).group(0)
if 'href="/assets/tools.css"' not in a:
    a=a.replace('</head>', '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>', 1)
embed=('<div class="toolpage tool-embed"><div class="embed-head">'
 '<div class="embed-eyebrow">Free Tool &middot; Analyzer</div>'
 '<div class="embed-title">Score your own citable stat density</div>'
 '<div class="embed-deck">The formula above, made live. Paste your draft and see which claims a model can lift and which will not survive extraction.</div>'
 '</div>'+card+'</div>')
anchor='<h3>Design backward from the headline</h3>'
assert anchor in a, "embed anchor missing"
a=a.replace(anchor, embed+'\n'+anchor, 1)
cj='\n<!-- Chart.js -->'
assert cj in a
a=a.replace(cj, '\n'+scr+cj, 1)
open(ART,"w",encoding="utf-8").write(a)
print("embedded CSD:", a.count('id="csd"'), "| tools.css:", a.count('assets/tools.css'))
print("done")
