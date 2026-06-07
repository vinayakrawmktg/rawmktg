# What is Largest Contentful Paint (LCP)?

Largest Contentful Paint (LCP) is a Core Web Vital that measures the time from navigation to when the largest visible content element, usually a hero image or headline block, finishes rendering. Google's good threshold is 2.5 seconds.

## How it works

LCP tracks the moment the main content becomes visible, which correlates with when a user feels the page is usable. Common causes of slow LCP are large unoptimized images, slow server response, render-blocking resources, and client-side rendering that delays the main element.

Fixes include optimizing and preloading the LCP element, improving server response time, and ensuring the main content is server-rendered rather than script-injected.

## LCP vs Time to First Byte

TTFB measures how quickly the server starts responding; LCP measures how quickly the main content appears. TTFB is one upstream component of LCP, but a fast TTFB can still precede a slow LCP if heavy client-side work delays rendering. TTFB is the server's part; LCP is the whole journey to visible content.

## Why it matters for B2B

LCP is a user-experience and conversion metric more than an AI-citation one, but its most common cause, client-side rendering of the main element, is exactly what also hides content from [non-rendering AI crawlers](/blogs/how-ai-crawlers-index-your-site). So fixing LCP by server-rendering the hero content often improves crawlability as a side effect, which is the version of this work worth prioritizing.

**Common mistake**

Lazy-loading the hero or main image. The LCP element should load eagerly with high priority; deferring it, or letting a render-blocking webfont sit in front of it, is the most common cause of a slow LCP.

*Source: https://rawmktg.com/glossary/largest-contentful-paint · rawmktg. by Vinayak Ravi*
