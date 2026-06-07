# What is Client-side rendering (CSR)?

Client-side rendering (CSR) is an approach where the server returns a near-empty HTML shell and the browser constructs the visible content by running JavaScript after the page loads. The meaningful content does not exist in the initial response.

## How it works

With CSR, the initial HTML is often little more than a div and a script bundle. The framework then fetches data and builds the DOM in the user's browser. This makes for fluid app-like experiences but means the first response a crawler sees contains almost no content.

Engines that render JavaScript can eventually see CSR content, but only after the deferred rendering pass, and only if the scripts execute cleanly within their time and resource limits.

## CSR vs SSR

CSR builds the page in the browser; SSR builds it on the server and ships complete HTML. To a crawler the difference is stark: SSR content is present in the first response, while CSR content is absent until JavaScript runs. SSR is the safer default when discoverability matters.

## Why it matters for B2B

CSR is the single most common reason a modern site is invisible to AI crawlers. A beautifully built React or Vue page can return an empty shell to GPTBot or PerplexityBot, which often do not execute the JavaScript that would fill it in. The content is real for users and nonexistent for the engines, with no error to warn you.

**Common mistake**

Shipping the main content as a client-rendered app and assuming engines will render it. Rendering is deferred and not guaranteed, and [most AI crawlers do not run JavaScript at all](/blogs/how-ai-crawlers-index-your-site), so CSR-only content is often invisible to exactly the bots you want citing you.

*Source: https://rawmktg.com/glossary/client-side-rendering · rawmktg. by Vinayak Ravi*
