#!/usr/bin/env python3
"""One-off finalize pass for the homepage rework + category structure."""
import re, glob, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 1) Promote the approved preview to the live homepage
home = open("index.preview.html", encoding="utf-8").read()
open("index.html", "w", encoding="utf-8").write(home)
print("[1] index.html promoted from preview")

# 2) Generate 5 category pages from the homepage clusters
ARIA_TO_SLUG = {
    "Industry teardowns": "industry-teardowns",
    "How AI search works": "how-ai-search-works",
    "The technical layer": "technical-layer",
    "Content and authority architecture": "content-authority",
    "Ranking signals and measurement": "ranking-signals",
}
CAT_STYLE = open("preview-topic-teardowns.html", encoding="utf-8").read()
CAT_STYLE = re.search(r"<style>([\s\S]*?)</style>", CAT_STYLE).group(1)

NAV_MENU = """          <div class="nav-menu" role="menu">
            <a role="menuitem"{a1} href="/topics/industry-teardowns"><span class="nm-num">01</span>The industry teardowns</a>
            <a role="menuitem"{a2} href="/topics/how-ai-search-works"><span class="nm-num">02</span>How AI search actually works</a>
            <a role="menuitem"{a3} href="/topics/technical-layer"><span class="nm-num">03</span>The technical layer</a>
            <a role="menuitem"{a4} href="/topics/content-authority"><span class="nm-num">04</span>Content &amp; authority architecture</a>
            <a role="menuitem"{a5} href="/topics/ranking-signals"><span class="nm-num">05</span>Ranking signals &amp; measurement</a>
          </div>"""

def nav_menu_for(active_slug):
    keys = ["industry-teardowns","how-ai-search-works","technical-layer","content-authority","ranking-signals"]
    fmt = {f"a{i+1}": (' class="active"' if keys[i]==active_slug else '') for i in range(5)}
    return NAV_MENU.format(**fmt)

def strip_tags(s): return re.sub(r"<[^>]+>", "", s).strip()

# pull each cluster block from the homepage
clusters = re.findall(r'<section class="cluster"[^>]*aria-label="([^"]*)"[\s\S]*?</section>', home)
sections = re.split(r'(<section class="cluster")', home)
# simpler: iterate over each cluster section via finditer
cat_meta = []
for m in re.finditer(r'<section class="cluster"[^>]*aria-label="([^"]*)">([\s\S]*?)</section>', home):
    aria, inner = m.group(1), m.group(2)
    slug = ARIA_TO_SLUG.get(aria)
    if not slug: continue
    num = strip_tags(re.search(r'<div class="cluster-num">([\s\S]*?)</div>', inner).group(1))
    title = strip_tags(re.search(r'<h2 class="cluster-title">([\s\S]*?)</h2>', inner).group(1))
    frame = strip_tags(re.search(r'<p class="cluster-frame">([\s\S]*?)</p>', inner).group(1))
    grid = re.search(r'<div class="article-grid"[^>]*>([\s\S]*?)</div>\s*<div class="explore-more">', inner)
    grid_inner = grid.group(1)
    grid_inner = grid_inner.replace('src="assets/images/', 'src="/assets/images/')
    count = grid_inner.count('class="article-card"')
    topic_num = re.sub(r"\s*/.*$", "", num).strip()  # "01"
    cat_meta.append((slug, title, frame, count, topic_num, grid_inner))

os.makedirs("topics", exist_ok=True)
for slug, title, frame, count, topic_num, grid_inner in cat_meta:
    desc = frame.replace('"', "&quot;")
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="robots" content="index, follow" />
  <title>{title} · rawmktg.</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{desc}" />
  <meta name="author" content="Vinayak Ravi" />
  <link rel="canonical" href="https://rawmktg.com/topics/{slug}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://rawmktg.com/topics/{slug}" />
  <meta property="og:title" content="{title} · rawmktg." />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />
  <meta property="og:site_name" content="rawmktg." />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title} · rawmktg." />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />
  <script type="application/ld+json">
  {{ "@context":"https://schema.org","@type":"CollectionPage","name":"{title}","url":"https://rawmktg.com/topics/{slug}","description":"{desc}","isPartOf":{{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}},"author":{{"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com"}} }}
  </script>
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/favicon-180.png" />
  <link rel="alternate" type="application/rss+xml" title="rawmktg." href="https://rawmktg.com/feed.xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" /></noscript>
  <style>{CAT_STYLE}</style>
  <script>(function(){{var l=false;function load(){{if(l)return;l=true;var s=document.createElement('script');s.async=true;s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852';s.crossOrigin='anonymous';document.head.appendChild(s);}}var ev=['scroll','mousemove','touchstart','keydown','click'];ev.forEach(function(e){{window.addEventListener(e,load,{{passive:true,once:true}});}});setTimeout(load,3000);}})();</script>
</head>
<body>

<nav class="site-nav" aria-label="Site navigation">
  <div class="page">
    <div class="nav-row">
      <a href="/" class="rm-logo" aria-label="rawmktg home">raw<span class="mktg">mktg</span><span class="dot">.</span></a>
      <div class="nav-links">
        <div class="nav-dropdown">
          <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">Articles <span class="caret" aria-hidden="true">&#9662;</span></button>
{nav_menu_for(slug)}
        </div>
        <a href="/#about">About</a>
        <a href="/#newsletter" class="cta">Subscribe</a>
      </div>
    </div>
  </div>
</nav>

<header class="topic-hero">
  <div class="page">
    <div class="topic-crumb"><a href="/">rawmktg.</a> / Topics</div>
    <div class="topic-kicker">Topic {topic_num}</div>
    <h1 class="topic-title">{title}</h1>
    <p class="topic-frame">{frame}</p>
    <div class="topic-count">{count} {"article" if count==1 else "articles"}</div>
  </div>
</header>

<section class="listing" aria-label="Articles in this topic">
  <div class="page">
    <div class="article-grid" role="list">{grid_inner}</div>
  </div>
</section>

<footer class="site-foot" aria-label="Site footer">
  <div class="page">
    <div class="foot-row">
      <a href="/" style="font-family:'Geist',system-ui;font-weight:800;font-size:15px;letter-spacing:-0.04em;">raw<span style="color:var(--ink-2)">mktg</span><span style="color:var(--signal)">.</span></a>
      <div class="foot-links">
        <a href="/#about">About</a>
        <a href="mailto:vinayak@rawmktg.com">Contact</a>
        <a href="/llms.txt">llms.txt</a>
      </div>
      <span>&copy; 2026 rawmktg.</span>
    </div>
  </div>
</footer>

</body>
</html>
"""
    open(f"topics/{slug}.html", "w", encoding="utf-8").write(page)
print(f"[2] generated {len(cat_meta)} category pages:", ", ".join(s for s,*_ in cat_meta))

# 3) Em-dash scrub across articles + privacy + 404
DROP_DASH_FILES = glob.glob("blogs/*.html") + ["privacy.html", "404.html"]
def scrub(path):
    h = open(path, encoding="utf-8").read(); orig = h
    h = re.sub(r'(Fig\.?\s*\d+)\s*—\s*', r'\1: ', h)
    h = re.sub(r'(Table\s*\d+)\s*—\s*', r'\1: ', h)
    h = h.replace('.md — optimized for AI and LLM tools', '.md. Optimized for AI and LLM tools')
    h = re.sub(r'\s*—\s*', ', ', h)   # remaining prose em dashes -> comma
    if h != orig: open(path, "w", encoding="utf-8").write(h)
    return h.count("—")
left = sum(scrub(f) for f in DROP_DASH_FILES)
print(f"[3] em-dash scrub done across {len(DROP_DASH_FILES)} files; remaining em dashes: {left}")

# 4) Roll the nav dropdown across articles + privacy + 404
NAV_BLOCK = '''<div class="nav-links">
        <div class="nav-dropdown">
          <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">Articles <span class="caret" aria-hidden="true">&#9662;</span></button>
          <div class="nav-menu" role="menu">
            <a role="menuitem" href="/topics/industry-teardowns"><span class="nm-num">01</span>The industry teardowns</a>
            <a role="menuitem" href="/topics/how-ai-search-works"><span class="nm-num">02</span>How AI search actually works</a>
            <a role="menuitem" href="/topics/technical-layer"><span class="nm-num">03</span>The technical layer</a>
            <a role="menuitem" href="/topics/content-authority"><span class="nm-num">04</span>Content &amp; authority architecture</a>
            <a role="menuitem" href="/topics/ranking-signals"><span class="nm-num">05</span>Ranking signals &amp; measurement</a>
          </div>
        </div>
        <a href="/#about">About</a>
        <a href="/#newsletter" class="cta">Subscribe</a>
      </div>'''
DROPDOWN_CSS = '''
    .nav-links{align-items:center;}
    .nav-dropdown{position:relative;}
    .nav-trigger{font:inherit;color:var(--mute);background:none;border:0;cursor:pointer;letter-spacing:0.14em;text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;padding:0;transition:color 0.15s;}
    .nav-trigger:hover,.nav-dropdown:hover .nav-trigger,.nav-dropdown:focus-within .nav-trigger{color:var(--ink);}
    .nav-trigger .caret{font-size:9px;color:var(--faint);}
    .nav-menu{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%) translateY(-6px);background:var(--paper);border:1px solid var(--rule);border-radius:10px;box-shadow:0 10px 30px rgba(42,39,34,0.12);padding:8px;min-width:300px;opacity:0;visibility:hidden;transition:opacity 0.15s,transform 0.15s;z-index:200;}
    .nav-dropdown:hover .nav-menu,.nav-dropdown:focus-within .nav-menu{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0);}
    .nav-menu a{display:block;padding:10px 12px;border-radius:6px;font-family:var(--f-mono);font-size:10.5px;font-weight:500;letter-spacing:0.10em;text-transform:uppercase;color:var(--ink-2);transition:background 0.12s,color 0.12s;white-space:nowrap;}
    .nav-menu a:hover{background:var(--paper-2);color:var(--signal);}
    .nav-menu .nm-num{color:var(--faint);margin-right:8px;}
'''
nav_pat = re.compile(r'<div class="nav-links">\s*<a href="/#articles">Articles</a>\s*<a href="/#newsletter" class="cta">Subscribe</a>\s*</div>')
rolled = 0
for path in glob.glob("blogs/*.html") + ["privacy.html", "404.html"]:
    h = open(path, encoding="utf-8").read(); orig = h
    if "nav-dropdown" not in h:
        h = nav_pat.sub(NAV_BLOCK, h, count=1)
        if ".nav-dropdown" not in h:  # inject CSS once
            h = h.replace("</style>", DROPDOWN_CSS + "  </style>", 1)
    if h != orig: open(path, "w", encoding="utf-8").write(h); rolled += 1
print(f"[4] nav dropdown rolled into {rolled} pages")

# 5) Update generator hint() so future builds stay em-dash-free
g = open("scripts/generate_llm_md.py", encoding="utf-8").read()
g = g.replace("is available at https://rawmktg.com{mdurl} — optimized for AI and LLM tools.",
              "is available at https://rawmktg.com{mdurl}. Optimized for AI and LLM tools.")
open("scripts/generate_llm_md.py", "w", encoding="utf-8").write(g)
print("[5] generator hint updated")

# 6) Add category pages to sitemap.xml
sm = open("sitemap.xml", encoding="utf-8").read()
today = datetime.date.today().isoformat()
if "/topics/" not in sm:
    entries = ""
    for slug, *_ in cat_meta:
        entries += f"  <url>\n    <loc>https://rawmktg.com/topics/{slug}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>\n"
    sm = sm.replace("</urlset>", entries + "</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("[6] sitemap.xml: added 5 topic URLs")
else:
    print("[6] sitemap.xml already has /topics/")
print("FINALIZE COMPLETE")
