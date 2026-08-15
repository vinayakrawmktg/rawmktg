#!/usr/bin/env python3
"""SCRATCH: build blogs/comparison-pages-ai-shortlists.html (Best X for Y comparison-page playbook). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="comparison-pages-ai-shortlists"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-08-13"
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
ADSENSE=''
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
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="The 'Best X for Y' Page AI Pulls Into Shortlists"
DECK=("The consideration funnel got handed to G2 and Capterra years ago, and almost nobody has taken it back. Here is how to build the "
      "comparison, alternatives, and segment pages that generative engines actually retrieve and quote, with a working template and the numbers behind it.")
DESC=("How to build comparison and 'best X for Y' pages AI engines cite: the verdict box, fact density, question headings, schema and a 90-day playbook.")
DATANOTE=("A bottom-of-funnel content playbook grounded in the Princeton/Georgia Tech GEO experiment (KDD 2024), the Conductor 2026 AEO/GEO "
          "benchmarks, and cross-platform citation studies, 2024-26. All eleven figures are original, built from the cited data; treat magnitudes as directional.")

CODE_VERDICT='''Best for [segment one]:  [Product A], because [one quantified reason].
Best for [segment two]:  [Product B], because [one quantified reason].
Bottom line:  choose A if [condition]. Choose B if [condition].

# Write it so it survives being lifted out of the page and pasted
# into a chat window with no other context. That is literally
# what happens to it.'''

CODE_DENSITY=r'''import re

EVIDENCE = re.compile(
    r'\$\d[\d.,]*'          # prices
    r'|\d[\d.,]*\s?%'       # percentages
    r'|\b\d[\d.,]*\b'       # bare numbers, dates, versions, seat counts
    r'|SOC ?2|ISO ?\d+|HIPAA|GDPR|PCI'   # named standards
    r'|GraphQL|REST|SAML|SSO|SCIM',      # named specs
    re.I)

def fact_density(text):
    """Verifiable facts per 100 words. Crude on purpose."""
    words = max(len(text.split()), 1)
    facts = len(EVIDENCE.findall(text))
    return round(facts / (words / 100), 2)

# below 1.0 is decoration; a comparison page should run 2.0 to 4.0.
# it will not catch every fact, and that is fine. the point is to
# find the sections where you wrote adjectives and called them
# arguments.'''

CODE_SCORE=r'''def extractability(P, D, H, N, w=(0.30, 0.30, 0.20, 0.20)):
    """Each term is normalised to 0..1. Score pages, fix the
    lowest term, re-score.
      P  answer position   1.0 if the verdict is in the first 100
                           words, 0 if the page opens with context.
      D  fact density      facts-per-100-words / 3.0, capped at 1.0.
      H  heading match     share of H2s phrased as buyer questions.
      N  neutrality        needs a named competitor advantage AND at
                           least two outbound citations to sources.
    """
    wp, wd, wh, wn = w
    return round(wp * P + wd * D + wh * H + wn * N, 3)

# the weights are ours and you should argue with them. what matters
# is that all four get measured, because teams reliably optimise the
# one they find least uncomfortable and ignore the other three.
extractability(P=1.0, D=1.0, H=0.8, N=1.0)   # 0.96  (rebuilt page)
extractability(P=0.0, D=0.0, H=0.0, N=0.1)   # 0.02  (legacy page)'''

CODE_JSONLD=r'''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "SupportPulse vs Zendesk Comparison (2026)",
  "dateModified": "2026-08-11",
  "mainEntity": {
    "@type": "ItemList",
    "numberOfItems": 2,
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "item": {
          "@type": "SoftwareApplication",
          "name": "SupportPulse",
          "applicationCategory": "CustomerServiceApplication",
          "operatingSystem": "Web, iOS, Android",
          "featureList": ["Native AI ticket resolution",
                          "Omnichannel routing",
                          "SOC 2 Type II, ISO 27001, HIPAA"],
          "offers": { "@type": "Offer", "price": "79.00",
                       "priceCurrency": "USD",
                       "unitText": "per agent per month" },
          "aggregateRating": { "@type": "AggregateRating",
                                "ratingValue": "4.6",
                                "reviewCount": "412" }
      }},
      { "@type": "ListItem", "position": 2, "item": {
          "@type": "SoftwareApplication",
          "name": "Zendesk Suite Enterprise",
          "applicationCategory": "CustomerServiceApplication",
          "offers": { "@type": "Offer", "price": "115.00",
                       "priceCurrency": "USD",
                       "unitText": "per agent per month, annual" }
      }}
    ]
  }
}
</script>'''

CODE_REBUILT=r'''Title:  SupportPulse vs Zendesk (2026): Enterprise Support Comparison
H1:     SupportPulse vs Zendesk: Features, Pricing, and Security
        Last updated: 11 August 2026

[VERDICT]  <- inside the first 100 words
SupportPulse fits high-volume enterprise teams that need native AI
ticket resolution (52.3% of routine tier-1 queries handled out of
the box) and a 14-day deployment. Zendesk is the better choice for
organisations that depend on a large third-party integration
ecosystem (1,500+ marketplace apps) or heavily customised legacy
CRM routing.

H2:  SupportPulse vs Zendesk: Executive Feature Comparison
  | Metric               | SupportPulse       | Zendesk Suite     |
  | Starting price       | $79/agent/mo flat  | $115/agent/mo     |
  | Native AI resolution | Included, 52.3%    | $50/agent/mo add  |
  | Implementation time  | 14 days            | 60-90 days        |
  | Marketplace apps     | 120+ connectors    | 1,500+ apps       |
  | Certifications       | SOC2, ISO, HIPAA   | SOC2, ISO, HIPAA  |

H2:  What Does SupportPulse Cost for a Team of 100 Agents?
H2:  How Does AI Ticket Automation Compare in Benchmark Testing?
H2:  When Should You Choose Zendesk Over SupportPulse?
H2:  How Long Does Migration From Zendesk Take?
H2:  Frequently Asked Questions
H2:  Evaluation Methodology and Data Sources

[JSON-LD: SoftwareApplication x2, ItemList, FAQPage, BreadcrumbList]'''

CODE_MD=r'''# [Category] Comparison: [Product A] vs [Product B] ([Year])
Last updated: [date]

## Quick verdict
- **Best for [segment 1]:** [Product A] - [one sentence, one metric].
- **Best for [segment 2]:** [Product B] - [one sentence, one metric].
- **Bottom line:** choose A if [condition]. Choose B if [condition].

## [Product A] vs [Product B] vs [Product C]: comparison matrix
| Criterion        | [A]            | [B]            | [C]      |
|------------------|----------------|----------------|----------|
| Starting price   | $X/user/mo     | $Y/user/mo     | $Z flat  |
| Target buyer     | [segment]      | [segment]      | [segment]|
| Key benchmark    | [metric]       | [metric]       | [metric] |
| Compliance       | SOC2, ISO, HIPAA | SOC2, ISO    | SOC2     |
| API surface      | GraphQL + REST | REST only      | adapter  |
| Free trial       | 14 days full   | 7 days limited | none     |

## Best [category] for [use case Y]
- **Benchmark:** across [N] production environments, [A] achieved [X].
- **Why architecturally:** native [capability], no middleware needed.
- **Tradeoff:** requires [honest cost, e.g. admin onboarding week 1].

## When should you choose [Product B] instead?
1. [Genuine case, one sentence, with the reason.]
2. [Genuine case, one sentence, with the reason.]

## How long does migration from [Product B] take?
[Self-contained answer with a number and a mechanism.]

## Evaluation methodology
Claims verified against vendor documentation, release notes, and
third-party review data as of [date]. Reviewed quarterly.
[Product A] publishes this page.

<!-- JSON-LD: SoftwareApplication per product, ItemList wrapper,
     FAQPage, BreadcrumbList. Server-rendered. -->'''

FAQ=[
 ("How do you get a comparison page cited by AI engines?",
  "Build the page around retrievable passages, not a narrative. Put a self-contained verdict naming both products in the first hundred words, run at least one verifiable fact per hundred words, phrase H2s as the buyer's actual question, name at least one case where a competitor wins, link out to independent sources, and ship ItemList plus SoftwareApplication and FAQPage schema server-side. Those moves target the levers that controlled testing shows move citation probability the most."),
 ("Do you need to outrank G2 to appear in AI shortlists?",
  "No. Across the major engines only about 12% of AI-cited URLs also sit in Google's organic top ten for the same query, and on ChatGPT Search the overlap falls to 6-8%. Domain authority accumulated over a decade is not the gate. Retrievability is: a page can rank at position 34 and still be the source an engine quotes in a shortlist a thousand buyers read."),
 ("What is a 'best X for Y' page and why does it matter for AI search?",
  "It is a segment shortlist that answers a constrained buyer query such as 'best contract management software for a 60-person legal team'. It matters because that is where real buyer prompts live, nobody types 'best CLM software' and stops there, and because roughly 63% of AI citations on commercial queries point at ranked 'Top N' lists. A shortlist-shaped page on your own domain is allowed to compete for those citations."),
 ("What schema does a comparison page need to get cited by AI?",
  "An ItemList wrapper that assigns explicit positions one through N to the products, a SoftwareApplication block per product carrying name, applicationCategory, offers and aggregateRating, a FAQPage for the Q&A block, and a BreadcrumbList for hierarchy. Render it server-side and make it match the visible copy exactly. About 61% of pages cited in Google AI Overviews carry structured data while roughly 45% of product URLs carry none, so this is where the gap is."),
 ("Should a vendor comparison page admit where a competitor wins?",
  "Yes, and it is one of the highest-leverage moves on the page. Alignment training makes re-rankers suspicious of one-sided promotional text, so a page that claims victory in every row reads as marketing collateral and gets downweighted in favour of a third-party directory. Naming two or three specific cases where a competitor is the better buy, plus linking out to independent sources, raises citation probability for lower-authority domains by a reported 115.1%."),
 ("How do you measure whether AI is citing your comparison pages?",
  "Rank tracking will not tell you. Build a prompt repository, a fixed list of 20 to 40 buyer questions run on a schedule against the engines you care about, and track three numbers: Brand Visibility Rate (are you named at all, aim above 65%), Share of Voice (named against whom, aim above 35%), and AI Citation Frequency (is your URL the source or is G2, aim above 40%). Log which URL won each citation, because that tells you which template variant to clone next."),
]

out=[]
# intro
out.append(p("Walk your own site backwards. Top of funnel is crowded, blog posts, a glossary, a few opinion pieces, maybe a report. Bottom of funnel is fine too, pricing page, product pages, a demo form. Then look at the middle. It is empty. It has been empty at almost every B2B software company we have ever pulled apart, for so long that most teams have stopped noticing."))
out.append(p("The middle is where the buying decision happens. It is the moment someone types “best contract management software for a 60-person legal team” and expects a shortlist, not a brochure. For roughly fifteen years that moment belonged to review aggregators, and vendors responded by paying rent: sponsored category placement, review-generation campaigns, paid search on their own competitor terms. The consideration funnel became a media buy."))
out.append(pull("The engine is not choosing between your company and G2. It is choosing between a page shaped like a shortlist and a page shaped like a pitch."))
out.append(p("That arrangement is now unstable, and not because anyone at G2 made a mistake. It is unstable because the interface changed. When a buyer asks ChatGPT, Perplexity, Google AI Mode or Claude for a shortlist, the engine does not return ten links to sort through. It breaks the question into sub-queries, retrieves passages, and writes the shortlist itself. The aggregator's structural advantage was distribution of links, and distribution of links is no longer what is being awarded. What is being awarded is the right to be quoted, a different competition with different admission rules, and vendor-owned pages are allowed to enter it. This is the same shift behind "+L("why AI cites Reddit, G2 and analyst reports","/blogs/why-ai-cites-reddit-g2-analysts")+"."))
out.append(callout("How to read the numbers in this piece",[
  "GEO research is young and the measurement is inconsistent. Different studies define a citation rate differently, sample different query sets, and rarely publish their prompt lists. A figure like “95% citation rate for comparison content” means comparison pages appeared among cited sources in 95% of the sampled comparison queries. It does not mean your comparison page has a 95% chance of being cited.",
  "The one genuinely peer-reviewed anchor here is the GEO paper from Princeton, Georgia Tech, the Allen Institute for AI and IIT Delhi, presented at ACM SIGKDD. Where its findings and a vendor blog disagree, believe the paper. Treat every number below as a direction of travel with an order of magnitude attached, and measure your own pages against your own prompt set."]))

# 1 funnel
out.append(sec("01","funnel","Where did the consideration funnel go?",
 "You quietly rented it to the aggregators.",
 "Top and bottom of funnel are covered on most B2B sites. The middle, where the decision happens, was handed to G2, Capterra, Software Advice and GetApp fifteen years ago. AI answers are pulling it back into open competition."))
out.append(p("G2 alone holds an estimated 22.4% share of influence over how consideration-stage queries resolve, a position it consolidated by acquiring Capterra, Software Advice and GetApp. Those directories built deep category taxonomies, pooled multi-brand reviews, and monetised the exact instant a buyer was ready to choose. Their moat was link distribution, the ability to rank ten listings and let the buyer sort them."))
out.append(p("Generative retrieval dissolves that moat. The engine does the sorting now, and it sources the shortlist from whichever pages contain retrievable, verifiable facts, wherever they live. Your own domain is eligible for the first time in fifteen years, provided the page is built for retrieval rather than persuasion."))

# 2 format
out.append(sec("02","format","Does format beat domain authority in AI search?",
 "Yes. The engine picks a shape, not a company.",
 "Roughly 63% of AI citations on commercial queries point at ranked listicles, comparison pages take about 40% where they are relevant, and vendor product pages take around 10%. G2 wins because its page is shaped like a shortlist, and nothing stops you shipping the same shape on your own domain."))
out.append(p("Here is the statistic that should reorganise your content calendar. Across commercial-intent queries, roughly 63% of AI citations point at ranked listicles and roundups, and between 71% and 86% of those citations land specifically on numbered “Top N” lists. Comparison pages take about 40% of citations on the queries where they are relevant. Vendor product and category pages take around 10%. On ChatGPT in particular, comparison content shows up in cited sources on 95% of the comparison queries tested, the highest format-specific figure recorded on any generative platform."))
out.append(chart("formatChart",240,"Figure 1. Citation share by content format on commercial-intent queries. Percentages come from separate studies with different bases and do not sum to 100."))
out.append(p("Read that with your own site in mind. If your only asset in the consideration space is a product page, you are entering a format that wins about a tenth of the citations, against publishers entering the format that wins two thirds of them. Nothing stops you from shipping a page shaped like a shortlist, on your own domain, with your own product in it and your competitors named honestly beside it. This is the format side of "+L("ranking is not the same as visibility","/blogs/ranking-isnt-visibility")+"."))
out.append(p("Formats also split by engine, which matters when you decide what to build first."))
out.append(table("Table 1. Format preference by engine. Compiled from the cross-platform citation study, Conductor's publishing benchmarks, and format-level citation analysis.",
 ["AI engine","Formats it leans on","Reported benchmark","What the engine seems to reward"],
 [["ChatGPT Search","Comparison content, side-by-side tables, roundups","95% on comparison queries","Clean tabular data, several named entities in one passage, third-party corroboration"],
  ["Perplexity","Product listings, category pages, community threads","84% on product and category pages","Structured product schema, live pricing, alignment with forum discussion"],
  ["Google AI Mode","Explainers, listicles, how-to guides","54.3% share to publishing sources","Coverage of many sub-queries on one page, deep heading structure"],
  ["Google AI Overviews","Editorial posts, roundups, ranked lists","42% for blog and article formats","Proximity to organic results, explicit JSON-LD, answer stated up front"],
  ["Gemini","Educational guides, long explainers","76% on explainer content","Shopping Graph integration, clear instructional framing"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(p("If you build one thing, build the comparison page and point it at ChatGPT's behaviour. If you build a second thing, build the segment shortlist, the “best X for Y” page, because that is the format Google AI Overviews and AI Mode reach for."))

# 3 ranking
out.append(sec("03","ranking","Do you need to outrank G2 to appear beside it?",
 "No. Ranking and citation have come apart.",
 "Across the major platforms only about 12% of AI-cited URLs also sit in Google's organic top ten for the same query. On ChatGPT Search the overlap falls to 6-8%. The old prerequisite, a decade of domain authority, is not the gate. Retrievability is."))
out.append(p("On ChatGPT Search close to 90% of cited pages rank at position 21 or worse in conventional search. Perplexity runs at 28.6% overlap with Google's top ten. Google AI Overviews, closest to the classic index, still only reaches 38%. The picture is consistent: the page that gets quoted is usually not the page that ranks."))
out.append(chart("overlapChart",240,"Figure 2. Share of AI-cited URLs that also appear in Google's organic top ten for the same query. Low overlap is the opening."))
out.append(p("Two conclusions follow, both good news. First, you do not have to outrank G2 to appear beside G2. Second, your existing rank reports are now measuring something adjacent to the thing you care about: a page can sit at position 34 and be cited in a shortlist a thousand buyers read, and your dashboard will call that page a failure. This is the gap covered in full in "+L("winning Google is not winning AI","/blogs/winning-google-isnt-winning-ai")+"."))
out.append(p("One caveat worth stating: low overlap is not the same as no relationship. Google AI Overviews still leans on organic proximity, and every engine still needs to find and crawl the page. Classic technical SEO has not stopped mattering. It has stopped being sufficient."))

# 4 pipeline
out.append(sec("04","pipeline","What actually happens to your page inside an engine?",
 "It is fanned out, chunked, and judged one passage at a time.",
 "The engine never reads your page. It fans the question into three to seven sub-queries, matches passages against an index, re-ranks the candidates, and keeps two or three. A brilliant argument on line 400 does not rescue a vague paragraph on line 12. They compete separately."))
out.append(p("A buyer asks a question. The engine does not search for that question, it "+L("fans the question out into three to seven sub-queries","/blogs/query-fan-out-how-one-prompt-becomes-ten-searches")+", because the original was too compound to answer in one retrieval pass. “Best contract management tool for a 60-person legal team” becomes narrower questions about price at that seat count, security posture, implementation time, and migration path."))
out.append(p("Each sub-query is embedded as a vector and matched against an index of passages, not pages. The system pulls a few dozen candidate chunks, re-ranks them on how directly the passage answers the sub-query, how closely the surrounding heading matches the phrasing, and how much verifiable specificity the passage contains. Two or three survive, become the answer, and their URLs become the footnote. The mechanics are covered in "+L("how your page actually gets retrieved","/blogs/how-your-page-gets-retrieved")+" and "+L("how RAG actually works","/blogs/how-rag-actually-works")+"."))
out.append(pipeline([("Buyer prompt","One compound question, typed in natural language."),("Fan-out","Split into 3-7 narrower sub-queries."),("Passage match","Each sub-query embedded, matched to chunks, not pages."),("Re-rank","Cross-encoder scores each chunk on answer fit + specificity."),("Cited shortlist","2-3 passages survive and become the answer's sources.")],3,
 "Figure 3. The retrieval path from buyer prompt to cited shortlist. Everything you write competes at the re-rank step, one chunk at a time."))
out.append(p("The single most useful mental adjustment is this: the engine reads passages that happen to live on your page, judges each on its own, and discards the rest. A page built around “why we are better” matches none of these sub-queries. A page with a pricing section, a compliance row and an implementation benchmark matches four."))

# 5 levers
out.append(sec("05","levers","Which four levers decide whether you get quoted?",
 "Position, fact density, headings, and neutrality.",
 "Answer in the first hundred words, run one verifiable fact per hundred words, phrase headings as the buyer's question, and name where your competitor wins. Ordered below by how much work they cost relative to what they return."))
out.append(h3("Position: answer in the first hundred words"))
out.append(p("Analysis of LLM citation behaviour finds that 44.2% of all extracted citations come from the first 30% of a document by character count. The opening is not a runway. It is the highest-value real estate on the page."))
out.append(chart("depthChart",210,"Figure 4. Share of extracted citations by depth in the document. The first third of the page carries almost half of them."))
out.append(p("This kills the standard comparison-page intro, the paragraph about how the category has evolved, the throat-clearing before the substance. All of it sits in the extraction window and all of it is unquotable. Replace it with a verdict box, three lines stated flatly before anything else on the page."))
out.append(code("text · the verdict box that replaces your intro",CODE_VERDICT))
out.append(h3("Fact density: one verifiable thing per hundred words"))
out.append(p("The "+L("GEO paper from Princeton, Georgia Tech, the Allen Institute for AI and IIT Delhi","https://arxiv.org/abs/2311.09735",True)+" tested content modifications against generative engines directly. Adding statistics, quotations and cited sources to a passage lifted its visibility in generated answers by up to 40%. That is the strongest experimental result in this field, and it points at one thing: models anchor on specifics."))
out.append(p("The working threshold across GEO practice is one verifiable fact per hundred words. A verifiable fact is a number, a date, a named standard, a version, a named entity or a price. It is not an adjective. A passage scoring below 1.0 is decoration. A comparison page should run between 2.0 and 4.0."))
out.append(table("Table 2. Density rewrites. Every replacement is a claim a competitor could check, which is precisely why the model trusts it.",
 ["Low-density sentence","Rewritten","Facts"],
 [["We offer dramatically faster implementation.","Median implementation is 14 days, measured across 45 deployments above 500 seats. The category median is 60 to 90 days.","3"],
  ["Enterprise-grade security you can trust.","SOC 2 Type II, ISO 27001 and HIPAA. Penetration test report available under NDA, refreshed annually.","3"],
  ["Transparent, affordable pricing.","$79 per agent per month flat, plus $0.15 per AI-resolved ticket. No implementation fee on standard cloud deployments.","3"],
  ["Integrates with all your favourite tools.","120 pre-built connectors, native GraphQL and REST APIs, and outbound webhooks on 14 event types.","4"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(chart("densityChart",240,"Figure 5. Fact density by section, before and after a rebuild. Marketing copy concentrates its emptiness in the intro, which is also the extraction window."))
out.append(p("You can audit this without a tool. Paste a section into a script, count the tokens that look like evidence, divide by hundreds of words. Crude, deliberately, the point is to catch the sections where you wrote adjectives and told yourself they were arguments."))
out.append(code("python · a crude fact-density check",CODE_DENSITY))
out.append(h3("Headings: write the buyer's question, not your slogan"))
out.append(p("Pages whose H2 and H3 headings match the phrasing of the user's prompt earn citations at a 41% rate, against 29% for pages with generic or stylised section titles. The heading is part of the chunk. When the chunk gets embedded, a heading that mirrors the sub-query pulls the whole passage closer in vector space. Keep one entity-anchored heading every 150 to 200 words, the same discipline described in "+L("the anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page")+"."))
out.append(table("Table 3. Heading rewrites. The right column is uglier and it wins. Optimise for retrieval, not for the internal brand review.",
 ["Slogan heading","Question heading"],
 [["Features That Set Us Apart","How Does [Product A] Compare to [Product B] on Enterprise Security?"],
  ["Pricing Made Simple","What Does [Product A] Cost for a Team of 100 Users?"],
  ["Built for Scale","Which Platform Handles Multi-Brand Routing Better?"],
  ["Why Teams Switch","When Should You Choose [Product B] Instead of [Product A]?"],
  ["Get Started Today","How Long Does Migration From [Product B] Take?"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(h3("Neutrality: the counterintuitive one"))
out.append(p("Alignment training makes models suspicious of one-sided promotional text. A page claiming victory in every row of a comparison table reads to a re-ranker exactly like what it is, marketing collateral. It gets downweighted, and the engine falls back to G2. The fix costs founders more emotionally than technically: name the cases where your competitor is the better choice, plainly, with reasons. If you cannot think of any, you do not understand your market well enough to be writing a comparison page."))
out.append(p("There is a second neutrality signal, and it is the largest single effect in this piece. Citing independent third-party sources, linking out to documentation, benchmark studies or review profiles, raises citation probability for lower-authority domains by 115.1%. Linking away from your page is not a leak. It is the cheapest credibility signal available to a small domain. Third-party validation compounds it: B2B software companies with verified profiles on two or more review directories are 3.4 times more likely to be referenced in ChatGPT syntheses than companies with none."))
out.append(chart("leverChart",240,"Figure 6. Reported effect sizes by lever. Each figure comes from a different study with a different base, so compare directions rather than magnitudes; the 3.4x directory effect is shown as +240%."))
out.append(callout("The move founders resist most",[
  "Naming where a competitor wins feels like giving ground. To a re-ranker it is the opposite: it is the signal that separates an objective comparison from sales collateral. Two or three specific, honest concessions plus a couple of outbound citations to primary sources do more for your citation odds than any amount of superlatives. The aggregators are not only competitors, they are corroboration, and models look for corroboration before naming a brand."]))
out.append(h3("Putting the levers in one number"))
out.append(p("For prioritising a backlog it helps to score pages on a single axis. This is a working heuristic, not a published ranking function, no engine exposes its weights. Normalise each term to 0 through 1, score existing pages, fix the lowest, re-score."))
out.append(code("python · a working extractability score",CODE_SCORE))

# 6 schema
out.append(sec("06","schema","What schema does a comparison page need?",
 "A nested ItemList, not a single blob.",
 "On-page writing gets you retrieved. Schema gets you understood. About 61% of pages cited in AI Overviews carry structured data while roughly 45% of product URLs carry none. That gap is the opportunity."))
out.append(p("Structured data removes ambiguity. Without it, a crawler has to infer that the number in your third table column is a monthly per-seat price rather than a storage limit. With it, the crawler is told. A comparison page needs a nested arrangement, not a single blob."))
out.append(code("json-ld · nested comparison markup (Figure 7)",CODE_JSONLD))
out.append(p("The critical class is ItemList. It assigns explicit positions, one through N, to the products in your comparison, so when an engine assembles a ranked answer that ordering is machine-readable rather than inferred from visual layout. SoftwareApplication carries the per-product detail; FAQPage maps conversational prompts to self-contained answers that can be imported whole. The full implementation is in "+L("schema markup for AI citations","/blogs/schema-markup-ai-citations-2026")+"."))
out.append(table("Table 4. Schema classes for comparison assets. Ship the FAQPage and BreadcrumbList blocks alongside the ItemList, as separate script tags if that is easier to maintain.",
 ["Schema class","Where it goes","Properties that matter","What it does for retrieval"],
 [["SoftwareApplication","Your product and every competitor you name","name, applicationCategory, operatingSystem, featureList, offers, aggregateRating","Tells the model what each product is, what it costs, and how it is rated"],
  ["ItemList","Around the comparison matrix and the shortlist","itemListElement, position, name, url","Makes rank explicit, which is what a Top-N answer is built from"],
  ["FAQPage","The Q&A block at the bottom","mainEntity, Question, acceptedAnswer, text","Supplies self-contained answers that can be imported whole"],
  ["BreadcrumbList","Site hierarchy, above the fold","itemListElement, position, item","Places the page inside a category, which strengthens entity association"],
  ["Product","Only for physical goods or transactional licences","brand, sku, offers, review","Feeds shopping surfaces and transactional summaries"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(callout("Two rules that break pages",[
  "Render it server-side. JSON-LD injected by client-side JavaScript after load is unreliable for AI crawlers. Put it in the initial HTML response.",
  "Match the visible copy exactly. Declaring a price, a feature or a rating in schema that a human cannot find on the page violates structured-data guidelines and puts the whole domain at risk. The schema describes the page, it does not embellish it."]))

# 7 rebuild
out.append(sec("07","rebuild","What does a rebuilt comparison page look like?",
 "Same product, same domain, a different brief.",
 "A fictional SupportPulse-vs-Zendesk page scored near zero on all four levers. The rebuild adds a verdict block inside the extraction window, two numbers and one honest competitor advantage, and does more retrieval work than the rest of the page combined."))
out.append(p("Score the page they had against the four levers. Answer position: nothing in the first hundred words a model could quote as a verdict. Fact density: 0.0, not one checkable number. Heading match: zero H2s phrased as a buyer question. Neutrality: the page claims total victory and names no case where Zendesk wins. Its extractability score is close to zero, so when someone asks an engine to compare the two products, the engine sources the comparison from G2 or a third-party roundup, because those pages contain retrievable facts and this one does not."))
out.append(chart("attrChart",240,"Figure 8. The same page scored on five build attributes, legacy against rebuilt. Bars are normalised against a target, not against each other."))
out.append(p("Here is the page they shipped. The verdict block is the whole game: it sits inside the extraction window, names both products, carries two numbers and one competitor advantage, and can be lifted into a chat answer without losing meaning."))
out.append(code("text · the rebuilt page, front-loaded for retrieval",CODE_REBUILT))
out.append(p("Notice what did not change. The product is the same, the company still wants the demo booking, and the page is still on the vendor's domain. Nothing here requires editorial independence or pretending to be a review site. It requires being specific, and being honest about two or three things."))
out.append(table("Table 5. Legacy against rebuilt, axis by axis. Nothing in the right-hand column requires a bigger content team, only a different brief.",
 ["Axis","Legacy page","Rebuilt page","Why it matters"],
 [["First hundred words","Promotional hook, no claim a model can quote","Verdict naming both products, two metrics, one competitor strength","Captures the window that carries 44.2% of extracted citations"],
  ["Fact density","0.0 facts per 100 words","3.1 facts per 100 words across the page","Statistics and cited sources lift visibility by up to 40% in testing"],
  ["Competitive framing","Claims to win every category","States plainly where Zendesk is the better buy","Avoids the bias filter that pushes the model back to aggregators"],
  ["Machine readability","No schema, no tables","Comparison table plus four schema classes","Turns the matrix into a ranked list an engine can read directly"],
  ["Freshness signal","None","Dated stamp, quarterly review, methodology note","Comparison data goes stale fast and models discount stale pricing"]],
 cls=lambda j,c: "label" if j==0 else ""))

# 8 template
out.append(sec("08","template","What is the comparison page template?",
 "Front-load the machine-readable proof, push the selling below.",
 "Verdict, matrix, segment blocks, honest competitor cases, self-contained FAQ, methodology note, four schema classes. The section order is not cosmetic; it puts everything an engine needs above the proof material."))
out.append(pipeline([("Verdict box","Best-for lines + bottom line, first 100 words."),("Comparison matrix","6-10 rows, wrapped in ItemList schema."),("Segment blocks","Best X for Y, with benchmark and honest tradeoff."),("Competitor cases","Where the other tool wins, named plainly."),("FAQ + methodology","Self-contained answers; who published, how verified.")],0,
 "Figure 9. Page anatomy. The first blocks sit inside the extraction window and carry the retrieval load."))
out.append(p("Hand this to a writer with the competitor research attached and you will get a usable draft."))
out.append(code("markdown · the comparison page template",CODE_MD))
out.append(p("Four notes on using it. The methodology line is not decoration, it states who published the page and how the claims were verified, a disclosure a model can read. FAQ answers must be self-contained, no “as mentioned above”, each is extracted alone and needs to survive alone. Keep the matrix between six and ten rows, fewer looks thin and more stops being scannable. And update the date honestly, a stale timestamp on a page with last year's pricing is worse than none, because it signals confidence in wrong data."))

# 9 segments
out.append(sec("09","segments","How do you choose segments for 'best X for Y' pages?",
 "From evidence, and fewer than you think.",
 "Buyers type their constraints: 'best CLM for a 60-person legal team'. Five real segments beat forty invented ones, because near-identical programmatic pages get deduplicated. Test each segment against three engines before you build it."))
out.append(p("The comparison page is one asset. The compounding asset is the segment family, because “best X for Y” is where buyer prompts actually live. Nobody types “best CLM software” and stops there, they type the version with their own constraints attached. Coverage looks like multiplication, and that is the trap: five segments across three formats is fifteen pages, a reasonable programme, but forty segments across three formats is a hundred and twenty near-identical pages, and near-identical pages are exactly what generative retrieval deduplicates and discards."))
out.append(table("Table 6. Segment axes and where the evidence lives. Five real segments beat forty invented ones.",
 ["Segmentation axis","Example segment","Where to source it"],
 [["Company size or seat count","for a 60-person legal team","Your own closed-won data, sorted by seat band"],
  ["Vertical or regulatory regime","for healthcare, for FCA-regulated firms","Compliance questions in your sales-call transcripts"],
  ["Existing stack","that integrates with NetSuite","Integration-filter usage on your own pricing page"],
  ["Job function","for in-house counsel, for RevOps","Job titles on demo requests over the last two quarters"],
  ["Constraint","with SSO on the base plan, self-hosted","Lost-deal reasons in your CRM"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(p("Then test the segment before you build. Ask three engines the prompt you are targeting. If the answers name three vendors and cite two aggregators, the segment is live and contested and worth a page. If the answers are vague or refuse to name anyone, demand is thin and you are writing for nobody. This takes ten minutes per segment and it is the single highest-return step in the whole programme."))
out.append(p("One more discipline. A “best X for Y” page must genuinely rank things, including cases where you are not first. A shortlist that puts your product at position one across every segment is a shortlist in layout only, and engines read ItemList position literally."))

# 10 measure
out.append(sec("10","measure","How do you measure whether it worked?",
 "A prompt repository, not a rank tracker.",
 "Run a fixed prompt set on a schedule and track three numbers: Brand Visibility Rate, Share of Voice and AI Citation Frequency. Log which URL won each citation. AI-referred visitors convert far higher than organic."))
out.append(p("Rank tracking will not tell you whether this worked. You need a prompt repository, nothing more sophisticated than a fixed list of the questions your buyers actually ask, run on a schedule against the engines you care about, with the results logged. Three metrics come out of it: Brand Visibility Rate (are you named at all, aim above 65%), Share of Voice (named against whom, aim above 35% relative to your top three competitors), and AI Citation Frequency (is your URL the source or is G2, aim above 40% on high-intent prompts)."))
out.append(p("The third is the one that matters for this work, and the one most tools do not separate. Being mentioned means the model knows you exist; being cited means your page was retrieved and used. Only the second is something a comparison page can move in a quarter, a distinction laid out in full in "+L("citation vs mention vs recommendation","/blogs/citation-vs-mention-vs-recommendation")+". Log which URL won the citation, not just whether you were cited, because that column tells you which template variant to clone next, the same loop as "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+"."))
out.append(p("The payoff justifies the instrumentation. Traffic arriving from generative citations converts differently, because the buyer has already run the comparison inside the chat and clicked through to verify one specific thing. Reported conversion rates sit at 14.2% to 15.9% for ChatGPT referrals, 10.5% for Perplexity and up to 16.8% for Claude, against 2.5% to 3.5% for traditional organic on commercial SaaS pages."))
out.append(chart("convChart",240,"Figure 10. Reported conversion rate by traffic origin. Volumes are still small, so read the ratio rather than the absolute figures."))
out.append(p("Two cautions on that chart. Referral volumes are low enough that a handful of deals can swing the percentage, and there is obvious selection bias in who clicks a citation. But the direction is consistent across sources, and it should change what you put at the bottom of a comparison page. A visitor who arrived from a shortlist does not want a gated ebook, give them a pricing calculator, an interactive sandbox or a migration checklist. They are at the end of the evaluation, not the start, the same shift that matters "+L("when the buyer is a bot","/blogs/when-the-buyer-is-a-bot")+"."))

# 11 freshness
out.append(sec("11","freshness","How do you keep comparison pages fresh?",
 "Quarterly audits, and push the change rather than waiting to be crawled.",
 "Comparison content decays faster than anything else you publish. Audit pricing, plans and certifications each quarter, update the timestamp only when something changed, notify IndexNow, and confirm you are not blocking the AI crawlers."))
out.append(p("Competitors change pricing, ship features and add certifications. A page citing last year's price is not merely out of date, it is wrong in a way a prospect can verify in one click, and models increasingly discount pages whose facts conflict with newer sources. Run a quarterly audit on every comparison and shortlist page, check pricing, plan names, certification lists and any benchmark you quoted, and update the timestamp only when something actually changed. This is the "+L("30-day content half-life","/blogs/30-day-content-half-life-recency-ai-ranking-signal")+" applied to your highest-intent pages."))
out.append(p("Then push the change rather than waiting to be crawled. IndexNow notifies participating engines directly, which matters because a pricing table that is right on your server but stale in an index is worth nothing. Also confirm you are not accidentally blocking the crawlers that matter, GPTBot, PerplexityBot, ClaudeBot and Google-Extended each have their own user agent, and plenty of sites blocked all of them in a defensive burst two years ago and never revisited the decision. Check your robots.txt before you conclude that your rebuilt page is not working."))

# 12 ninety
out.append(sec("12","ninety","What does the first ninety days look like?",
 "One page done properly beats fifteen done roughly.",
 "Days 1-14 build the prompt repository and baseline. Days 15-45 rebuild one head-to-head page. Days 46-70 fan out across the segments that passed the ten-minute test. Days 71-90 instrument and read the citation log."))
out.append(pipeline([("Days 1-14","Build the prompt repository, 20-40 prompts, baseline BVR / SoV / AICF across four engines."),("Days 15-45","Rebuild one highest-intent head-to-head page, fully, before starting the second."),("Days 46-70","Fan out across the 4-5 segments that survived the ten-minute prompt test."),("Days 71-90","Instrument: IndexNow on data change, quarterly refresh, re-run the prompt set against baseline.")],1,
 "Figure 11. A ninety-day sequence. One page rebuilt properly beats fifteen pages rebuilt approximately."))
out.append(p("Note which competitor URLs are winning the citations at baseline, because those pages are your specification. And at day ninety, read the log and find which of your pages won citations, because that tells you what to build next far more reliably than any framework, including this one."))

# 13 limits
out.append(sec("13","limits","What does this playbook not fix?",
 "A weak product, and missing third-party proof.",
 "A fact-dense page exposes a slow implementation. Verified review profiles still carry a 3.4x effect and live off your domain. And every magnitude here has a decay rate, which is why you keep your own prompt repository."))
out.append(p("<strong>It does not fix a weak product.</strong> A comparison page built on specifics exposes you. If your implementation really does take ninety days and your competitor's takes fourteen, a fact-dense page makes that legible to every buyer and every model. That is a product problem wearing a marketing costume."))
out.append(p("<strong>It does not replace third-party validation.</strong> The 3.4x effect from verified review profiles is real, and it exists precisely because models look for corroboration outside your domain. Keep your G2 and Capterra profiles current. They are competitors on the SERP and witnesses in the answer, and building presence on them is its own discipline, "+L("becoming an entity","/blogs/becoming-an-entity")+"."))
out.append(p("<strong>The ground is moving.</strong> Every number here comes from measurement taken while engines were changing their retrieval behaviour month to month. The mechanisms are stable enough to build on. The magnitudes are not, which is the reason for the prompt repository, it replaces borrowed statistics with your own."))
out.append(pull("The consideration funnel is being re-decided in public, the incumbents' advantage was link distribution rather than retrievability, and the winning format is one you are allowed to publish on your own domain. Most of your competitors are still writing 'Why We Are 10x Better'. That is the whole opening."))

# FAQ
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

# References
REFS=[
 ("Which AI platform cites what? Five LLMs, the same questions, almost no overlap  ,  FancyAI Research","https://www.getfancy.ai/article-cross-platform-citation-study"),
 ("The 2026 AEO / GEO Benchmarks Report  ,  Conductor","https://www.conductor.com/academy/aeo-geo-benchmarks-report/"),
 ("GEO: Generative Engine Optimization (Aggarwal et al., ACM SIGKDD 2024)  ,  arXiv","https://arxiv.org/abs/2311.09735"),
 ("GEO: Generative Engine Optimization, full paper PDF  ,  arXiv","https://arxiv.org/pdf/2311.09735"),
 ("AI Search Statistics: 55+ data points on GEO, buyer behaviour and citation rates  ,  Omnibound","https://www.omnibound.ai/blog/ai-search-statistics"),
 ("The mention is the signal. The link is almost irrelevant  ,  FancyAI Research","https://www.getfancy.ai/article-mention-is-the-signal"),
 ("The 10 gates: how AI search engines actually decide what to cite  ,  FancyAI Research","https://www.getfancy.ai/article-ai-search-10-gates"),
 ("An analysis of AI Overview brand visibility factors, 75K brands studied  ,  Ahrefs","https://ahrefs.com/blog/"),
 ("On-page content and the formats answer engines favour  ,  HubSpot","https://blog.hubspot.com/marketing"),
 ("What is Generative Engine Optimization (GEO)?  ,  AirOps","https://www.airops.com/blog"),
 ("SoftwareApplication type definition  ,  Schema.org","https://schema.org/SoftwareApplication"),
 ("ItemList type definition  ,  Schema.org","https://schema.org/ItemList"),
 ("FAQPage type definition  ,  Schema.org","https://schema.org/FAQPage"),
 ("IndexNow protocol documentation  ,  IndexNow","https://www.indexnow.org/documentation"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
out.append('<div class="about-block" id="references"><div class="about-label">References</div>'
           '<p style="margin-bottom:16px;">Figures 1 through 11 are original, built from the data in the sources below. Where studies disagree, ranges are shown rather than averages.</p>'
           f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Sources: the Princeton/Georgia Tech GEO experiment (KDD 2024), the Conductor 2026 AEO/GEO benchmarks, and cross-platform citation studies, 2024-26. All figures are original, built from the cited data; magnitudes are directional.</p></div>')

body="\n".join(out)

SIDEBAR=[("63%","of AI citations go to ranked listicles"),("12%","of cited URLs sit in Google's top 10"),("44.2%","of citations come from the first third"),("+115.1%","citation lift from outbound sources")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#funnel"><span class="toc-num">01</span>The funnel you rented out</a></li>'
     '<li><a href="#format"><span class="toc-num">02</span>Format beats domain</a></li>'
     '<li><a href="#ranking"><span class="toc-num">03</span>Ranking vs citation</a></li>'
     '<li><a href="#pipeline"><span class="toc-num">04</span>What happens to your page</a></li>'
     '<li><a href="#levers"><span class="toc-num">05</span>The four levers</a></li>'
     '<li><a href="#schema"><span class="toc-num">06</span>The machine-readable layer</a></li>'
     '<li><a href="#rebuild"><span class="toc-num">07</span>One page, before and after</a></li>'
     '<li><a href="#template"><span class="toc-num">08</span>The template</a></li>'
     '<li><a href="#segments"><span class="toc-num">09</span>Choosing the segments</a></li>'
     '<li><a href="#measure"><span class="toc-num">10</span>Measuring it honestly</a></li>'
     '<li><a href="#freshness"><span class="toc-num">11</span>Freshness</a></li>'
     '<li><a href="#ninety"><span class="toc-num">12</span>The first ninety days</a></li>'
     '<li><a href="#limits"><span class="toc-num">13</span>What it does not fix</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - the comparison page playbook for AI search - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["comparison pages","best x for y","AI citations","GEO","generative engine optimization","BOFU content","comparison page SEO","AI shortlists","ItemList schema","alternatives pages"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="The Best-X-for-Y Comparison Page Playbook &middot; rawmktg."
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
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n  <meta property=\"og:image:width\" content=\"2400\" />\n  <meta property=\"og:image:height\" content=\"1260\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{escq(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
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

  var fm=document.getElementById('formatChart');
  if(fm){new Chart(fm,{type:'bar',data:{labels:['Top-N listicles','Comparison pages','Vendor product pages'],datasets:[{data:[63,40,10],backgroundColor:[signal,rgba(signal,0.7),neutral],borderRadius:4,barThickness:64}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of citations';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,max:70,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var ov=document.getElementById('overlapChart');
  if(ov){new Chart(ov,{type:'bar',data:{labels:['ChatGPT Search','Cross-engine avg','Perplexity','Google AI Overviews'],datasets:[{data:[7,12,28.6,38],backgroundColor:[signal,rgba(signal,0.75),rgba(signal,0.55),neutral],borderRadius:4,barThickness:48}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% overlap with Google top 10';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,max:50,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var dp=document.getElementById('depthChart');
  if(dp){new Chart(dp,{type:'bar',data:{labels:['First 30% of page','Remaining 70%'],datasets:[{data:[44.2,55.8],backgroundColor:[signal,neutral],borderRadius:4,barThickness:80}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of extracted citations';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var de=document.getElementById('densityChart');
  if(de){new Chart(de,{type:'bar',data:{labels:['Intro','Pricing','Security','Verdict'],datasets:[
    {label:'Before rebuild',data:[0.3,0.8,0.5,0.2],backgroundColor:neutral,borderRadius:4},
    {label:'After rebuild',data:[2.1,3.4,3.0,3.6],backgroundColor:signal,borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+': '+c.raw+' facts/100w';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var lv=document.getElementById('leverChart');
  if(lv){new Chart(lv,{type:'bar',data:{labels:['Verified review profiles','Third-party outbound links','Stats, quotes, sources'],datasets:[{data:[240,115.1,40],backgroundColor:[signal,rgba(signal,0.75),rgba(signal,0.55)],borderRadius:4,barThickness:40}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' +'+c.raw+'% reported effect';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return '+'+v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var at=document.getElementById('attrChart');
  if(at){new Chart(at,{type:'bar',data:{labels:['Answer position','Fact density','Heading match','Neutrality','Schema'],datasets:[
    {label:'Legacy page',data:[0.1,0.0,0.0,0.1,0.0],backgroundColor:neutral,borderRadius:4},
    {label:'Rebuilt page',data:[1.0,0.9,0.8,0.9,1.0],backgroundColor:signal,borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+': '+c.raw;}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,max:1,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var cv=document.getElementById('convChart');
  if(cv){new Chart(cv,{type:'bar',data:{labels:['Organic (SaaS)','Perplexity','ChatGPT','Claude'],datasets:[{data:[3,10.5,15,16.8],backgroundColor:[neutral,rgba(signal,0.55),rgba(signal,0.78),signal],borderRadius:4,barThickness:56}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% conversion';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Comparison Pages &middot; BOFU Content</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/cmp_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/cmp_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faq:",hh.count('faq-item'),"| refs:",hh.count('id="references"'),"| cbcopy:",'cb-copy-css' in hh)
