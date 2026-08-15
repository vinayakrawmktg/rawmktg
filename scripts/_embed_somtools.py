#!/usr/bin/env python3
"""SCRATCH: embed the SoM (updated PWV) + Sample-Size planner into the Share of Model article."""
import re, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
ART="blogs/share-of-model-measurement.html"
a=open(ART,encoding="utf-8").read()

def extract(toolfile,cid):
    h=open(toolfile,encoding="utf-8").read()
    body=re.search(r'<section class="card" id="'+cid+r'">.*?</section>', h, re.S).group(0)
    scr=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', h, re.S) if "getElementById('"+cid+"')" in s][-1]
    return body, scr

pv_body,pv_script=extract("tools/platform-weighted-visibility-calculator.html","pv")
ssc_body,ssc_script=extract("tools/sample-size-confidence-planner.html","ssc")

def embed(eyebrow,title,deck,body):
    return (f'<div class="toolpage tool-embed"><div class="embed-head"><div class="embed-eyebrow">{eyebrow}</div>'
            f'<div class="embed-title">{title}</div><div class="embed-deck">{deck}</div></div>{body}</div>\n')

E_PV=embed("Free Tool &middot; Calculator","Compute your Share of Model",
  "The weighted formula above, made live. Enter per-engine mention and prompt counts for a visibility score, then add field mentions to get your Share of Model, your share of the whole competitive field.",pv_body)
E_SSC=embed("Free Tool &middot; Calculator","Plan your sample size",
  "How many runs and prompts you need for a number you can trust, plus a Wilson confidence interval for a rate you have already measured.",ssc_body)

assert a.count('<div class="toolpage tool-embed">')==0, "already embedded"
if 'assets/tools.css' not in a:
    a=a.replace('</head>\n<body>', '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>\n<body>',1)
a=a.replace('<h2 id="scoring">', E_PV+'<h2 id="scoring">',1)
a=a.replace('<h2 id="engines">', E_SSC+'<h2 id="engines">',1)
a=a.replace('<!-- Chart.js -->', pv_script+'\n'+ssc_script+'\n<!-- Chart.js -->',1)

open(ART,"w",encoding="utf-8").write(a)
print("embeds:",a.count('tool-embed'),"| pv:",a.count('id="pv"'),"| ssc:",a.count('id="ssc"'),
      "| tools.css:",a.count('assets/tools.css'),"| pv-script:",a.count("getElementById('pv')"),"| ssc-script:",a.count("getElementById('ssc')"))
