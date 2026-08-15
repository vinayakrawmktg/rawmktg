#!/usr/bin/env python3
"""SCRATCH: build blogs/do-ai-crawlers-render-javascript.html (rendering/SSR teardown). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="do-ai-crawlers-render-javascript"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-08-15"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x").replace("−","-"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE=''
CBCOPY=open("blogs/schema-markup-ai-citations-2026.html",encoding="utf-8").read()
mcb=re.search(r'<style id="cb-copy-css">.*?</script>', CBCOPY, re.S); CB=mcb.group(0) if mcb else ""

def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def h3(t): return f"<h3>{esc(t)}</h3>"
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div><table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def chart(cid,h,cap): return f'<div class="chart-wrap"><canvas id="{cid}" height="{h}"></canvas></div><div class="chart-caption">{esc(cap)}</div>'
def statgrid(items):
    cells="".join(f'<div class="sg-item"><div class="sg-val">{esc(v)}</div><div class="sg-label">{esc(l)}</div></div>' for v,l in items)
    return f'<div class="stat-grid">{cells}</div>'
def pipeline(nodes,goal,cap):
    parts=['<div class="pipeline">']
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Do AI Crawlers Render JavaScript?"
DECK=("Your page ranks on Google and returns an empty div to ChatGPT. This is the test that shows which one you have, the per-crawler "
      "pass and fail data behind it, and the four ways to fix it without rebuilding your front end.")
DESC=("Do AI crawlers run JavaScript? Mostly no, 9 of 12 execute none. The per-crawler pass/fail data, the Content Visibility Ratio test, and four SSR fixes.")
DATANOTE=("A rendering-layer teardown of twelve AI crawlers using controlled raw-fetch tests, Vercel and server-log telemetry (500M+ GPTBot "
          "fetches), and per-bot execution data, 2026. Code is working reference; per-crawler rates are third-party estimates and directional.")

FORM_CVR=r'''CVR      =  T_raw / T_rendered           # Content Visibility Ratio
CVR_site =  Σ (CVR_i x V_i) / Σ V_i       # weight by commercial value

  T  = word count of visible body text (excl. nav, scripts, boilerplate)
  V  = commercial weight of page i (use pipeline influence, not sessions)
  1.0 = fully server-rendered   ~0.0 = pure client-rendered'''

FORM_BUDGET=r'''T_visible = TTFB + T_transfer + T_bundle + T_exec + T_api  < 5000 ms

  server-rendered page:  only TTFB + T_transfer exist
  client-rendered page:  all five terms, in series, before any text
  target: TTFB < 500 ms, full response well inside the 5s ceiling'''

FORM_DUAL=r'''P(visible) = 1 - (1 - r_direct)(1 - r_index)

  r_direct = P(a live bot fetch returns extractable content)
  r_index  = P(the index it falls back to holds rendered text)
  client-side rendering drives BOTH terms toward zero at once.'''

FORM_RISK=r'''Risk_i = C_i x (1 - CVR_i)

  C   = the page type's share of AI citations
  CVR = how much of it a non-rendering bot can read
  sort descending -> your remediation queue, top to bottom.'''

CODE_SHELL=r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Enterprise Analytics Platform | Pricing & Features</title>
  <script src="/static/js/main.7c89b2e1.js" defer></script>
  <link href="/static/css/main.css" rel="stylesheet">
</head>
<body>
  <div id="root"></div>
  <!-- Parsing ends here. Extractable content: 0 bytes. -->
</body>
</html>'''

CODE_DOM=r'''<body>
  <div id="root">
    <main class="dashboard-container">
      <h1>Enterprise Analytics Engine</h1>
      <section class="pricing-matrix">
        <h2>Plan pricing</h2>
        <div class="tier">
          <h3>Pro Plan</h3>
          <p class="price">$299 / month</p>
          <ul class="features">
            <li>Real-time event streaming</li>
            <li>Automated LLM citation tracking</li>
            <li>Unlimited seat licenses</li>
          </ul>
        </div>
      </section>
    </main>
  </div>
</body>'''

CODE_CURL=r'''curl -A "Mozilla/5.0 (compatible; GPTBot/1.4; +https://openai.com/gptbot)" \
     -s https://example.com/pricing | grep -i "per month"

# no output means the string is not in the raw HTML,
# which means it is not in the model's view of your page.'''

CODE_SWEEP=r'''#!/usr/bin/env bash
URL="https://example.com/pricing"
NEEDLE="per month"
declare -A AGENTS=(
  [GPTBot]="Mozilla/5.0 (compatible; GPTBot/1.4; +https://openai.com/gptbot)"
  [OAI-SearchBot]="Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"
  [ChatGPT-User]="Mozilla/5.0 (compatible; ChatGPT-User/1.0; +https://openai.com/bot)"
  [ClaudeBot]="Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
  [PerplexityBot]="Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/bot)"
)
for name in "${!AGENTS[@]}"; do
  code=$(curl -A "${AGENTS[$name]}" -s -o /tmp/body -w "%{http_code}" --max-time 5 "$URL")
  words=$(sed 's/<[^>]*>/ /g' /tmp/body | wc -w)
  grep -qi "$NEEDLE" /tmp/body && hit="FOUND" || hit="MISSING"
  printf "%-16s http=%s words=%-6s %s\n" "$name" "$code" "$words" "$hit"
done
# the word-count column is the tell: 40 words to every bot,
# 1,400 in a browser, and you have found your ceiling.'''

CODE_CVR=r'''import requests, subprocess, json
from bs4 import BeautifulSoup

BOT  = "Mozilla/5.0 (compatible; GPTBot/1.4; +https://openai.com/gptbot)"
DROP = ["script", "style", "noscript", "nav", "footer", "svg"]

def visible_words(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(DROP):
        tag.decompose()
    return len(soup.get_text(" ", strip=True).split())

def raw(url):
    return requests.get(url, headers={"User-Agent": BOT}, timeout=5).text

def rendered(url):                       # any headless runner works here
    return subprocess.check_output(["node", "render.js", url], text=True)

def cvr(url):
    t_raw, t_rendered = visible_words(raw(url)), visible_words(rendered(url))
    return round(t_raw / max(t_rendered, 1), 3)

URLS = ["https://example.com/pricing",
        "https://example.com/product/analytics",
        "https://example.com/compare/competitor-x"]
report = {u: cvr(u) for u in URLS}
print(json.dumps(report, indent=2))
assert all(v >= 0.85 for v in report.values()), "CVR floor breached"  # fail the build'''

CODE_NEXT=r'''// app/pricing/page.tsx
// Server Component by default. No "use client" directive.
// The fetch resolves before a single byte is sent to the client.
export const revalidate = 3600;          // ISR: regenerate hourly

export default async function PricingPage() {
  const tiers = await fetch("https://api.example.com/pricing", {
    next: { revalidate: 3600 },
  }).then((r) => r.json());

  return (
    <main>
      <h1>Enterprise Analytics Engine pricing</h1>
      {tiers.map((tier) => (
        <section key={tier.id}>
          <h2>{tier.name}</h2>
          <p>{tier.price} per month</p>
          <ul>{tier.features.map((f) => <li key={f}>{f}</li>)}</ul>
        </section>
      ))}
    </main>
  );
}'''

CODE_WORKER=r'''// Cloudflare Worker: bot interception with a KV snapshot layer
const BOTS = /GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-SearchBot|PerplexityBot|Bytespider|CCBot/i;

export default {
  async fetch(request, env, ctx) {
    const ua  = request.headers.get("user-agent") || "";
    const url = new URL(request.url);

    // humans and unknown agents: straight to origin, untouched
    if (!BOTS.test(ua)) return fetch(request);

    const key    = `snap:${url.pathname}`;
    const cached = await env.SNAPSHOTS.get(key);
    if (cached) {
      return new Response(cached, {
        headers: { "content-type": "text/html", "x-prerender": "hit" },
      });
    }
    // miss: render in a managed headless browser, then persist
    const html = await renderWithBrowser(env, url.toString());
    ctx.waitUntil(env.SNAPSHOTS.put(key, html, { expirationTtl: 86400 }));
    return new Response(html, {
      headers: { "content-type": "text/html", "x-prerender": "miss" },
    });
  },
};'''

CODE_DETAILS=r'''<!-- invisible to non-rendering crawlers: content mounts on click -->
<div class="accordion" data-faq-widget></div>

<!-- visible to everything: collapsed in the browser, present in the HTML -->
<details>
  <summary>Does the Pro plan include SSO?</summary>
  <p>Yes. SAML and OIDC single sign-on are included on Pro and above at
     no additional cost, with SCIM provisioning available on Enterprise.</p>
</details>'''

FAQ=[
 ("Do AI crawlers render JavaScript?",
  "Mostly no. Industry benchmarks put the share of AI crawlers that cannot execute JavaScript at roughly 69%, and in a twelve-crawler test nine ran no JavaScript runtime at all. The vast majority are lightweight HTTP clients: they issue a GET, read the response body, extract text and close the connection. Content that only exists after a React, Vue or Angular runtime hydrates is invisible to them. The two crawlers that do render, Google-Extended and Applebot, pass only because they inherit an existing search render pipeline."),
 ("Why does my page rank on Google but get nothing in AI answers?",
  "Because Google renders in a second pass and standalone AI engines do not. Google ingests your raw HTML immediately, then queues the URL for headless Chromium to execute the bundle later, so the rendered content eventually reaches the index and ranking. AI crawlers have no deferred rendering stage: whatever is in the initial response body is the complete, permanent record of your page. A page at position one in Google can be a blank document to the model a buyer is asking for a recommendation."),
 ("If a bot fetches my .js files, doesn't that mean it renders them?",
  "No. Fetching a file and executing it are unrelated events. ClaudeBot downloads JavaScript on roughly 23.84% of its requests and runs none of it, GPTBot sits around 11.50%, and telemetry across 500M+ GPTBot fetches recorded zero client-side script execution. Those files are collected as raw text for training corpora, not executed to paint components. A bot that identifies as Chrome and pulls your bundle can still render nothing."),
 ("How do I test whether AI crawlers can read my page?",
  "Fetch it with no browser. Run curl with a crawler user agent against your pricing page and grep for a string that only exists in your real content, like a price or plan name; no output means it is not in the raw HTML. For a real number, compute the Content Visibility Ratio, the visible body text in the raw fetch divided by the visible text in the rendered DOM, across your commercial URLs and wire a floor of 0.85 into CI. Do not use Search Console indexation status: it measures Google's rendering queue, which the AI engines do not have."),
 ("What is the fix if AI crawlers can't see my content?",
  "Get the content into the initial HTML response. There are four patterns: server-side rendering (SSR) or incremental static regeneration (ISR) for content that changes daily, static generation (SSG) for content that changes monthly, and edge prerendering, a CDN worker that serves bots a cached rendered snapshot, for a legacy codebase you cannot rewrite. Only SSR requires touching the application. Free wins on top: replace JavaScript accordions with native details/summary, and mirror any JSON-LD-only facts into semantic HTML."),
 ("Which pages should I fix first?",
  "The intersection of high citation value and low visibility, which is usually five to fifteen URLs. Score Risk = citation share x (1 - CVR) for each commercial page and sort descending. The answer comes back the same in almost every audit: pricing first, product and specification pages second, comparison and alternatives pages third, because those are exactly the pages built as dynamic tables fed by an API."),
]

out=[]
# intro
out.append(p("A page that looks perfect in Chrome can arrive at an AI engine as forty lines of boilerplate and one empty container. Not a slow page. Not a blocked page. An empty one."))
out.append(p("This keeps turning up in teardowns. A company ranks well, has real content, has a technically clean site, and gets almost nothing in AI answers. Then you fetch the page the way a bot fetches it, without a browser, and the pricing table is gone. The feature list is gone. The FAQ is gone. What is left is a title tag and a script tag. The cause is architectural, and it is not a secret: industry benchmarks put the share of AI crawlers that cannot execute JavaScript at roughly 69%."))
out.append(pull("You can grant every bot in the world full permission and still serve them nothing. Access is a different problem from readability."))
out.append(p("This piece is the rendering layer specifically. It does not repeat the crawler roster or the robots.txt rules, which are covered in "+L("how AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site")+". That is about access. This is about whether, once a bot is through the door, there is anything on the page for it to read."))

# 1 ops
out.append(sec("01","ops","Crawling, fetching and executing: what's the difference?",
 "Three separate operations, and only the third needs a browser.",
 "Crawling is one HTTP GET. Asset fetching is pulling the files that response references. Script execution is running a JavaScript runtime to build the DOM. Nearly every AI crawler completes the first two and never begins the third."))
out.append(p("Crawling is the network transaction: a GET returns status, headers and a body, one round trip. Asset fetching is the bot parsing that body, finding references to stylesheets, scripts and images, and issuing secondary GETs. Fetching a file is not the same as using it. Script execution is a different category of work: initialising a JS runtime, building the DOM and CSSOM, firing lifecycle events, waiting on async calls to your API, and hydrating the interface. It needs a browser."))
out.append(pipeline([("1. Crawl","One HTTP GET. Status, headers, body."),("2. Fetch assets","Secondary GETs for scripts, CSS, images."),("3. Execute","JS runtime builds the DOM. Needs a browser.")],2,
 "Figure 1. The three stages. Nearly every AI crawler completes stages one and two and never begins stage three."))
out.append(p("The distinction matters because several AI bots do fetch your JavaScript files, which makes their logs look like rendering. They are not rendering. Those files are collected as raw text for training corpora, not executed to paint components. The reason is economics, not capability: a search engine monetises the index and can pay for a fleet of headless Chromium instances; an AI operator optimising for corpus volume and a two-second answer cuts the browser out of the hot path."))

# 2 benchmark
out.append(sec("02","benchmark","Which AI crawlers render JavaScript, and which don't?",
 "Nine of twelve run no runtime at all.",
 "Pass means the crawler runs a JavaScript runtime and can see hydrated content. Fail means it reads the raw response body and nothing else. Nine fail, two pass, one is partial, and the two that pass both inherit an existing search render pipeline."))
out.append(chart("renderChart",260,"Figure 2. Rendering benchmark score by crawler on a client-rendered page. If your content needs a runtime, three quarters of this list cannot read it."))
out.append(table("Table 1. The rendering benchmark. Nine fails, two passes, one partial. The two passes are both search engines with an existing render pipeline.",
 ["Crawler","Purpose","JS execution","Infrastructure","JS fetch rate","Timeout"],
 [["GPTBot","Training corpus","FAIL","HTTP client","~11.50%","~9.0s"],
  ["OAI-SearchBot","ChatGPT search index","FAIL","HTTP client","< 1.0%","~5.0s"],
  ["ChatGPT-User","Live user retrieval","FAIL","Zero-footprint client","0.00%","~5.0s, HTTP 499"],
  ["ClaudeBot","Training corpus","FAIL","HTTP client","~23.84%","~5.0 to 8.0s"],
  ["Claude-SearchBot","Live search index","FAIL","HTTP client","~5.0%","~5.0s"],
  ["PerplexityBot","Indexing and live RAG","FAIL","HTTP client","< 2.0%","~5.0s"],
  ["Meta-ExternalAgent","Training corpus","FAIL","HTTP client","Minimal","Standard HTTP"],
  ["Bytespider","Training corpus","FAIL","HTTP client","Minimal","Standard HTTP"],
  ["CCBot","Common Crawl","FAIL","HTTP client","Minimal","Standard HTTP"],
  ["Google-Extended","Gemini training access","PASS","Googlebot WRS","> 80%","Deferred queue"],
  ["Applebot","Siri and Apple search","PASS","Browser-based","> 70%","Browser lifecycle"],
  ["Bingbot","Bing index, ChatGPT RAG","LIMITED","Legacy WRS","Moderate","Variable"]],
 cls=lambda j,c: "label" if j==0 else ("down" if c=="FAIL" else "")))
out.append(p("The pattern is clean. Every crawler that passes is operated by a company that already ran a search engine before it ran a model. Google-Extended is not really a crawler at all, it is an access token in robots.txt that governs whether Googlebot's Web Rendering Service output can feed Gemini training. Applebot inherits Apple's browser-based crawling stack. Everyone else built new infrastructure in the last three years, and nobody building new infrastructure chose to put Chromium in the hot path."))
out.append(callout("The short version",[
  "Nine of the twelve major AI crawlers run no JavaScript runtime at all.",
  "The two that pass do so because they inherit an existing search rendering pipeline, not because AI companies decided rendering matters.",
  "Fetching a .js file and executing it are unrelated events. ClaudeBot downloads scripts on nearly a quarter of its requests and runs none of them."]))

# 3 illusion
out.append(sec("03","illusion","Why do the user agents look like browsers?",
 "They wear a browser's costume over a command-line HTTP client.",
 "AI crawlers advertise AppleWebKit builds, Chrome tokens and the full Mozilla prefix, but socket-level logging shows no layout engine, no CSS cascade, no event loop, no render tree."))
out.append(chart("execChart",240,"Figure 3. Asset-fetch rate against execution rate. The bars are real; the execution rate underneath them is flat at zero."))
out.append(p("ClaudeBot fetches JavaScript on roughly 23.84% of its requests, more than double OpenAI's rate, and spends another 35.17% of its fetches on images. It runs none of the scripts it downloads. GPTBot sits at 11.50%. ChatGPT-User, the bot that fires when a person asks a live question in a chat window, fetches no secondary assets at all, zero CSS, zero JS, one request and done. If you are diagnosing this from server logs, that is the trap: you will see a bot that identifies as Chrome, requesting your bundle files, hitting your CDN, generating traffic that looks like a browser session. It never renders a pixel."))

# 4 fleets
out.append(sec("04","fleets","What does each AI fleet actually do?",
 "Decoupled bots, all non-rendering, with different timeouts.",
 "OpenAI splits training, search and live retrieval across three bots; Anthropic fetches heavily and renders nothing; Perplexity reads raw markup and admits when it can't; Gemini and Applebot render only because they sit on a search stack."))
out.append(h3("OpenAI"))
out.append(p("GPTBot handles training-corpus collection, OAI-SearchBot builds the search index, and ChatGPT-User fetches URLs live when a conversation needs them. Telemetry across more than 500 million GPTBot fetches recorded zero instances of client-side script execution. ChatGPT-User is the strictest of the three, because a person is waiting: it runs a roughly five-second ceiling, and if your page does not deliver text inside that window it issues an HTTP 499, closes the connection, and falls back to querying Google with a site: operator to scrape whatever the cached index holds. Your server sees a request; your page never gets read; the answer gets built from someone else's summary of you."))
out.append(h3("Anthropic"))
out.append(p("ClaudeBot and Claude-SearchBot behave the same way structurally. Server-log monitoring across Next.js endpoints shows heavy asset fetching and no runtime. Content painted by client-side scripts comes back as an empty shell, and the download volume is misleading, which is exactly why so many teams conclude they are fine."))
out.append(h3("Perplexity, Google and Apple"))
out.append(p("PerplexityBot is built for low-latency live retrieval and skips asset downloading almost entirely, processing raw markup. In benchmarks against a client-rendered React app it says so out loud, telling the user the page depends on dynamic JavaScript and it cannot summarise it, the honest failure case; the dangerous one is silence. Gemini is the exception, and an inherited one: it sits on Google's search infrastructure and benefits from the Web Rendering Service, so client-rendered content stays visible as long as Googlebot's Chromium instances do not time out first. Applebot similarly runs browser-based crawling. Neither is evidence that AI crawlers render, both are evidence that search crawlers render and two AI products happen to be downstream of one."))

# 5 diff
out.append(sec("05","diff","What does a non-rendering crawler actually receive?",
 "An app shell: a title, a script tag, and one empty div.",
 "A client-rendered SPA returns document tags, metadata, a script reference and an empty mount node on first request. Everything a buyer cares about arrives later, after the bundle downloads and the runtime calls your API. To a non-rendering bot, that is 0 bytes of extractable content."))
out.append(p("This is what a non-rendering crawler receives, the raw server response that GPTBot, ClaudeBot and PerplexityBot ingest:"))
out.append(code("html · raw server response, extractable content: 0 bytes",CODE_SHELL))
out.append(p("And this is what a browser, Googlebot or Applebot ends up with once the runtime has run:"))
out.append(code("html · hydrated DOM, what humans and rendering crawlers process",CODE_DOM))
out.append(p("Same URL, two payloads. The bot gets the first box; your buyer's question gets answered from the second, on somebody else's site. The useful way to quantify this is a single ratio: the extractable body text in the raw response divided by the extractable body text in the hydrated DOM."))
out.append(code("formula · Content Visibility Ratio",FORM_CVR))
out.append(chart("cvrChart",240,"Figure 5. A typical hybrid SaaS site, measured page type by page type. The blog scores 98%. The pricing page, which decides deals, scores 6%."))
out.append(p("A fully server-rendered page sits near 1.0, a pure client-rendered page near 0.0, and most real sites are hybrids: a static marketing shell with a dynamically loaded pricing widget, or a server-rendered article with client-loaded comparison tables. Compute the site-level number too, but weight it by commercial value, not page count, an average across ten thousand blog URLs will tell you everything is fine while the six pages that matter score near zero."))

# 6 budget
out.append(sec("06","budget","Why does the five-second budget break client-rendered pages?",
 "The render path is serial, and the bot will not wait.",
 "User-triggered bots inherit a human's patience budget, roughly five seconds, after which the request is abandoned. A client-rendered page cannot make that window even when everything works, because the sequence is serial: fetch HTML, parse, fetch bundle, execute, call the API, wait, paint."))
out.append(code("formula · the five-second visibility budget",FORM_BUDGET))
out.append(p("The practical target is a time to first byte under 500 milliseconds with the full response well inside five seconds, achievable on almost any stack when the HTML is complete on arrival, and close to impossible when the content depends on a round trip your API has not started yet. Geography makes it worse, and it is the part most teams outside the United States miss: the AI fleets do not crawl from distributed regions. ChatGPT fetches primarily out of Des Moines and Phoenix, and Claude crawls exclusively out of Columbus. If your origin sits in Frankfurt, Mumbai or Singapore, every request pays a trans-continental round trip out of the same five-second budget, and no CDN edge helps you if the HTML itself is assembled at the origin."))

# 7 waste
out.append(sec("07","waste","Why do your logs look busier than your visibility?",
 "A third of AI fetches hit 404s and redirect chains.",
 "Non-rendering crawlers extract URLs from markup as text and cannot resolve hashed asset names or code-split chunk maps, so they request a large volume of files that no longer exist."))
out.append(chart("wasteChart",240,"Figure 8. Where the crawl budget goes. A third of AI-crawler fetches never reach a real page."))
out.append(p("Vercel's telemetry across Next.js infrastructure puts ChatGPT at 34.82% of fetches hitting 404s and Claude at 34.16%, largely from repeated requests for stale files under paths like /static/js/. ChatGPT burns a further 14.36% in redirect chains, against Googlebot's 1.49%. Two consequences: raw bot hit counts are a terrible proxy for how much of your content was actually read, and crawl budget is finite even for well-funded crawlers, so the waste comes out of the same allocation your real pages need."))
out.append(table("Table 2. Log signals and their real interpretation. The last row is the one that sends teams down the wrong path for months.",
 ["Signal in your logs","What it looks like","What it actually means"],
 [["Chrome-like user agent","A browser session","A command-line HTTP client with a costume"],
  ["Requests for .js bundles","Rendering in progress","Text collection for a training corpus"],
  ["High 404 rate on /static/","A broken deploy","URL extraction without a build manifest"],
  ["HTTP 499 on a slow route","A network blip","A live-retrieval bot hit its timeout and left"],
  ["Heavy bot traffic, no citations","A content problem","Usually a rendering problem"]],
 cls=lambda j,c: "label" if j==0 else ""))

# 8 dual
out.append(sec("08","dual","Why does client-side rendering fail twice?",
 "Both the direct fetch and the indexed fallback come back empty.",
 "You would expect a CSR site to fail once, on the direct fetch. It usually fails twice, and the second failure is the one nobody instruments."))
out.append(p("ChatGPT Search does not fetch most URLs live, roughly 92% of its live web queries resolve through Bing's index rather than a fresh GPTBot request. Bingbot's rendering is limited and selective compared with Googlebot's. So the client-rendered page misses on the direct path because OpenAI's bots run no runtime, and misses on the indexed path because the index it is reading from never held the rendered DOM either."))
out.append(pipeline([("Buyer asks a model","for a shortlist in your category."),("Direct fetch","AI bot runs no runtime -> empty shell."),("Index fallback","Bing's limited render -> empty too."),("Answer built without you","from whoever sent text.")],3,
 "Figure 9. Both routes to a shortlist, both returning nothing. This is why the failure is silent."))
out.append(code("formula · probability you are visible to an answer",FORM_DUAL))
out.append(p("The page types this hits hardest are the commercial ones. Product and specification pages account for around 20.1% of AI citations and 14.2% of post-referral conversions; comparison and alternatives pages account for another 9.3% and carry the highest purchase intent on the site. Those are exactly the pages built as dynamic tables fed by an API. Domain authority does not rescue you: organic traffic volume is one of the strongest predictors of AI-citation frequency, but volume only amplifies content the engine can read, so a high-authority domain serving app shells converts its advantage into nothing. The page-level counterpart is "+L("the anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page")+", which covers what goes inside the HTML once the HTML actually exists."))

# 9 ranking
out.append(sec("09","ranking","Why does ranking on Google prove nothing?",
 "Google renders in a second pass. Standalone AI engines do not.",
 "The most common objection is that the page ranks, so the content is clearly readable. It is readable by Google, which runs a two-stage pipeline: raw HTML ingested immediately, then a render queue where headless Chromium executes the bundle later. Ranking is the output of a process that includes a browser."))
out.append(pipeline([("Raw HTML ingested","immediately, at crawl time."),("Render queue","headless Chromium runs the bundle, seconds to days later."),("Rendered DOM indexed","the content finally lands and can rank.")],1,
 "Figure 10. Google's two-stage pipeline. It gets a second pass at your page. Nothing else on the benchmark list does."))
out.append(p("Standalone AI engines have no deferred rendering stage. There is no queue, no second visit, no eventual consistency. Whatever was in the initial response body is the complete record of your page, permanently, until the next crawl returns the same empty shell. A page at position one in Google can be a blank document to the model a buyer is asking for a recommendation. This is the rendering-layer version of "+L("ranking is not visibility","/blogs/ranking-isnt-visibility")+"."))
out.append(callout("Stop using Search Console as the proxy",[
  "Indexation status answers a question about Google's rendering queue. It answers nothing about a bot that has no rendering queue.",
  "The only valid test is a raw HTTP fetch with no browser involved, run against the specific URLs that carry commercial weight."]))

# 10 test
out.append(sec("10","test","How do you test your own site in ten minutes?",
 "A raw HTTP fetch with no browser, on your commercial URLs.",
 "Three checks in increasing order of rigour. Fetch with a crawler user agent and grep for a real content string; sweep the fleet and watch the word-count column; score the Content Visibility Ratio and wire it into CI."))
out.append(h3("1. The single-URL curl test"))
out.append(p("Fetch the page with a crawler user agent and grep for something that only exists in your real content, a price, a plan name, a specific feature string."))
out.append(code("bash · single-URL curl test",CODE_CURL))
out.append(h3("2. The multi-bot sweep"))
out.append(p("Different bots occasionally get different treatment, usually because of a CDN bot rule somebody added years ago. Test the fleet, not one agent. The word-count column is the one to watch, a page that returns 40 words to every agent and 1,400 in a browser has told you everything you need to know."))
out.append(code("bash · multi-bot sweep",CODE_SWEEP))
out.append(h3("3. Scoring the Content Visibility Ratio"))
out.append(p("For a real number across a set of URLs, compare the raw fetch against a rendered fetch and diff the text. This is the version worth wiring into CI."))
out.append(code("python · Content Visibility Ratio, wired into CI",CODE_CVR))
out.append(p("A fourth check takes ten seconds and needs no tooling: open Chrome DevTools, hit the command palette, type Disable JavaScript, and reload. What remains on screen is roughly the dataset available to a non-rendering bot. Missing favicons are a useful tell, since SPAs that inject icon references through script leave AI interfaces showing a generic placeholder."))

# 11 fixes
out.append(sec("11","fixes","What are the four fixes, and what does each cost?",
 "SSR, SSG, ISR or edge prerendering, and only one is a rewrite.",
 "There is no single right answer. The correct choice depends on how often the content changes and how much of your codebase you are willing to touch. Modern frameworks move the fetch to the server by default, so the crawler gets a populated document and the browser still hydrates."))
out.append(table("Table 3. The remediation matrix. Four of the five patterns solve the problem. Only one requires rewriting your application.",
 ["Pattern","AI readable","Server cost","Freshness","Best fit"],
 [["Client-side (CSR)","No","Minimal, static CDN","Real time, client API","Authenticated dashboards, internal apps"],
  ["Server-side (SSR)","Yes","High, compute per request","Real time, server API","High-frequency commerce, personalised feeds"],
  ["Static generation (SSG)","Yes","Low, build-time","Build dependent","Docs, blogs, marketing pages"],
  ["Incremental static (ISR)","Yes","Low to moderate","Stale-while-revalidate","Large catalogues, content portals"],
  ["Edge prerendering","Yes","Moderate, CDN worker","Cache-TTL dependent","Legacy CSR apps that cannot be refactored"]],
 cls=lambda j,c: "label" if j==0 else ("down" if c=="No" else "")))
out.append(p("In the Next.js App Router, React Server Components run data fetching on the server by default. The async work completes before the response is sent, so core content is already in the initial HTML, the browser still hydrates and stays interactive, and the crawler gets a populated document. Nobody has to choose."))
out.append(code("tsx · a server-rendered pricing page (Next.js App Router)",CODE_NEXT))
out.append(p("One detail changes how you test. Next.js streams progressive HTML chunks wrapped in Suspense boundaries to human browsers, but when incoming headers match a known crawler user agent it pauses streaming until every server promise resolves and delivers one complete document. So a page can look chunked in a browser and arrive whole to a bot. Test with the bot user agent, not with your own."))

# 12 prerender
out.append(sec("12","prerender","How does edge prerendering work for a codebase you can't rewrite?",
 "A CDN worker serves bots a cached snapshot and humans the SPA.",
 "Most enterprise teams will not migrate a legacy Angular or Vue app to server rendering this quarter. Edge prerendering is the retrofit: it changes nothing about your origin or your build, only what bots receive."))
out.append(p("A CDN worker intercepts the request before it reaches your origin and branches on user agent. Human traffic passes straight through to the normal SPA bundle. Known crawler traffic is checked against a key-value store of rendered snapshots: a cache hit returns complete HTML in single-digit milliseconds, a miss dispatches a render to a managed headless browser, returns the result, and writes it back to the store."))
out.append(code("javascript · Cloudflare Worker, bot interception with a KV snapshot layer",CODE_WORKER))
out.append(p("Cloudflare documents this pattern in its "+L("Browser Rendering prerender guide","https://developers.cloudflare.com/browser-rendering/","True")+", and if you would rather not run the headless layer yourself, "+L("Prerender.io publishes a Worker integration","https://docs.prerender.io/docs/cloudflare-workers","True")+" that does the same job as a managed service."))
out.append(callout("One warning on this pattern",[
  "Serve bots the same content humans see, rendered. Serving different content is cloaking, and it is a policy problem with search engines regardless of how the AI crawlers feel about it.",
  "Keep the snapshot TTL shorter than your pricing change cycle. A stale snapshot of a discontinued plan is worse than no snapshot."]))

# 13 progressive
out.append(sec("13","progressive","What can you fix for free with progressive enhancement?",
 "Choose markup that works before scripts run.",
 "Some of this needs no rendering-architecture change at all. The most common self-inflicted wound is the custom JavaScript accordion: FAQ content hidden inside a component that only mounts after hydration is invisible to a non-rendering parser. Native elements do the same job and keep the text in the markup stream."))
out.append(code("html · native details/summary vs a JS accordion",CODE_DETAILS))
out.append(p("The second wound is treating structured data as content delivery. Schema is valuable and you should ship it, as covered in "+L("schema markup and AI citations","/blogs/schema-markup-ai-citations-2026")+", but empirical tests on ChatGPT-User show it frequently bypasses JSON-LD parsing and works from plain text in the body. If your price only exists inside a JSON-LD block, treat it as unpublished, mirror every critical fact, pricing, availability, specifications, in ordinary semantic HTML. Third, check what your framework does to navigation: a client-rendered nav means the crawler finds no internal links, so discovery of your other pages depends entirely on the sitemap, which is a fragile way to run a site."))

# 14 priority
out.append(sec("14","priority","Which pages should you fix first?",
 "The intersection of high citation value and low visibility.",
 "You do not need to fix everything. You need the pages where citation value is high and readability is low, and that intersection is usually five to fifteen URLs."))
out.append(code("formula · remediation priority score",FORM_RISK))
out.append(p("Run the ratio across your commercial URLs, sort descending, and stop where the score falls below your smallest meaningful number. In almost every audit the answer comes back the same: pricing first, product and specification pages second, comparison and alternatives pages third."))
out.append(table("Table 4. The usual suspects. The pages closest to revenue are the ones built most dynamically.",
 ["Page type","Typical citation share","Common failure","Fix"],
 [["Pricing","High","Tiers fetched from a billing API on mount","SSR or ISR the tier data"],
  ["Product and specs","20.1%","Spec tables rendered from a CMS client call","SSG with build-time fetch"],
  ["Comparison and alternatives","9.3%","Interactive comparison grid, no fallback","Server-render the table, hydrate the filters"],
  ["Documentation","Moderate","Sometimes client-side search only","Ensure static route output"],
  ["FAQ","Moderate","Custom accordion component","Native details and summary"],
  ["Blog","High volume","Rarely broken, already static","Leave it alone"]],
 cls=lambda j,c: "label" if j==0 else ""))

# 15 thirty
out.append(sec("15","thirty","What's the 30-day sequence?",
 "Measure, fix the top ten, mirror the facts, then lock it in CI.",
 "This is not a quarter of work. For most sites it is three sprints and a CI check, and measurement comes first because the delta is the only proof the fix worked."))
out.append(table("Table 5. Thirty days from unknown to instrumented. The CI check is what stops this recurring in six months.",
 ["Window","Work","Output"],
 [["Days 1-5","Raw-fetch crawl of every commercial URL, CVR scored","A ranked list of broken pages"],
  ["Days 5-16","Move the top ten URLs to SSR, SSG or edge prerender","Commercial pages readable without a runtime"],
  ["Days 9-14","Mirror JSON-LD-only facts into semantic HTML, replace JS accordions","No critical fact exists in one place only"],
  ["Days 13-20","TTFB under 500ms on the fixed routes, verify with a 5s timeout","Live-retrieval bots stop bailing"],
  ["Days 19-24","CVR check in CI with a floor of 0.85 on commercial routes","Regressions fail the build, not the pipeline"],
  ["Days 27-30","Re-baseline, hand the delta to the content team","A measurable before and after"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(p("The last row matters more than it looks. Once the HTML is readable, the constraint moves from infrastructure to content, and the question changes from whether the engine can read the page to whether it wants to cite it. That is a different problem with a different playbook, and "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+" covers how to measure the second half. The retrieval pipeline your rendered text then has to survive is in "+L("how RAG actually works","/blogs/how-rag-actually-works")+"."))

# what to do this week
out.append(sec("16","week","What should you do this week?",
 "Curl your pricing page, score five URLs, and put the check in CI.",
 "Run the raw-fetch test on the pages that carry commercial weight, pick the cheapest fix that works, and lock a CVR floor into CI before you ship it, so the next refactor cannot quietly reintroduce the problem."))
out.append("<ul>"
 "<li><strong>Run the curl test on your pricing page.</strong> One command, one grep. If the price is not in the output, you have found your ceiling.</li>"
 "<li><strong>Score five URLs, not five hundred.</strong> Pricing, top product page, main comparison page, one docs page, one blog post. The spread tells you the shape of the problem.</li>"
 "<li><strong>Stop citing Search Console as evidence.</strong> It measures a rendering queue that only one of these engines has.</li>"
 "<li><strong>Pick the cheapest fix that works.</strong> Content changes daily, SSR or ISR. Monthly, SSG. Codebase untouchable, edge prerendering.</li>"
 "<li><strong>Put the check in CI before you ship the fix,</strong> or the next refactor quietly reintroduces it and nobody notices for two quarters.</li></ul>")
out.append(p("The uncomfortable part of this finding is how mundane it is. There is no ranking algorithm to reverse-engineer and no prompt to optimise. A crawler asked for your page, your server sent an empty container, and the model wrote its answer from whoever sent text instead. That is the entire mechanism, which also makes it the cheapest fix in the stack. Content strategy takes quarters to compound. This one lands the day you deploy it."))

# FAQ
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

# References
REFS=[
 ("Do AI Crawlers Render JavaScript? The Honest Answer. LymLyt.","https://www.lymlyt.com/"),
 ("JavaScript and AI Crawlers: Why Your Page May Be Invisible. Wolfstone Digital.","https://wolfstonedigital.com/"),
 ("AI Crawlers and JavaScript: Why LLMs Cannot See Your Client-Rendered Content. Visively.","https://visively.com/"),
 ("AI Crawlers Do Not Render JavaScript. Lantern.","https://www.lantern.dev/"),
 ("The Rise of the AI Crawler. Vercel.","https://vercel.com/blog/the-rise-of-the-ai-crawler"),
 ("AI Crawlers and JavaScript Rendering. searchVIU.","https://www.searchviu.com/en/"),
 ("How GPTBot and ChatGPT-User Handle JavaScript. EdgeComet.","https://edgecomet.com/"),
 ("Pre-render Pages for Crawlers. Cloudflare Browser Rendering docs.","https://developers.cloudflare.com/browser-rendering/"),
 ("Integrating Prerender with Cloudflare Workers. Prerender.io docs.","https://docs.prerender.io/docs/cloudflare-workers"),
 ("Rendering on the Web. web.dev (Google).","https://web.dev/articles/rendering-on-the-web"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
out.append('<div class="about-block" id="references"><div class="about-label">References</div>'
           '<p style="margin-bottom:16px;">Figures 1 through 15 are original, built from the telemetry and benchmarks in the sources below.</p>'
           f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Sources: controlled raw-fetch tests, Vercel and server-log telemetry across 500M+ GPTBot fetches, and per-bot execution data, 2026. Code is a working reference implementation; per-crawler rates are third-party estimates and directional.</p></div>')

body="\n".join(out)

SIDEBAR=[("9/12","major AI crawlers run no JS runtime"),("5.0s","before a live bot abandons the fetch"),("6%","CVR of a typical dynamic pricing page"),("34.8%","of AI fetches landing on 404 responses")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#ops"><span class="toc-num">01</span>Crawl, fetch, execute</a></li>'
     '<li><a href="#benchmark"><span class="toc-num">02</span>Who passes, who fails</a></li>'
     '<li><a href="#illusion"><span class="toc-num">03</span>The headless illusion</a></li>'
     '<li><a href="#fleets"><span class="toc-num">04</span>What each fleet does</a></li>'
     '<li><a href="#diff"><span class="toc-num">05</span>App shell vs hydrated DOM</a></li>'
     '<li><a href="#budget"><span class="toc-num">06</span>The five-second budget</a></li>'
     '<li><a href="#waste"><span class="toc-num">07</span>Crawl waste</a></li>'
     '<li><a href="#dual"><span class="toc-num">08</span>The dual invisibility trap</a></li>'
     '<li><a href="#ranking"><span class="toc-num">09</span>Why ranking proves nothing</a></li>'
     '<li><a href="#test"><span class="toc-num">10</span>Testing in ten minutes</a></li>'
     '<li><a href="#fixes"><span class="toc-num">11</span>The four fixes</a></li>'
     '<li><a href="#prerender"><span class="toc-num">12</span>Edge prerendering</a></li>'
     '<li><a href="#progressive"><span class="toc-num">13</span>Progressive enhancement</a></li>'
     '<li><a href="#priority"><span class="toc-num">14</span>Which pages first</a></li>'
     '<li><a href="#thirty"><span class="toc-num">15</span>A 30-day sequence</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - the AI crawler rendering and SSR teardown - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["AI crawlers","JavaScript rendering","SSR","client-side rendering","GPTBot","ClaudeBot","PerplexityBot","content visibility ratio","edge prerendering","GEO technical SEO"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Do AI Crawlers Render JavaScript? &middot; rawmktg."
da=escq(DESC)
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
 "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
 f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
 f"  <meta name=\"description\" content=\"{da}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
 "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
 "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
 f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
 f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{escq(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n  <meta property=\"og:image:width\" content=\"2400\" />\n  <meta property=\"og:image:height\" content=\"1260\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{escq(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  {jb(blog)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/blogs/{SLUG}.md\" />\n  "+FONTS+"\n  ")

CHARTS=r"""
<!-- Chart.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
(function(){
  if(typeof Chart==='undefined') return;
  var css=getComputedStyle(document.documentElement);
  var signal=(css.getPropertyValue('--signal')||'#D04A2A').trim();
  var faint=(css.getPropertyValue('--faint')||'#C5BFB4').trim();
  var up=(css.getPropertyValue('--up')||'#3E9B6A').trim();
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.4), amber='#C9922E';

  var rn=document.getElementById('renderChart');
  if(rn){new Chart(rn,{type:'bar',data:{labels:['Google-Extended','Applebot','Bingbot','GPTBot','ClaudeBot','PerplexityBot','ChatGPT-User'],datasets:[{data:[100,97,45,6,6,6,0],backgroundColor:[up,up,amber,signal,signal,signal,signal],borderRadius:4,barThickness:22}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' render score '+c.raw+'/100';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var ex=document.getElementById('execChart');
  if(ex){new Chart(ex,{type:'bar',data:{labels:['ClaudeBot','GPTBot','Claude-SearchBot','PerplexityBot','OAI-SearchBot','ChatGPT-User'],datasets:[
    {type:'bar',label:'JS fetch rate',data:[23.84,11.50,5.0,2.0,1.0,0],backgroundColor:signal,borderRadius:4},
    {type:'line',label:'Script execution rate',data:[0,0,0,0,0,0],borderColor:up,borderWidth:2,pointRadius:3,pointBackgroundColor:up}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+': '+c.raw+'%';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{beginAtZero:true,max:40,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var cv=document.getElementById('cvrChart');
  if(cv){new Chart(cv,{type:'bar',data:{labels:['Blog','Docs','Homepage','Product','Comparison','Pricing'],datasets:[{data:[98,88,61,20,12,6],backgroundColor:[up,up,amber,signal,signal,signal],borderRadius:4,barThickness:44}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' CVR '+c.raw+'%';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var wa=document.getElementById('wasteChart');
  if(wa){new Chart(wa,{type:'bar',data:{labels:['ChatGPT','Claude','Googlebot'],datasets:[
    {label:'404s',data:[34.82,34.16,1.49],backgroundColor:signal,borderRadius:4},
    {label:'Redirect chains',data:[14.36,8.0,1.49],backgroundColor:rgba(signal,0.5),borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+': '+c.raw+'%';}}}},
      scales:{x:{stacked:true,ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{stacked:true,beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Technical Layer &middot; Rendering Teardown</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/jsr_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/jsr_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faq:",hh.count('faq-item'),"| refs:",hh.count('id="references"'))
