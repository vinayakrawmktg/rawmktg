#!/usr/bin/env python3
"""SCRATCH: build blogs/property-vista-authority-paradox.html (native figures). Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="property-vista-authority-paradox"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"
PUB="2026-06-11"

def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'")
        .replace("“",'"').replace("”",'"').replace("…","...").replace(" "," "))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)

# ---- scaffold from the (native) Noterro article ----
T=open("blogs/noterro-ai-search-teardown.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")          # carries all native figure CSS (chart-wrap, donut, compare-grid, tt, code, callout, pull-quote)
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
CHARTJS_SRC='<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>'

GA=('<!-- Google tag (gtag.js) -->\n  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
    "gtag('js',new Date());gtag('config','G-4B3LL6MJKN');"
    "(function(){function l(){if(window.__gaLd)return;window.__gaLd=1;"
    "var s=document.createElement('script');s.async=1;"
    "s.src='https://www.googletagmanager.com/gtag/js?id=G-4B3LL6MJKN';"
    "document.head.appendChild(s);}"
    "if(document.readyState==='complete')l();else window.addEventListener('load',l);"
    "setTimeout(l,3000);})();</script>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'

# ---- renderers ----
def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest):
    cap=f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>'
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def code(label,body,lang=None):
    lng=f'<span class="code-lang">{esc(lang)}</span>' if lang else ''
    return (f'<div class="code-wrap"><div class="code-label">{esc(label)}</div>'
            f'<div class="code-block">{lng}<pre>{H.escape(norm(body))}</pre></div></div>')
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers)
    body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            klass=cls(j,c) if cls else ""
            attr=(' class="'+klass+'"') if klass else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return (f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div>'
            f'<table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')
def chart(cid,height,caption):
    return (f'<div class="chart-wrap"><canvas id="{cid}" height="{height}"></canvas></div>'
            f'<div class="chart-caption">{esc(caption)}</div>')
def donut(cid,pct,lbl,pctcolor,caption):
    return (f'<div class="chart-wrap"><div class="donut-box"><canvas id="{cid}" height="240"></canvas>'
            f'<div class="donut-center"><span class="donut-pct" style="color:{pctcolor}">{esc(pct)}</span>'
            f'<span class="donut-lbl">{esc(lbl)}</span></div></div></div>'
            f'<div class="chart-caption">{esc(caption)}</div>')
def compare(left_label,left_items,right_label,right_items,caption):
    li="".join(f"<li>{esc(x)}</li>" for x in left_items)
    ri="".join(f"<li>{esc(x)}</li>" for x in right_items)
    return (f'<div class="compare-grid">'
            f'<div class="compare-col"><div class="compare-col-label seo">{esc(left_label)}</div><ul>{li}</ul></div>'
            f'<div class="compare-col"><div class="compare-col-label geo">{esc(right_label)}</div><ul>{ri}</ul></div>'
            f'</div><div class="chart-caption">{esc(caption)}</div>')
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras)
    return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'

# ---- content ----
HEADLINE="The Authority Paradox"
DECK="How a DR-63 brand with G2, Gartner and Crunchbase backlinks became nearly invisible on ChatGPT and Perplexity."
DESC=("A single-brand GEO teardown of Property Vista, a DR-63 multifamily proptech brand with strong backlinks, "
      "rich schema and clean technical hygiene that is nearly invisible on ChatGPT and Perplexity. The cause: a "
      "JavaScript bot wall that serves every AI crawler a challenge page instead of content.")
DATANOTE=("Data: Ahrefs Site Explorer and Brand Radar, plus direct technical inspection of propertyvista.com, "
          "captured June 2026. Figures are estimates; example code is illustrative.")

out=[]
out.append(p("Property Vista has the backlinks, the schema, and the brand authority to dominate AI search in multifamily proptech. It shows up on almost none of it. Here is what is working, what is quietly breaking, and the one lesson every B2B brand should take to heart."))
out.append(callout("The teardown in 30 seconds",[
 "<strong>Strong foundation:</strong> DR 63, roughly 1,200 referring domains, profiles on G2, Gartner and Crunchbase, and a clean structured-data graph.",
 "<strong>Near-zero payoff:</strong> 80 organic keywords, zero citations on ChatGPT and Perplexity, organic traffic down 53% in a year.",
 "<strong>The culprit:</strong> a JavaScript bot-protection wall that serves every AI crawler a challenge page instead of content.",
 "<strong>The lesson:</strong> authority you block is authority you waste. In the AI era, crawlability is the whole game.",
]))
out.append(p("Property Vista is enterprise multifamily property-management software, big in Canada and growing in the US. On paper it is a healthy, established brand: the kind of domain that should be the default answer when a property operator asks an AI assistant which software to use to run their buildings. It isn't. And the reason it isn't is so common, and so fixable, that it makes Property Vista a near-perfect teaching case. Nearly everything most teams obsess over, links, schema, site structure, is already done. The one thing almost nobody checks is the thing quietly undoing all of it. We pulled the data from Ahrefs and inspected the live site. Here is the autopsy."))

# 01 wins
out.append(sec("01","wins","What does Property Vista get right?","More than most - the foundation is genuinely strong.",
 "Let us start with the wins, because there are real ones, and they are the reason the gaps sting. Property Vista is not just linked from anywhere; it is linked from the exact places AI engines trust when they answer questions about software."))
out.append(table("High-authority referring domains",["Source","Authority","Why it matters for AI"],[
 ("Gartner","DR 92","Category authority models lean on"),
 ("Crunchbase","DR 91","Entity record, cited since 2018"),
 ("G2","DR 91","The review site AI trusts on “which tool” questions"),
 ("TrustRadius","DR 84","Software reviews and ratings"),
 ("BetaKit","DR 77","Canadian tech press, news-grade signal"),
], cls=lambda j,c: "label" if j==0 else ("up" if j==1 else "")))
out.append(p("That is the strongest part of the story. When ChatGPT or Perplexity assembles an answer about property-management tools, these are the sources it leans on, and Property Vista already has a seat at every one of those tables. The rest of the foundation is just as sound. The homepage ships a well-formed JSON-LD graph (Organization, WebSite, WebPage, Person and Article), which is more than most B2B sites bother with and is the layer that lets a machine read the page as an entity rather than a blob of text. The technical hygiene is clean across the board."))
out.append(table("Technical hygiene audit, propertyvista.com",["Element","Status","Detail"],[
 ("H1 structure","PASS","Exactly one H1"),
 ("Canonical","PASS","Self-referencing"),
 ("XML sitemap","PASS","Valid index with 3 child maps"),
 ("HTTPS / viewport","PASS","Served securely, mobile-ready"),
 ("JSON-LD graph","PASS","Org, WebSite, WebPage, Person, Article"),
], cls=lambda j,c: "up" if (j==1 and c=="PASS") else ("label" if j==0 else "")))
out.append(p("Geography is disciplined too: traffic splits cleanly, roughly 47% Canada and 42% US, with the rest noise. No scattered international dilution. The brand knows who it is for. Put those four together, a citation-grade backlink profile, a real structured-data foundation, clean technical hygiene, and disciplined geography, and you have a domain with genuine authority and a clean technical base. Which is exactly why what comes next is so frustrating."))
out.append(pull("Property Vista did the expensive work. Then it locked the doors on the cheap mistake."))

# 02 the wall
out.append(sec("02","wall","So why is it nearly invisible in AI search?","One JavaScript bot wall blocks every AI crawler.",
 "Every page on propertyvista.com sits behind a custom JavaScript bot-protection challenge. Request the site without running JavaScript in a real browser and you get an interstitial that reads “verifying your request” and a reload loop, not content."))
out.append(p("We tested it with the real user agents of the crawlers that matter. Every one of them bounced, and not one received real HTML."))
out.append(code("Crawler access test","""$ curl -A "GPTBot/1.2" https://propertyvista.com/
< HTTP/1.1 415 Unsupported Media Type
< (JavaScript challenge interstitial - not page content)""","bash"))
out.append(table("What the AI crawlers actually get",["Crawler","HTTP response","Gets real HTML?"],[
 ("GPTBot (OpenAI)","415 / challenge","No"),
 ("OAI-SearchBot","challenge","No"),
 ("PerplexityBot","503","No"),
 ("ClaudeBot (Anthropic)","503","No"),
 ("Google-Extended","503","No"),
 ("Googlebot","503","No"),
 ("Bingbot","503","No"),
], cls=lambda j,c: "label" if j==0 else ("neg" if (j==2 and c=="No") else "")))
out.append(p("AI crawlers do not execute JavaScript; they request, read, and move on. So the rich schema, the valid sitemap, the clean structure we just praised? Invisible. The engines that would cite Property Vista literally cannot read it. Even robots.txt and the sitemap, both valid and well-formed, are served the challenge page to a non-JS crawler instead of the file itself. The map to the building is locked inside the building."))

# 03 citation concentration
out.append(sec("03","citations","Where do its AI citations actually come from?","Almost entirely Grok - 13 of 15 tracked citations.",
 "Look at where Property Vista's AI citations actually come from."))
out.append(chart("pvCitationsChart",300,"AI citations by platform - one engine carries the brand, the rest sit at zero - Source: Ahrefs Brand Radar, June 2026"))
out.append(p("Of 15 tracked citations, 13 are on Grok, which leans heavily on real-time X data and third-party mentions, so it can cite a brand without crawling its site. That is exactly why it still works here. The engines that must fetch and read the live page, ChatGPT and Perplexity, return nothing. Worse, the trend is negative nearly everywhere: AI Overviews down 3, ChatGPT down 2, AI Mode down 1. The one number propping up the brand's AI presence is the one it controls least."))

# 04 branded trap
out.append(sec("04","branded","Is Property Vista ranking for anything but its own name?","Barely - about 89% of its traffic is branded.",
 "Now look at what Property Vista actually ranks for."))
out.append(donut("pvBrandedChart","89%","branded / navigational","var(--signal)",
 "Share of organic traffic by query intent - branded: property vista, my vista, yieldstar login, tenantsure"))
out.append(p("Roughly 89% of organic traffic comes from branded or navigational queries, property vista, my vista, yieldstar login, tenantsure. The non-branded category demand (multifamily lead management, rent-payment letters) is a thin sliver. This matters enormously for AI visibility, because engines cite brands for category questions only when those brands rank for category questions. Property Vista owns its own name and very little else, so when a buyer asks an AI for the best multifamily management software, there is nothing of its own to surface."))

# 05 slow bleed
out.append(sec("05","bleed","Why is traffic sliding while authority holds?","That gap is the classic fingerprint of a crawl problem.",
 "All of this shows up in the trendline."))
out.append(chart("pvTrafficChart",300,"Monthly organic traffic, last 12 months - down ~53% YoY (one anomalous Nov spike of 2,407 excluded) - Source: Ahrefs Site Explorer"))
out.append(p("Organic traffic fell from roughly 374 monthly visits a year ago to about 175 now, down around 53% (one anomalous November spike aside). Here is the tell: the domain's authority is flat-to-rising over the same period. Authority up, traffic down is the classic fingerprint of a crawl-and-index problem, not a link problem. The site is slowly falling out of the index because the crawlers keep hitting a wall."))

# 06 diagnosis
out.append(sec("06","diagnosis","What is the actual diagnosis?","Authority in, almost nothing out.",
 "Stack the two halves and the paradox is stark."))
out.append(compare("What they have earned",
 ["DR 63 - roughly 1,200 referring domains","Profiles on G2, Gartner, Crunchbase","Rich JSON-LD schema graph","Valid sitemap, clean H1 structure","App Store, BBB, TrustRadius links"],
 "What it converts to",
 ["80 organic keywords (mostly branded)","0 citations on ChatGPT and Perplexity","Organic traffic down 53% YoY","AI visibility riding on one engine","Category demand going to rivals"],
 "Everything earned on the left; almost nothing it converts to on the right - with the wall in between."))
out.append(p("On one side, everything a brand spends years and budget earning: DR 63, twelve hundred referring domains, profiles on the directories AI trusts, a real schema graph. On the other, what it converts to: 80 keywords, zero presence on the AI engines that matter, traffic in steady decline. The gap between them isn't a content problem or a link problem. It is an access problem. One infrastructure decision, a bot wall that doesn't tell a scraper from a search engine, neutralizes the entire investment. Property Vista isn't losing because it is weak. It is losing because it is unreadable."))
out.append(pull("An engine that can't read you can't cite you. In the AI era, that's the difference between a brand and a ghost."))

# 07 lessons
out.append(sec("07","lessons","What should every B2B brand steal from this?","Five lessons, in order of how often they get missed.",""))
out.append(p("<strong>1. Crawlability is now the whole game.</strong> In the old model, a bot wall cost you a little crawl efficiency. In the AI model, it costs you existence, an engine that can't read you can't cite you, full stop. Before you optimize a single tag, confirm that GPTBot, ClaudeBot, PerplexityBot and the search crawlers all get a 200 and real HTML. Test with their actual user agents, not your browser."))
out.append(p("<strong>2. Authority you block is authority you waste.</strong> Links and schema are necessary, not sufficient. They only pay off if a machine can reach the page they are attached to. Audit access before you audit anything else; everything downstream depends on it."))
out.append(p("<strong>3. Win the directories - AI reads them even when it can't read you.</strong> The only reason Property Vista appears anywhere in AI answers is its third-party footprint: Crunchbase, G2, Gartner. Those profiles stay crawlable when your own site isn't. Keep them complete, current and review-rich; they are your insurance policy."))
out.append(p("<strong>4. Ranking for your own name is a trap dressed as a win.</strong> Branded traffic looks great on a dashboard and does nothing for discovery. AI engines cite you on category questions, the ones buyers ask before they know your name. If 89% of your traffic is branded, you are invisible to everyone who hasn't already found you."))
out.append(p("<strong>5. Watch the gap between authority and traffic.</strong> When your Domain Rating holds or climbs while organic traffic slides, stop blaming content and start checking access and indexation. A widening gap is an early-warning light most teams never look at."))

# 08 the fix
out.append(sec("08","fix","What is the Monday-morning fix?","Days of work, not a replatform.",
 "None of this needs a rebuild. The highest-impact moves are days of work. First, let the crawlers in: allow-list verified AI and search bots through the protection layer so they bypass the challenge, then confirm with their real user agents. Next, declare access explicitly in robots.txt."))
out.append(code("robots.txt","""User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

Sitemap: https://propertyvista.com/sitemap.xml""","robots.txt"))
out.append(p("Then add an llms.txt so engines have a curated map of what to read."))
out.append(code("llms.txt","""# Property Vista
> Multifamily property management software for Canada and the US.

## Core pages
- Platform overview: /
- Tenant screening:  /screening
- Payments:          /payments
- Pricing:           /pricing""","llms.txt"))
out.append(p("And give the page the types the category rewards, SoftwareApplication and FAQPage, so the machine knows what you are and can lift your answers cleanly."))
out.append(code("SoftwareApplication JSON-LD","""{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Property Vista",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web, iOS, Android",
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.5", "ratingCount": "120" }
}""","json"))
out.append(p("That is the entire unlock. Open the door, point to the rooms, and label the furniture."))

# 09 become the answer
out.append(sec("09","answer","How do you win AI search from here?","Stop optimizing to rank. Make sure the machines can read you.",
 "The shift underneath all of this is simple to state and hard to internalize. Search used to reward the brand that ranked. AI rewards the brand that gets quoted."))
out.append(p("You don't win by being the best ad on the results page anymore; you win by being the answer the model gives before any page loads. Property Vista has everything it needs to be that answer in multifamily proptech: the authority, the relationships, the structure. It is all sitting behind a door it accidentally locked. The brands that win the next few years won't necessarily be the ones with the most links or the biggest budgets. They will be the ones that made absolutely sure the machines could read them. Open the door."))

# FAQ
FAQ=[
 ("Why is Property Vista nearly invisible on ChatGPT and Perplexity despite strong authority?","Because every page on propertyvista.com sits behind a JavaScript bot-protection challenge. AI crawlers like GPTBot, PerplexityBot and ClaudeBot do not execute JavaScript, so they receive a challenge or error page (HTTP 415 or 503) instead of real HTML. The site's strong backlinks, rich JSON-LD schema and valid sitemap are all invisible to the engines because the engines literally cannot read the page. An engine that can't read you can't cite you."),
 ("What is the authority paradox in AI search?","It is the gap between authority earned and authority converted. Property Vista has a Domain Rating of 63, around 1,200 referring domains, and profiles on G2, Gartner and Crunchbase, yet it ranks for only about 80 keywords, has zero citations on ChatGPT and Perplexity, and has lost roughly 53% of its organic traffic in a year. Authority holding flat or rising while traffic falls is the classic fingerprint of a crawl-and-index problem, not a content or link problem."),
 ("How do you make a site readable to AI crawlers?","Allow-list verified AI and search bots through any bot-protection layer so they bypass JavaScript challenges, then confirm with their real user agents that they receive a 200 and real HTML. Declare access explicitly in robots.txt, publish an llms.txt that maps your key pages, and add SoftwareApplication and FAQPage schema so engines know what you are and can lift your answers. These are days of work, not a replatform."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Data source: Ahrefs (organic keywords, referring domains, Brand Radar AI citations) and a direct technical inspection of propertyvista.com, captured June 2026.</p></div>')

body="\n".join(out)

# interlinks (within <main> only - body is main content here)
LINKS=[
 ("AI crawlers do not execute JavaScript","/blogs/how-ai-crawlers-index-your-site"),
 ("a well-formed JSON-LD graph","/blogs/schema-markup-ai-citations-2026"),
 ("the directories AI trusts","/blogs/authority-seeding-ai-llm-trust"),
 ("engines cite brands for category questions","/blogs/topical-authority-cluster-ai-shortlists"),
 ("add an llms.txt","/glossary/llms-txt"),
 ("the brand that gets quoted","/blogs/why-engines-recommend-different-vendors"),
]
for ph,u in LINKS:
    np=norm(ph)
    if np in body: body=body.replace(np,f'<a href="{u}">{np}</a>',1)
    else: print("LINK MISS:",ph)

# sidebar
SIDEBAR=[("DR 63","Domain Rating, top-tier authority"),("3/7","AI engines citing Property Vista"),("89%","Of traffic is its own brand name")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#wins"><span class="toc-num">01</span>What it gets right</a></li>'
     '<li><a href="#wall"><span class="toc-num">02</span>The bot wall</a></li>'
     '<li><a href="#citations"><span class="toc-num">03</span>Citation concentration</a></li>'
     '<li><a href="#branded"><span class="toc-num">04</span>The branded trap</a></li>'
     '<li><a href="#diagnosis"><span class="toc-num">05</span>The diagnosis</a></li>'
     '<li><a href="#fix"><span class="toc-num">06</span>The Monday-morning fix</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div>'
              f'<div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=(f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." '
            f'class="article-header-img" width="2400" height="1260" loading="eager">')

# schema
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),
 "image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,
 "author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},
 "mainEntityOfPage":{"@type":"WebPage","@id":URL},
 "keywords":["Property Vista","AI search","GEO","AI citations","bot wall","crawlability","llms.txt","schema","structured data","multifamily proptech","property management software","Ahrefs Brand Radar"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
 {"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
personLD={"@context":"https://schema.org",**person}

hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;'
      'clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean '
      f'Markdown version of this page is available at {URL}.md. Optimized for AI and LLM tools.</div>')
TITLE="The Authority Paradox &middot; Property Vista GEO Teardown &middot; rawmktg."
da=escq(DESC)
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
 "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n"
 "  <meta name=\"robots\" content=\"index, follow\" />\n"
 f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
 f"  <meta name=\"description\" content=\"{da}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
 "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
 "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
 f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  <meta property=\"article:published_time\" content=\"{PUB}T00:00:00Z\" />\n"
 f"  <meta property=\"article:modified_time\" content=\"{PUB}T00:00:00Z\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{H.escape(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  {jb(blog)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/blogs/{SLUG}.md\" />\n  "+FONTS+"\n  ")

CHARTS="""
<!-- Chart.js -->
"""+CHARTJS_SRC+"""
<script>
(function(){
  if(typeof Chart==='undefined') return;
  var signal='#D04A2A', up='#3E9B6A', mono="'JetBrains Mono', monospace";
  var text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.07)';

  var bar=document.getElementById('pvCitationsChart');
  if(bar){
    new Chart(bar,{type:'bar',
      data:{labels:['Grok (xAI)','Gemini','Google AI Overviews','ChatGPT','Perplexity','Microsoft Copilot','Google AI Mode'],
        datasets:[{data:[13,1,1,0,0,0,0],
          backgroundColor:[up,'rgba(255,255,255,0.55)','rgba(255,255,255,0.55)',signal,signal,signal,signal],
          borderRadius:4,barThickness:18,minBarLength:3}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' citations';}}}},
        scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},
                y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});
  }

  var dn=document.getElementById('pvBrandedChart');
  if(dn){
    new Chart(dn,{type:'doughnut',
      data:{labels:['Branded / navigational','Non-branded category demand'],
        datasets:[{data:[89,11],backgroundColor:[signal,up],borderColor:'#1A1815',borderWidth:3}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:'70%',
        plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:10},boxWidth:10,boxHeight:10,padding:14}},
          tooltip:{callbacks:{label:function(c){return ' '+c.label+': '+c.raw+'%';}}}}}});
  }

  var ln=document.getElementById('pvTrafficChart');
  if(ln){
    new Chart(ln,{type:'line',
      data:{labels:['Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun'],
        datasets:[{data:[374,327,323,310,270,285,307,228,252,264,264,208,175],
          borderColor:'#2FB6A8',backgroundColor:'rgba(47,182,168,0.12)',fill:true,tension:0.35,
          borderWidth:2,pointRadius:3,pointBackgroundColor:'#2FB6A8',pointBorderColor:'#2FB6A8'}]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' visits/mo';}}}},
        scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},
                y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});
  }
})();
</script>"""

tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">GEO Teardown &middot; Multifamily Proptech</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">June 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")

final=head+STYLE+"\n  "+ADSENSE+tail
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(final)
hh=open(f"blogs/{SLUG}.html").read()
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
      "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),
      "| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count("code-block")-0,
      "| compare:",hh.count('class="compare-grid"'),"| callout:",hh.count('class="callout-box"'))
