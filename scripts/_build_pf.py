#!/usr/bin/env python3
"""SCRATCH: build blogs/product-feeds-ai-shopping-agents.html"""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="product-feeds-ai-shopping-agents"; URL=f"https://rawmktg.com/blogs/{SLUG}"
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

HEADLINE="Product Feeds for AI Shopping Agents"
DECK=("An AI agent doing your customer's shopping never sees your storefront. It reads a structured feed and a handful of data fields, then "
      "decides whether to surface, compare, or buy your product. Here is how to be in the set it chooses from.")
DESC=("How to get your products recommended by AI shopping agents: the structured product feed, the fields that decide inclusion (price with ISO currency, availability, identifiers, images), Product/Offer schema, the 2026 discovery-vs-checkout settlement, the competing protocols (OpenAI ACP, Google UCP/AP2, Visa, Mastercard), and how to measure it.")
DATANOTE=("Figures are 2026 industry estimates (OpenAI Economic Research, Salesforce State of Marketing 2026, Adobe Analytics) and the protocol "
          "landscape is moving fast, OpenAI retired Instant Checkout in March 2026. Treat specifics as directional and confirm current feed specs with each platform.")

CODE_FEED=r'''# A single line of a product feed (JSONL), the unit an agent actually reads.
# Merchants push a gzip file (.jsonl.gz / .csv.gz / .xml.gz) to the platform endpoint,
# updated daily. This is the record, not your marketing page.
{
  "id": "SKU-10482",
  "title": "Aero Running Shoe, Men's, Volt",
  "description": "Lightweight road running shoe, 8mm drop, 220g. Breathable knit upper.",
  "link": "https://example.com/p/aero-running-shoe",
  "image_link": "https://example.com/img/aero-volt-1.jpg",
  "additional_image_link": ["https://example.com/img/aero-volt-2.jpg"],
  "price": "129.00 USD",              # price WITH ISO 4217 currency code
  "availability": "in_stock",         # in_stock | out_of_stock | preorder
  "inventory_quantity": 42,
  "gtin": "0195819023471",            # GTIN / MPN / brand = the identifiers agents match on
  "brand": "Aero",
  "condition": "new",
  "google_product_category": "Apparel & Accessories > Shoes",
  "shipping": "US:::5.99 USD",
  "return_policy": "30-day free returns",
  "enabled_for": ["search", "checkout"]   # eligibility flags the platform reads
}'''

CODE_SCHEMA=r'''<!-- Product + Offer schema on the PDP: the on-page truth an agent corroborates the feed against. -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Aero Running Shoe, Men's, Volt",
  "gtin": "0195819023471",
  "brand": {"@type": "Brand", "name": "Aero"},
  "image": ["https://example.com/img/aero-volt-1.jpg"],
  "offers": {
    "@type": "Offer",
    "price": "129.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "url": "https://example.com/p/aero-running-shoe",
    "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type":"MonetaryAmount","value":"5.99","currency":"USD"}},
    "hasMerchantReturnPolicy": {"@type":"MerchantReturnPolicy","returnPolicyCategory":"https://schema.org/MerchantReturnFiniteReturnWindow","merchantReturnDays":30}
  },
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "812"}
}
</script>'''

out=[]; A=out.append

A(sec("01","what","What is agentic commerce, and what changes for you?",
      "Agentic commerce is when an autonomous AI agent researches, compares and buys on a shopper's behalf: the human sets the intent, the agent handles discovery, comparison, and checkout or handoff.",
      "The practical change is that the agent never sees your storefront, your design, your copy, your CRO. It reads a structured feed and a few data fields, and decides from those."))
A(p("This is the sequel to "+L("when the buyer is a bot","/blogs/when-the-buyer-is-a-bot")+": that piece covered why agentic commerce matters and how the protocol stack works; this one is the operational how, how to structure your product data so an agent includes, compares and recommends you. The mindset shift is total. For twenty years, ecommerce optimisation meant persuading a human on a page. An agent is not persuaded by a page. It is fed a record, and it reasons over fields."))
A(p("The 2026 settlement made this concrete. After OpenAI retired Instant Checkout in March 2026, the industry converged on a division of labour: AI handles discovery and comparison, merchants keep checkout in their own environment. So the job is no longer 'sell to the agent'. It is 'be in the set the agent surfaces, with data clean enough to be chosen', then convert the human when the agent hands them back."))

A(sec("02","big","How big is agentic shopping, really?",
      "Big enough to plan for now. Roughly 50 million shopping queries a day already happen inside ChatGPT, AI agents drove about 20% of global orders in the 2025 holiday season ($262B), and AI-driven traffic to US retail sites grew 393% year over year in early 2026.",
      "This is not a horizon bet. The discovery layer has already moved; the question is whether your product data is ready for it."))
A(chart("shareChart",260,"Figure 1. AI agents drove roughly 20% of global orders in the 2025 holiday season (Salesforce). The discovery layer has already shifted; feeds are how you show up in it."))
A(p("The numbers describe a channel that is past the experimental stage. Around 50 million shopping queries a day run inside ChatGPT alone (about 2% of all its queries, per OpenAI's own research); Salesforce put AI agents behind roughly a fifth of global holiday orders; and Adobe measured a near-quadrupling of AI-referred traffic to US retail. The buyers are already asking agents what to buy. What decides the answer is not on your homepage, it is in your feed."))

A(sec("03","find","How does a shopping agent actually find your product?",
      "Through a structured product feed you push to the platform, plus corroborating data on the open web, not by crawling and interpreting your storefront.",
      "If you are not in the feed, or your feed record is incomplete, you are invisible to the agent no matter how good your site is."))
A(p("An agent assembles a shortlist the way a database query does: it reads structured records, filters on attributes (price, availability, category, eligibility), and ranks on signals it can compute (relevance, rating, price competitiveness). The primary source is the feed, a file you push to the platform, and the secondary source is corroboration from the open web, your PDP schema, reviews, and third-party listings. Both have to be clean and consistent, because "+L("an agent discards outliers the same way an AI answer does","/blogs/clean-site-zero-citations")+"."))

A(sec("04","feed","What is a product feed, and what do you push?",
      "A gzip-compressed file (.jsonl.gz, .csv.gz or .xml.gz) pushed to the platform's endpoint, usually updated daily, that lists every product with its price, availability, images, identifiers and eligibility flags.",
      "The feed record, not your web page, is the unit an agent reads. Treat it as your most important storefront."))
A(p("Mechanically, you push a compressed feed to an endpoint the platform provides (OpenAI's, for example), with daily updates accepted. Each record tells the agent what you sell, whether it is in stock, the price with its currency, the images, and the eligibility flags for search and checkout. Get the format right and you are in the catalogue; get a field wrong and the record is filtered out before a shopper ever sees it."))
A(code("Code 1. One product-feed record (JSONL). This is what the agent reads, not your PDP.",CODE_FEED))

A(sec("05","fields","Which fields decide whether you get included?",
      "Price with an ISO currency code, availability, a stable product identifier (GTIN/MPN/brand), images, category, and the platform's eligibility flags. Miss any and the record is filtered before ranking.",
      "Inclusion is a data-quality gate before it is a relevance contest, most products lose at the gate, not the ranking."))
A(table("Table 1. The feed fields that decide inclusion, and what a miss costs you.",
        ["Field","Why the agent needs it","What a miss costs"],
        [["price + ISO currency","Filter and comparison; '129.00 USD' not '$129'","Excluded from price-filtered and comparison queries"],
         ["availability / stock","Agents drop out-of-stock items","Surfaced then discarded, or never surfaced"],
         ["GTIN / MPN / brand","The identifier agents match and de-duplicate on","Not matched to the query or merged wrongly"],
         ["images","Required for most shopping surfaces","Record rejected or down-ranked"],
         ["product category","Routes you into the right query set","Shown for the wrong intents, or none"],
         ["eligibility flags","Platform's search/checkout gating","Silently excluded despite a valid product"]]))
A(p("The pattern mirrors the rest of GEO: inclusion is a gate you pass with clean, complete, machine-readable data, and only then does relevance and ranking decide the order. Most merchants lose products at the gate, an unpriced item, a stale stock status, a missing GTIN, long before any ranking logic runs."))

A(sec("06","schema","Does on-page Product schema still matter if the feed does the work?",
      "Yes. The feed gets you into the catalogue; Product/Offer schema on your PDP is the on-page truth an agent corroborates the feed against, and it is what web-crawling agents read when there is no feed.",
      "Feed and schema must agree, exactly, on price, availability and identifiers, or the agent trusts neither."))
A(p("Not every agent works from a pushed feed; some read the open web, and all of them cross-check. Product and Offer schema on the PDP, with the same GTIN, price, currency and availability as the feed, gives the agent a consistent second source. The "+L("schema playbook","/blogs/schema-markup-ai-citations-2026")+" covers the full stack; for shopping, the load-bearing types are Product, Offer, AggregateRating and the shipping/return details, all matching the feed to the character."))
A(code("Code 2. Product / Offer schema on the PDP, every value matching the feed record above.",CODE_SCHEMA))

A(sec("07","protocols","What are the competing agentic-commerce protocols?",
      "At least five launched between April 2025 and January 2026: OpenAI's Agentic Commerce Protocol (ACP), Google's UCP and AP2, Visa's Trusted Agent Protocol, and Mastercard's Agent Pay.",
      "You do not have to bet on one, but you do have to keep a clean, standards-shaped feed so you can plug into whichever your buyers use."))
A(table("Table 2. The agentic-commerce protocol landscape (2026). Roles overlap and are still shifting.",
        ["Protocol","Backer","What it governs"],
        [["Agentic Commerce Protocol (ACP)","OpenAI (with Stripe)","Product discovery and the agent-to-merchant commerce handshake in ChatGPT"],
         ["Universal Commerce Protocol (UCP)","Google","Merchant product and offer exchange for agentic surfaces"],
         ["Agent Payments Protocol (AP2)","Google","Authorising and executing agent-initiated payments"],
         ["Trusted Agent Protocol","Visa","Verifying that an agent is acting for a real cardholder"],
         ["Agent Pay","Mastercard","Tokenised, authenticated agent payments"]]))
A(p("The takeaway is not to master all five. It is that they all consume structured product and offer data, so a clean, well-identified feed and matching schema are the portable asset that lets you onboard to whichever protocol your buyers' agents adopt. Chase the data quality, not the protocol of the month."))

A(sec("08","discovery","Discovery or checkout, which is the job now?",
      "Discovery. Since the 2026 settlement, AI agents surface and compare while merchants keep checkout, so your goal is to be in the agent's shortlist with data clean enough to be chosen, then convert the human on your own site.",
      "You are optimising to be selected by the agent and handed a ready-to-buy human, not to close the sale inside the chat."))
A(p("OpenAI's retirement of Instant Checkout six months after launch reset expectations: the durable pattern is AI-led discovery, merchant-owned checkout. That is good news operationally, it means your conversion, payments and data stay in your environment, and the new work is narrow: get discovered and get chosen. The agent does the shortlisting; you win by being a clean, complete, competitively-priced record, and by keeping the checkout it hands off to fast and frictionless."))

A(sec("09","recommend","What makes an agent recommend you, not just list you?",
      "The same signals a human comparison uses, made machine-readable: competitive and correctly-formatted price, real availability, strong ratings, complete attributes, and corroboration across the web.",
      "Inclusion is data quality; recommendation is data quality plus the trust signals an agent can compute."))
A(p("Once you are in the set, the agent ranks. It rewards what it can verify: a price it can compare cleanly, stock it can trust, an "+L("aggregate rating and reviews corroborated off-site","/blogs/mentions-beat-links")+", and complete attributes that match the shopper's constraints (size, spec, compatibility). It penalises ambiguity, an item with no reviews, a vague category, or a price that disagrees between feed, PDP and third-party listings. Recommendation is won on the same axis as citation: be the cleanest, most corroborated, least ambiguous option."))

A(sec("10","hygiene","Why do products drop out of AI shopping results after they were showing?",
      "Feed drift. Stale stock status, a lapsed price, a failed daily update, or an eligibility flag flipping off silently removes products that were previously surfaced.",
      "An agent's catalogue is only as current as your last successful feed push, so feed hygiene is an operational discipline, not a one-time setup."))
A(p("The most common silent failure is not a bad initial feed, it is drift. A product sells out but the feed still says in_stock (so the agent surfaces it, the shopper bounces, and the platform down-ranks you); a price changes on the site but not the feed (so feed and PDP disagree and the agent distrusts both); a daily push fails and the whole catalogue goes stale. Monitor push success, reconcile feed against live stock and price daily, and treat feed health like uptime."))

A(sec("11","measure","How do you measure whether agents recommend you?",
      "Run real shopping prompts across the agentic surfaces your buyers use, several times each, and log whether your product is surfaced, how it ranks against rivals, and whether the price, stock and attributes it shows are correct.",
      "It is the Share-of-Model discipline applied to products instead of brands."))
A(p("Build a portfolio of the shopping questions your buyers ask an agent, 'best [product] for [use] under [price]', '[your product] vs [rival]', and run each several times across ChatGPT shopping, Google's agentic surfaces and the rest, because "+L("one run per prompt is noise","/blogs/share-of-model-measurement")+". Log three things: are you surfaced, where do you rank, and are the price/stock/attributes the agent shows correct. A wrong price or stale stock is a feed-hygiene failure (section 10); being absent entirely is an inclusion failure (sections 4 and 5)."))

A(sec("12","checklist","The AI-shopping-feed checklist",
      "Ten checks that decide whether an agent can find, trust and recommend your products. Most catalogues fail on identifiers or freshness.",
      "Run it against your live feed and a sample PDP, and reconcile the two."))
A(table("Table 3. The agent-ready product-feed checklist.",
        ["#","Check","Pass looks like"],
        [["1","Feed pushed to the platform","Valid .jsonl.gz/.csv.gz/.xml.gz at the endpoint"],
         ["2","Daily updates succeeding","Monitored push with success/failure alerts"],
         ["3","Price + ISO currency","'129.00 USD', not '$129', on every item"],
         ["4","Accurate availability","Stock status reconciled to live inventory daily"],
         ["5","Stable identifiers","GTIN/MPN/brand on every product"],
         ["6","Images","Primary + additional images per item"],
         ["7","Eligibility flags set","Enabled for search (and checkout where used)"],
         ["8","PDP schema matches feed","Product/Offer values identical to the feed"],
         ["9","Ratings & reviews present","AggregateRating populated and corroborated off-site"],
         ["10","Measured","Shopping prompts run across agents, accuracy verified"]],
        cls=lambda j,c:("num" if j==0 else "")))

A(sec("13","limits","What a feed won't do",
      "A perfect feed gets you found and fairly compared; it will not make an uncompetitive product win, and it does not replace the human conversion you still own.",
      "Data quality is the entry ticket, not the whole game."))
A(p("Two honest limits. First, an agent recommends on merits it can compute, so a clean feed surfaces an over-priced or poorly-reviewed product accurately as over-priced and poorly-reviewed; the feed removes the reasons you are wrongly excluded, it does not fix the product or the price. Second, because the 2026 settlement keeps checkout with you, the handed-off human still has to convert on your site, so a fast, low-friction "+L("pricing and checkout experience","/blogs/pricing-page-ai-will-quote")+" still matters. The feed wins the shortlist; you still close the sale."))

FAQ=[
 ("What is agentic commerce?",
  "Agentic commerce is when an autonomous AI agent researches, compares and buys products on a shopper's behalf: the human sets the intent and the agent handles discovery, comparison, and checkout or handoff. It differs from conversational commerce (which assists a human shopping in chat) by delegating the decision and, sometimes, the transaction to the agent. Since 2026 the common pattern is AI-led discovery with checkout kept in the merchant's environment."),
 ("How do AI shopping agents find products?",
  "Primarily through a structured product feed the merchant pushes to the platform, a gzip-compressed file (.jsonl.gz, .csv.gz or .xml.gz) updated daily with each product's price, availability, images, identifiers and eligibility flags, and secondarily through corroborating web data such as Product/Offer schema on your PDP and third-party listings. The agent reads records and fields, not your storefront design, so if you are not in the feed you are invisible to it."),
 ("What fields does a product feed need for AI shopping agents?",
  "At minimum a stable identifier (GTIN/MPN/brand), a price with its ISO currency code (e.g. '129.00 USD'), an availability/stock status, images, a product category, and the platform's eligibility flags for search and checkout. Inclusion is a data-quality gate: a missing identifier, an unpriced item, or a stale stock status filters the product out before any ranking happens."),
 ("Do I still need Product schema if I have a feed?",
  "Yes. The feed gets you into the catalogue, but Product and Offer schema on your product page is the on-page truth agents corroborate the feed against, and it is what web-crawling agents read when there is no feed. The critical rule is that the schema and the feed must agree exactly on price, currency, availability and identifiers; if they disagree, the agent trusts neither."),
 ("What are the agentic-commerce protocols (ACP, UCP, AP2)?",
  "At least five launched between April 2025 and January 2026: OpenAI's Agentic Commerce Protocol (ACP, with Stripe) for discovery and the commerce handshake in ChatGPT; Google's Universal Commerce Protocol (UCP) for merchant product exchange and its Agent Payments Protocol (AP2) for agent-initiated payments; Visa's Trusted Agent Protocol for verifying an agent acts for a real cardholder; and Mastercard's Agent Pay for tokenised agent payments. All consume structured product data, so a clean feed and matching schema are the portable asset."),
 ("Why did my product stop showing in AI shopping results?",
  "Almost always feed drift. If the item sells out but the feed still says in_stock, if a price changes on the site but not the feed, or if a daily feed push fails, the agent either surfaces stale data (and down-ranks you when shoppers bounce) or drops the product. An agent's catalogue is only as current as your last successful push, so reconcile the feed against live stock and price daily and monitor push success."),
 ("How do you get an AI agent to recommend your product, not just list it?",
  "Inclusion is data quality; recommendation adds the trust signals an agent can compute: a competitive, correctly-formatted price, accurate availability, a populated aggregate rating corroborated by off-site reviews, and complete attributes that match the shopper's constraints. Agents penalise ambiguity, no reviews, a vague category, or a price that disagrees across feed, PDP and third-party listings, so be the cleanest, most corroborated, least ambiguous option."),
]
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
A(faq_html)

REFS=[
 ("ChatGPT Commerce & Agentic Shopping Statistics 2026. Elogic.","https://elogic.co/blog/chatgpt-commerce-statistics/"),
 ("ChatGPT Instant Checkout: What Happened to It in 2026. Hypotenuse.","https://www.hypotenuse.ai/blog/chatgpts-instant-checkout-the-next-phase-of-agentic-commerce"),
 ("AI Shopping Assistant Guide 2026: Agentic Commerce Protocols. Opascope.","https://opascope.com/insights/ai-shopping-assistant-guide-2026-agentic-commerce-protocols/"),
 ("ChatGPT Instant Checkout: ACP Protocol Retailer Guide (2026). Ekamoira.","https://www.ekamoira.com/blog/chatgpt-instant-checkout-agentic-commerce-protocol-2026"),
 ("Agentic Commerce in 2026: How AI Agents Buy Products. Paz.ai.","https://www.paz.ai/agentic-commerce"),
 ("Product structured data (Product, Offer). Google Search Central.","https://developers.google.com/search/docs/appearance/structured-data/product"),
 ("Product and Offer types. Schema.org.","https://schema.org/Product"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
A('<div class="about-block" id="references"><div class="about-label">References</div>'
  '<p style="margin-bottom:16px;">Market figures and the protocol landscape are 2026 industry estimates from the sources below; specifics move fast, confirm current feed specs with each platform.</p>'
  f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
A('<div class="about-block"><div class="about-label">About rawmktg.</div>'
  '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("~50M","shopping queries a day inside ChatGPT"),("20%","of 2025 holiday orders driven by AI agents"),("+393%","YoY growth in AI-referred US retail traffic"),("5","competing agentic-commerce protocols")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#what"><span class="toc-num">01</span>What changes for you</a></li>'
     '<li><a href="#big"><span class="toc-num">02</span>How big it is</a></li>'
     '<li><a href="#find"><span class="toc-num">03</span>How agents find products</a></li>'
     '<li><a href="#feed"><span class="toc-num">04</span>The product feed</a></li>'
     '<li><a href="#fields"><span class="toc-num">05</span>The fields that decide inclusion</a></li>'
     '<li><a href="#schema"><span class="toc-num">06</span>Product schema</a></li>'
     '<li><a href="#protocols"><span class="toc-num">07</span>The protocol landscape</a></li>'
     '<li><a href="#discovery"><span class="toc-num">08</span>Discovery vs checkout</a></li>'
     '<li><a href="#recommend"><span class="toc-num">09</span>Getting recommended</a></li>'
     '<li><a href="#hygiene"><span class="toc-num">10</span>Feed hygiene</a></li>'
     '<li><a href="#measure"><span class="toc-num">11</span>Measuring it</a></li>'
     '<li><a href="#checklist"><span class="toc-num">12</span>The checklist</a></li>'
     '<li><a href="#limits"><span class="toc-num">13</span>What it won\'t do</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - getting recommended by AI shopping agents - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["agentic commerce","AI shopping agents","product feed","Agentic Commerce Protocol","ACP","Product schema","ChatGPT shopping","AI checkout","get recommended by AI","merchant feed"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Product Feeds for AI Shopping Agents &middot; rawmktg."
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
  var sc=document.getElementById('shareChart');
  if(sc){new Chart(sc,{type:'doughnut',data:{labels:['AI-agent-driven orders','Everything else'],datasets:[{data:[20,80],backgroundColor:[signal,neutral],borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'64%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of 2025 holiday orders';}}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">How AI Search Works &middot; Agentic Commerce</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Sep 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/pf_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/pf_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| jsonld_ok:",ok,"| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),
 "| code:",hh.count('class="code-block"'),"| callout:",hh.count('callout-box"'),"| faq:",len(re.findall('faq-item',hh)),"| outlinks:",len(re.findall(r'href="/(blogs|tools|methodology|features)',hh)))
