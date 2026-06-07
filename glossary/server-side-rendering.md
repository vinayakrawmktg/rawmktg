# What is Server-side rendering (SSR)?

Server-side rendering (SSR) is an approach where the server builds a page's complete HTML before sending it to the browser. The content is present in the first response, so crawlers and AI engines see it without needing to execute JavaScript.

## How it works

With SSR, the server runs the framework, fetches data, and returns fully formed HTML. The browser can display it immediately, then optionally attach interactivity. Static site generation (SSG) is a close relative that builds the HTML at deploy time rather than per request.

Both put the content where every crawler can read it on the first pass, which is the behaviour you want for any page that needs to be discovered, indexed, or cited.

## SSR vs static rendering (SSG)

SSR generates the HTML on each request, which suits frequently changing data; SSG generates it once at build time and serves the same file to everyone, which is faster and cheaper but needs a rebuild to update. For a glossary or content site, SSG is usually ideal: stable content, instant delivery, fully crawlable HTML.

## Why it matters for B2B

SSR and SSG are the most reliable way to [guarantee AI crawlers see your content](/blogs/how-ai-crawlers-index-your-site), because there is nothing to execute. Your existing rawmktg pages already ship complete HTML, which is why the earlier audits could read every term and definition directly from the source. Keeping the new glossary on the same rendering path preserves that citability by default.

**Example**

The test for whether SSR is doing its job: fetch the page with JavaScript disabled (or "View source") and confirm the main content and links are present in the initial HTML.

```
curl -s https://example.com/page | grep "your headline"
```

*Source: https://rawmktg.com/glossary/server-side-rendering · rawmktg. by Vinayak Ravi*
