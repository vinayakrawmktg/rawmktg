# What is robots.txt?

robots.txt is a plain-text file at the root of a domain that tells crawlers which URL paths they are allowed to request. It controls crawling, not indexing, and compliance is voluntary on the crawler's side.

## How it works

When a compliant crawler arrives, it reads /robots.txt first and obeys the Allow and Disallow rules for its user-agent. You can target specific bots by name, which is how sites grant or deny access to AI crawlers separately from search crawlers.

A critical misunderstanding: disallowing a URL does not remove it from the index. It only stops the crawler from fetching the body. A blocked URL can still appear in results as a bare link if other pages point to it.

## robots.txt vs noindex

These solve opposite problems. robots.txt stops a page being crawled; noindex stops a page being indexed. They also conflict: if you Disallow a URL, the crawler can never see the noindex tag on it, so the page can stay indexed. To deindex a page you must allow the crawl and serve noindex.

## Why it matters for B2B

robots.txt is now where you decide your relationship with AI training and answer crawlers. [Blocking GPTBot or CCBot](/blogs/how-ai-crawlers-index-your-site) keeps your content out of certain corpora; allowing OAI-SearchBot keeps you eligible for ChatGPT's live citations. These are business decisions, not just technical ones, and they belong in one reviewed file rather than left to defaults.

> **Note** , A single stray `Disallow: /` shipped to production has taken entire sites out of search overnight. It is the highest-blast-radius two lines on your domain.

**Example**

```
User-agent: *
Disallow: /cart/
Disallow: /*?sort=

Sitemap: https://example.com/sitemap.xml
```

Remember it controls crawling, not indexing: a disallowed URL can still appear in results if it is linked elsewhere. To keep a page out of the index, allow the crawl and use `noindex`.

*Source: https://rawmktg.com/glossary/robots-txt · rawmktg. by Vinayak Ravi*
