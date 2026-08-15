#!/usr/bin/env python3
"""SCRATCH: embed the 2 comparison tools into the comparison-pages article as on-page assets."""
import re, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
ART="blogs/comparison-pages-ai-shortlists.html"
a=open(ART,encoding="utf-8").read()

def extract(toolfile,cid):
    h=open(toolfile,encoding="utf-8").read()
    body=re.search(r'<section class="card" id="'+cid+r'">.*?</section>', h, re.S).group(0)
    scripts=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', h, re.S) if "getElementById('"+cid+"')" in s]
    return body, scripts[-1]

cpe_body,cpe_script=extract("tools/comparison-page-extractability-scorer.html","cpe")
csg_body,csg_script=extract("tools/comparison-schema-generator.html","csg")

def embed(eyebrow,title,deck,body):
    return (f'<div class="toolpage tool-embed"><div class="embed-head"><div class="embed-eyebrow">{eyebrow}</div>'
            f'<div class="embed-title">{title}</div><div class="embed-deck">{deck}</div></div>{body}</div>\n')

E1=embed("Free Tool &middot; Diagnostic","Score your comparison page",
  "The four levers above, made live. Set answer position, fact density, heading match and neutrality to get a single extractability score, and the one lever to fix first.",cpe_body)
E2=embed("Free Tool &middot; Generator","Generate your comparison schema",
  "Turn the markup above into your own nested ItemList + SoftwareApplication JSON-LD. Enter two products, copy the block, and server-render it on your page.",csg_body)

assert a.count('<div class="toolpage tool-embed">')==0, "already embedded"
if 'assets/tools.css' not in a:
    a=a.replace('</head>\n<body>', '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>\n<body>',1)
# insert E1 before section 6 (schema), E2 before section 7 (rebuild)
a=a.replace('<h2 id="schema">', E1+'<h2 id="schema">',1)
a=a.replace('<h2 id="rebuild">', E2+'<h2 id="rebuild">',1)
# insert both tool scripts before the Chart.js block
a=a.replace('<!-- Chart.js -->', cpe_script+'\n'+csg_script+'\n<!-- Chart.js -->',1)

open(ART,"w",encoding="utf-8").write(a)
print("embeds:",a.count('tool-embed'),"| cpe:",a.count('id="cpe"'),"| csg:",a.count('id="csg"'),
      "| cpe script:",a.count("getElementById('cpe')"),"| csg script:",a.count("getElementById('csg')"))
