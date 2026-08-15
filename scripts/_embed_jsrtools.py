#!/usr/bin/env python3
"""SCRATCH: embed CVR checker + remediation advisor into the JS-rendering article."""
import re, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
ART="blogs/do-ai-crawlers-render-javascript.html"
a=open(ART,encoding="utf-8").read()

def extract(toolfile,cid):
    h=open(toolfile,encoding="utf-8").read()
    body=re.search(r'<section class="card" id="'+cid+r'">.*?</section>', h, re.S).group(0)
    scr=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', h, re.S) if "getElementById('"+cid+"')" in s][-1]
    return body, scr

cvr_body,cvr_script=extract("tools/content-visibility-ratio-checker.html","cvr")
rra_body,rra_script=extract("tools/rendering-remediation-advisor.html","rra")

def embed(eyebrow,title,deck,body):
    return (f'<div class="toolpage tool-embed"><div class="embed-head"><div class="embed-eyebrow">{eyebrow}</div>'
            f'<div class="embed-title">{title}</div><div class="embed-deck">{deck}</div></div>{body}</div>\n')

E_CVR=embed("Free Tool &middot; Analyzer","Score your Content Visibility Ratio",
  "The ratio above, made live. Paste the raw fetch and the rendered page and see how many words a non-rendering bot never sees.",cvr_body)
E_RRA=embed("Free Tool &middot; Advisor","Find your rendering fix",
  "Answer three questions and get the cheapest of the four fixes, SSR, SSG, ISR or edge prerendering, that fits your change frequency and codebase.",rra_body)

assert a.count('<div class="toolpage tool-embed">')==0, "already embedded"
if 'assets/tools.css' not in a:
    a=a.replace('</head>\n<body>', '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>\n<body>',1)
# CVR checker after the CVR-diff section (#diff) -> before #budget
a=a.replace('<h2 id="budget">', E_CVR+'<h2 id="budget">',1)
# remediation advisor after the four-fixes section (#fixes) -> before #prerender
a=a.replace('<h2 id="prerender">', E_RRA+'<h2 id="prerender">',1)
a=a.replace('<!-- Chart.js -->', cvr_script+'\n'+rra_script+'\n<!-- Chart.js -->',1)

open(ART,"w",encoding="utf-8").write(a)
print("embeds:",a.count('tool-embed'),"| cvr:",a.count('id="cvr"'),"| rra:",a.count('id="rra"'),
      "| tools.css:",a.count('assets/tools.css'),"| cvr-script:",a.count("getElementById('cvr')"),"| rra-script:",a.count("getElementById('rra')"))
