#!/usr/bin/env python3
"""SCRATCH: build blogs/pricing-page-ai-will-quote.html"""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="pricing-page-ai-will-quote"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-09-16"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x").replace("−","-"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav',"</nav>"); NEWS=sl('<section class="newsletter-section',"</section>"); FOOT=sl('<footer class="site-foot',"</footer>")
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
def chart(cid,h,cap): return f'<div class="chart-wrap"><canvas id="{cid}" height="{h}"></canvas></div><div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="The Pricing Page AI Will Quote"
DECK=("Buyers ask AI what things cost, and the answer is assembled from whatever it can extract. If your price is trapped in an image, a "
      "\"contact us\", or a JavaScript widget, the model quotes a competitor or makes a number up. Here is how to write the page it lifts instead.")
DESC=("How to write a pricing page AI engines will quote: put real numbers in extractable text, lead with an answer block, add a comparison table, mark it up with Offer/PriceSpecification schema, and avoid the 'contact us' trap that makes AI cite a competitor or hallucinate your price.")
DATANOTE=("Grounded in RawMktg's own audit findings (pricing pages are rarely quoted when they carry no numbers), the answer-block and retrieval "
          "patterns behind AI citation, and 2026 GEO benchmarks on structured, extractable content. Directional where it says so.")

CODE_ANSWER=r'''<!-- The pricing answer block: price in the first sentence, above the fold, in real text. -->
<h1>How much does [Product] cost?</h1>

<p class="answer">
  [Product] costs <strong>$29/user/month on Starter, $59 on Growth, and $99 on
  Scale</strong> (billed annually; monthly is ~20% higher). The free plan covers
  up to 3 users. Enterprise is custom-quoted and starts around $2,000/month.
  There are no setup fees and you can change tiers at any time.
</p>

<h2>Plans and pricing at a glance</h2>
<table>
  <thead><tr><th>Plan</th><th>Price / user / mo</th><th>Best for</th></tr></thead>
  <tbody>
    <tr><td>Free</td><td>$0 (up to 3 users)</td><td>Trials and solo use</td></tr>
    <tr><td>Starter</td><td>$29</td><td>Small teams</td></tr>
    <tr><td>Growth</td><td>$59</td><td>Scaling teams</td></tr>
    <tr><td>Scale</td><td>$99</td><td>Larger teams</td></tr>
    <tr><td>Enterprise</td><td>Custom (~$2,000+/mo)</td><td>SSO, SLAs, procurement</td></tr>
  </tbody>
</table>'''

CODE_SCHEMA=r'''<!-- Offer / PriceSpecification schema: makes the numbers machine-readable, not inferred. -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product]",
  "offers": [
    {
      "@type": "Offer",
      "name": "Starter",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "price": "29.00",
        "priceCurrency": "USD",
        "unitText": "user/month",
        "billingIncrement": 1
      },
      "url": "https://example.com/pricing#starter",
      "availability": "https://schema.org/InStock"
    },
    {
      "@type": "Offer",
      "name": "Growth",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "price": "59.00", "priceCurrency": "USD", "unitText": "user/month"
      }
    }
  ]
}
</script>'''

out=[]; A=out.append

A(sec("01","wrong","Why does AI keep getting your pricing wrong?",
      "Because the number a model returns is only as good as what it can extract, and most pricing pages hand it nothing extractable: a price locked in an image, a JavaScript widget, or hidden behind 'contact sales'.",
      "When the page offers no lifted-out number, the model falls back to stale training data, a review site, or a competitor's page, and often just invents a figure."))
A(p("AI frequently gets SaaS pricing wrong, and the friction lands on you: a buyer arrives having been told the wrong number, or worse, a competitor's number. The cause is almost never that the model is careless. It is that a pricing answer has to be assembled from extractable facts, and a page built for a human, an interactive slider, a 'starting at' with the real tiers behind a toggle, a table rendered by JavaScript, gives a retrieval system nothing to lift."))
A(p("This is the same failure the "+L("clean-site-zero-citations teardown","/blogs/clean-site-zero-citations")+" found across an entire segment: pages with no pricing almost never get quoted when a buyer asks an AI what something costs. The fix is not more content. It is putting the actual numbers where a model can read them, in text, in a table, and in schema, and this piece is the how."))

A(sec("02","intent","Why is the pricing page worth optimising first?",
      "Because 'what does X cost' is a decision-stage question asked immediately before a purchase, and it is one of the highest-intent queries a buyer ever types into an AI.",
      "A model that quotes your price correctly does part of your sales qualification for you; one that quotes it wrong, or quotes a rival, costs you the deal before you know it existed."))
A(p("Pricing sits with comparisons and alternatives at the bottom of the funnel, the "+L("decision-stage pages that predict revenue","/blogs/comparison-pages-ai-shortlists")+". When a buyer asks an assistant \"how much is [Product] and what do you get\", they are minutes from a shortlist. The answer the model gives, your real tiers, a stale number, or a competitor's plan, shapes that shortlist directly."))
A(p("And unlike a thought-leadership post, a pricing page is cheap to fix and entirely in your control. You are not chasing a citation on someone else's site; you are making sure your own most commercial page is legible to the machine that is increasingly the first place buyers ask."))

A(sec("03","needs","What does AI actually need to quote a price?",
      "Three things, in order: the real numbers in extractable text, a clean comparison table, and Offer/PriceSpecification schema, all consistent with each other.",
      "Structured 'answer objects', an opening answer plus a quotable table, earn several times more citations than the same facts buried in prose."))
A(p("Think of it as three layers that reinforce each other. The text layer is the sentence a model can lift verbatim. The table layer is the structured comparison it can parse into tiers. The schema layer is the machine-readable declaration that removes all ambiguity. A page with all three is quotable three ways; a page with none is a guess."))
A(table("Table 1. What a model needs, and the common pricing-page failure that denies it.",
        ["What AI needs","Why","Common failure"],
        [["Real numbers in text","The chunk a retriever lifts verbatim","'Starting at' with tiers behind a toggle"],
         ["A comparison table","Parses into structured tiers and inclusions","Table rendered only by JavaScript"],
         ["Offer / PriceSpecification schema","Removes ambiguity; machine-readable","No schema, price must be inferred"],
         ["Consistency across all three","Conflicting numbers get discarded or averaged","Page says $29, schema says $25, G2 says $39"]]))

A(sec("04","answerblock","Where should the price go on the page?",
      "In an answer block in the first 40 to 55 words after the heading, stated plainly, with the actual numbers, before any marketing copy.",
      "That opening block is the window a retriever extracts. Lead with the answer; put the persuasion below it."))
A(p("The pattern is the same one behind every "+L("high-citation page","/blogs/anatomy-of-a-high-citation-page")+": a self-contained answer that stands on its own if lifted out of the page entirely. For pricing, that means the first thing after \"How much does [Product] cost?\" is the price of every tier in one readable sentence, not a value proposition, not a testimonial, not a slider."))
A(code("Code 1. The pricing answer block: real numbers in the first sentence, then a parseable table.",CODE_ANSWER))
A(p("Two rules make or break it. First, use real figures, not \"affordable\" or \"flexible\"; a model cannot quote an adjective. Second, keep the block in server-side HTML so a non-rendering crawler sees it, because "+L("the main AI crawlers do not reliably execute JavaScript","/blogs/do-ai-crawlers-render-javascript")+"."))

A(sec("05","numbers","What if your pricing is 'it depends'?",
      "Make the range quotable. Usage-based, tiered and custom pricing can all be extracted if you state the anchors, from, to, per-unit, and the typical case, in plain text.",
      "'Contact us' is the one answer a model cannot pass on, so give it something, even a floor and a representative example."))
A(p("Most B2B pricing is not a single number, and that is fine. What a model needs is the shape of the number: the entry price, the unit, and a representative example. \"From $500/month; most mid-market teams land around $1,500\" is quotable. \"Let's talk\" is not. The table below shows how to make each pricing model legible."))
A(table("Table 2. How to make each pricing model quotable.",
        ["Pricing model","What to publish","Example a model can lift"],
        [["Flat per-seat","Every tier's per-seat price","\"$29/$59/$99 per user per month\""],
         ["Usage-based","Unit price + a typical monthly bill","\"$0.002 per request; ~$400/mo at 200k requests\""],
         ["Tiered / bundled","Each tier's price and what changes between them","\"Growth adds SSO and doubles the API limit for $200/mo\""],
         ["Custom / enterprise","A published floor and a representative deal size","\"Enterprise starts ~$2,000/mo; typical deals $3k-$8k\""],
         ["Freemium","The free ceiling and first paid step","\"Free to 3 seats, then $29/seat\""]]))
A(callout("The 'contact us' trap",
    ["A pricing page with no number is not neutral, it is an instruction to the model to look elsewhere. It will quote a review site's estimate, a years-old figure from training data, or a competitor who did publish, and it may simply hallucinate a plausible-sounding price with your name attached.",
     "If procurement or strategy genuinely forbids a public price, publish a floor and a representative range anyway. A defensible \"from $X, typically $Y\" beats a confident wrong number you never got to see."]))

A(sec("06","schema","How do you mark up pricing so it is machine-readable?",
      "With Product plus Offer and PriceSpecification (UnitPriceSpecification for per-unit pricing) in JSON-LD, one Offer per tier, matching the visible numbers exactly.",
      "Schema does not replace the visible price, it confirms it, so a model does not have to infer the figure from prose."))
A(p("Structured data is the difference between a model reading your price and a model guessing it. "+L("The schema playbook","/blogs/schema-markup-ai-citations-2026")+" covers the full stack; for pricing specifically, the load-bearing types are Product, Offer, and PriceSpecification. Emit one Offer per plan, use UnitPriceSpecification for per-seat or per-unit pricing, and, critically, keep every number identical to what the page displays, mismatched schema is worse than none."))
A(code("Code 2. Offer / PriceSpecification JSON-LD, one Offer per tier, numbers matching the visible table.",CODE_SCHEMA))

A(sec("07","consistency","Why does AI show an old or wrong price even after you fix the page?",
      "Because models corroborate across sources, and if your page, your schema, and third-party listings (G2, Capterra, review posts) disagree, the model averages, picks the most-cited, or defaults to stale training data.",
      "Price parity across every surface is what makes the correct number win."))
A(p("Fixing your own page is necessary but not sufficient. A retrieval system assembling a pricing answer weighs corroboration: if four sources say $39 and your page says $29, the $29 is the outlier, and outliers get discarded. Audit where your price appears off-site, review platforms, directories, old blog posts, partner pages, and reconcile them to the current number. This is the pricing-specific case of "+L("keeping your entity consistent everywhere","/blogs/becoming-an-entity")+"."))
A(p("Freshness matters too. Update the visible price, the schema, and the dateModified together when pricing changes, and re-crawl the third-party listings you can edit. Models lean on recency, and a page that visibly changed last week beats one last touched two years ago."))

A(sec("08","retrievable","How do you make sure a crawler can actually read it?",
      "Serve the price, the table and the schema in server-side HTML, allow the AI crawlers in robots.txt, and check the raw fetch, not the rendered page.",
      "A price that only appears after JavaScript runs is invisible to the crawlers that feed most AI answers."))
A(p("The most common silent failure is a pricing table that renders client-side. To a human it looks perfect; to OAI-SearchBot or PerplexityBot fetching the raw HTML, the table is empty. View source (not the rendered DOM) and confirm the numbers are literally in the markup. Then confirm your robots.txt allows the search-and-retrieval crawlers, GPTBot, OAI-SearchBot, PerplexityBot and the rest, so the page can be pulled into answers at all. The mechanics are in "+L("how your page gets retrieved","/blogs/how-your-page-gets-retrieved")+"."))

A(sec("09","measure","How do you know it worked?",
      "Ask the engines. Run a prompt set of real pricing questions across ChatGPT, Perplexity, Gemini and Google AI, several times each, and check whether they quote your price, quote it correctly, and cite your page.",
      "Track three things: are you named, is the number right, and is your page the source, not a competitor's."))
A(p("A pricing fix has a uniquely clean success metric, because there is a factual right answer. Build a small portfolio of the questions buyers actually ask, \"how much does [Product] cost\", \"[Product] vs [Rival] pricing\", \"is [Product] worth it\", and run each several times per engine, because "+L("one run per prompt is noise","/blogs/share-of-model-measurement")+". Log whether your brand is named, whether the quoted figure matches your real price, and which URL is cited. A wrong number that names you is a corroboration problem (section 7); a right number that cites a competitor is a retrievability or answer-block problem (sections 4 and 8)."))

A(sec("10","checklist","The pricing-page checklist",
      "Ten checks that take an afternoon and decide whether an AI can quote you. Most pricing pages fail on the first three.",
      "Run this against your live page in view-source, not the rendered view."))
A(table("Table 3. The AI-quotable pricing-page checklist.",
        ["#","Check","Pass looks like"],
        [["1","Real numbers in text","Every tier's price is in server-side HTML, not an image or widget"],
         ["2","Answer block first","Price of all tiers in the first 40-55 words after the H1"],
         ["3","Comparison table","A parseable table of tiers and what changes between them"],
         ["4","Offer/PriceSpecification schema","One Offer per tier, numbers matching the page exactly"],
         ["5","Ranges for 'it depends'","Floor, unit, and a representative example published"],
         ["6","No naked 'contact us'","At least a floor and typical range, even for custom"],
         ["7","Off-site parity","G2, Capterra, directories reconciled to the current price"],
         ["8","Freshness","Visible price, schema and dateModified updated together"],
         ["9","Crawler access","robots.txt allows GPTBot, OAI-SearchBot, PerplexityBot"],
         ["10","Measured","A pricing prompt set run across engines, numbers verified"]],
        cls=lambda j,c:("num" if j==0 else "")))

A(sec("11","limits","What this does not fix",
      "A perfect pricing page gets your number quoted correctly; it does not, on its own, get you onto the shortlist.",
      "Being quoted accurately is table stakes for the buyers already asking about you. Getting recommended in the first place is a separate, off-site job."))
A(p("Two honest limits. First, a quotable price helps most when the buyer already names you, \"how much is [Product]\"; it does less for the category query, \"best [category] tools and their pricing\", where you also need to be in the "+L("comparison and alternatives pages the model pulls from","/blogs/comparison-pages-ai-shortlists")+" and corroborated across "+L("the off-site sources engines trust","/blogs/mentions-beat-links")+". Second, this is on-page hygiene: it removes the reasons a model cannot quote you. It does not manufacture the demand or authority that gets you named when the buyer has not heard of you yet."))

FAQ=[
 ("Why does ChatGPT show the wrong price for my product?",
  "Usually because your real numbers are not in extractable text. If the price sits in an image, a JavaScript-rendered widget, or behind 'contact sales', a model cannot lift it and falls back to stale training data, a review site's estimate, or a competitor's page, and sometimes invents a figure. Put every tier's price in server-side HTML, add an answer block and a table, mark it up with Offer schema, and reconcile any conflicting prices on third-party sites."),
 ("How do you optimise a pricing page for AI search?",
  "Lead with an answer block that states every tier's real price in the first 40-55 words after the heading; add a parseable comparison table; mark it up with Product/Offer/PriceSpecification JSON-LD whose numbers match the page exactly; publish ranges (floor, unit, typical case) instead of 'contact us'; serve it all in server-side HTML; reconcile off-site listings to the current price; and verify by running pricing prompts across engines."),
 ("Should you put pricing on your website for AI to find?",
  "Yes, at least a floor and a representative range. A page with no number is an instruction to the model to look elsewhere, and it will quote a review site, an old figure, or a competitor, or hallucinate a price with your name on it. If a public list price is genuinely impossible, publish 'from $X, typically $Y' so there is a defensible number for the model to cite."),
 ("What schema should a pricing page use?",
  "Product with one Offer per plan, and PriceSpecification (use UnitPriceSpecification for per-seat or per-unit pricing) carrying the price, currency and unit. Include availability and a URL per tier. The single most important rule is that every number in the schema matches the visible price exactly; mismatched schema is worse than none because it gives the model conflicting signals."),
 ("Why does AI still show an old price after I updated the page?",
  "Because models corroborate across sources. If your page now says $29 but G2, Capterra and old blog posts still say $39, the outlier gets discarded or averaged out. Update the visible price, the schema and the dateModified together, then reconcile every third-party listing you can edit. Recency also matters, a visibly recently-updated page outweighs a stale one."),
 ("Does AI read JavaScript-rendered pricing tables?",
  "Often not. The main AI search crawlers do not reliably execute JavaScript, so a table that renders client-side can look perfect to a human and be completely empty in the raw HTML a crawler fetches. Check view-source, not the rendered DOM, and confirm the numbers are literally in the markup. If they only appear after JS runs, the price is invisible to most AI answers."),
 ("How do you measure whether AI quotes your price correctly?",
  "Build a prompt set of the real pricing questions buyers ask ('how much does X cost', 'X vs Y pricing'), run each several times across ChatGPT, Perplexity, Gemini and Google AI, and log three things: whether your brand is named, whether the quoted figure matches your real price, and which URL is cited. A wrong number that names you is a corroboration problem; a right number citing a competitor is a retrievability or answer-block problem."),
]
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
A(faq_html)

REFS=[
 ("ChatGPT SEO & GEO 2026: 12 Tips To Get Cited In AI Answers. Yotpo.","https://www.yotpo.com/blog/chatgpt-seo-geo-tips/"),
 ("GEO: The Complete Guide to AI-First Content Optimization 2026. ToTheWeb.","https://totheweb.com/blog/beyond-seo-your-geo-checklist-mastering-content-creation-for-ai-search-engines/"),
 ("Generative Engine Optimization (GEO) for B2B: The Complete 2026 Guide. Mersel AI.","https://www.mersel.ai/generative-engine-optimization"),
 ("Product, Offer and PriceSpecification. Schema.org.","https://schema.org/Offer"),
 ("Merchant listing (product) structured data. Google Search Central.","https://developers.google.com/search/docs/appearance/structured-data/product"),
 ("Generative Engine Optimization (GEO): The 2026 Guide to AI Search Visibility. LLMrefs.","https://llmrefs.com/generative-engine-optimization"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
A('<div class="about-block" id="references"><div class="about-label">References</div>'
  '<p style="margin-bottom:16px;">The answer-block, schema and retrieval patterns draw on RawMktg\'s audit findings and the 2026 GEO sources below.</p>'
  f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
A('<div class="about-block"><div class="about-label">About rawmktg.</div>'
  '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("40-55","words: the answer block a retriever lifts"),("3 layers","text, table, schema, all consistent"),("~4x","citation lift from answer objects vs prose"),("0","the number 'contact us' gives a model")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#wrong"><span class="toc-num">01</span>Why AI gets pricing wrong</a></li>'
     '<li><a href="#intent"><span class="toc-num">02</span>Why optimise it first</a></li>'
     '<li><a href="#needs"><span class="toc-num">03</span>What AI needs to quote a price</a></li>'
     '<li><a href="#answerblock"><span class="toc-num">04</span>Where the price goes</a></li>'
     '<li><a href="#numbers"><span class="toc-num">05</span>When pricing is "it depends"</a></li>'
     '<li><a href="#schema"><span class="toc-num">06</span>Machine-readable markup</a></li>'
     '<li><a href="#consistency"><span class="toc-num">07</span>Why the old price persists</a></li>'
     '<li><a href="#retrievable"><span class="toc-num">08</span>Making it crawlable</a></li>'
     '<li><a href="#measure"><span class="toc-num">09</span>Knowing it worked</a></li>'
     '<li><a href="#checklist"><span class="toc-num">10</span>The checklist</a></li>'
     '<li><a href="#limits"><span class="toc-num">11</span>What it doesn\'t fix</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - pricing pages for AI search - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["pricing page SEO","pricing page for AI","AI search pricing","GEO","answer engine optimization","Offer schema","PriceSpecification","ChatGPT pricing","answer block","structured data pricing"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="How to Write a Pricing Page AI Will Quote &middot; rawmktg."
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
  var fc=document.getElementById('fmtChart');
  if(fc){new Chart(fc,{type:'bar',data:{labels:['Price in an image','"Contact us" only','Price in prose','Price + table','Price + table + schema'],datasets:[{data:[0,0,2,3,4],backgroundColor:[signal,signal,neutral,rgba(up,0.6),up],borderRadius:4,barThickness:38}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.raw===0?' effectively unquotable':' relative quotability: '+c.raw+'/4';}}}},
      scales:{x:{beginAtZero:true,max:4,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid},title:{display:true,text:'how quotable a model finds it (directional)',color:text,font:{family:mono,size:9}}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Content &amp; Authority &middot; Money Pages</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Sep 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body.replace('<h2 id="needs"',chart("fmtChart",260,"Figure 1. How quotable a pricing page is by format (directional). A price in an image or behind 'contact us' is effectively invisible to a model; text plus a table plus matching schema is quotable three ways.")+'\n<h2 id="needs"',1)
 +"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/ppq_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/ppq_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| jsonld_ok:",ok,"| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),
 "| code:",hh.count('class="code-block"'),"| callout:",hh.count('callout-box"'),"| faq:",len(re.findall('faq-item',hh)),"| outlinks:",len(re.findall(r'href="/(blogs|tools|methodology|features)',hh)))
