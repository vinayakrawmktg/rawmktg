#!/usr/bin/env python3
"""SCRATCH: build blogs/payments-getting-found-google-ai.html (payments GEO+SEO playbook). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="payments-getting-found-google-ai"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-08-05"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'

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
def chart(cid,h,cap): return f'<div class="chart-wrap"><canvas id="{cid}" height="{h}"></canvas></div><div class="chart-caption">{esc(cap)}</div>'
def donut(cid,cap): return f'<div class="chart-wrap"><div class="donut-box" style="max-width:320px;margin:6px auto;"><canvas id="{cid}" height="260"></canvas></div></div><div class="chart-caption">{esc(cap)}</div>'
def statgrid(items):
    cells="".join(f'<div class="sg-item"><div class="sg-val">{esc(v)}</div><div class="sg-label">{esc(l)}</div></div>' for v,l in items)
    return f'<div class="stat-grid">{cells}</div>'
def pipeline(nodes,goal,cap):
    parts=['<div class="pipeline">']
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Getting Found on Google and AI"
DECK=("A payments marketer's playbook, drawn from GEO and SEO audits of 48 digital-payments companies. Where discovery really "
      "happens now, why brands win their name but lose the category, and the 90-day system that closes the gap.")
DESC=("A payments playbook from 48 fintech audits: why discovery doubled, how brands win their name but lose the category, "
      "and the 90-day plan to get found on Google and AI.")
DATANOTE=("An aggregate analysis of full GEO (Generative Engine Optimization) and SEO audits of 48 digital-payments and money-movement "
          "companies, spend and expense management, AP/AR automation, corporate and fleet cards, supply-chain and trade finance, and "
          "accounting automation, August 2026. Every number is an aggregate of those audits; brands are named to illustrate a tactic, "
          "not to rank or endorse anyone.")

out=[]
out.append('<p class="lead">'+norm("For a decade, getting found in payments meant one job: rank on Google for the terms buyers search. That job has not gone away, but a second one has appeared beside it, and most brands in the category are still only playing the first.")+'</p>')
out.append(p("The finance leader evaluating a spend-management tool, the controller comparing AP-automation vendors, the founder shopping for a corporate card, they now run the same question through two systems at once. They still open Google, but they also ask ChatGPT, Perplexity, Gemini, Copilot or Grok to shortlist the options. Both systems return an answer. Your brand is either inside that answer or it is invisible."))

# 01 THE SHIFT
out.append(sec("01","shift","How has discovery changed for payments buyers?","Discovery doubled, and most payments brands optimised for only half of it.",
  "The category is no longer competing only for blue links; it is competing to be the named recommendation inside an AI-generated answer. The good news: both systems draw on the same underlying signals, clear content, technical cleanliness and third-party trust, so the work compounds. Fixing your site for AI usually fixes it for Google too, which is "+L("why winning Google and winning AI are now one job","/blogs/winning-google-isnt-winning-ai")+"."))
out.append(pipeline([("Buyer question","one question, asked twice"),("Google","a page of ranked blue links"),("AI assistant","one synthesised answer that names a few brands"),("The shortlist","you are in it, or you are invisible")],3,
  "Figure 1, The same buyer question now runs through classic search and AI assistants in parallel. You have to show up in both, and "+L("classic SEO alone no longer gets you there","/blogs/why-traditional-seo-is-no-longer-enough")+"."))

# DATASET
out.append(sec("02","dataset","What's in the 48-company dataset?","Full GEO and SEO audits of 48 digital-payments and money-movement companies, spread across five overlapping sub-sectors.",
  "Each audit examined the same three pillars: website health for both Google and AI crawlers; content gaps, the buyer questions rivals answer and the company does not; and authority, how the company's links and listings compare with rivals. Every number here is an aggregate of those audits."))
out.append(table("Figure 2, the five sub-sectors represented in the 48-company sample",["Sub-sector","What these companies do","Representative buyer terms"],[
 ("Spend & expense management","Corporate cards, expense control and bill pay in one platform","\"spend management\", \"expense management software\""),
 ("AP / AR automation","Automating invoices, collections and payables","\"accounts receivable automation\", \"AP automation\""),
 ("Corporate & fleet cards","Issuing and managing payment cards","\"corporate card\", \"fleet fuel cards\""),
 ("Supply-chain & trade finance","Early payments, invoice discounting, working capital","\"invoice discounting\", \"supply chain finance\""),
 ("Accounting automation","Bookkeeping, close and reconciliation software","\"bookkeeping software\", \"accounting automation\""),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(h3("The shape of the field"))
out.append(p("Three benchmark numbers give a feel for the typical competitor you are up against, and explain why the opportunity is so evenly distributed: almost everyone sits in the same middle band, so small, deliberate moves change the standings."))
out.append(statgrid([("~3,500","Median monthly Google visits"),("~1,200","Median referring domains"),("49","Median Domain Rating (0-100)"),("86","Median AI citations per audit")]))
out.append(chart("payAuthority",210,"Figure 3, Domain Rating is clustered. Most companies sit in the same 35-60 band, which is exactly why the category is winnable, no one holds an unassailable lead."))

# FINDING 1
out.append(sec("03","wrong-traffic","Are you ranking for the wrong traffic?","Probably. A large share of payments' free Google traffic comes from informational \"learner\" queries, definitions, formulas and calculators, not from buyers.",
  "Think \"what is DPO\", \"EIN lookup\", \"YTD meaning\", \"how to read a cash flow statement\". These pages rank well and pull real volume, but they attract students and analysts, not buyers with a purchase in motion. In roughly 4 in 10 audits the single biggest traffic driver was informational content only loosely related to what the company sells."))
out.append(donut("payIntent","Figure 4, the typical intent mix. Category leaders are distinguished less by total traffic than by how much of it is commercial."))
out.append(callout("A quick test for any content page",[
 "Would the person who searched this term ever buy what you sell? If the honest answer is no, the page may still have a role in brand or SEO plumbing, but it should never be counted as marketing performance. A page that earns 500 visits from people ready to buy beats 50,000 from people looking up a definition.",
 "Audit your top 20 traffic pages and label each \"learner\" or \"buyer\". If more than half are learner pages, you have a routing problem, not a traffic problem, add a clear, contextual path from every high-traffic guide to the relevant product or category page.",
]))

# FINDING 2
out.append(sec("04","page-2-trap","The Page-2 Trap: are you winning your name but losing the category?","Almost certainly. Companies rank #1 for their brand and one niche term, but sit on page two or three for the broad category terms buyers actually compare on.",
  "71% of the sample showed this exact signature: strong on brand, weak on category. The important nuance is that this is the good kind of problem. Ranking #21 for \"spend management\" means you already rank, Google already trusts the page enough to place it. Moving from page two to page one is a fundamentally easier job than starting from nothing."))
out.append(statgrid([("~50%","Stuck on page 2-3 for their core category term"),("71%","Strong on brand, weak on the category"),("100%","Had at least one low-difficulty category term within reach")]))
out.append(table("The recurring ranking signature, by term type",["Term type","Typical rank in the data","Buyer intent","Priority"],[
 ("Your brand / product name","#1-2","Already yours","Defend"),
 ("Niche \"owned\" term","#1-3","High, but small volume","Protect & expand"),
 ("Core category term","#20-25 (page 2-3)","High, this is the prize","Attack first"),
 ("Adjacent category term","#25-35","Medium","Attack second"),
 ("Broad head term","Not ranking","Mixed, giants own it","Later / selective"),
], cls=lambda j,c:"label" if j==0 else ("up" if (j==3 and "Attack first" in c) else "")))
out.append(h3("Why the leaders win these terms"))
out.append(p("Look at who occupies the top of \"corporate card\", \"spend management\" or \"AP automation\" and you see the same discipline: Ramp, Brex, Bill.com and a few peers run deep, purpose-built hubs for each category term, a strong landing page, a cluster of supporting articles, comparison pages, and "+L("dense internal linking that concentrates authority on the money page","/blogs/internal-linking-for-ai-retrieval")+". They are not necessarily higher-authority domains overall; they are simply more deliberate about aiming that authority at the category."))

# FINDING 3
out.append(sec("05","technical","Is technical health quietly taxing your visibility?","Yes, and it is now an AI tax too. None of the 48 sites was broken, but nearly every one carried a backlog of small issues that, together, cap performance.",
  "What has changed is the stakes: AI crawlers are far less forgiving than Google of messy markup, slow pages and undescribed images. A page an AI engine cannot cleanly parse is a page it will not quote, so technical hygiene has quietly become a GEO issue, not just an SEO one, part of "+L("how AI crawlers actually read your site","/blogs/how-ai-crawlers-index-your-site")+"."))
out.append(chart("payTech",240,"Figure 6, the recurring technical issues, ranked by how many of the 48 sites they affected. Not glamorous, but cheap to fix, and they compound."))
out.append(callout("The AI-readability rule of thumb",[
 "If a busy human skimming on a phone can find the answer to a buyer question in five seconds, an AI engine can lift it. Put a short, direct answer near the top of every buyer page, keep the "+L("markup clean and schema-marked","/blogs/schema-markup-ai-citations-2026")+", describe every image, and you have simultaneously served Google, the AI engines and the reader, the same shape as "+L("any high-citation page","/blogs/anatomy-of-a-high-citation-page")+".",
]))

# FINDING 4
out.append(sec("06","geo","Which pages do AI engines actually cite?","Your free guides, almost never your buyer pages. AI engines already cite payments brands heavily, in 46% of audits they were quoting the company's definitions and explainers, not its product pages.",
  "So the brand shows up when someone asks \"what is DPO?\" and vanishes when someone asks \"what's the best AP automation tool?\". This is the most encouraging finding in the dataset: the problem is not presence, it is what gets cited, and that is fixable."))
out.append(chart("payEngines",250,"Figure 7, where the citations came from across all 48 audits. Google's AI Mode and AI Overviews, plus Grok, were by far the heaviest citers, a reminder that \"AI search\" and \"Google\" are converging, not diverging."))
out.append(table("Citations by engine, read",["AI engine","Citations (all 48 audits)","Read"],[
 ("Google AI Mode","1,874","The new front door to Google, highest citer in the set."),
 ("Grok","1,588","Surprisingly active; rewards fresh, clear content."),
 ("Google AI Overviews","1,584","Confirms: winning Google and winning AI are the same job."),
 ("ChatGPT","986","The assistant buyers name most in conversation."),
 ("Perplexity","752","Research-heavy buyers live here; loves citable sources."),
 ("Copilot","349","Enterprise and Microsoft-shop reach."),
 ("Gemini","278","Growing; tied to Google's wider ecosystem."),
], cls=lambda j,c:"label" if j==0 else ("up" if j==1 else "")))
out.append(p("The engine mix matters for where you focus, and each assistant "+L("weighs sources a little differently","/blogs/why-engines-recommend-different-vendors")+", but "+L("Google's AI Mode and AI Overviews","/blogs/ai-mode-vs-ai-overviews")+" dominate this category. Optimising your buyer pages to be cleanly quotable pays off across all of them at once."))
out.append(h3("The move: redirect the engine you already have"))
out.append(p("You do not need a new content machine. You need to aim the one that already ranks and already gets cited. Build buyer \"hub\" pages, for the category term, the key use cases, and head-to-head comparisons, write a short quotable answer at the top of each, and interlink your popular guides into them so both authority and readers flow toward the pages that convert."))
out.append(pipeline([("Pages that earn attention","guides, definitions, free calculators"),("Make them quotable + interlink","answer-first opener, route the authority"),("Pages that close","category hub, use-case and comparison pages")],2,
  "Figure 8, the GEO play in three steps: take the pages that already earn attention and route it to the pages that close."))

# FINDING 5
out.append(sec("07","authority","Is your authority gap really a directory-and-data gap?","Mostly, yes. The link gap in this category was rarely exotic, it came down to missing review-directory profiles and a shortage of original, linkable data.",
  "In 90% of audits the company was missing at least one of the major software directories, G2, Capterra, GetApp, or the analyst listing buyers weight most, Gartner Peer Insights (absent in 35% of cases). These are among the highest-trust pages in the whole category, they are frequently cited by AI engines, and most of them you can simply claim."))
out.append(table("The content and authority gaps that repeated across the 48 companies",["Authority lever","Sites with the gap","Effort","Payoff"],[
 ("Claim software directories (G2, Capterra, GetApp)","90%","Low, self-serve","High: trust + AI citations"),
 ("Get listed on Gartner Peer Insights","35%","Low-medium","High: the listing buyers trust most"),
 ("Publish one original data report","98%","Medium-high","Compounding links + citations"),
 ("Add comparison / \"vs\" pages","69%","Medium","Captures bottom-of-funnel buyers"),
], cls=lambda j,c:"label" if j==0 else ("up" if j==3 else "")))
out.append(p("The second lever showed up in 98% of audits: the chance to publish one original data report. Payments companies sit on genuinely unique data, how businesses spend, pay, get paid and manage cash. A single credible annual report (\"how mid-market finance teams pay in 2026\") earns links from finance media, gives AI engines a fresh source to cite, and lifts Google rankings, all at once. It is the rare marketing task that is both high-impact and self-serve, and it is exactly the kind of earned coverage that "+L("the directories and analyst reports AI trusts","/blogs/why-ai-cites-reddit-g2-analysts")+" are built from, the same logic as "+L("seeding authority the engines already read","/blogs/authority-seeding-ai-llm-trust")+"."))

# THE PLAN
out.append(sec("08","plan","What's the 90-day operating system?","One sequenced plan, run as three parallel tracks: fix what leaks, aim content at buyers, then earn the trust that makes it stick.",
  "The order is deliberate, fix the leaks first so nothing you build later drains away, then aim your content at buyers, then earn the authority that makes it all compound. Because most companies start from a healthy-but-unfocused base, the first month is light on repairs and heavy on the buyer hub."))
out.append(table("The first 90 days",["Window","Focus","Concrete moves"],[
 ("Month 1","Tidy up + start the buyer hub","Fix broken pages, review noindex tags, resolve canonical mix-ups; add alt text and security headers, compress images, set image dimensions; build strong pages for your core category term and top use cases."),
 ("Months 1-2","Move page two to page one","Strengthen category pages with clear answers, proof and internal links; add a short quotable answer near the top of every buyer page; route high-traffic guides to the buyer pages so learner visits become pipeline."),
 ("Months 2-3","Build trust + a moat","Claim G2, Capterra and GetApp and get onto Gartner Peer Insights; publish one original data report and pitch it to finance media; add comparison pages, then re-measure at day 90."),
], cls=lambda j,c:"label" if j==0 else ""))

# PRIORITISE
out.append(sec("09","prioritise","Where should you spend the quarter?","On the top-left quadrant, high impact, low effort: category hub pages, claimed directories, and the quick technical wins that make everything else quotable.",
  "If you can only do a few things, spend the effort where impact is highest and effort is lowest. The pattern across all 48 companies points to the same place."))
out.append(callout("Five things to do this quarter",[
 "1. Route your learner traffic to buyer pages, stop the leak.",
 "2. Pick one low-difficulty category term and move it from page two to page one.",
 "3. Add a short, quotable answer to the top of every buyer page.",
 "4. Claim G2, Capterra, GetApp and Gartner Peer Insights.",
 "5. Ship one original data report from your own payments data.",
]))

# KEEP SCORE
out.append(sec("10","measure","What should you actually measure?","Not traffic, most of it is learners. Track category rankings, the buyer-versus-learner mix, AI citations of buyer pages, listings live, and new referring domains.",
  "The metrics below track whether you are winning the buyers and the AI answers, which is what the plan is really for. Set a baseline now and re-check every 90 days."))
out.append(table("The payments marketing scorecard",["Metric","What it really measures","Cadence"],[
 ("Rank for your core category terms","Progress out of the Page-2 Trap","Monthly"),
 ("Share of buyer vs learner traffic","Whether your traffic can convert","Quarterly"),
 ("AI citations of buyer/product pages","GEO progress, named as the tool, not the guide","Quarterly"),
 ("Directory & analyst listings live","Trust signals buyers and AI weigh most","Quarterly"),
 ("New referring domains from target sites","Authority you are actually earning","Monthly"),
 ("Assisted conversions from content","The bottom line: does discovery drive pipeline?","Monthly"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("The AI-citation number deserves special mention: it is simply the share of your buyer questions on which the assistants name you, measured on a fixed set of prompts and "+L("re-run on a schedule","/blogs/prompt-to-citation-tracking")+". Today, for almost every payments brand, that number sits on your guides, not your buyer pages. The brands that start measuring and moving it now will define the default answers their whole market reads."))

# TAKEAWAY
out.append(sec("11","takeaway","Why is the category winnable?","Because authority is clustered, almost everyone sits in the same band. What separates the brands that win their category from the ones stuck on page two is aim, not budget.",
  "Success in payments marketing is not reserved for the biggest budgets or the highest-authority domains. What separates the winners is the discipline to point existing traffic and authority at the buyers who are ready to act, in both places they now decide."))
out.append(pull("In a category where the buyer now discovers you twice, pointing the traffic and authority you already have at the buyers ready to act is the whole game."))
out.append(p("Fix the leaks, build the buyer hub, and earn the trust signals that Google and the AI engines both reward. Do those three things in order and the same work pays off twice, once in classic search, once in the AI answer. The same pattern shows up in every category we audit, "+L("ranking is not the same as visibility","/blogs/ranking-isnt-visibility")+", and payments is no exception."))

FAQ=[
 ("How has getting found in payments changed in 2026?","Discovery has doubled. For a decade it meant ranking on Google; now buyers run the same question through Google and an AI assistant (ChatGPT, Perplexity, Gemini, Copilot or Grok) at once. Both return an answer, and your brand is either inside the AI's synthesised answer or invisible, no matter how well you rank underneath. Because both systems reward the same signals, clear content, technical cleanliness and third-party trust, the work compounds: fixing your site for AI usually fixes it for Google too."),
 ("What is the Page-2 Trap in payments marketing?","It is the near-universal pattern where a company ranks #1 for its own brand name and one narrow niche term, but sits on page two or three for the broad category terms buyers actually compare on, like \"spend management\" or \"AP automation\". 71% of the 48 audited companies showed this signature. It is the good kind of problem: ranking #21 means Google already trusts the page, so moving from page two to page one is far easier than starting from nothing, and every audit had at least one low-difficulty category term within reach."),
 ("Why do AI engines cite our guides but not our product pages?","Because your guides are the pages written to answer a question cleanly, and buyer pages usually are not. In 46% of audits, AI engines quoted the company's free definitions and explainers, almost never its product pages, so the brand appears for \"what is DPO?\" and vanishes for \"what's the best AP tool?\". The fix is not more content: add a short, quotable answer at the top of each buyer page, keep the markup clean, and interlink your popular guides into the hub pages so both authority and readers flow to the pages that convert."),
 ("What should a payments marketer fix first?","Fix the leaks, then aim at buyers. In month one, repair broken pages and canonical or noindex mix-ups, add the missing security headers, compress images and set their dimensions, then start a buyer hub for your core category term. Only after the site is clean and aimed should you invest in the slower earned-media work, claiming G2, Capterra, GetApp and Gartner Peer Insights, and publishing one original data report, that wins durable AI citations."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Data source: an aggregate analysis of GEO + SEO audits of 48 digital-payments and transactions companies (website health, Google presence and AI-citation scans across the major engines), August 2026. Brand names are used illustratively and no company is ranked or endorsed.</p></div>')

body="\n".join(out)

SIDEBAR=[("48","Payments companies audited"),("71%","Strong on brand, weak on the category"),("7,411","AI citations logged across the set")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#shift"><span class="toc-num">01</span>Discovery doubled</a></li>'
     '<li><a href="#dataset"><span class="toc-num">02</span>About the 48 audits</a></li>'
     '<li><a href="#wrong-traffic"><span class="toc-num">03</span>The wrong traffic</a></li>'
     '<li><a href="#page-2-trap"><span class="toc-num">04</span>The Page-2 Trap</a></li>'
     '<li><a href="#technical"><span class="toc-num">05</span>The silent AI tax</a></li>'
     '<li><a href="#geo"><span class="toc-num">06</span>Cited for the wrong pages</a></li>'
     '<li><a href="#authority"><span class="toc-num">07</span>The authority gap</a></li>'
     '<li><a href="#plan"><span class="toc-num">08</span>The 90-day plan</a></li>'
     '<li><a href="#prioritise"><span class="toc-num">09</span>Where to spend the quarter</a></li>'
     '<li><a href="#measure"><span class="toc-num">10</span>What to measure</a></li>'
     '<li><a href="#takeaway"><span class="toc-num">11</span>Why it is winnable</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - payments GEO & SEO playbook - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["payments marketing","fintech marketing","GEO","AI visibility","SEO","AI citations","spend management","AP automation","corporate cards","B2B SaaS"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Getting Found on Google and AI: The Payments Playbook &middot; rawmktg."
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
 f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en-IN" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n  <meta property=\"og:image:width\" content=\"2400\" />\n  <meta property=\"og:image:height\" content=\"1260\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{H.escape(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  {jb(blog)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/blogs/{SLUG}.md\" />\n  "+FONTS+"\n  ")

CHARTS=r"""
<!-- Chart.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
(function(){
  if(typeof Chart==='undefined') return;
  var css=getComputedStyle(document.documentElement);
  var signal=(css.getPropertyValue('--signal')||'#D04A2A').trim();
  var faint=(css.getPropertyValue('--faint')||'#C5BFB4').trim();
  var up=(css.getPropertyValue('--up')||'#3E9B6A').trim();
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.4);

  var au=document.getElementById('payAuthority');
  if(au){new Chart(au,{type:'bar',data:{labels:['DR <35','35-45','45-55','55-65','DR >65'],datasets:[{data:[4,14,18,9,3],backgroundColor:[neutral,signal,signal,rgba(signal,0.6),neutral],borderRadius:4,barThickness:38}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' of 48 companies';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,max:22,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var it=document.getElementById('payIntent');
  if(it){var cp={id:'cI',afterDatasetsDraw:function(ch){var a=ch.chartArea;if(!a)return;var ctx=ch.ctx,x=(a.left+a.right)/2,y=(a.top+a.bottom)/2;ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=up;ctx.font='700 30px '+mono;ctx.fillText('~38%',x,y-7);ctx.fillStyle=text;ctx.font='9px '+mono;ctx.fillText('buyer intent',x,y+15);ctx.restore();}};
    new Chart(it,{type:'doughnut',data:{labels:['Learner / informational 62%','Buyer / commercial 38%'],datasets:[{data:[62,38],backgroundColor:[neutral,up],borderColor:'#1A1815',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'66%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:10},boxWidth:10,boxHeight:10,padding:12}},tooltip:{callbacks:{label:function(c){return ' '+c.label;}}}}},plugins:[cp]});}

  var tc=document.getElementById('payTech');
  if(tc){var tl=['Security headers','Slow pages','Heavy images','Title tags','No image size','Broken links','Missing alt','Dense text'];var tv=[83,77,73,54,54,48,42,38];
    new Chart(tc,{type:'bar',data:{labels:tl,datasets:[{data:tv,backgroundColor:tv.map(function(v){return v>=70?signal:v>=50?rgba(signal,0.6):neutral;}),borderRadius:4,barThickness:18}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of 48 sites';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var en=document.getElementById('payEngines');
  if(en){var el=['Google AI Mode','Grok','Google AI Overviews','ChatGPT','Perplexity','Copilot','Gemini'];var ev=[1874,1588,1584,986,752,349,278];
    var ec=[signal,signal,signal,rgba(signal,0.7),rgba(signal,0.55),neutral,neutral];
    new Chart(en,{type:'bar',data:{labels:el,datasets:[{data:ev,backgroundColor:ec,borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.toLocaleString()+' citations';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v>=1000?(v/1000)+'k':v;}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">GEO &amp; SEO Teardown &middot; Payments &amp; Fintech</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/pay_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/pay_cb.js"],capture_output=True,text=True)
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),
 "| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| statgrid:",hh.count('class="stat-grid"'),"| h2:",hh.count("<h2"))
