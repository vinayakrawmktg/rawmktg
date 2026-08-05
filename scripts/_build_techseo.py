#!/usr/bin/env python3
"""SCRATCH one-off: build the Technical SEO collection into the existing glossary.
Generates /glossary/<slug>.html entries from the uploaded term .md files, matching
the existing entry template. Do NOT commit."""
import os, re, json, glob, html
import yaml

ROOT = "/sessions/optimistic-youthful-planck/mnt/rawmktg"
SRC  = "/tmp/seoglossary/nested"
os.chdir(ROOT)

TPL = open("glossary/citation-gap.html", encoding="utf-8").read()
def slice_between(s, a, b, inc=True):
    i = s.index(a); j = s.index(b, i) + len(b)
    return s[i:j] if inc else s[i+len(a):j-len(b)]
STYLE   = slice_between(TPL, "<style>", "</style>")
ADSENSE = slice_between(TPL, "<script>(function(){var l=false", "})();</script>")
NAV     = slice_between(TPL, '<nav class="site-nav"', "</nav>")
NEWS    = slice_between(TPL, '<section class="newsletter-section"', "</section>")
FOOT    = slice_between(TPL, '<footer class="site-foot"', "</footer>")

def norm(t):
    return t.replace("—", ", ").replace("–", "-")
def esc_text(t):
    return html.escape(norm(t), quote=False)
def esc_attr(t):
    return html.escape(norm(t), quote=True)
def inline(t):
    t = esc_text(t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    return t

def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
    fm = yaml.safe_load(m.group(1)); body = m.group(2)
    # body sections by '## '
    secs = []
    for chunk in re.split(r'\n## ', body):
        if chunk.startswith('## '): chunk = chunk[3:]
        # first chunk contains <small>, # H1, capsule; skip (we use frontmatter)
        if chunk.lstrip().startswith('<small>') or chunk.lstrip().startswith('# '):
            continue
        lines = chunk.split('\n', 1)
        head = lines[0].strip()
        rest = lines[1] if len(lines) > 1 else ''
        if head.lower() in ('go deeper', 'related terms'):
            continue
        paras = [p.strip() for p in re.split(r'\n\s*\n', rest) if p.strip()]
        secs.append((head, paras))
    return fm, secs

def render(fm, secs):
    slug = fm['slug']; term = fm['term']; desc = fm['description']; h1 = fm['h1']
    url = f"https://rawmktg.com/glossary/{slug}"
    # sections html
    body_html = []
    for head, paras in secs:
        body_html.append(f"      <h2>{esc_text(head)}</h2>")
        for p in paras:
            body_html.append(f"      <p>{inline(p)}</p>")
    body_html = "\n".join(body_html)
    # foot
    gd = "".join(f'<a href="{g["url"]}">{esc_text(g["label"])}</a>' for g in fm.get('goDeeper', []))
    rel = "".join(f'<a href="/glossary/{r["slug"]}">{esc_text(r["name"])}</a>' for r in fm.get('relatedTerms', []))
    foot = (f'      <div class="gloss-foot">\n'
            f'        <div><div class="row-label">Go deeper</div><div class="links">{gd}</div></div>\n'
            f'        <div class="related"><div class="row-label">Related terms</div><div class="links">{rel}</div></div>\n'
            f'      </div>')
    # JSON-LD
    dterm = {"@context":"https://schema.org","@type":"DefinedTerm","name":term,
             "description":norm(desc),"url":url,"inDefinedTermSet":"https://rawmktg.com/glossary",
             "dateModified":"2026-06-07"}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":norm(q["q"]),
             "acceptedAnswer":{"@type":"Answer","text":norm(q["a"])}} for q in fm.get('faq',[])]}
    title = f"What is {esc_attr(term)}? &middot; rawmktg."
    da = esc_attr(desc)
    hint = ('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;'
            'margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">'
            'If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page '
            f'is available at https://rawmktg.com/glossary/{slug}.md. Optimized for AI and LLM tools.</div>')
    head = (
      '<!doctype html>\n<html lang="en">\n<head>\n'
      '  <meta charset="utf-8" />\n  <meta name="robots" content="index, follow" />\n'
      f'  <title>{title}</title>\n'
      '  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
      f'  <meta name="description" content="{da}" />\n'
      '  <meta name="author" content="Vinayak Ravi" />\n'
      f'  <link rel="canonical" href="{url}" />\n'
      '  <meta property="og:type" content="article" />\n'
      f'  <meta property="og:url" content="{url}" />\n'
      f'  <meta property="og:title" content="{title}" />\n'
      f'  <meta property="og:description" content="{da}" />\n'
      '  <meta property="og:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />\n'
      '  <meta property="og:site_name" content="rawmktg." />\n'
      '  <meta name="twitter:card" content="summary_large_image" />\n'
      f'  <meta name="twitter:title" content="{title}" />\n'
      f'  <meta name="twitter:description" content="{da}" />\n'
      '  <meta name="twitter:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />\n'
      f'  <script type="application/ld+json">{json.dumps(dterm)}</script>\n'
      f'  <script type="application/ld+json">{json.dumps(faq)}</script>\n'
      '  <link rel="icon" type="image/x-icon" href="/favicon.ico" />\n'
      '  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png" />\n'
      '  <link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16.png" />\n'
      '  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/favicon-180.png" />\n'
      '  <link rel="alternate" type="application/rss+xml" title="rawmktg." href="https://rawmktg.com/feed.xml" />\n'
      f'  <link rel="alternate" type="text/markdown" href="/glossary/{slug}.md" />\n'
      '  <link rel="preconnect" href="https://fonts.googleapis.com" />\n'
      '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
      '  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" />\n'
      '  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'" />\n'
      '  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" /></noscript>\n  '
    )
    mainhtml = (
      '\n<main class="gloss">\n  <div class="page">\n    <div class="gloss-wrap">\n'
      '      <div class="gloss-crumb"><a href="/">rawmktg.</a> / <a href="/glossary">Glossary</a></div>\n'
      '      <div class="gloss-eyebrow">Technical SEO</div>\n'
      f'      <h1>{esc_text(h1)}</h1>\n'
      f'      <p class="capsule">{esc_text(desc)}</p>\n'
      + body_html + "\n" + foot + "\n"
      '    </div>\n  </div>\n</main>\n\n'
    )
    out = (head + STYLE + "\n  " + ADSENSE + "\n</head>\n<body>\n" + hint + "\n\n"
           + NAV + "\n" + mainhtml + NEWS + "\n\n" + FOOT + "\n</body>\n</html>\n")
    out = out.replace("/technical-seo-glossary/", "/glossary/").replace('href="/technical-seo-glossary"', 'href="/glossary"')
    return out

files = [f for f in glob.glob(f"{SRC}/*.md") if os.path.basename(f) not in ("index.md","_FULL-combined-preview.md")]
order = []  # (group, term, slug, shortdef)
n=0
for path in sorted(files):
    fm, secs = parse(path)
    htmlout = render(fm, secs)
    open(f"glossary/{fm['slug']}.html","w",encoding="utf-8").write(htmlout)
    order.append((fm['group'], fm['term'], fm['slug'], norm(fm['description'])))
    n+=1
print("generated tech entries:", n)
# report em/en dashes in generated files
em = sum(open(f"glossary/{s}.html").read().count("—") for *_,s,_ in [(g,t,sl,d) for g,t,sl,d in order])
em = sum(open(f"glossary/{sl}.html").read().count("—") for g,t,sl,d in order)
en = sum(open(f"glossary/{sl}.html").read().count("–") for g,t,sl,d in order)
print("em dashes:", em, "| en dashes:", en)
# save order for hub builder
json.dump(order, open("/tmp/tech_order.json","w"))
print("groups:", sorted(set(g for g,_,_,_ in order)))
