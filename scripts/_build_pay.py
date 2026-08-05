#!/usr/bin/env python3
"""SCRATCH: build blogs/why-ai-cites-razorpay-over-airpay.html. Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="why-ai-cites-razorpay-over-airpay"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-13"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," "))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/why-ai-cites-domo-over-databricks.html",encoding="utf-8").read()
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

HEADLINE="Why AI Cites Razorpay Over Airpay"
DECK="The visibility gap deciding which payment brands AI assistants surface when buyers ask, a six-brand teardown of India's payment-gateway market."
DESC=("A GEO and SEO teardown of India's payment-gateway market: why Razorpay and Stripe each win ~21% of AI answers while "
      "Airpay sits at 3%. The two discovery tracks, the answer-shaped content engine behind the leaders, the 94%-spam backlink "
      "trap, the crawl faults that gate visibility, and the flywheel that widens the gap.")
DATANOTE=("A neutral, data-led teardown of AI and search visibility in India's payment-gateway market, using Airpay as a "
          "mid-market lens against six leaders. Based on a scan of 40 buyer prompts across four AI engines (ChatGPT, Google "
          "AI Overviews, Claude, Gemini) plus organic-keyword, content-gap, backlink and technical-crawl data, June 2026. "
          "Figures are estimates and describe this data set, not the entire market.")

out=[]
out.append('<p class="lead">'+norm("For most of the internet's history, getting found meant ranking on Google. That game still matters. But a second game has begun, and it is reshaping how buyers in India choose a payment gateway: many no longer scroll ten blue links, they ask an assistant. ChatGPT, a Google AI Overview, Gemini or Claude replies with a short answer that names a few brands. If a brand sits inside that answer it makes the shortlist; if not, it is invisible, no matter how good the product is.")+'</p>')
out.append(p("To see how this plays out in payments, we used one mid-market Indian gateway, Airpay, as a lens, and compared it against the market leaders across 40 common buyer questions on four AI engines, alongside search, content and link data from June 2026. The patterns are not unique to one company; they describe the whole market."))

# 01
out.append(sec("01","changing","Why is getting found changing?","A second discovery game, the AI answer, now decides who makes the shortlist.",
  "Today many buyers do not compare ten links, they ask an assistant, which replies with a short answer naming three to five brands. Being left out of that handful is far more costly than ranking a little lower on Google."))

# 02
out.append(sec("02","two-paths","How do buyers discover a payment gateway now?","Two tracks: the search journey, and the AI answer that hands back a shortlist.",
  "Discovery runs on two tracks at once. The older track is the familiar search journey, where the buyer does the comparing. The newer track is the AI answer, where the assistant does the comparing and names fewer brands."))
out.append(pipeline([("Buyer query","types a question"),("Many links","Google shows ten"),("Clicks several","opens tabs"),("Compares","does the work"),("Chooses","picks one")],-1,
  "The traditional search path: the buyer compares, and a page-two brand still has a chance to be seen."))
out.append(pipeline([("Asks an assistant","one question"),("One answer","AI does the comparing"),("Names 3-5 brands","the shortlist"),("Buyer shortlists","those only")],2,
  "The AI answer path: shorter, and it names fewer brands. The shortlist is the new front page."))
out.append(callout("Why this matters",[
 "On the search path, a brand on page two still has a chance to be seen. On the AI path, the answer usually names only a handful of brands. Being left out of that handful is far more costly than ranking a little lower on Google.",
]))

# 03
out.append(sec("03","who-wins","Who wins AI answers in payments today?","Razorpay and Stripe dominate; Airpay appears in just 3% of answers.",
  "We asked four AI engines, ChatGPT, Google AI Overviews, Claude and Gemini, 40 buyer questions about payments, then counted how often each brand was named. Two names dominate."))
out.append(chart("payShare",260,"Figure 1 - share of AI answers by brand, across four engines. Razorpay and Stripe each appear in ~21%; Airpay in 3%. Source: 40-prompt scan, June 2026"))
out.append(p("Wix follows at 13%, helped by its website-builder audience asking about payments; EnKash and Wise sit at 6%. The picture also changes by engine: Airpay shows up a little on ChatGPT and Google AI Overviews, and not at all on Claude and Gemini, so visibility has to be earned engine by engine. Grouped into eight buyer topics, Airpay appears only for Wix and website-integration questions and is silent across the core payment topics, gateway basics, EMI, comparisons, compliance, the very topics where new buyers start."))
out.append(table("When Airpay is missing, the AI cites someone else",["Buyer question","Brands the AI named instead"],[
 ("Best payment gateway for small businesses in India?","Payoneer, Razorpay, Wise"),
 ("How much do payment gateways charge per transaction?","GoCardless, Razorpay"),
 ("How can I offer EMI payment options?","Razorpay, Innoviti, Paytm"),
 ("Which Indian gateway supports buy-now-pay-later?","Cashfree, Stripe"),
 ("Top payment gateway providers in India?","Enterslice, Razorpay"),
], cls=lambda j,c:"label" if j==0 else ""))

# 04
out.append(sec("04","content","What's the content engine behind the leaders?","Answer-shaped guide content at scale, the raw material assistants quote.",
  "Why do the same few brands keep showing up in AI answers? Because they show up in regular search first. AI engines build answers from the pages they trust, and the leaders have spent years publishing pages that answer buyer questions, the same "+L("definitional library","/blogs/internal-linking-for-ai-retrieval")+" pattern that wins citations."))
out.append(p("The leaders did not just write about their own product. They built large libraries of simple guides on topics their buyers care about, what UPI is, how to check a GST number, what a cancelled cheque looks like, how to register a business. Those pages pull in enormous monthly search volume. Comparing Airpay against six leading gateways (Razorpay, Cashfree, PayU, CCAvenue, Instamojo and Easebuzz), we found 8,940 keywords where at least one of them ranks and Airpay does not appear at all."))
out.append(chart("payVolume",240,"Figure 2 - monthly searches won by competitor guide pages that Airpay does not rank for. A sample of the 8,940-keyword content gap."))
out.append(table("The content gap, a sample",["Buyer topic","Monthly searches","A competitor that ranks"],[
 ("gst","2,190,000","Razorpay, Cashfree"),
 ("udyam registration","1,490,000","Razorpay, Cashfree"),
 ("gst search","871,000","Razorpay, Cashfree"),
 ("meesho seller","757,000","Razorpay, Easebuzz"),
 ("msme registration","285,000","Razorpay, Cashfree"),
 ("cancelled cheque","119,000","Razorpay, Easebuzz"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("The cost shows up in the traffic mix. Almost all of Airpay's search visitors arrive by typing its brand name, it captures the demand it already has but creates almost none from buyers who do not yet know it."))
out.append(donut("payBranded","Figure 3 - Airpay's search traffic is essentially all branded: 4,476 brand-name visits versus 19 non-branded."))
out.append(callout("The pattern",[
 "Leaders win AI answers because they win search. They win search because they publish answer-shaped content at scale. Airpay ranks well for its own name, but without guide content it has little for engines, or buyers, to discover.",
]))

# 05
out.append(sec("05","trust","What about trust, links and authority?","Airpay has a healthy DR 59, but 94% of its backlinks are flagged as spam.",
  "Content is only half the story. Search and AI engines also weigh trust, and one of the biggest signals is backlinks, the links other sites point at yours. Each strong link is a little like a vote of confidence."))
out.append(donut("paySpam","Figure 4 - quality of the 2,786 sites linking to Airpay: about 94% are flagged as spam, a pattern common across Indian fintech."))
out.append(p("Airpay's domain rating of 59 was built over years, yet of the 2,786 sites that link to it, about 94% are flagged as spam, junk that can erode trust rather than build it. There is opportunity in the same data: 3,411 quality sites link to Airpay's competitors but not to Airpay, each one editorial coverage, a directory listing, or a mention the leaders earned and Airpay has not. The trust gap, like the content gap, measures work the leaders did first, the engine behind "+L("off-site authority","/blogs/why-ai-cites-reddit-g2-analysts")+"."))

# 06
out.append(sec("06","mechanics","What website mechanics gate visibility?","Fixable crawl faults: missing H1s, no canonicals, broken links, no alt text.",
  "Even strong content needs a clean, readable site for engines to use it. A "+L("crawl of Airpay's site","/blogs/how-ai-crawlers-index-your-site")+" surfaced a set of common, fixable faults, typical of fast-growing sites whose technical hygiene has not kept pace."))
out.append(table("Crawl faults that gate visibility",["Site issue","Scale","What it affects"],[
 ("Pages missing a main heading (H1)","53 pages (72%)","Engines struggle to tell what the page is about"),
 ("Pages with no canonical tag","85 pages (100%)","Engines can get confused about the real page"),
 ("Broken internal links","14 links","Dead ends waste visitor and crawler trust"),
 ("Images with no description text","548 images","Lost meaning for engines and screen readers"),
 ("Security headers switched off","~1,165 pages (99%)","Weaker safety signals across the site"),
], cls=lambda j,c:"label" if j==0 else ("neg" if j==1 else "")))
out.append(p("The lesson is not that one site is broken. Visibility is a stack, content, trust and technical health all have to line up, and a weakness in any layer caps the others."))

# 07
out.append(sec("07","flywheel","What's the pattern? (the visibility flywheel)","Each layer feeds the next; the gap widens when nothing changes.",
  "Put the pieces together and a loop appears. The leaders are not winning because of one clever tactic, they are winning because each layer feeds the next and the whole thing compounds."))
out.append(pipeline([("Publish content","answer-shaped guides"),("Engines cite it","search & AI"),("Buyers discover","the brand"),("Links & mentions grow","earned coverage"),("Engines trust more","and repeat")],-1,
  "The visibility flywheel: content earns citations, citations earn discovery, discovery earns links, links earn trust, which earns more citations. A little stronger each turn."))
out.append(p("This is why the gap between leaders and challengers tends to widen, not narrow, when nothing changes. A brand that is not in the loop is not standing still, it is falling behind a flywheel that is speeding up, the same "+L("compounding effect","/blogs/geo-compounding-flywheel")+" we see across categories."))

# 08
out.append(sec("08","market","What does it mean for the market?","The shortlist is the new front page, for leaders and challengers alike.",
  "The shift to AI answers raises the stakes for everyone."))
out.append(p("<strong>For the leaders:</strong> the moat is real, but it is made of content and trust, not magic. It can be matched by anyone willing to publish at the same quality and earn the same coverage. The risk is complacency, because the AI answer rewards the brand that best answers the question, not simply the biggest name."))
out.append(p("<strong>For the challengers:</strong> brand strength alone does not convert into discovery. A challenger can own its name in search and still be missing from the buyer's shortlist. The path forward is consistent: publish answer-shaped content on the topics buyers actually ask about, keep the site clean enough for engines to read, and replace junk links with a smaller number of genuine ones."))
out.append(pull("The assistant names a short list and rarely a long one. That makes being in the answer more valuable, and being absent more expensive, than any single position on Google ever was."))
out.append(callout("Method & data",[
 "A neutral analysis, not an endorsement of any brand. AI visibility: a scan of 40 buyer prompts across four engines (ChatGPT, Google AI Overviews, Claude, Gemini), June 2026. Search: organic-keyword and content-gap exports for Airpay and six competitors. Trust: referring-domain and link-intersect exports with domain rating and spam flags. Website health: a technical crawl of Airpay's site. Figures are rounded; percentages describe this data set rather than the entire market.",
]))

FAQ=[
 ("Why does AI cite Razorpay over Airpay?","Because Razorpay shows up in regular search first, and AI engines build answers from the pages they trust. Razorpay has spent years publishing answer-shaped guide content (UPI, GST, business registration) that wins enormous search volume, while Airpay has almost none. Razorpay appears in ~21% of AI answers across four engines; Airpay in 3%, a roughly 7x gap. It is a content and trust gap, not a product gap."),
 ("What is 'share of AI answers'?","It is how often a brand is named when an AI assistant answers a buyer's question. In this scan of 40 payment prompts across ChatGPT, Google AI Overviews, Claude and Gemini, Razorpay and Stripe each appeared in about 21% of answers, Wix in 13%, EnKash and Wise in 6%, and Airpay in 3%. Because assistants name only three to five brands, share of answers decides who makes the shortlist."),
 ("Can a challenger payment brand catch up?","Yes, but only by closing the same gaps the leaders closed first. Publish answer-shaped guide content on the core topics buyers ask about (not just product pages), fix the technical faults that stop engines reading the site (missing H1s, no canonicals, broken links), and replace spam backlinks with a smaller number of genuine, editorial ones. Brand strength alone does not convert into AI discovery."),
 ("Do backlinks still matter for AI visibility?","Yes. Trust is a major input, and backlinks are one of the biggest trust signals. But quality matters more than volume: Airpay has 2,786 referring domains yet about 94% are flagged as spam, which can erode trust rather than build it. Meanwhile 3,411 quality sites link to its competitors and not to Airpay, the editorial coverage the leaders earned and it has not."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Data source: a scan of 40 buyer prompts across ChatGPT, Google AI Overviews, Claude and Gemini, plus organic-keyword, content-gap, referring-domain and technical-crawl data for Airpay and six competitors, captured June 2026.</p></div>')

body="\n".join(out)

SIDEBAR=[("6","Payment SaaS brands torn down"),("3%","Airpay share of AI answers"),("7x","Leader citation advantage vs Airpay")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#changing"><span class="toc-num">01</span>Getting found is changing</a></li>'
     '<li><a href="#two-paths"><span class="toc-num">02</span>Two discovery paths</a></li>'
     '<li><a href="#who-wins"><span class="toc-num">03</span>Who wins AI answers</a></li>'
     '<li><a href="#content"><span class="toc-num">04</span>The content engine</a></li>'
     '<li><a href="#trust"><span class="toc-num">05</span>Trust, links & authority</a></li>'
     '<li><a href="#mechanics"><span class="toc-num">06</span>Website mechanics</a></li>'
     '<li><a href="#flywheel"><span class="toc-num">07</span>The visibility flywheel</a></li>'
     '<li><a href="#market"><span class="toc-num">08</span>What it means</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["payment gateway","India","Razorpay","Airpay","Stripe","GEO","SEO teardown","AI citations","share of AI answers","backlinks","content gap","Ahrefs"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Why AI Cites Razorpay Over Airpay: India Payment-Gateway GEO Teardown &middot; rawmktg."
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

CHARTS="""
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
  var neutral=rgba(faint,0.45);

  var sh=document.getElementById('payShare');
  if(sh){new Chart(sh,{type:'bar',data:{labels:['Razorpay','Stripe','Wix','EnKash','Wise','Airpay'],
    datasets:[{data:[21,21,13,6,6,3],backgroundColor:[up,up,neutral,neutral,neutral,signal],borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of AI answers';}}}},
      scales:{x:{beginAtZero:true,max:25,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var vol=document.getElementById('payVolume');
  if(vol){new Chart(vol,{type:'bar',data:{labels:['gst','udyam registration','gst search','meesho seller','msme registration','cancelled cheque'],
    datasets:[{data:[2190000,1490000,871000,757000,285000,119000],backgroundColor:neutral,borderRadius:4,barThickness:18}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+(c.raw/1000000>=1?(c.raw/1000000).toFixed(2)+'M':(c.raw/1000).toFixed(0)+'K')+' monthly searches';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v>=1000000?(v/1000000)+'M':(v/1000)+'K';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  function donutc(id,vals,colors,big,small,bigColor){var el=document.getElementById(id);if(!el)return;
    var centerPlugin={id:'center_'+id,afterDatasetsDraw:function(ch){var a=ch.chartArea;if(!a)return;var ctx=ch.ctx,x=(a.left+a.right)/2,y=(a.top+a.bottom)/2;ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=bigColor;ctx.font='700 30px '+mono;ctx.fillText(big,x,y-7);ctx.fillStyle=text;ctx.font='9px '+mono;ctx.fillText(small,x,y+15);ctx.restore();}};
    new Chart(el,{type:'doughnut',data:{labels:vals.map(function(v){return v[0]+' '+v[1]+'%';}),datasets:[{data:vals.map(function(v){return v[1];}),backgroundColor:colors,borderColor:'#1A1815',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'66%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:10},boxWidth:10,boxHeight:10,padding:12}},tooltip:{callbacks:{label:function(c){return ' '+c.label.replace(/ [0-9.]+%$/,'')+': '+c.raw+'%';}}}}},plugins:[centerPlugin]});}
  donutc('payBranded',[['Branded',99.6],['Non-branded',0.4]],[signal,neutral],'100%','brand-name',signal);
  donutc('paySpam',[['Spam-flagged',94],['Clean',6]],[signal,up],'94%','spam-flagged',signal);
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">GEO &amp; SEO Teardown &middot; Payments</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Jun 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)
hh=open(f"blogs/{SLUG}.html").read()
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC SLOPE:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),
 "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| pipelines:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| listitem:",hh.count('role="listitem"'))
