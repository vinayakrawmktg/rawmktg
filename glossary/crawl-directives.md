# What Are Crawler Directives?

Crawler directives (also called crawl directives) are the Allow and Disallow instructions inside robots.txt, plus the robots meta tag and X-Robots-Tag header, that tell a crawler which URL paths it may fetch, index, or use for training. They are matched per user-agent, so different bots can be given different access.

## How it works

Each directive applies to the user-agent group it sits under. Specificity matters: most modern crawlers honour the longest matching rule, so a narrow Allow can carve an exception out of a broad Disallow. Order is less important than match length.

Directives accept simple wildcards (\* for any sequence, $ for end of URL), which is how you block patterns like \*?sort= without naming every URL.

## Crawl directives vs the robots meta tag

A robots.txt directive governs whether a URL is fetched at all. The robots meta tag (and its X-Robots-Tag HTTP header equivalent) lives in the page response and governs what the engine does after fetching, such as noindex or nofollow. One gates the door; the other gives instructions once inside.

## Why it matters for B2B

Sloppy directives [quietly starve AI crawlers](/blogs/how-ai-crawlers-index-your-site). A wildcard meant to block a tracking parameter can also block a whole content directory if the pattern is too greedy. Because AI crawlers are newer and less forgiving than Googlebot, an over-broad Disallow can silently remove you from a model's citable set with no error anywhere in your analytics.

**Common mistake**

Putting `noindex` inside robots.txt. Google does not support it there, and if you also Disallow the URL the crawler can never read a noindex on the page itself. Allow the crawl, set noindex on the page.

*Source: https://rawmktg.com/glossary/crawl-directives · rawmktg. by Vinayak Ravi*
