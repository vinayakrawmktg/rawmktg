# What is Crawl budget?

Crawl budget is the number of URLs a search engine will fetch on your site in a given window. It is governed by how fast your server can respond and how much demand the engine has to recrawl your pages.

## How it works

Search engines do not crawl every page every day. They allocate effort based on two things: crawl rate limit, which is how hard they can hit your server without degrading it, and crawl demand, which reflects how popular and how fresh your URLs are.

On small sites this is rarely a constraint. It becomes one on large sites, sites with slow servers, or sites that generate near-infinite low-value URLs, where the crawler spends its allowance on junk before it reaches the pages that matter.

## Crawl budget vs crawl rate

Crawl rate is one input to crawl budget, not a synonym for it. Crawl rate is the ceiling on requests per second the crawler will make. Crawl budget is the realized total over time, which also depends on demand. You can have generous rate capacity and still get little crawling if demand is low.

## Why it matters for B2B

AI answer engines and their crawlers face the same economics. If [GPTBot, PerplexityBot, or Google's crawler](/blogs/how-ai-crawlers-index-your-site) burns its allowance on faceted-filter URLs and session-ID duplicates, your genuinely citable pages get fetched late or not at all, and a page that is never fetched can never be cited.

For most B2B sites the fix is not begging for more budget but spending less: prune low-value URLs, fix duplication, and keep the paths to your money pages shallow.

**Common mistake**

Trying to "increase" crawl budget by submitting URLs and pinging sitemaps, when the real lever is spending less of it. Letting faceted filters, session IDs, and tracking parameters spawn near-infinite low-value URLs is what starves your money pages of crawls.

*Source: https://rawmktg.com/glossary/crawl-budget · rawmktg. by Vinayak Ravi*
