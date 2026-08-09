#!/usr/bin/env python3
"""SCRATCH: build blogs/field-service-software-ai-visibility-gap.html (FSM SEO/GEO teardown). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="field-service-software-ai-visibility-gap"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-08-09"
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
def chart(cid,h,cap): return f'<div class="chart-wrap"><canvas id="{cid}" height="{h}"></canvas></div><div class="chart-caption">{esc(cap)}</div>'
def statgrid(items):
    cells="".join(f'<div class="sg-item"><div class="sg-val">{esc(v)}</div><div class="sg-label">{esc(l)}</div></div>' for v,l in items)
    return f'<div class="stat-grid">{cells}</div>'
def pipeline(nodes,goal,cap):
    parts=['<div class="pipeline">']
    for i,(t,dd) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(dd)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Field Service Software SEO: The AI Visibility Gap"
DECK=("A data-led teardown of how ten field service management platforms show up, or do not, across Google and AI answer engines, "
      "and the durable lessons any B2B software team can take from it.")
DESC=("Field service management software SEO/GEO teardown: why authority isn't traffic, the branded-demand trap, AI citations across 6 engines, winnable buyer keywords, and a 90-day playbook.")
DATANOTE=("A neutral teardown of ten leading field service management (FSM) platforms using Ahrefs worldwide organic, backlink and "
          "AI-citation data plus live technical checks of each vendor's field service page, August 2026. Figures are third-party "
          "estimates and directional; brands are named only as illustrative examples any B2B software team can learn from.")

CODE_JSONLD='''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Acme Field Service",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web, iOS, Android",
  "description": "Scheduling, dispatch, and invoicing for field service teams.",
  "offers": { "@type": "Offer", "price": "65.00", "priceCurrency": "USD" },
  "aggregateRating": {
    "@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "1200"
  }
}
</script>'''
CODE_LLMS='''# llms.txt  (serve at https://yourdomain.com/llms.txt)
# A plain-text map of the pages you most want AI engines to use.

## Product
- /field-service-management: what the product does, who it is for
- /pricing: plans and pricing

## Buyer guides
- /guides/field-service-software: category overview
- /compare/acme-vs-competitor: honest comparison'''
CODE_ROBOTS='''User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml'''
CODE_SNAP='''{
  "month": "2026-08",
  "non_branded_organic_visits": 4200,
  "ai_citations": { "chatgpt": 120, "google_ai": 95, "perplexity": 60,
                    "gemini": 30, "copilot": 25, "grok": 40 },
  "nonbranded_share_top10": 0.38,
  "category_referring_domains": 210,
  "paid_to_organic_ratio_core": 0.9
}'''

FAQ=[
 ("Which field service software has the best AI visibility?",
  "Among focused FSM vendors, Housecall Pro leads AI citations by a wide margin with about 7,809 across the major engines, followed by Jobber (4,379) and ServiceTitan (3,845). IFS trails at 478, while ServiceMax (12) and OverIT (10) are effectively invisible, a 651x spread between the category leader and the least-visible vendor."),
 ("Does domain authority predict organic traffic for field service software?",
  "No. Domain Rating tracks organic traffic loosely at best. The clearest example in the category is an asset-centric vendor with a Domain Rating of 68 and over 2,300 referring domains, the residue of years as a leader, that earns only about 332 organic visits a month because its content did not follow the product. Authority is a stock; traffic is a flow."),
 ("What are the best keywords for field service software?",
  "The most winnable buyer terms combine intent with low difficulty: dispatch software (3,600/mo, KD 4), plumbing software (2,200/mo, KD 9), work order software (2,900/mo, KD 12) and competitor-comparison terms like 'servicetitan competitors' (600/mo, KD 1). The broad head term, field service management software (9,400/mo, KD 52), is a medium-term pillar play."),
 ("How do you get field service software cited by AI engines?",
  "Make the page machine-readable and answerable. Add SoftwareApplication and FAQ JSON-LD schema, publish an llms.txt pointing crawlers to priority pages, ensure a clean robots.txt and sitemap, give each page one clear H1 and a direct answer near the top, and ship honest comparison pages, which AI engines quote readily."),
 ("What is the difference between SEO and GEO for field service software?",
  "SEO is winning Google's ranked results; GEO (generative engine optimization) is getting named inside AI answers from ChatGPT, Gemini, Perplexity and others. They overlap, the same structured, answer-first content helps both, but AI visibility is a distinct scoreboard: high organic traffic does not automatically produce AI citations, and vice versa."),
]

FIELD=[
 ["Microsoft Dynamics 365","96","302.9M","2.8M","2.6M"],
 ["Salesforce","92","9.6M","221K","209K"],
 ["SAP","91","4.5M","105K","91K"],
 ["ServiceNow","87","1.4M","35K","31K"],
 ["Jobber","90","322K","9K","27K"],
 ["Housecall Pro","89","140K","11K","21K"],
 ["ServiceTitan","80","338K","14K","13K"],
 ["IFS FSM","77","81K","4K","9K"],
 ["PTC ServiceMax","68","332","172","2K"],
 ["OverIT","47","2K","150","882"],
]
BUYER=[
 ["servicetitan competitors","600","1","Comparison, high intent"],
 ["dispatch software","3,600","4","Quick win"],
 ["plumbing software","2,200","9","Quick win, vertical"],
 ["work order software","2,900","12","Near-term"],
 ["field service management software","9,400","52","Medium term, pillar page"],
]

out=[]
out.append(p("Field service management (FSM) software is a growing market: research puts it at $5.12 billion in 2025, rising to $5.88 billion in 2026, a compound annual growth rate of about 15 percent. Demand is real and buyers are searching in plain, searchable language."))
out.append(p("Yet when you look at how the category's ten most visible vendors actually perform in organic search and in AI answers, a clear and repeatable set of lessons emerges, and they apply far beyond field service. The question is whether your brand shows up when buyers search, on Google and now inside AI answers. For most of the field, the answer is: not for the terms that matter."))
out.append(pull("Authority is a stock. Traffic is a flow. Link equity pointed at nothing converts to nothing."))

# 01 short version
out.append(sec("01","short","What is the short version?",
 "Field service vendors compete hard on product and barely at all on discovery.",
 "AI citations range from tens of thousands down to fewer than 50; the buyer terms are winnable; and most of the field has not run the sequence that wins Google and AI at once. That gap is the opportunity."))
out.append(h3("The seven takeaways"))
out.append("<ul>"
 "<li><strong>Domain Rating is a vanity metric.</strong> One vendor holds a trust score of 68 and 2,300+ linking domains, yet earns roughly 332 organic visits a month. Authority without live, matched content produces almost nothing.</li>"
 "<li><strong>Branded demand is a trap.</strong> For most vendors, the top organic terms are the company's own name and login page, demand you already own, not new buyers.</li>"
 "<li><strong>AI visibility is a distinct scoreboard.</strong> Some vendors are cited across every engine thousands of times; two others are effectively invisible with fewer than 50 combined.</li>"
 "<li><strong>The buyer-term map is winnable.</strong> Many high-intent field service terms carry a difficulty under 30, and some comparison terms sit near zero.</li>"
 "<li><strong>Structured data is the cheapest AI-visibility lever.</strong> The single biggest legibility gap on the pages we checked was missing JSON-LD schema.</li>"
 "<li><strong>Links still separate the pack.</strong> Referring-domain counts track durable authority and which brands AI engines treat as safe to cite.</li>"
 "<li><strong>Paid search masks organic gaps.</strong> The thinnest-organic vendor buys the most ads, defending high-intent terms it has not earned.</li></ul>")

# 1 market
out.append(sec("02","market","Is the market actually growing, and are buyers searching?",
 "Yes on both. FSM has moved from a back-office cost center to a strategic driver of uptime, retention and recurring revenue.",
 "Predictive maintenance, AI-assisted dispatch, and outcome-based contracts (now ~33% of service orgs, up from 19%) are pushing adoption, and buyers describe their needs in plain, searchable language."))
out.append(statgrid([("62%","want reliable mobile + offline"),("61%","want intelligent scheduling/routing"),("60%","want integrated billing"),("~15%","market CAGR (2025-26)")]))

# 2 landscape
out.append(sec("03","landscape","What does the visibility landscape look like?",
 "Organic visibility spans roughly five orders of magnitude, read it in two tiers.",
 "Enterprise suites sit on giant corporate domains where field service is one product among hundreds, so their traffic reflects the whole company. The focused FSM domains are the honest read on category search performance."))
out.append(table("Table 1. The field, at a glance. Ahrefs worldwide, August 2026, measured at subdomain scope.",
 ["Vendor","DR","Organic visits/mo","Keywords","Ref. domains"],
 FIELD, cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Note how loosely trust score (Domain Rating) tracks with either organic keywords or traffic, the pattern that anchors this whole teardown, and the same one behind the "+L("carbon and ESG software teardown","/blogs/authority-isnt-the-moat")+"."))

# 3 lesson one authority
out.append(sec("04","authority","Lesson one: is authority the same as traffic?",
 "No. High Domain Rating does not guarantee visits.",
 "An asset-centric vendor holds a trust score of 68 and 2,334 linking domains, the residue of years as a category leader, yet its legacy domain earns about 332 organic visits a month because the product moved and the domain has almost no live, optimized content."))
out.append(chart("drChart",240,"Figure 1. Domain Rating vs organic traffic across the focused vendors. Authority is a stock; traffic is a flow, and one DR-68 domain earns only a few hundred visits."))
out.append(p("This is the same gap covered in "+L("ranking isn't visibility","/blogs/ranking-isnt-visibility")+": link equity pointed at nothing converts to nothing."))

# 4 lesson two branded trap
out.append(sec("05","branded","Lesson two: what is the branded-demand trap?",
 "The top organic terms for most vendors are the brand name and the login page.",
 "Those visits are real, but they are people who already know you, not new buyers discovering the category. Non-branded, problem-led searches are exactly what AI engines quote, so a branded skew quietly caps both organic growth and AI eligibility."))
out.append(pipeline([("Learn","'what is field service software' - AI answers this directly."),("Compare","'best HVAC dispatch software' - AI shortlists here."),("Buy","'[brand] pricing / login' - the demand you already own.")],1,
 "Figure 2. Buyers move from learning to buying. AI engines increasingly answer the first two stages, where branded content never appears."))

# 5 lesson three AI scoreboard
out.append(sec("06","ai-citations","Lesson three: are AI answers a separate scoreboard?",
 "Yes. Being cited in AI answers does not automatically follow from organic traffic.",
 "It requires being readable, answerable and trusted. Among focused vendors the spread is stark: the leaders earn thousands of citations while two are effectively invisible with fewer than 50 combined, a 651x gap."))
out.append(chart("citeChart",260,"Figure 3. Total AI citations across the major engines (focused vendors). A 651x spread from Housecall Pro to the least-visible vendor."))
out.append(statgrid([("1,725","Housecall Pro, AI Overviews"),("1,479","Housecall Pro, Grok"),("1,220","Housecall Pro, Gemini"),("1,111","Housecall Pro, ChatGPT")]))
out.append(p("High AI visibility does not require the most traffic; it requires clearing every stage of the citation pipeline, the mechanism detailed in "+L("how your page gets retrieved","/blogs/how-your-page-gets-retrieved")+"."))
out.append(pipeline([("Crawl","Engine fetches the page, if robots.txt allows."),("Parse","Reads structure: H1, schema, clean HTML."),("Retrieve","Pulls the most quotable passage."),("Rank","Weighs it against competing sources."),("Cite","Names the source. Miss any stage, you are invisible.")],4,
 "Figure 4. A page must clear all five stages to be reliably cited by AI engines."))
out.append(callout("The two stages most teams skip",[
 "Engines cannot cite what they cannot read. Two low-cost, high-leverage moves make a page machine-readable: a structured-data block that tells the engine exactly what the page is, and an llms.txt file that points AI crawlers to your priority pages, more on whether "+"llms.txt does anything yet in the technical section below."]))

# 6 lesson four technical
out.append(sec("07","technical","Lesson four: do boring technical foundations still decide legibility?",
 "Yes. A page that engines cannot read cannot rank and cannot be cited, no matter how good the product is.",
 "Across the ten field service pages checked live, the technical picture was uneven, several were missing the basics that let Google and AI engines read a page."))
out.append(table("Table 2. A minimum legibility checklist for any B2B product page.",
 ["Signal","Why it matters for search and AI","Effort"],
 [["One clear H1","Tells engines the page's primary topic. Several pages had zero or multiple H1s.","1 hr"],
  ["JSON-LD structured data","The single biggest AI-legibility lever. Multiple product pages had none.","6-8 hrs"],
  ["Valid robots.txt with sitemap","Directs crawlers and points them to your page index.","1-2 hrs"],
  ["XML sitemap at the standard path","Helps discovery and indexation. A few returned an app shell instead.","3-4 hrs"],
  ["Open Graph + Twitter tags","Clean titles, descriptions and previews for shares and engines.","2-3 hrs"],
  ["llms.txt","Owner guidance for AI crawlers. Most vendors do not have one yet.","1-2 hrs"]],
 cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Tell engines what the page is with a SoftwareApplication schema block, the full pattern is in "+L("schema markup for AI citations","/blogs/schema-markup-ai-citations-2026")+":"))
out.append(code("JSON-LD: tell engines what the page is",CODE_JSONLD))
out.append(p("Point AI crawlers to your priority pages with an llms.txt, and confirm your robots.txt permits the "+L("named AI bots","/blogs/how-ai-crawlers-index-your-site")+":"))
out.append(code("llms.txt: guide AI crawlers to your priority pages",CODE_LLMS))
out.append(code("robots.txt: allow crawlers and declare your sitemap",CODE_ROBOTS))

# 7 lesson five buyer terms
out.append(sec("08","buyer-terms","Lesson five: is the buyer-term map winnable?",
 "More winnable than it looks. Many high-intent field service terms carry low difficulty.",
 "Broad category terms like field service management software carry volume but higher difficulty (a medium-term play); comparison and alternative terms combine real buying intent with very low difficulty, and AI engines quote comparison pages readily."))
out.append(chart("buyerChart",240,"Figure 5. Buyer terms by difficulty. Comparison and vertical terms sit in the easy-to-win band; the head term is a medium-term pillar."))
out.append(table("Table 3. A working target list. Ahrefs Keywords Explorer, worldwide; difficulty is a 0-100 estimate.",
 ["Buyer term","Global searches/mo","Difficulty","Play"],
 BUYER, cls=lambda j,c:("label" if j==0 else ("up" if (j==2 and c.isdigit() and int(c)<20) else ""))))

# 8 lesson six links
out.append(sec("09","links","Lesson six: do links still separate the pack?",
 "Yes. Referring-domain counts track durable authority and, indirectly, which brands AI engines treat as safe to cite.",
 "The lesson is not to chase links blindly, but to earn category-relevant ones. Among the pure-plays, the vendor with the broadest link base is the only SMB tool to reach a trust score of 90."))
out.append(table("Table 4. A relevance-first link priority for B2B software.",
 ["Set","Examples","Why it helps"],
 [["1. Directories and review sites","G2, Capterra, GetApp, Software Advice, TrustRadius","Buyers and AI engines both read them. Fast, mostly self-serve."],
  ["2. Trade and industry media","HVAC, plumbing and field service trade publications","Reaches the exact buyers and builds category trust."],
  ["3. News, research and data","'Best software' roundups, original data studies","One data report earns many links at once and gets cited by AI."]],
 cls=lambda j,c:"label" if j==0 else ""))

# 9 lesson seven paid
out.append(sec("10","paid","Lesson seven: does paid search mask organic gaps?",
 "Yes. The vendor thinnest on organic among the SMB tools buys the most paid traffic.",
 "It uses ads to defend high-intent commercial queries it has not yet earned organically. Paid is rented demand: when spend stops, the traffic stops."))
out.append(p("The strongest organic performer invests comparatively little in paid, because its content engine already captures the demand it needs. Use paid to buy time while organic and AI visibility compound, not as a permanent substitute, the same trap covered in "+L("getting found on Google and AI","/blogs/payments-getting-found-google-ai")+"."))

# 10 playbook
out.append(sec("11","playbook","What is the 90-day playbook?",
 "Front-load cheap technical fixes, then compound content and links.",
 "The order matters: fixes first so everything you publish is legible, then buyer pages, then the links and data that lift the whole domain."))
out.append(table("Table 5. A 90-day search and AI-visibility roadmap. Content and links run in parallel.",
 ["Phase","Focus","Concrete moves"],
 [["Month 1","Fix and instrument","Add schema and llms.txt, fix H1s, sitemap and robots.txt. Claim directory and review-site profiles. Stand up AI-citation and non-branded-traffic tracking."],
  ["Months 1-2","Build buyer pages","Ship pages for the easiest high-intent terms, a plain 'what is field service software' explainer, and a short answer box near the top of each product page."],
  ["Months 2-3","Trust and moat","Publish comparison and alternative pages, then one original data report, and pitch it to trade media for links and AI citations."]],
 cls=lambda j,c:"label" if j==0 else ""))
out.append(h3("A measurement framework"))
out.append(p("Most teams measure organic traffic and stop. In an AI-search world that misses half the picture. Track these five together, monthly, the same discipline as "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+":"))
out.append(table("Table 6. A five-metric scorecard for search and AI visibility.",
 ["Metric","What it tells you","Healthy direction"],
 [["Non-branded organic traffic","New-buyer discovery, not brand harvesting","Up"],
  ["AI citations by engine","Whether AI answers name you","Up, across 4+ engines"],
  ["Share of top-10 terms that are non-branded","Whether content is creating demand","Above 50%"],
  ["Referring domains (category-relevant)","Durable authority","Steady growth"],
  ["Paid-to-organic ratio on core terms","How rented your demand is","Down over time"]],
 cls=lambda j,c:"label" if j==0 else ""))
out.append(code("A minimal monthly visibility snapshot (store one per month, watch the trend)",CODE_SNAP))

# 11 founders vs marketers
out.append(sec("12","owners","Founders vs marketers: who owns what?",
 "Founders set the conditions; marketers run the plays.",
 "Pretending this is only a marketing project guarantees it stalls."))
out.append(table("Table 7. The split that keeps the program moving.",
 ["If you are a founder, focus on","If you are a marketer, focus on"],
 [["Treat search and AI visibility as a product surface, not a channel. Fund structured data and technical health like features.","Kill the branded-traffic illusion in reporting. Separate branded from non-branded and report the non-branded line."],
  ["Resist vanity metrics. Ask for non-branded traffic and AI citations, not Domain Rating.","Own the buyer-term map. Ship comparison and alternative pages first; they are high intent and low difficulty."],
  ["Invest in one original data asset a year. It is the cheapest durable moat for links and AI citations.","Make every key page readable: schema, llms.txt, one H1, a direct answer near the top."],
  ["Hire or partner for content plus technical SEO plus digital PR together, not in silos.","Measure the five-metric scorecard monthly and let it drive the roadmap."]]))

# bottom line
out.append(sec("13","takeaway","What is the bottom line?",
 "The vendors that win the next few years will not be the ones with the highest trust score or the biggest ad budget.",
 "They will be the ones whose pages are legible to machines, whose content answers real buyer questions before the buyer knows their name, and who earn category-relevant links and cite-worthy data."))
out.append(p("Field service software is a healthy, growing market where buyers search in plain language and increasingly ask AI engines for recommendations. None of the winning work is exotic. It is a sequence, and most of the field has not run it yet."))
out.append(pull("That gap, between a category with real, searchable demand and vendors who have not built for it, is the opportunity."))

# FAQ
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, AI search and B2B discoverability. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Methodology: Ahrefs worldwide data and live technical checks across ten FSM vendors, August 2026. Brands are named only as illustrative examples of patterns any B2B software team can learn from.</p></div>')

body="\n".join(out)

SIDEBAR=[("651x","citation spread, leader vs least-visible"),("7,809","Housecall Pro AI citations"),("332","visits/mo on a DR-68 domain"),("KD 1-12","the winnable buyer terms")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#short"><span class="toc-num">01</span>The short version</a></li>'
     '<li><a href="#market"><span class="toc-num">02</span>A growing market</a></li>'
     '<li><a href="#landscape"><span class="toc-num">03</span>The landscape</a></li>'
     '<li><a href="#authority"><span class="toc-num">04</span>Authority isn\'t traffic</a></li>'
     '<li><a href="#branded"><span class="toc-num">05</span>The branded trap</a></li>'
     '<li><a href="#ai-citations"><span class="toc-num">06</span>AI is a separate scoreboard</a></li>'
     '<li><a href="#technical"><span class="toc-num">07</span>Technical legibility</a></li>'
     '<li><a href="#buyer-terms"><span class="toc-num">08</span>The buyer-term map</a></li>'
     '<li><a href="#links"><span class="toc-num">09</span>Links still matter</a></li>'
     '<li><a href="#paid"><span class="toc-num">10</span>Paid masks gaps</a></li>'
     '<li><a href="#playbook"><span class="toc-num">11</span>The 90-day playbook</a></li>'
     '<li><a href="#owners"><span class="toc-num">12</span>Founders vs marketers</a></li>'
     '<li><a href="#takeaway"><span class="toc-num">13</span>The bottom line</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - field service management software SEO and GEO teardown - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["field service management software","field service software seo","dispatch software","work order software","GEO","AI citations","ai visibility","servicetitan","housecall pro","jobber","B2B SaaS SEO"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Field Service Software SEO/GEO Teardown &middot; rawmktg."
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

  var dr=document.getElementById('drChart');
  if(dr){new Chart(dr,{type:'bar',data:{labels:['ServiceTitan','Jobber','Housecall Pro','IFS FSM','ServiceMax','OverIT'],datasets:[
    {label:'Domain Rating',data:[80,90,89,77,68,47],backgroundColor:neutral,borderRadius:4,yAxisID:'y'},
    {label:'Organic visits/mo',data:[338000,322000,140000,81000,332,2000],backgroundColor:signal,borderRadius:4,yAxisID:'y1',type:'line',borderColor:signal,pointRadius:4,fill:false}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:10}}},tooltip:{callbacks:{label:function(c){return c.dataset.label==='Domain Rating'?' DR '+c.raw:' '+c.raw.toLocaleString()+' visits';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},
        y:{position:'left',beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:9}},grid:{color:grid},title:{display:true,text:'DR',color:text,font:{family:mono,size:9}}},
        y1:{position:'right',type:'logarithmic',ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v>=1000?(v/1000)+'k':v;}},grid:{drawOnChartArea:false},title:{display:true,text:'visits/mo (log)',color:text,font:{family:mono,size:9}}}}}});}

  var ci=document.getElementById('citeChart');
  if(ci){new Chart(ci,{type:'bar',data:{labels:['Housecall Pro','Jobber','ServiceTitan','IFS FSM','ServiceMax','OverIT'],datasets:[{data:[7809,4379,3845,478,12,10],backgroundColor:[up,signal,signal,rgba(signal,0.7),neutral,neutral],borderRadius:4,barThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.toLocaleString()+' AI citations';}}}},
      scales:{x:{type:'logarithmic',ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v>=1000?(v/1000)+'k':v;}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var by=document.getElementById('buyerChart');
  if(by){new Chart(by,{type:'bar',data:{labels:['servicetitan competitors','dispatch software','plumbing software','work order software','field service mgmt software'],datasets:[{data:[1,4,9,12,52],backgroundColor:[up,up,up,up,signal],borderRadius:4,barThickness:22}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' KD '+c.raw+' / 100';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid},title:{display:true,text:'Keyword difficulty (0-100)',color:text,font:{family:mono,size:10}}},y:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Field Service Software &middot; AI Visibility Research</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/fsm_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/fsm_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,"| h1:",hh.count("<h1"),
 "| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faq:",hh.count('faq-item'),"| cbcopy:",'cb-copy-css' in hh)
