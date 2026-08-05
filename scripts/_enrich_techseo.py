#!/usr/bin/env python3
"""SCRATCH: add one concrete callout to each Technical SEO glossary entry, matching
the AI-Search collection. Idempotent. Do NOT commit."""
import os
ROOT="/sessions/optimistic-youthful-planck/mnt/rawmktg"; os.chdir(ROOT)

C={
"crawl-budget":("Common mistake","<p>Trying to \"increase\" crawl budget by submitting URLs and pinging sitemaps, when the real lever is spending less of it. Letting faceted filters, session IDs, and tracking parameters spawn near-infinite low-value URLs is what starves your money pages of crawls.</p>"),
"robots-txt":("Example","<pre>User-agent: *\nDisallow: /cart/\nDisallow: /*?sort=\n\nSitemap: https://example.com/sitemap.xml</pre><p>Remember it controls crawling, not indexing: a disallowed URL can still appear in results if it is linked elsewhere. To keep a page out of the index, allow the crawl and use <code>noindex</code>.</p>"),
"crawl-directives":("Common mistake","<p>Putting <code>noindex</code> inside robots.txt. Google does not support it there, and if you also Disallow the URL the crawler can never read a noindex on the page itself. Allow the crawl, set noindex on the page.</p>"),
"log-file-analysis":("Example","<pre>66.249.66.1 - - [07/Jun/2026:10:22:01] \"GET /glossary/crawl-budget\" 200 \"Googlebot\"</pre><p>What to hunt for: bots burning requests on parameter and filter URLs, or never reaching your deep pages at all.</p>"),
"orphan-page":("Common mistake","<p>Assuming a page in your XML sitemap is discoverable. A URL can sit in the sitemap and still be an orphan if nothing links to it; sitemaps aid discovery but do not replace internal links, and orphaned pages get crawled rarely and ranked poorly.</p>"),
"indexing":("Common mistake","<p>Reading \"crawled\" as \"indexed.\" Search Console's <code>Crawled - currently not indexed</code> means Google fetched the page and chose not to store it, usually a quality or duplication signal, not a technical block.</p>"),
"noindex":("Common mistake","<p>Blocking a page in robots.txt and adding <code>noindex</code> at the same time. If the crawler is disallowed it never sees the noindex, so the URL can linger in the index. noindex only works if the page stays crawlable.</p>"),
"canonicalization":("Common mistake","<p>Treating canonical tags as commands. They are hints: an engine can ignore a canonical when other signals (internal links, sitemaps, redirects) contradict it. Keep every signal pointing at the same canonical URL.</p>"),
"rel-canonical":("Example","<pre>&lt;link rel=\"canonical\" href=\"https://example.com/page\" /&gt;</pre><p>Put a self-referencing canonical on every page. The usual errors: canonicalising everything to the homepage, or pointing at a noindexed or redirected URL, both of which scramble the signal.</p>"),
"duplicate-content":("Common mistake","<p>Worrying about a \"duplicate content penalty.\" There is no penalty; the real cost is split signals and the engine choosing a version for you. Consolidate with a self-referencing canonical or a 301 instead.</p>"),
"index-bloat":("Common mistake","<p>Letting tag pages, filter combinations, internal search results, and thin archives all get indexed. Thousands of low-value URLs dilute crawl attention and perceived quality; noindex or canonicalise the ones that do not deserve to rank.</p>"),
"rendering":("Common mistake","<p>Assuming the crawler sees what your browser sees. \"View source\" (the raw HTML) is closer to what a non-rendering crawler gets than the rendered DOM. If content only appears after JavaScript runs, many crawlers never see it.</p>"),
"client-side-rendering":("Common mistake","<p>Shipping the main content as a client-rendered app and assuming engines will render it. Rendering is deferred and not guaranteed, and most AI crawlers do not run JavaScript at all, so CSR-only content is often invisible to exactly the bots you want citing you.</p>"),
"server-side-rendering":("Example","<p>The test for whether SSR is doing its job: fetch the page with JavaScript disabled (or \"View source\") and confirm the main content and links are present in the initial HTML.</p><pre>curl -s https://example.com/page | grep \"your headline\"</pre>"),
"hydration":("Common mistake","<p>Letting hydration block interactivity or shift layout. The HTML is there for crawlers, but heavy hydration delays INP and can make content jump (CLS), so the user-experience signals still suffer even when indexing is fine.</p>"),
"javascript-seo":("Common mistake","<p>Relying on client-side rendering for content you need indexed and cited. The safe pattern is server-side or static rendering of the core content, with JavaScript layered on for interactivity, so the page is fully legible without it.</p>"),
"site-architecture":("Common mistake","<p>Burying important pages many clicks deep. A flat structure, where money pages are reachable in two or three clicks from the homepage, gets them crawled more and signals their importance; deep, sprawling hierarchies do the opposite.</p>"),
"internal-linking":("Common mistake","<p>Making key pages reachable only from the footer or sitemap, and linking with generic \"read more\" anchors. Contextual in-body links with descriptive anchor text pass both relevance and authority; nav-only links signal low priority.</p>"),
"xml-sitemap":("Example","<pre>&lt;url&gt;\n  &lt;loc&gt;https://example.com/page&lt;/loc&gt;\n  &lt;lastmod&gt;2026-06-07&lt;/lastmod&gt;\n&lt;/url&gt;</pre><p>Include only canonical, indexable URLs. Listing redirected, noindexed, or duplicate URLs wastes crawl signals and erodes trust in the sitemap.</p>"),
"breadcrumb-navigation":("Example","<p>Pair a visible trail with <code>BreadcrumbList</code> schema so engines read the hierarchy and can show it in results.</p><pre>Home / Glossary / Crawl budget</pre>"),
"faceted-navigation":("Common mistake","<p>Letting filter combinations (color, size, price, sort order) generate crawlable, indexable URLs. This is the classic crawl-budget and index-bloat trap; contain it with canonical tags, robots rules, or parameter handling before it spawns thousands of near-duplicates.</p>"),
"url-structure":("Common mistake","<p>Shipping URLs with session IDs, tracking parameters, and mixed case. Each variant looks like a separate URL to a crawler and splits signals; keep URLs lowercase, stable, readable, and free of needless parameters.</p>"),
"core-web-vitals":("Example","<pre>LCP  &lt; 2.5s    loading\nINP  &lt; 200ms   responsiveness\nCLS  &lt; 0.1     visual stability</pre><p>These are the \"good\" thresholds, scored on real-world field data, not just a lab test.</p>"),
"largest-contentful-paint":("Common mistake","<p>Lazy-loading the hero or main image. The LCP element should load eagerly with high priority; deferring it, or letting a render-blocking webfont sit in front of it, is the most common cause of a slow LCP.</p>"),
"cumulative-layout-shift":("Common mistake","<p>Omitting width and height on images and embeds, or injecting banners and ads above content after load. Both shove the page around as it renders and spike CLS; reserve space for anything that arrives late.</p>"),
"interaction-to-next-paint":("Common mistake","<p>Blocking the main thread with heavy JavaScript, including third-party tags, so taps and clicks feel laggy. INP measures that delay across the whole visit, so trimming and deferring scripts is the main lever.</p>"),
"time-to-first-byte":("Common mistake","<p>Treating a slow TTFB as a front-end problem. It is mostly server and network: slow origin responses, no caching, or no CDN. A high TTFB caps every downstream metric, including LCP.</p>"),
"http-status-codes":("Example","<pre>200  OK           serve the page\n301  Moved        permanent redirect (passes signals)\n404  Not Found    page is gone\n410  Gone         gone for good\n503  Unavailable  temporary, retry later</pre><p>Returning the right code is how you tell crawlers what to do. A \"not found\" page that returns 200 is a soft 404.</p>"),
"301-redirect":("Common mistake","<p>Mass-redirecting old URLs to the homepage instead of the closest equivalent page. A 301 passes signals only when the target is a genuine replacement; redirecting everything to the homepage is often treated as a soft 404 and drops the signal.</p>"),
"302-redirect":("Common mistake","<p>Using a 302 (temporary) for a permanent move. It tells engines to keep the original URL indexed, so ranking signals never consolidate on the new one. Use a 301 for anything permanent.</p>"),
"redirect-chain":("Example","<pre>/old → /new            one hop (good)\n/old → /interim → /new  chain (avoid)</pre><p>Each extra hop adds latency and risks signal loss, and some crawlers stop following after a few. Point every old URL straight at the final destination.</p>"),
"soft-404":("Common mistake","<p>Serving \"no results\" or empty pages with a 200 status. Crawlers cannot tell the page is empty, so they keep it indexed and waste crawl on it. Return a real 404 or 410, or add genuine content.</p>"),
}

def block(label,inner):
    return ('      <div class="gloss-callout">\n'
            f'        <div class="cl-label"><strong>{label}</strong></div>\n'
            f'        {inner}\n'
            '      </div>\n')

done=0; missing=[]
for slug,(label,inner) in C.items():
    p=f"glossary/{slug}.html"
    if not os.path.exists(p): missing.append(slug); continue
    h=open(p,encoding="utf-8").read()
    if '<div class="gloss-callout">' in h: continue
    foot='<div class="gloss-foot">'
    h=h.replace(foot, block(label,inner)+"      "+foot, 1)
    open(p,"w",encoding="utf-8").write(h); done+=1
print("callouts added:",done,"| missing:",missing or "none","| defined:",len(C))
em=sum(open(f"glossary/{s}.html").read().count("—") for s in C if os.path.exists(f"glossary/{s}.html"))
print("em dashes across tech entries:",em)
