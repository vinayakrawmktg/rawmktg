# What Noterro Gets Right About AI Search

> And the gaps even strong brands should close. A bootstrapped allied-health software company has quietly become one of the most AI-visible brands in its category, here is how it happened, and what every software team can copy.

*Source: https://rawmktg.com/blogs/noterro-ai-search-teardown · rawmktg. by Vinayak Ravi*


Search is splitting in two. One half still looks like the ten blue links we have used for twenty years. The other half is a chat window: a person asks ChatGPT, Gemini, or Perplexity which practice-management tool they should buy, and an answer comes back already filtered, summarized, and recommended. For most software companies, that second half is a blind spot. They have no idea whether the models can see them, and most of the time the answer is that they cannot.

Noterro is an exception, and an instructive one. It is a practice-management platform for allied-health clinics: physiotherapists, massage therapists, chiropractors, and naturopaths. It is bootstrapped, profitable, and has taken no outside capital. It is not the kind of company you would expect to be winning a technology race against venture-funded competitors. Yet when we mapped its footprint across the AI surfaces that increasingly mediate buying decisions, Noterro was cited on every single one.

Getting cited is not magic; it is a pipeline. A page has to be [crawlable, then self-describing, then authoritative](/blogs/how-rag-actually-works), before a model will name it in an answer.

Crawlable

robots, sitemap, clean HTML

→

Self-describing

JSON-LD schema, llms.txt

→

Authoritative

quality links: G2, YouTube

→

Citable

the model names you in answers

Figure 1 · How a page becomes an AI citation

The things Noterro did right along that pipeline are not expensive, not proprietary, and not dependent on a large marketing budget. They are choices any disciplined team can copy. The things it has not yet done are equally instructive, because they show where the frontier is moving next. We will take the wins first.

## Part One: What Noterro Gets Right

### 1. It shows up everywhere the models look

The single most striking finding is breadth. Noterro is cited across all seven AI surfaces we track, and the volume is real, not token.

Figure 2 · Noterro AI citations by platform · orange = most headroom · Source: Ahrefs Brand Radar, June 2026

Most SaaS companies of comparable size appear on one or two platforms, and plenty appear on none. Breadth matters more than depth here, because different audiences live on different assistants and you do not get to choose which one your next customer opens. A clinic owner researching software in ChatGPT and a developer-minded founder asking Grok are two different buyers, and Noterro is present for both. The lesson for other companies is to stop treating "AI search" as a single channel to be won, and start treating it as presence across a fragmented set of engines, each of which assembles its answers from slightly different signals.

### 2. It treats structured data as a first-class citizen

The reason Noterro is so legible to machines is not luck. Its homepage carries three blocks of JSON-LD structured data, and each one does a specific job: an Organization block (who the company is), a WebApplication block (what the product is, plus an aggregate rating), and a FAQPage block that mirrors a twelve-question on-page FAQ in machine-readable form. That last one is the quiet masterstroke, because question-and-answer markup maps almost perfectly onto how people query assistants:

FAQPage JSON-LD

```
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Is Noterro HIPAA compliant?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Yes. Noterro follows HIPAA and PIPEDA protocols, with encrypted storage and 2FA."
    }
  }]
}
</script>
```

When someone asks whether Noterro is HIPAA compliant, the model already has a clean, sourced answer to surface. The transferable lesson: schema is not a nice-to-have for SEO specialists, it is the primary interface between your site and the models. An Organization type, a FAQPage type, and a product or WebApplication type are the minimum, and they pay for themselves quickly.

### 3. It shipped an llms.txt before most teams knew it existed

Noterro serves a valid llms.txt file: a plain-text document, modeled loosely on robots.txt, that summarizes the product and indexes the pages the company most wants surfaced. It looks roughly like this:

llms.txt

```
# Noterro
Practice management software for allied health clinics.

## Product
- [Noterro GO](/mobile-clinic-management-software): clinic management for mobile therapists
- [Pricing](/pricing): plans and pricing

## Resources
- [Help Center](https://help.noterro.com)
```

The striking thing is not that Noterro implemented it perfectly, but that the company bothered at all. It signals a team paying attention to where discovery is heading rather than only optimizing for where it has been. The lesson is less about the file itself and more about posture: the companies that win in AI search treat it as a live, fast-moving surface and ship small experiments early, rather than waiting for a settled best practice that may never fully arrive.

### 4. The fundamentals are boringly, completely correct

It is easy to get excited about llms.txt and forget that AI visibility still rests on traditional technical hygiene. Noterro's is close to flawless.

Fig. 4a: Technical hygiene audit, noterro.com

| Element | Status | Detail |
| --- | --- | --- |
| robots.txt | PASS | Valid, points to the sitemap |
| XML sitemap | PASS | Well-formed, 1,270 URLs |
| Heading structure | PASS | Exactly one H1, clean hierarchy |
| Canonical tags | PASS | Present |
| Open Graph / Twitter | PASS | Complete metadata sets |
| HTTPS | PASS | Served securely |

None of this is glamorous, and that is the point. The reason Noterro's structured data and llms.txt actually work is that they sit on top of a site the crawlers can navigate without friction. A brilliant schema block on a site with a broken sitemap and three competing H1s is a stereo in a car with no engine. Do the unglamorous foundational work first, then layer the AI-specific signals on top.

### 5. It earned authority the legitimate way

Noterro carries a Domain Rating of 80, high for a vertical SaaS company, and its strongest backlinks come from places that genuinely matter:

Fig. 4b: Highest-value referring domains

| Source | DR | Why it matters for AI |
| --- | --- | --- |
| youtube.com | 99 | Hosts tutorials and the Crash Course; heavily cited for how-to answers |
| g2.com | 91 | The review platform models lean on when users ask which tool to choose |
| fresha.com | 91 | Wellness/booking ecosystem; high topical relevance |
| globenewswire.com | 91 | Press distribution; news-grade co-citation signals |

These are exactly the sources assistants cite when they recommend a product, so the authority compounds: [the same links that help rankings also feed the models' confidence](/blogs/authority-seeding-ai-llm-trust). The lesson is quality over volume. A handful of links from YouTube, G2, and a credible industry directory will do more for AI citation than hundreds of low-grade directory links.

A brilliant schema block on a site the crawlers cannot navigate is a stereo in a car with no engine. Do the unglamorous work first.

## Part Two: The Gaps Worth Closing

If the story stopped there, the takeaway would be simple: do the fundamentals, add schema and llms.txt, earn good links. But Noterro is interesting precisely because a company can do all of that and still leave its biggest opportunity on the table. The gaps below are not failures. They are the natural next frontier for a brand that has already won the technical race.

### 1. The brand is doing almost all the work

Here is the number that reframes everything: roughly [82% of Noterro's organic traffic comes from branded searches](/blogs/hr-saas-ai-visibility-gap). People typing "noterro" or "noterro login" account for about 11,900 of its 14,500 monthly organic visits.

82%branded

Figure 3 · Where Noterro's organic traffic comes from · branded 11,900/mo · non-branded 2,600/mo

Everything non-branded, the entire universe of people searching "practice management software" or "SOAP note software" without knowing Noterro exists, adds up to only about 2,600 visits. This is a wonderful problem to have, because it means the brand is strong and customers are loyal. But it also means Noterro is mostly found by people who already know the name. The much larger pool of buyers still comparing options, the exact moment an assistant gets asked which clinic software is best for a physiotherapy practice, is largely uncaptured. And brand demand has a ceiling; you can only own your own name so many times. Read the branded-versus-non-branded split as a leading indicator: a high branded share looks healthy on a dashboard, but it can disguise the fact that you are not winning the category-level queries where new customers, and now AI assistants, actually make decisions.

### 2. There is not enough content for the models to cite on competitive questions

This gap is the direct cause of the first one. AI assistants can only cite a brand for a non-branded question if the brand has published something worth citing on that topic. Noterro's homepage is excellent, but a homepage cannot answer how to choose chiropractic software. Those answers need dedicated pages, and the depth data shows the shortfall:

Fig. 5a: Citable pages by platform (depth, not breadth)

| Platform | Pages Cited | Read |
| --- | --- | --- |
| Google AI Mode | 67 | Deep |
| Grok (xAI) | 89 | Deep |
| Google AI Overviews | 45 | Solid |
| ChatGPT | 7 | Shallow |
| Microsoft Copilot | 3 | Shallow |

The breadth of presence is there; the depth of citable content is not yet, especially on ChatGPT and Copilot. This is the most important lesson in the article: technical optimization makes you eligible for AI citation, but [content is what gets you cited](/blogs/anatomy-of-a-high-citation-page). Schema tells a model what a page is. It cannot manufacture a page that does not exist. The companies that pull ahead from here will pair Noterro-grade infrastructure with a steady stream of genuinely useful, non-branded answer content.

### 3. The backlink profile needs a cleanup

Authority cuts both ways. Alongside the genuinely strong links, about 29% of Noterro's [referring domains are flagged as spam](/glossary/referring-domains): link-farm directories and low-quality auto-listings of the kind that accrue to almost any domain once it reaches a certain size.

29%flagged as spam

Figure 4 · Referring domain quality · 1,010 total · clean 715 · spam-flagged 295

Most were probably never built by Noterro at all. The risk is not a sudden penalty; it is slow erosion of the trust signals both search engines and models rely on. The fix is unglamorous and cheap: assemble the list and submit a disavow file through Search Console:

disavow.txt

```
# disavow.txt - submit via Google Search Console
# Spam directories and link farms
domain:buybacklinks.agency
domain:kingranks.com
domain:topbilliondirectory.com
domain:rankyour.website
```

The broader lesson is that authority needs maintenance, not just accumulation. A link profile is a garden, not a trophy case.

### 4. A multi-market product with a single-market setup

Noterro serves clinics across Canada, the United States, the United Kingdom, Australia, and beyond, and its pricing even differs by region. Today the traffic is concentrated at home:

Fig. 5b: Traffic by market

| Market | Share of traffic | Monthly visits |
| --- | --- | --- |
| Canada | 61.1% | 8,900 |
| United States | 34.3% | 5,000 |
| United Kingdom | 1.3% | 185 |
| Australia | 1.0% | 146 |

Yet the site carries no hreflang markup, the signal that tells search and AI engines which regional version of a page to serve to whom. A few lines would help the models stop guessing:

hreflang

```
<link rel="alternate" hreflang="en-ca" href="https://www.noterro.com/" />
<link rel="alternate" hreflang="en-us" href="https://www.noterro.com/us/" />
<link rel="alternate" hreflang="en-gb" href="https://www.noterro.com/uk/" />
<link rel="alternate" hreflang="x-default" href="https://www.noterro.com/" />
```

The lesson generalizes to any company selling across borders: if your product is global, your technical setup should say so. Otherwise you are asking the models to guess which version of you to recommend in London versus Toronto, and they will not always guess in your favor.

Technical optimization makes you eligible for AI citation. Content is what gets you cited.

## The Synthesis

The most useful way to read Noterro is as a company that has finished the first half of the AI-search playbook better than almost anyone, with the entire second half still in front of it.

Half 1 · Infrastructure - largely done

- Clean fundamentals: robots, sitemap, H1
- Structured data / JSON-LD
- llms.txt
- Legitimately earned authority

Half 2 · Content & authority - the frontier

- Non-branded answer content
- Comparison & category pages
- Completed G2 / review profiles
- Clean, maintained link profile

Figure 5 · Infrastructure makes models able to see you. Content and authority make them recommend you.

The first half is infrastructure: clean fundamentals, rich structured data, an llms.txt, and legitimately earned authority. That work is necessary, it is copyable, and it is where most companies should start, because without it nothing else registers. But infrastructure is increasingly table stakes. As more companies implement schema and tidy their sitemaps, the differentiator shifts to the second half: depth of content and strength of entity authority. The brand that publishes the clearest answer to which software is best for a mental-health practice, backs it with a completed G2 profile and a well-structured FAQ, and keeps its link profile clean, is the brand the assistant will name when a buyer asks. That position is sticky once established, which is exactly why the companies investing in it now will be hard to dislodge later.

For Noterro, the path forward is unusually clear, because the hard, foundational part is already done. For everyone else, the lesson is twofold. Copy the fundamentals Noterro got right, because they are the price of admission. Then do the thing Noterro has not yet done, and build the content and authority that turn visibility into citations. The first makes the models able to see you. The second makes them recommend you.

Frequently Asked Questions

### Why is Noterro so visible in AI search?

Noterro is cited across all seven AI engines tracked because it pairs clean technical fundamentals with three blocks of JSON-LD structured data (Organization, WebApplication, and a FAQPage that mirrors its on-page FAQ), a published llms.txt file, and a high-quality backlink profile (DR 80) from sources models trust, such as YouTube and G2. Those signals make its pages crawlable, self-describing, and authoritative, the three conditions a page must meet before a model will name it.

### What is the biggest gap in Noterro's AI-search strategy?

Content depth on non-branded, competitive questions. About 82% of Noterro's organic traffic is branded, and it has few dedicated pages answering category-level queries like which practice-management software is best, so assistants have little to cite when buyers compare options. ChatGPT and Copilot cite only 7 and 3 of its pages respectively. Technical optimization makes a brand eligible for citation; published answer content is what actually gets it cited.

### What can other software companies copy from Noterro?

The infrastructure half of the playbook, all of which is low-cost and non-proprietary: correct technical fundamentals (valid robots.txt, clean sitemap, a single H1, canonicals, HTTPS), Organization plus FAQPage plus WebApplication schema, a published llms.txt, and a small number of high-authority backlinks rather than many low-grade ones. Then go beyond Noterro by publishing non-branded answer content and cleaning up spam links with a disavow file.

About rawmktg.

rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Data source: Ahrefs (organic keywords, referring domains, Brand Radar AI citations) and a manual structured-data and technical audit of noterro.com, captured June 2026.
