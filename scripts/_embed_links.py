#!/usr/bin/env python3
"""SCRATCH: add 3 home embeds + inline tool links across the blog library. Do NOT commit."""
import os, re, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
UP="/sessions/optimistic-youthful-planck/mnt/uploads"
def esc(t): return H.escape(t,quote=False)

# ---------- 3 home embeds (extract card+js from original uploaded tools, patch to brand) ----------
def card_js(srcfile, body_sub=None, js_sub=None):
    s=open(os.path.join(UP,srcfile),encoding="utf-8").read()
    i=s.index('<section class="card"'); j=s.index('<section class="method"')
    card=s[i:j].rstrip()
    m=re.search(r'<script>(.*?)</script>\s*</body>', s, re.S); js=m.group(1).strip()
    def clean(x):
        return (x.replace("&mdash;",", ").replace("&ndash;","-").replace("&rsquo;","'").replace("&#x2019;","'")
                 .replace("&ldquo;",'"').replace("&rdquo;",'"').replace("\\u2014",", ").replace("\\u2013","-")
                 .replace("—",", ").replace("–","-").replace("’","'").replace("“",'"').replace("”",'"'))
    card=clean(card); js=clean(js)
    for a,b in (body_sub or []): card=card.replace(a,b)
    for a,b in (js_sub or []): js=js.replace(a,b)
    return card, js

EMBEDS3=[
 {"slug":"geo-readiness-scorecard","blog":"blogs/geo-foundation-audit.html","grid":"score",
  "src":"geo-readiness-scorecard.html",
  "body_sub":[('class="band" id="sBand"','class="scoreband" id="sBand"'),('<div class="grid">','<div class="grid score">')],
  "js_sub":[("'#E0694A'","'#BC3F1D'"),("'#F3B23E'","'#8A8278'"),("'#3FD17E'","'#3E9B6A'")],
  "eyebrow":"Free interactive tool","title":"Score your GEO readiness",
  "deck":"Rate your brand across the four levers that decide AI citation, crawlability, authority, Information Gain and structure, and get your gaps ranked."},
 {"slug":"content-mix-planner","blog":"blogs/topical-authority-cluster-ai-shortlists.html","grid":"mix",
  "src":"content-mix-planner.html",
  "body_sub":[('<div class="grid">','<div class="grid mix">')],
  "js_sub":[("'#FF6A2C'","'#BC3F1D'"),("'#5E8FF0'","'#8A8278'"),("'#F3B23E'","'#B4ADA2'"),("'#3FD17E'","'#D6D0C5'")],
  "eyebrow":"Free interactive tool","title":"Plan a citation-optimized content mix",
  "deck":"Turn your monthly content capacity into a flagship / derivative / product / news split built for AI citations."},
 {"slug":"zero-click-traffic-risk","blog":"blogs/geo-compounding-flywheel.html","grid":"zero",
  "src":"zero-click-traffic-risk.html",
  "body_sub":[('<div class="grid">','<div class="grid zero">'),('style="--c:var(--red)"','style="--c:var(--signal)"'),('style="--c:var(--amber);display:none"','style="--c:var(--mute);display:none"')],
  "eyebrow":"Free interactive tool","title":"Estimate your zero-click exposure",
  "deck":"See how much of your organic traffic is at risk as AI Overviews and AI Mode answer more queries without a click."},
]

def insert_embed(e):
    path=e["blog"]; h=open(path,encoding="utf-8").read()
    if 'id="'+ {"geo-readiness-scorecard":"sScore","content-mix-planner":"mTotal","zero-click-traffic-risk":"tClicks"}[e["slug"]] +'"' in h:
        return "already"
    if 'href="/assets/tools.css"' not in h:
        h=h.replace("</head>", '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>',1)
    card,js=card_js(e["src"], e["body_sub"], e.get("js_sub"))
    frag=('\n<section class="toolpage tool-embed">\n  <div class="embed-head">'
      f'<div class="embed-eyebrow">{esc(e["eyebrow"])}</div><div class="embed-title">{esc(e["title"])}</div>'
      f'<div class="embed-deck">{esc(e["deck"])}</div></div>\n'+card+
      f'\n  <div class="embed-foot">A free rawmktg tool. <a href="/tools/{e["slug"]}">Open the full tool &rarr;</a> &middot; <a href="/tools">see all tools</a></div>\n</section>\n<script>\n'+js+'\n</script>\n')
    placed=None
    for a in ['<div class="faq-section"','<div class="about-block"']:
        idx=h.find(a)
        if idx!=-1: h=h[:idx]+frag+"\n"+h[idx:]; placed=a; break
    if not placed:
        idx=h.find("</main>"); h=h[:idx]+frag+"\n"+h[idx:]; placed="</main>"
    open(path,"w",encoding="utf-8").write(h); return placed

# ---------- inline tool links across the library ----------
LINKS={
 "blogs/aec-ai-visibility-gap.html":[("page-citability-analyzer",["AI citations","get cited","cited"]),("geo-readiness-scorecard",["visibility gap","audit"])],
 "blogs/hr-saas-ai-visibility-gap.html":[("saas-funnel-gap-analyzer",["funnel","BOFU"]),("page-citability-analyzer",["AI citations","cited"])],
 "blogs/india-senior-living-ai-visibility-gap.html":[("page-citability-analyzer",["AI citations","cited"]),("geo-readiness-scorecard",["audit","visibility"])],
 "blogs/autonomous-retail-ai-visibility-gap.html":[("page-citability-analyzer",["AI citations","cited"]),("geo-readiness-scorecard",["audit","visibility"])],
 "blogs/container-tracking-saas-seo-geo-analysis.html":[("saas-funnel-gap-analyzer",["funnel","informational"]),("geo-readiness-scorecard",["audit","visibility"])],
 "blogs/cross-border-backlinks.html":[("geo-lift-calculator",["authority","backlink"]),("page-citability-analyzer",["cited","citations"])],
 "blogs/cx-saas-seo-discoverability-analysis.html":[("geo-readiness-scorecard",["audit","visibility"]),("zero-click-traffic-risk",["zero-click","AI Overviews"])],
 "blogs/noterro-ai-search-teardown.html":[("page-citability-analyzer",["cited","citation"]),("geo-readiness-scorecard",["fundamentals","audit"])],
 "blogs/property-vista-authority-paradox.html":[("geo-readiness-scorecard",["crawlability","audit"]),("page-citability-analyzer",["cited","citation"])],
 "blogs/how-rag-actually-works.html":[("page-citability-analyzer",["Information Gain","cited","chunk"])],
 "blogs/geo-foundation-audit.html":[("page-citability-analyzer",["Information Gain","cited"]),("content-recency-decay",["recency","freshness"])],
 "blogs/geo-compounding-flywheel.html":[("content-recency-decay",["recency","freshness"]),("geo-lift-calculator",["Share of Model","citation"])],
 "blogs/why-engines-recommend-different-vendors.html":[("ai-platform-optimizer",["each engine","different engines","Perplexity"]),("page-citability-analyzer",["cited","citation"])],
 "blogs/how-ai-crawlers-index-your-site.html":[("geo-readiness-scorecard",["crawlability","crawl"]),("ai-platform-optimizer",["each engine","crawler"])],
 "blogs/schema-markup-ai-citations-2026.html":[("page-citability-analyzer",["cited","citation"]),("ai-platform-optimizer",["each engine","platform"])],
 "blogs/anatomy-of-a-high-citation-page.html":[("claim-anchoring-validator",["hallucination","claim"]),("geo-lift-calculator",["citation lift","Share of Model","statistics"])],
 "blogs/authority-seeding-ai-llm-trust.html":[("geo-lift-calculator",["authority","citation"]),("page-citability-analyzer",["cited","citation"])],
 "blogs/topical-authority-cluster-ai-shortlists.html":[("page-citability-analyzer",["Information Gain","cited"])],
 "blogs/hallucination-proofing-your-brand.html":[("page-citability-analyzer",["cited","citation"])],
 "blogs/30-day-content-half-life-recency-ai-ranking-signal.html":[("page-citability-analyzer",["cited","citation"])],
 "blogs/eeat-is-an-ai-signal-now.html":[("claim-anchoring-validator",["hallucination","verifiable","trust"]),("content-recency-decay",["recency","freshness"])],
 "blogs/prompt-to-citation-tracking.html":[("geo-lift-calculator",["Share of Model","citation"]),("zero-click-traffic-risk",["zero-click","AI Overviews"])],
 "blogs/rlhf-and-your-brand.html":[("page-citability-analyzer",["Information Gain","cited"]),("claim-anchoring-validator",["hallucination","verifiable"])],
}
LABEL={
 "page-citability-analyzer":"Page Citability Analyzer","content-recency-decay":"Content Recency Decay Estimator",
 "claim-anchoring-validator":"Claim-Anchoring Validator","ai-platform-optimizer":"AI Platform Optimization Matrix",
 "saas-funnel-gap-analyzer":"B2B SaaS Funnel Gap Analyzer","geo-readiness-scorecard":"GEO Readiness Scorecard",
 "geo-lift-calculator":"GEO Lift Calculator","zero-click-traffic-risk":"Zero-Click Traffic-at-Risk Estimator",
 "content-mix-planner":"GEO Content-Mix Planner",
}

def in_text(main, pos):
    lt=main.rfind('<',0,pos); gt=main.rfind('>',0,pos)
    return gt>=lt  # last char before pos is outside a tag

def add_link(path, slug, cands):
    h=open(path,encoding="utf-8").read()
    if f'href="/tools/{slug}"' in h: return "exists"
    ms=h.find('<main'); me=h.find('</main>')
    if ms<0 or me<0: return "nomain"
    pre,main,post=h[:ms],h[ms:me],h[me:]
    for ph in cands:
        for m in re.finditer(re.escape(ph), main, re.IGNORECASE):
            pos=m.start()
            if not in_text(main,pos): continue
            # skip if already inside an <a>
            before=main[max(0,pos-120):pos]
            if '<a ' in before and '</a>' not in before: continue
            seg=m.group(0)
            main=main[:pos]+f'<a href="/tools/{slug}" title="{esc(LABEL[slug])}">{seg}</a>'+main[m.end():]
            open(path,"w",encoding="utf-8").write(pre+main+post)
            return "ok:"+ph
    return "MISS"

print("=== EMBEDS ===")
for e in EMBEDS3:
    print(f"  {e['slug']:24} -> {e['blog'].split('/')[-1]:42} {insert_embed(e)}")

print("=== INLINE LINKS ===")
emb_slug={e["blog"]:e["slug"] for e in EMBEDS3}
emb_slug.update({"blogs/30-day-content-half-life-recency-ai-ranking-signal.html":"content-recency-decay",
 "blogs/anatomy-of-a-high-citation-page.html":"page-citability-analyzer",
 "blogs/hallucination-proofing-your-brand.html":"claim-anchoring-validator",
 "blogs/how-rag-actually-works.html":"ai-platform-optimizer",
 "blogs/cx-saas-seo-discoverability-analysis.html":"saas-funnel-gap-analyzer"})
misses=0
for path,links in LINKS.items():
    res=[]
    for slug,cands in links:
        if emb_slug.get(path)==slug: res.append(slug+":skip(embed)"); continue
        r=add_link(path,slug,cands); res.append(slug+":"+r)
        if r=="MISS": misses+=1
    print(f"  {path.split('/')[-1][:40]:40} "+" | ".join(res))
print("total MISSES:",misses)
