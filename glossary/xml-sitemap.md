# What is XML sitemap?

An XML sitemap is a machine-readable file that lists the URLs you want search engines to know about, optionally with metadata like last-modified dates. It aids discovery but does not guarantee crawling or indexing.

## How it works

The sitemap gives engines a clean list of canonical URLs to consider, which is especially useful for large sites, new sites with few backlinks, or pages that are hard to reach by crawling. You submit it in Search Console and reference it in robots.txt.

It should contain only indexable, canonical, 200-status URLs. Listing redirects, noindexed pages, or 404s sends mixed signals and erodes the engine's trust in the file.

## XML sitemap vs HTML sitemap

An XML sitemap is built for crawlers: a structured URL list with metadata. An HTML sitemap is a human-facing page of links. They serve different audiences, and an XML sitemap is the one engines actually consume. Neither replaces good internal linking; a sitemap is a discovery aid, not an architecture substitute.

## Why it matters for B2B

A clean, accurate sitemap is the backstop that gets AI crawlers to your full term set even before internal links are fully crawled. The earlier audit confirmed all 32 of your AI-Search Glossary terms were present in the sitemap, which is precisely what you want: every term URL listed, canonical, and returning 200, so no page depends solely on link discovery.

**Example**

```
<url>
  <loc>https://example.com/page</loc>
  <lastmod>2026-06-07</lastmod>
</url>
```

Include only canonical, indexable URLs. Listing redirected, noindexed, or duplicate URLs wastes crawl signals and erodes trust in the sitemap.

*Source: https://rawmktg.com/glossary/xml-sitemap · rawmktg. by Vinayak Ravi*
