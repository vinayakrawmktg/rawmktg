#!/usr/bin/env python3
"""SCRATCH: build /methodology canonical measurement page. Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="methodology"; URL=f"https://rawmktg.com/{SLUG}"; PUB="2026-08-26"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x").replace("−","-"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
CBCOPY=open("blogs/schema-markup-ai-citations-2026.html",encoding="utf-8").read()
mcb=re.search(r'<style id="cb-copy-css">.*?</script>', CBCOPY, re.S); CB=mcb.group(0) if mcb else ""

def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def h3(t): return f"<h3>{esc(t)}</h3>"
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div><table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u): return f'<a href="{u}">{norm(t)}</a>'

HEADLINE="The rawmktg Measurement Methodology"
DECK=("One standard for every number we publish. What a prompt portfolio must contain, how many times we run it, how we bound "
      "the result, and what has to be true before a figure is called decision-grade rather than directional.")
DESC=("The canonical, versioned rawmktg methodology for measuring AI-search visibility: prompt portfolio tiers, 8 to 12 runs per prompt per engine, Wilson and bootstrap intervals, a 200-observation per-cell guard, and refresh cadence.")
DATANOTE="Version 1.0, effective 26 August 2026. This page is the single source of truth. Where an article and this page disagree, this page wins, and the article is corrected."

FORM_SOM=r'''SoM(b) =  Σ_e Σ_p  w_e · w_p · score(b,e,p)   ÷   Σ over every brand in the field

  b  brand            score  0.30 mention + 0.30 recommendation
  e  engine                   + 0.20 position + 0.15 sentiment + 0.05 prominence
  p  prompt           w_e, w_p  engine and prompt-bucket weights
  Share of Model is a share of the whole field, not a raw inclusion rate.'''

FORM_N=r'''n  =  z^2 · p(1-p) / e^2          # observations per brand per engine

  z = 1.96 (95%)   p = expected inclusion rate   e = target margin
  For p = 0.30 and e = 0.02, n ~ 2,000 observations.
  At 10 runs per prompt that is ~200 prompts per engine cell.'''

FORM_GUARD=r'''-- No cell is reported until it clears the sample floor.
SELECT brand_id, engine, AVG(present) AS inclusion
FROM   observations
WHERE  portfolio_version = 'v2026.08'
GROUP  BY brand_id, engine
HAVING COUNT(*) >= 200;   -- under-sampled cells are withheld, not shown'''

out=[]
out.append(callout("Version 1.0 &middot; effective 26 August 2026",[
  "This is the canonical specification behind every visibility number rawmktg publishes, in articles, teardowns and the free tools. It is versioned. When it changes, the version and the changelog at the foot of this page change with it, and any figure that depends on the change is restamped. If a teardown and this page ever disagree, this page is correct."]))
out.append(p("Most AI-visibility numbers you will see anywhere, including screenshots in sales decks, come from a single query typed once into one engine. That is not a measurement, it is an anecdote with a timestamp. AI answers are non-deterministic: ask the same question ten times and the set of brands named changes, sometimes by fifteen points, with nothing altered on any website. A method that ignores that variance reports noise as fact. This page defines the method that does not."))
out.append(pull("A number is only decision-grade when it would survive being measured again next week. Everything here exists to make that true."))

out.append(sec("01","portfolio","What has to be in a prompt portfolio?",
 "A frozen, versioned set of real buyer prompts, bucketed by intent, held constant across cycles.",
 "The portfolio is the instrument. It is assembled once, version-stamped, and never quietly edited, because changing the questions between cycles makes the trend meaningless. Prompts are sorted into intent buckets so a brand that wins commercial questions but loses research questions is visible, not averaged away."))
out.append(p("Every prompt is a real question a buyer in the category would ask an assistant, phrased the way a person phrases it, not a keyword. Prompts are split into three buckets, commercial (best, top, alternatives), research (how, what, comparison), and brand (named-entity checks). Each bucket carries a weight, because an appearance in a high-intent commercial answer is worth more than one in a definitional aside. The portfolio is stored with a version tag such as v2026.08 and frozen for the life of that version, so every cycle measures the same instrument."))
out.append(table("Table 1. Portfolio tiers. The tier sets the width of the question set, not the statistical rigour, which is fixed in section 2.",
 ["Tier","Prompts","What it answers","Confidence"],
 [["Baseline / diagnostic","50 to 150","A fast read: are we present at all, and where are the obvious holes","Directional, not for board slides"],
  ["Decision-grade / standard","250 to 500","The default. Share and trend you can act on and defend","Roughly a plus or minus 2-point margin"],
  ["Enterprise / category","500+","Full category coverage, per-segment and per-region breakouts","Tight intervals on sub-segments"]],
 cls=lambda j,c: "label" if j==0 else ("up" if "default" in c.lower() else "")))
out.append(p("Different rawmktg articles run different tiers on purpose. The "+L("prompt-to-citation baseline","/blogs/prompt-to-citation-tracking")+" starts at 50 to 150 because it is a 30-day diagnostic; the "+L("Share of Model spec","/blogs/share-of-model-measurement")+" runs 250 to 500 because it is decision-grade. Those are not contradictions, they are named tiers of the same method. What never changes between them is the run count."))

out.append(sec("02","runs","How many times is each prompt run?",
 "Eight to twelve times per prompt per engine. The default is ten. This is fixed at every tier.",
 "Portfolio width is a scope choice; run count is not. Because a single response is a coin flip, each prompt is issued 8 to 12 times to every engine and the results are averaged, which is what turns a set of anecdotes into an inclusion rate with a real interval around it. Fewer than eight runs and the interval is too wide to act on."))
out.append(p("Ten runs is the working default. Below eight, cycle-to-cycle swings are dominated by sampling noise rather than real change, which is how a brand appears to gain or lose fifteen points in a month with no work done. This is the single parameter that must be identical everywhere, and it is the one earlier drafts were loosest about. A baseline diagnostic may use a narrow portfolio, but it still runs each prompt the full eight-to-twelve times, otherwise it is not a baseline, it is a guess."))
out.append(callout("The rule that overrides the others",[
  "If you take one number from this page, take this: 8 to 12 runs per prompt per engine, default 10, at every tier and in every article. A wide portfolio run once is worse than a narrow portfolio run ten times."]))

out.append(sec("03","engines","Which engines count, and how are they weighted?",
 "Each engine is measured and reported separately, then combined with evidence-based weights, never averaged blind.",
 "ChatGPT Search, Google AI Overviews, Perplexity, Copilot and Gemini cite different sources for the same question, so a blended single number hides where you are winning. Engines are weighted by audience reach and citation behaviour, and every headline figure ships with its per-engine breakdown."))
out.append(p("The engines diverge enough that optimising for one does little for another, which is why cross-engine source overlap is low and why the report keeps them apart. Weights reflect reach and how much each engine actually influences a buyer, and they live in the versioned config so a weight change is a version change. The composite is only ever presented alongside the per-engine rows it is built from."))

out.append(sec("04","bounds","How is a number bounded and guarded?",
 "Every rate carries a Wilson interval, trends use response-level bootstrap, and no cell is reported below 200 observations.",
 "A point estimate with no interval invites over-reading. Inclusion rates are reported with 95% Wilson intervals; period-over-period changes are tested with a response-level bootstrap so a move is only called real when it clears the noise band; and any brand-engine cell with fewer than 200 observations is withheld rather than shown."))
out.append(code("formula &middot; Share of Model",FORM_SOM))
out.append(code("formula &middot; observations for a target margin",FORM_N))
out.append(p("The sample maths is why decision-grade lands at 250 to 500 prompts: at a 30% base rate and a plus or minus 2-point target, you need roughly 2,000 observations per engine, which at ten runs is about 200 prompts per engine cell. You can size any target yourself with the "+L("sample-size and confidence planner","/tools/sample-size-confidence-planner")+". The 200-observation floor is enforced in the query, not left to judgement."))
out.append(code("sql &middot; the per-cell sample-size guard",FORM_GUARD))

out.append(sec("05","cadence","How often is it re-run, and what makes a figure decision-grade?",
 "Monthly on a frozen portfolio, restamped on every version change. Decision-grade requires the standard tier, full runs, and a passing sample guard.",
 "Cadence is monthly so trend outpaces noise without burning tokens. A figure earns the decision-grade label only when it is measured on a 250-plus prompt portfolio, at 8 to 12 runs, with every reported cell clearing 200 observations. Anything short of that is published as directional and labelled as such."))
out.append(p("The distinction is a labelling rule, not a soft preference. Directional numbers, from a baseline portfolio, are allowed and useful, but they are never dressed up as decision-grade, and they never appear without the word. Declared inputs that cannot be measured, whether a brand publishes original research, has named expert quotes, runs an aged and authentic community account, are kept in a visibly separate declared section with an asserted, not measured label, and are never folded silently into a measured composite."))

out.append(sec("06","changelog","What changes, and how do you know it changed?",
 "Every change to a parameter, weight or portfolio version is recorded here with a date.",
 "Versioning is the trust mechanism. A methodology that can be edited invisibly is worth nothing, so every change to a weight, a threshold, a run default or a portfolio version is logged below with the date it took effect and what it affected."))
changelog=('<div class="tt-wrap"><div class="tt-label">Changelog</div><table class="tt"><thead><tr><th>Version</th><th>Date</th><th>Change</th></tr></thead><tbody>'
 '<tr><td class="label">v1.0</td><td>26 Aug 2026</td><td>Initial published standard. Fixes the run count at 8 to 12 (default 10) across all tiers and articles; defines the baseline / decision-grade / enterprise portfolio tiers; sets the 200-observation per-cell reporting floor.</td></tr>'
 '</tbody></table></div>')
out.append(changelog)

FAQ=[
 ("How many prompts should an AI-visibility measurement use?",
  "It depends on what the number is for, and rawmktg uses three named tiers. A baseline diagnostic uses 50 to 150 prompts and is directional. A decision-grade programme, the default, uses 250 to 500 prompts, which at ten runs per prompt gives roughly a plus or minus 2-point margin. Enterprise or full-category work uses 500 or more. The tier sets how wide the question set is; it does not change the run count, which is fixed."),
 ("How many times should you run each prompt?",
  "Eight to twelve times per prompt per engine, with ten as the default, at every tier. AI answers are non-deterministic, so a single response is a coin flip. Averaging 8 to 12 runs is what converts anecdotes into an inclusion rate with a usable confidence interval. Below eight runs, month-to-month swings are dominated by sampling noise rather than real change."),
 ("Why not just average all the engines into one score?",
  "Because ChatGPT Search, Google AI Overviews, Perplexity, Copilot and Gemini cite different sources for the same question, so a blended number hides where you are winning and losing. rawmktg measures and reports each engine separately, then combines them with evidence-based weights held in a versioned config, and always shows the per-engine breakdown behind any composite."),
 ("What makes a number decision-grade rather than directional?",
  "Three things together: a portfolio of at least 250 prompts, 8 to 12 runs per prompt per engine, and every reported brand-engine cell clearing 200 observations. If any of the three is missing, the figure is published as directional and labelled that way. Declared inputs that cannot be measured are kept in a separate section and never folded into a measured score."),
 ("Why is this methodology versioned?",
  "So it cannot be edited invisibly. A method that can change without a record is not a standard. Every change to a weight, threshold, run default or portfolio version is logged in the changelog on this page with its effective date, and any published figure that depends on the change is restamped."),
]
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

out.append('<div class="about-block"><div class="about-label">Where this method is applied</div>'
 '<p>Read the full spec and worked example in '+L("Share of Model, measured properly","/blogs/share-of-model-measurement")+'. Size your own sample with the '+L("sample-size and confidence planner","/tools/sample-size-confidence-planner")+'. See the baseline version in '+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+', and the metric taxonomy in '+L("citation vs mention vs recommendation","/blogs/citation-vs-mention-vs-recommendation")+'.</p></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
 '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("8-12","runs per prompt per engine, fixed"),("10","the working default"),("250-500","prompts for a decision-grade read"),("200","observation floor per reported cell"),("v1.0","effective 26 Aug 2026")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#portfolio"><span class="toc-num">01</span>The prompt portfolio</a></li>'
     '<li><a href="#runs"><span class="toc-num">02</span>Runs per prompt</a></li>'
     '<li><a href="#engines"><span class="toc-num">03</span>Engines and weights</a></li>'
     '<li><a href="#bounds"><span class="toc-num">04</span>Bounds and guards</a></li>'
     '<li><a href="#cadence"><span class="toc-num">05</span>Cadence and grade</a></li>'
     '<li><a href="#changelog"><span class="toc-num">06</span>Versioning</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">The standard</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">On this page</div><ul class="toc-list">{toc}</ul></div></aside>')

def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
tech={"@context":"https://schema.org","@type":"TechArticle","headline":norm(HEADLINE),"description":norm(DESC),"url":URL,"datePublished":PUB,"dateModified":PUB,"version":"1.0","author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["AI visibility methodology","Share of Model","prompt portfolio","runs per prompt","Wilson interval","sample size","GEO measurement"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":"Methodology","item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="The rawmktg Measurement Methodology &middot; v1.0 &middot; rawmktg."
da=escq(DESC)
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
 "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
 f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
 f"  <meta name=\"description\" content=\"{da}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
 "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
 "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
 f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
 f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{escq(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 "  <meta property=\"og:image\" content=\"https://rawmktg.com/assets/images/og-default.png\" />\n  <meta property=\"og:image:width\" content=\"1200\" />\n  <meta property=\"og:image:height\" content=\"630\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{escq(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 "  <meta name=\"twitter:image\" content=\"https://rawmktg.com/assets/images/og-default.png\" />\n"
 f"  {jb(tech)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/{SLUG}.md\" />\n  "+FONTS+"\n  ")
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Methodology &middot; v1.0</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Effective Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CB+"\n</body>\n</html>\n")
open(f"{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+tail)

hh=open(f"{SLUG}.html").read()
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (json.loads(b) or True))
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| h1:",hh.count("<h1"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),"| faq:",hh.count('faq-item'))
