# What is Orphan page?

An orphan page is a page that no other page on the site links to. Crawlers discover pages by following links, so an orphan has no path in and is reachable only via the sitemap, a direct URL, or an external link.

## How it works

Crawlers build their map of your site by following internal links from page to page. A page with zero inbound internal links sits outside that graph. It may still be discovered through an XML sitemap or an external backlink, but it receives none of the internal authority that flows along links.

Orphans are usually accidental: old landing pages, pages whose nav entry was removed, or programmatically generated pages that were never linked from anywhere.

## Orphan page vs noindexed page

A noindexed page is deliberately kept out of the index but is still linked and crawled. An orphan page is usually meant to rank but has been cut off from the link graph by mistake. One is an intentional exclusion; the other is an unintentional one.

## Why it matters for B2B

Orphans are a common, invisible cause of weak AI visibility. A page can be in your sitemap and technically indexable yet receive almost no crawl attention and accrue no internal authority, so it rarely surfaces as a citation. The earlier audit of your own AI-Search Glossary checked exactly this: the term pages were linked from the index, so they were not orphaned. Apply the same test to every new set you publish.

## Frequently asked questions

**What are orphan pages in SEO?**

Orphan pages are pages that no other page on the site links to. Because crawlers discover pages by following links, an orphan has no internal path in and accrues none of the authority that flows along links.

**How do you find orphan pages?**

Compare the full list of your URLs (from the sitemap, analytics, or server logs) against the pages reachable by crawling internal links; URLs in the former but not the latter are orphans. Crawlers like Screaming Frog do this when given both a crawl and a URL source.

**How do you fix orphan pages?**

Add internal links to them from relevant, crawlable pages, or, if the page has no value, noindex or remove it. The goal is that every page worth indexing is reachable through the link graph.

**Common mistake**

Assuming a page in your XML sitemap is discoverable. A URL can sit in the sitemap and still be an orphan if nothing links to it; sitemaps aid discovery but do not replace internal links, and orphaned pages get crawled rarely and ranked poorly.

*Source: https://rawmktg.com/glossary/orphan-page · rawmktg. by Vinayak Ravi*
