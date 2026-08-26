#!/usr/bin/env python3
"""SCRATCH: surface xml-sitemaps-for-ai-discovery into listings/sitemap/feed/llms + inbound links."""
import os, re, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="xml-sitemaps-for-ai-discovery"; URL=f"https://rawmktg.com/blogs/{SLUG}"
TITLE="The Broken-Sitemap Tax"
TOPIC="Technical Layer &middot; Indexation"
DESC_CARD="Real-time AI indexers quit after 3 redirect hops and read lastmod as a schedule. The hop ceiling, cache-instruction status codes, honest timestamps, and IndexNow push."
IMG="/assets/images/xml-sitemaps-for-ai-discovery-card"

CARD=(f'      <a href="/blogs/{SLUG}" class="article-card">\n'
 f'        <img src="{IMG}.webp" srcset="{IMG}-400.webp 400w, {IMG}-700.webp 700w, {IMG}.webp 1000w" '
 f'sizes="(max-width:768px) calc(100vw - 40px), (max-width:1024px) 46vw, 340px" alt="{TITLE}" class="card-img" loading="lazy" width="1000" height="525">\n'
 f'        <div class="card-body">\n'
 f'          <div class="card-topic">{TOPIC}</div>\n'
 f'          <div class="card-title">{TITLE}</div>\n'
 f'          <p class="card-desc">{DESC_CARD}</p>\n'
 f'          <div class="card-footer"><span class="card-arrow" aria-hidden="true">&rarr;</span></div>\n'
 f'        </div>\n      </a>\n')

def insert_before_first_card(path, anchor='      <a href="/blogs/do-ai-crawlers-render-javascript" class="article-card">'):
    s=open(path,encoding="utf-8").read()
    assert SLUG not in s, f"{path} already has slug"
    assert anchor in s, f"anchor missing in {path}"
    s=s.replace(anchor, CARD+anchor, 1)
    open(path,"w",encoding="utf-8").write(s)
    print("card ->", path)

insert_before_first_card("index.html")
insert_before_first_card("topics/technical-layer.html")

# sitemap.xml  (insert before do-ai-crawlers url block)
s=open("sitemap.xml",encoding="utf-8").read()
assert SLUG not in s
entry=(f'  <url>\n    <loc>{URL}</loc>\n    <lastmod>2026-08-26</lastmod>\n'
       f'    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
anc='  <url>\n    <loc>https://rawmktg.com/blogs/do-ai-crawlers-render-javascript</loc>'
assert anc in s
s=s.replace(anc, entry+anc,1)
open("sitemap.xml","w",encoding="utf-8").write(s); print("sitemap ok")

# feed.xml  (insert as newest item + bump lastBuildDate)
s=open("feed.xml",encoding="utf-8").read()
assert SLUG not in s
fdesc=("The discovery-layer teardown for AI search. Real-time indexers (OAI-SearchBot, Claude-SearchBot, PerplexityBot) "
 "enforce a 1-3 redirect-hop ceiling against Googlebot's ~10, and read your sitemap's lastmod as a recrawl schedule rather "
 "than an inventory. Covers the three-hop ceiling and discovery yield, status codes as cache instructions (301/308 vs 302/307), "
 "zero-hop root files, hash-based honest lastmod, sitemap partitioning and hygiene, freshness as the highest-leverage lever "
 "(3.2x citation inside 30 days), IndexNow push-vs-pull, the selection-vs-absorption split across engines, a Sitemap Health "
 "Index, a CI discovery-gate, and a 90-day sequence.")
item=(f'    <item>\n      <title><![CDATA[{TITLE}: XML Sitemaps for AI Discovery &middot; rawmktg.]]></title>\n'
 f'      <link>{URL}</link>\n      <guid isPermaLink="true">{URL}</guid>\n'
 f'      <pubDate>Wed, 26 Aug 2026 00:00:00 +0000</pubDate>\n'
 f'      <description><![CDATA[{fdesc}]]></description>\n    </item>\n')
anc='    <item>\n      <title><![CDATA[Do AI Crawlers Render JavaScript?'
assert anc in s
s=s.replace(anc, item+anc,1)
s=s.replace('<lastBuildDate>Fri, 15 Aug 2026 00:00:00 +0000</lastBuildDate>',
            '<lastBuildDate>Wed, 26 Aug 2026 00:00:00 +0000</lastBuildDate>',1)
open("feed.xml","w",encoding="utf-8").write(s); print("feed ok")

# llms.txt  (insert new bullet as first blog entry)
s=open("llms.txt",encoding="utf-8").read()
assert SLUG not in s
llm=("- [The Broken-Sitemap Tax: XML Sitemaps for AI Discovery](https://rawmktg.com/blogs/xml-sitemaps-for-ai-discovery) - "
 "August 2026. The discovery layer for AI search: your XML sitemap is now a scheduling instruction, not an inventory manifest. "
 "Three crawler families read it differently: training crawlers (GPTBot, ClaudeBot, CCBot) ingest a bulk manifest patiently and "
 "tolerate ~5 hops; real-time search indexers (OAI-SearchBot, Claude-SearchBot, PerplexityBot) read lastmod to prioritise the "
 "recrawl queue, ignore Crawl-delay, and enforce a hard 1-3 redirect-hop ceiling vs Googlebot's ~10 and the spec's 30; "
 "user-triggered fetchers arrive with a URL and ignore the file. The three-hop ceiling: scheme + host + trailing-slash "
 "normalisation can burn the whole budget before content is served, and the crawler abandons the request silently (a 301 in "
 "your log, then nothing). discovery_yield = share of declared URLs that return 200, resolve inside the hop budget, and "
 "self-canonical; most sites score 0.60-0.85. Status codes are cache instructions: 301/308 cache the target (pay the hop once), "
 "302/307 do not (re-requested every cycle); the 301-then-302 pattern invalidates the cache; redirect-to-noindex wastes the "
 "whole fetch. Root files (robots.txt, sitemap.xml, llms.txt, llms-full.txt) must return 200 with zero client-visible hops, "
 "PerplexityBot refuses any redirect on llms.txt, use a transparent internal rewrite not a redirect. lastmod is the signal you "
 "probably lie with: build-stamping today's date on all 12,000 URLs earns a recrawl demotion; timestamp_trust = content-changed "
 "URLs / lastmod-changed URLs (below 0.2, publish no lastmod). Fix with hash-based lastmod (hash the rendered body minus "
 "volatile regions). Partition sitemaps under ~5,000 URLs with a sitemap index; drop changefreq and priority (ignored). "
 "Freshness is the highest-leverage lever: pages updated within 30 days are cited ~3.2x more, 76.4% of top ChatGPT Search "
 "citations come from pages under 30 days, citation half-life ~2 months; AI Overviews is more forgiving (65% within a year). "
 "IndexNow inverts pull to push: notify Bing, Yandex, Naver, Seznam, Yep on change, recrawl in seconds not days, ~10s signed "
 "fanout; verify a root key file, submit only changed URLs. What a clean sitemap can't do: get you cited, that is content "
 "(quotations +41%, statistics +31-41%, cited sources +28% and +115% at rank 5, strict headings +17.3%, keyword stuffing -8%); "
 "and selection differs from absorption (ChatGPT 6.88 citations / 0.2713 influence, AI Overviews 12.06 / 0.0584, Perplexity "
 "16.35 / 0.0646). Put a number on it: the tax (redirect hops x fetches, x egress) and a Sitemap Health Index (0.40 response + "
 "0.30 hop + 0.20 timestamp trust + 0.10 freshness), gate both in CI. A 90-day sequence: routing first, timestamps second, "
 "partition and push third, telemetry last. Includes working bash/nginx/python/xml/yaml (hop sweep, transparent rewrites, "
 "hash-based lastmod, async validator, IndexNow pipeline, GitHub Actions discovery-gate).\n")
anc="- [Do AI Crawlers Render JavaScript?]"
assert anc in s
s=s.replace(anc, llm+anc,1)
open("llms.txt","w",encoding="utf-8").write(s); print("llms.txt ok")

print("done insertions")
