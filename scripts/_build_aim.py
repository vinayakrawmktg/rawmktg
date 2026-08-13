#!/usr/bin/env python3
"""SCRATCH: build blogs/ai-mode-vs-ai-overviews.html (How AI Search Works). Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="ai-mode-vs-ai-overviews"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-13"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/winning-google-isnt-winning-ai.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE=''  # AdSense removed: no ad units, hurts TBT

def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def h3(t): return f"<h3>{esc(t)}</h3>"
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        rowcls=""; cells=r
        if isinstance(r,tuple) and len(r)==2 and isinstance(r[0],str) and r[0]=="__hl__": rowcls=' class="hl"'; cells=r[1]
        tds=""
        for j,c in enumerate(cells):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr{rowcls}>{tds}</tr>"
    return f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div><table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def compare(label_a,items_a,label_b,items_b):
    la="".join(f"<li>{esc(x)}</li>" for x in items_a); lb="".join(f"<li>{esc(x)}</li>" for x in items_b)
    return (f'<div class="compare-grid"><div class="compare-col"><div class="compare-col-label seo">{esc(label_a)}</div><ul>{la}</ul></div>'
            f'<div class="compare-col"><div class="compare-col-label geo">{esc(label_b)}</div><ul>{lb}</ul></div></div>')
def chart(cid,h,cap): return f'<div class="chart-wrap"><canvas id="{cid}" height="{h}"></canvas></div><div class="chart-caption">{esc(cap)}</div>'
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
def code(label,lang,lines):
    pre="\n".join(lines)
    return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><span class="code-lang">{esc(lang)}</span><pre>{pre}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="AI Mode vs AI Overviews"
DECK="Google's two AI surfaces share a query box but run different retrieval logic and cite different sources, and a B2B brand has to earn its place in both. How each one decides what to show."
DESC=("Google split search into two AI products: AI Overviews and AI Mode. They share a query box but agree on sources only 13.7% of "
      "the time across 730K paired responses. The architecture split, query fan-out, why ranking wins one surface but not the other, "
      "who AI Mode actually cites, and the dual-track GEO playbook.")
DATANOTE=("A mechanism breakdown of Google's two AI surfaces, AI Overviews and AI Mode, built from published citation-overlap studies "
          "(Ahrefs 730K response pairs, STAT, SE Ranking, BrightEdge, BuzzStream) captured June 2026. Figures are drawn from those "
          "sources and cited at the foot of this report. AI outputs vary by run; the pattern is the point.")

REFS=[
 ("Ahrefs - Are AI Mode and AI Overviews just different versions of the same answer? (730K responses)","https://ahrefs.com/blog/ai-overviews-vs-ai-mode/"),
 ("Moz - Only 12% of AI Mode citations match URLs in the organic SERP","https://moz.com/blog/ai-mode-citations"),
 ("BrightEdge - AI Overview citations now 54% from organic rankings","https://www.brightedge.com/resources/weekly-ai-search-insights/rank-overlap-after-16-months-of-aio"),
 ("Ahrefs - 38% of AI Overview citations pull from the top 10","https://ahrefs.com/blog/ai-overview-citations-top-10/"),
 ("BuzzStream - AI citation overlap: do AI platforms cite the same sites?","https://www.buzzstream.com/blog/ai-citation-overlap/"),
 ("Aleyda Solis - Google's query fan-out technique and what it means for SEO","https://www.aleydasolis.com/en/ai-search/google-query-fan-out/"),
 ("Google - Optimizing your website for generative AI features in Search","https://developers.google.com/search/docs/fundamentals/ai-optimization-guide"),
 ("Semrush - What is Google AI Mode (and how to optimize for it)","https://www.semrush.com/blog/google-ai-mode/"),
]

out=[]
out.append('<p class="lead">'+norm("Google did not add AI to search. It split search into two AI products that share a query box, and they disagree about which sources deserve a citation almost nine times out of ten. For anyone doing GEO, that disagreement is the whole story: you cannot optimize for \"Google AI\" as a single target. There are two targets, they reward different work, they pull from different places, and a page that wins one can be invisible in the other.")+'</p>')
out.append(p("The first surface is "+L("AI Overviews","#architecture")+": the boxed summary above the blue links. You never ask for it, it fires automatically on roughly a quarter of queries. The second is AI Mode: a separate tab you deliberately select, where search becomes a conversation that remembers what you asked three turns ago. Same box, same brand, two retrieval engines with their own logic, update cadence and citation habits. Across 730,000 paired responses, the same query produces two completely different source lists 86.3% of the time."))

# 01
out.append(sec("01","architecture","What's behind Google's two AI surfaces?","Both run on Gemini, but they search a different number of times, touch different indexes, and weigh ranking differently.",
  "AI Overviews is a passive summarization layer stitched into the standard results page. AI Mode is an active, standalone conversational tab the user opts into. That is where the resemblance ends."))
out.append(compare("AI Overviews - passive summary",
  ["Automatic trigger, fires on ~25% of queries","Single-pass RAG over the standard index","Reads top-ranking standard-index docs","~200 words, ~21-second session","Low source diversity, ranking-led"],
  "AI Mode - conversational research",
  ["User-activated tab, opted into","Parallel query fan-out, retrieves many times","Reads live web + Knowledge Graph + Shopping Graph (50B+ SKUs)","~800 words, ~49-second session","High source diversity, rank-decoupled"]))
out.append(p("AI Overviews is, mechanically, a thin wrapper on classic ranking: it pulls high-ranking documents from the standard index and hands them to a Gemini summarizer. Speed is the point, and the sources skew toward what was already going to rank. AI Mode runs on the Gemini 3 family, keeps conversational context across follow-ups, and crucially does not retrieve once, it retrieves many times, in parallel, against several indexes at once. That single design choice drives the low overlap."))

# 02
out.append(sec("02","fan-out","How does query fan-out break the rules?","AI Mode shreds your query into sub-queries and runs them concurrently across specialized indexes.",
  "Classic search maps one query to one retrieval path. "+L("AI Mode does not do that","/blogs/how-rag-actually-works")+". It takes the parent query, decomposes it into sub-queries, and runs them in parallel. The technique is called query fan-out, and it is why AI Mode cites pages you have never seen rank for the head term."))
out.append(pipeline([("Decompose","Gemini splits the parent query"),("Parallel retrieval","sub-queries hit many indexes at once"),("Evaluate & extract","isolate the passages that answer each"),("Synthesize & cite","one narrative, many sources")],3,
  "Query fan-out, four stages. A complex question can split into up to 16 concurrent sub-queries pulling live news, spec sheets, pricing feeds and forum threads in one pass."))
out.append(p("That parallelism is exactly why AI Mode surfaces deep internal pages, product documentation and niche forum posts that never rank for the primary keyword. It bypasses the single-index bottleneck classic search lives inside. The implication for a brand is blunt: ranking for the head term no longer guarantees you are in the room when the answer gets assembled. It is the same reason "+L("the Google leader is not the AI leader","/blogs/winning-google-isnt-winning-ai")+" in category after category."))

# 03
out.append(sec("03","overlap","How much do the two surfaces actually overlap?","Just 13.7% of cited sources, across 730K paired responses. They draw from largely separate pools.",
  "Here is the number that should reorganize a GEO roadmap. Ahrefs studied 730,000 paired responses and found AI Overviews and AI Mode agreed on sources just 13.7% of the time. It is not an Ahrefs artifact: independent studies land in the same low-overlap neighborhood."))
out.append(table("Overlap and concordance studies, 2025-26",["Study","Sample","What was compared","Overlap"],[
 ("__hl__",("Ahrefs","730K response pairs","AI Overviews vs AI Mode citations","13.7%")),
 ("Ahrefs","Top-3 citations","AI Overviews vs AI Mode","16.3%"),
 ("STAT","40K keywords","AI Mode URL vs organic top-10","12%"),
 ("SE Ranking","Cross-query set","AI Mode URL vs organic (domain: 51%)","14%"),
 ("BuzzStream","30K citations, 595 prompts","Citations exclusive to one platform","76.1%"),
 ("Agency monitor","12 verticals, Jan-Apr 2026","AIO-cited page also cited in AI Mode","15%"),
], cls=lambda j,c:"label" if j==0 else ("up" if j==3 else "")))
out.append(p("But there is a twist that changes how you read all of this. Low source overlap does not mean the two surfaces give different answers. They mostly do not. The disagreement is about citations, not conclusions."))
out.append(code("similarity.py - URL sets vs answer text","python",[
 '<span class="cm"># 1 / URL overlap - how many cited links are shared?</span>',
 'jaccard(A, B) = |A &#8745; B| / |A &#8746; B|',
 '   A = AI Overviews cited-URL set',
 '   B = AI Mode cited-URL set',
 '   result &#8776; <span class="kw">0.137</span>   <span class="cm"># low. the links barely intersect.</span>',
 '',
 '<span class="cm"># 2 / answer overlap - do the two texts agree?</span>',
 'cosine(u, v) = (u &#183; v) / (||u|| &#183; ||v||)',
 '   u = embed(AIO answer)',
 '   v = embed(AI Mode answer)',
 '   result &#8776; <span class="st">0.86</span>    <span class="cm"># high. the conclusions converge.</span>',
]))
out.append(pull("Both surfaces reach the same conclusion nine times out of ten. They just cite entirely different sources, in different language, to get there."))
out.append(p("That gap is the GEO opportunity stated precisely. The conclusion is not the prize, the citation is. Two brands can both be \"the answer\" while only one gets named and linked. Your job is not to be correct, the model is already correct without you. Your job is to be the source it reaches for when it justifies the answer, and because the two surfaces reach for different sources, you have to earn that slot twice."))

# 04
out.append(sec("04","ranking","How does each surface treat your organic ranking?","Opposite relationships: AI Overviews tracks it, AI Mode is decoupled from it.",
  "This is where the dual-track strategy comes from. The two surfaces have opposite relationships with classic ranking, and that contrast decides which tactics you point at which surface."))
out.append(chart("aimConcordance",200,"Figure 1 - share of cited URLs that match the organic top-10 for the same query. AI Overviews 38%; AI Mode just 12%."))
out.append(compare("AI Overviews - tracks organic",
  ["38% of cited URLs rank in the organic top 10","Organic-rank share of citations climbed 32.3% to 54.5% (mid-2024 to late-2025)","Healthcare and other YMYL verticals reach 75.3%","If you can rank, you can largely earn the Overview"],
  "AI Mode - decoupled",
  ["Only ~12% of cited URLs match the exact organic top-10 (14% per SE Ranking)","Domain-level overlap is ~51%: it knows your site","It pulls the buried comparison page, the docs, the data study","Your homepage is not the asset, your depth is"]))
out.append(p("Read those in sequence. AI Overviews still respects classic ranking signals, and the dependency is strengthening over time. AI Mode refuses that shortcut: it recognizes your site as authoritative but declines to cite your money landing page, reaching instead for the deep internal resource that resolves a specific sub-query. The work that wins each surface is "+L("not the same","/blogs/why-engines-recommend-different-vendors")+"."))

# 05
out.append(sec("05","prompt-tests","What does the split look like on real prompts?","Complex multi-intent queries diverge hard; flat factual queries collapse onto the same canonical sources.",
  "Theory is cheap. Here is what the split looks like on real prompts. The first query is complex and multi-intent, the kind that triggers full fan-out. The second is a flat factual entity query, the one situation where both surfaces collapse onto the same sources."))
out.append(compare("AI Overviews - \"smart ring vs watch vs mat?\"",
  ["One short paragraph of summary","Cites three top-ranking product-review URLs","Leans on authoritative health portals","Clean, fast, shallow"],
  "AI Mode - same question",
  ["Fan-out splits it: sensor specs, battery life, medical accuracy","A comparative layout with spec cards","Cites a dozen-plus sources: Reddit, product docs, niche publications","Runs a research project, not a summary"]))
out.append(callout("The exception that proves the mechanic",[
 "Ask a flat factual question, \"What products does Adidas offer?\", and every surface, including third-party models, converges on the same foundational sources: the annual report, the investor-relations portal, and Wikipedia. Wikipedia carries 35% of citations shared across AI engines despite being only 3.8% of total citations. Factual identity queries pull from canonical sources, so the surfaces agree.",
]))
out.append(p("The pattern is consistent: the more a query needs to be reasoned across dimensions, the more fan-out engages and the more the two surfaces split apart. Most B2B buying questions, \"best X for Y\", \"X vs Y\", \"how do teams handle Z\", are exactly the multi-intent prompts that maximize divergence, which is why B2B brands feel the split harder than consumer ones."))

# 06
out.append(sec("06","topology","Who does AI Mode actually cite?","A concentrated mix: the top five domains take 38%, and Google's own properties take 22.8%.",
  "If 13.7% tells you the surfaces differ, the domain mix tells you how, and where the oxygen for external brands actually is. AI Mode concentrates its citations hard, and three of its top five domains are Google's own."))
out.append(chart("aimDomains",260,"Figure 2 - AI Mode citation share by domain, top 5. Three of the five (YouTube, blog.google, Google.com) are Google-owned, 22.8% of the total."))
out.append(p("Two trends inside that chart matter for planning. Self-citation is rising fast: Google.com citations tripled between mid-2025 and early 2026 as help docs and Maps features got wired into the chat interface. And "+L("user-generated content is surging","/blogs/why-ai-cites-reddit-g2-analysts")+": Reddit citations jumped 450% over three months. AI Overviews behaves differently again, leaning multimodal, with YouTube holding a 23.3% share and a relevant on-page video raising AIO citation odds by 156%."))
out.append(table("AI Mode citation behavior, four numbers to plan around",["Metric","Value","What it means"],[
 ("Sidebar block links","90.8%","Most citations render as block links, not inline (8.9% inline, 0.3% traditional)"),
 ("URLs surviving 3 runs","9.2%","Run the same query 3x and only 9.2% of URLs persist; 60%+ of domains rotate"),
 ("Reddit citation rise","450%","Over a three-month window, reflecting appetite for real-world experience"),
 ("On-page video lift","156%","Increase in AI Overviews citation odds from a relevant video"),
], cls=lambda j,c:"label" if j==0 else ("up" if j==1 else "")))
out.append(p("The volatility number is the one most teams underweight. AI Mode uses a probabilistic retrieval model that continuously reshuffles its sources, so you are not chasing a fixed ranking that holds still once you win it. You are raising your inclusion odds across a distribution that re-rolls on every query, which reframes the whole measurement question."))

# 07
out.append(sec("07","playbook","How do you appear in Google AI Mode?","Semantic depth and entity authority, not keyword density. Three levers, in order of leverage.",
  "Because AI Mode is conversational and runs on fan-out, the work that earns citations is depth and authority. Three levers."))
out.append(h3("Lever 01 - Structure pages for extraction"))
out.append(p("After every target H2, lead with a direct, self-contained answer of 40 to 55 words before any narrative, matching Gemini's extraction patterns. Treat each H2 as a "+L("standalone answer","/blogs/anatomy-of-a-high-citation-page")+" and phrase headings as natural questions. Cut conversational filler: statistics with clear source citations lift citation probability by 40% to 70%. Apply "+L("FAQPage, Article and Product schema","/blogs/schema-markup-ai-citations-2026")+" so crawlers can parse and credit claims."))
out.append(h3("Lever 02 - Build off-site co-citation"))
out.append(p("Participate in relevant Reddit, Quora and Stack Overflow threads, AI Mode leans on UGC for real-world reviews, so mentions in high-engagement threads convert directly into citation rate. Build YouTube guides (Gemini treats transcripts as text, so speak your brand and methodology terms clearly). And keep LinkedIn, Crunchbase, G2 and Capterra profiles detailed and current, because the Knowledge Graph and Shopping Graph use them to verify entity relationships during comparisons."))
out.append(h3("Lever 03 - Measure the right thing"))
out.append(p("Track Brand Inclusion Rate (is your brand present in the synthesized answer at all), Mention and Citation Rate (where your name is generated and your URL explicitly linked), and "+L("Share of AI Voice","/blogs/prompt-to-citation-tracking")+" (your citation volume against competitors across a fixed prompt set, plus co-citation mapping). This lever forces teams to abandon a fifteen-year-old dashboard, because 93% of AI Mode sessions end without a click. Click-through rate, rank position and traffic volume are measuring a door almost nobody walks through anymore."))
out.append(compare("Legacy metrics - retire these",
  ["Click-through rate (CTR)","Keyword rank position","Page impressions","Organic traffic volume"],
  "Generative metrics - track these",
  ["Brand Inclusion Rate","Mention Rate %","Share of AI Voice (SOAV)","Sentiment & co-citation mapping"]))

# 08
out.append(sec("08","takeaway","What's the dual-track takeaway?","AI Overviews reward the page; AI Mode rewards the brand. You run both tracks at once.",
  "One sentence carries the strategy. The architectural split forces a parallel approach, because the tactics that win one surface do almost nothing for the other."))
out.append(table("The dual-track alignment",["Dimension","AI Overviews","AI Mode"],[
 ("Optimize for","Page-level ranking","Domain-level authority"),
 ("Core tactic","40-55 word direct summaries","Multi-platform mentions"),
 ("Content shape","Direct, comparative tables","Modular informational hubs"),
 ("Wins on","Top-10 rankings + schema","Proprietary research + off-site presence"),
 ("Scoreboard","Citation share vs rank","Inclusion rate vs competitors"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("AI Overviews is, at bottom, a ranking game with a summarization layer bolted on top. Win it with structured data, concise summary blocks and the top-10 positions you already chase. AI Mode is an authority game decided before the click that never comes. Win it with comprehensive topic coverage, proprietary research worth citing, and a presence on the platforms it trusts more than your own homepage."))
out.append(callout("The bottom line",[
 "Optimize for one surface and you are half-visible. The brands that hold organic visibility through this shift run both tracks at once, treating Google not as one AI to please but as two engines that have to be earned separately. The 13.7% overlap is not a problem to solve. It is the map.",
]))

# references
refli="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in REFS)
out.append(f'<div class="about-block"><div class="about-label">Sources &amp; further reading</div><ol style="margin:0;padding-left:18px;font-family:var(--f-mono);font-size:11.5px;line-height:1.7;color:var(--mute)">{refli}</ol></div>')

FAQ=[
 ("What is the difference between Google AI Overviews and AI Mode?","AI Overviews is the boxed summary that fires automatically above the blue links on about a quarter of queries; it is a single-pass summary of top-ranking pages. AI Mode is a separate, user-activated conversational tab that runs query fan-out, retrieving many sub-queries in parallel across the live web, Knowledge Graph and Shopping Graph. Both run on Gemini, but they cite the same sources only 13.7% of the time."),
 ("Why do AI Overviews and AI Mode cite different sources?","Because they retrieve differently. AI Overviews summarizes pages that already rank in the standard index, so its sources skew toward classic SEO winners. AI Mode decomposes a query into up to 16 sub-queries and runs them across multiple specialized indexes, surfacing deep pages, documentation and forum threads that never rank for the head term. Across 730K paired responses the two agree on sources just 13.7% of the time, though their answers converge about 86%."),
 ("Does ranking in Google's organic top 10 get me into AI Mode?","Not reliably. Only about 12% of AI Mode's cited URLs match the exact organic top-10 URL for the same query (14% per SE Ranking). Domain-level overlap is higher, around 51%, so AI Mode recognizes your site, it just pulls deeper pages than your money landing page. AI Overviews is the opposite: roughly 38% of its citations rank in the organic top 10, and that dependency is strengthening."),
 ("How do you optimize for Google AI Mode?","Three levers: structure pages for extraction (lead each H2 with a 40-55 word direct answer, add FAQPage and Article schema); build off-site co-citation (Reddit and forum participation, YouTube with clean transcripts, accurate G2/Capterra/Crunchbase profiles); and measure the right thing (Brand Inclusion Rate, Mention and Citation Rate, Share of AI Voice) since 93% of AI Mode sessions end without a click."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven explainers and teardowns on how AI search decides what to recommend, pulling citation and SEO data to show exactly where the visibility gaps are. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("13.7%","Citation overlap between AI Overviews and AI Mode"),("86.3%","Of queries return two different source lists"),("93%","Of AI Mode sessions end without a click")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#architecture"><span class="toc-num">01</span>Two surfaces, one box</a></li>'
     '<li><a href="#fan-out"><span class="toc-num">02</span>Query fan-out</a></li>'
     '<li><a href="#overlap"><span class="toc-num">03</span>The 13.7% boundary</a></li>'
     '<li><a href="#ranking"><span class="toc-num">04</span>Ranking concordance</a></li>'
     '<li><a href="#prompt-tests"><span class="toc-num">05</span>Two prompts, two behaviors</a></li>'
     '<li><a href="#topology"><span class="toc-num">06</span>Who AI Mode cites</a></li>'
     '<li><a href="#playbook"><span class="toc-num">07</span>The playbook</a></li>'
     '<li><a href="#takeaway"><span class="toc-num">08</span>The dual-track close</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this report</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":"AI Mode vs AI Overviews: Google's Two AI Surfaces","description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["AI Mode","AI Overviews","Google","query fan-out","GEO","generative engine optimization","AI citations","Gemini","citation overlap"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="AI Mode vs AI Overviews: Google's Two AI Surfaces (and Why They Cite Differently) &middot; rawmktg."
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
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.4);

  var cc=document.getElementById('aimConcordance');
  if(cc){new Chart(cc,{type:'bar',data:{labels:['AI Overviews','AI Mode'],datasets:[{data:[38,12],backgroundColor:[up,signal],borderRadius:4,barThickness:30}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% match the organic top-10';}}}},
      scales:{x:{beginAtZero:true,max:50,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var dm=document.getElementById('aimDomains');
  if(dm){var lab=['Wikipedia','YouTube','blog.google','Reddit','Google.com'];var val=[11.22,9.51,5.95,5.82,5.62];var goog=[false,true,true,false,true];
    var cols=goog.map(function(g){return g?signal:neutral;});
    new Chart(dm,{type:'bar',data:{labels:lab,datasets:[{data:val,backgroundColor:cols,borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of AI Mode citations'+(goog[c.dataIndex]?' (Google-owned)':'');}}}},
      scales:{x:{beginAtZero:true,max:12,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">How AI Search Works &middot; Mechanism</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Jun 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

import subprocess
hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/aim_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/aim_cb.js"],capture_output=True,text=True)
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC SLOPE:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),
 "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| compare:",hh.count('class="compare-grid"'),"| pipeline:",hh.count('class="pipeline"'),"| code:",hh.count('class="code-block"'),"| callout:",hh.count('class="callout-box"'),"| listitem:",hh.count('role="listitem"'))
