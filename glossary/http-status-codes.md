# What is HTTP status codes?

HTTP status codes are the three-digit numbers a server returns with every response. They tell crawlers and browsers what happened: success (200), redirection (3xx), client errors like missing pages (4xx), or server failures (5xx).

## How it works

Crawlers read status codes to decide what to do with a URL: index a 200, follow a 301 to its target, drop a 404 over time, and back off on 5xx errors. The codes are the primary technical language a site uses to communicate page state.

The ones that matter most for SEO are 200, 301, 302, 304, 404, 410, and 5xx. Misreporting them, such as serving a 200 for a missing page, confuses engines.

## HTTP status codes vs the visible page

What a user sees and what the server reports can diverge. A page can display a friendly Not Found message while returning a 200 status, which tells crawlers the page is fine. The status code, not the visible content, is what engines act on, which is why soft 404s are a problem.

## Why it matters for B2B

Status codes are the first thing to check when an AI engine stops citing a page. A page returning 5xx during crawls, redirecting unexpectedly, or serving soft 404s will be dropped from retrieval regardless of content quality. Your log files plus a status check are the fastest diagnosis of why a previously cited page went quiet.

**Example**

```
200  OK           serve the page
301  Moved        permanent redirect (passes signals)
404  Not Found    page is gone
410  Gone         gone for good
503  Unavailable  temporary, retry later
```

Returning the right code is how you tell crawlers what to do. A "not found" page that returns 200 is a soft 404.

*Source: https://rawmktg.com/glossary/http-status-codes · rawmktg. by Vinayak Ravi*
