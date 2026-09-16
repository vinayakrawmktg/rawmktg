#!/usr/bin/env python3
"""SCRATCH: build blogs/ai-visibility-tools-compared.html (deep 7-tool buyer's guide)."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="ai-visibility-tools-compared"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-09-16"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x").replace("−","-"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav',"</nav>"); NEWS=sl('<section class="newsletter-section',"</section>"); FOOT=sl('<footer class="site-foot',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
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
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'
def prof(use,icp): # compact use-case / ICP line
    return (f'<p><strong>Use case:</strong> {norm(use)}<br><strong>Target audience / ICP:</strong> {norm(icp)}</p>')

HEADLINE="AI Visibility Tools, Compared"
DECK=("A deep buyer's guide to the seven platforms that track whether ChatGPT, Perplexity, Gemini and Google AI answers mention your brand. Each "
      "profiled on use case, ideal customer, exact per-tier pricing, and what customers actually say, plus the job none of them finish.")
DESC=("An in-depth 2026 comparison of seven AI visibility tools, Profound, Peec AI, AthenaHQ, Scrunch AI, Otterly, Semrush and SE Ranking. Use case, ICP, exact per-tier pricing, and customer reviews for each, plus API vs scraping, ghost citations, which to buy, and why tracking is only half the job.")
DATANOTE=("Pricing, tiers and coverage are published vendor figures gathered in September 2026 and change often, confirm before you buy. Customer "
          "sentiment is summarised from public reviews (G2, Capterra and independent write-ups). RawMktg builds a diagnosis-and-remediation product in "
          "this space and is not affiliated with, nor paid by, any tracker here; the comparison is independent and sourced.")

CODE_TRACKER=r'''# minimum-viable AI visibility tracker: run a prompt set, log who gets named.
# The paid tools automate this across engines; the logic itself is not complicated.
import itertools, csv, re, datetime as dt
from openai import OpenAI            # swap in Perplexity / Gemini / Anthropic clients too

client  = OpenAI()
BRAND   = "YourBrand"
PROMPTS = open("prompts.txt").read().splitlines()   # the questions your buyers actually ask
RUNS    = 5                                          # one run per prompt is noise, see Share of Model
URL_RE  = re.compile(r"https?://([^/\s)]+)")

rows = []
for prompt, run in itertools.product(PROMPTS, range(RUNS)):
    # IMPORTANT: enable the web-search tool, or you measure parametric memory, not real citations.
    r = client.responses.create(model="gpt-5", tools=[{"type": "web_search"}], input=prompt)
    text = r.output_text
    rows.append({
        "date":    dt.date.today().isoformat(),
        "engine":  "chatgpt",
        "prompt":  prompt,
        "named":   BRAND.lower() in text.lower(),        # the binary that matters
        "domains": sorted(set(URL_RE.findall(text))),    # your outreach + competitive map
    })

csv.DictWriter(open("visibility.csv","w"), fieldnames=list(rows[0])).writerows(rows)
# Answer Share = share of (prompt x run x engine) rows where named == True.'''

out=[]; A=out.append

A(sec("01","what","What is an AI visibility tool, and what does it actually do?",
      "It runs a fixed set of buyer questions against AI answer engines on a schedule, then records whether your brand was named, which URLs were cited, and which competitors were recommended instead.",
      "That is the whole category in one sentence. Everything else, dashboards, sentiment, alerts, share-of-voice charts, is presentation layered on top of that loop."))
A(p("The category exists because "+L("winning Google is no longer the same as winning AI","/blogs/winning-google-isnt-winning-ai")+". A buyer now describes a problem to ChatGPT, Perplexity, Gemini or Google's AI answers and gets back a shortlist assembled from sources they never see and you do not control. Classic rank tracking cannot observe any of it, there is no blue-link SERP to scrape, so a new instrument had to appear. This guide profiles seven of them in depth: Profound, Peec AI, AthenaHQ, Scrunch AI, Otterly, Semrush and SE Ranking."))
A(p("Every product here runs the same three-step loop: store a prompt set, query one or more answer engines on a cadence, and parse each answer for your brand, the cited domains, and the rival brands named around you. The differences that decide which one is right for you are narrow but consequential: how the tool collects the data, how many engines it covers, how sound its sampling is, its use case and ideal customer, its real per-tier price, what its customers actually report, and the job it leaves unfinished. We take them in that order."))

A(sec("02","collect","How do these tools actually get their data?",
      "Two ways, and the choice determines whether your numbers are real: API calls, or UI scraping that simulates a logged-in user in a browser.",
      "It is the single most important thing to ask a vendor, and the one most buyers never ask."))
A(p("An API call is cheap, fast and stable, but the API is not the product your buyer uses. API responses frequently strip the citations, source links and formatting that appear in the real chat interface, and an API call made without the web-search tool enabled returns the model's parametric memory, not a live retrieved answer, so the citation data is either missing or synthetic. Measure that and you are measuring a different product than the one your customer sees."))
A(p("UI scraping drives a real browser session against the actual front end, so it captures what a human would: the rendered answer, the citation chips, the sources panel, the follow-up context. It is slower, more fragile and more expensive to run at scale, but it is the only method that reflects reality. The practical tell when evaluating a tool is simple: ask whether its numbers come from the API or the UI, and be sceptical of any dashboard that will not answer."))
A(table("Table 1. API versus UI scraping, the tradeoff that decides data quality.",
        ["","API collection","UI scraping"],
        [["What it sees","Model output, often without citations or the search tool","The rendered answer a real user sees, with citation chips and sources"],
         ["Cost & speed","Cheap, fast, stable","Expensive, slower, breaks when the UI changes"],
         ["Citations","Often stripped or synthetic (parametric memory)","Captured as displayed"],
         ["Accuracy vs reality","An approximation","What your buyer actually experiences"]]))
A(p("This is why two tools pointed at the same brand, same prompts, same day can report different numbers. Before you compare scores across tools, confirm you are comparing the same collection method."))

A(sec("03","wrong","What can the numbers get wrong?",
      "More than vendors admit. AI answers hallucinate citations, cite a domain without naming the brand, misread sentiment, and vary run to run, so a single confident number is usually three kinds of error stacked together.",
      "A tool that hides its error bars is selling certainty it does not have."))
A(p("Generative models invent sources, or subtly alter a real domain, and legacy tools that scrape the answer text and regex out URLs will log those as real citations, producing false positives. The defence is cross-model overlap: a source that appears for the same query across several engines is far more likely to be genuine than a one-off that may be a hallucination. Then there are ghost citations, where a domain is cited but the brand is never named in the text, only reliably caught by UI-level detection. Sentiment scoring, which several tools sell, is only around 70 to 85 percent accurate because AI prose is full of hedged language classifiers misread. And the same prompt returns different answers on different runs, which is why "+L("one run per prompt is measurement theatre","/blogs/share-of-model-measurement")+" and five to ten runs is the floor."))
A(table("Table 2. The four errors baked into every AI visibility number, and how a good tool mitigates each.",
        ["Error","What happens","Mitigation to look for"],
        [["Hallucinated citation","Model invents or alters a source URL; tool logs a false positive","Cross-model overlap; UI-verified sources"],
         ["Ghost citation","Domain cited but brand not named in the text","UI-level detection, not text-string parsing"],
         ["Sentiment misread","Hedged AI prose misclassified (~70-85% accuracy)","Treat sentiment as directional; sample manually"],
         ["Run-to-run variance","Same prompt, different answer each run","5-10 runs per prompt; report the distribution"]]))

A(sec("04","evaluate","How do you evaluate an AI visibility tool?",
      "On six axes: data collection method, platform coverage, prompt methodology, data depth, actionability, and pricing transparency.",
      "Weight collection method and methodology above the dashboard. A beautiful chart built on API data and one run per prompt is a confident wrong answer."))
A(table("Table 3. The six things to check before you buy, and the red flag on each.",
        ["Criterion","What to check","Red flag"],
        [["Data collection","API or UI scraping; whether the search tool is on","Won't say; API-only sold as 'what users see'"],
         ["Platform coverage","ChatGPT, Google AI Overviews, AI Mode, Perplexity, Gemini, Copilot, Grok, Claude","Only ChatGPT, or 'AI search' with no engine list"],
         ["Prompt methodology","Prompt count, runs per prompt, whether you control the set","One run per prompt; a fixed list you cannot edit"],
         ["Data depth","Share of voice, sentiment, exact cited URLs, competitors named","Mention counts only, no source URLs"],
         ["Actionability","Whether it tells you why you are missing and what to fix","A number that moves with no next step"],
         ["Pricing transparency","Published tiers, engines and query volume per tier","'Book a demo' only; basic engines as paid add-ons"]]))
A(p("The reference for the methodology axis is the "+L("Share of Model measurement discipline","/blogs/share-of-model-measurement")+": a defensible prompt portfolio, multiple runs per prompt, and every number reported with its prompt set, engine and date attached. Hold any tool you trial to that bar."))

A(sec("05","compared","The seven tools at a glance",
      "They span a 10x price range and three shapes: enterprise depth (Profound, and Evertune above it), clean mid-market analytics (Peec, AthenaHQ, Scrunch), and budget or agency-friendly tracking (Otterly, and the SEO incumbents Semrush and SE Ranking).",
      "Entry prices below are published tiers as of September 2026 and move constantly; the deep profiles that follow give every tier."))
A(chart("priceChart",300,"Figure 1. Published entry price per month (September 2026), USD. Enterprise tiers run into the thousands."))
A(chart("engineChart",300,"Figure 2. Maximum answer engines tracked (top tier or with add-ons). Entry tiers often cover far fewer, Profound's Starter is ChatGPT only."))
A(table("Table 4. The field at a glance. Entry price and top-tier engine count set the bookends; the profiles below fill in every tier.",
        ["Tool","Entry price","Top-tier engines","Shape","Ideal customer in one line"],
        [["Otterly.ai","$29/mo","7 (4 core + add-ons)","Budget / agency","Solopreneurs and agencies running client AEO reporting"],
         ["Peec AI","~$92/mo (€85)","6","Mid-market analytics","B2B teams wanting clean, shareable measurement + sentiment"],
         ["Profound","$99/mo","~11","Enterprise depth","Mid-market to enterprise brands with a real AI-search case"],
         ["Semrush AI Toolkit","$99/mo per domain","7","Incumbent suite","SEO teams already living in Semrush"],
         ["SE Ranking (SE Visible)","$99/mo","4","Incumbent, affordable","Agencies and SMBs wanting cheap prompt tracking"],
         ["AthenaHQ","$295/mo","8","Mid-market + recommendations","Teams wanting analytics plus some guidance, one brand"],
         ["Scrunch AI","$300/mo","8","Monitoring + agent analytics","Teams also watching how AI agents crawl their site"]],
        cls=lambda j,c:("num" if j==1 else "")))

# ---- deep profiles ----
A(sec("06","profound","Profound: the enterprise-depth pick",
      "The deepest and broadest tracker, ~11 engines with sentiment, real-time metadata and an MCP server, at an enterprise price. G2 rates it 4.6.",
      "Buy it when coverage, governance and analytics depth are the requirement, not when you just need a number."))
A(prof("Enterprise-grade AI visibility analytics and governance across the widest set of answer engines, with automation (MCP) for technical teams.",
       "Mid-market to enterprise brands with a genuine AI-search business case and budget; over-built for a solo marketer."))
A(table("Table 5. Profound pricing (published, September 2026; annual billing gives two months free).",
        ["Tier","Price / month","What you get"],
        [["Starter","$99 ($82.50 annual)","ChatGPT only, 50 tracked prompts, 100 agent credits, 1 seat"],
         ["Growth","$399 ($332.50 annual)","3 answer engines, 100 prompts, 400 agent credits, 3 seats"],
         ["Enterprise","Custom (~$2,000-$5,000+)","Up to ~11 engines, multi-brand, SSO/SAML, SOC 2, MCP server, 24h SLA"]],
        cls=lambda j,c:("num" if j==1 else "")))
A(p("<strong>What customers say.</strong> G2 reviewers (4.6/5) consistently praise the depth of analytics, the reporting value, the rapid product updates and strong support. The recurring criticisms are that pricing is high enough to exclude smaller teams and that the breadth carries a learning curve; most reviewers feel the value lands for mid-market and enterprise brands but is hard to justify for a small team without a clear AI-search case."))

A(sec("07","peec","Peec AI: the clean mid-market analytics",
      "The strongest clean, self-serve analytics-and-reporting tool for the majors, reporting mention rate, position-in-answer and sentiment, with unlimited seats and a no-card trial.",
      "The sensible default for a B2B team that wants a trustworthy, shareable number without an enterprise contract."))
A(prof("Clean measurement and reporting of brand mentions, answer position and sentiment across the major engines, with source-level citation data for outreach.",
       "Mid-market B2B marketing teams and in-house SEOs who want a dashboard to show leadership, not an optimization engine."))
A(table("Table 6. Peec AI pricing (published, September 2026; annual in brackets). Extra AI models beyond three cost €30-140/mo.",
        ["Tier","Price / month","What you get"],
        [["Starter","€85 (€70)","50 prompts, pick 3 engines, sentiment, unlimited seats"],
         ["Pro","€205 (€180)","150 prompts, ~3,500 queries, API access"],
         ["Advanced","€425 (€360)","350 prompts, higher volume"],
         ["Enterprise","Custom","All engines incl. Claude Sonnet, GPT-5 Search, DeepSeek, Qwen, Mistral"]],
        cls=lambda j,c:("num" if j==1 else "")))
A(p("<strong>What customers say.</strong> Reviewers praise the clean interface, the suggested-prompts feature that saves setup time, the source-level citation data, and that sentiment is bundled into the mid tier where rivals charge a premium or omit it; unlimited seats and a no-card trial make it easy to start. The two consistent gripes: paying for broad engine coverage adds a few hundred euros on top of the €205 headline (the most common billing surprise), and Peec is a monitoring tool, it shows what is happening, not how to act on it."))

A(sec("08","athena","AthenaHQ: analytics with a nudge toward action",
      "A mid-market tracker across eight platforms that pairs monitoring with recommendations, on a credit model that makes real spend less predictable than the $295 sticker.",
      "A middle ground for a single brand that wants analytics plus some guidance, if you can live without a free trial."))
A(prof("AI visibility analytics across eight engines with an 'Ask Athena' assistant and implementable recommendations, for a single brand and country by default.",
       "Mid-market in-house teams wanting more direction than a pure monitor; less suited to agencies because per-brand cost scales fast."))
A(table("Table 7. AthenaHQ pricing (published, September 2026). Monitoring cadence and Ask Athena usage both draw from the credit pool.",
        ["Tier","Price / month","What you get"],
        [["Self-Serve","$295","3,600 credits, 8 platforms, 3 seats, 1 country"],
         ["Growth","$545","10,000 credits"],
         ["Enterprise","~$2,000+","multi-brand / multi-country; extra credits $100 per 1,250"]],
        cls=lambda j,c:("num" if j==1 else "")))
A(p("<strong>What customers say.</strong> One reviewer reported \"immediate positive impacts\" from implemented recommendations inside the first month, and the analytics are well regarded. The consistent caution is the credit model: the $295 headline understates real spend because monitoring and Ask Athena share one credit pool, per-brand pricing scales faster than most agency retainers, and there is no free trial, so you commit sight-unseen."))

A(sec("09","scrunch","Scrunch AI: monitoring plus agent analytics",
      "A category-leading monitor that also watches how AI agents and crawlers use your site, dense on engines (8 engines, 700 prompts at $500), with a 7-day trial and no free tier.",
      "For teams who want the AI-answer analytics layer and the agent-experience layer in one tool."))
A(prof("AI visibility monitoring plus agent-experience analytics, how AI crawlers and agents fetch and use your pages, across the major engines at high prompt density.",
       "Mid-market to enterprise teams who care about both citation share and how agents interact with the site; not a fix-it tool."))
A(table("Table 8. Scrunch AI pricing (published, September 2026; annual in brackets).",
        ["Tier","Price / month","What you get"],
        [["Starter","$300 ($250)","Monitoring across the major engines"],
         ["Growth","$500 ($417)","8 engines, 700 prompts (~$62.50 per engine), agent analytics"],
         ["Enterprise","Custom","multi-brand"]],
        cls=lambda j,c:("num" if j==1 else "")))
A(p("<strong>What customers say.</strong> Reviewers call Scrunch a category leader in visibility monitoring and note its engine density beats most direct competitors on a per-engine basis. The limits are the familiar ones: actionable insight stops at monitoring (it surfaces gaps but does not fix them), the price is high, and there is only a 7-day trial with no free tier, so it is hard to adopt as a standalone solution."))

A(sec("10","otterly","Otterly.ai: the budget and agency pick",
      "The cheapest entry point at $29 and the most agency-friendly, pairing low prices with a 25-factor GEO audit on every prompt and unlimited workspaces higher up.",
      "The easiest way to find out whether you have a problem at all, and a workhorse for agencies running many client accounts."))
A(prof("Affordable AI visibility tracking plus per-prompt GEO auditing and agent analytics, built to scale across many client workspaces.",
       "Solopreneurs and consultants on Lite; marketing and AEO agencies on Standard and up, where reviewers call it essential for client reporting."))
A(table("Table 9. Otterly.ai pricing (published, September 2026; 15% annual discount). Claude, AI Mode and Gemini are add-ons.",
        ["Tier","Price / month","What you get"],
        [["Lite","$29","15 prompts, 4 engines (ChatGPT, AI Overviews, Perplexity, Copilot), daily tracking, 1 workspace, 1,000 GEO audits/mo"],
         ["Standard","$189","100 prompts, API + MCP, agent analytics, unlimited workspaces, 5,000 GEO URL audits, Looker connector"],
         ["Premium","$489","400 prompts, same features at higher volume"],
         ["Enterprise","from $1,000","custom"]],
        cls=lambda j,c:("num" if j==1 else "")))
A(p("<strong>What customers say.</strong> G2 reviewers are mostly small businesses and agencies: the $29 Lite plan suits solopreneurs tracking one brand, while the $189 Standard plan is cited by marketing and advertising reviewers as essential for client reporting and AEO service delivery. The catch is that some engines you will want (Claude, AI Mode, Gemini) are add-ons, so the real cost for full coverage runs above the headline."))

A(sec("11","semrush","Semrush AI Visibility Toolkit: the incumbent suite",
      "AI tracking bolted onto the SEO suite you may already run, from $99/mo per domain, convenient and familiar but shallower than a specialist.",
      "The path of least resistance if your team already lives in Semrush."))
A(prof("AI brand and competitor visibility tracking plus an AI-readiness site audit, inside the wider Semrush SEO platform.",
       "SEO teams already paying for Semrush who want to extend into AI answers without a new vendor or login."))
A(table("Table 10. Semrush AI visibility pricing (published, September 2026). Real setups land $300-$1,090+ once domains, seats and prompts are added.",
        ["Tier","Price / month","What you get"],
        [["AI Toolkit (Base)","$99 per domain","25 prompts, ChatGPT/Google AI/Gemini/Perplexity, brand + competitor analysis, AI-readiness audit, 300 reports/day"],
         ["Semrush One: Starter","$199","50 prompts"],
         ["Semrush One: Pro+","$299","100 prompts"],
         ["Semrush One: Advanced","$549","200 prompts"],
         ["Enterprise AIO","Custom","200+ prompts, adds Claude, Copilot, DeepSeek"]],
        cls=lambda j,c:("num" if j==1 else "")))
A(p("<strong>What customers say.</strong> The appeal in reviews is convenience: one login, one report, no new contract, and a credible AI-readiness audit. The limitation reviewers note is depth, fewer engines on the self-serve tiers (Claude, Copilot and DeepSeek require Enterprise AIO), and an AI module that is broader but shallower than a dedicated specialist's."))

A(sec("12","seranking","SE Ranking (SE Visible): the affordable incumbent",
      "Cheap, unlimited AI-source prompt tracking across the majors, sold standalone as SE Visible from $99 or bundled into SE Ranking's SEO plans.",
      "The value pick for agencies and SMBs, especially if you already use SE Ranking."))
A(prof("Affordable AI visibility and prompt tracking with competitor research across Google AI Overviews, AI Mode, ChatGPT and Perplexity.",
       "Agencies and SMBs wanting low-cost AI tracking, and existing SE Ranking customers extending their suite."))
A(table("Table 11. SE Ranking AI pricing (published, September 2026). The bundled add-on's real cost is higher than the base plan suggests.",
        ["Tier","Price / month","What you get"],
        [["SE Visible: Basic","$99","~200 prompts, ~30,000 answers analysed, 4 engines"],
         ["SE Visible: Core","$189","~450 prompts, ~67,500 answers analysed"],
         ["As add-on to SE Ranking","$129-$279 plan + AI add-on","Realistically $150-$240+/mo for meaningful AI coverage"],
         ["Enterprise","Custom",""]],
        cls=lambda j,c:("num" if j==1 else "")))
A(p("<strong>What customers say.</strong> Reviewers like the price-to-coverage ratio, unlimited AI-source tracking and prompt tracking on every plan, and the convenience for existing SE Ranking users. The common note is that the headline entry price is misleading: meaningful AI coverage requires the add-on or SE Visible, which pushes the real monthly cost to $150-$240+, and engine coverage is narrower than the specialists'."))

A(sec("13","rest","Who else is worth knowing about?",
      "Above this set sits Evertune (enterprise, consumer-panel data and shopping intelligence, ~$800-$3,000+/mo, demo-led); below it, a long tail of Frase, Bloomiro, ZipTie and Writesonic compete on a single feature each.",
      "Evaluate these only once you know your priority axis; for most buyers the seven profiled above cover the range."))
A(p("Evertune is the notable omission from the deep profiles because it is demo-led and priced for enterprise (published figures range from $800 to $3,000+ a month), but its consumer-panel methodology, AI Brand Index, model-version tracking and new shopping-intelligence layer make it the serious option above Profound for large brands that want perception data, not just citation counts. The long tail, Frase (content plus visibility), Bloomiro, ZipTie, Writesonic and others, each optimise one axis, price, content grading, or a niche engine, and are worth a look only after the six-axis framework in section 4 tells you which axis you actually care about."))

A(sec("14","gap","What do none of these tools actually do?",
      "They measure. Almost none of them fix. Every profile above ends on the same criticism from customers, monitoring-only, because a tracker tells you that you are absent and which page beat you, but does not diagnose why or generate the fix.",
      "That is the line between AI visibility measurement and AI visibility remediation, and it is where most of the budget quietly leaks."))
A(p("Read the seven reviews together and one phrase repeats: shows what is happening, not how to act on it. That is not a knock on any single vendor, it is the shape of the category. A "+L("clean dashboard number will not tell you why a technically healthy page still gets zero citations","/blogs/clean-site-zero-citations")+", will not write the answer block, clear the retrieval blocker, or build the comparison page that moves the number. Reporting the gap and closing it are two different jobs."))
A(callout("Where measurement ends and remediation begins",
    ["A tracker is a thermometer. It tells you the temperature and whether it is rising. Useful, necessary, and not a cure.",
     "RawMktg sits on the other side of that line. It "+L("audits the page the way an AI crawler sees it","/features/ai-visibility-audit")+", measures "+L("Share of Model","/features/share-of-model")+", and returns located, prioritised findings and the fix, not just a score. Run a tracker to know your position; run diagnosis-and-remediation to change it. Honest buyers budget for both, and read the tracker's number through the accuracy caveats in section 3."]))

A(sec("15","cost","What actually drives the price?",
      "Prompt volume and engine count, not the sticker. A tool's real cost is prompts x runs x engines x cycles, and every serious methodology multiplies all three, which is why '$29' and '$399' converge once you cover the engines and run enough to trust the number.",
      "Match each tool's query allowance to the sampling you actually need before comparing headline tiers."))
A(p("Work it backwards from methodology. A defensible program tracks, say, 100 buyer prompts, five runs each, across five engines, 2,500 queries per cycle before competitors. That instantly rules out entry tiers: Profound Starter (50 prompts, one engine), Otterly Lite (15 prompts), and Semrush Base (25 prompts) are proof-of-problem plans, not measurement programs. Query allowances are the hidden meter, Peec Pro includes ~3,500 monthly queries and the moment your set or run count grows you move up a tier."))
A(code("Formula. Size the plan you actually need before you compare sticker prices.",
      "monthly_queries  =  prompts  x  runs_per_prompt  x  engines  x  cycles_per_month\n\n"
      "  100 prompts  x  5 runs  x  5 engines  x  1 cycle       =   2,500 / month\n"
      "  + 3 competitors tracked on the same prompt set         =  ~10,000 / month\n\n"
      "  Match this to each tool's query/credit allowance, not its headline tier."))

A(sec("16","which","Which AI visibility tool should you buy?",
      "By profile: enterprise breadth, Profound (or Evertune above it); clean mid-market measurement, Peec AI; analytics with guidance, AthenaHQ; monitoring plus agent analytics, Scrunch; agency or budget, Otterly; already on an SEO suite, Semrush or SE Ranking's module.",
      "Buy for the collection method you trust and the engines your buyers use, then confirm the query allowance covers real sampling."))
A(table("Table 12. A starting point by profile. Trial two before committing; collection method and query limits differ more than the marketing suggests.",
        ["If you are...","Start with","Because"],
        [["An enterprise needing breadth and governance","Profound (Evertune for perception data)","Widest coverage, sentiment, MCP automation, the controls large teams require"],
         ["A mid-market B2B team wanting a clean number","Peec AI","Trustworthy self-serve measurement, sentiment bundled, unlimited seats, no-card trial"],
         ["A team wanting analytics plus recommendations","AthenaHQ","Pairs monitoring with Ask Athena guidance, if the credit model fits"],
         ["Also watching how AI agents crawl your site","Scrunch AI","Adds an agent-experience layer most trackers lack"],
         ["An agency or budget-first team","Otterly.ai","$29 entry, 25-factor GEO audit, unlimited workspaces for client work"],
         ["Already paying for Semrush or SE Ranking","That suite's AI module","No extra login; upgrade to a specialist once you know your priority axis"],
         ["Just proving the problem exists","Otterly Lite ($29) or the script below","Enough to confirm you are absent before spending on automation"]]))

A(sec("17","run","How do you actually run one once you have it?",
      "Point it at the questions your buyers really ask, run at least five times per prompt per engine, enable the search tool so you measure real citations, and report Answer Share plus who gets cited instead of you, each tagged with prompt set, engine and date.",
      "The tool automates the loop; the discipline is yours. A number without its prompt set, engine and date is not comparable to anything, including its own value last quarter."))
A(p("Whichever tool you pick, the rules do not change: build the portfolio from real buyer questions across the buying stages, run each several times, and read the cited-domains list as your outreach and competitive map. If you want to understand the machinery before you pay for it, the loop is about a dozen lines of code, and it shows exactly why the search tool must be enabled."))
A(code("Code 1. A minimum-viable tracker. The paid tools automate this across engines and add dashboards; the core logic is this small.",CODE_TRACKER))
A(p("For the full measurement stack, prompt design through GA4 attribution and Looker reporting, see "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+", and for the standard the numbers should meet, the "+L("RawMktg methodology","/methodology")+"."))

A(sec("18","method","Method and honest limits",
      "This is an independent buyer's guide built from published vendor pricing and public customer reviews gathered in September 2026. It is not exhaustive, not affiliated, and the numbers move fast.",
      "Treat prices, query volumes and engine counts as directionally true, not as a live quote."))
A(p("Pricing tiers, query allowances, engine coverage and features in this category change monthly, and several vendors quote enterprise pricing only on request, so confirm current details with each vendor before you buy. Customer sentiment is summarised from public reviews on G2, Capterra and independent write-ups and reflects reviewers' experiences, not ours. RawMktg builds a diagnosis-and-remediation product and is not a neutral party on the measurement-versus-remediation point in section 14; the tool comparison itself is kept even-handed and sourced. Where a call is a judgement (ideal customer, shape), that is our read."))

FAQ=[
 ("What is an AI visibility tool?",
  "An AI visibility tool runs a fixed set of buyer questions against AI answer engines, ChatGPT, Google AI Overviews and AI Mode, Perplexity, Gemini, Copilot and others, on a schedule, and records whether your brand was named, which URLs were cited, and which competitors were recommended instead. It is rank tracking for AI answers, which ordinary SEO tools cannot see because there is no blue-link results page to read."),
 ("Which AI visibility tool is best in 2026?",
  "It depends on your profile. Profound is the deepest for enterprise breadth and governance (G2 4.6, ~11 engines) and Evertune sits above it for consumer-panel perception data. Peec AI is the clean mid-market analytics pick with sentiment bundled. AthenaHQ adds recommendations; Scrunch adds agent analytics. Otterly.ai is the budget and agency choice from $29. If you already pay for Semrush or SE Ranking, start with their bundled module. Trial two before committing."),
 ("How much do AI visibility tools cost in 2026?",
  "Published entry prices span roughly 10x: Otterly $29, Peec ~$92 (€85), Profound $99, Semrush $99 per domain, SE Visible $99, AthenaHQ $295 and Scrunch $300, with enterprise plans (and Evertune) custom-quoted into the thousands. The real cost is driven by query volume, prompts times runs times engines, so a defensible program often needs a mid or upper tier regardless of the headline; match the query or credit allowance to your sampling."),
 ("Are AI visibility numbers accurate?",
  "Only as accurate as the method. Models hallucinate citations, cite domains without naming the brand (ghost citations), and answer the same prompt differently each run, and sentiment scoring is only about 70-85 percent accurate. The most reliable tools use UI scraping rather than API-only collection, verify citations with cross-model overlap, and run each prompt five to ten times. Treat a single confident number with no error bars with suspicion."),
 ("What is the difference between API and UI-scraping data collection?",
  "An API call is cheap and stable but often strips citations and, without the search tool enabled, returns the model's memory rather than a live retrieved answer, so it is an approximation. UI scraping drives a real browser against the actual chat interface and captures what a user sees, including citation chips and sources. It is slower and more expensive but far more accurate. Always ask a vendor which method it uses."),
 ("Which AI visibility tool is best for agencies?",
  "Otterly.ai is the most agency-friendly: a $29 entry point, unlimited workspaces on Standard, a 25-factor per-prompt GEO audit, and a Looker Studio connector, and its G2 reviewers are largely agencies using it for client reporting. SE Ranking is the affordable alternative if you already use the suite. AthenaHQ and Scrunch are strong analytically but their per-brand pricing scales faster than most agency retainers."),
 ("What is the difference between tracking AI visibility and fixing it?",
  "Tracking tells you whether and how often you are cited and which page beat you; fixing diagnoses why your page was not retrievable or answerable and generates the change that would move the number. Almost every tool in this category measures, and customer reviews of all seven repeat the same 'monitoring-only' criticism. Budget for both: a tracker to know your position, and diagnosis-and-remediation to improve it."),
 ("Which engines should an AI visibility tool cover?",
  "At minimum ChatGPT, Google AI Overviews, Google AI Mode, Perplexity, Gemini and Microsoft Copilot, because the major engines disagree on which brands to cite and a single-engine number is misleading. Broader tools add Grok, Claude, Amazon Rufus, Meta AI and DeepSeek. Watch entry tiers: Profound's Starter is ChatGPT only, and several tools gate engines behind add-ons, so match coverage to the engines your buyers actually use."),
 ("How many times should each prompt run?",
  "At least five times per engine, ten is better, because a single run swings the result several points for no real reason. Re-run the same prompt set on a schedule and report the number with its prompt set, engine and date so it is comparable over time. This is also why query and credit allowances, not sticker prices, decide the true cost of a tool."),
]
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
A(faq_html)

REFS=[
 ("Profound Pricing 2026: Plans, Limits and True Cost. Trakkr.","https://trakkr.ai/reviews/profound-review/pricing"),
 ("Profound Reviews 2026 (4.6/5). G2.","https://www.g2.com/products/profound/reviews"),
 ("Peec AI Pricing: Plans, Costs & Extra Fees (2026). Workduo.","https://www.workduo.ai/blog/peec-ai-pricing"),
 ("Peec AI Review & Pricing 2026: Clean Reporting, Nothing More. Ryze.","https://www.get-ryze.ai/blog/peec-ai-review-pricing-2026"),
 ("AthenaHQ Pricing in 2026. Trakkr.","https://trakkr.ai/reviews/athenahq-review/pricing"),
 ("Scrunch AI Review 2026: Pricing, Features & Honest Verdict. CrawlRaven.","https://crawlraven.com/blog/scrunch-ai-review"),
 ("OtterlyAI Pricing 2026. G2.","https://www.g2.com/products/otterlyai/pricing"),
 ("Semrush AI Visibility Toolkit Pricing 2026. Trakkr.","https://trakkr.ai/reviews/semrush-review/pricing"),
 ("SE Visible by SE Ranking Pricing 2026. Trakkr.","https://trakkr.ai/reviews/seranking-review/pricing"),
 ("Evertune Review (2026): Pricing, Features, Pros & Cons. Trakkr.","https://trakkr.ai/reviews/evertune-review"),
 ("API vs UI Data in AI Visibility Tools: Why Your Tracking Data Might Be Wrong. Superlines.","https://www.superlines.io/articles/api-vs-ui-data-ai-visibility-tools"),
 ("AI Visibility Tool Accuracy: How to Evaluate 8 Top Tracking Platforms. Rankdots.","https://rankdots.com/blog/ai-visibility-tool-accuracy"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
A('<div class="about-block" id="references"><div class="about-label">References</div>'
  '<p style="margin-bottom:16px;">Pricing, tiers and coverage are published vendor figures gathered September 2026; customer sentiment is summarised from the public reviews below. Confirm current details with each vendor.</p>'
  f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
A('<div class="about-block"><div class="about-label">About rawmktg.</div>'
  '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
  '<p>Disclosure: RawMktg builds an AI-visibility diagnosis and remediation product and is not affiliated with any tracking tool named here. The comparison is independent and sourced; the measurement-versus-remediation framing reflects our point of view.</p></div>')

body="\n".join(out)

SIDEBAR=[("7","tools profiled in depth"),("$29–$300","published entry prices per month"),("API vs UI","the collection choice that decides accuracy"),("5–10","runs per prompt for a number you can trust")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#what"><span class="toc-num">01</span>What the tools do</a></li>'
     '<li><a href="#collect"><span class="toc-num">02</span>API vs UI scraping</a></li>'
     '<li><a href="#wrong"><span class="toc-num">03</span>What the numbers get wrong</a></li>'
     '<li><a href="#evaluate"><span class="toc-num">04</span>The six evaluation axes</a></li>'
     '<li><a href="#compared"><span class="toc-num">05</span>The seven at a glance</a></li>'
     '<li><a href="#profound"><span class="toc-num">06</span>Profound</a></li>'
     '<li><a href="#peec"><span class="toc-num">07</span>Peec AI</a></li>'
     '<li><a href="#athena"><span class="toc-num">08</span>AthenaHQ</a></li>'
     '<li><a href="#scrunch"><span class="toc-num">09</span>Scrunch AI</a></li>'
     '<li><a href="#otterly"><span class="toc-num">10</span>Otterly.ai</a></li>'
     '<li><a href="#semrush"><span class="toc-num">11</span>Semrush</a></li>'
     '<li><a href="#seranking"><span class="toc-num">12</span>SE Ranking</a></li>'
     '<li><a href="#rest"><span class="toc-num">13</span>Evertune &amp; the rest</a></li>'
     '<li><a href="#gap"><span class="toc-num">14</span>What none of them do</a></li>'
     '<li><a href="#cost"><span class="toc-num">15</span>What drives the price</a></li>'
     '<li><a href="#which"><span class="toc-num">16</span>Which to buy</a></li>'
     '<li><a href="#run"><span class="toc-num">17</span>How to run one</a></li>'
     '<li><a href="#method"><span class="toc-num">18</span>Method &amp; limits</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this guide</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - a 2026 buyer\'s guide - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["AI visibility tools","GEO tools","Profound","Peec AI","AthenaHQ","Scrunch AI","Otterly","Semrush AI toolkit","SE Ranking","Evertune","share of model","answer engine optimization","AI visibility pricing"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="AI Visibility Tools, Compared: 7 Platforms (2026 Buyer's Guide) &middot; rawmktg."
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
  var neutral=rgba(faint,0.4);
  var pc=document.getElementById('priceChart');
  if(pc){new Chart(pc,{type:'bar',data:{labels:['Otterly.ai','Peec AI','Profound','Semrush','SE Ranking','AthenaHQ','Scrunch AI'],datasets:[{data:[29,92,99,99,99,295,300],backgroundColor:[up,rgba(signal,0.55),rgba(signal,0.6),rgba(signal,0.6),rgba(signal,0.6),rgba(signal,0.85),signal],borderRadius:4,barThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' $'+c.raw+'/mo published entry tier';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return '$'+v;}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
  var ec=document.getElementById('engineChart');
  if(ec){new Chart(ec,{type:'bar',data:{labels:['Profound','AthenaHQ','Scrunch AI','Otterly','Semrush','Peec AI','SE Ranking'],datasets:[{data:[11,8,8,7,7,6,4],backgroundColor:[signal,rgba(signal,0.7),rgba(signal,0.7),rgba(signal,0.6),rgba(signal,0.6),rgba(signal,0.5),neutral],borderRadius:4,barThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' up to '+c.raw+' answer engines (top tier/add-ons)';}}}},
      scales:{x:{beginAtZero:true,max:12,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Measurement &middot; Buyer's Guide</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Sep 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/avt_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/avt_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| jsonld_ok:",ok,"| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),
 "| code:",hh.count('class="code-block"'),"| callout:",hh.count('callout-box"'),"| faq:",len(re.findall('faq-item',hh)),"| outlinks:",len(re.findall(r'href="/(blogs|tools|methodology|features)',hh)))
