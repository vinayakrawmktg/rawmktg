#!/usr/bin/env python3
"""SCRATCH: build product/marketing pages in rawmktg design system. Do NOT commit as content."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
def esc(t): return H.escape(t,quote=False)
def escq(t): return H.escape(t,quote=True)

AUDIT="https://app.rawmktg.com/audit"
APP="https://app.rawmktg.com"
ENTITY="Sageo Consulting LLP"
ADDR="TB3, Sowparnika Ananda, Sompura Gate, Sarjapur Road, Bangalore 562125, Karnataka"
COUNTRY="India"
REG="[LLP registration number, to add before publishing]"

# ---------------- NEW PRODUCT NAV ----------------
NAV='''<nav class="site-nav" aria-label="Site navigation">
  <div class="page">
    <div class="nav-row">
      <a href="/" class="rm-logo" aria-label="rawmktg home">raw<span class="mktg">mktg</span><span class="dot">.</span></a>
      <div class="nav-links">
        <div class="nav-dropdown">
          <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">Product <span class="caret" aria-hidden="true">&#9662;</span></button>
          <div class="nav-menu" role="menu">
            <span class="nm-sub">Features</span>
            <a role="menuitem" href="/features/ai-visibility-audit"><span class="nm-num">01</span>AI Visibility Audit</a>
            <a role="menuitem" href="/features/share-of-model"><span class="nm-num">02</span>Share of Model</a>
            <a role="menuitem" href="/features/findings-and-fixes"><span class="nm-num">03</span>Findings &amp; Fixes</a>
            <a role="menuitem" href="/features/competitor-tracking"><span class="nm-num">04</span>Competitor Tracking</a>
            <span class="nm-sub">Use cases</span>
            <a role="menuitem" href="/use-cases/b2b-saas-marketing"><span class="nm-num">&rarr;</span>For B2B SaaS marketing</a>
            <a role="menuitem" href="/use-cases/technical-seo"><span class="nm-num">&rarr;</span>For technical SEO</a>
            <a role="menuitem" href="/use-cases/agencies"><span class="nm-num">&rarr;</span>For agencies</a>
            <a role="menuitem" href="/pricing"><span class="nm-num">$</span>Pricing</a>
          </div>
        </div>
        <a href="/research">Research</a>
        <a href="/tools">Tools</a>
        <a href="/glossary">Glossary</a>
        <a href="'''+APP+'''" class="nav-signin">Sign in</a>
        <a href="'''+AUDIT+'''" class="cta">Free audit</a>
      </div>
    </div>
  </div>
</nav>'''

# ---------------- UPDATED FOOTER ----------------
FOOT='''<footer class="site-foot" aria-label="Site footer">
  <div class="page">
    <div class="foot-top">
      <div>
        <div class="foot-col-label">Product</div>
        <div class="foot-cats">
          <a href="/features/ai-visibility-audit">AI Visibility Audit</a>
          <a href="/features/share-of-model">Share of Model</a>
          <a href="/features/findings-and-fixes">Findings &amp; Fixes</a>
          <a href="/features/competitor-tracking">Competitor Tracking</a>
          <a href="/pricing">Pricing</a>
        </div>
      </div>
      <div>
        <div class="foot-col-label">Research</div>
        <div class="foot-cats">
          <a href="/research">All research</a>
          <a href="/topics/industry-teardowns">Industry teardowns</a>
          <a href="/tools">Free tools</a>
          <a href="/glossary">Glossary</a>
          <a href="/methodology">Methodology</a>
        </div>
      </div>
    </div>
    <div class="foot-row">
      <a href="/" style="font-family:'Geist',system-ui;font-weight:800;font-size:15px;letter-spacing:-0.04em;">raw<span style="color:var(--ink-2)">mktg</span><span style="color:var(--signal)">.</span></a>
      <div class="foot-links"><a href="/about">About</a><a href="/contact">Contact</a><a href="/pricing">Pricing</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/refunds">Refunds</a><a href="/llms.txt">llms.txt</a></div>
      <span>&copy; 2026 rawmktg.</span>
    </div>
  </div>
</footer>'''

def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
ORG={"@context":"https://schema.org","@type":"Organization","name":"RawMktg","legalName":ENTITY,"url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}

def head(title,desc,slug,extra_schema=None,og_img="/assets/images/og-default.png"):
    URL=f"https://rawmktg.com/{slug}" if slug else "https://rawmktg.com/"
    sch=[{"@context":"https://schema.org","@type":"WebPage","name":title,"url":URL,"description":desc,"isPartOf":{"@type":"WebSite","name":"RawMktg","url":"https://rawmktg.com"}},ORG]
    if extra_schema: sch=extra_schema+sch
    sj="\n  ".join(jb(o) for o in sch)
    canon=URL
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
     "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
     f"  <title>{esc(title)}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
     f"  <meta name=\"description\" content=\"{escq(desc)}\" />\n  <meta name=\"author\" content=\"RawMktg\" />\n"
     "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
     "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
     "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
     "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
     f"  <link rel=\"canonical\" href=\"{canon}\" />\n"
     f'  <link rel="alternate" hreflang="en-US" href="{canon}" />\n  <link rel="alternate" hreflang="en" href="{canon}" />\n  <link rel="alternate" hreflang="x-default" href="{canon}" />\n'
     "  <meta property=\"og:type\" content=\"website\" />\n"
     f"  <meta property=\"og:url\" content=\"{canon}\" />\n  <meta property=\"og:title\" content=\"{escq(title)}\" />\n"
     f"  <meta property=\"og:description\" content=\"{escq(desc)}\" />\n  <meta property=\"og:site_name\" content=\"RawMktg\" />\n"
     f"  <meta property=\"og:image\" content=\"https://rawmktg.com{og_img}\" />\n  <meta property=\"og:image:width\" content=\"1200\" />\n  <meta property=\"og:image:height\" content=\"630\" />\n"
     "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
     f"  <meta name=\"twitter:title\" content=\"{escq(title)}\" />\n  <meta name=\"twitter:description\" content=\"{escq(desc)}\" />\n"
     f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{og_img}\" />\n"
     f"  {sj}\n"
     "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n  "
     +FONTS+"\n  "+STYLE+"\n  <link rel=\"stylesheet\" href=\"/assets/marketing.css\" />\n</head>\n<body>\n\n"+NAV+"\n\n")

def page(slug,title,desc,body,extra_schema=None):
    html=head(title,desc,slug,extra_schema)+'<main id="main">\n'+body+'\n</main>\n\n'+FOOT+'\n</body>\n</html>\n'
    path=(slug+".html") if slug else "index.html"
    d=os.path.dirname(path)
    if d and not os.path.isdir(d): os.makedirs(d)
    open(path,"w",encoding="utf-8").write(html)
    return html

# ---- component helpers ----
def hero(eyebrow,h1,lede,ctas,note=None):
    cs="".join(f'<a href="{u}" class="m-btn {cls}">{esc(t)}</a>' for t,u,cls in ctas)
    eb=f'<span class="m-eyebrow">{esc(eyebrow)}</span>' if eyebrow else ''
    nt=f'<p class="m-cta-note">{esc(note)}</p>' if note else ''
    return f'<section class="m-hero"><div class="mkt">{eb}<h1>{esc(h1)}</h1><p class="m-lede">{lede}</p><div class="m-cta-row">{cs}</div>{nt}</div></section>\n'
def sec(h2,paras=None,inner="",kicker=None):
    k=f'<span class="m-kicker">{esc(kicker)}</span>' if kicker else ''
    ps="".join(f"<p>{x}</p>" for x in (paras or []))
    hh=f"<h2>{esc(h2)}</h2>" if h2 else ''
    return f'<section class="m-section"><div class="mkt">{k}{hh}{ps}{inner}</div></section>\n'
def layers(items):
    out='<div class="layers">'
    for num,h3,p in items:
        out+=f'<div class="layer"><span class="layer-num">{esc(num)}</span><h3>{esc(h3)}</h3><p>{esc(p)}</p></div>'
    return out+'</div>'
def cards(items,cols="two"):
    out=f'<div class="m-grid {cols}">'
    for it in items:
        h3=it.get("h"); p=it.get("p"); more=it.get("more")
        m=f'<a href="{more[1]}" class="m-more">{esc(more[0])} &rarr;</a>' if more else ''
        out+=f'<div class="m-card"><h3>{esc(h3)}</h3><p>{p}</p>{m}</div>'
    return out+'</div>'
def steps(items):
    out='<div class="steps">'
    for i,(h3,p) in enumerate(items,1):
        out+=f'<div class="step"><span class="step-num">Step {i}</span><h3>{esc(h3)}</h3><p>{esc(p)}</p></div>'
    return out+'</div>'
def shot(img,alt,cap,narrow=False):
    cls="shot narrow" if narrow else "shot"
    return (f'<figure class="{cls}"><img src="/assets/product/{img}" alt="{escq(alt)}" '
            f'width="1600" height="1000" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>')
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+=f"<td{attr}>{esc(c)}</td>"
        body+=f"<tr>{tds}</tr>"
    lab=f'<div class="tt-label">{esc(label)}</div>' if label else ''
    return f'<div class="tt-wrap">{lab}<table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def close(h2,p,ctas):
    cs="".join(f'<a href="{u}" class="m-btn {cls}">{esc(t)}</a>' for t,u,cls in ctas)
    return f'<section class="m-close"><div class="mkt"><h2>{esc(h2)}</h2><p>{esc(p)}</p><div class="m-cta-row">{cs}</div></div></section>\n'
def stats(items):
    out='<div class="m-stats">'
    for b,s in items: out+=f'<div class="m-stat"><b>{esc(b)}</b><span>{esc(s)}</span></div>'
    return out+'</div>'
def L(t,u): return f'<a href="{u}">{esc(t)}</a>'

# ======================= HOMEPAGE =======================
home=""
home+=hero(None,"Find out why AI assistants don't recommend you",
 "Twenty tools will tell you that ChatGPT didn't mention your brand. Almost none will tell you why not, or what to change. <strong>RawMktg diagnoses the cause and generates the fix.</strong>",
 [("Run a free audit",AUDIT,"primary"),("See pricing","/pricing","secondary")],
 "No card required. Audits 25 pages and takes about two minutes.")
home+=sec(None,inner='<div class="mkt">'+shot("audit-result.png","A real free audit result showing citability, pages readable without JavaScript, crawlers refused, and the top three fixes.","A real free audit result. Median citability, how much survives a no-JavaScript fetch, and the three fixes worth doing first.")+'</div>' if False else '')
home+='<section class="m-section"><div class="mkt">'+shot("audit-result.png","A real free audit result showing citability, pages readable without JavaScript, crawlers refused, and the top three fixes.","A real free audit result. Median citability, how much survives a no-JavaScript fetch, and the three fixes worth doing first.")+'</div></section>\n'
home+=sec("Your buyers stopped clicking ten blue links",[
 "When someone asks an AI assistant \"what's the best field service software\", they get an answer, three or four vendors, named and described. Not a list of pages to evaluate. A recommendation.",
 "If your brand isn't in that answer, you are not losing a ranking position. You are absent from the shortlist entirely, and nothing in your analytics will tell you it happened."])
home+=sec("Four problems that look identical from the outside",[
 "\"We're not being mentioned\" has at least four distinct causes, and they need opposite fixes. RawMktg tests each one separately."],
 inner=layers([
  ("Layer 0 &middot; Measure","Measure","How often are you actually named, across a repeatable set of buying questions? With a confidence interval, so you can tell a real change from sampling noise."),
  ("Layer 1 &middot; Mention","Does the model know you exist?","Some brands are missing from the model's memory of the category. That is an off-site, entity and corroboration problem. No amount of on-page editing fixes it."),
  ("Layer 2 &middot; Citation","Can a bot actually read your pages?","AI crawlers fetch differently from browsers. Pages that render fine for a human can return almost nothing to a bot. We measure exactly how much survives."),
  ("Layer 3 &middot; Recommendation","Can your content be quoted?","Retrievable is not the same as quotable. An assistant composing an answer needs a self-contained, factual passage it can lift. Most marketing pages don't have one."),
 ])+'<p class="layers-note"><strong>You cannot fix a mention problem with better on-page content, and you cannot fix a citation problem with more press coverage.</strong> Knowing which one you have is the entire point.</p>')
home+=sec("How it works",None,inner=steps([
 ("Point it at your site","We crawl the way an AI crawler does, respecting robots.txt, at a modest rate, identifying ourselves honestly."),
 ("Get findings, not a score","Seven scoring rubrics and around fifty individual checks produce specific, located faults: this page, this problem, this fix, worth this many points."),
 ("Apply generated fixes","Findings come with artefacts, JSON-LD structured data, rewritten answer blocks, llms.txt files, content briefs, not just advice."),
 ("Measure whether it worked","On paid plans we ask AI assistants your buying questions on a schedule and report your share of their answers against named competitors, over time."),
]))
home+=sec("Built to be honest about uncertainty",None,
 inner=shot("share-of-model.png","Share of Model over time, every figure with a confidence interval, no arrow drawn where a change is not significant.","Share of Model over time. Every figure carries an interval; where a change is not significant, no arrow is drawn.")
 +cards([
  {"h":"Every number carries an interval","p":"AI answers vary run to run. A tool that samples once and reports a percentage is reporting noise. We sample repeatedly and publish the range."},
  {"h":"No arrow without significance","p":"When a change is not statistically distinguishable from noise, we say \"no significant change\" and draw nothing. Most dashboards will happily show you a trend that isn't there."},
  {"h":"Measured and asserted are kept apart","p":"Some inputs can't be measured, whether you publish original research, for instance. Those are labelled \"asserted, not measured\" and never quietly blended into a score."},
  {"h":"Competitors cost nothing extra","p":"Your competitors are scored from the same answers we already collected. We don't charge per tracked brand, because there is no marginal cost to us."},
 ],cols="two"))
home+=sec("Who it's for",None,inner=cards([
 {"h":"B2B SaaS marketing teams","p":"You own the pipeline number and AI search is quietly changing it.","more":("See the use case","/use-cases/b2b-saas-marketing")},
 {"h":"Technical SEO leads","p":"You need to know which pages a bot can't retrieve, and why.","more":("See the use case","/use-cases/technical-seo")},
 {"h":"Agencies","p":"You need defensible reporting across several clients.","more":("See the use case","/use-cases/agencies")},
],cols="three"))
home+=close("Start with your own site","The free audit crawls 25 pages and returns real findings. No card, no call, no trial countdown.",
 [("Run a free audit",AUDIT,"primary"),("Compare plans","/pricing","secondary")])
HOME_SCHEMA=[
 {"@context":"https://schema.org","@type":"SoftwareApplication","name":"RawMktg","applicationCategory":"BusinessApplication","operatingSystem":"Web","description":"Diagnose why AI assistants don't recommend your brand and generate the fixes, with Share of Model measured with confidence intervals.","offers":{"@type":"Offer","price":"99","priceCurrency":"USD"},"publisher":{"@type":"Organization","name":"RawMktg","url":"https://rawmktg.com"}},
 {"@context":"https://schema.org","@type":"WebSite","name":"RawMktg","url":"https://rawmktg.com"},
]
page("","RawMktg: find out why AI assistants don't recommend you",
 "RawMktg diagnoses why AI assistants don't recommend your brand and generates the fix. Free audit crawls 25 pages; measure Share of Model with confidence intervals.",
 home,HOME_SCHEMA)

# ======================= FEATURE: AI VISIBILITY AUDIT =======================
b=hero("Feature &middot; Layer 2, Citation","AI Visibility Audit",
 "Crawl your site the way an AI crawler does, and find out which pages return almost nothing when a bot asks for them, plus the exact reason each one fails.",
 [("Audit your site free",AUDIT,"primary")],"25 pages, no card, about two minutes.")
b+='<section class="m-section"><div class="mkt">'+shot("audit-result.png","The audit summary showing three headline numbers, each mapping to a different failure mode.","The audit summary. Three numbers that each map to a different failure mode.")+'</div></section>\n'
b+=sec("A browser and a bot see different websites",[
 "Your pages probably look fine. You checked. But AI crawlers frequently do not execute JavaScript, and a page assembled client-side can hand a bot an empty shell while showing a human a complete page. Nothing about this is visible from your browser, your analytics or your CMS.",
 "We fetch every page twice, once as a plain request with no JavaScript, once fully rendered, and compare what survives.",
 "<strong>Content Visibility Ratio (CVR)</strong> is the visible words in a raw, no-JavaScript fetch divided by the visible words in the rendered page. A commercial page should be at or above <strong>0.85</strong>. Below that, a bot is reading a fraction of what you wrote, and on some stacks it reads nothing at all."])
b+=sec("What the audit checks",["Seven scoring rubrics, around fifty individual checks. Every one produces a located finding rather than a grade."],
 inner=cards([
  {"h":"Retrieval readiness","p":"Section independence, entity naming, temporal anchors, answer position, vocabulary match, markup integrity, table framing and specificity, the eight properties that decide whether a passage can be lifted into an answer."},
  {"h":"Bot access","p":"Whether AI crawlers are permitted, blocked or silently failing, including the ones your robots.txt never mentions and your CDN may be challenging."},
  {"h":"Page citability","p":"Question headings, front-loaded claims, statistic density, quotes and attribution, section length, scannable structure."},
  {"h":"llms.txt validation","p":"If you publish one, we check it properly: single H1, name-shaped heading, blockquote summary, sectioning, link syntax, whether descriptions actually carry facts."},
  {"h":"Claim anchoring","p":"Answer capsules, section autonomy, proof pairing and brand association, whether a claim can survive being quoted away from its page."},
  {"h":"GEO readiness","p":"Server rendering, load speed, schema markup, consistent entity naming, hard statistics, named expert quotes, first-party data and earned media."},
 ],cols="three"))
b+=sec("Findings, not a number",[
 "A score out of 100 tells you nothing you can act on. Every check that fails produces a finding: which page, which problem, which fix, <strong>worth how many points</strong>, with the evidence attached, the actual markup or text that failed.",
 "Findings are ranked by remediation priority, so the list starts with what will move the number most for the least work.",
 "A finding only changes state on evidence. If a page was skipped, failed to fetch, or wasn't sampled on a given crawl, its findings carry forward unchanged. We never mark something resolved just because we stopped looking at it."],
 inner=shot("findings-list.png","A list of located, point-weighted findings ordered by what moves the score most.","Findings are located and point-weighted, so the list can be ordered by what actually moves the number."))
b+=sec("Crawl volume by plan",None,inner=table(None,
 ["Plan","Pages","Cadence"],
 [["Free audit","25","One-off"],["Diagnostic","500","Weekly"],["Visibility","2,000","Weekly"],["Program","10,000","Weekly"]],
 cls=lambda j,c:"label" if j==0 else "")+'<p class="m-quiet" style="margin-top:12px;"><a href="/pricing" style="color:var(--signal);text-decoration:none;">Full pricing &rarr;</a></p>')
b+=sec("Related",None,inner=cards([
 {"h":"Findings &amp; Fixes","p":"What we generate once a fault is found.","more":("Read more","/features/findings-and-fixes")},
 {"h":"Share of Model","p":"Measuring whether the fix worked.","more":("Read more","/features/share-of-model")},
 {"h":"Competitor Tracking","p":"Who is being recommended instead.","more":("Read more","/features/competitor-tracking")},
],cols="three")+'<p class="m-note">The evidence behind this feature: <a href="/blogs/do-ai-crawlers-render-javascript">do AI crawlers render JavaScript?</a> and <a href="/blogs/how-ai-crawlers-index-your-site">how AI crawlers index your site</a>.</p>')
b+=close("See what a bot actually reads","Run the free audit on your own domain. 25 pages, real findings, no card.",
 [("Audit your site free",AUDIT,"primary"),("See pricing","/pricing","secondary")])
page("features/ai-visibility-audit","AI Visibility Audit: crawl your site like an AI crawler | RawMktg",
 "Crawl your site the way an AI crawler does and find which pages return almost nothing to a bot, with the exact reason each fails. Content Visibility Ratio, floor 0.85.",b)

# ======================= FEATURE: SHARE OF MODEL =======================
b=hero("Feature &middot; Layer 0, Measure","Share of Model",
 "How often AI assistants name your brand, as a share of the whole field, measured repeatedly, reported with a confidence interval, and never dressed up as more certain than it is.",
 [("See plans","/pricing","primary"),("Start with a free audit",AUDIT,"secondary")])
b+=sec("A share, not a rate",[
 "Share of Model is your brand's weighted presence divided by the total weighted presence of every brand in the field, across the same questions, the same engines and the same cadence.",
 "That denominator matters. \"We were mentioned 30% of the time\" is close to meaningless without knowing who else was in the answer and how often. A field share tells you whether you are the default recommendation, one of several, or absent."],
 inner=shot("share-of-model.png","Field share for every tracked brand, each with the confidence interval that says how certain it is.","Field share for every tracked brand, with the interval that says how certain it is."))
b+=sec("What goes into the score",["Presence is not a yes/no. For each brand, in each answer, we score five things, and the weights sum to 100."],
 inner=table(None,["Signal","Weight","What it captures"],
 [["Mention","30%","Was the brand named at all"],
  ["Recommendation","30%","Was it actually recommended, or just listed"],
  ["Position","20%","Where in the answer, first is not the same as fifth"],
  ["Sentiment","15%","How it was characterised"],
  ["Entity accuracy","5%","Did the model describe you correctly"]],
 cls=lambda j,c:"label" if j==0 else ""))
b+=sec("The prompt portfolio is the instrument",[
 "You define a set of real buying questions, the things your prospects actually ask. That set is then <strong>frozen and versioned</strong>. A measurement instrument that changes underneath you produces a trend line that means nothing, so a running cycle cannot have its own questions edited mid-flight.",
 "Each question is asked repeatedly, not once. AI answers vary run to run; a single sample is an anecdote. The full sampling standard is on our <a href=\"/methodology\">measurement methodology</a> page."])
b+=sec("Honest statistics, by construction",None,
 inner=shot("significance-gate.png","A metric whose change is not significant: the interval spans zero, the interface says no significant change and draws no arrow.","When the interval on a change spans zero, the interface says so and draws nothing.")
 +cards([
  {"h":"Every figure has an interval","p":"We report the range, not just the point. A 12% share from twenty samples and a 12% share from two thousand are different claims, and the interval is what says so."},
  {"h":"The significance gate","p":"If the interval on a change spans zero, the interface says \"no significant change\" and draws no arrow. We would rather show you nothing than a movement that is sampling noise."},
  {"h":"Thin cells say so","p":"Cut the data by engine and by question type and the sample per cell shrinks fast. Below the minimum needed to carry an interval, a cell reports \"not enough data\" rather than a number."},
  {"h":"Failed runs are excluded, not counted as zero","p":"If a measurement fails to complete, it leaves the denominator entirely. Counting a failure as an absence is a systematic downward bias, and it is a common one."},
 ],cols="two"))
b+=sec("Raw answers are kept",[
 "We store every AI response verbatim, not just the numbers we extracted from it. When our extraction improves, we can re-analyse your entire history against the better method instead of starting the trend line over.",
 "Every stored score carries the version of the rubric that produced it, so figures from different methods are never silently compared."])
b+=sec("Coverage by plan",None,inner=table(None,["Plan","Prompts","Cadence","Engines"],
 [["Diagnostic","25","Monthly","ChatGPT, Google AI Overviews"],
  ["Visibility","100","Weekly","+ Google AI Mode, Copilot"],
  ["Program","250","Monthly","+ Perplexity, Claude, Grok"]],
 cls=lambda j,c:"label" if j==0 else "")
 +'<p class="m-quiet" style="margin-top:12px;">Diagnostic and Program measure monthly on purpose. Ten samples in one cycle carries a real interval; the same ten spread across four weekly cycles gives you four under-powered ones. <a href="/pricing" style="color:var(--signal);text-decoration:none;">Full pricing &rarr;</a></p>')
b+='<p class="m-note" style="margin:0 0 40px;">The method in depth: <a href="/blogs/share-of-model-measurement">Share of Model, measured properly</a> and the versioned <a href="/methodology">measurement methodology</a>.</p>'
b+=close("Measure your share of the answer","Start with a free audit, then add measurement on a paid plan.",
 [("See plans","/pricing","primary"),("Competitor tracking","/features/competitor-tracking","secondary")])
page("features/share-of-model","Share of Model: measure AI answer share with intervals | RawMktg",
 "Measure how often AI assistants name your brand as a share of the whole field, sampled repeatedly, reported with a confidence interval, with a significance gate.",b)

# ======================= FEATURE: FINDINGS & FIXES =======================
b=hero("Feature &middot; Remediation","Findings &amp; Fixes",
 "Most tools end at \"your schema markup could be improved\". We end at the schema markup, generated, valid, and ready to paste.",
 [("See findings for your site",AUDIT,"primary")])
b+=sec("What a finding is",[
 "One failed check, on one page or entity. Each carries a fix, a point value and a status. Not a category, not a severity band, a specific thing that is wrong in a specific place."],
 inner=shot("finding-detail.png","One finding expanded: the page, the check that failed, the quoted evidence, and the fix.","One finding: the page, the check that failed, the evidence, and the fix.")
 +cards([
  {"h":"Located","p":"The URL, and the actual markup or text that failed the check, quoted as evidence. You should never have to hunt for what we meant."},
  {"h":"Weighted","p":"A point value derived from the rubric, so the list can be ordered by what actually moves the number rather than by how alarming it sounds."},
  {"h":"Prioritised","p":"Ranked by remediation priority, impact against effort, so the top of the list is where to start on Monday morning."},
  {"h":"Stateful","p":"Findings persist across crawls. You can see what was fixed, what regressed, and what has been sitting there for three months."},
 ],cols="two")
 +'<p class="m-note">A finding only changes state on evidence. If a page was skipped, failed to fetch or wasn\'t sampled this crawl, its findings carry forward unchanged. Nothing is auto-resolved because we stopped looking, a "fixed" count that quietly includes pages nobody checked is worse than no count.</p>')
b+=sec("Artefacts, the fix generated",["Findings attach generated output you can use directly."],
 inner=shot("artefact-jsonld.png","A generated JSON-LD artefact attached to its finding, built from the page's own content.","A generated artefact attached to its finding, valid JSON-LD, built from the page's own content.")
 +table(None,["Artefact","What it is"],
 [["JSON-LD","Structured data for the page, generated from its actual content"],
  ["Answer block","A rewritten opening passage that leads with the answer, carries a statistic and can survive being quoted out of context"],
  ["llms.txt","A valid file for your site, correctly sectioned, with descriptions that carry facts"],
  ["robots.txt","Corrected directives where AI crawlers are being blocked unintentionally"],
  ["Schema snippet","Targeted markup for a specific failing check"],
  ["Content brief","Where the fix is editorial rather than technical, what the page needs to say, and why"]],
 cls=lambda j,c:"label" if j==0 else ""))
b+=sec("Asserted is not measured",[
 "Some inputs genuinely cannot be tested by crawling. Whether you publish original first-party research, for instance, or whether a quoted expert is real.",
 "Those are recorded as declared, you assert them, and rendered with an explicit \"asserted, not measured\" badge. They are never quietly blended into a measured score, because a number that mixes the two is not a measurement of anything."])
b+=sec("Export and integrate",[
 "Findings export to CSV with their evidence attached, so they can go into a ticket tracker or a client report without retyping. Visibility and Program plans include API access for findings, pages and rollups."])
b+=sec("Related",None,inner=cards([
 {"h":"AI Visibility Audit","p":"Where findings come from.","more":("Read more","/features/ai-visibility-audit")},
 {"h":"Share of Model","p":"Whether the fix moved the number.","more":("Read more","/features/share-of-model")},
 {"h":"For technical SEO","p":"The workflow in practice.","more":("Read more","/use-cases/technical-seo")},
],cols="three"))
b+=close("Get fixes, not advice","Run a free audit and see the findings, and the artefacts, for your own site.",
 [("Run a free audit",AUDIT,"primary"),("See pricing","/pricing","secondary")])
page("features/findings-and-fixes","Findings & Fixes: generated JSON-LD, answer blocks, llms.txt | RawMktg",
 "Every failed check becomes a located finding with the evidence quoted and a generated fix attached: JSON-LD, rewritten answer blocks, llms.txt, robots.txt and content briefs.",b)

# ======================= FEATURE: COMPETITOR TRACKING =======================
b=hero("Feature &middot; Layers 1 &amp; 3","Competitor &amp; Citation Tracking",
 "Find out who is being recommended in your place, how consistently, and which sources the assistant leaned on to say it.",
 [("See plans","/pricing","primary")])
b+=sec("The models will tell you who your competitors are",[
 "You do not have to guess at the field. Every answer we collect is scanned for brand names, and the ones that recur are surfaced, ranked by how many separate answers named them.",
 "It is frequently not the list you would have written. Assistants routinely name adjacent products, incumbents you had discounted, and occasionally a company you have never heard of that is showing up in a third of answers.",
 "You choose which of those become tracked competitors. The field is a judgement about who a buyer actually compares you against, so it stays yours to set."],
 inner=shot("discovered-brands.png","Brands the models named, ranked by how many separate answers mentioned each.","Brands the models named, ranked by how many separate answers mentioned them."))
b+=sec("Competitors cost nothing extra to score",[
 "Every tracked brand is scored from the same answers we already collected for your own brand. There is no second round of measurement, so there is no marginal cost, which is why we don't price per tracked brand.",
 "A vendor charging you per competitor is charging for something that costs them nothing.",
 "Adding a competitor changes the denominator. Share of Model divides by the field's total presence, so figures from before and after a change to the tracked set are not directly comparable. The interface says so rather than drawing a continuous line across the change."])
b+=sec("Citations, where the answer came from",[
 "When an assistant uses web search to answer, it cites sources. We record every citation in every answer and aggregate them."],
 inner=shot("cited-domains.png","The sources assistants actually leaned on for the category, and whether any of them are yours.","The sources assistants actually leaned on, and whether any of them are yours.")
 +cards([
  {"h":"Which domains get cited","p":"The sources the model actually leans on for your category, review sites, comparison pages, competitors' own documentation, forums."},
  {"h":"Whether any of them are yours","p":"Including subdomains. A brand cited zero times across hundreds of citations has a retrieval problem, not a content problem, and that is a different fix."},
  {"h":"Which of your pages were cited","p":"Citations are matched back to the pages we crawled, so a cited URL connects to its own findings and its own visibility score."},
  {"h":"Cross-engine overlap","p":"How much the engines agree on sources. Very low overlap means engine-specific work; very high overlap means a small set of pages is deciding your category."},
 ],cols="two"))
b+=sec("Tracked competitors by plan",None,inner=table(None,["Plan","Tracked competitors"],
 [["Diagnostic","3"],["Visibility","5"],["Program","10"]],cls=lambda j,c:"label" if j==0 else "")
 +'<p class="m-quiet" style="margin-top:12px;"><a href="/pricing" style="color:var(--signal);text-decoration:none;">Full pricing &rarr;</a></p>')
b+='<p class="m-note" style="margin:0 0 40px;">The research behind this: <a href="/blogs/citation-vs-mention-vs-recommendation">citation vs mention vs recommendation</a> and <a href="/blogs/share-of-model-measurement">Share of Model</a>.</p>'
b+=close("See who is winning your category","Start with a free audit, then track competitors and citations on a paid plan.",
 [("See plans","/pricing","primary"),("How measurement works","/features/share-of-model","secondary")])
page("features/competitor-tracking","Competitor & Citation Tracking for AI answers | RawMktg",
 "See which brands AI assistants recommend instead of you, how consistently, and which sources they cited. Competitors scored from the same answers, no per-brand pricing.",b)

# ======================= USE CASE: B2B SAAS MARKETING =======================
b=hero("Use case","For B2B SaaS marketing teams",
 "You own the pipeline number. A growing share of your category's buying research now happens inside an AI assistant that recommends three vendors and never mentions the rest, and none of it shows up in your analytics.",
 [("Audit your site free",AUDIT,"primary")])
b+=sec("The problem you actually have",[
 "A prospect asks ChatGPT which tools to consider. They get an answer naming four competitors. They evaluate those four. You never appear in a report, because there was no click to attribute and no impression to count.",
 "Traditional search told you where you ranked. AI search tells you nothing at all unless you go and measure it."])
b+=sec("What you get",None,
 inner=shot("share-of-model.png","The Share of Model number you take to a board meeting, with the interval that makes it defensible.","The number you take to a board meeting, with the interval that makes it defensible.")
 +cards([
  {"h":"A defensible number for the board","p":"Share of Model with a confidence interval, tracked over time against named competitors. When a change isn't statistically real, it says so, which matters more than it sounds the first time someone challenges the chart."},
  {"h":"A diagnosis, not just a gap","p":"Whether you are absent because the model doesn't know you, because bots can't retrieve your pages, or because your content can't be quoted. Three different problems with three different owners."},
  {"h":"Work your team can actually do","p":"Located findings with generated fixes, structured data, rewritten answer blocks, content briefs, prioritised by impact against effort."},
  {"h":"Evidence the work paid off","p":"Re-measure on a schedule and see whether the fix moved your share, with the same honesty about significance applied to the improvement as to the problem."},
 ],cols="two"))
b+=sec("Questions this answers",None,inner=cards([
 {"h":"\"Are we in the consideration set?\"","p":"Across your real buying questions, how often you are named and how often you are actually recommended, which are not the same number."},
 {"h":"\"Who is winning our category?\"","p":"The brands assistants name instead of you, ranked by how many answers name them, including ones you had not considered competitors."},
 {"h":"\"Why aren't we being cited?\"","p":"Whether your pages are even retrievable by AI crawlers, and which sources the models are using in your category instead."},
 {"h":"\"Did last quarter's content work?\"","p":"Movement in your share since the change, with an interval, and a plain statement when the movement is not distinguishable from noise."},
],cols="two"))
b+=sec("Where to start",[
 "Run the free audit on your own domain. It crawls 25 pages and returns real findings, no card, no call. If the diagnosis is useful, <strong>Diagnostic at $99/month</strong> adds weekly crawls of 500 pages and monthly measurement."])
b+=close("Find out if you're in the answer","Audit your own domain free, then measure your share of the category.",
 [("Run a free audit",AUDIT,"primary"),("Compare plans","/pricing","secondary")])
page("use-cases/b2b-saas-marketing","AI search visibility for B2B SaaS marketing teams | RawMktg",
 "A growing share of B2B buying research happens inside AI assistants that recommend a few vendors and never mention the rest. Measure your Share of Model and fix the gap.",b)

# ======================= USE CASE: TECHNICAL SEO =======================
b=hero("Use case","For technical SEO",
 "Retrieval is the part of AI visibility that is genuinely technical, genuinely measurable, and almost entirely unserved by the tools in this category.",
 [("Audit your site free",AUDIT,"primary")])
b+=sec("Rendering is the whole problem",[
 "Googlebot renders JavaScript. Many AI crawlers do not, or do so inconsistently. A React-driven page that Google indexes perfectly can hand an AI crawler a nav, a footer and nothing else.",
 "We fetch every page twice, raw and rendered, and give you the ratio between them.",
 "<strong>Content Visibility Ratio</strong>, visible words in a raw fetch divided by visible words in the rendered DOM. Floor for a commercial page is <strong>0.85</strong>. This is a number you can take to an engineering team, put in a ticket and re-measure after the fix."])
b+=sec("What we check that a general SEO crawler doesn't",None,inner=cards([
 {"h":"AI crawler access specifically","p":"Not just Googlebot. Whether the named AI crawlers are permitted, blocked in robots.txt, or being challenged by your CDN or WAF without anyone noticing."},
 {"h":"Section independence","p":"Whether a passage still makes sense lifted out of its page. Retrieval works on chunks, and a chunk full of \"as mentioned above\" is unusable."},
 {"h":"Markup integrity","p":"Heading hierarchy, table framing and structured data as a retrieval system reads them, not as a validator does."},
 {"h":"Entity naming consistency","p":"Whether your product is called the same thing across your own site. Inconsistent naming fragments the entity a model is trying to build."},
 {"h":"llms.txt, validated properly","p":"Single H1, name-shaped heading, blockquote summary, sectioning, link syntax, whether the descriptions carry facts or adjectives."},
 {"h":"Temporal anchors","p":"Whether content states when it is from. Undated pages age badly in a system that weights recency and cannot tell."},
],cols="three"))
b+=sec("Output that goes straight into a ticket",None,
 inner=shot("findings-list.png","Every finding names the URL and quotes the evidence, and exports to CSV with the evidence attached.","Every finding names the URL and quotes the evidence. Exports to CSV with the evidence attached.")
 +'<ul style="font-family:var(--f-prose);font-size:14.5px;line-height:1.7;color:var(--ink-2);max-width:66ch;">'
 '<li>Every finding names the URL and quotes the evidence, the actual markup or text that failed.</li>'
 '<li>Generated artefacts: JSON-LD, schema snippets, corrected robots.txt directives, valid llms.txt.</li>'
 '<li>CSV export with evidence attached, for your tracker or a client report.</li>'
 '<li>API access on Visibility and Program for findings, pages and rollups.</li>'
 '<li>Findings persist across crawls, so you can prove a fix landed, and see when one regresses.</li></ul>')
b+=sec("Crawling that behaves itself",[
 "We respect robots.txt, crawl at a modest rate, and identify our crawler honestly in its user agent. Rendering is used only on the passes that need it, because rendering every page is slow and expensive and mostly unnecessary."])
b+='<p class="m-note" style="margin:0 0 40px;">The research: <a href="/blogs/do-ai-crawlers-render-javascript">do AI crawlers render JavaScript?</a>, <a href="/blogs/how-your-page-gets-retrieved">how your page gets retrieved</a> and <a href="/blogs/xml-sitemaps-for-ai-discovery">the broken-sitemap tax</a>.</p>'
b+=close("Measure what a bot can retrieve","Run a free audit and get located, evidence-backed findings you can ticket.",
 [("Run a free audit",AUDIT,"primary"),("How the audit works","/features/ai-visibility-audit","secondary")])
page("use-cases/technical-seo","AI crawler retrieval audit for technical SEO | RawMktg",
 "Fetch every page raw and rendered, measure the Content Visibility Ratio, and get evidence-backed findings on AI crawler access, section independence and markup integrity.",b)

# ======================= USE CASE: AGENCIES =======================
b=hero("Use case","For agencies",
 "Clients are asking what you are doing about AI search. Most answers available to you are either a dashboard with no diagnosis or an opinion with no evidence.",
 [("Try it on a prospect",AUDIT,"primary")])
b+=sec("The pitch runs itself",[
 "The free audit crawls 25 pages and returns real, located findings on any site you point it at. That is a credible leave-behind for a first conversation, and it costs nothing to produce.",
 "Prospects tend to find \"these eleven pages return almost nothing to an AI crawler, here is the markup that fixes it\" more persuasive than a category-level score."],
 inner=shot("audit-result.png","The free audit on any site you point it at, a credible leave-behind for a first conversation.","The free audit on any site you point it at, a credible leave-behind for a first conversation."))
b+=sec("Delivery your team can staff",None,inner=cards([
 {"h":"Work that is already scoped","p":"Findings are located and point-weighted, ranked by impact against effort. A junior can work the top of the list without needing to invent the plan."},
 {"h":"Artefacts, not advice","p":"Generated JSON-LD, rewritten answer blocks, llms.txt and content briefs. Less of the retainer spent producing deliverables by hand."},
 {"h":"Exports for client reports","p":"CSV with evidence attached, so a finding can be pasted into a deck or a ticket without being retyped or paraphrased into something less true."},
 {"h":"API access","p":"Findings, pages and rollups are available over the API on Visibility and Program, if you report inside your own client portal."},
],cols="two"))
b+=sec("Reporting that survives a sceptical client",[
 "The uncomfortable question in this category is \"how do you know that number is real?\" Most tools cannot answer it, because they sampled once.",
 "Every figure we report carries a confidence interval, and when a month-on-month change is not statistically distinguishable from noise, the interface says so and draws no arrow. That is a harder chart to present and a much easier one to defend.",
 "It also protects you in the other direction. When a client's numbers move for reasons unrelated to your work, the interval is the thing that says so before anyone builds a narrative on it."])
b+=sec("Plans for multi-client work",[
 "<strong>Program at $899/month</strong> covers three projects, 10,000 pages, 250 prompts and up to ten tracked competitors across all seven engines.",
 "<strong>Agency plans start at $1,500/month</strong> and are arranged by conversation, more projects, and terms that suit reselling. <a href=\"/contact\">Get in touch</a>."])
b+=close("Put a credible audit in front of a prospect","Run an audit on any domain, and talk to us about agency terms.",
 [("Run an audit on a prospect",AUDIT,"primary"),("Talk to us about agency terms","/contact","secondary")])
page("use-cases/agencies","AI search visibility reporting for agencies | RawMktg",
 "A free, evidence-backed audit for any prospect domain, located findings your team can staff, generated artefacts, CSV and API exports, and reporting that survives a sceptical client.",b)

# ======================= CONTACT =======================
b=hero(None,"Contact","A real person reads these. We aim to reply within one business day.",
 [("Run a free audit",AUDIT,"primary")])
b+=sec(None,None,inner='<div class="m-contact">'
 +f'<div class="m-card"><h3>Support</h3><p>Questions about the product, a crawl that didn\'t behave, or anything in your account.<br><a href="mailto:support@rawmktg.com">support@rawmktg.com</a></p></div>'
 +f'<div class="m-card"><h3>Sales</h3><p>Agency terms, larger volumes, or anything not covered by the published plans.<br><a href="mailto:sales@rawmktg.com">sales@rawmktg.com</a></p></div>'
 +f'<div class="m-card"><h3>Billing and refunds</h3><p>Invoices, cancellations and refunds. See our <a href="/refunds">refund policy</a> first, it may answer the question faster.<br><a href="mailto:support@rawmktg.com">support@rawmktg.com</a></p></div>'
 +f'<div class="m-card"><h3>Privacy and data</h3><p>Data requests, deletion, or anything in our <a href="/privacy">privacy policy</a>.<br><a href="mailto:privacy@rawmktg.com">privacy@rawmktg.com</a></p></div>'
 +'</div>')
b+=sec("Company details",None,inner=f'<p class="m-entity"><strong>{esc(ENTITY)}</strong>{esc(ADDR)}<br>{esc(COUNTRY)}<br>{esc(REG)}</p>')
b+=sec("Billing is handled by Paddle",[
 "Payments for RawMktg subscriptions are processed by <strong>Paddle</strong>, our authorised reseller and merchant of record. Paddle appears on your statement and issues your invoice. You can also reach them directly using the details on your receipt."])
b+=sec("Our crawler",[
 "If you have seen our crawler on your site and want to ask about it, or want it to stop, email <a href=\"mailto:support@rawmktg.com\">support@rawmktg.com</a>. We respect robots.txt, crawl at a modest rate and identify ourselves honestly in our user agent."])
CONTACT_SCHEMA=[{"@context":"https://schema.org","@type":"Organization","name":"RawMktg","legalName":ENTITY,"url":"https://rawmktg.com","address":{"@type":"PostalAddress","streetAddress":ADDR,"addressCountry":COUNTRY},"contactPoint":[{"@type":"ContactPoint","email":"support@rawmktg.com","contactType":"customer support"},{"@type":"ContactPoint","email":"sales@rawmktg.com","contactType":"sales"},{"@type":"ContactPoint","email":"privacy@rawmktg.com","contactType":"privacy"}]}]
page("contact","Contact RawMktg",
 "Contact RawMktg. Support, sales, billing and privacy mailboxes, company details, and how our crawler behaves. Billing is handled by Paddle as merchant of record.",b,CONTACT_SCHEMA)

# ======================= ABOUT (rewrite) =======================
b=hero(None,"About RawMktg",
 "RawMktg is a product for finding out why AI assistants don't recommend your brand, and fixing it, built by the team behind one of the most-cited independent research programmes in AI search.",
 [("Run a free audit",AUDIT,"primary"),("See pricing","/pricing","secondary")])
b+=sec("What we build",[
 "RawMktg crawls your site the way an AI crawler does, measures how often assistants name you as a share of your whole category, locates the specific reasons you are absent, and generates the fixes, structured data, rewritten answer blocks, llms.txt files and content briefs.",
 "It is organised around four layers, Measure, Mention, Citation and Recommendation, because \"we're not being recommended\" has four different causes that need opposite fixes. The product tests each one separately. The company behind it is <strong>"+esc(ENTITY)+"</strong>."])
b+=sec("The research programme",[
 "Before it was a product, RawMktg was a research publication, and that work continues. We have published 47 original teardowns and technical playbooks, 51 free tools, a 65-term glossary and a versioned measurement methodology, more first-party research on AI search than anyone else in the category.",
 "That research is not marketing decoration. It is where the product's methods came from, and every claim a product page makes is backed by a published piece you can read. Browse it all in <a href=\"/research\">the research library</a>."])
b+=sec("Built on honest measurement",[
 "The position that runs through both the research and the product is that AI answers vary, so every number should carry an interval and no trend should be drawn unless it clears significance. We would rather show you nothing than a movement that is sampling noise. The full standard is public on our <a href=\"/methodology\">measurement methodology</a> page."])
b+=sec("Who is behind it",[
 "RawMktg is built by Vinayak Ravi and operated by "+esc(ENTITY)+", registered at "+esc(ADDR)+", "+esc(COUNTRY)+". Questions, including about our crawler, go to <a href=\"mailto:support@rawmktg.com\">support@rawmktg.com</a>, or see the <a href=\"/contact\">contact page</a>."])
b+=close("See what a bot reads on your site","Start with a free audit of your own domain. No card, no call.",
 [("Run a free audit",AUDIT,"primary"),("Read the research","/research","secondary")])
page("about","About RawMktg",
 "RawMktg is a product for finding out why AI assistants don't recommend your brand and fixing it, backed by 47 original teardowns, 51 tools and a versioned methodology.",b)

print("built product pages:", [p for p in ["index.html","features/ai-visibility-audit.html","features/share-of-model.html","features/findings-and-fixes.html","features/competitor-tracking.html","use-cases/b2b-saas-marketing.html","use-cases/technical-seo.html","use-cases/agencies.html","contact.html","about.html"] if os.path.exists(p)])
# expose NAV/FOOT for the research builder
open("/tmp/prod_nav.html","w").write(NAV)
open("/tmp/prod_foot.html","w").write(FOOT)

