#!/usr/bin/env python3
"""SCRATCH: backend audit fixes. Do NOT commit."""
import os, re, json, glob, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
def esc(t): return H.escape(t,quote=True)
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
ORG={"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
WS={"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}

# production page set
prod=["index.html","about.html","contact.html","privacy.html","terms.html","tools.html"]
prod+=glob.glob("blogs/*.html")+glob.glob("glossary/*.html")+glob.glob("topics/*.html")+glob.glob("tools/*.html")
prod=[p for p in prod if os.path.exists(p)]

# ---------- 1. hreflang standardize ----------
hl_added=0
for f in prod:
    t=open(f,encoding="utf-8").read()
    if "hreflang" in t: continue
    m=re.search(r'(<link rel="canonical" href="([^"]+)" />)', t)
    if not m: continue
    url=m.group(2)
    block=(m.group(1)
      +f'\n  <link rel="alternate" hreflang="en-US" href="{url}" />'
      +f'\n  <link rel="alternate" hreflang="en" href="{url}" />'
      +f'\n  <link rel="alternate" hreflang="x-default" href="{url}" />')
    t=t.replace(m.group(1),block,1)
    open(f,"w",encoding="utf-8").write(t); hl_added+=1
print("hreflang added to",hl_added,"pages")

# ---------- 2. trust pages: OG + JSON-LD ----------
def field(t,pat):
    m=re.search(pat,t); return m.group(1) if m else ""
trust=["about.html","contact.html","privacy.html","terms.html"]
tr=0
for f in trust:
    t=open(f,encoding="utf-8").read()
    url=field(t,r'<link rel="canonical" href="([^"]+)" />')
    title=field(t,r'<title>(.*?)</title>').replace(" &middot; rawmktg.","").replace(" · rawmktg.","").strip()
    desc=field(t,r'name="description" content="([^"]*)"')
    if 'property="og:' not in t:
        og=('  <meta property="og:type" content="website" />\n'
            f'  <meta property="og:url" content="{esc(url)}" />\n'
            f'  <meta property="og:title" content="{esc(title)}" />\n'
            f'  <meta property="og:description" content="{esc(desc)}" />\n'
            '  <meta property="og:site_name" content="rawmktg." />\n'
            '  <meta name="twitter:card" content="summary_large_image" />\n'
            f'  <meta name="twitter:title" content="{esc(title)}" />\n'
            f'  <meta name="twitter:description" content="{esc(desc)}" />\n')
    else: og=""
    if "application/ld+json" not in t:
        webpage={"@context":"https://schema.org","@type":"WebPage","name":title,"url":url,"description":desc,"isPartOf":WS}
        crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
          {"@type":"ListItem","position":2,"name":title,"item":url}]}
        sd="  "+jb(webpage)+"\n  "+jb(crumb)+"\n  "+jb({"@context":"https://schema.org",**ORG})+"\n"
    else: sd=""
    if og or sd:
        t=t.replace("</head>", og+sd+"</head>",1)
        open(f,"w",encoding="utf-8").write(t); tr+=1
print("trust pages enriched:",tr)

# ---------- 3. topic pages: BreadcrumbList ----------
tp=0
for f in glob.glob("topics/*.html"):
    t=open(f,encoding="utf-8").read()
    if "BreadcrumbList" in t: continue
    url=field(t,r'<link rel="canonical" href="([^"]+)" />')
    title=field(t,r'<title>(.*?)</title>').replace(" &middot; rawmktg.","").replace(" · rawmktg.","").strip()
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
      {"@type":"ListItem","position":2,"name":title,"item":url}]}
    t=t.replace("</head>","  "+jb(crumb)+"\n</head>",1)
    open(f,"w",encoding="utf-8").write(t); tp+=1
print("topic pages breadcrumb added:",tp)

# ---------- 4. inbound blog interlinks ----------
def in_text(main,pos):
    lt=main.rfind('<',0,pos); gt=main.rfind('>',0,pos); return gt>=lt
def add_link(srcfile, target_slug, cands):
    path="blogs/"+srcfile+".html"
    if not os.path.exists(path): return "nosrc"
    h=open(path,encoding="utf-8").read()
    if f'href="/blogs/{target_slug}"' in h: return "exists"
    ms=h.find('<main'); me=h.find('</main>')
    if ms<0: return "nomain"
    pre,main,post=h[:ms],h[ms:me],h[me:]
    for ph in cands:
        for m in re.finditer(re.escape(ph),main):
            pos=m.start()
            if not in_text(main,pos): continue
            before=main[max(0,pos-120):pos]
            if '<a ' in before and '</a>' not in before: continue
            main=main[:pos]+f'<a href="/blogs/{target_slug}">{m.group(0)}</a>'+main[m.end():]
            open(path,"w",encoding="utf-8").write(pre+main+post)
            return "ok:"+srcfile+":"+ph
    return None
INBOUND={
 "rlhf-and-your-brand":[("eeat-is-an-ai-signal-now",["RLHF","reinforcement learning","preference"]),("how-rag-actually-works",["preference","reranker"])],
 "noterro-ai-search-teardown":[("schema-markup-ai-citations-2026",["structured data","FAQPage","WebApplication"]),("hr-saas-ai-visibility-gap",["practice management","SaaS"]),("anatomy-of-a-high-citation-page",["structured data"])],
 "property-vista-authority-paradox":[("how-ai-crawlers-index-your-site",["JavaScript","bot","challenge","render"]),("hr-saas-ai-visibility-gap",["authority"])],
 "cx-saas-seo-discoverability-analysis":[("container-tracking-saas-seo-geo-analysis",["funnel","BOFU","MOFU","SaaS"]),("hr-saas-ai-visibility-gap",["funnel","SaaS"])],
 "container-tracking-saas-seo-geo-analysis":[("cx-saas-seo-discoverability-analysis",["logistics","tracking","SaaS"]),("aec-ai-visibility-gap",["SaaS"])],
 "india-senior-living-ai-visibility-gap":[("autonomous-retail-ai-visibility-gap",["visibility gap","vertical","category"]),("aec-ai-visibility-gap",["visibility gap"])],
}
print("inbound interlinks:")
for target,sources in INBOUND.items():
    done=None
    for src,cands in sources:
        r=add_link(src,target,cands)
        if r and r.startswith("ok"): done=r; break
        if r=="exists": done="exists"; break
    print("  ->",target,":",done or "MISS")

# ---------- 5. robots.txt ----------
r=open("robots.txt",encoding="utf-8").read()
r=r.replace("User-agent: GPTBot\nDisallow: /","User-agent: GPTBot\nAllow: /")
r=r.replace("User-agent: CCBot\nDisallow: /","User-agent: CCBot\nAllow: /")
r=r.replace("ai-train=no","ai-train=yes")
open("robots.txt","w",encoding="utf-8").write(r)
print("robots.txt: GPTBot/CCBot allowed:", "GPTBot\nAllow" in r and "CCBot\nAllow" in r, "| ai-train=yes:", "ai-train=yes" in r)

# ---------- 6. llms.txt topic hubs ----------
l=open("llms.txt",encoding="utf-8").read()
if "## Topic Hubs" not in l:
    sec=("## Topic Hubs\n"
     "- [The industry teardowns](https://rawmktg.com/topics/industry-teardowns) - Single-brand and vertical GEO teardowns showing where AI-visibility gaps are.\n"
     "- [How AI search actually works](https://rawmktg.com/topics/how-ai-search-works) - The mechanics of retrieval, RAG, and how engines choose what to cite.\n"
     "- [The technical layer](https://rawmktg.com/topics/technical-layer) - Crawlability, rendering, schema and the plumbing AI engines need.\n"
     "- [Content & authority architecture](https://rawmktg.com/topics/content-authority) - Information Gain, topical authority, and earned-media authority for citations.\n"
     "- [Ranking signals & measurement](https://rawmktg.com/topics/ranking-signals) - Recency, E-E-A-T, Share of Model and measuring AI citations.\n\n")
    idx=l.find("## Pages")
    l=l[:idx]+sec+l[idx:] if idx!=-1 else l+"\n"+sec
    open("llms.txt","w",encoding="utf-8").write(l)
print("llms.txt topic hubs added:", "## Topic Hubs" in open('llms.txt').read())
print("DONE")
