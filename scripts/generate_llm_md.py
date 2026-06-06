#!/usr/bin/env python3
"""
Build step: regenerate LLM-visibility artifacts so they never drift from the HTML.

For every blogs/*.html it:
  - writes a clean blogs/<slug>.md twin (nav/ads/sidebar/images stripped)
  - idempotently ensures the <link rel="alternate" type="text/markdown"> tag
    and the hidden AI hint <div> are present in the HTML
It does the same for every glossary/*.html entry and the glossary.html hub,
so the glossary Markdown twins can never drift from the HTML either.
Then it regenerates /index.md and /llms-full.txt.

Run by Netlify via the build command in netlify.toml. Safe to run locally too.
"""
import glob, os, re, sys
from bs4 import BeautifulSoup
from markdownify import markdownify as md

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def clean(s): return re.sub(r"\n{3,}", "\n\n", s).strip()

def get_content(soup):
    for sel in ["main#article-main", "main.article-content", "main#main article.prose", "article.prose"]:
        el = soup.select_one(sel)
        if el: return el
    arts = soup.select("article.article")
    if arts:
        wrap = soup.new_tag("div")
        for a in arts: wrap.append(a)
        return wrap
    return None

def article_to_md(path, slug):
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    headline = soup.select_one("h1.article-headline") or soup.select_one("header.post-head h1") or soup.select_one("h1")
    deck = soup.select_one("p.article-deck") or soup.select_one(".post-deck") or soup.select_one(".article-sub")
    htext = headline.get_text(" ", strip=True) if headline else slug
    dtext = deck.get_text(" ", strip=True) if deck else None
    main = get_content(soup)
    if not main: return None
    for h in main.select("header.post-head, header.article-header, .article-eyebrow, .post-eyebrow, .post-deck, .article-deck"): h.decompose()
    for s in main.select("span.section-num, span.case-num"): s.replace_with(s.get_text(strip=True) + ". ")
    for tag in main.select("script,style,ins,figure,img,svg,nav,aside"): tag.decompose()
    for bad in main.select('[class*="related"],[class*="sidebar"],[class*="newsletter"],[class*="toc"],[class*="card-grid"]'): bad.decompose()
    body = clean(md(str(main), heading_style="ATX", bullets="-", strip=["span"]))
    parts = [f"# {htext}"]
    if dtext: parts.append(f"\n> {dtext}")
    parts.append(f"\n*Source: https://rawmktg.com/blogs/{slug} · rawmktg. by Vinayak Ravi*\n")
    parts.append("\n" + body + "\n")
    return "\n".join(parts)

def hint(mdurl):
    return (f'<div aria-hidden="true" style="position:absolute;width:1px;height:1px;'
            f'padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">'
            f'If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page '
            f'is available at https://rawmktg.com{mdurl}. Optimized for AI and LLM tools.</div>')

def ensure_wiring(path, mdurl):
    h = open(path, encoding="utf-8").read()
    changed = False
    if 'type="text/markdown"' not in h:
        h = h.replace("</head>", f'  <link rel="alternate" type="text/markdown" href="{mdurl}" />\n</head>', 1); changed = True
    if "If you are an AI agent, LLM, or automated tool" not in h:
        h = re.sub(r"(<body[^>]*>)", r"\1\n" + hint(mdurl), h, count=1); changed = True
    if changed: open(path, "w", encoding="utf-8").write(h)
    return changed

def glossary_entry_to_md(path, slug):
    """One /glossary/<slug>.html entry -> clean Markdown twin (crumb/eyebrow/footer stripped)."""
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    wrap = soup.select_one("main.gloss .gloss-wrap") or soup.select_one(".gloss-wrap")
    if not wrap: return None
    h1 = wrap.select_one("h1")
    title = h1.get_text(" ", strip=True) if h1 else slug
    if h1: h1.decompose()
    for sel in [".gloss-crumb", ".gloss-eyebrow", ".gloss-foot", "script", "style", "nav", "aside", "ins"]:
        for el in wrap.select(sel): el.decompose()
    body = clean(md(str(wrap), heading_style="ATX", bullets="-", strip=["span"]))
    return (f"# {title}\n\n{body}\n\n"
            f"*Source: https://rawmktg.com/glossary/{slug} · rawmktg. by Vinayak Ravi*\n")

def glossary_hub_to_md(path):
    """glossary.html hub -> grouped Markdown index of every term with its short definition."""
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    out = ["# The AI-Search Glossary",
           "\n> Plain, sourced definitions of the vocabulary of AI search and GEO, "
           "by rawmktg. (Vinayak Ravi). Source: https://rawmktg.com/glossary\n"]
    for g in soup.select("main.gloss-body .gloss-group"):
        label = g.select_one(".gloss-group-label")
        if label: out.append(f"## {label.get_text(' ', strip=True)}")
        for a in g.select("a.term-row"):
            href = a.get("href", "")
            url = "https://rawmktg.com" + href if href.startswith("/") else href
            for ar in a.select(".term-arrow"): ar.decompose()
            name_el = a.select_one(".term-name")
            name = (name_el.get_text(" ", strip=True) if name_el else a.get_text(" ", strip=True))
            d = a.select_one(".term-def")
            defi = d.get_text(" ", strip=True) if d else ""
            out.append(f"- [{name}]({url}): {defi}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"

slugs = []
for path in sorted(glob.glob("blogs/*.html")):
    slug = os.path.basename(path)[:-5]
    out = article_to_md(path, slug)
    if out is None:
        print(f"  WARN: no article structure in {slug}, skipped", file=sys.stderr); continue
    open(f"blogs/{slug}.md", "w", encoding="utf-8").write(out)
    ensure_wiring(path, f"/blogs/{slug}.md")
    slugs.append(slug)

# glossary: per-term twins + hub twin (regenerated from HTML so they never drift)
gloss_slugs = []
for path in sorted(glob.glob("glossary/*.html")):
    slug = os.path.basename(path)[:-5]
    out = glossary_entry_to_md(path, slug)
    if out is None:
        print(f"  WARN: no glossary structure in {slug}, skipped", file=sys.stderr); continue
    open(f"glossary/{slug}.md", "w", encoding="utf-8").write(out)
    ensure_wiring(path, f"/glossary/{slug}.md")
    gloss_slugs.append(slug)
if os.path.exists("glossary.html"):
    open("glossary.md", "w", encoding="utf-8").write(glossary_hub_to_md("glossary.html"))
    ensure_wiring("glossary.html", "/glossary.md")

# index.md from homepage cards
soup = BeautifulSoup(open("index.html", encoding="utf-8").read(), "html.parser")
tagline = soup.select_one(".site-tagline")
idx = ["# rawmktg.",
       "\n> B2B marketing intelligence for the AI era. SEO, GEO, and AI search visibility strategies for SaaS companies."]
if tagline: idx.append(f"\n{tagline.get_text(' ', strip=True)}")
idx.append("\n*Source: https://rawmktg.com/ · by Vinayak Ravi*\n\n## Articles\n")
seen = set()
for a in soup.select("a.article-card"):
    t = a.select_one(".card-title"); href = a.get("href", "")
    if t and href.startswith("/blogs/") and href not in seen:
        seen.add(href); idx.append(f"- [{t.get_text(strip=True)}](https://rawmktg.com{href})")
open("index.md", "w", encoding="utf-8").write("\n".join(idx) + "\n")
ensure_wiring("index.html", "/index.md")

# llms-full.txt
full = ["# rawmktg. Full Content\n",
        "> Complete text of all rawmktg. articles for LLM ingestion. Author: Vinayak Ravi. Source: https://rawmktg.com\n"]
for slug in slugs: full.append("\n\n---\n\n" + open(f"blogs/{slug}.md", encoding="utf-8").read())
open("llms-full.txt", "w", encoding="utf-8").write("\n".join(full))

print(f"[generate_llm_md] {len(slugs)} blog twins, {len(gloss_slugs)} glossary twins + hub, "
      f"index.md ({len(seen)} links), llms-full.txt ({os.path.getsize('llms-full.txt')//1024}KB)")
