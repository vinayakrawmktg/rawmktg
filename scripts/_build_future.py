#!/usr/bin/env python3
"""SCRATCH: build blogs/why-traditional-seo-is-no-longer-enough.html (How AI Search Works). Do NOT commit."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="why-traditional-seo-is-no-longer-enough"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-07-01"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
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
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div><table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def compare(label_a,items_a,label_b,items_b):
    la="".join(f"<li>{esc(x)}</li>" for x in items_a); lb="".join(f"<li>{esc(x)}</li>" for x in items_b)
    return (f'<div class="compare-grid"><div class="compare-col"><div class="compare-col-label seo">{esc(label_a)}</div><ul>{la}</ul></div>'
            f'<div class="compare-col"><div class="compare-col-label geo">{esc(label_b)}</div><ul>{lb}</ul></div></div>')
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
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Why Traditional SEO Is No Longer Enough"
DECK="The shift from blue links to AI answers, and what it does to your B2B pipeline. AI tools now shape the shortlist before a buyer ever contacts sales."
DESC=("AI search is rewriting B2B discovery: 80% of deals go to the vendor already favored before sales contact, and chatbots now "
      "shape the shortlist more than websites or peers. Why traditional SEO is no longer enough, how RAG picks its sources, what the "
      "Princeton GEO study proves works, the citation flywheel, how to measure it, and a 90-day roadmap.")
DATANOTE=("A strategy briefing on the shift from SEO to Generative Engine Optimization, built from published research and benchmarks: "
          "the Princeton/Georgia Tech GEO study (10,000 queries), 6sense and Gartner buyer surveys, Conductor's 100M-citation benchmark, "
          "and documented B2B SaaS case studies, 2025-26. Figures are drawn from those sources and cited at the foot of this article.")

REFS=[
 ("Princeton, Georgia Tech, Allen Institute, IIT Delhi, GEO: Generative Engine Optimization (ACM SIGKDD 2024)","https://collaborate.princeton.edu/en/publications/geo-generative-engine-optimization/"),
 ("6sense / Omnibound, B2B Buying Statistics 2026","https://www.omnibound.ai/blog/b2b-buying-statistics"),
 ("Gartner, 67% of B2B buyers prefer a rep-free experience","https://www.gartner.com/en/newsroom/press-releases/2026-03-09-gartner-sales-survey-finds-67-percent-of-b2b-buyers-prefer-a-rep-free-experience"),
 ("Gartner, 69% of buyers turn to sales reps to validate AI-generated insights","https://www.gartner.com/en/newsroom/press-releases/2026-05-20-gartner-survey-finds-sixty-nine-percent-of-b-two-b-buyers-turn-to-sales-reps-to-validate-ai-generated-insights"),
 ("Frase, The complete GEO playbook (Conductor 100M-citation benchmark)","https://www.frase.io/blog/how-to-get-cited-by-ai-search-engines-the-complete-geo-playbook"),
 ("Pixis, ChatGPT vs Perplexity vs Gemini: platform-specific GEO","https://pixis.ai/blog/chatgpt-vs-perplexity-vs-gemini-how-each-ai-engine-cites-differently-and-how-to-optimize-for-each/"),
 ("cheers.tech, AI search engine source differences","https://www.cheers.tech/geo-academy/ai-search-engine-source-differences"),
 ("Quattr, GEO metrics: measuring visibility in AI search","https://www.quattr.com/blog/generative-engine-optimization-metrics"),
 ("Discovered Labs, GEO metrics: what KPIs matter (2026)","https://discoveredlabs.com/blog/geo-metrics-what-kpis-matter-how-to-track-them-2026"),
 ("Elementera, What the Princeton GEO paper shows your business","https://www.elementera.com/blog/generative-engine-optimization-what-geo-aeo-ai-search-paper-shows-your-business"),
 ("HubSpot, Answer Engine Optimization case studies (2026)","https://blog.hubspot.com/marketing/answer-engine-optimization-case-studies"),
 ("Optimist, Real-world AEO & GEO case studies for B2B","https://www.yesoptimist.com/aeo-geo-case-studies/"),
 ("AI Thinker Lab, GEO 2026: Princeton-backed","https://aithinkerlab.com/generative-engine-optimization-2026/"),
]

out=[]
out.append('<p class="lead">'+norm("For almost thirty years, search worked the same way. You typed a question, Google handed you a list of blue links, and then you did the real work: clicking around, reading a few pages, and piecing the answer together yourself. That model is breaking down. Today's AI tools do not just point you to pages, they read the pages for you and write one clear answer. Buyers do not want a trip to ten websites anymore. They want the answer, right now.")+'</p>')
out.append(compare("Old way, retrieval",
  ["The engine finds pages and ranks them","You open them, read them, compare","You build the answer yourself","A page ranked sixth still gets seen"],
  "New way, synthesis",
  ["The engine reads many pages in real time","It writes a single answer","A few sources are cited inside it","A source not named is invisible"]))
out.append(p("This is not a small design change, it is a traffic problem. When an AI answer sits on top of the page, fewer people scroll down to click. On average, click rates fall about 28%. For B2B SaaS, it gets worse fast: some see organic traffic drop up to 40% within 90 days of AI features going live on their main commercial keywords. And your rankings can look fine while your leads dry up, if the AI answers the question without a click, that top ranking does not turn into a single lead."))
out.append(statgrid([("28%","Average CTR drop when an AI answer sits above the links"),("40%","Organic traffic decline some SaaS firms see within 90 days"),("25-39%","Of AI citations come from pages outside the top organic ranks")]))
out.append(p("That last number matters most. A 2026 Conductor benchmark of 13,770 websites and 100 million citations found 25% to 39% of AI citations come from pages not ranked in the top organic results. AI picks its sources by different rules than Google's old ranking system, so winning the old game does not mean you win the new one. That is why marketers are learning "+L("Generative Engine Optimization","/blogs/geo-foundation-audit")+" (GEO): making sure your brand gets cited, mentioned and recommended across ChatGPT, Perplexity, Gemini and Claude, where B2B deals are now won or lost."))
out.append(callout("How to read this briefing",[
 "This is the map, not the manual. It covers the whole shift end to end, the business case, the mechanism, the proof and the plan, at a level a leadership team can act on. Where a topic has its own playbook, each section hands off to that deeper article. Start here, then follow the links that matter to your team.",
]))

# 01
out.append(sec("01","buyers","How do B2B buyers actually buy now?","In quiet, self-guided research, and the shortlist is increasingly formed inside a chat window.",
  "Buying has moved almost fully into self-guided research. The 6sense 2025 report found 80% of B2B deals are won by the vendor the buyer already liked before ever contacting sales; 92% start with a specific vendor in mind, and 95% of winning vendors were on the buyer's Day One shortlist. If you are not on that first list, you are mostly playing to lose."))
out.append(chart("fsShortlist",240,"Figure 1 - what shapes the B2B vendor shortlist, relative influence across a 500-buyer scan. AI chatbots now outrank vendor websites and peer referrals. Source: G2 / 6sense 2025"))
out.append(p("AI chatbots are now the single most influential source shaping vendor shortlists, named by 17.1% of buyers, ahead of vendor websites (12.8%) and peer recommendations (8.9%). For software buyers, 51% now start their research in a chatbot instead of Google. The habit speeds things up (sales cycles shrank from 11.3 to 10.1 months) but the buying group is bigger: a typical enterprise deal now involves 13 people inside the company and 9 outside. Millennials and Gen Z make up 71% of business buyers, and 44% of them prefer to buy with no sales rep at all."))
out.append(callout("The catch",[
 "Self-service rules the early stage, but people still want a human before they sign. Gartner found 67% of buyers prefer a rep-free experience, yet 69% still ask a sales rep to check what the AI told them. Why? Trust: about half of buyers say they have hit misleading claims from AI, and about half say the same about sales reps. Buyers now use both, and cross-check each one.",
]))
out.append(p("The lesson is simple. If AI shapes the shortlist, and the shortlist decides the deal, then getting recommended by AI is not a nice-to-have, it is a pipeline input."))

# 02
out.append(sec("02","how","How does AI search really work?","Most engines use Retrieval-Augmented Generation: they fetch live pages first, then write a grounded answer.",
  "AI engines do not answer from memory alone. Most use "+L("Retrieval-Augmented Generation","/blogs/how-rag-actually-works")+" (RAG): the engine fetches live pages, then writes an answer grounded in what it found. Four steps tell you exactly where to plant your content."))
out.append(pipeline([("Query fan-out","split into 4-8 sub-searches"),("Retrieval","pull relevant passages, not pages"),("Synthesis","blend into one answer"),("Citation","credit checkable facts only")],3,
  "The RAG pipeline. Your job in GEO is to be the passage that survives step 4: a clear, fact-dense block that is easy to lift and hard to argue with."))
out.append(p("Retrieval pulls specific text blocks, not whole pages, and each engine reaches into a different index. That is the executive summary; the full pipeline, chunking, vector retrieval, re-ranking, and the GraphRAG upgrade that beat standard RAG 96% of the time, is decoded in "+L("How RAG Actually Works","/blogs/how-rag-actually-works")+". The one takeaway for now: clear structure and clear links between your facts help the engine trust and use them."))

# 03
out.append(sec("03","platforms","Why does each AI cite sources differently?","Because each engine weights authority, freshness and format differently, so a one-size plan fails.",
  "A Yext study found 86% of AI citations come from brand-controlled sources like your own site, directory listings and review profiles, you have more control than you think. But the details differ by platform, the reason "+L("engines recommend different vendors","/blogs/why-engines-recommend-different-vendors")+" for the same query."))
out.append(table("How the major engines pick sources",["Platform","How it picks","What it rewards","What it means for you"],[
 ("ChatGPT Search","Queries Bing, pulls 8-12 pages, cites 3-6","Domain authority; 87% of citations match Bing's top 10","Build real authority; sites over 32K referring domains are 3.5x more likely to be cited"),
 ("Perplexity","Live search each time, pulls 10-20, cites 2-4","Niche, specialist sites; 24% of citations are vertical","Deep expert content can win without a huge domain, and it passes real referral traffic"),
 ("Google AI Overviews","Google's index, powered by Gemini","Structured, multi-format; YouTube most-cited outside source","Only 4.5% of cited URLs match page-one results, so deeper pages matter"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Treat the table as the summary; the per-engine deep dive, with a 60-day multi-engine rollout, lives in "+L("Why Engines Recommend Different Vendors","/blogs/why-engines-recommend-different-vendors")+", and Google's two surfaces get their own breakdown in "+L("AI Mode vs AI Overviews","/blogs/ai-mode-vs-ai-overviews")+". One quiet but critical point first: AI crawlers can only cite what they can reach. An old or strict "+L("robots.txt","/blogs/how-ai-crawlers-index-your-site")+" can block bots like OAI-SearchBot or PerplexityBot without you knowing. If they cannot crawl you, you are out before the game starts."))

# 04
out.append(sec("04","research","What does the research say actually works?","Statistics, expert quotes and clear writing lift AI visibility; keyword stuffing backfires by ~8%.",
  "GEO is not guesswork. A study presented at ACM SIGKDD 2024 (Princeton, Georgia Tech, the Allen Institute, IIT Delhi) built a 10,000-query test set and tried nine content changes. The results are clear and a little surprising."))
out.append(table("Princeton GEO study, change vs AI visibility",["Content change","Effect on AI visibility"],[
 ("Add real statistics and data","Strong lift"),
 ("Add expert quotations","Strong lift"),
 ("Write in clear, fluent language","Lift"),
 ("Keyword stuffing","Down about 8%"),
], cls=lambda j,c:("up" if j==1 and "lift" in c.lower() else ("neg" if j==1 else "label" if j==0 else ""))))
out.append(p("Old-school keyword stuffing does not just fail, it backfires: AI reads for meaning, so repeated keywords look like low quality and the model picks a cleaner source. What works is the opposite, expert quotes, exact numbers, and clear, simple writing. The full nine-tactic study and the page-level patterns that win are pulled apart in "+L("Anatomy of a High-Citation Page","/blogs/anatomy-of-a-high-citation-page")+"; the three moves that matter most are below."))
out.append(h3("Lead with the answer"))
out.append(p("Put a direct "+L("40 to 60 word answer","/tools/answer-block-optimizer")+" in the first third of the page or section, engines grab these opening blocks. Pages with these answer capsules get cited 40% more often than ones that open with a slow, vague intro. Turn your H2 and H3 headings into real questions, worded the way buyers ask them, the "+L("anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page")+"."))
out.append(callout("Case in point, 280% more citations",[
 "An enterprise security page ranked well on Google but got zero AI citations, it opened with a long history of security systems. The team rewrote the intro to lead with a dense fact (which three protocols matter, and the exact share each holds). That one change drove a 280% jump in AI citations in 60 days.",
]))
out.append(h3("Rebuild your proof"))
out.append(p("Old case studies lean on feelings and story; AI cannot use that. To be citable, a case study needs a simple proof formula: a clear claim, a specific number, and the context to repeat it. Also write public pages that answer late-stage worries head on, like switching costs and setup risk. Buying groups look these up when a deal stalls, and AI cites them."))
out.append(h3("Fix your name confusion"))
out.append(p("Say your homepage calls you a \"workflow platform,\" your G2 page says \"project management tool,\" and your LinkedIn says \"team collaboration solution.\" To an AI that looks like three fuzzy identities, so its confidence drops and it picks a rival with one clear, matching label everywhere. Use the same category words across your site, review profiles and press, and back them with consistent "+L("entity schema","/blogs/schema-markup-ai-citations-2026")+"."))

# 05
out.append(sec("05","flywheel","What is the citation flywheel?","Off-site trust that compounds: AI cites your data, writers link it, authority rises, you get cited again.",
  "You cannot win GEO on your own site alone, AI checks your claims against the wider web, and that trust is concentrated: the top 20% of cited domains capture 80% of all AI references. G2 is the most-cited software review site across ChatGPT, Perplexity and Google, so your "+L("review density there","/blogs/why-ai-cites-reddit-g2-analysts")+" is a direct input."))
out.append(pipeline([("AI cites your data","original, fact-dense"),("Writers find & link it","research via AI"),("Authority rises","earned coverage"),("Cited again","a little stronger")],-1,
  "The citation flywheel: as AI cites your original data, human writers find it and link it, those links lift your authority, which raises your odds of being cited next time. The loop tightens, the same "+L("compounding effect","/blogs/geo-compounding-flywheel")+" across the whole GEO stack."))
out.append(p("This is not theory. In one documented case, a SaaS team published 66 targeted AEO articles in month one, then seeded genuinely helpful answers on high-intent "+L("Reddit threads","/blogs/reddit-geo-playbook")+" that already ranked on Google, driving a 600% jump in citations and a six-fold rise in trials. "+L("The GEO Compounding Flywheel","/blogs/geo-compounding-flywheel")+" models the full loop, the Share-of-Citation math, and why it gets harder to dislodge over time."))

# 06
out.append(sec("06","measure","How do you measure GEO?","With citation metrics, not pageviews. Citation Rate, share of voice, and AI referral traffic.",
  "You cannot manage what you cannot see, and pageviews will not show you this. A solid GEO scorecard tracks a handful of new metrics, the same "+L("prompt-to-citation discipline","/blogs/prompt-to-citation-tracking")+" applied on a fixed cadence."))
out.append(table("The GEO scorecard",["Metric","What it tells you"],[
 ("AI Visibility Score","How often your brand shows up across a set of industry prompts"),
 ("Share of Voice","How often you are cited versus your top 3-5 rivals"),
 ("Citation Rate","How often the engine links to your page, not just names you"),
 ("Prompt-Level Performance","How you do on specific money prompts like \"best CRM for startups\""),
 ("Citation Quality","Whether you appear up top or buried at the end"),
 ("Sentiment","Whether AI calls you a \"market leader\" or a \"budget option\""),
 ("AI Referral Traffic","Real clicks from perplexity.ai, chatgpt.com and Google AI Mode in GA4"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("As a benchmark: Ahrefs found about 26% of brands have zero citations in Google AI Overviews. Most SaaS firms start at an 8% to 15% citation rate; good on-page and schema work pushes that to 20% to 30%; category leaders reach 40% to 50% or more. This is the scorecard in brief, "+L("Prompt-to-Citation Tracking","/blogs/prompt-to-citation-tracking")+" builds the full measurement stack: prompt portfolios, GA4 AI attribution, and revenue per citation as the ROI metric."))

# 07
out.append(sec("07","results","What results are real companies seeing?","Documented B2B wins from structure, proof and fixing name confusion, not from writing more posts.",
  "The proof is in the pipeline. These are documented B2B SaaS outcomes from 2025 and 2026. The pattern: wins come from structure, clear proof, and fixing name confusion."))
out.append(table("Documented B2B SaaS GEO results",["Company","What they did","Result"],[
 ("B2B tech (Optimist)","Clean Q&A + schema to fix name confusion","49x more AI-referred revenue, 26x more AI referral traffic in 14 months"),
 ("Financing platform (Concurate)","Real author names, expert bios, valid FAQ schema","+315% Google AI Overview citations, 100% lift in AI referrals in 4 months"),
 ("Series C HR tech","Released anonymized platform data as fact-dense assets","Brand mentions rose 12 to 48/month, displacing two rivals in 90 days"),
 ("Mature SaaS (Discovered)","Fixed schema, 66 targeted articles, seeded Reddit","AI-referred trials grew 575 to 3,500+/month in seven weeks"),
 ("SaaS platform (GreenBanana)","Rebuilt pricing/feature pages for conversational prompts","$4.8M new AUM in 120 days, a 415% return"),
 ("CloudEagle (Quattr)","Optimized 33 product pages, AI-native SEO + internal linking","3x AI citation share, 77% of new traffic bottom-funnel"),
], cls=lambda j,c:"label" if j==0 else ("up" if j==2 else "")))
out.append(p("The gap between winners and laggards is already wide. In one review of legal software, Clio scored 89 out of 100 for AI visibility while a rival scored 2. That gap decides who lands on the shortlist. The buyers never see the score, they just see who the AI recommends."))

# 08
out.append(sec("08","roadmap","What's the 90-day roadmap?","Three tracks at once: technical foundations, citation-first content, then off-site authority.",
  "Google's own guidance is that winning at AI search does not need a whole new playbook, it needs solid SEO basics (valuable content, verified schema, clean structure) aimed at how AI reads. Run three tracks at once."))
out.append(table("The 90-day GEO roadmap",["Track","Window","The work"],[
 ("Technical","Days 1-30","Audit robots.txt so no rule blocks AI bots; deploy valid JSON-LD on product, solutions and pricing pages; set up GA4 filters for AI referral sessions."),
 ("Content","Days 31-60","Add a 40-60 word answer capsule atop key pages; turn headings into buyer questions; rebuild case studies into claim + metric + context; publish honest objection pages."),
 ("Authority","Days 61-90","Align category words across your site, G2, LinkedIn and press; build partner citation networks; earn genuine mentions on Reddit and Quora."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(callout("Where to start",[
 "Two free tools cover the first two tracks: the "+L("GEO Readiness Scorecard","/tools/geo-readiness-scorecard")+" flags the technical and content gaps capping your citations, and the "+L("Off-Site Authority Stack Scorecard","/tools/off-site-authority-scorecard")+" scores the authority track, review sites, analysts, community and entity schema.",
]))

# 09
out.append(sec("09","window","Why is the window closing?","AI engines are locking in a trusted-source list per category now, and entrenched sources keep getting cited.",
  "AI engines are building their trusted-source lists for each software category right now. Once an engine locks in a brand as the go-to source, it keeps citing that brand, the entrenchment effect, and it creates a loop that is hard to break into later."))
out.append(p("The real risk: leaders who do not build their brand's authority and citation footprint in the next 6 to 12 months may find their product quietly left out of the AI answers that now guide the B2B buying journey. Not ranked lower. Left out. Traditional SEO is not dead, it is the foundation, but on its own it is no longer enough. The brands that win from here pair clean technical SEO with citation-first GEO content and tight, honest conversion pages. Do that, and you land on the Day One shortlist at the exact moment the buyer decides."))
out.append(pull("The goal is simple to say and hard to fake: become the answer, not just the ad."))
out.append(callout("The five-minute version",[
 "AI now writes the answer instead of listing links, and click-through can fall up to 40% on core terms. 80% of B2B deals go to the vendor already favored before sales contact, and chatbots shape that shortlist more than websites or peers.",
 "AI picks sources by clarity and proof, not keyword rank, keyword stuffing actually hurts you by about 8%. Lead with a 40-60 word answer, rebuild proof into claim + metric + context, and use one category label everywhere.",
 "Track citation rate, not pageviews. Move in the next 6 to 12 months, before the trusted-source list locks in.",
]))

FAQ=[
 ("What is GEO (Generative Engine Optimization)?","GEO is the practice of getting your brand cited, mentioned and recommended inside AI-generated answers across ChatGPT, Perplexity, Gemini, Google AI Overviews and Claude. Where traditional SEO optimizes to rank a page in a list of links, GEO optimizes to become the source an AI engine lifts and credits when it synthesizes an answer. It combines technical hygiene (crawlability, schema), citation-first content (answer capsules, statistics, expert quotes), and off-site authority (reviews, mentions, partner citations)."),
 ("Is traditional SEO dead?","No. Traditional SEO is the foundation GEO builds on, Google itself says you win AI search with solid SEO basics: valuable content, verified schema, and clean site structure. But on its own SEO is no longer enough, because a top ranking no longer guarantees a click or a citation. Between 25% and 39% of AI citations come from pages that are not ranked in the top organic results, so you have to optimize for how AI reads and cites, not just how Google ranks."),
 ("Why is my organic traffic dropping even though my rankings are stable?","Because AI answers are intercepting the click. When a generative answer sits above the links, click-through falls about 28% on average, and some B2B SaaS firms see organic traffic drop up to 40% within 90 days of AI features going live on their main commercial keywords. Your page can still rank at the top of Search Console while the AI answers the question without sending anyone to your site, so rank and session counts no longer tell you the truth."),
 ("How do you get cited by AI search engines?","Lead with a direct 40-60 word answer in the first third of each page or section (these get cited ~40% more often), add real statistics and expert quotes (the Princeton study found these give the strongest lift, while keyword stuffing cuts visibility ~8%), phrase headings as buyer questions, deploy valid schema, make sure your robots.txt admits AI crawlers, and use one consistent category label across your site, G2 and press. Then build off-site corroboration through reviews and genuine community mentions."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
refli="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in REFS)
out.append(f'<div class="about-block"><div class="about-label">Sources &amp; further reading</div><ol style="margin:0;padding-left:18px;font-family:var(--f-mono);font-size:11.5px;line-height:1.7;color:var(--mute)">{refli}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven playbooks and teardowns on how AI search decides what to recommend, pulling citation and SEO data to show exactly where the visibility gaps are. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("80%","Of B2B deals won by the favored vendor before sales contact"),("51%","Of software buyers now start research in a chatbot"),("40%","Organic traffic drop some SaaS firms see in 90 days")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#buyers"><span class="toc-num">01</span>The new buyer</a></li>'
     '<li><a href="#how"><span class="toc-num">02</span>How AI search works</a></li>'
     '<li><a href="#platforms"><span class="toc-num">03</span>Each AI cites differently</a></li>'
     '<li><a href="#research"><span class="toc-num">04</span>What research proves</a></li>'
     '<li><a href="#flywheel"><span class="toc-num">05</span>The citation flywheel</a></li>'
     '<li><a href="#measure"><span class="toc-num">06</span>How to measure GEO</a></li>'
     '<li><a href="#results"><span class="toc-num">07</span>Real results</a></li>'
     '<li><a href="#roadmap"><span class="toc-num">08</span>The 90-day roadmap</a></li>'
     '<li><a href="#window"><span class="toc-num">09</span>The window is closing</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this briefing</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["GEO","generative engine optimization","AEO","SEO","AI search","B2B SaaS","AI citations","RAG","Princeton GEO study","shortlist"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Why Traditional SEO Is No Longer Enough: The Shift to GEO &middot; rawmktg."
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
  var amber='#C99A2E';
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.4);
  var sl=document.getElementById('fsShortlist');
  if(sl){var lab=['AI chatbots','Review sites (G2)','Your website (SEO)','Peer referrals','Cold outbound'];var val=[88,71,49,33,14];
    var cols=[up,up,amber,signal,rgba(signal,0.7)];
    new Chart(sl,{type:'bar',data:{labels:lab,datasets:[{data:val,backgroundColor:cols,borderRadius:4,barThickness:22}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' shortlist-influence index '+c.raw+'/100';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">How AI Search Works &middot; Strategy</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Jul 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/fs_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/fs_cb.js"],capture_output=True,text=True)
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),
 "| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| compare:",hh.count('class="compare-grid"'),"| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| statgrid:",hh.count('class="stat-grid"'),"| listitem:",hh.count('role="listitem"'))
