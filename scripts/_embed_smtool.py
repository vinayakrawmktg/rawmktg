#!/usr/bin/env python3
"""SCRATCH: embed the discovery-yield auditor into the sitemap article."""
import os, re
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
ART="blogs/xml-sitemaps-for-ai-discovery.html"
TOOL="tools/sitemap-discovery-yield-auditor.html"

a=open(ART,encoding="utf-8").read()
t=open(TOOL,encoding="utf-8").read()
assert 'id="sdy"' not in a, "already embedded"

# 1. extract the tool card section
card=re.search(r'<section class="card" id="sdy">.*?</section>', t, re.S).group(0)
# 2. extract the tool logic script (the IIFE for sdy)
scr=re.search(r'<script>\s*\(function\(\)\{\s*var root=document\.getElementById\(\x27sdy\x27\).*?\}\)\(\);\s*</script>', t, re.S).group(0)

# 3. ensure tools.css link in head
if 'href="/assets/tools.css"' not in a:
    a=a.replace('</head>', '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>', 1)

# 4. build embed block
embed=('<div class="toolpage tool-embed"><div class="embed-head">'
 '<div class="embed-eyebrow">Free Tool &middot; Auditor</div>'
 '<div class="embed-title">Score your own discovery yield</div>'
 '<div class="embed-deck">The formula above, made live. Run the hop-sweep against your sitemap, paste the output, and see how many declared URLs a real-time indexer can actually resolve.</div>'
 '</div>'+card+'</div>')

# 5. insert embed before section 03 (status codes)
anchor='<h2 id="status">'
assert anchor in a, "status anchor missing"
a=a.replace(anchor, embed+'\n'+anchor, 1)

# 6. insert script before Chart.js block
cj='\n<!-- Chart.js -->'
assert cj in a, "chart.js anchor missing"
a=a.replace(cj, '\n'+scr+cj, 1)

open(ART,"w",encoding="utf-8").write(a)
print("embedded. tools.css:",a.count('assets/tools.css'),"| sdy card:",a.count('id="sdy"'),"| sdy script:",a.count("getElementById('sdy')"))
