#!/usr/bin/env python3
"""SCRATCH: build blogs/hr-saas-ai-visibility-gap.html in the rawmktg teardown format.
Do NOT commit."""
import os, re, json, html as H
from PIL import Image
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

SLUG="hr-saas-ai-visibility-gap"
URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"

def norm(t):
    t=(t.replace("—",", ").replace("–","-")
        .replace("‘","'").replace("’","'")
        .replace("“",'"').replace("”",'"').replace("…","..."))
    t=re.sub(r",\s*,",",",t)
    return t

# ---- reusable blocks sliced from an existing teardown ----
T=open("blogs/aec-ai-visibility-gap.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")
ADSENSE=sl("<script>(function(){var l=false","})();</script>")
GA=sl("<!-- Google tag (gtag.js) -->","gtag('config','G-4B3LL6MJKN');</script>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")

# extra CSS for figures (white charts on paper)
FIGCSS=("""
    .article-figure{margin:30px 0 10px;}
    .article-figure img{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:8px;background:#fff;}
    .figcap{font-family:var(--f-mono);font-size:9.5px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--mute);text-align:center;margin:12px 0 30px;line-height:1.55;}
  """)
STYLE=STYLE.replace("</style>",FIGCSS+"</style>")

def dim(path):
    im=Image.open("."+path); return im.size

def fig(name,cap):
    full=f"/assets/images/{name}.webp"; w,h=dim(full)
    srcset=f"/assets/images/{name}-760.webp 760w, {full} {w}w"
    sizes="(max-width:768px) calc(100vw - 40px), 652px"
    return (f'<figure class="article-figure">\n'
            f'  <img src="{full}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
            f'loading="lazy" alt="{H.escape(norm(cap),quote=True)}" />\n'
            f'  <figcaption class="figcap">{H.escape(norm(cap))}</figcaption>\n</figure>')

def p(t): return f"<p>{norm(t)}</p>"
def answer(t): return f'<div class="section-answer">{norm(t)}</div>'

# ---------------- content ----------------
HEADLINE="When Buyers Ask AI Which HR Software to Use, One Brand Owns the Answer"
DECK=("A nearly 6× ChatGPT-citation lead, a 15× organic-traffic gap, and an AI moat almost "
      "nobody in HR SaaS is building. Six findings from the data on ADP, Workday, Sage, Gusto, "
      "BambooHR and Rippling.")
DESC=("Ahrefs organic-search and AI-citation data across six HR SaaS platforms (ADP, Workday, Sage, "
      "Gusto, BambooHR, Rippling). Sage owns a ~6x AI-citation lead, ADP a 15x traffic gap, and the "
      "consideration layer is empty at every brand. Six findings and what to do about them.")
DATANOTE=("Based on Ahrefs organic-keyword, referring-domain and AI-citation data across six HR SaaS "
          "platforms (ADP, Workday, Sage, Gusto, BambooHR, Rippling), captured June 2026. Funnel and "
          "brand/non-brand classifications computed from full keyword exports across all markets.")

INTRO=[
 "Ask ChatGPT which HR or payroll platform a mid-market company should use, and one name comes back more often than any other. It is not the biggest brand in the category. It is not the best-funded challenger, the most recognisable logo, or the site with the most traffic. It is Sage, a forty-year-old accounting-software company most American HR buyers would not place at the top of their shortlist.",
 "That gap, between who buyers expect to see and who actually shows up at the moment of discovery, is the story of HR SaaS search in 2026. We pulled Ahrefs organic-search and AI-citation data across six of the category's most prominent platforms, ADP, Workday, Sage, Gusto, BambooHR and Rippling, and the pattern was consistent. The brands winning the old visibility game are not the ones winning the new one, and almost nobody is building for where discovery is heading.",
 "Here is what the data showed.",
]

SIDEBAR=[("~6×","Sage's ChatGPT-citation lead over the field"),
         ("15×","Organic-traffic gap, ADP vs Rippling"),
         ("89%","Of Workday's organic traffic is just its brand name"),
         ("11×","ADP's link-to-traffic efficiency over Workday")]

FINDINGS=[
 dict(id="ai-visibility",num="01",title="AI Visibility Is Already Being Decided, and One Brand Owns It",
  ans="Sage earns roughly 1,200 ChatGPT citations a month, nearly 6× Workday (214) and BambooHR (189). It leads every major AI surface: Google AI Overviews (~1,300), Perplexity (1,200) and Copilot (512).",
  blocks=[
   ("p","Ahrefs now tracks how often each domain is cited across AI assistants, and the HR SaaS leaderboard looks nothing like the brand-recognition leaderboard. Sage is cited three to six times more than the field on every consumer AI surface that matters. Its lead is not marginal; it is categorical."),
   ("fig","hr-saas-fig1-ai-citations","Monthly AI citations across ChatGPT, Google AI Overviews and Perplexity. Source: Ahrefs, June 2026."),
   ("p","The more revealing story is who trails. Workday, the enterprise category leader by revenue and brand, sits near the bottom at 214 ChatGPT citations. Its gated, sales-led content gives AI engines very little to quote. BambooHR, genuinely beloved inside HR circles, is similarly thin in the model's eyes. Meanwhile Rippling punches well above its size (613 AI Overview pages, 677 Perplexity citations) because its security and IT-glossary content is exactly the kind of explanatory material AI crawlers lift."),
   ("p","Why it matters: a growing share of software evaluation now begins with an AI query, and the model's answer is assembled from what the open web already vouches for. The brands absent from those answers today were not judged and rejected, they were never in the corpus to begin with. As AI-mediated discovery compounds, that absence becomes a direct, and increasingly expensive, pipeline problem."),
  ]),
 dict(id="authority-traffic",num="02",title="Authority Is Nearly Identical. Traffic Is Not. A 15× Gap.",
  ans="Five of the six brands sit at Domain Rating 86-91, elite, hard-won authority. Yet organic traffic ranges from ADP's 7.4M monthly visits to Rippling's 500K. A 15× spread sitting on top of nearly identical authority.",
  blocks=[
   ("p","Put the six side by side and the first surprise is how little their core authority differs. Domain Rating clusters between 83 and 91, a band that takes years of brand-building and link acquisition to reach. The second surprise is how little that authority predicts traffic."),
   ("fig","hr-saas-fig2-traffic-dr","Monthly organic traffic with Domain Rating labelled. Source: Ahrefs, June 2026."),
   ("table3",),
   ("p","ADP alone draws more organic traffic, and more traffic value ($17.9M a month), than the other five combined. Authority, in other words, is the ticket into the game, not the score. What separates these brands is what they choose to point that authority at. ADP points it at calculators. Workday points it at its own brand name. Those two choices explain most of the table above, and they are the subject of the next three findings."),
  ]),
 dict(id="branded-traffic",num="03",title="Most of This Organic Traffic Is Just the Brand's Own Name",
  ans="Workday: 89% of organic traffic is branded. Gusto: 72%. Strip the brand name out of Workday and only ~216K monthly visits remain, less than BambooHR earns from non-brand search alone.",
  blocks=[
   ("p","Branded traffic, people typing “workday login” or “gusto payroll”, is valuable, but it is a lagging indicator of marketing spend and category fame, not something search independently earns. Non-brand traffic is the real measure of a content engine. Split the six on that line and the dependence is stark."),
   ("fig","hr-saas-fig3-branded-share","Branded vs non-brand share of organic traffic. Source: Ahrefs keyword exports, June 2026."),
   ("p","Workday is the most brand-dependent platform in the set: nine in ten organic visits are its own name or an acquired product (Peakon, VNDLY). Gusto (72%) and Rippling (61%) are similarly brand-led, reflecting how much venture-funded demand generation drives their search footprint. Only BambooHR (57% non-brand) and Sage (54%) have search strategies that genuinely acquire new, unbranded audiences."),
   ("p","The risk is structural. When organic search mostly recaptures demand the brand already created, it is a mirror of marketing spend rather than an independent growth channel, and the moment brand or paid investment dips, so does the “organic” line that depends on it."),
  ]),
 dict(id="empty-middle",num="04",title="The Funnel Is Inverted, the Consideration Layer Is Empty",
  ans="MoFu (consideration) traffic is just 2-13% of the total at every brand. The “best HR software” and “X vs Y” queries, where buyers actually choose, are owned by G2, Capterra and Forbes Advisor, not the vendors.",
  blocks=[
   ("p","Map every keyword to a funnel stage and the same shape appears six times: a reasonable top (awareness), a heavy bottom (brand and decision), and almost nothing in the middle. The consideration layer, comparison terms, “best,” “alternatives,” “vs,” is where buyers narrow their shortlist, and it is precisely where these vendors are absent."),
   ("fig","hr-saas-fig4-funnel","Share of organic traffic by funnel stage. Amber = MoFu. Source: Ahrefs, June 2026."),
   ("p","That real estate has not vanished, it has been ceded to third-party review aggregators. And here the two stories connect: those same aggregators (G2, Capterra, software-roundup media) are exactly the sources AI engines lean on when recommending tools. So the empty middle is not only lost consideration-stage traffic; it is lost AI citations too. The funnel inversion and the AI-visibility gap are the same problem viewed from two angles."),
  ]),
 dict(id="owned-utilities",num="05",title="A Free Calculator Out-Earns an Entire Competitor",
  ans="ADP's payroll and tax calculators pull roughly 2.6M non-brand visits a month, more than the total traffic of any other brand in the set. Per 1,000 referring domains, ADP converts authority into traffic 11× more efficiently than Workday.",
  blocks=[
   ("p","ADP's non-brand dominance is not built on thousands of blog posts. It is built on a handful of durable, link-worthy utilities, a paycheck calculator (415K visits a month on its own), a salary calculator, a tax calculator. These tools rank for enormous, evergreen demand and earn links passively. Measure non-brand traffic earned per 1,000 referring domains and the efficiency gap is dramatic."),
   ("fig","hr-saas-fig5-link-efficiency","Non-brand visits earned per 1,000 referring domains, a link-to-traffic conversion measure. Source: Ahrefs, June 2026."),
   ("p","ADP converts at ~121K non-brand visits per 1,000 referring domains; Workday, with a comparable link base, manages ~11K. Same authority, an order-of-magnitude difference in yield, because Workday has little non-brand content to rank. The lesson generalises: links raise the ceiling, but only owned, ranking content decides whether you reach it. Workday, Gusto and Rippling all have the authority to support an ADP-style utility; none has built one."),
  ]),
 dict(id="referring-domains",num="06",title="Referring Domains Are the Hidden Engine, and One Brand Is Running on Fumes",
  ans="Sage's 34.6K referring domains are nearly 4× Rippling's 8.9K. Rippling also carries the lowest dofollow share (74%) and the highest spam rate (26%), the structural reason its content cannot break into competitive non-brand terms.",
  blocks=[
   ("p","Underneath every finding so far sits one engine: the referring-domain profile. It is what builds Domain Rating, which governs how competitively a site can rank and how often AI engines cite it. Profiled by quality, the six diverge sharply."),
   ("fig","hr-saas-fig6-refdomains","Referring domains by Domain Rating band. Source: Ahrefs, June 2026."),
   ("p","Volume alone misleads, 17-26% of every brand's referring domains are spam-flagged scrapers and directories. The metric that actually correlates with rankings, AI citations and traffic is the count of editorial DR-60-plus domains: Sage (4,469), Workday (3,145), ADP (2,840), BambooHR (2,721), Gusto (2,687) and, far behind, Rippling (1,221). Rippling's thin, lower-quality base is the clearest single constraint in the category and the direct cause of its narrow non-brand footprint and lowest-in-set DR of 83."),
   ("p","These signals reinforce one another, which is why the gaps here are structural rather than seasonal. Referring domains lift Domain Rating; higher DR lets content rank and earns AI citations; that traffic builds brand demand; brand demand attracts more links. The loop compounds."),
   ("fig","hr-saas-fig7-flywheel","The visibility flywheel: each turn makes the next easier, and widens the gap for anyone outside it."),
   ("p","For Rippling, the implication is concrete: closing even half the referring-domain gap to its peers would lift its authority ceiling across rankings and AI citations simultaneously. For everyone, the 17-26% spam load is a shared, immediate disavow opportunity."),
  ]),
]

# data table 3
TABLE3_ROWS=[
 ("ADP","91","21.8K","88.4K","7.4M","$17.9M","up"),
 ("Workday","87","20.0K","23.5K","2.0M","$3.0M",""),
 ("Sage","88","34.6K","77.1K","1.3M","$3.6M",""),
 ("Gusto","86","20.9K","41.7K","1.0M","$3.0M",""),
 ("BambooHR","90","19.1K","42.0K","585K","$1.3M",""),
 ("Rippling","83","8.9K","33.6K","500K","$1.1M","neg"),
]
def table3():
    head="".join(f"<th>{c}</th>" for c in
        ["Brand","DR","Ref. Domains","Organic KWs","Organic Traffic/mo","Traffic Value/mo"])
    rows=""
    for b,dr,rd,kw,tr,tv,cls in TABLE3_ROWS:
        trcls=' class="up"' if cls=="up" else (' class="mute"' if cls=="neg" else "")
        rows+=(f'<tr><td class="label">{b}</td><td>{dr}</td><td>{rd}</td><td>{kw}</td>'
               f'<td{trcls}>{tr}</td>'
               f'<td>{tv}</td></tr>')
    return ('<div class="tt-wrap">\n<div class="tt-label">Fig. 2b: Authority vs Traffic, six HR SaaS brands · Source: Ahrefs, June 2026</div>\n'
            f'<table class="tt"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>\n</div>')

# analysis
DATA_SAYS=[
 ("AI visibility is a present moat, not a future one.","Sage's lead was not won this quarter, it was built over years of authoritative, well-cited content. The brands absent from AI answers today face a catch-up that gets more expensive every quarter the gap compounds."),
 ("Brand dependence is hiding fragility.","Workday and Gusto look strong on an organic dashboard, but strip the brand name and most of the traffic disappears. Search is mirroring their marketing spend, not adding to it."),
 ("The empty middle is the shared, winnable opportunity.","No vendor owns the consideration layer. The first to build genuine comparison and category content, and earn links to it, takes share that currently sits with review aggregators, and earns AI citations in the process."),
 ("Owned utilities beat content volume.","ADP's calculators prove a single durable tool can out-earn an entire competitor's content library. Authority is necessary; a reason to rank is what converts it."),
 ("Links set the ceiling; everything else decides whether you hit it.","Referring-domain quality underwrites rankings and AI citations alike. Rippling's thin profile caps its upside no matter how good its content gets."),
]
DO=[
 ("Audit your AI-citation footprint now.","Measure where you appear across ChatGPT, AI Overviews, Perplexity and Copilot before optimising anything else. You cannot close a gap you have not measured, and this is the surface buyers are moving to fastest."),
 ("Build for the empty middle.","Create comparison hubs, category pages and “alternatives” content for the consideration-stage queries, then earn niche-relevant links to them. This is the single largest uncontested opportunity in the category."),
 ("Ship a durable owned utility.","A calculator, benchmark tool or template engine that ranks for evergreen non-brand demand will out-earn dozens of blog posts and attract links passively, exactly the ADP playbook."),
 ("Fix the link foundation where it is thin, and disavow spam everywhere.","For under-linked challengers (Rippling), closing the referring-domain gap is the highest-leverage move available. For everyone, review the 17-26% spam-flagged domains."),
 ("Treat non-brand traffic as the real scoreboard.","Branded traffic flatters the dashboard. Track non-brand visits and non-brand keyword growth as the true measure of whether search is adding demand or just reflecting it."),
 ("Get into the sources AI trusts.","Depth of presence on G2, Capterra and editorial software media is not just referral traffic, it is the citation infrastructure that decides whether AI recommends you at all."),
]
CLOSING=[
 "The visibility hierarchy in HR SaaS has almost nothing to do with product quality, funding, or even brand size. Workday is the category's most valuable brand and one of its least visible in AI search. Sage is far from the obvious leader and owns the AI answer. ADP turns the same authority everyone else has into ten times the traffic, off a handful of calculators.",
 "What separates them is infrastructure, referring domains, content built for the right stage of the funnel, and presence in the sources that feed AI recommendations. That infrastructure compounds, which means today's gaps quietly widen on their own. The brands that win the next five years of HR-software discovery are the ones building it now, while the surface is still being decided. The rest are relying on a brand-demand engine that search is only reflecting back to them, right up until the moment buyers stop searching their name and start asking the model instead.",
]
FAQ=[
 ("Which HR software brand has the most AI visibility?","Across the six platforms analysed, Sage has the strongest AI-citation profile by a wide margin, roughly 1,200 ChatGPT citations a month and the lead on Google AI Overviews, Perplexity and Copilot, three to six times the field. Its advantage traces directly to the largest and cleanest referring-domain base in the set (34.6K domains, 17.6% spam), since AI engines preferentially cite well-linked, authoritative sources."),
 ("Why does ADP get so much more organic traffic than its competitors?","ADP draws 7.4M monthly organic visits, more than the other five brands combined, primarily from free payroll and tax calculators that rank for very high-volume, evergreen non-brand queries (its paycheck calculator alone earns ~415K visits a month). These owned utilities convert ADP's domain authority into traffic about 11× more efficiently than a brand like Workday, which has comparable authority but little non-brand content."),
 ("What is the biggest shared SEO weakness across HR SaaS companies?","The empty middle of the funnel. Across all six brands, consideration-stage (MoFu) queries account for just 2-13% of organic traffic. The “best HR software,” “alternatives” and “X vs Y” terms buyers use to choose a tool are dominated by third-party review sites rather than the vendors, which also costs the vendors AI citations, since those same review sites are what AI models quote."),
 ("How much do referring domains affect HR SaaS search visibility?","Substantially. Referring domains build Domain Rating, which sets the ceiling for how competitively a site can rank and how often AI engines cite it. In this cohort the editorial DR-60-plus domain count tracks both keyword breadth and AI visibility, and the brand with the thinnest profile (Rippling, 8.9K domains, DR 83) is the most visibility-constrained. But links alone do not create traffic, owned, ranking content does, which is why ADP and Workday, with similar link bases, differ 11× in non-brand traffic."),
]
KEYNUMBERS=[
 ("~6×","Sage's ChatGPT-citation lead over Workday and BambooHR"),
 ("15×","Organic-traffic gap, ADP (7.4M) vs Rippling (500K), on near-identical authority"),
 ("89%","Share of Workday's organic traffic that is just its own brand name"),
 ("11×","ADP's link-to-traffic efficiency advantage over Workday on non-brand visits"),
 ("2-13%","Consideration-stage (MoFu) share of organic traffic, empty at every brand"),
]
ABOUT=("rawmktg. publishes data-driven teardowns of B2B verticals, pulling AI-citation and SEO data "
       "across the main players to show exactly where the visibility gaps are. Method: same data, "
       "same lens, every time. Contact: vinayak@rawmktg.com")
DATASRC=("Data source: Ahrefs (organic keywords, referring domains, AI citations), captured June 2026. "
         "Funnel and brand/non-brand classifications computed from full keyword exports across all markets.")

# inline interlinks: phrase -> url (first occurrence in body)
LINKS=[
 ("what the open web already vouches for","/blogs/authority-seeding-ai-llm-trust"),
 ("The loop compounds.","/blogs/geo-compounding-flywheel"),
 ("comparison hubs, category pages","/blogs/topical-authority-cluster-ai-shortlists"),
 ("Audit your AI-citation footprint now.","/blogs/geo-foundation-audit"),
 ("those same review sites are what AI models quote","/blogs/how-rag-actually-works"),
 ("Domain Rating, which governs how competitively","/glossary/domain-rating"),
]

# ---------------- assemble body ----------------
out=[]
out.append("".join(p(t) for t in INTRO))
for f in FINDINGS:
    out.append(f'<h2 id="{f["id"]}"><span class="section-num">{f["num"]}</span>{norm(f["title"])}</h2>')
    out.append(answer(f["ans"]))
    for blk in f["blocks"]:
        if blk[0]=="p": out.append(p(blk[1]))
        elif blk[0]=="fig": out.append(fig(blk[1],blk[2]))
        elif blk[0]=="table3": out.append(table3())
# analysis sections
out.append('<h2>What the Data Says About HR SaaS Visibility in 2026</h2>')
for lead,rest in DATA_SAYS:
    out.append(f"<p><strong>{norm(lead)}</strong> {norm(rest)}</p>")
out.append('<h2>What HR SaaS Companies Should Actually Do</h2>')
out.append(p("Based on what the data shows, here is the sequence we would recommend for any HR or payroll platform that wants to close the discoverability gap with the category's visibility leaders."))
out.append("<ul>"+"".join(f"<li><strong>{norm(l)}</strong> {norm(r)}</li>" for l,r in DO)+"</ul>")
out.append('<h2>Closing Thought</h2>')
out.append("".join(p(t) for t in CLOSING))
# FAQ
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{norm(q)}</h3><p class="faq-a">{norm(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
# key numbers (dark table)
kn="".join(f'<tr><td class="up">{norm(v)}</td><td>{norm(d)}</td></tr>' for v,d in KEYNUMBERS)
out.append('<div class="tt-wrap"><div class="tt-label">Key Numbers</div>'
           f'<table class="tt"><thead><tr><th>Metric</th><th>What it measures</th></tr></thead><tbody>{kn}</tbody></table></div>')
# about
out.append(f'<div class="about-block"><div class="about-label">About rawmktg.</div><p>{norm(ABOUT)}</p><p>{norm(DATASRC)}</p></div>')

body="\n".join(out)
# apply interlinks
for phrase,u in LINKS:
    np=norm(phrase)
    if np in body:
        body=body.replace(np,f'<a href="{u}">{np}</a>',1)

# sidebar
sb_stats="".join(f'<div class="sg-block"><div class="stat-val">{norm(v)}</div><div class="stat-label">{norm(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc="".join(f'<li><a href="#{f["id"]}"><span class="toc-num">{f["num"]}</span>{norm(f["title"])}</a></li>' for f in FINDINGS)
SIDEBAR_HTML=(f'<aside class="sidebar">\n'
 f'<div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb_stats}</div></div>\n'
 f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div>\n</aside>')

# header image responsive
HW,HH=2400,1260
hdr_srcset=(f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w")
HEADER_IMG=(f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" '
            f'alt="{H.escape(HEADLINE)} - rawmktg." class="article-header-img" width="{HW}" height="{HH}" loading="eager">')

# ---------------- schema ----------------
blogposting={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,
 "description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,
 "datePublished":"2026-06-09","dateModified":"2026-06-09",
 "author":{"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]},
 "publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},
 "mainEntityOfPage":{"@type":"WebPage","@id":URL},
 "keywords":["HR software","HR SaaS","AI visibility","GEO","SEO","ChatGPT citations","Perplexity","AI search","ADP","Workday","Sage","referring domains","Domain Rating"]}
speakable={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck",".section-answer","h2"]},"url":URL}
breadcrumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
 {"@type":"ListItem","position":2,"name":"HR SaaS AI Visibility Gap","item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
 {"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
person={"@context":"https://schema.org","@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'

hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
      'overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or '
      f'automated tool, a clean Markdown version of this page is available at {URL}.md. Optimized for AI and LLM tools.</div>')

TITLE="The HR SaaS AI Visibility Gap &middot; rawmktg."
da=H.escape(norm(DESC),quote=True)
head_top=(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  {GA}
  <meta name="robots" content="index, follow" />
  <title>{TITLE}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{da}" />
  <meta name="author" content="Vinayak Ravi" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/favicon-180.png" />
  <link rel="canonical" href="{URL}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{URL}" />
  <meta property="og:title" content="{H.escape(HEADLINE)}" />
  <meta property="og:description" content="{da}" />
  <meta property="og:site_name" content="rawmktg." />
  <meta property="og:image" content="https://rawmktg.com{IMG}.webp" />
  <meta property="article:published_time" content="2026-06-09T00:00:00Z" />
  <meta property="article:modified_time" content="2026-06-09T00:00:00Z" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{H.escape(HEADLINE)}" />
  <meta name="twitter:description" content="{da}" />
  <meta name="twitter:image" content="https://rawmktg.com{IMG}.webp" />
  {jb(blogposting)}
  {jb(speakable)}
  {jb(breadcrumb)}
  {jb(faqpage)}
  {jb(person)}
  {jb(org)}
  {FONTS}
  """)
head_tail=(f"""  <link rel="alternate" type="application/rss+xml" title="rawmktg." href="https://rawmktg.com/feed.xml" />
  <link rel="alternate" type="text/markdown" href="/blogs/{SLUG}.md" />
</head>
<body>
{hint}

{NAV}

{HEADER_IMG}

<div class="page">
  <header class="article-header">
    <div class="article-eyebrow">
      <span class="eyebrow-tag">Analysis &middot; HR SaaS</span>
      <span class="eyebrow-sep">&middot;</span>
      <span class="eyebrow-date">June 2026</span>
    </div>
    <h1 class="article-headline">{norm(HEADLINE)}</h1>
    <p class="article-deck">{norm(DECK)}</p>
    <p class="article-data-note">{norm(DATANOTE)}</p>
  </header>
</div>

<div class="page">
  <div class="article-body">
    <main class="article-content" id="article-main">
{body}
    </main>
{SIDEBAR_HTML}
  </div>
</div>

{NEWS}

{FOOT}
</body>
</html>
""")

head=head_top+"  "+STYLE+"\n  "+ADSENSE+"\n"+head_tail
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head)
em=open(f"blogs/{SLUG}.html").read().count("—")
en=open(f"blogs/{SLUG}.html").read().count("–")
print(f"wrote blogs/{SLUG}.html | em dashes:{em} en dashes:{en} | bytes:{os.path.getsize(f'blogs/{SLUG}.html')}")
