# Product Feeds for AI Shopping Agents

> An AI agent doing your customer's shopping never sees your storefront. It reads a structured feed and a handful of data fields, then decides whether to surface, compare, or buy your product. Here is how to be in the set it chooses from.

*Source: https://rawmktg.com/blogs/product-feeds-ai-shopping-agents · rawmktg. by Vinayak Ravi*


## 01. What is agentic commerce, and what changes for you?

**Agentic commerce is when an autonomous AI agent researches, compares and buys on a shopper's behalf: the human sets the intent, the agent handles discovery, comparison, and checkout or handoff.** The practical change is that the agent never sees your storefront, your design, your copy, your CRO. It reads a structured feed and a few data fields, and decides from those.

This is the sequel to [when the buyer is a bot](/blogs/when-the-buyer-is-a-bot): that piece covered why agentic commerce matters and how the protocol stack works; this one is the operational how, how to structure your product data so an agent includes, compares and recommends you. The mindset shift is total. For twenty years, ecommerce optimisation meant persuading a human on a page. An agent is not persuaded by a page. It is fed a record, and it reasons over fields.

The 2026 settlement made this concrete. After OpenAI retired Instant Checkout in March 2026, the industry converged on a division of labour: AI handles discovery and comparison, merchants keep checkout in their own environment. So the job is no longer 'sell to the agent'. It is 'be in the set the agent surfaces, with data clean enough to be chosen', then convert the human when the agent hands them back.

## 02. How big is agentic shopping, really?

**Big enough to plan for now. Roughly 50 million shopping queries a day already happen inside ChatGPT, AI agents drove about 20% of global orders in the 2025 holiday season ($262B), and AI-driven traffic to US retail sites grew 393% year over year in early 2026.** This is not a horizon bet. The discovery layer has already moved; the question is whether your product data is ready for it.

Figure 1. AI agents drove roughly 20% of global orders in the 2025 holiday season (Salesforce). The discovery layer has already shifted; feeds are how you show up in it.

The numbers describe a channel that is past the experimental stage. Around 50 million shopping queries a day run inside ChatGPT alone (about 2% of all its queries, per OpenAI's own research); Salesforce put AI agents behind roughly a fifth of global holiday orders; and Adobe measured a near-quadrupling of AI-referred traffic to US retail. The buyers are already asking agents what to buy. What decides the answer is not on your homepage, it is in your feed.

## 03. How does a shopping agent actually find your product?

**Through a structured product feed you push to the platform, plus corroborating data on the open web, not by crawling and interpreting your storefront.** If you are not in the feed, or your feed record is incomplete, you are invisible to the agent no matter how good your site is.

An agent assembles a shortlist the way a database query does: it reads structured records, filters on attributes (price, availability, category, eligibility), and ranks on signals it can compute (relevance, rating, price competitiveness). The primary source is the feed, a file you push to the platform, and the secondary source is corroboration from the open web, your PDP schema, reviews, and third-party listings. Both have to be clean and consistent, because [an agent discards outliers the same way an AI answer does](/blogs/clean-site-zero-citations).

## 04. What is a product feed, and what do you push?

**A gzip-compressed file (.jsonl.gz, .csv.gz or .xml.gz) pushed to the platform's endpoint, usually updated daily, that lists every product with its price, availability, images, identifiers and eligibility flags.** The feed record, not your web page, is the unit an agent reads. Treat it as your most important storefront.

Mechanically, you push a compressed feed to an endpoint the platform provides (OpenAI's, for example), with daily updates accepted. Each record tells the agent what you sell, whether it is in stock, the price with its currency, the images, and the eligibility flags for search and checkout. Get the format right and you are in the catalogue; get a field wrong and the record is filtered out before a shopper ever sees it.

Code 1. One product-feed record (JSONL). This is what the agent reads, not your PDP.

```
# A single line of a product feed (JSONL), the unit an agent actually reads.
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
}
```

## 05. Which fields decide whether you get included?

**Price with an ISO currency code, availability, a stable product identifier (GTIN/MPN/brand), images, category, and the platform's eligibility flags. Miss any and the record is filtered before ranking.** Inclusion is a data-quality gate before it is a relevance contest, most products lose at the gate, not the ranking.

Table 1. The feed fields that decide inclusion, and what a miss costs you.

| Field | Why the agent needs it | What a miss costs |
| --- | --- | --- |
| price + ISO currency | Filter and comparison; '129.00 USD' not '$129' | Excluded from price-filtered and comparison queries |
| availability / stock | Agents drop out-of-stock items | Surfaced then discarded, or never surfaced |
| GTIN / MPN / brand | The identifier agents match and de-duplicate on | Not matched to the query or merged wrongly |
| images | Required for most shopping surfaces | Record rejected or down-ranked |
| product category | Routes you into the right query set | Shown for the wrong intents, or none |
| eligibility flags | Platform's search/checkout gating | Silently excluded despite a valid product |

The pattern mirrors the rest of GEO: inclusion is a gate you pass with clean, complete, machine-readable data, and only then does relevance and ranking decide the order. Most merchants lose products at the gate, an unpriced item, a stale stock status, a missing GTIN, long before any ranking logic runs.

## 06. Does on-page Product schema still matter if the feed does the work?

**Yes. The feed gets you into the catalogue; Product/Offer schema on your PDP is the on-page truth an agent corroborates the feed against, and it is what web-crawling agents read when there is no feed.** Feed and schema must agree, exactly, on price, availability and identifiers, or the agent trusts neither.

Not every agent works from a pushed feed; some read the open web, and all of them cross-check. Product and Offer schema on the PDP, with the same GTIN, price, currency and availability as the feed, gives the agent a consistent second source. The [schema playbook](/blogs/schema-markup-ai-citations-2026) covers the full stack; for shopping, the load-bearing types are Product, Offer, AggregateRating and the shipping/return details, all matching the feed to the character.

Code 2. Product / Offer schema on the PDP, every value matching the feed record above.

```
<!-- Product + Offer schema on the PDP: the on-page truth an agent corroborates the feed against. -->
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
</script>
```

## 07. What are the competing agentic-commerce protocols?

**At least five launched between April 2025 and January 2026: OpenAI's Agentic Commerce Protocol (ACP), Google's UCP and AP2, Visa's Trusted Agent Protocol, and Mastercard's Agent Pay.** You do not have to bet on one, but you do have to keep a clean, standards-shaped feed so you can plug into whichever your buyers use.

Table 2. The agentic-commerce protocol landscape (2026). Roles overlap and are still shifting.

| Protocol | Backer | What it governs |
| --- | --- | --- |
| Agentic Commerce Protocol (ACP) | OpenAI (with Stripe) | Product discovery and the agent-to-merchant commerce handshake in ChatGPT |
| Universal Commerce Protocol (UCP) | Google | Merchant product and offer exchange for agentic surfaces |
| Agent Payments Protocol (AP2) | Google | Authorising and executing agent-initiated payments |
| Trusted Agent Protocol | Visa | Verifying that an agent is acting for a real cardholder |
| Agent Pay | Mastercard | Tokenised, authenticated agent payments |

The takeaway is not to master all five. It is that they all consume structured product and offer data, so a clean, well-identified feed and matching schema are the portable asset that lets you onboard to whichever protocol your buyers' agents adopt. Chase the data quality, not the protocol of the month.

## 08. Discovery or checkout, which is the job now?

**Discovery. Since the 2026 settlement, AI agents surface and compare while merchants keep checkout, so your goal is to be in the agent's shortlist with data clean enough to be chosen, then convert the human on your own site.** You are optimising to be selected by the agent and handed a ready-to-buy human, not to close the sale inside the chat.

OpenAI's retirement of Instant Checkout six months after launch reset expectations: the durable pattern is AI-led discovery, merchant-owned checkout. That is good news operationally, it means your conversion, payments and data stay in your environment, and the new work is narrow: get discovered and get chosen. The agent does the shortlisting; you win by being a clean, complete, competitively-priced record, and by keeping the checkout it hands off to fast and frictionless.

## 09. What makes an agent recommend you, not just list you?

**The same signals a human comparison uses, made machine-readable: competitive and correctly-formatted price, real availability, strong ratings, complete attributes, and corroboration across the web.** Inclusion is data quality; recommendation is data quality plus the trust signals an agent can compute.

Once you are in the set, the agent ranks. It rewards what it can verify: a price it can compare cleanly, stock it can trust, an [aggregate rating and reviews corroborated off-site](/blogs/mentions-beat-links), and complete attributes that match the shopper's constraints (size, spec, compatibility). It penalises ambiguity, an item with no reviews, a vague category, or a price that disagrees between feed, PDP and third-party listings. Recommendation is won on the same axis as citation: be the cleanest, most corroborated, least ambiguous option.

## 10. Why do products drop out of AI shopping results after they were showing?

**Feed drift. Stale stock status, a lapsed price, a failed daily update, or an eligibility flag flipping off silently removes products that were previously surfaced.** An agent's catalogue is only as current as your last successful feed push, so feed hygiene is an operational discipline, not a one-time setup.

The most common silent failure is not a bad initial feed, it is drift. A product sells out but the feed still says in\_stock (so the agent surfaces it, the shopper bounces, and the platform down-ranks you); a price changes on the site but not the feed (so feed and PDP disagree and the agent distrusts both); a daily push fails and the whole catalogue goes stale. Monitor push success, reconcile feed against live stock and price daily, and treat feed health like uptime.

## 11. How do you measure whether agents recommend you?

**Run real shopping prompts across the agentic surfaces your buyers use, several times each, and log whether your product is surfaced, how it ranks against rivals, and whether the price, stock and attributes it shows are correct.** It is the Share-of-Model discipline applied to products instead of brands.

Build a portfolio of the shopping questions your buyers ask an agent, 'best [product] for [use] under [price]', '[your product] vs [rival]', and run each several times across ChatGPT shopping, Google's agentic surfaces and the rest, because [one run per prompt is noise](/blogs/share-of-model-measurement). Log three things: are you surfaced, where do you rank, and are the price/stock/attributes the agent shows correct. A wrong price or stale stock is a feed-hygiene failure (section 10); being absent entirely is an inclusion failure (sections 4 and 5).

## 12. The AI-shopping-feed checklist

**Ten checks that decide whether an agent can find, trust and recommend your products. Most catalogues fail on identifiers or freshness.** Run it against your live feed and a sample PDP, and reconcile the two.

Table 3. The agent-ready product-feed checklist.

| # | Check | Pass looks like |
| --- | --- | --- |
| 1 | Feed pushed to the platform | Valid .jsonl.gz/.csv.gz/.xml.gz at the endpoint |
| 2 | Daily updates succeeding | Monitored push with success/failure alerts |
| 3 | Price + ISO currency | '129.00 USD', not '$129', on every item |
| 4 | Accurate availability | Stock status reconciled to live inventory daily |
| 5 | Stable identifiers | GTIN/MPN/brand on every product |
| 6 | Images | Primary + additional images per item |
| 7 | Eligibility flags set | Enabled for search (and checkout where used) |
| 8 | PDP schema matches feed | Product/Offer values identical to the feed |
| 9 | Ratings & reviews present | AggregateRating populated and corroborated off-site |
| 10 | Measured | Shopping prompts run across agents, accuracy verified |

## 13. What a feed won't do

**A perfect feed gets you found and fairly compared; it will not make an uncompetitive product win, and it does not replace the human conversion you still own.** Data quality is the entry ticket, not the whole game.

Two honest limits. First, an agent recommends on merits it can compute, so a clean feed surfaces an over-priced or poorly-reviewed product accurately as over-priced and poorly-reviewed; the feed removes the reasons you are wrongly excluded, it does not fix the product or the price. Second, because the 2026 settlement keeps checkout with you, the handed-off human still has to convert on your site, so a fast, low-friction [pricing and checkout experience](/blogs/pricing-page-ai-will-quote) still matters. The feed wins the shortlist; you still close the sale.

## Frequently asked questions

### What is agentic commerce?

Agentic commerce is when an autonomous AI agent researches, compares and buys products on a shopper's behalf: the human sets the intent and the agent handles discovery, comparison, and checkout or handoff. It differs from conversational commerce (which assists a human shopping in chat) by delegating the decision and, sometimes, the transaction to the agent. Since 2026 the common pattern is AI-led discovery with checkout kept in the merchant's environment.

### How do AI shopping agents find products?

Primarily through a structured product feed the merchant pushes to the platform, a gzip-compressed file (.jsonl.gz, .csv.gz or .xml.gz) updated daily with each product's price, availability, images, identifiers and eligibility flags, and secondarily through corroborating web data such as Product/Offer schema on your PDP and third-party listings. The agent reads records and fields, not your storefront design, so if you are not in the feed you are invisible to it.

### What fields does a product feed need for AI shopping agents?

At minimum a stable identifier (GTIN/MPN/brand), a price with its ISO currency code (e.g. '129.00 USD'), an availability/stock status, images, a product category, and the platform's eligibility flags for search and checkout. Inclusion is a data-quality gate: a missing identifier, an unpriced item, or a stale stock status filters the product out before any ranking happens.

### Do I still need Product schema if I have a feed?

Yes. The feed gets you into the catalogue, but Product and Offer schema on your product page is the on-page truth agents corroborate the feed against, and it is what web-crawling agents read when there is no feed. The critical rule is that the schema and the feed must agree exactly on price, currency, availability and identifiers; if they disagree, the agent trusts neither.

### What are the agentic-commerce protocols (ACP, UCP, AP2)?

At least five launched between April 2025 and January 2026: OpenAI's Agentic Commerce Protocol (ACP, with Stripe) for discovery and the commerce handshake in ChatGPT; Google's Universal Commerce Protocol (UCP) for merchant product exchange and its Agent Payments Protocol (AP2) for agent-initiated payments; Visa's Trusted Agent Protocol for verifying an agent acts for a real cardholder; and Mastercard's Agent Pay for tokenised agent payments. All consume structured product data, so a clean feed and matching schema are the portable asset.

### Why did my product stop showing in AI shopping results?

Almost always feed drift. If the item sells out but the feed still says in\_stock, if a price changes on the site but not the feed, or if a daily feed push fails, the agent either surfaces stale data (and down-ranks you when shoppers bounce) or drops the product. An agent's catalogue is only as current as your last successful push, so reconcile the feed against live stock and price daily and monitor push success.

### How do you get an AI agent to recommend your product, not just list it?

Inclusion is data quality; recommendation adds the trust signals an agent can compute: a competitive, correctly-formatted price, accurate availability, a populated aggregate rating corroborated by off-site reviews, and complete attributes that match the shopper's constraints. Agents penalise ambiguity, no reviews, a vague category, or a price that disagrees across feed, PDP and third-party listings, so be the cleanest, most corroborated, least ambiguous option.

References

Market figures and the protocol landscape are 2026 industry estimates from the sources below; specifics move fast, confirm current feed specs with each platform.

1. [ChatGPT Commerce & Agentic Shopping Statistics 2026. Elogic.](https://elogic.co/blog/chatgpt-commerce-statistics/)
2. [ChatGPT Instant Checkout: What Happened to It in 2026. Hypotenuse.](https://www.hypotenuse.ai/blog/chatgpts-instant-checkout-the-next-phase-of-agentic-commerce)
3. [AI Shopping Assistant Guide 2026: Agentic Commerce Protocols. Opascope.](https://opascope.com/insights/ai-shopping-assistant-guide-2026-agentic-commerce-protocols/)
4. [ChatGPT Instant Checkout: ACP Protocol Retailer Guide (2026). Ekamoira.](https://www.ekamoira.com/blog/chatgpt-instant-checkout-agentic-commerce-protocol-2026)
5. [Agentic Commerce in 2026: How AI Agents Buy Products. Paz.ai.](https://www.paz.ai/agentic-commerce)
6. [Product structured data (Product, Offer). Google Search Central.](https://developers.google.com/search/docs/appearance/structured-data/product)
7. [Product and Offer types. Schema.org.](https://schema.org/Product)

About rawmktg.

rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com
