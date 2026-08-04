# Authority Isn't Demand

> Eight identity companies, Okta to Cognito, fight for the same buyers on Google and inside AI answers. Who built a demand engine, who is renting traffic, and who is about to be re-sorted by AI search.

*Source: https://rawmktg.com/blogs/authority-isnt-demand · rawmktg. by Vinayak Ravi*


Customer identity is one of the most instructive categories in B2B software right now. It sits at the crossroads of two audiences that rarely overlap: developers who integrate authentication in an afternoon, and security and IT leaders who sign the enterprise contract. It has decades-old incumbents and venture-backed challengers fighting in the same search results, and it is being reshaped, in real time, by the [shift from Google to AI answers](/blogs/why-traditional-seo-is-no-longer-enough).

We pulled organic, paid and backlink data for eight players on 9 July 2026, the incumbents Okta, Auth0 (now owned by Okta) and Ping Identity; the developer-first challengers Stytch, WorkOS, Frontegg and Descope; and the platform-embedded outlier, AWS Cognito, then ran a 40-question AI visibility scan across ChatGPT, Google AI, Claude and Gemini. The picture that emerges is not big versus small. It is about who has built a demand engine, who is renting traffic, and who is about to be caught out by the next platform shift.

## 01. Who wins the identity search war?

**Okta owns authority; WorkOS owns buyer intent; Descope and Cognito have authority but almost no demand.** Free visits is estimated organic traffic. Top-3 terms is the count of search terms where a site holds one of the first three positions. Traffic value is what those visits would cost through ads, a fair proxy for commercial weight.

The cohort scoreboard, monthly (Ahrefs, 9 Jul 2026)

| Company | Trust (DR) | Free visits | Top-3 terms | Traffic value | Ad spend |
| --- | --- | --- | --- | --- | --- |
| Okta [incumbent] | 91 | 1,579,900 | 15,440 | ~$1.65M | ~$133,800 |
| Auth0 [incumbent] | 90 | 430,900 | 4,954 | ~$285,000 | ~$59,400 |
| Ping Identity [incumbent] | 82 | 137,900 | 2,535 | ~$202,000 | ~$26,300 |
| Frontegg [challenger] | 71 | 37,800 | 572 | ~$65,700 | ~$5,500 |
| Stytch [challenger] | 74 | 37,200 | 410 | ~$22,600 | $0 |
| WorkOS [challenger] | 82 | 32,300 | 1,083 | ~$62,400 | ~$15,100 |
| Descope [challenger] | 75 | 19,300 | 448 | ~$19,300 | ~$2,100 |
| AWS Cognito [embedded] | ~96 | 17,400 | 72 | ~$17,000 | $0 |

Three things jump out. The gap between incumbents and everyone else is enormous, Okta alone pulls more free traffic than the other seven combined, several times over. [Trust score does not decide the race](/blogs/why-ai-cites-domo-over-databricks) among challengers: Descope (75) outscores Stytch (74) and Frontegg (71), yet earns the least buyer traffic of the three. And ad spend does not track with size.

Figure 1 - link authority (trust score) against monthly free visits, log scale. Okta and Auth0 sit top-right, strong on both. Descope and Cognito sit bottom-right: real authority, almost no buyer traffic. That quadrant is where stored potential goes to waste.

The clearest divide in the cohort is not big versus small. It is authority versus demand, and they are not the same thing.

## 02. What does each company do well, and not?

**Auth0 owns the language; WorkOS owns buyer intent; Descope and Cognito banked authority they never converted.** The cohort splits into distinct playbooks. Some own the vocabulary, some own the commercial phrases, and some have authority with no buyer-facing pages to spend it on.

### Okta and Ping: the incumbents who own the shelf

Okta is the category's gravity well, 1.5 million-plus free visits a month and over 15,000 top-three terms, built over a decade across every identity topic a buyer could search. It owns the enterprise vocabulary: single sign-on, lifecycle management, zero trust. Ping plays a similar game one tier down on compliance-heavy terms. The weakness is inertia: incumbent content is broad but dated, and it ranks on accumulated authority, not because it is the clearest answer, which matters more now that AI answer engines reward the plainest answer, not the oldest, most-linked page. Okta's acquisition of Auth0 is a tell, it bought the developer demand engine it could not build organically.

### Auth0: the content engine everyone should study

If you study one company here, make it Auth0: 11,000-plus ranking terms, nearly 5,000 in the top three, 430,000-plus free visits a month, all on developer education that compounds. It did not win by writing about Auth0, it won by owning the language of the category, what a JWT is, how OAuth works, what a magic link does, and built tools developers link to reflexively (nearly 34,000 referring domains from the real developer web). The move that built the moat is almost embarrassingly simple: take the concept every developer has to learn, and publish the clearest explanation on the internet.

The page that anchors thousands of searches

jwt

```
// A JSON Web Token is three base64 parts joined by dots:
header.payload.signature

// Decoded payload of a login token:
{
  "sub": "user_8f3a9c",       // who the user is
  "iss": "https://auth.acme.com",  // who issued it
  "iat": 1752000000,           // issued-at
  "exp": 1752003600            // expires in one hour
}
```

Every developer who learns the concept on Auth0's page arrives at the buying decision already inside Auth0's frame. Educational content is not a cost center, it is a moat, the [definitional library](/blogs/internal-linking-for-ai-retrieval) that wins citations. The risk now is the same one facing all the incumbents: much of that library was built for Google's ten blue links, not for an AI box that summarizes the concept without ever sending the click.

### Stytch and WorkOS: the efficient challengers

Stytch and WorkOS are the clearest proof that focus beats volume. Stytch ranks for barely 1,000 terms yet earns 37,000 free visits a month on $0 of ads. WorkOS is sharper on commercial intent: of its ~2,000 ranking terms, more than half sit in the top three, a hit rate the incumbents cannot match, and it owns buyer phrases like "sso provider" at position one.

Figure 2 - top-3 hit rate: the share of a site's ranking terms that reach Google's top 3. WorkOS turns a small footprint into the highest quality-of-ranking in the cohort; Descope and Frontegg rank broad but shallow.

The tradeoff is ceiling: a tightly focused footprint captures buyers who already know what they want but does less to create demand among developers still learning. The strongest position would combine WorkOS-style commercial discipline with an Auth0-style education layer. Right now, no challenger has both.

### Frontegg and Descope: strong products, unfinished demand engines

Both have genuinely good products and healthy authority, yet neither has converted it into buyer-facing search presence. Descope is the sharpest example of the trap, [the authority paradox](/blogs/property-vista-authority-paradox): a trust score of 75, higher than Stytch and Frontegg, but the least buyer traffic in the group. The reason is instructive, its single largest source of free traffic is a blog post about Claude versus ChatGPT, a topic with nothing to do with buying identity software.

Figure 3 - where Descope's visits actually come from. Nearly a third arrive from one off-topic "claude vs chatgpt" post; the high-intent buyer terms (sso, ciam) bring almost none.

The authority is real; the buyer pages that would turn it into pipeline have not been built. This is the most common failure mode in B2B: [mistaking traffic for demand](/blogs/ranking-isnt-visibility), a visit from someone comparing chatbots is not a lead. Descope's paid strategy shows the same half-built pattern: it spends ~$2,100/month bidding on rival brand names with a clean "try Descope instead" message, but points those ads at a thin destination while the same terms sit wide open on free search where it ranks near zero. Conquest advertising only pays off when a strong comparison page and organic presence sit behind it.

### AWS Cognito: distribution without a demand engine

Cognito ranks for ~125 terms and publishes almost no marketing content, yet still pulls 17,000 visits a month because it rides one of the highest-authority domains on the internet and shows up wherever a developer already lives inside AWS. Distribution, not marketing, does the work, until the AI scan exposes the ceiling. When buyers ask an AI tool which platform to choose, Cognito is largely absent, because it has published nothing to be cited. A distribution moat wins acquisition; it does not win preference.

## 03. How does AI search reshuffle the cohort?

**It scrambles the Google hierarchy: AI names MojoAuth and LoginRadius over Okta, rewarding the clearest answer.** The most forward-looking finding has nothing to do with Google rankings. Across 40 buyer questions on four engines, the brands the AI tools named most were not only the incumbents, smaller, sharper vendors appeared again and again, the same split behind [why the Google leader is not the AI leader](/blogs/winning-google-isnt-winning-ai).

Figure 4 - brands named across the 40-prompt AI scan. MojoAuth, Oloid and LoginRadius are a fraction of Okta's size on Google, yet the AI tools recommend them more often. AI answers do not rank by domain authority.

The pattern within a single brand makes the point concrete. Descope showed up in AI answers only where it had published direct, comparison-style content, and vanished everywhere else.

Descope's AI visibility by buyer question type (out of 5 prompts each)

| Buyer question type | Appeared | Why |
| --- | --- | --- |
| Pricing & packaging | 40% | Its best topic; appeared for "best passwordless login" |
| Alternatives to vendors | 20% | Appeared for "alternatives to Auth0" |
| Implementation / setup | 20% | Appeared for "integrating magic links" |
| Proof & credibility | 20% | One review-style mention |
| Comparisons (X vs Y) | 0% | No compare page for AI to lift |
| Security & compliance | 0% | A core buyer worry, absent |
| Integrations / workflow fit | 0% | Nothing published to cite |
| Which tool to pick | 0% | The final question; others named every time |

### How an AI engine decides who to cite

Buyer asks

best passwordless auth?

→

Engine retrieves

candidate pages, live web

→

Ranks by clarity

direct, answer-shaped text

→

Synthesizes

one answer, names a few

→

Cites the brand

clearest page wins

Domain authority barely enters at step 3. What matters is whether your page states the answer plainly enough for the model to quote it, which is why a DR-40 vendor can beat a DR-90 incumbent in an AI answer.

### What answer-shaped content actually looks like

Pages should be built to be quoted, the [anatomy of a high-citation page](/blogs/anatomy-of-a-high-citation-page). Two moves do most of the work. First, lead each key page with the question as a heading and a tight, 40-to-60 word direct answer the model can lift verbatim.

Lead with a liftable answer

html

```
<h2>What is an authentication service?</h2>
<p class="answer">
  An authentication service verifies that users are who they
  claim to be, then issues a secure token their apps can trust.
  It handles login, multi-factor, sessions, and social or SSO
  sign-in, so teams do not build and maintain that themselves.
</p>
```

Second, wrap the page in [structured data](/blogs/schema-markup-ai-citations-2026) so machines can parse the question-and-answer pairs without guessing. A small block of FAQ schema turns an ordinary page into a clean, citable source.

FAQ schema makes a page citable

json-ld

```
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How much does a passwordless auth platform cost?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Priced per monthly active user, with a free tier to ~7,500 MAUs and paid plans from ~$0.02 to $0.05 per MAU beyond that."
    }
  }]
}
```

The strategic window

For fifteen years, domain authority protected incumbents and made challenger content a slow, uphill grind. AI answers weaken that protection. A challenger that builds a disciplined library of clear comparison, pricing and security pages can be cited next to companies fifty times its size. The brands that recognize this in 2026 will look prescient in 2028.

## 04. What does the B2B demand engine look like?

**One loop: own the language, build buyer pages, earn links, get AI-cited, and pipeline follows.** Every company that wins this cohort runs some version of the same loop. The strivers are missing one or more links in it.

Own the language

definitive explainers

→

Build buyer pages

category, pricing, vs

→

Earn real links

dev tools, data reports

→

Get AI-cited

answer-shaped pages

→

Pipeline

buyers in your frame

Where each sits: Auth0 nails 1 and 3; WorkOS nails 2; Descope and Frontegg have the authority for 3 but skipped 2, so the engine never turns over; Cognito relies on distribution and runs none of it.

If you are the challenger reading this, the sequence matters as much as the parts. Fix the foundation first, then buyer pages, then trust, and you turn authority into demand inside a single quarter.

The same engine, as a build order

| Step | Window | The work |
| --- | --- | --- |
| 1, Fix the foundation | Weeks 1-4 | Clear the technical debt that blocks crawling and AI parsing: hidden pages, heavy assets, missing structured data, thin titles. |
| 2, Ship buyer pages | Weeks 2-8 | Build the category, pricing, alternatives and "vs" pages rivals already rank for. The step Descope and Frontegg skipped. |
| 3, Make pages answer-shaped | Weeks 2-8 | Lead with the question and a liftable answer, add FAQ schema, keep prose clean. This is what gets you AI-cited. |
| 4, Earn expertise links | Weeks 6-12 | Publish one flagship data report and a developer tool worth linking to. Lifts rank, backlinks and citations at once. |
| 5, Measure demand, not traffic | Ongoing | Track buyer-intent rankings, AI mention rate and pipeline separately from vanity traffic. Re-run the scan quarterly. |

## 05. What are the seven lessons for any B2B company?

**Authority is table stakes; measure buyer traffic; own the language; focus beats breadth; treat AI as a reset.** Strip away the identity specifics and this cohort teaches a set of lessons that apply to any B2B company competing for demand.

Seven lessons

| # | Lesson | Why |
| --- | --- | --- |
| 1 | Authority is table stakes, not a strategy | A strong trust score earns the right to compete, nothing more. Descope outranks peers on authority and still earns the least buyer traffic. |
| 2 | Measure buyer traffic, not total traffic | The most dangerous number in a dashboard is a big traffic figure made of the wrong visits. Segment by intent and judge each separately. |
| 3 | Own the language of your category | Auth0 built its position by teaching the concepts buyers search before they look for a vendor. Write the definitive page on each. |
| 4 | Focus beats breadth on a challenger budget | WorkOS holds half its terms in the top three by targeting commercial phrases with discipline. If you cannot outspend, out-focus. |
| 5 | Paid and organic must work as one system | Descope pays for rival-brand clicks that land on thin pages while the same terms sit unclaimed on free search. Build the page, then own it. |
| 6 | Distribution wins acquisition, not preference | Cognito's default-in-AWS advantage carries it until the buyer starts comparing, then absence from AI answers costs the deal. |
| 7 | Treat AI answers as a reset, and move first | AI rewards the clearest answer, not the biggest domain. A structured library written to be quoted gets cited beside far larger companies. |

Authority is earned, demand is built, and the clearest answer, not the oldest one, is what gets chosen.

The bottom line

The identity cohort is not a story about who has the most links. It is about who has turned authority into demand, and who is about to be re-sorted by AI. Okta and Auth0 built demand engines that still lead but were designed for a search era that is ending. Stytch and WorkOS prove focus and clarity can beat scale. Descope, Frontegg and Cognito each have a real asset they have not yet converted into a buyer-facing presence.

Method & data

Organic, paid and backlink metrics from Ahrefs Site Explorer (subdomains mode), pulled 9 July 2026; AWS Cognito measured at the aws.amazon.com/cognito path, its trust score inherited from the wider Amazon domain. AI visibility from a 40-prompt scan across ChatGPT, Google AI, Claude and Gemini. Traffic and spend figures are estimates and will move over time.

Frequently Asked Questions

### Why does Descope get so little buyer traffic despite high authority?

Because authority and demand are different things. Descope carries a DR of 75, higher than Stytch (74) and Frontegg (71), but earns the least buyer traffic of the three because it never built the buyer-intent pages, category, pricing, alternatives and "vs" pages, that turn authority into pipeline. Nearly a third of its free visits come from one off-topic "claude vs chatgpt" blog post, while high-intent terms like sso and ciam bring almost none. The authority is real; the demand engine is unfinished.

### Which identity vendors do AI tools recommend most?

Across a 40-prompt scan of ChatGPT, Google AI, Claude and Gemini, the most-named identity vendors were MojoAuth (37), Oloid (24) and LoginRadius (22), all a fraction of Okta's size on Google, followed by ScaleKit (15), Ping Identity (14), FusionAuth and WorkOS (13 each), Stytch (12) and Okta (11). AI answers do not rank by domain authority; they reward the clearest, most structured answer to the exact question asked.

### How can a challenger brand beat an incumbent in AI answers?

By writing the clearest, most structured answer to the specific question a buyer asks. AI engines barely weigh domain authority when they pick who to cite, they retrieve candidate pages, rank by clarity, and quote the page that states the answer plainly. A DR-40 vendor with a disciplined library of comparison, pricing and security pages (each leading with a 40-60 word direct answer and FAQ schema) can be cited beside a DR-90 incumbent. That window is open in most B2B categories right now.

### What makes content 'answer-shaped' for AI?

Two moves. First, lead each key page with the buyer's question as a heading and a tight, 40-to-60 word self-contained answer the model can lift verbatim, before any narrative. Second, wrap the page in FAQ or Article schema so machines can parse the question-and-answer pairs without guessing. Together they turn a page an AI ignores into one an AI quotes with your name attached.

About rawmktg.

rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Data source: Ahrefs Site Explorer (organic, paid, referring domains) plus a 40-prompt AI visibility scan across ChatGPT, Google AI, Claude and Gemini for eight identity vendors, captured 9 July 2026.
