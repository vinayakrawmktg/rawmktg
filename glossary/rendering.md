# What is Rendering?

Rendering is the process of converting a page's raw HTML, CSS, and JavaScript into the fully constructed DOM that a user sees and [a crawler reads](/blogs/how-ai-crawlers-index-your-site). What gets rendered, and when, determines what content engines actually index.

## How it works

A browser fetches the HTML, then runs CSS and JavaScript to build the final page. Search engines do the same in two waves: an initial pass on the raw HTML, then a later, resource-intensive rendering pass that executes JavaScript and sees content injected after load.

The gap between those waves is where problems live. Content that only appears after JavaScript runs may be indexed late, partially, or not at all if the rendering pass is deferred or fails.

## Rendering vs indexing

Rendering produces the content; indexing decides whether to store it. An engine renders to discover what is on the page, then indexes the result. If rendering misses content, indexing never gets a chance to store it, which is why rendering problems masquerade as indexing problems.

## Why it matters for B2B

Most AI answer crawlers are far less patient renderers than Googlebot. Several fetch close to raw HTML and execute little or no JavaScript. If your key content or citations only materialize after client-side rendering, those crawlers may never see them, so the page exists for users but is blank to the engines you want citing you.

**Common mistake**

Assuming the crawler sees what your browser sees. "View source" (the raw HTML) is closer to what a non-rendering crawler gets than the rendered DOM. If content only appears after JavaScript runs, many crawlers never see it.

*Source: https://rawmktg.com/glossary/rendering · rawmktg. by Vinayak Ravi*
