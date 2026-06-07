# What is Time to First Byte (TTFB)?

Time to First Byte (TTFB) is the time between a browser making a request and receiving the first byte of the server's response. It captures server processing, network latency, and any redirects before content begins arriving.

## How it works

TTFB rolls up DNS lookup, connection setup, server-side processing, and the start of the response. High TTFB points to slow backend work, missing caching, distant servers, or redirect chains adding round trips before the real response.

Improvements come from caching, faster backend code, a CDN closer to users, and eliminating unnecessary redirects.

## TTFB vs page load time

TTFB measures only when the response starts; page load time measures when it finishes and the page is usable. TTFB is the opening move; everything else, including downloading, rendering, and LCP, happens after it. A bad TTFB delays everything downstream, but a good TTFB does not guarantee a fast page.

## Why it matters for B2B

TTFB is the one page-experience metric with a direct crawler consequence: it shapes crawl rate. A slow server lowers the rate at which [crawlers, including AI crawlers](/blogs/how-ai-crawlers-index-your-site), will request your pages, because they throttle to avoid overloading you. On large sites that throttling directly reduces how many of your pages get fetched and become eligible for citation.

**Common mistake**

Treating a slow TTFB as a front-end problem. It is mostly server and network: slow origin responses, no caching, or no CDN. A high TTFB caps every downstream metric, including LCP.

*Source: https://rawmktg.com/glossary/time-to-first-byte · rawmktg. by Vinayak Ravi*
