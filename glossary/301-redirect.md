# What is 301 redirect?

A 301 redirect is a permanent redirect that tells browsers and crawlers a URL has moved for good to a new location. Engines transfer the old URL's ranking signals to the destination and eventually replace the old URL with the new one in the index.

## How it works

When a crawler requests a 301'd URL, the server responds with the code and the new location, and the crawler follows it. Over time the engine consolidates the old URL's accumulated authority onto the target and indexes the destination in its place.

301s are the correct tool for site migrations, URL changes, consolidating duplicates, and retiring pages whose value should move elsewhere.

## 301 vs 302

A 301 is permanent and signals that the move is final, so signals consolidate onto the target. A 302 is temporary and tells engines to keep the original URL indexed because the change is expected to be reversed. Using a 302 for a permanent move is a frequent mistake that delays signal transfer.

## Why it matters for B2B

When you change the glossary's URL path at deploy, 301s are what preserve any authority the pages have earned. Get the redirect type wrong, use a 302 or a redirect chain, and you risk stranding citations on URLs that no longer resolve cleanly, which can quietly drop you from AI answers that previously named the old address.

**Common mistake**

Mass-redirecting old URLs to the homepage instead of the closest equivalent page. A 301 passes signals only when the target is a genuine replacement; redirecting everything to the homepage is often treated as a soft 404 and drops the signal.

*Source: https://rawmktg.com/glossary/301-redirect · rawmktg. by Vinayak Ravi*
