#!/usr/bin/env python3
"""SCRATCH: build blogs/authority-isnt-the-moat.html (carbon & ESG GEO/SEO teardown). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="authority-isnt-the-moat"; URL=f"https://rawmktg.com/blogs/{SLUG}"
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
ADSENSE=''  # AdSense removed: no ad units, hurts TBT
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

HEADLINE="Carbon & ESG Software SEO: Why Content Beats Authority in AI Search"
DECK=("The search and AI-visibility teardown of 10 carbon and ESG platforms, and the content work nobody shipped. "
      "Product capability is converging; distribution is not.")
DESC=("Carbon accounting and ESG software SEO/GEO teardown: why authority isn't the moat, content is. AI citations across 7 engines, cheap buyer keywords (KD 1-19), and the GEO playbook.")
DATANOTE=("A neutral teardown of ten leading carbon and ESG platforms using live search and AI-visibility data across seven engines "
          "(Google AI Overviews, AI Mode, ChatGPT, Perplexity, Gemini, Copilot, Grok), plus technical site checks. Data snapshot: "
          "August 2026. Figures are third-party estimates and directional; brands are referenced as illustrative examples only.")

CODE_ROBOTS='''# robots.txt - allow the major AI answer engines
User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended   # Gemini / AI Overviews
Allow: /

User-agent: ClaudeBot
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml'''

CODE_LLMS='''# llms.txt - https://yourdomain.com/llms.txt
# Guide for AI crawlers: the pages worth citing.

## Product
- [Carbon accounting software](/product): measure Scope 1-3, audit-ready.
- [CSRD reporting](/csrd): map data to ESRS and file with confidence.

## Methodology
- [How GHG accounting works](/learn/ghg-accounting): plain-English guide.
- [Scope 3 explained](/learn/scope-3): the 15 categories, with examples.

## Proof
- [Benchmark report 2026](/research/benchmark): original emissions data.'''

CODE_JSONLD='''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is carbon accounting software?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Carbon accounting software measures an organization's
       greenhouse-gas emissions across Scopes 1, 2, and 3, then turns
       that data into audit-ready reports for CSRD, ISSB, and the SEC."
    }
  }]
}
</script>'''

CODE_ANSWER='''## What is Scope 3?

Scope 3 is all the indirect emissions in a company's value
chain, both upstream and downstream: purchased goods, business
travel, and the use of sold products. It is usually the largest
and hardest-to-measure share of a company's footprint,
spanning 15 defined categories under the GHG Protocol.

<!-- then expand: the 15 categories, examples, how to measure -->'''

FAQ=[
 ("Is domain authority the moat in carbon and ESG software?",
  "No. Eight of the ten most-visible carbon and ESG platforms already carry a domain rating of 63 or higher, so authority is uniform and no longer a differentiator. What separates the traffic and AI-citation leaders is content footprint: ranked-keyword counts range from about 250 to nearly 12,000 across companies with near-identical authority. More published, well-structured pages move the needle; more backlinks do not."),
 ("What are the best buyer keywords for carbon accounting software?",
  "The highest-value, lowest-competition buyer terms in the category include emissions management software (KD 1), csrd software (KD 2, ~$18 CPC), scope 3 software (KD 2), carbon management software (KD 5), esg reporting software (KD 9), esg software (KD 11, ~$12 CPC) and carbon accounting software (KD 19). Most sit in an easy-to-win band yet are claimed by only one or two vendors."),
 ("How do you get cited by AI engines like ChatGPT and Perplexity?",
  "Four concrete steps: let the named AI crawlers in via robots.txt, publish an llms.txt index of your best pages, add Organization, Product and FAQPage JSON-LD schema, and write answer-first, leading each section with a self-contained 40-60 word answer an engine can lift verbatim. AI answers cite the clearest relevant passage, not the highest-authority domain."),
 ("Does llms.txt help with AI citations?",
  "llms.txt is a plain-text file that tells AI crawlers which pages matter most. It takes about five minutes to ship and most of the carbon and ESG field has not published one. It is not a magic ranking lever, but combined with crawl access, schema and answer-first content it lowers the cost of being found and quoted by generative engines."),
 ("Should carbon and ESG founders or marketers own AI search?",
  "Both, with a split. Founders own the highest-leverage inputs: proprietary data as a moat, a defensible point of view, protected engineering time for site health and schema, and deciding which two or three category terms to own. Marketers own execution: turning that data into structured, answer-first buyer pages, owning the buyer-term map, and measuring AI citations and rankings."),
]

FIELD=[
 ["Greenly","76","78,152","11,939","922"],
 ["Workiva","75","111,593","6,207","299"],
 ["Sphera","75","15,175","878","151"],
 ["Cority","67","9,652","626","79"],
 ["Sweep","65","7,236","1,093","57"],
 ["Persefoni","67","9,837","1,127","39"],
 ["Watershed","73","7,380","370","18"],
 ["Microsoft (section)","96","~2,900","~220","13"],
 ["Position Green","63","3,777","248","12"],
 ["Salesforce (section)","92","~1,344","~130","4"],
]
BUYER=[
 ["emissions management software","250","1","$0.70","Wide open"],
 ["csrd software","150","2","$18.00","Easy, top intent"],
 ["scope 3 software","80","2","$6.00","Easy, on-topic"],
 ["carbon management software","400","5","$0.60","Easy"],
 ["esg reporting software","1,000","9","$0.35","Easy, high volume"],
 ["esg software","900","11","$12.00","Easy, high intent"],
 ["carbon accounting software","1,000","19","$0.40","Medium, high volume"],
 ["carbon footprint software","250","60","$5.00","Hard, contested"],
]

out=[]
out.append(p("The product race in carbon accounting and ESG software is maturing fast. Audit-grade data, Scope 3 depth, and agentic AI are becoming table stakes. The race that is still wide open is distribution: who gets found when a buyer searches Google, and who gets named when that same buyer asks ChatGPT, Perplexity, or Google's AI."))
out.append(p("This teardown uses live search and AI-visibility data across ten leading platforms to show where the opportunity sits, and what to do about it. Brands appear as examples to learn from, not to rank or rate."))
out.append(pull("Almost every serious vendor has the authority to win these surfaces. Almost none has done the work. That is the gap, and gaps like this do not stay open."))

# 01 short version
out.append(sec("01","short","What is the short version?",
 "Ten of the most visible carbon and ESG brands compete hard on product and barely at all on discovery.",
 "Their sites are strong enough to rank for almost anything they choose to write about. Most simply have not written it. That gap is the whole opportunity, and it is closing as faster-moving competitors publish."))
out.append(h3("The seven takeaways"))
out.append("<ul>"
 "<li><strong>Authority is not the bottleneck.</strong> Eight of ten sites already carry a domain rating of 63+. More links will not move the needle; more published pages will.</li>"
 "<li><strong>Content footprint decides traffic.</strong> Ranked-keyword counts range from ~250 to nearly 12,000 across near-identical authority. The spread is a publishing choice.</li>"
 "<li><strong>AI answers cite content, not authority.</strong> The two highest-authority domains earn the fewest AI citations; the biggest content library earns the most, by an order of magnitude.</li>"
 "<li><strong>The buyer terms are cheap and unclaimed.</strong> Terms like carbon accounting software and csrd software are low difficulty and high commercial value, and most vendors rank for none of them.</li>"
 "<li><strong>Paid search is filling the gap.</strong> The vendors thinnest on organic content spend most on ads for exactly the terms they could own.</li>"
 "<li><strong>GEO and SEO are the same work.</strong> Structured, answer-first content wins Google features and AI citations at once. One program, not two.</li>"
 "<li><strong>This is a founder problem too.</strong> Proprietary data, a defensible point of view, and engineering time for schema and site health are set at the top, not delegated to a content calendar.</li></ul>")

# 1 why distribution
out.append(sec("02","battleground","Why is distribution the new battleground?",
 "Because regulation is manufacturing demand, and that demand is routed through search and AI answers.",
 "CSRD, ISSB, the SEC climate rules, the UK SRS and Australia's AASB S2 are pushing thousands of companies toward audit-ready software on a fixed timeline, a growing buying population that starts most journeys by searching."))
out.append(p("When a sustainability lead or a CFO's team goes looking for a platform, they do two things: they Google a category term, and increasingly they ask an AI assistant to shortlist vendors. Both surfaces are won with published, structured content. Neither is won with a better demo or a bigger funding round. So the question is simple: for a category with surging, search-led demand, who has actually built for search, and who is leaving the channel open?"))

# 2 methodology
out.append(sec("03","method","How did we measure this?",
 "Live search and AI-visibility data for ten platforms across seven AI engines, plus technical site checks.",
 "Domain authority, organic traffic and keywords, backlinks, paid presence, and a count of citations across Google AI Overviews, AI Mode, ChatGPT, Perplexity, Gemini, Copilot and Grok, cross-referenced with the market's own product research."))
out.append(callout("Two honest caveats",[
 "Two of the ten are hyperscalers (a global cloud company and a global CRM company) whose whole domains dwarf the field. For them, the numbers are scoped to the sustainability product section, and flagged throughout so the comparison stays fair.",
 "These are estimates and a single-day snapshot; read them as direction, not gospel. The patterns, not the decimal places, are the point."]))

# 3 finding one authority
out.append(sec("04","authority","Is authority the moat? (It isn't.)",
 "No. The pure-play vendors cluster in a narrow domain-rating band from the low 60s to mid 70s.",
 "When authority is this uniform it stops being a differentiator. What separates traffic leaders from laggards is not how strong their domains are; it is how much they have published."))
out.append(chart("drChart",240,"Figure 1. Domain rating is uniform across the pure-play field (63-76). The two hyperscaler sections sit far above (92, 96), yet earn among the fewest citations."))
out.append(p("Look at the outliers. One well-known enterprise brand carries a domain rating of 73, higher than several competitors, yet sits near the bottom of the traffic range with a tiny keyword footprint. The traffic leaders are the two firms with the largest content libraries, not the strongest link profiles. The lesson: stop buying links and start shipping pages. You have already cleared the authority bar. This is the same pattern behind "+L("ranking isn't visibility","/blogs/ranking-isnt-visibility")+"."))

# 4 finding two content footprint
out.append(sec("05","footprint","What actually decides traffic?",
 "Content footprint. On near-identical authority, the leaders rank for 10x to 30x more terms than the laggards.",
 "The content leader ranks for nearly 12,000 keywords on a deep library of definitional pages; several category-famous enterprise brands rank for a few hundred terms each, almost all their own brand name."))
out.append(chart("kwChart",260,"Figure 2. Ranked-keyword footprint. Same authority, up to 30x the coverage, a decision about whether content is a product surface or a brochure."))
out.append(table("Table 1. The full field, at a glance. *Total citations across seven AI engines; Microsoft and Salesforce scoped to their sustainability sections.",
 ["Company","Domain rating","Organic visits/mo","Ranked keywords","AI citations*"],
 FIELD, cls=lambda j,c:"label" if j==0 else ""))

# 5 finding three AI cites content
out.append(sec("06","ai-citations","Do AI answers cite authority, or content?",
 "Content, overwhelmingly. Authority barely enters into it.",
 "The two hyperscaler sustainability sections have the highest domain ratings in the set (92 and 96) and among the fewest AI citations. The content leader, on a lower domain rating, earns citations by the hundreds."))
out.append(chart("citeChart",300,"Figure 3. Total AI citations across seven engines. Highest authority, fewest citations, content is the moat, not DR."))
out.append(p("AI engines are not consulting a link-authority score when they build an answer; they are retrieving the clearest, most relevant passage they can find and citing its source. If you have not written the passage, you cannot be the source, the mechanism detailed in "+L("how your page gets retrieved","/blogs/how-your-page-gets-retrieved")+"."))
out.append(h3("Where the citations actually come from"))
out.append(p("Google's AI Overviews and AI Mode are where most citation volume lives, so the same content that wins a Google featured snippet tends to win the AI citation, your existing SEO work compounds here. And breadth matters: the leaders are cited across every engine, while thinner sites get a stray citation on one or two. Being citable everywhere is a function of having enough well-structured pages that every engine finds something to quote, which is "+L("why engines recommend different vendors","/blogs/why-engines-recommend-different-vendors")+"."))
out.append(h3("How an AI answer gets built"))
out.append(pipeline([("Crawl","Engine fetches your pages, if robots.txt allows it."),("Parse","It reads structure: headings, schema, clean HTML."),("Retrieve","It pulls the most quotable passage for the query."),("Cite","It names the source. Miss any stage, you are invisible.")],3,
 "Figure 4. The four stages of an AI citation, and the specific lever you control at each one."))

# 6 finding four buyer terms
out.append(sec("07","buyer-terms","Are the buyer terms cheap and unclaimed?",
 "Yes. The terms that signal a ready buyer are both low difficulty and high commercial value.",
 "Difficulty runs mostly between 1 and 19 out of 100. csrd software carries a CPC near $18 and esg software near $12, yet most of these terms are won by only one or two vendors, and several are effectively open."))
out.append(chart("buyerChart",260,"Figure 5. Buyer-intent terms by difficulty. Most sit in the easy-to-win band (KD under 20); only carbon footprint software is contested."))
out.append(table("Table 2. A working target list. Most category buyer terms are low difficulty; the winners simply built a page for each.",
 ["Buyer term","US volume/mo","Difficulty","CPC","Read"],
 BUYER, cls=lambda j,c:("label" if j==0 else ("up" if (j==2 and c.isdigit() and int(c)<20) else ""))))
out.append(callout("What this means for a marketer",["You do not need a huge budget or two years to win these. You need one clear, well-structured page per term, built answer-first, shipped before a competitor claims it."]))

# 7 finding five paid crutch
out.append(sec("08","paid","Is paid search a moat?",
 "No, it is rented visibility. The vendors thinnest on organic content spend most aggressively on ads.",
 "The moment the budget stops, so does the traffic. Organic and AI visibility compound: a buyer page that ranks and gets cited keeps working for years at close to zero marginal cost."))
out.append(p("Paid search has its place, it is fast and measurable, but it is a bridge you cross while the durable asset gets built underneath it. The strategic mistake is treating paid as the strategy rather than the bridge. This is the same trap covered in "+L("getting found on Google and AI","/blogs/payments-getting-found-google-ai")+"."))

# 8 GEO playbook
out.append(sec("09","playbook","How do you make your pages citable?",
 "Four concrete, mostly technical moves that help traditional SEO at the same time.",
 "Let the AI crawlers in, publish an llms.txt, add structured data, and write answer-first. GEO and SEO are one program, not two."))
out.append(h3("Step 1: let the AI crawlers in"))
out.append(p("AI engines can only cite what they can fetch. Confirm your robots.txt permits the named AI bots, and do not let an over-aggressive bot wall block them, one hyperscaler sustainability page in this study returned a bot challenge to non-browser requests, which can suppress citations. See "+L("how AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site")+"."))
out.append(code("robots.txt",CODE_ROBOTS))
out.append(h3("Step 2: publish an llms.txt"))
out.append(p("An llms.txt file is a plain-text index that tells AI crawlers which pages matter. It is a five-minute file that most of the field has not shipped, more on whether "+L("llms.txt actually does anything yet","/blogs/does-llms-txt-do-anything-yet")+"."))
out.append(code("llms.txt",CODE_LLMS))
out.append(h3("Step 3: add structured data (JSON-LD)"))
out.append(p("Schema is how a page self-describes to machines. The clearest pattern in this study: the sustainability section that ships Product and FAQPage schema already ranks number one for a non-branded buyer term, while a far larger competitor that ships no schema does not. Put Organization, Product and FAQPage on your key pages, the full pattern is in "+L("schema markup for AI citations","/blogs/schema-markup-ai-citations-2026")+"."))
out.append(code("FAQPage JSON-LD (paste into the page head)",CODE_JSONLD))
out.append(h3("Step 4: write answer-first"))
out.append(p("Structure invites the citation; the words earn it. Lead each key section with a direct, self-contained answer of roughly 40 to 60 words that an engine can lift verbatim, then expand below it."))
out.append(code("answer-first section pattern",CODE_ANSWER))

# 9 technical checklist
out.append(sec("10","technical","What is the technical foundation checklist?",
 "The plumbing that has to work before content can compound.",
 "Even large, sophisticated brands fail some of these, one hyperscaler in this study serves a broken XML sitemap and ships no structured data on its product page."))
out.append(table("Table 3. The technical checks every site was run against, with the fixes that matter most.",
 ["Element","Why it matters","Typical effort"],
 [["Valid robots.txt","Directs crawlers and, critically, permits AI bots","1-2 hrs"],
  ["Working XML sitemap","Page discovery; a broken one silently caps rankings","3-4 hrs"],
  ["llms.txt","Tells AI crawlers what to prioritize","1-2 hrs"],
  ["Organization + Product JSON-LD","Lets engines identify and quote the entity","4-6 hrs"],
  ["FAQPage schema","The format AI engines lift most readily","2-4 hrs"],
  ["One descriptive H1 per page","Names the topic for crawlers and readers","2 hrs"],
  ["Open Graph + Twitter tags","Controls sharing and secondary entity signals","2-3 hrs"],
  ["hreflang for locales","Consolidates international ranking signals","3 hrs"],
  ["Server-side rendered content","If text is JS-only, crawlers may miss it","varies"]],
 cls=lambda j,c:"label" if j==0 else ""))

# 10 compounding loop
out.append(sec("11","compounding","Why does one good page pay out three times?",
 "Because a single well-built asset compounds across three channels at once.",
 "Build one page for a buyer term, structure it so an AI engine can quote it, back it with a data point no competitor has. That page ranks, which earns links; the links raise authority, which lifts the ranking; the structure earns AI citations, which drive referral traffic and brand searches, which lift rankings again."))
out.append(pipeline([("One buyer page","Answer-first, schema, original data."),("Ranks on Google","Earns editorial links."),("Links raise authority","Which lifts the ranking further."),("AI citations","Referral traffic + brand search, which lifts rankings again.")],3,
 "Figure 6. Paid search cannot start this loop. Content is the only input that does."))

# 11 segments
out.append(sec("12","segments","How should the motion match the buyer?",
 "The method is constant; the vocabulary changes by segment.",
 "Win the definitional and how-to terms that establish authority, then the buyer terms that convert, then earn the topical links and data citations that make you the source AI engines trust."))
out.append(table("Table 4. Segment plays: mapping buyer profiles to a distribution motion.",
 ["Buyer segment","What they search for","The content play","Example to study"],
 [["Listed multinationals","Audit trail, XBRL, SEC and CSRD parity","Compliance explainers, framework mapping, assurance content","Reporting-led players who own compliance keywords"],
  ["Complex value chains","Product carbon footprint, supplier data","Methodology deep-dives, Scope 3 guides, calculators","Vendors ranking for scope 3 and PCF terms"],
  ["Heavy industry (EHS + carbon)","Process safety, LCA, chemical compliance","Regulatory and standards content, site-level how-tos","EHS suites with deep, mature libraries"],
  ["Mid-market and SME","Fast, affordable carbon tracking","Definitional and how-to content, transparent pricing","The educational-content leader in the set"],
  ["Ecosystem-native (cloud/CRM)","Integration with existing stack","Integration guides, comparison and migration pages","The section that ships strong Product and FAQ schema"],
  ["Financial institutions","PCAF, portfolio carbon, disclosures","Methodology and standards content for finance readers","Ledger-first platforms targeting finance terms"]],
 cls=lambda j,c:"label" if j==0 else ""))

# 12 90 days
out.append(sec("13","ninety-days","What does the first 90 days look like?",
 "A focused quarter fixes the foundation and ships the first compounding assets.",
 "Fix the plumbing first. Publishing into a broken foundation, no schema, a broken sitemap, blocked AI bots, wastes the content."))
out.append(table("Table 5. The 90-day operating system.",
 ["Phase","Focus","Concrete actions","Owner"],
 [["Weeks 1-2","Fix the plumbing","Audit and fix robots.txt, sitemap, crawl access. Ship llms.txt. Add Organization + Product + FAQ schema to key pages.","Engineering + SEO"],
  ["Weeks 2-6","Ship buyer pages","Build one answer-first page per priority buyer term, starting with the easy, high-CPC ones. Reuse a proven template.","Content + Product"],
  ["Weeks 4-8","Build the topic layer","Publish definitional and how-to guides (Scope 3, CSRD, GHG accounting) with FAQ schema for AI lift.","Content"],
  ["Weeks 6-10","Comparison + proof","Ship honest comparison pages and one original data report from your own platform data.","Marketing + Data"],
  ["Weeks 8-12","Earn and measure","Pitch the data report to trade media for links. Stand up AI-citation and rank tracking. Reprioritize.","Marketing"]],
 cls=lambda j,c:"label" if j==0 else ""))

# 13 owners
out.append(sec("14","owners","Who owns what: founders or marketers?",
 "The highest-leverage inputs are founder decisions; the execution is the marketer's craft.",
 "Pretending this is only a marketing project guarantees it stalls."))
out.append(table("Table 6. The split that keeps the program moving.",
 ["Founders should focus on","Marketers should focus on"],
 [["Proprietary data as a moat: what benchmark or dataset can only you publish?","Turning that data into ranked, cited pages and a repeatable buyer-page template."],
  ["A sharp, defensible point of view worth being cited for.","Structuring content answer-first with schema so engines quote it."],
  ["Protecting engineering time for site health, schema and crawlability.","Owning the buyer-term map and the editorial calendar behind it."],
  ["Positioning: the two or three terms you intend to own, and saying no to the rest.","Measuring AI citations and rankings, and reallocating toward what compounds."],
  ["Treating distribution as a product surface with a budget, not a campaign line.","Running the 90-day system and reporting the leading indicators."]]))

# 14 metrics
out.append(sec("15","metrics","Which metrics actually matter?",
 "Leading indicators of durable discovery, not vanity metrics.",
 "Track whether you are building beyond your own name, capturing buyer terms, and getting cited across engines."))
out.append(table("Table 7. The metrics that tell you this is working.",
 ["Metric","What it tells you","Healthy direction"],
 [["Non-branded keyword count","Whether you are building beyond your own name","Up and to the right"],
  ["Buyer-term rankings (top 10)","Bottom-of-funnel capture","More terms in the top 10"],
  ["AI citations across engines","GEO visibility and breadth","Cited on all major engines"],
  ["Share of organic vs paid traffic","Whether the durable asset is growing","Organic share rising"],
  ["Referring domains from trade media","Topical authority, not just volume","Relevant, editorial links"],
  ["Branded search volume","Whether category work lifts brand demand","Rising over time"]],
 cls=lambda j,c:"label" if j==0 else ""))

# 15 takeaway
out.append(sec("16","takeaway","What is the takeaway?",
 "The category is manufacturing its own demand through regulation, and routing it through search and AI answers.",
 "Almost every serious vendor has the authority to win those surfaces. Almost none has done the work."))
out.append(p("For founders, the move is to treat distribution as a product surface: fund the site health, protect the engineering time, and decide which category terms you intend to own. For marketers, the move is to stop renting visibility and start building the compounding asset, one structured, answer-first, buyer-intent page at a time."))
out.append(pull("The winners of the next few years will not be decided by who has the best model of an emissions factor. They will be decided by who is easiest to find."))

# FAQ
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, AI search and B2B discoverability. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>A neutral teardown for founders and marketers. Data snapshot August 2026; figures are third-party estimates and directional. Brands are referenced as illustrative examples only.</p></div>')

body="\n".join(out)

SIDEBAR=[("922 / 18","content leader vs best-known brand, AI citations"),("30x","keyword gap on equal authority"),("63-76","pure-play domain-rating band"),("KD 1-19","difficulty of the buyer terms")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#short"><span class="toc-num">01</span>The short version</a></li>'
     '<li><a href="#battleground"><span class="toc-num">02</span>Why distribution wins</a></li>'
     '<li><a href="#method"><span class="toc-num">03</span>How we measured it</a></li>'
     '<li><a href="#authority"><span class="toc-num">04</span>Authority isn\'t the moat</a></li>'
     '<li><a href="#footprint"><span class="toc-num">05</span>Content footprint</a></li>'
     '<li><a href="#ai-citations"><span class="toc-num">06</span>AI cites content</a></li>'
     '<li><a href="#buyer-terms"><span class="toc-num">07</span>Cheap buyer terms</a></li>'
     '<li><a href="#paid"><span class="toc-num">08</span>Paid is a crutch</a></li>'
     '<li><a href="#playbook"><span class="toc-num">09</span>The GEO playbook</a></li>'
     '<li><a href="#technical"><span class="toc-num">10</span>Technical checklist</a></li>'
     '<li><a href="#compounding"><span class="toc-num">11</span>One page, three payouts</a></li>'
     '<li><a href="#segments"><span class="toc-num">12</span>Segment plays</a></li>'
     '<li><a href="#ninety-days"><span class="toc-num">13</span>The first 90 days</a></li>'
     '<li><a href="#owners"><span class="toc-num">14</span>Founders vs marketers</a></li>'
     '<li><a href="#metrics"><span class="toc-num">15</span>Metrics that matter</a></li>'
     '<li><a href="#takeaway"><span class="toc-num">16</span>The takeaway</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - carbon and ESG software SEO and GEO teardown - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["carbon accounting software","esg reporting software","esg software seo","carbon and ESG software","GEO","AI citations","csrd software","content marketing","domain authority","ai visibility"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Carbon &amp; ESG Software SEO/GEO Teardown &middot; rawmktg."
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
  if(dr){new Chart(dr,{type:'bar',data:{labels:['Microsoft*','Salesforce*','Greenly','Workiva','Sphera','Watershed','Persefoni','Cority','Sweep','Position Green'],datasets:[{data:[96,92,76,75,75,73,67,67,65,63],backgroundColor:['#7a869a','#7a869a',signal,signal,signal,signal,signal,signal,signal,signal],borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' DR '+c.raw;}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9},maxRotation:60,minRotation:45},grid:{color:'transparent'}},y:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var kw=document.getElementById('kwChart');
  if(kw){new Chart(kw,{type:'bar',data:{labels:['Greenly','Workiva','Persefoni','Sweep','Sphera','Cority','Watershed','Position Green','Microsoft*','Salesforce*'],datasets:[{data:[11939,6207,1127,1093,878,626,370,248,220,130],backgroundColor:[up,up,signal,signal,signal,signal,signal,signal,neutral,neutral],borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.toLocaleString()+' ranked keywords';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9},maxRotation:60,minRotation:45},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v>=1000?(v/1000)+'k':v;}},grid:{color:grid}}}}});}

  var ci=document.getElementById('citeChart');
  if(ci){new Chart(ci,{type:'bar',data:{labels:['Greenly','Workiva','Sphera','Cority','Sweep','Persefoni','Watershed','Microsoft*','Position Green','Salesforce*'],datasets:[{data:[922,299,151,79,57,39,18,13,12,4],backgroundColor:[up,signal,signal,rgba(signal,0.8),rgba(signal,0.7),rgba(signal,0.6),rgba(signal,0.5),neutral,rgba(signal,0.4),neutral],borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' AI citations';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var by=document.getElementById('buyerChart');
  if(by){new Chart(by,{type:'bar',data:{labels:['emissions mgmt software','csrd software','scope 3 software','carbon mgmt software','esg reporting software','esg software','carbon accounting software','carbon footprint software'],datasets:[{data:[1,2,2,5,9,11,19,60],backgroundColor:[up,up,up,up,up,up,up,signal],borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' KD '+c.raw+' / 100';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid},title:{display:true,text:'Keyword difficulty (0-100)',color:text,font:{family:mono,size:10}}},y:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Carbon &amp; ESG &middot; GEO + SEO Teardown</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/carbon_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/carbon_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,"| h1:",hh.count("<h1"),
 "| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faq:",hh.count('faq-item'),"| cbcopy:",'cb-copy-css' in hh)
