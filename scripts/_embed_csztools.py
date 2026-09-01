#!/usr/bin/env python3
"""SCRATCH: embed answer-block-optimizer + geo-readiness-scorecard into clean-site article; add inbound link."""
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
ART="blogs/clean-site-zero-citations.html"
a=open(ART,encoding="utf-8").read()

def extract(slug,inpid):
    t=open(f"tools/{slug}.html",encoding="utf-8").read()
    card=[c for c in re.findall(r'<section class="card">.*?</section>', t, re.S) if f'id="{inpid}"' in c][0]
    scr=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', t, re.S) if inpid in s][0]
    return card,scr

# ensure tools.css in head
if 'href="/assets/tools.css"' not in a:
    a=a.replace('</head>', '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>', 1)

EMB=[
 ("answer-block-optimizer","abIn","Free Tool &middot; Optimizer","Optimize your own answer block",
  "The decision-page pattern above, made live. Paste a draft answer and see whether a retriever can lift it cleanly, and what is dragging the score down.",
  '<a href="/blogs/anatomy-of-a-high-citation-page">the shape of a high-citation page</a>.</p>'),
 ("geo-readiness-scorecard","checklist","Free Tool &middot; Scorecard","Score your own GEO readiness",
  "Run the gate check before you publish. Tick what is true of your buyer-path pages and get a readiness score with the gaps that matter most.",
  '<a href="/blogs/prompt-to-citation-tracking">prompt-to-citation tracking stack</a>.</p>'),
]
scripts=[]
for slug,inpid,eyebrow,title,deck,anchor in EMB:
    assert f'id="{inpid}"' not in a, f"{slug} already embedded"
    card,scr=extract(slug,inpid)
    embed=('<div class="toolpage tool-embed"><div class="embed-head">'
      f'<div class="embed-eyebrow">{eyebrow}</div>'
      f'<div class="embed-title">{title}</div>'
      f'<div class="embed-deck">{deck}</div>'
      '</div>'+card+'</div>')
    assert anchor in a, f"anchor missing for {slug}"
    a=a.replace(anchor, anchor+'\n'+embed, 1)
    scripts.append(scr)

cj='\n<!-- Chart.js -->'
assert cj in a
a=a.replace(cj, '\n'+'\n'.join(scripts)+cj, 1)
open(ART,"w",encoding="utf-8").write(a)
print("embedded:", a.count('id="abIn"'), a.count('id="checklist"'), "| tools.css:", a.count('assets/tools.css'))

# stacked layout for embeds (article column is narrower than a full tool page)
STYLE_FIX='<style id="tool-embed-fix">.tool-embed .grid.mix,.tool-embed .grid.score{grid-template-columns:1fr;gap:22px;}.tool-embed .ta{min-height:150px;}</style>\n'
if 'id="tool-embed-fix"' not in a:
    firsthead=EMB[0][5]
    a=a.replace('<div class="toolpage tool-embed"><div class="embed-head"><div class="embed-eyebrow">Free Tool &middot; Optimizer', STYLE_FIX+'<div class="toolpage tool-embed"><div class="embed-head"><div class="embed-eyebrow">Free Tool &middot; Optimizer',1)
    open(ART,"w",encoding="utf-8").write(a)

# inbound link from winning-google-isnt-winning-ai
f="blogs/winning-google-isnt-winning-ai.html"; h=open(f,encoding="utf-8").read()
if "/blogs/clean-site-zero-citations" not in h:
    anchor="the links each player"
    i=h.find(anchor)
    if i<0:
        anchor="one-day snapshot"
        i=h.find(anchor)
    assert i>=0, "wg anchor missing"
    j=h.find("</p>", i)
    clause=" A companion teardown scores 41 investing and wealth brands and finds <a href=\"/blogs/clean-site-zero-citations\">the cleanest sites earning zero AI citations</a>."
    h=h[:j]+clause+h[j:]
    assert h.count("/blogs/clean-site-zero-citations")==1
    open(f,"w",encoding="utf-8").write(h); print("inbound -> winning-google-isnt-winning-ai")
else:
    print("winning-google already links")
