#!/usr/bin/env python3
"""SCRATCH: build blogs/why-ai-cites-reddit-g2-analysts.html. Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="why-ai-cites-reddit-g2-analysts"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-13"

def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'")
        .replace("“",'"').replace("”",'"').replace("…","...").replace(" "," "))
    t=re.sub(r"\[\d+(?:,\s*\d+)*\]","",t)
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/property-vista-authority-paradox.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'

def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def h3(t): return f"<h3>{esc(t)}</h3>"
def code(label,body,lang=None):
    lng=f'<span class="code-lang">{esc(lang)}</span>' if lang else ''
    return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block">{lng}<pre>{H.escape(body)}</pre></div></div>'
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
def pipeline(nodes,goal,cap):
    parts=['<div class="pipeline">']
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def compare(ll,litems,rl,ritems,cap):
    li="".join(f"<li>{esc(x)}</li>" for x in litems); ri="".join(f"<li>{esc(x)}</li>" for x in ritems)
    return (f'<div class="compare-grid"><div class="compare-col"><div class="compare-col-label seo">{esc(ll)}</div><ul>{li}</ul></div>'
            f'<div class="compare-col"><div class="compare-col-label geo">{esc(rl)}</div><ul>{ri}</ul></div></div><div class="chart-caption">{esc(cap)}</div>')
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def L(t,u,ext=True):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Why AI Cites Reddit, G2 & Analysts Over Your Website"
DECK="The off-site authority stack AI engines actually pull from when buyers ask, and the tactics to seed G2 reviews, Reddit presence, and analyst mentions so they feed LLM answers."
DESC=("AI engines are consensus engines: they cross-reference third-party sources before recommending a product. "
      "Review sites drive up to 85% of B2B AI citations. The off-site authority stack, the data on what gets cited, "
      "and the playbook to seed G2, Reddit and analyst reviews, plus the CITABLE content framework and entity schema.")
DATANOTE=("Authority-seeding playbook for marketing and PR leaders, synthesizing the KDD 2026 GEO benchmark, AI-citation "
          "studies across ChatGPT, Perplexity, Gemini, Copilot and AI Overviews, and platform data-licensing disclosures. "
          "Figures are illustrative models; example code is illustrative.")

out=[]
out.append('<p class="lead">'+norm("Large language models do not trust your marketing copy. They behave as consensus engines: before recommending a product, they cross-reference your claims across neutral, third-party sources. That is why review directories, Reddit threads, and analyst review pages now drive more AI recommendations than your own domain.")+'</p>')
out.append(callout("TL;DR, the bottom line up front",[
 "<strong>AI engines are consensus engines.</strong> They cross-reference claims across neutral third-party sources before recommending. Aggregate review sites alone account for up to 85% of citations on broad B2B category queries.",
 "<strong>Fewer clicks, far higher value.</strong> AI-citation visitors convert at roughly 14.2% versus 2.8% for traditional organic, about 5x.",
 "<strong>The playbook:</strong> seed G2 and the review ecosystem, realign analyst relations toward crawlable review assets, build authentic Reddit presence, apply the CITABLE content framework, then anchor it all with entity schema on your own site.",
]))

# 01
out.append(sec("01","off-site","Why did your website stop being enough?","AI engines trust third-party corroboration, not self-published copy.",
  "For two decades, B2B marketing optimized a direct channel between your domain and the buyer. Then generative engines began answering inside the interface, and the link started to disappear. Zero-click searches have climbed from 45% in 2016 to a projected 68% in 2026, and AI Overviews are associated with a 34-58% CTR decline for the top organic position."))
out.append(p("Here is the twist that reframes the conversation: the traffic that does arrive from a generative engine is dramatically higher intent. Visitors who click an inline citation inside an AI answer convert at roughly 14.2%, about five times the 2.8% that standard organic converts at."))
out.append(chart("rgConv",190,"Figure 1 - fewer clicks, but each one is worth far more: AI-citation traffic converts ~5x higher than standard organic."))
out.append(callout("Why your website stopped being enough",[
 "LLMs do not evaluate authority from self-published, promotional copy. They function as consensus engines, using dense vector search and Retrieval-Augmented Generation to cross-reference your claims across a distributed web of neutral, third-party sources.",
 "If your claims about capability, pricing or category leadership exist only on your own domain, the engine treats them as biased and unverified. To be cited, your brand must be mentioned, validated and corroborated across an off-site authority stack: independent review platforms, structured knowledge bases, community discussions, and analyst reports.",
]))
out.append(chart("rgStack",260,"Figure 2 - the off-site authority stack for the query \"best B2B SaaS tool for ops teams.\" Your website is the smallest signal. Source: Ahrefs Brand Radar, June 2026"))
out.append(p("This is the strategic core of authority seeding: optimizing your own website is necessary but no longer sufficient. The decisive battleground has moved off your domain, and it builds on the same idea as "+L("authority seeding for AI trust","/blogs/authority-seeding-ai-llm-trust",ext=False)+"."))

# 02
out.append(sec("02","how-cite","How do generative engines choose what to cite?","A RAG pipeline retrieves third-party passages and scores them by position and quality.",
  "A generative engine ingests a query and synthesizes an answer through a modular pipeline that pairs a language model with a retrieval system, the same "+L("RAG mechanics","/blogs/how-rag-actually-works",ext=False)+" behind every AI answer."))
out.append(pipeline([("Query reformulation","strip noise, map to search expressions"),("Hybrid search","lexical + vector retrieval"),("Summarize","extract relevant passages"),("Generate","compile an answer with citations")],3,
  "Figure 3 - the real-time RAG pipeline. Off-site platforms feed the retrieval step, which is where citation decisions are made."))
out.append(p("Researchers measure a brand's visibility with two metrics. Position-Adjusted Word Count (PAWC) counts the words attributed to your source, weighted by a positional decay factor, so being mentioned early and substantively is mathematically rewarded. Subjective Impression (a G-Eval score) judges quality across seven dimensions: relevance, logical influence, uniqueness, positional prominence, volume contributed, click likelihood, and information diversity."))
out.append(h3("What the data says actually works"))
out.append(p("The "+L("KDD GEO benchmark","https://arxiv.org/abs/2311.09735")+" tested nine content strategies across a 10,000-query benchmark. The results are a near-perfect inversion of legacy SEO instincts."))
out.append(chart("rgPawc",260,"Figure 4 - lift in Position-Adjusted Word Count vs baseline. Precise, attributable additions win; keyword stuffing is actively penalized."))
out.append(table("GEO content strategies, ranked by citation lift",["Strategy","PAWC lift","Mechanism"],[
 ("Quotation addition","+41%","Attributed quotes from credentialed experts and neutral third parties"),
 ("Statistics addition","+31%","Replacing qualitative claims with precise, named numerical data"),
 ("Fluency optimization","+28%","Cleaner syntax so the model can parse and summarize"),
 ("Cite sources","+28%","Outbound links to authoritative references (.edu, .gov, journals)"),
 ("Technical terms","+18%","Domain-specific terminology aligned to professional queries"),
 ("Authoritative tone","+10%","Framing claims with evidence-backed confidence"),
 ("Keyword stuffing","-8%","Ineffective, triggers active deprioritization by LLMs"),
], cls=lambda j,c: "label" if j==0 else ("up" if (j==1 and not c.startswith("-")) else ("neg" if (j==1 and c.startswith("-")) else ""))))
out.append(callout("Three principles to take away",[
 "<strong>Precision and attributability win.</strong> Specific statistics and named quotes give the model discrete, verifiable units it can lift directly. Vague prose gives it nothing.",
 "<strong>Fluency is a ranking factor.</strong> Improving readability lifted visibility 28% without adding a single new fact.",
 "<strong>Quality lets underdogs leapfrog.</strong> Optimized content gave rank-5 pages a 115% visibility increase, letting smaller brands bypass incumbents' domain-authority advantage.",
]))

# 03
out.append(sec("03","economics","Why are off-site platforms hard-wired into the models?","Training-data licensing deals make Reddit, G2 and publishers paid gatekeepers of truth.",
  "Off-site dominance is not just an algorithmic preference, it is wired into the AI industry's finances. Facing copyright litigation and data depletion, frontier labs are buying legal, high-quality, real-time training data through multi-million-dollar licensing deals."))
out.append(table("AI training-data licensing deals (reported)",["Platform","AI partner","Reported value","Strategic utility"],[
 ("Reddit","Google","$60M / year","Real-time threads, peer sentiment, natural language"),
 ("Reddit","OpenAI","Undisclosed","Live discussions, user product comparisons"),
 ("News Corp","OpenAI","~$50M / yr","High-authority news archives (WSJ, NY Post)"),
 ("Dotdash Meredith","OpenAI","$16M+ / year","Lifestyle, technical, consumer-intent content"),
 ("Axel Springer","OpenAI","$13M / year","European news, business journalism"),
 ("Financial Times","OpenAI","$5-10M / year","Gated macro and corporate intelligence"),
], cls=lambda j,c: "label" if j==0 else ""))
out.append(p("Crucially, these contracts are shifting from flat training fees to usage-based real-time retrieval pricing: platforms get paid when an engine accesses and displays their content to ground a live answer. That turns Reddit, G2 and elite publishers into licensed gatekeepers of factual truth. If your product isn't indexed, discussed and validated inside those partner datasets, you are structurally excluded from the retrieval context."))

# 04
out.append(sec("04","tier1-g2","Tier 1: how do you seed G2 and the review ecosystem?","Treat a review profile as a structured dataset, ecosystem-wide and descriptive.",
  "In an AI-first world, a review profile is not a sales landing page, it is a structured semantic dataset engines crawl, parse and cite. Because aggregate review sites drive up to 85% of citations on broad B2B category queries, optimizing these directories is non-negotiable."))
out.append(p("Adopt an ecosystem approach, not a single profile. Maintaining verified, consistent profiles across G2, Capterra, TrustRadius and Clutch supplies a multi-platform consensus signal that can make a model up to three times more likely to cite you. Acquire reviews compliantly and make them descriptive, full of real use cases, concrete metrics and precise comparisons, the exact material engines lift."))
out.append('<p>'+norm("<strong>Trigger on success milestones</strong> (clean onboarding, a positive QBR, a resolved ticket). <strong>Reduce friction</strong> with direct review links. <strong>Never incentivize</strong>, G2 enforces strict compliance and can suspend profiles. <strong>Integrate into core workflows</strong> like renewal check-ins for a steady, compliant influx.")+'</p>')
out.append(p("Engines use G2's category mappings to retrieve the definitive competitor set for categorical prompts, so accurate mapping is a visibility lever. In March 2026, G2 expanded its taxonomy with AI-era categories including AI Search Visibility Optimization Tools and AI Search & Retrieval Infrastructure."))
out.append(callout("CRM tie-in",["G2 now connects first-party buyer-intent and customer-voice data directly into CRM via partnerships such as HubSpot Breeze Agents, so reps can see which competitors a prospect is researching on G2 inside their own workspace."]))

# 05
out.append(sec("05","tier2-analysts","Tier 2: how should analyst relations change?","Chase open, crawlable review directories, not gated Magic Quadrants.",
  "Analyst relations has long chased prestige placements. But citation-pattern analysis reveals a stark mismatch between classic AR priorities and what engines actually retrieve."))
out.append(p("The Gartner Paradox: an analysis of over a million cited URLs found "+L("Gartner accounts for 81.7% of all analyst-site citations","https://otterly.ai/blog/gartner-ai-citations/")+", despite Gartner blocking major AI crawlers in robots.txt. It is retrieved anyway through the Bing index, third-party citation chains, pre-block historical caches, and Google AI integration. The most important finding is what gets cited: gated flagship reports like the Magic Quadrant account for under 1% of Gartner's AI citations. Fully 96% come from its open Reviews product."))
out.append(chart("rgGartner",260,"Figure 5 - the Gartner Paradox: gated flagship research is almost never cited; open, structured review directories dominate."))
out.append(compare("Flagship reports (Magic Quadrant)",
 ["Gated behind paywalls and logins","Under 1% of analyst citations","Freeform, narrative, editorial","Analyst view on strategy & roadmap"],
 "Public review directories",
 ["Openly crawlable and indexable","96% of analyst citations","Standardized, machine-readable comparisons","Direct \"best tools in category X\" resolution"],
 "Figure 6 - flagship vs open review directories, on the dimensions that decide AI citation."))
out.append(p("Flagship placements still matter for prestige and late-stage enablement, but they are practically ineffective for top-of-funnel AI visibility. Pursue open, un-gated analyst content; keep analyst review profiles fresh like G2; and when you earn an accolade, publish a structured, declarative summary on your own crawlable site so models can extract and verify it."))

# 06
out.append(sec("06","tier3-reddit","Tier 3: how do you seed Reddit authentically?","Build real account authority and structure comments the way engines extract.",
  "Reddit's citation rates make community engagement a core pillar: 46.7% in Perplexity and 21% in Google AI Overviews. But Reddit punishes inauthenticity, automated spam and thinly veiled promotion are removed fast."))
out.append(chart("rgReddit",170,"Figure 7 - Reddit commands an outsized share of citations in B2B AI answers, especially on Perplexity."))
out.append(table("Scoring subreddits for GEO priority",["Subreddit","Domain","Engagement","GEO priority"],[
 ("r/SaaS","B2B software, startups, growth","High (~50/day)","9/10"),
 ("r/sysadmin","IT infra, security, hardware","Very high (~150/day)","8/10"),
 ("r/CRM","Pipeline ops, sales-tech","Low (~5/day)","8/10"),
 ("r/marketing","Demand gen, brand, strategy","High (~40/day)","7/10"),
 ("r/startups","VC, scaling, ops models","High (~30/day)","6/10"),
], cls=lambda j,c: "label" if j==0 else ""))
out.append(p("Build account authority before you mention anything: aged accounts with real posting history, organic karma from genuinely answering questions, expert flairs, and employee subject-matter experts posting from authentic personal accounts, never a corporate handle. Then build comments the way engines extract them."))
out.append(pipeline([("Direct answer","name the pick, up front"),("Credentials","who you are, real context"),("Measurable outcome","hard numbers"),("Honest caveat","a balanced limitation")],0,
  "Figure 8 - the four-part comment architecture engines preferentially cite: answer, credentials, outcome, caveat."))
out.append(callout("Worked example, a citation-ready comment",[
 "\"For growing sales teams managing complex pipelines, HubSpot wins because of its advanced pipeline automation. As an operations director managing a 25-person team, I migrated from Salesforce nine months ago. Within the first quarter, our average close rate improved 18% and manual data entry dropped 30%. The main limitation: advanced custom reporting has a steeper learning curve for non-technical staff.\"",
 "Why it works: direct answer first, credentialed context, hard numbers, and a balanced caveat that signals authenticity, engines preferentially cite balanced, non-promotional perspectives.",
]))

# 07 CITABLE
out.append(sec("07","citable","What does citation-ready content look like? (CITABLE)","Seven parts engineered around how RAG systems extract and verify information.",
  "To produce content engines can retrieve, parse and cite, apply the seven-part CITABLE framework. It is the on-page complement to "+L("anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page",ext=False)+"."))
out.append(callout("The CITABLE framework",[
 "<strong>C</strong> - Clear entity & structure &middot; <strong>I</strong> - Intent architecture &middot; <strong>T</strong> - Third-party validation &middot; <strong>A</strong> - Answer grounding &middot; <strong>B</strong> - Block-structured for RAG &middot; <strong>L</strong> - Latest & consistent &middot; <strong>E</strong> - Entity graph & schema",
]))
out.append(p("<strong>Clear entity & structure.</strong> Open with a Bottom-Line-Up-Front summary under 120 words; format your H1 as a direct question and add a source-linked Key Facts box of three to five stats. <strong>Intent architecture.</strong> Answer five to seven adjacent intents (alternatives, integrations, pricing, limits, benchmarks) under H2/H3 headers, linked hub-and-spoke. <strong>Third-party validation.</strong> Back claims with neutral comparisons and reviews; self-congratulatory copy actively hurts citation rates."))
out.append(p("<strong>Answer grounding.</strong> Begin each answer with a 40-60 word direct response, add inline citations, and close each section with a standalone quotable fact; original statistics can lift LLM visibility 30-40%. <strong>Block-structured for RAG.</strong> Break content into self-contained 200-400 word blocks under descriptive headers; block formatting can cut failed retrievals by up to 49%. <strong>Latest & consistent.</strong> Keep every metric identical across your site, docs, review profiles and press; inconsistency makes models skip you. <strong>Entity graph & schema.</strong> State relationships (\"alternative to X,\" \"integrates with Y\") in copy and mirror them in schema."))

# 08
out.append(sec("08","entity","How do you anchor your entity on-site?","Entity SEO plus JSON-LD sameAs/about/mentions make off-site mentions resolve to you.",
  "Off-site authority is decisive, but your website remains the canonical source of truth for your core entity. If engines can't connect fragmented off-site mentions back to you, they may ignore your brand, or hallucinate a competitor as the source. The sameAs property links your entity to high-authority profiles (LinkedIn, Wikipedia, G2, Crunchbase, Wikidata); about defines a page's subject; mentions maps secondary topics. This is the "+L("structured-data layer","/blogs/schema-markup-ai-citations-2026",ext=False)+" that resolves your entity."))
out.append(code("Organization + WebPage entity anchor (JSON-LD)",
"""{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "EnterpriseFlow",
      "url": "https://www.example.com",
      "sameAs": [
        "https://www.wikidata.org/wiki/Q12345678",
        "https://www.linkedin.com/company/enterpriseflow",
        "https://www.g2.com/products/enterpriseflow",
        "https://crunchbase.com/organization/enterpriseflow"
      ]
    },
    {
      "@type": "WebPage",
      "about": [{ "@type": "Thing", "name": "Workflow Automation" }],
      "mentions": [{ "@type": "Thing", "name": "Cloud Computing" }]
    }
  ]
}""","json"))
out.append(p("Make your content easy to ingest: serve a clean markdown version to AI user-agents, add a root-level "+L("llms.txt","/glossary/llms-txt",ext=False)+" mapping your core pages, and keep robots.txt, canonicals and redirects clean so AI crawlers aren't blocked from key pages."))
out.append(code("llms.txt, root directory example",
"""# EnterpriseFlow
> Cloud-native B2B workflow automation for enterprise operations.

## Core pages
- [Product overview](https://www.example.com/product): capabilities & modules
- [Pricing](https://www.example.com/pricing): plans, limits, enterprise tiers
- [Integrations](https://www.example.com/integrations): Snowflake, Salesforce, HubSpot

## Documentation
- [Docs](https://docs.example.com): setup, API, admin
- [Security & compliance](https://www.example.com/security): SOC 2, GDPR""","markdown"))

# 09
out.append(sec("09","operationalize","How do you operationalize and measure GEO?","AI-first metrics, a manual prompt matrix, and a cross-functional loop.",
  "Without tracking and an execution plan, teams misallocate budget on obsolete tactics. Replace classic metrics with AI-first indicators: Reference Rate (AI share of voice), Citation Frequency, Sentiment Alignment, and AI Referral Traffic via GA4 referral groupings, the kind of "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking",ext=False)+" that closes the loop."))
out.append(p("Build a manual Prompt Matrix before buying tools: freeze 8-12 conversational prompts spanning the buyer journey, then query them monthly across ChatGPT, Perplexity, Claude and Gemini, logging your visibility share, competitor mentions, cited sources and sentiment as a baseline."))
out.append(pipeline([("Customer Success","triggers reviews"),("PR","seeds unlinked mentions"),("Product Marketing","builds citable assets"),("Engineering","schema + llms.txt")],-1,
  "Figure 9 - GEO governance is a loop across Customer Success, PR, Product Marketing and Engineering, not one team's job."))
out.append(table("The 30-day Reddit GEO engagement calendar",["Phase","Subreddit activity","Editorial support","Focus"],[
 ("Days 1-7","Identify targets; audit discussions","Map buyer intents; add BLUF","Community mapping"),
 ("Days 8-14","3-5 non-promotional threads for karma","JSON-LD sameAs on core pages","Credibility & tech"),
 ("Days 15-21","Contextual, balanced brand mentions","Use-case guides & comparison tables","Authority seeding"),
 ("Days 22-30","Address sentiment; launch an AMA","First Prompt Matrix audit","Measurement"),
], cls=lambda j,c: "label" if j==0 else ""))
out.append(callout("The 60-minute GEO reset",[
 "<strong>1. Run the Verdict Test (10 min).</strong> Query your brand + category on ChatGPT and Perplexity. Note which competitors and sources are cited, and where you're missing.",
 "<strong>2. Optimize a key page (30 min).</strong> Replace three vague claims with quantified, source-linked stats, add one comparison table, and write a 2-3 sentence BLUF under 120 words.",
 "<strong>3. Anchor your entity (20 min).</strong> Implement or verify homepage JSON-LD and add sameAs links to your verified G2 and LinkedIn profiles.",
]))

# 10
out.append(sec("10","exec","What should executives do?","Reallocate budget to seeding, stand up governance, and commit to answer grounding.",
  "Managing discoverability as search shifts from rankings to recommendations means adapting budgets, roles and content together."))
out.append(p("<strong>Reallocate budget to seeding platforms.</strong> Trim keyword-focused SEO and some performance spend; fund G2 review campaigns, Reddit community seeding, and partnerships with open, crawlable analyst firms. <strong>Stand up GEO governance.</strong> Align PR, product marketing, customer success and engineering. <strong>Commit to answer grounding.</strong> Move from superficial posts to data-rich resources, original research, specific customer metrics, expert case studies, so engines can extract, verify and cite you."))
out.append(pull("In the post-search era, you don't win the recommendation by talking about yourself on your own website. You win it by being independently corroborated everywhere else, in a format machines can lift. Seed the consensus, then anchor it."))

FAQ=[
 ("Is traditional SEO dead?","No, but its role narrowed. Classic SEO still gets you crawled and indexed, which underpins the Bing and Google pipelines engines rely on. What changed is that on-page keyword optimization no longer determines whether you're recommended. Authority now comes from third-party corroboration and citation-ready structure, not keyword density, which is actively penalized."),
 ("If AI sends far fewer clicks, why invest at all?","Because the few clicks convert about 5x higher (14.2% vs 2.8%), and most of the influence happens with no click at all, the AI's recommendation shapes the buyer's shortlist before they ever reach your site. You're optimizing for being named in the answer, not just for referral traffic."),
 ("We're a small brand. Can we realistically out-cite incumbents?","Yes, this is the most encouraging finding. Optimized content gave rank-5 pages a 115% visibility increase, because engines reward precision and machine-readability over raw domain authority. Disciplined seeding and CITABLE content let smaller players leapfrog incumbents who still rely on legacy SEO."),
 ("Isn't seeding Reddit and reviews just astroturfing?","It becomes astroturfing when it's inauthentic, incentivized or hidden, and engines and moderators punish that. The compliant approach uses real employee experts, aged authentic accounts, honest balanced comments with caveats, and reviews earned at genuine success milestones with no incentives. Authenticity is the strategy."),
 ("Should we abandon Gartner Magic Quadrant placements?","No. They retain prestige and late-stage sales-enablement value. But for top-of-funnel AI visibility they're nearly invisible (under 1% of citations), so don't let them absorb the AR budget. Shift weight toward open analyst content and crawlable review directories, which drive 96% of analyst citations."),
 ("How do we even measure this?","Start manual and free: freeze 8-12 buyer-journey prompts and query them monthly across ChatGPT, Perplexity, Claude and Gemini, logging Reference Rate, Citation Frequency, sentiment and cited sources. Add GA4 AI-referral tracking. Only graduate to paid AI-visibility platforms once you have a baseline."),
 ("What's the single fastest thing we can do this week?","The 60-minute reset: run the Verdict Test on your brand, quantify and source-link three claims on your top page plus add a comparison table and BLUF, then anchor your homepage with JSON-LD sameAs links to G2 and LinkedIn. It touches content, structure and entity in an hour."),
 ("How long until authority seeding shows results?","Treat it as a quarterly program, not a campaign. The 30-day calendar builds the foundation, but compounding citation gains come from sustained consistency: fresh reviews, ongoing community presence, and updated facts across every surface engines cross-reference."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')

SOURCES=[
 ("GEO: Generative Engine Optimization, KDD benchmark (arXiv)","https://arxiv.org/abs/2311.09735"),
 ("How Gartner dominates 81.7% of analyst citations while blocking AI crawlers (Otterly.ai)","https://otterly.ai/blog/gartner-ai-citations/"),
 ("Mastering AI Citations: the GEO playbook (Frase)","https://www.frase.io/"),
 ("LLM SEO: the B2B guide to getting cited (Virayo)","https://virayo.com/blog/generative-engine-optimization-strategies"),
 ("Third-party validation and authority signals (Discovered Labs)","https://www.discoveredlabs.com/"),
 ("The price of AI training data, $5M to $250M (Quartz)","https://qz.com/"),
 ("The new SEO is GEO: optimize your Reddit presence (Single Grain)","https://www.singlegrain.com/"),
 ("9 marketing trends in 2026, with data (Ahrefs)","https://ahrefs.com/blog/"),
]
src_items="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in SOURCES)
out.append(f'<div class="sources-block"><div class="sources-label">Sources & further reading</div><ul class="sources-list">{src_items}</ul></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div><p>rawmktg. publishes data-driven teardowns of how AI search decides what to recommend. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("85%","Review-site share of B2B AI citations"),("5x","AI-citation conversion lift vs organic"),("3","Off-site authority tiers to seed")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#off-site"><span class="toc-num">01</span>The off-site stack</a></li>'
     '<li><a href="#how-cite"><span class="toc-num">02</span>How engines cite</a></li>'
     '<li><a href="#economics"><span class="toc-num">03</span>The new economics</a></li>'
     '<li><a href="#tier1-g2"><span class="toc-num">04</span>Tier 1: G2 & reviews</a></li>'
     '<li><a href="#tier2-analysts"><span class="toc-num">05</span>Tier 2: analysts</a></li>'
     '<li><a href="#tier3-reddit"><span class="toc-num">06</span>Tier 3: Reddit</a></li>'
     '<li><a href="#citable"><span class="toc-num">07</span>The CITABLE framework</a></li>'
     '<li><a href="#entity"><span class="toc-num">08</span>Anchor your entity</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this guide</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'

def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),
 "image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,
 "publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},
 "keywords":["authority seeding","off-site SEO","G2 reviews","Reddit GEO","analyst relations","AI citations","GEO","consensus engine","CITABLE","entity SEO","schema","share of model"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Why AI Cites Reddit, G2 &amp; Analysts Over Your Website &middot; rawmktg."
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
 f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en-IN" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n  <meta property=\"og:image:width\" content=\"2400\" />\n  <meta property=\"og:image:height\" content=\"1260\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{H.escape(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  {jb(blog)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/blogs/{SLUG}.md\" />\n  "+FONTS+"\n  ")

CHARTS="""
<!-- Chart.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
(function(){
  if(typeof Chart==='undefined') return;
  var css=getComputedStyle(document.documentElement);
  var signal=(css.getPropertyValue('--signal')||'#D04A2A').trim();
  var faint =(css.getPropertyValue('--faint')||'#C5BFB4').trim();
  var up=(css.getPropertyValue('--up')||'#3E9B6A').trim();
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.45);
  function hbar(id,labels,data,colors,suffix,max){var e=document.getElementById(id);if(!e)return;
    new Chart(e,{type:'bar',data:{labels:labels,datasets:[{data:data,backgroundColor:colors,borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+(suffix||'');}}}},
      scales:{x:{beginAtZero:true,max:max,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  hbar('rgConv',['AI-citation traffic','Standard organic'],[14.2,2.8],[up,neutral],'% conversion',16);
  hbar('rgStack',['Review sites (G2)','Reddit threads','Analyst reviews','PR / earned media','Your website'],[85,47,41,28,12],[up,up,neutral,neutral,signal],' citations',100);
  hbar('rgPawc',['Quotation addition','Statistics addition','Fluency','Cite sources','Technical terms','Authoritative tone','Keyword stuffing'],[41,31,28,28,18,10,-8],[up,up,up,up,up,up,signal],'% PAWC lift',45);
  hbar('rgReddit',['Perplexity','Google AI Overviews'],[46.7,21],[signal,neutral],'% of citations from Reddit',60);

  var g=document.getElementById('rgGartner');
  if(g){new Chart(g,{type:'doughnut',data:{labels:['Open review directories','Gated flagship reports','Other Gartner pages'],
    datasets:[{data:[96,1,3],backgroundColor:[up,signal,neutral],borderColor:'#1A1815',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:10},boxWidth:10,boxHeight:10,padding:12}},
      tooltip:{callbacks:{label:function(c){return ' '+c.label+': '+c.raw+'%';}}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Authority Seeding &middot; Off-Site GEO</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">June 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)
hh=open(f"blogs/{SLUG}.html").read()
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| pipelines:",hh.count('class="pipeline"'),"| compare:",hh.count('class="compare-grid"'),
 "| code:",hh.count("code-block")-1,"| callout:",hh.count('class="callout-box"'),"| listitem:",hh.count('role="listitem"'),"| hreflang:",hh.count("hreflang"))
