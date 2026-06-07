# What is Hydration?

Hydration is the process where client-side JavaScript attaches event handlers and state to already-rendered server HTML, turning static markup into a fully interactive page without rebuilding it from scratch.

## How it works

In a hydrated app, the server sends complete HTML (good for crawlers), then the framework runs in the browser to make it interactive. Done well, the content is visible immediately and interactivity arrives shortly after.

Done poorly, hydration mismatches can cause the framework to discard or replace the server HTML, and heavy hydration bundles can delay interactivity enough to hurt page-experience metrics.

## Hydration vs client-side rendering

CSR renders content in the browser from nothing; hydration starts from server-rendered content and only adds behaviour. The crawler-relevant difference is that hydrated pages already contain their content in the initial HTML, so even [non-rendering AI crawlers can read them](/blogs/how-ai-crawlers-index-your-site), whereas pure CSR pages cannot.

## Why it matters for B2B

Hydration is the bridge that lets you have app-like interactivity without sacrificing crawlability, as long as the content is real in the server HTML and not injected during hydration. The trap is treating hydration as a place to fetch and insert the main content; if you do, you have effectively reverted to CSR for any engine that does not run your scripts.

**Common mistake**

Letting hydration block interactivity or shift layout. The HTML is there for crawlers, but heavy hydration delays INP and can make content jump (CLS), so the user-experience signals still suffer even when indexing is fine.

*Source: https://rawmktg.com/glossary/hydration · rawmktg. by Vinayak Ravi*
