# What is noindex?

noindex is a directive that tells search engines to keep a page out of their index. It is delivered as a robots meta tag in the HTML head or as an X-Robots-Tag HTTP header, and the page must be crawlable for it to be seen.

## How it works

When an engine fetches a page carrying noindex, it processes the page but does not add it to the index, and over time drops any previously indexed version. The page can still be crawled and its links followed unless you also specify nofollow.

The most common failure is combining noindex with a robots.txt Disallow on the same URL. Because the Disallow stops the fetch, the engine never sees the noindex and the page can remain indexed.

## noindex vs Disallow

noindex removes a page from the index but allows crawling; Disallow blocks crawling but does not remove the page from the index. To deindex reliably you want noindex with the URL left crawlable. To save crawl budget on URLs you do not care about indexing, Disallow is the tool.

## Why it matters for B2B

noindex is how you keep low-value pages from diluting an AI engine's view of your site. Thin internal search results, tag archives, and staging pages add noise that can blur which of your pages is the authoritative answer. Selectively noindexing them concentrates crawl and citation attention on the pages you actually want named.

## Frequently asked questions

**What is a noindex tag and what does it do?**

noindex is a directive, a robots meta tag or X-Robots-Tag header, that tells search engines to keep a page out of their index. The page can still be crawled, but it will not appear in results.

**How do you noindex a page?**

Add a robots meta tag with the noindex value to the page's head, or send an X-Robots-Tag noindex HTTP header. The URL must stay crawlable, because a page blocked in robots.txt can never be read to see the noindex.

**How do you find pages that are noindexed?**

Crawl the site with a tool like Screaming Frog and filter for the noindex directive, or check Search Console's Pages report for URLs excluded by a noindex tag.

**How do you fix 'Excluded by noindex tag' in Search Console?**

That status is informational, not an error; it means the page carries noindex. If the page should be indexed, remove the noindex directive and request reindexing. If exclusion is intended, no action is needed.

**Common mistake**

Blocking a page in robots.txt and adding `noindex` at the same time. If the crawler is disallowed it never sees the noindex, so the URL can linger in the index. noindex only works if the page stays crawlable.

*Source: https://rawmktg.com/glossary/noindex · rawmktg. by Vinayak Ravi*
