#!/usr/bin/env python3
"""SCRATCH: sync fixed tool embeds into articles + regenerate llms.txt Free Tools (fix 8)."""
import os, re, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

# ---------- sync embeds ----------
def sync(tool, art, cid):
    t=open("tools/"+tool+".html",encoding="utf-8").read()
    body=re.search(r'<section class="card" id="'+cid+r'">.*?</section>', t, re.S).group(0)
    scr=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', t, re.S) if "getElementById('"+cid+"')" in s][-1]
    a=open("blogs/"+art+".html",encoding="utf-8").read()
    a2=re.sub(r'<section class="card" id="'+cid+r'">.*?</section>', lambda m: body, a, count=1, flags=re.S)
    assert ('id="'+cid+'"') in a2, f"card section missing for {cid} in {art}"
    oldscr=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', a2, re.S) if "getElementById('"+cid+"')" in s][-1]
    a2=a2.replace(oldscr,scr,1)
    open("blogs/"+art+".html","w",encoding="utf-8").write(a2)
    # node-check embedded script
    open("/tmp/sy.js","w").write(scr[8:-9])
    r=subprocess.run(["node","--check","/tmp/sy.js"],capture_output=True,text=True)
    return "OK" if r.returncode==0 else "FAIL "+r.stderr[:200]

for tool,art,cid in [
  ("facet-coverage-auditor","query-fan-out-how-one-prompt-becomes-ten-searches","fca"),
  ("claim-anchoring-validator","hallucination-proofing-your-brand","caTool"),
  ("comparison-schema-generator","comparison-pages-ai-shortlists","csg"),
  ("ai-bot-log-analyzer","does-llms-txt-do-anything-yet","log"),
]:
    print(f"sync {cid:7} -> {art:52} {sync(tool,art,cid)}")

# ---------- llms.txt: append the 20 missing tools ----------
llms=open("llms.txt",encoding="utf-8").read()
listed=set(re.findall(r'rawmktg\.com/tools/([a-z0-9-]+)', llms))
allslugs=sorted(s.replace("tools/","").replace(".html","") for s in
                [os.path.basename(p) for p in __import__("glob").glob("tools/*.html")])
missing=[s for s in allslugs if s not in listed]
def meta(slug):
    h=open("tools/"+slug+".html",encoding="utf-8").read()
    name=(re.search(r'<h1 class="article-headline">([^<]+)</h1>',h) or [None,slug])[1]
    desc=(re.search(r'<meta name="description" content="([^"]+)"',h) or [None,''])[1]
    import html as H; return H.unescape(name), H.unescape(desc)
bullets=[]
for s in missing:
    nm,ds=meta(s)
    bullets.append(f"- [{nm}](https://rawmktg.com/tools/{s}) - {ds}")
block="\n".join(bullets)+"\n"
# insert before the heading that follows Free Tools
llms=re.sub(r'(## Free Tools\n(?:.*\n)*?)(\n## )', lambda m: m.group(1)+block+m.group(2), llms, count=1)
open("llms.txt","w",encoding="utf-8").write(llms)
listed2=set(re.findall(r'rawmktg\.com/tools/([a-z0-9-]+)', llms))
print("\nllms.txt tools listed now:", len(listed2), "of", len(allslugs), "| appended:", len(missing))
