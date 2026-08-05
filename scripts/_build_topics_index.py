#!/usr/bin/env python3
"""SCRATCH: build /topics landing page + nav link + sitemap + llms. Do NOT commit."""
import os, re, json, glob, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
def esc(t): return H.escape(t,quote=False)
def escq(t): return H.escape(t,quote=True)
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
ORG={"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
OG="https://rawmktg.com/assets/images/og-default.png"

T=open("blogs/property-vista-authority-paradox.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'

# nav with Tools + new "Browse all topics" item
NAV=sl('<nav class="site-nav"',"</nav>")
OLD_LAST='<a role="menuitem" href="/topics/ranking-signals"><span class="nm-num">05</span>Ranking signals &amp; measurement</a>'
NEW_LAST=OLD_LAST+'\n            <a role="menuitem" href="/topics"><span class="nm-num">&rarr;</span>Browse all topics</a>'

TOPICS=[
 ("industry-teardowns","The industry teardowns","Single-brand and vertical GEO teardowns showing exactly where AI-visibility gaps hide, and how to close them."),
 ("how-ai-search-works","How AI search actually works","The mechanics of AI search: retrieval, RAG, Share of Model, and how engines decide what to cite."),
 ("technical-layer","The technical layer","Crawlability, rendering, schema, and the technical plumbing AI engines need to read you."),
 ("content-authority","Content & authority architecture","Information Gain, topical authority, and the earned-media authority that wins AI citations."),
 ("ranking-signals","Ranking signals & measurement","Recency, E-E-A-T, preference training, and how to measure your brand's AI citations."),
]
def count(slug):
    f=f"topics/{slug}.html"
    return open(f).read().count('class="article-card"') if os.path.exists(f) else 0

tiles=""
for slug,title,desc in TOPICS:
    n=count(slug)
    tiles+=(f'<a class="tool-tile" href="/topics/{slug}">'
      f'<div class="tt-cat">{n} article'+('s' if n!=1 else '')+'</div>'
      f'<div class="tt-name">{esc(title)}</div>'
      f'<div class="tt-desc">{esc(desc)}</div>'
      f'<div class="tt-go">Browse topic &rarr;</div></a>\n      ')

URL="https://rawmktg.com/topics"
DESC="Browse rawmktg by topic: industry teardowns, how AI search works, the technical layer, content & authority, and ranking signals & measurement."
itemlist={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"https://rawmktg.com/topics/{s}","name":t} for i,(s,t,d) in enumerate(TOPICS)]}
coll={"@context":"https://schema.org","@type":"CollectionPage","name":"Topics","url":URL,"description":DESC,"isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
  {"@type":"ListItem","position":2,"name":"Topics","item":URL}]}
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
  "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
  "  <title>Topics &middot; rawmktg.</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
  f"  <meta name=\"description\" content=\"{escq(DESC)}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
  "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
  "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
  "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
  "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
  f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
  f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
  "  <meta property=\"og:type\" content=\"website\" />\n"
  f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"Topics\" />\n"
  f"  <meta property=\"og:description\" content=\"{escq(DESC)}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
  f'  <meta property="og:image" content="{OG}" />\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />\n'
  "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
  f"  <meta name=\"twitter:title\" content=\"Topics\" />\n  <meta name=\"twitter:description\" content=\"{escq(DESC)}\" />\n  <meta name=\"twitter:image\" content=\"{OG}\" />\n"
  f"  {jb(coll)}\n  {jb(itemlist)}\n  {jb(crumb)}\n  {jb({'@context':'https://schema.org',**ORG})}\n"
  "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n  "+FONTS+"\n  ")
nav=NAV.replace(OLD_LAST,NEW_LAST,1)
page=(head+STYLE+'\n  <link rel="stylesheet" href="/assets/tools.css" />\n  '+ADSENSE+
  "\n</head>\n<body>\n\n"+nav+"\n\n"
  '<div class="page">\n  <header class="article-header">\n    <div class="article-eyebrow"><span class="eyebrow-tag">Browse by topic</span><span class="eyebrow-sep">&middot;</span><span class="eyebrow-date">AI Search Intelligence</span></div>\n'
  '    <h1 class="article-headline">Topics</h1>\n    <p class="article-deck">Five tracks covering how AI search decides what to recommend, and how to get your brand cited. Start anywhere.</p>\n  </header>\n</div>\n\n'
  '<main class="toolpage" id="article-main">\n  <div class="page">\n    <div class="tools-grid">\n      '+tiles+'\n    </div>\n  </div>\n</main>\n\n'
  +NEWS+"\n\n"+FOOT+"\n</body>\n</html>\n")
open("topics.html","w",encoding="utf-8").write(page)
print("built topics.html | tiles:",page.count("tool-tile"),"| em:",page.count(chr(8212)))

# ---- nav site-wide: add 'Browse all topics' ----
n=0
for f in glob.glob("**/*.html",recursive=True):
    if "/.git/" in f: continue
    t=open(f,encoding="utf-8").read()
    if OLD_LAST in t and 'href="/topics">' not in t.split('nav-menu')[-1][:600] and '>Browse all topics<' not in t:
        t=t.replace(OLD_LAST,NEW_LAST,1)
        open(f,"w",encoding="utf-8").write(t); n+=1
print("nav 'Browse all topics' added to",n,"pages")

# ---- sitemap ----
s=open("sitemap.xml",encoding="utf-8").read()
if "<loc>https://rawmktg.com/topics</loc>" not in s:
    anchor=s.find("<loc>https://rawmktg.com/topics/")
    us=s.rfind("<url>",0,anchor)
    s=s[:us]+f"<url>\n    <loc>{URL}</loc>\n    <lastmod>2026-06-12</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>\n  "+s[us:]
    open("sitemap.xml","w",encoding="utf-8").write(s)
print("sitemap /topics:", "<loc>https://rawmktg.com/topics</loc>" in open("sitemap.xml").read())

# ---- llms ----
l=open("llms.txt",encoding="utf-8").read()
if "https://rawmktg.com/topics)" not in l:
    l=l.replace("## Topic Hubs\n","## Topic Hubs\n- [All topics](https://rawmktg.com/topics) - Browse every track: teardowns, how AI search works, technical layer, content & authority, ranking signals.\n",1)
    open("llms.txt","w",encoding="utf-8").write(l)
print("llms /topics:", "https://rawmktg.com/topics)" in open("llms.txt").read())
print("DONE")
