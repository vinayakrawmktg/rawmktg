#!/usr/bin/env python3
"""SCRATCH: GSC-driven exact-match FAQ additions (7 articles) + tool meta/deck sharpening (5 tools)."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

def esc(t): return H.escape(t,quote=False)

# (slug, question, answer)
ART=[
 ("becoming-an-entity",
  "Is Wikidata a knowledge graph, and how does it help SEO?",
  "Yes. Wikidata is a free, structured knowledge graph whose entries each carry a unique QID, and it is one of the primary sources large language models and Google's Knowledge Graph draw on to resolve entities. For Wikidata SEO the payoff is that a Wikidata entry helps you become a known entity: it gives your brand a machine-readable identifier a model can attach facts to, which is why a Wikidata QID and a consistent sameAs link from your site to your Wikidata and Wikipedia knowledge-graph nodes are among the highest-leverage entity signals you can build."),
 ("share-of-model-measurement",
  "What is Share of Model tracking, and do you need an agency for it?",
  "Share of Model tracking is measuring, on a fixed cadence, how often and how prominently a brand is named across AI answers for a category, then trending it over time. You do not need a Share of Model agency to start: the method is a frozen prompt portfolio run 8 to 12 times per engine with the results scored and bounded, which an in-house team can run themselves. An agency mainly helps with scale and consistency, not with anything proprietary; the full standard is public on the measurement methodology page."),
 ("schema-markup-ai-citations-2026",
  "What is the best schema for AI search citations?",
  "There is no single tag; the schema that earns AI search citations is the set that resolves your entity and your facts unambiguously. In practice that means Organization with a sameAs array to bind your identity, Article or the relevant content type for the page, and Product, FAQPage or Dataset where they apply, all cross-linked by explicit @id. Structured data does not force a citation, but sites with fully implemented JSON-LD see materially higher AI citation rates because the model can extract a fact and attribute it to a resolved entity."),
 ("do-ai-crawlers-render-javascript",
  "Can AI crawlers execute JavaScript?",
  "Mostly no. In a twelve-crawler test, nine ran no JavaScript runtime at all, so for AI search JavaScript rendering you should assume the crawler sees only your raw server-rendered HTML. Two crawlers pass only because they inherit a search engine's render pipeline, and one is limited. If your content, pricing or specifications only appear after client-side JavaScript executes, most AI crawlers cannot read them, which is why server-side rendering or prerendering is the fix."),
 ("citation-vs-mention-vs-recommendation",
  "Citation vs mention: what is the difference?",
  "A mention names your brand in the answer text; a citation links or attributes a specific claim to your page as a source. Mentions and citations are not interchangeable: you can be mentioned constantly and never cited, or cited as a source without being recommended as the answer. Mentions build the prior that you belong in the category, citations ground a specific claim in your content, and recommendations convert, each has a different cause and a different fix."),
 ("30-day-content-half-life-recency-ai-ranking-signal",
  "How does content recency affect AI rankings?",
  "Strongly, and faster than in classic SEO. Content updated within roughly the last 30 days is cited at several times the rate of static pages on competitive commercial queries, and pages left untouched for months face a sharply higher chance of losing citations entirely. Content recency behaves like a decay curve, so a genuine substantive refresh, not a changed byline date, on your commercially important pages is one of the highest-leverage ranking signals in AI search."),
 ("comparison-pages-ai-shortlists",
  "What makes a comparison page get pulled into AI shortlists?",
  "Four things: a verdict box that names a winner for a specific segment, high fact density with real numbers and prices, question-shaped headings that match how buyers ask, and visible neutrality that names where each option wins. AI engines pull ranked, extractable comparison pages into shortlists far more often than undifferentiated listicles, and only a small share of cited comparison URLs sit in Google's organic top ten, so page structure matters more than the domain's rank."),
]

for slug,q,a in ART:
    f=f"blogs/{slug}.html"; s=open(f,encoding="utf-8").read()
    if q in s: print("skip (present):",slug); continue
    # 1. visible FAQ: insert as first item
    item=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>'
    m=re.search(r'<div class="faq-item">', s)
    assert m, f"no faq-item in {slug}"
    s=s[:m.start()]+item+s[m.start():]
    # 2. FAQPage JSON-LD: prepend question to mainEntity array
    qobj=json.dumps({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    anc='"@type": "FAQPage", "mainEntity": ['
    if anc not in s: anc='"@type":"FAQPage","mainEntity":['
    assert anc in s, f"no FAQPage mainEntity in {slug}"
    s=s.replace(anc, anc+qobj+", ", 1)
    open(f,"w",encoding="utf-8").write(s)
    print("optimized:",slug)

# ---- TOOLS: append exact-query phrase to meta descriptions + deck ----
# (slug, phrase to ensure present in description/deck, deck-append sentence)
TOOLS=[
 ("llms-txt-validator","llms.txt checker"," It is a free llms.txt validator and checker for AI search."),
 ("ai-bot-log-analyzer","AI bot tracker"," A free AI bot tracker for your server logs."),
 ("rrf-rank-fusion-calculator","RRF calculator"," The free RRF calculator for reciprocal rank fusion."),
 ("sentiment-share-of-voice-calculator","free share of voice calculator"," A free share of voice calculator for AI answers."),
 ("cross-engine-source-overlap-calculator","source overlap calculator"," The free source overlap calculator across AI engines."),
]
for slug,phrase,deckadd in TOOLS:
    f=f"tools/{slug}.html"; s=open(f,encoding="utf-8").read()
    if deckadd.strip() in s: print("skip tool (present):",slug); continue
    # append to visible deck
    m=re.search(r'(<p class="article-deck">)(.*?)(</p>)', s, re.S)
    assert m, f"no deck in {slug}"
    deck=m.group(2).rstrip()
    if not deck.endswith('.'): deck=deck+'.'
    s=s[:m.start(2)]+deck+deckadd+s[m.end(2):]
    # append phrase to the three description meta tags
    for pat in [r'(<meta name="description" content=")([^"]*)(")',
                r'(<meta property="og:description" content=")([^"]*)(")',
                r'(<meta name="twitter:description" content=")([^"]*)(")']:
        def rep(mm):
            body=mm.group(2)
            if phrase.lower() in body.lower(): return mm.group(0)
            b=body.rstrip();
            if not b.endswith('.'): b=b+'.'
            return mm.group(1)+b+' '+deckadd.strip()+mm.group(3)
        s=re.sub(pat, rep, s, count=1)
    open(f,"w",encoding="utf-8").write(s)
    print("tool optimized:",slug)
print("done")
