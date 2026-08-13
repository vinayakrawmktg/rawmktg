#!/usr/bin/env python3
"""SCRATCH: build /tools hub + per-tool pages in rawmktg brand. Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
UP="/sessions/optimistic-youthful-planck/mnt/uploads"
os.makedirs("tools", exist_ok=True)

def clean(s):
    return (s.replace("&mdash;",", ").replace("&ndash;","-")
             .replace("&rsquo;","'").replace("&lsquo;","'").replace("&#x2019;","'")
             .replace("&ldquo;",'"').replace("&rdquo;",'"').replace("&#x201c;",'"').replace("&#x201d;",'"')
             .replace("\\u2014",", ").replace("\\u2013","-")
             .replace("—",", ").replace("–","-").replace("’","'").replace("‘","'")
             .replace("“",'"').replace("”",'"'))
def esc(t): return H.escape(t,quote=False)
def escq(t): return H.escape(t,quote=True)

# ---- scaffold ----
T=open("blogs/property-vista-authority-paradox.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE=''  # AdSense removed: no ad units, hurts TBT
# add Tools link to nav (between Glossary and About)
NAV=NAV.replace('<a href="/glossary">Glossary</a>','<a href="/glossary">Glossary</a>\n        <a href="/tools">Tools</a>',1)

def extract(srcfile):
    s=open(os.path.join(UP,srcfile),encoding="utf-8").read()
    i=s.index('<section class="card"')
    j=s.index('</main>',i)
    body=s[i:j].strip()
    m=re.search(r'<script>(.*?)</script>\s*</body>', s, re.S)
    js=m.group(1).strip()
    return body, js

def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'

ORG={"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}

def build_tool(t):
    body, js = extract(t["src"])
    body=clean(body); js=clean(js)
    # grid modifier
    body=body.replace('<div class="grid">', f'<div class="grid {t["grid"]}">',1)
    # per-tool patches
    for a,b in t.get("body_sub",[]): body=body.replace(a,b)
    for a,b in t.get("js_sub",[]): js=js.replace(a,b)
    URL=f"https://rawmktg.com/tools/{t['slug']}"
    desc=clean(t["desc"]); deck=clean(t["deck"]); title=t["title"]
    webapp={"@context":"https://schema.org","@type":"WebApplication","name":title,"url":URL,
      "description":desc,"applicationCategory":t["appcat"],"operatingSystem":"Web, all browsers",
      "browserRequirements":"Requires JavaScript","isAccessibleForFree":True,
      "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
      "publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"}}
    webpage={"@context":"https://schema.org","@type":"WebPage","name":title,"url":URL,"description":desc,
      "isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
      {"@type":"ListItem","position":2,"name":"Tools","item":"https://rawmktg.com/tools"},
      {"@type":"ListItem","position":3,"name":title,"item":URL}]}
    orgld={"@context":"https://schema.org",**ORG}
    TITLE=f"{esc(title)} &middot; Free GEO Tool &middot; rawmktg."
    head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
      "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n"
      "  <meta name=\"robots\" content=\"index, follow\" />\n"
      f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
      f"  <meta name=\"description\" content=\"{escq(desc)}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
      "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
      "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
      "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
      "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
      f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
      "  <meta property=\"og:type\" content=\"website\" />\n"
      f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{escq(title)}\" />\n"
      f"  <meta property=\"og:description\" content=\"{escq(desc)}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
      "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
      f"  <meta name=\"twitter:title\" content=\"{escq(title)}\" />\n  <meta name=\"twitter:description\" content=\"{escq(desc)}\" />\n"
      f"  {jb(webapp)}\n  {jb(webpage)}\n  {jb(crumb)}\n  {jb(orgld)}\n"
      "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n  "
      +FONTS+"\n  ")
    header=('<div class="page">\n  <header class="article-header">\n    <div class="article-eyebrow">'
      f'<span class="eyebrow-tag">{esc(t["cat"])}</span>'
      '<span class="eyebrow-sep">&middot;</span><span class="eyebrow-date">Updated June 2026</span></div>\n'
      f'    <h1 class="article-headline">{esc(title)}</h1>\n    <p class="article-deck">{esc(deck)}</p>\n  </header>\n</div>\n')
    out=(head+STYLE+'\n  <link rel="stylesheet" href="/assets/tools.css" />\n  '+ADSENSE+
      "\n</head>\n<body>\n\n"+NAV+"\n\n"+header+
      '\n<main class="toolpage" id="article-main">\n  <div class="page">\n'+body+'\n  </div>\n</main>\n\n'
      +NEWS+"\n\n"+FOOT+"\n\n<script>\n"+js+"\n</script>\n</body>\n</html>\n")
    open(f"tools/{t['slug']}.html","w",encoding="utf-8").write(out)
    em=out.count(chr(8212))+out.count("&mdash;")
    return em

TOOLS=[
 {"slug":"geo-readiness-scorecard","src":"geo-readiness-scorecard.html","title":"GEO Readiness Scorecard",
  "cat":"Free Tool · Diagnostic","grid":"score","appcat":"BusinessApplication",
  "deck":"Rate your brand across the four things that decide whether AI engines cite you - crawlability, authority, Information Gain, and structure - and get your biggest gaps, ranked.",
  "desc":"Score your brand's readiness to be cited by AI engines across crawlability, authority, Information Gain, and structure, with your top gaps ranked.",
  "body_sub":[('class="band" id="sBand"','class="scoreband" id="sBand"')],
  "js_sub":[("'#E0694A'","'#BC3F1D'"),("'#F3B23E'","'#8A8278'"),("'#3FD17E'","'#3E9B6A'")]},
 {"slug":"content-mix-planner","src":"content-mix-planner.html","title":"GEO Content-Mix Planner",
  "cat":"Free Tool · Planner","grid":"mix","appcat":"BusinessApplication",
  "deck":"Most content programs over-produce derivative posts and under-produce the original research AI engines actually cite. Set your monthly capacity and get a citation-optimized split.",
  "desc":"Turn your monthly content capacity into a citation-optimized mix: flagship research, derivative, product, and news.",
  "js_sub":[("'#FF6A2C'","'#BC3F1D'"),("'#5E8FF0'","'#8A8278'"),("'#F3B23E'","'#B4ADA2'"),("'#3FD17E'","'#D6D0C5'")]},
 {"slug":"zero-click-traffic-risk","src":"zero-click-traffic-risk.html","title":"Zero-Click Traffic-at-Risk Estimator",
  "cat":"Free Tool · Estimator","grid":"zero","appcat":"BusinessApplication",
  "deck":"As AI Overviews and AI Mode expand, more searches resolve without a click. Estimate how much of your organic traffic sits in the blast radius, and what survives.",
  "desc":"Estimate how much of your organic traffic is exposed to zero-click erosion as AI Overviews and AI Mode expand.",
  "body_sub":[('style="--c:var(--red)"','style="--c:var(--signal)"'),('style="--c:var(--amber);display:none"','style="--c:var(--mute);display:none"')]},
 {"slug":"geo-lift-calculator","src":"geo-lift-calculator.html","title":"GEO Lift Calculator",
  "cat":"Free Tool · Calculator","grid":"calc","appcat":"BusinessApplication",
  "deck":"Model the AI citation lift on your brand's Share of Model. Toggle the signals from the Princeton/KDD GEO research and see the modeled outcome, with diminishing returns applied.",
  "desc":"Model the AI citation lift on your brand's Share of Model using the Princeton/KDD GEO coefficients.",},
]

for t in TOOLS:
    em=build_tool(t)
    print(f"  built tools/{t['slug']}.html | em-dashes:{em}")

# ---- hub ----
HUBURL="https://rawmktg.com/tools"
tiles=""
for t in TOOLS:
    tiles+=(f'<a class="tool-tile" href="/tools/{t["slug"]}">'
      f'<div class="tt-cat">{esc(t["cat"])}</div>'
      f'<div class="tt-name">{esc(t["title"])}</div>'
      f'<div class="tt-desc">{esc(clean(t["desc"]))}</div>'
      f'<div class="tt-go">Open tool &rarr;</div></a>\n      ')
itemlist={"@context":"https://schema.org","@type":"ItemList","itemListElement":[
  {"@type":"ListItem","position":i+1,"url":f"https://rawmktg.com/tools/{t['slug']}","name":t["title"]} for i,t in enumerate(TOOLS)]}
coll={"@context":"https://schema.org","@type":"CollectionPage","name":"Free GEO & AI-search tools","url":HUBURL,
  "description":"Free interactive tools to measure and improve your brand's visibility in AI search.",
  "isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
crumbH={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
  {"@type":"ListItem","position":2,"name":"Tools","item":HUBURL}]}
HDESC="Free interactive tools to measure and improve your brand's visibility in AI search: GEO readiness, content mix, zero-click risk, and citation lift."
hubhead=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
  "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n"
  "  <meta name=\"robots\" content=\"index, follow\" />\n"
  "  <title>Free GEO &amp; AI-Search Tools &middot; rawmktg.</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
  f"  <meta name=\"description\" content=\"{escq(HDESC)}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
  "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
  "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
  "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
  "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
  f"  <link rel=\"canonical\" href=\"{HUBURL}\" />\n"
  "  <meta property=\"og:type\" content=\"website\" />\n"
  f"  <meta property=\"og:url\" content=\"{HUBURL}\" />\n  <meta property=\"og:title\" content=\"Free GEO &amp; AI-Search Tools\" />\n"
  f"  <meta property=\"og:description\" content=\"{escq(HDESC)}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
  f"  {jb(coll)}\n  {jb(itemlist)}\n  {jb(crumbH)}\n  {jb({'@context':'https://schema.org',**ORG})}\n"
  "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n  "+FONTS+"\n  ")
hub=(hubhead+STYLE+'\n  <link rel="stylesheet" href="/assets/tools.css" />\n  '+ADSENSE+
  "\n</head>\n<body>\n\n"+NAV+"\n\n"
  '<div class="page">\n  <header class="article-header">\n    <div class="article-eyebrow">'
  '<span class="eyebrow-tag">Free Tools</span><span class="eyebrow-sep">&middot;</span>'
  '<span class="eyebrow-date">AI Search Intelligence</span></div>\n'
  '    <h1 class="article-headline">GEO &amp; AI-search tools</h1>\n'
  '    <p class="article-deck">Free, no-signup tools to measure and improve how often AI engines cite your brand. Built on the same research behind our teardowns.</p>\n  </header>\n</div>\n\n'
  '<main class="toolpage" id="article-main">\n  <div class="page">\n    <div class="tools-grid">\n      '+tiles+'\n    </div>\n  </div>\n</main>\n\n'
  +NEWS+"\n\n"+FOOT+"\n</body>\n</html>\n")
open("tools.html","w",encoding="utf-8").write(hub)
print("  built tools.html (hub) | tiles:",hub.count("tool-tile")-( hub.count('.tool-tile')))
print("done. tools:",len(TOOLS))
