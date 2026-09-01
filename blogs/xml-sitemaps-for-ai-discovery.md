# The Broken-Sitemap Tax: XML Sitemaps for AI Discovery

> Your sitemap is no longer an index manifest. It is a scheduling instruction for machines that abandon a request after three hops, and the difference is costing you citations you never see.

*Source: https://rawmktg.com/blogs/xml-sitemaps-for-ai-discovery · rawmktg. by Vinayak Ravi*


Nobody puts a line item for this in the budget. It surfaces as something else. Publishing volume climbs and organic traffic flatlines. A competitor gets named in ChatGPT answers about your category and you do not. Your log export shows tens of thousands of AI-crawler requests a month, which looks like proof the machines are paying attention, right up until you check how many of those requests ended in a document that could be cited.

That gap is the Broken-Sitemap Tax: the compounding cost of declaring a set of URLs a generative engine cannot cheaply resolve into text. The URLs redirect. They carry timestamps nobody believes. They disagree with their own canonical tags. Each one is a fetch that costs the crawler compute and returns nothing usable, and every system with a budget responds the same way, it comes back less often, on fewer URLs, with less patience.

The tax is silent by design. You served three clean redirects and the client walked away. From the server's point of view, nothing failed.

This is not a rerun of the classical crawl-budget argument, which barely matters for most sites under a few thousand URLs. Two things changed. First, hop tolerance collapsed: real-time AI indexers enforce a ceiling of one to three redirect hops, against the ten Googlebot has tolerated and the thirty the HTTP spec permits. Second, the sitemap became a change feed: real-time indexers read its lastmod values to decide what to recrawl today, which makes timestamp integrity a ranking input rather than an administrative detail.

Scope

This piece covers the discovery layer: what you declare, how fast it resolves, and how you push changes. Crawler identities and robots.txt directives are covered in how AI crawlers index your site. Whether those crawlers execute your JavaScript once they arrive is covered in do AI crawlers render JavaScript. Neither is repeated here.

## 01. How did the sitemap become a schedule instead of a manifest?

**Three families of agent read the same file with three different tolerances.** Training crawlers ingest a bulk manifest patiently. Real-time search indexers read your lastmod to prioritise the recrawl queue and abandon slow fetches. User-triggered fetchers barely touch the file. The middle family is the one your sitemap is actually talking to.

Training crawlers like GPTBot, ClaudeBot and CCBot ingest bulk corpora asynchronously. They throttle themselves between 0.5 and 5.0 requests per second and tolerate multi-hop redirects, because nothing about their mission is time-bound. Real-time search indexers like OAI-SearchBot, Claude-SearchBot and PerplexityBot ground live answers under latency constraints closer to an API call than a crawl, and they ignore Crawl-delay entirely, because a delayed fetch is useless when a user is waiting. User-triggered fetchers like ChatGPT-User fire when a person pastes your URL into a chat and behave like a headless browser with a stopwatch running.

Training crawlers

Patient bulk manifest. Tolerate 5 hops. Model-release pace.

→

Real-time indexers

Read lastmod, prioritise recrawl. 1-3 hops. Answer pace.

→

User fetchers

Arrive with a URL in hand. Ignore the sitemap.

Figure 2. Same file, three readers, three tolerances. The middle column decides whether you are in today's answer.

Table 1. Crawler families and what each does with the file you publish at /sitemap.xml.

| Family | Agents | What it wants | Rate behaviour | Hop ceiling | Crawl-delay |
| --- | --- | --- | --- | --- | --- |
| Model training | GPTBot, ClaudeBot, CCBot, Google-Extended, Bytespider | A complete URL manifest for bulk ingestion | 0.5-5.0 req/s, async | Up to 5 hops | Honoured |
| Real-time search | OAI-SearchBot, Claude-SearchBot, PerplexityBot | Fresh lastmod to prioritise the recrawl queue | Continuous, high velocity | 1 to 3 hops | Ignored |
| User-triggered fetch | ChatGPT-User, Claude-User, Perplexity-User | Nothing. It arrives with a URL in hand | Bursty, tied to chat sessions | Up to 3 hops | Frequently bypassed |
| Specialised extractors | Diffbot, YouBot, cohere-ai, Mistral-Crawl | Entity and structured-data targets | Periodic, medium velocity | Up to 3 hops | Generally honoured |

One practical consequence: when people say their AI visibility is fine because GPTBot hits their site constantly, they are usually reading training-crawler logs. Training ingestion moves at the pace of model releases; citation in a live answer moves at the pace of the real-time index. Only one of them is affected by what you shipped this week. The full crawler roster and robots.txt directives are in [how AI crawlers index your site](/blogs/how-ai-crawlers-index-your-site).

## 02. What is the three-hop ceiling?

**Real-time indexers abandon a request after one to three redirects, silently.** The HTTP spec permits 30 redirects and Googlebot follows around 10. AI indexers enforce a hard ceiling of one to three hops, after which the request is dropped with no client-side error logged anywhere you can see.

Figure 3. Redirect tolerance by agent type. Most site architectures were designed against the grey bars and are now read by the orange ones.

Three hops sounds generous until you count what a legacy URL actually does. Scheme normalisation is one hop, host normalisation another, trailing-slash enforcement a third. A user arriving from an old PDF, an email footer, or a partner directory can burn the whole budget before a byte of content is served.

http://site/page

Scheme normalisation.

→

https://www.site/page

Host normalisation.

→

https://site/page

Trailing-slash enforcement.

→

https://site/page/

Content, finally, if any budget is left.

Figure 4. The chain almost every mature site has somewhere: three redirects for zero content. One rewrite rule collapses it.

The failure mode is what makes it expensive. A 404 is loud; a 500 pages someone; a crawler quietly hitting its hop ceiling produces a 301 in your access log, then silence. Your monitoring sees a successful response. The engine sees a resource it could not resolve inside its budget and moves to the next candidate, which belongs to someone else.

It helps to have a number. Define discovery yield as the share of declared URLs a real-time indexer can actually resolve into a citable document in one pass: three binary conditions, all cheap to measure.

formula · discovery yield

```
discovery_yield =  (1 / N) · Σ  [ s_i = 200 ]·[ h_i <= H ]·[ c_i = u_i ]

  N   URLs declared in the sitemap        H   agent hop ceiling (1-3)
  s   terminal status code                c   the page's declared canonical
  h   redirect hop count                  u   the URL as declared
  A URL counts only if it returns 200, resolves inside the hop budget,
  and points at itself as canonical. Most sites score 0.60 to 0.85.
```

bash · measure hop counts on the URLs you declare

```
#!/usr/bin/env bash
# Reports redirect hops and terminal status for every URL in a sitemap.
# Anything with hops >= 3 is at or past the real-time indexer ceiling.
SITEMAP="https://example.com/sitemap.xml"
UA="Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"

curl -s "$SITEMAP" \
  | grep -oP '(?<=<loc>)[^<]+' \
  | while read -r url; do
      chain=$(curl -sIL -A "$UA" -o /dev/null \
        -w '%{num_redirects} %{http_code} %{url_effective}' "$url")
      hops=$(echo "$chain"  | awk '{print $1}')
      code=$(echo "$chain"  | awk '{print $2}')
      final=$(echo "$chain" | awk '{print $3}')
      if [ "$hops" -ge 1 ] || [ "$code" != "200" ]; then
        printf 'HOPS=%s STATUS=%s  %s  ->  %s\n' "$hops" "$code" "$url" "$final"
      fi
    done
```

Run that against your own sitemap before reading further. The output is usually the most persuasive artefact in the entire audit, because it is your URLs and your numbers rather than an industry average.

Free Tool · Auditor

Score your own discovery yield

The formula above, made live. Run the hop-sweep against your sitemap, paste the output, and see how many declared URLs a real-time indexer can actually resolve.

Paste your crawl results

One URL per line: the hop-sweep output, or url,status,hops CSV

Load sample

A URL passes only if it returns 200 and resolves inside the three-hop ceiling. Real-time AI indexers abandon anything at three hops or more. Get the input by running the hop-sweep from the article against your own sitemap.

Discovery yield

0/ 1.0

Paste your crawl

Where the budget goes

The breakdown and worst offenders appear here.

## 03. Why are status codes cache instructions, not cosmetic detail?

**The wrong redirect code breaks caching, so you pay the hop cost on every cycle, forever.** A 301 (or 308) tells the agent the move is permanent and the target should be cached, so you pay the hop once. A 302 or 307 tells it nothing moved, so the original URL is re-requested on every cycle.

A 301 caches the new target, GPTBot immediately, ClaudeBot for roughly thirty days, PerplexityBot on the next cycle. A 308 does the same while guaranteeing the request method and body survive, which makes it correct for API endpoints, JSON feeds and IndexNow payloads where a silent rewrite to GET would destroy the request. A 302 or 307 keeps the original URL in the index and re-requests it every cycle. Multiply that by a few thousand URLs and a daily cadence and you have an egress line item nobody can explain.

Figure 5. Relative caching benefit against relative repeat-fetch waste, by response pattern. Temporary redirects are more expensive on every cycle after the first.

Table 2. How each response pattern is interpreted by AI crawlers, and what it costs on the next cycle.

| Response | Crawler caching behaviour | Recrawl impact | Indexing outcome |
| --- | --- | --- | --- |
| 200 OK direct | Canonical target stored immediately, no hop | Optimal, minimal budget | Immediate ingestion into retrieval context |
| 301 permanent | Target cached (GPTBot now, ClaudeBot ~30d) | Future crawls reallocate to the target | Canonical consolidates; method may rewrite to GET |
| 308 permanent | Target cached, method and body preserved | Future crawls reallocate to the target | Correct for API feeds and IndexNow payloads |
| 302 temporary | Target not cached, original retained | High, entry URL polled continuously | Signals unstable authority, delays ingestion |
| 307 temporary | Target not cached, POST payload preserved | High, original polled regularly | Blocks permanent canonical consolidation |
| 301 then 302 | Invalidates the cached 301 | Severe, perpetual loop checks | Early drop-off, silent eviction from citation pools |
| Redirect to noindex | Follows the hop, then rejects the target | Total budget waste | Immediate drop from index and candidates |

The pattern worth hunting is the 301 followed by a 302, which happens when a permanent migration rule and a temporary campaign or maintenance rule live in different layers and neither team knows about the other. Two more anti-patterns deserve a grep: user-agent-dependent redirects that serve bots a different path are cloaking and are detected, and geolocation redirects that bounce /en/ to /us/ create loops for crawlers that egress from a single region, which describes most AI fleets.

Target distribution

A healthy log profile for the URLs you declare: above 95% 200 OK, under 5% permanent redirects, under 1% temporary redirects. If your temporary-redirect share is in double digits, fix that first, before content, before schema, before anything else.

## 04. Why must root discovery files get zero hops, not three?

**robots.txt, sitemap.xml and llms.txt must return a 200 from the root with no redirect at all.** PerplexityBot refuses to follow redirects when fetching /llms.txt, so a single 301 there makes the file nonexistent to it. Use a transparent internal rewrite, invisible to the crawler, not a redirect, which is a hop it has to spend.

This breaks in a specific, common way. A team reorganises static assets, moves the files into a build-output directory, and adds a catch-all rewrite that happens to emit a 301. Everything still works in a browser. Every human test passes. The discovery layer goes dark and nothing reports it.

nginx · transparent rewrites for root discovery assets

```
server {
  listen 443 ssl http2;
  server_name example.com;

  # Root discovery assets. 200 OK, zero client-visible hops.
  location = /robots.txt {
    default_type text/plain;
    try_files /static_root/robots.txt =404;
    expires 1h;
    add_header Cache-Control "public, no-transform";
  }
  location = /sitemap.xml {
    default_type application/xml;
    try_files /static_root/sitemap.xml =404;
    expires 15m;
  }
  location = /llms.txt {
    default_type text/plain;
    try_files /static_root/llms.txt =404;
    expires 1h;
    add_header Access-Control-Allow-Origin "*";
  }
  location = /llms-full.txt {
    default_type text/plain;
    try_files /static_root/llms-full.txt =404;
    expires 1h;
  }

  # Everything else: collapse scheme, host, and slash in a single hop.
  location / {
    if ($http_x_forwarded_proto = "http") {
      return 301 https://example.com$request_uri;
    }
    proxy_pass http://origin_upstream;
  }
}
```

Table 3. The three root files, their consumers, and their redirect tolerance. Only one is forgiving, and not by much.

| Attribute | robots.txt | sitemap.xml | llms.txt |
| --- | --- | --- | --- |
| Protocol role | Access control and permission rules | Canonical URL inventory and change signal | Machine context map for agents |
| Primary consumer | Crawlers of every family | Search and AI indexers, aggregators | LLM agents and retrieval pipelines |
| Format | Plain-text key-value directives | UTF-8 XML against the sitemaps schema | Strict Markdown subset |
| Server requirement | 200 OK direct at the root | 200 OK, UTF-8, schema valid | 200 OK direct with text/plain |
| Redirect tolerance | Effectively zero | Tolerated but degrades efficiency | Zero, PerplexityBot fails outright |

On llms.txt itself, keep expectations calibrated. It is a clean specification with real adoption among developer tools, but large-scale log studies found 97% of published llms.txt files received zero automated crawler requests. Publish a valid one because it costs an hour and future-proofs the surface, but do not treat it as a discovery strategy, the XML sitemap is where the discovery work happens. The [dedicated llms.txt piece](/blogs/does-llms-txt-do-anything-yet) goes deeper on the spec.

## 05. Why is lastmod the signal you are probably lying with?

**Build-stamped timestamps tell the indexer everything changed, it checks, finds nothing, and demotes you.** AI indexers lean on lastmod harder than Google because freshness is the strongest scheduling input they have. Honest timestamps get a recrawl queue that tracks your publishing; false ones get you demoted as a source of scheduling information.

Here is the mechanism. Your build regenerates the sitemap on every deploy and stamps today's date on all 12,000 URLs, the default behaviour of most static-site generators and half the CMS plugins in circulation. The indexer takes you at your word and recrawls aggressively, compares the semantic hash of what it fetched against what it had, and finds nothing changed, on thousands of URLs. It will not do that twice: the recrawl priority of the whole file gets demoted, and the next time you ship something important you are in a slower queue.

formula · timestamp trust

```
timestamp_trust =  (URLs whose CONTENT changed) / (URLs whose LASTMOD changed)

  1.00  every timestamp change was a real content change
  0.04  you told the indexer 12,000 pages changed when 500 did
  < 0.7 = engineering ticket.  < 0.2 = better to publish no lastmod at all.
```

Figure 10. Relative citation rate by time since last genuine update. The cliff between the first two buckets is steeper than most editorial calendars assume.

The fix is to stop letting the build decide what changed and let a content hash decide instead: hash the rendered body with the volatile parts stripped, compare against the stored hash, and write a timestamp only when the comparison fails.

python · hash-based lastmod generation

```
import hashlib, json, re, datetime, pathlib

STATE = pathlib.Path(".sitemap-hashes.json")
VOLATILE = [
    re.compile(r'<nav\b.*?</nav>', re.S | re.I),
    re.compile(r'<footer\b.*?</footer>', re.S | re.I),
    re.compile(r'data-build-id="[^"]*"'),
    re.compile(r'\d{4}-\d{2}-\d{2}T[\d:+.-]+'),   # rendered timestamps
]

def semantic_hash(html: str) -> str:
    """Hash only the content a retrieval system would actually keep."""
    for pattern in VOLATILE:
        html = pattern.sub('', html)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = ' '.join(text.split()).lower()
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def resolve_lastmod(pages: dict[str, str]):
    """pages maps url -> rendered html. Returns url -> ISO 8601 lastmod."""
    prior = json.loads(STATE.read_text()) if STATE.exists() else {}
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    out, state, changed = {}, {}, []
    for url, html in pages.items():
        digest = semantic_hash(html)
        record = prior.get(url)
        if record and record['hash'] == digest:
            out[url] = record['lastmod']          # unchanged, keep the old date
            state[url] = record
        else:
            out[url] = now                        # genuinely new or edited
            state[url] = {'hash': digest, 'lastmod': now}
            changed.append(url)
    STATE.write_text(json.dumps(state, indent=2))
    print(f'{len(changed)} of {len(pages)} URLs changed this build')
    return out, changed
```

The changed list that falls out of this function is the same list you push to IndexNow later, which is not a coincidence. Two formatting rules while you are in there: use full W3C datetime with a UTC offset (2026-03-31T08:30:00+00:00, not a bare date), and never write a future lastmod, which happens more than you would expect when scheduled publishing and timezone handling collide.

## 06. Why should you partition the sitemap file?

**So a crawl-rate regression arrives with a filename attached, not buried in 48,000 URLs.** The protocol permits 50,000 URLs per file, but auditing guidance converges on ~5,000 for two reasons: a real-time indexer abandons a slow XML parse the way it abandons a slow redirect, and a monolithic file gives you one number to watch instead of a per-section signal.

xml · sitemap index and a compliant child file

```
<!-- /sitemap.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-docs.xml</loc>
    <lastmod>2026-08-24T09:12:00+00:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
    <lastmod>2026-08-26T06:40:00+00:00</lastmod>
  </sitemap>
</sitemapindex>

<!-- /sitemap-docs.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/docs/architecture</loc>
    <lastmod>2026-08-24T09:12:00+00:00</lastmod>
  </url>
  <url>
    <loc>https://example.com/docs/rate-limits</loc>
    <lastmod>2026-07-02T11:48:00+00:00</lastmod>
  </url>
</urlset>
<!-- No changefreq, no priority: ignored for years, pure parse-time cost. -->
```

Note what is absent: no changefreq and no priority. Both have been ignored by Google for years and appear in no documented AI-indexer behaviour, so they are bytes that cost parse time and buy nothing. The lastmod on the index entries is genuinely useful, because it lets an agent skip an entire child file it has already seen. Escape your ampersands, keep the file UTF-8, serve it over HTTPS, and declare the namespace, unescaped entities and missing namespaces are the two failures that break strict XML parsers outright.

## 07. What does sitemap hygiene actually require?

**Every URL in the file is a claim that it is canonical, live and indexable.** Zero non-200 URLs, exact canonical alignment, directive alignment (no noindex or robots-blocked URLs), and parameter discipline. Every URL that fails one test teaches the crawler to discount the whole file.

- **Zero non-200 URLs.** Anything returning 301, 302, 308, 404 or 5xx should be purged automatically, not quarterly by hand.
- **Canonical alignment.** The URL in loc must match the page's own canonical tag exactly, including trailing slash and protocol. Mismatches are a documented cause of eviction from citation candidate pools.
- **Directive alignment.** A URL carrying noindex or blocked in robots.txt must never appear, declaring a page you told crawlers not to read is a contradiction resolved against you.
- **Parameter discipline.** Session IDs, tracking parameters and faceted-navigation combinations produce near-duplicate URLs that consume budget and dilute the canonical signal.

python · sitemap validator with a hard fail

```
import asyncio, re, sys
import httpx
from xml.etree import ElementTree

NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
UA = 'Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)'
HOP_CEILING = 3
CANONICAL = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)

async def check(client, url):
    try:
        r = await client.get(url, follow_redirects=True, timeout=10.0)
    except httpx.RequestError as exc:
        return {'url': url, 'fail': f'network: {exc.__class__.__name__}'}
    hops = len(r.history)
    if r.status_code != 200:
        return {'url': url, 'fail': f'status {r.status_code}'}
    if hops >= HOP_CEILING:
        return {'url': url, 'fail': f'{hops} hops, at or past the ceiling'}
    if 'noindex' in r.headers.get('x-robots-tag', '').lower():
        return {'url': url, 'fail': 'x-robots-tag noindex'}
    match = CANONICAL.search(r.text[:200_000])
    if match and match.group(1).rstrip('/') != url.rstrip('/'):
        return {'url': url, 'fail': f'canonical drift -> {match.group(1)}'}
    return None

async def main(sitemap_url):
    async with httpx.AsyncClient(headers={'User-Agent': UA}) as client:
        xml = (await client.get(sitemap_url)).text
        urls = [e.text for e in ElementTree.fromstring(xml).iterfind('.//sm:loc', NS)]
        sem = asyncio.Semaphore(12)
        async def guarded(u):
            async with sem:
                return await check(client, u)
        results = await asyncio.gather(*(guarded(u) for u in urls))
    failures = [r for r in results if r]
    yield_rate = 1 - len(failures) / max(len(urls), 1)
    for f in failures[:40]:
        print(f"FAIL  {f['fail']:<38} {f['url']}")
    print(f'\ndiscovery yield: {yield_rate:.3f} over {len(urls)} URLs')
    sys.exit(1 if yield_rate < 0.98 else 0)

asyncio.run(main('https://example.com/sitemap-docs.xml'))
```

Wire that into CI as a blocking step on the sitemap build. A threshold of 0.98 is aggressive on purpose, the point of a gate is that it fails before the file ships, not that it produces a dashboard nobody opens. The canonical-and-structure side of this is covered in [the anatomy of a high-citation page](/blogs/anatomy-of-a-high-citation-page).

## 08. Why is freshness the highest-leverage variable you control?

**Content updated within 30 days is cited at ~3.2x the rate of static pages.** Everything above is about not losing; this is where the file earns. 76.4% of top-cited ChatGPT Search URLs come from pages updated in the preceding 30 days, and pages untouched for three months face ~3x the probability of losing citations entirely.

Google AI Overviews is more forgiving, 65% of citations from content updated within a year, 89% within three years. That difference is a strategy input: if ChatGPT Search is where your category gets decided, your update cadence is not a hygiene task, it is the campaign. Fitted to a simple exponential, the observed decay implies a citation half-life near two months for competitive commercial queries, the same shape as [the 30-day content half-life](/blogs/30-day-content-half-life-recency-ai-ranking-signal).

formula · freshness decay

```
C(t) =  e^(-λ·t)          # relative citation likelihood

  t  days since the last GENUINE content change
  λ  fitted to the fresh/stale ratio; implies a citation half-life
     near ~60 days for competitive commercial queries.
```

Two things follow. A page you update every ninety days spends most of its life in the shallow part of the curve, so a quarterly refresh is closer to maintenance than advantage. And the update has to be real, the decay is driven by the indexer detecting genuine change, the same hash comparison from the lastmod section. Changing a date in a byline is not a content update, and the system that decides whether you get cited is the one that already caught you doing it.

Practical cadence

Pick the twenty to fifty URLs that carry commercial intent, put them on a thirty-day substantive review, and let the long tail decay. Trying to keep twelve thousand pages inside thirty days is how sites end up build-stamping their sitemaps in the first place.

## 09. How does IndexNow push beat pull?

**You notify engines the instant a page changes, so recrawl happens in seconds, not days.** Everything so far optimises a pull model, you publish and wait to be noticed. IndexNow inverts the direction: on create, update or delete, your origin notifies participating engines directly and the URL enters a recrawl queue in seconds.

The participant list includes Bing, Yandex, Naver, Seznam and Yep, which matters more than it used to because a meaningful share of live ChatGPT Search grounding resolves through the Bing index rather than a direct fetch, the same downstream dependency described in [do AI crawlers render JavaScript](/blogs/do-ai-crawlers-render-javascript).

Figure 11. Time from publish to entering a recrawl queue, by discovery mechanism. The sitemap narrows the window; the push closes it.

### Ownership verification and payloads

Before you submit, you prove you control the domain: a key of 8 to 128 characters from a-z, A-Z, 0-9 and hyphen (a 32-character UUID with dashes stripped is the default), written into a UTF-8 file at the root named exactly {key}.txt, containing the key and nothing else. If you cannot write to the root, keyLocation lets you host it elsewhere, but verification scope is bounded by the directory the key sits in, a key at /catalog/key.txt authorises submissions under /catalog/ and nothing else. Single URLs go over GET percent-encoded; bulk submissions go over POST as JSON, up to 10,000 URLs, and the host field takes a bare FQDN with no protocol, path, slash or port.

http · both submission patterns

```
# Single URL, HTTP GET
GET /indexnow?url=https%3A%2F%2Fexample.com%2Fdocs&key=fa8c0a469da44e9b8f6a769f291829f5 HTTP/1.1
Host: api.indexnow.org

# Bulk submission, HTTP POST (up to 10,000 URLs)
POST /indexnow HTTP/1.1
Host: api.indexnow.org
Content-Type: application/json; charset=utf-8

{
  "host": "example.com",
  "key": "fa8c0a469da44e9b8f6a769f291829f5",
  "keyLocation": "https://example.com/fa8c0a469da44e9b8f6a769f291829f5.txt",
  "urlList": [
    "https://example.com/docs/rate-limits",
    "https://example.com/docs/architecture",
    "https://example.com/blog/sitemap-audit"
  ]
}
```

Table 4. IndexNow payload fields and response semantics. Most first-run failures are the host field or an unreachable key file.

| Field or code | Type | Validation rule | Purpose |
| --- | --- | --- | --- |
| host | String | FQDN only, no protocol, path, port or slash | Identifies the target origin |
| key | String | 8-128 chars from a-z, A-Z, 0-9 and hyphen | Authenticates ownership |
| keyLocation | String | HTTPS URL to the key file, scope bounded by its directory | Delegated verification when the root is unavailable |
| urlList | Array | Max 10,000 URLs per POST, percent-encoded | The batch of changed pages |
| 200 OK | Response | Payload received and validated | Triggers the inter-engine broadcast |
| 400 Bad Request | Response | Malformed JSON, host or URL format | Schema error, usually the host field |
| 403 Forbidden | Response | Key file missing, unreadable or mismatched | Ownership not proven |

Submitting to one endpoint reaches all of them. The receiving engine verifies your key, then broadcasts the payload to every other participant within about ten seconds, and that fanout is cryptographically signed rather than trusted on faith, each forwarded payload carries an RSA-signed SHA-256 digest of the body that the receiver verifies against the sender's published key set. That is what stops a third party from spoofing submissions on your behalf.

One authenticated POST

to a single IndexNow endpoint.

→

Verify key

receiver confirms ownership.

→

Signed broadcast

fanout to every participant in ~10s.

→

All engines queue

Bing, Yandex, Naver, Seznam, Yep.

Figure 12. One authenticated POST, verified once, broadcast to every participant. The signature headers make the fanout safe to trust.

python · production submission pipeline

```
import json, time
import requests
from typing import Iterable

class IndexNowPipeline:
    ENDPOINT = 'https://api.indexnow.org/indexnow'
    BATCH = 10_000

    def __init__(self, host: str, api_key: str, key_location: str | None = None):
        # host must be a bare FQDN. Strip anything the caller got wrong.
        self.host = host.replace('https://', '').replace('http://', '').strip('/')
        self.api_key = api_key
        self.key_location = key_location or f'https://{self.host}/{api_key}.txt'

    def preflight(self) -> bool:
        """Verify the key file is reachable and exact before submitting."""
        r = requests.get(self.key_location, timeout=10)
        if r.status_code != 200:
            print(f'key file unreachable: {r.status_code} at {self.key_location}')
            return False
        if r.text.strip() != self.api_key:
            print('key file contents do not match the key')
            return False
        return True

    def submit(self, urls: Iterable[str]) -> bool:
        urls = list(dict.fromkeys(urls))          # dedupe, preserve order
        if not urls:
            return True
        if not self.preflight():
            return False
        for i in range(0, len(urls), self.BATCH):
            batch = urls[i:i + self.BATCH]
            payload = {'host': self.host, 'key': self.api_key,
                       'keyLocation': self.key_location, 'urlList': batch}
            r = requests.post(self.ENDPOINT, data=json.dumps(payload),
                              headers={'Content-Type': 'application/json; charset=utf-8'},
                              timeout=15)
            if r.status_code == 200:
                print(f'pushed {len(batch)} URLs')
            elif r.status_code == 429:
                time.sleep(30)                    # back off, then retry
                return self.submit(urls[i:])
            else:
                print(f'submission failed: {r.status_code} {r.text[:200]}')
                return False
        return True

if __name__ == '__main__':
    # changed_urls comes from the hash comparison in the lastmod code above.
    pipeline = IndexNowPipeline('example.com', 'fa8c0a469da44e9b8f6a769f291829f5')
    pipeline.submit(changed_urls)
```

Call it from the deploy hook, after the sitemap is written and the validator has passed. Push only what changed, pushing your whole inventory on every deploy is the IndexNow equivalent of build-stamping your timestamps, and it earns you a 429 followed by a reputation you will not enjoy.

## 10. What can a clean sitemap not do for you?

**Discovery gets the page fetched. It does not get the page cited.** Those are separate systems with separate inputs. Content-level levers, statistics, quotations, cited sources and strict structure, drive citation, and source attribution overperforms for pages without domain authority.

The Princeton, Georgia Tech, Allen Institute and IIT Delhi GEO research measured how specific content modifications change citation performance, with lifts up to 40% over unoptimised baselines. The individual results are more useful than the headline.

Figure 13. Position-adjusted word-count lift by optimisation method. The last bar is the legacy tactic that still shows up in briefs.

Table 5. Content-level levers, measured. Source attribution overperforms for pages without domain authority.

| Method | Mechanism | Word-count lift | Impression lift |
| --- | --- | --- | --- |
| Quotation addition | Verifiable expert statements act as attributable anchors | +41% | +28% |
| Statistics addition | Numerical claims replace qualitative ones | +31% to +41% | +23% |
| Cite external sources | Inline references raise model confidence | +28% (+115% at rank 5) | +14% |
| Fluency optimisation | Cleaner prose lowers parsing cost | +28% | +14% |
| Strict heading hierarchy | Predictable structure improves chunk boundaries | +17.3% citation rate | +18.5% |
| Keyword stuffing | Repetition lowers information density | -8% | +5% |

The rank-5 finding is the interesting one for anyone without an established domain: applying source citation to a page at position five in classical results lifted its generative visibility by 115%, which suggests evidence density can substitute for authority in a way that was never true in link-based ranking. One more distinction worth carrying into reporting, a 2026 benchmark of 21,181 search-layer interactions separates citation selection (whether an engine includes your link) from citation absorption (how much your text shapes the answer).

Figure 14. Citation breadth against per-page influence. Perplexity cites the most sources and absorbs the least from each one.

Table 6. Selection against absorption. A Perplexity citation and a ChatGPT citation are not the same asset.

| Platform | Search trigger rate | Mean citations | Absorption influence | Behaviour |
| --- | --- | --- | --- | --- |
| ChatGPT Search | 98.64% | 6.88 | 0.2713 | Selective picking, deep absorption per page |
| Google AI Overviews | 99.67% | 12.06 | 0.0584 | Broad distribution, shallow extraction |
| Perplexity | 100.00% | 16.35 | 0.0646 | Exhaustive inclusion, low individual influence |

The practical read: optimising for ChatGPT Search rewards evidence density on a small number of pages, while optimising for Perplexity rewards breadth and concise semantic matching across many. Your sitemap strategy is the same in both cases; your content strategy is not. Scoring which of the two you are winning is the subject of [Share of Model, measured properly](/blogs/share-of-model-measurement), and the taxonomy underneath it is [citation vs mention vs recommendation](/blogs/citation-vs-mention-vs-recommendation).

## 11. How do you put a number on it and gate it?

**Two numbers: the tax you are paying, and a Sitemap Health Index you track monthly.** Audits that produce a list get deprioritised; audits that produce a number that moves get funded. Quantify the redirect waste directly, then track a composite over time and gate it in CI.

The first number quantifies the waste: count the redirect hops you serve crawlers per cycle and add a penalty for every URL whose terminal response is temporary, because those get re-requested indefinitely. Multiply by your CDN egress cost per request and you have a finance-legible version, usually small, and that is fine, the real cost was never the bandwidth, it is the fetches you did not get spent on pages you wanted read.

formula · the tax itself

```
tax =  f · Σ  h_i · (1 + τ_i·k)

  f   crawl cycles per period       τ   1 if terminal response is temporary
  h   redirect hops on URL i        k   re-request multiplier for temporaries
  x CDN egress cost/request = a finance-legible number. The real cost was
  never bandwidth; it is the fetches not spent on pages you wanted read.
```

formula · Sitemap Health Index

```
SHI =  0.40·R + 0.30·H + 0.20·γ + 0.10·F

  R  share of declared URLs returning 200 directly
  H  share resolving inside the three-hop ceiling
  γ  timestamp trust (from timestamp_trust above)
  F  share of commercial URLs updated within 30 days
  Score monthly. Treat anything under 80 as an open engineering item.
```

The weights are a starting point, not a law. Response health carries the most because it is a precondition for everything else; freshness carries the least because it is hardest to sustain and easiest to fake. Score it monthly, plot it, and treat anything under 80 as an open engineering item.

yaml · CI gate on the discovery layer

```
# .github/workflows/discovery-gate.yml
name: discovery-gate
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'          # weekly drift check against production
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install httpx
      - name: Root files must return 200 with zero hops
        run: |
          for f in robots.txt sitemap.xml llms.txt; do
            read -r hops status < <(curl -sIL -o /dev/null \
              -w '%{num_redirects} %{http_code}' "https://example.com/$f")
            echo "$f: hops=$hops status=$status"
            [ "$hops" = "0" ] && [ "$status" = "200" ] || exit 1
          done
      - name: Sitemap discovery yield must exceed 0.98
        run: python scripts/validate_sitemap.py
      - name: Push changed URLs to IndexNow
        if: github.event_name == 'push'
        run: python scripts/push_indexnow.py
        env:
          INDEXNOW_KEY: ${{ secrets.INDEXNOW_KEY }}
```

Pair the gate with log telemetry so you catch regressions that ship from outside your repository, which is where most of them come from. Segment requests by verified bot identity rather than user-agent string alone, using reverse and forward DNS or vendor-published IP ranges, and alert when AI-crawler traffic pushes origin p95 latency past 800ms or 5xx past 1%, when spoofed AI user-agents exceed 5% of bot traffic, and immediately if any root discovery file starts returning something other than 200. The verification mechanics tie back to [prompt-to-citation tracking](/blogs/prompt-to-citation-tracking).

## 12. What does the ninety-day sequence look like?

**Routing first, timestamps second, partition and push third, telemetry last.** None of this requires a replatform, it is routing rules, timestamps and telemetry, the highest return per engineering hour available to a marketing team that can get a sprint. The sequence matters: fixing freshness before hop counts ships fresh content into a layer that cannot resolve it.

Table 7. Ninety days, sequenced so each phase depends on the one before it.

| Window | Work | Verification |
| --- | --- | --- |
| Days 1-14 | Run the hop sweep across every declared URL. Collapse multi-hop chains into single rewrites. Make root files transparent. Purge non-200 URLs. | Discovery yield above 0.95, root files at zero hops |
| Days 15-30 | Replace build-stamped lastmod with hash-based generation. Move to ISO 8601 with UTC offsets. Add canonical alignment to the build. | Timestamp trust above 0.9, no future-dated entries |
| Days 31-60 | Split the sitemap by content type into files under 5,000 URLs. Publish a sitemap index. Wire IndexNow into the deploy hook. | Every child file parses, IndexNow returning 200 |
| Days 61-90 | Segment logs by verified bot identity. Alert on status-distribution drift and root-file regressions. Put top commercial URLs on a 30-day review. | Sitemap Health Index above 85 and rising |

The tax is invisible until you go looking for it. There is no notification, no red banner, just a slow divergence between how much you publish and how often you get named. Run the hop sweep. It takes ten minutes and it will tell you whether you are paying.

## Frequently asked questions

### Do XML sitemaps still matter for AI search?

Yes, more than they did, but for a different reason. Training crawlers read your sitemap as a bulk URL manifest, while real-time AI indexers (OAI-SearchBot, Claude-SearchBot, PerplexityBot) read its lastmod values to decide what to recrawl today. That makes the sitemap a scheduling instruction, not just an inventory. The discovery layer, what you declare, how fast it resolves, and how you push changes, decides whether an engine can cheaply turn your URL into a citable document.

### How many redirect hops will AI crawlers follow?

Far fewer than search engines. The HTTP spec permits 30 redirects and Googlebot has historically followed around 10, but real-time AI indexers enforce a hard ceiling of one to three hops and then abandon the request with no client-side error logged anywhere you can see. A legacy URL often burns that budget on scheme, host and trailing-slash normalisation alone, so a bot never reaches your content. Collapse multi-hop chains into a single rewrite rule.

### Why does the lastmod timestamp in my sitemap matter so much?

Because real-time indexers lean on freshness harder than Google does, and a false timestamp is a trust penalty. If your build stamps today's date on all 12,000 URLs every deploy, the indexer recrawls aggressively, finds nothing actually changed, and demotes the recrawl priority of the whole file. Measure timestamp trust as content-changed URLs over lastmod-changed URLs; below 0.2 you are better off publishing no lastmod at all, because an absent signal is neutral while a false one is penalised.

### What status code should a sitemap URL redirect use for AI crawlers?

A 301 (or 308 where the request method and body must survive, such as API feeds and IndexNow payloads). A 301 tells the agent the move is permanent and the new target should be cached, so you pay the hop once. A 302 or 307 tells it nothing moved, so the original URL stays in the index and gets re-requested on every cycle, which is more expensive on every cycle after the first. The worst pattern is a 301 followed by a 302, which invalidates the permanent cache.

### Do root files like robots.txt and sitemap.xml need special handling?

Yes. /robots.txt, /sitemap.xml, /llms.txt and /llms-full.txt must return an explicit 200 from the root host with zero client-visible redirects. PerplexityBot refuses to follow redirects at all for /llms.txt, so a single 301 there makes the file effectively nonexistent to it. Use a transparent internal rewrite (invisible to the crawler), not a redirect (a hop it has to spend). A build that adds a catch-all rewrite emitting a 301 is the most common silent break.

### What is IndexNow and should I use it?

IndexNow inverts discovery from pull to push: when you create, update or delete a page, your origin notifies participating engines directly and the URL enters a recrawl queue in seconds instead of days. Participants include Bing, Yandex, Naver, Seznam and Yep, and a meaningful share of live ChatGPT Search grounding resolves through Bing. Verify domain ownership with a key file at the root, submit only the URLs that genuinely changed (the same hash-derived list your sitemap uses), and call it from the deploy hook after the sitemap validator passes.

References

Figures 1 through 15 are original, built from the data and behaviour analyses in the sources below.

1. [AI crawler families, user agents, and network behaviour. SoRank.](https://www.sorank.com/glossary-geo-seo/ai-crawlers)
2. [AI crawlers and redirects: hop ceilings, status codes, and root file requirements. CaptainDNS.](https://www.captaindns.com/en/blog/ai-crawlers-redirects-handling-gptbot-claudebot-perplexitybot)
3. [Robots.txt behaviour across GPTBot, ClaudeBot, and PerplexityBot. Margen.](https://www.margen.net/robots-txt-ai-crawlers-gptbot-claudebot-perplexitybot/)
4. [AI crawler monitoring, identity verification, and alerting thresholds. Web-Alert.](https://web-alert.io/blog/ai-crawler-bot-monitoring-gptbot-claudebot-perplexitybot-guide)
5. [llms.txt vs robots.txt vs sitemap.xml: what each file does. Ryze.](https://www.get-ryze.ai/blog/llms-txt-vs-robots-txt-vs-sitemap-what-each-does-for-ai-crawlers)
6. [The llms.txt format specification.](https://llmstxtgenerate.com/llms-txt-format/)
7. [The original llms.txt proposal. Answer.AI.](https://www.answer.ai/posts/2024-09-03-llmstxt.html)
8. [AI search indexing, content freshness, lastmod, and IndexNow. NeuralAdX.](https://neuraladx.com/ai-search-indexing-content-freshness-sitemaps-lastmod-indexnow/)
9. [XML sitemap auditing guide. QuickSEO.](https://quickseo.ai/blog/xml-sitemap-checks-the-complete-2026-guide-to-auditing-fixing-your-sitemap)
10. [IndexNow protocol documentation.](https://www.indexnow.org/documentation)
11. [IndexNow participating engines and the shared registry.](https://www.indexnow.org/searchengines)
12. [IndexNow FAQ.](https://www.indexnow.org/faq)
13. [IndexNow API deep dive: JSON payloads and key delegation. MeshWorld.](https://meshworld.in/blog/web-dev/seo/indexnow/indexnow-api-deep-dive/)
14. [GEO: Generative Engine Optimization. Princeton University.](https://collaborate.princeton.edu/en/publications/geo-generative-engine-optimization/)
15. [Generative engine optimisation statistics and freshness benchmarks. Omnibound.](https://www.omnibound.ai/blog/generative-engine-optimization-statistics)

About rawmktg.

rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Sources: AI-crawler network-behaviour analyses, the Princeton/Georgia Tech GEO experiment, the IndexNow protocol docs, and 2026 citation-freshness and selection/absorption benchmarks. Code is a working reference implementation; per-crawler magnitudes are third-party estimates and directional.
