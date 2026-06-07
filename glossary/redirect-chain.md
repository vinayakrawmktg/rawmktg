# What is Redirect chain?

A redirect chain is a sequence of two or more redirects between the URL a user or crawler requests and the final destination. Each hop adds latency and a chance for signals to leak or for the crawler to stop following.

## How it works

Chains accumulate over time as sites migrate repeatedly: an old URL points to a newer one, which points to a newer one still. Each redirect is an extra round trip, slowing the response and consuming a little crawl effort.

Crawlers will follow a limited number of hops before giving up, and long chains risk the destination never being reached. The fix is to point every old URL directly at the final target in one hop.

## Redirect chain vs redirect loop

A chain eventually reaches a destination after multiple hops; a loop never does, because the redirects point back to each other and cycle endlessly. A loop is a hard error that breaks the page entirely, while a chain merely degrades performance and risks signal loss; both are worth eliminating.

## Why it matters for B2B

Chains slow crawlers and can strand the authority you meant to pass along, which is exactly the risk during a URL restructure. If the glossary moves more than once, collapse every redirect so each legacy URL jumps straight to the live page in a single hop; that preserves the cleanest possible path for engines that previously cited the old addresses.

**Example**

```
/old → /new            one hop (good)
/old → /interim → /new  chain (avoid)
```

Each extra hop adds latency and risks signal loss, and some crawlers stop following after a few. Point every old URL straight at the final destination.

*Source: https://rawmktg.com/glossary/redirect-chain · rawmktg. by Vinayak Ravi*
