#!/usr/bin/env python3
"""SCRATCH: build blogs/reddit-geo-playbook.html (Content & Authority). Do NOT commit."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="reddit-geo-playbook"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-30"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/ai-mode-vs-ai-overviews.html",encoding="utf-8").read()
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
        rowcls=""; cells=r
        if isinstance(r,tuple) and len(r)==2 and r[0]=="__hl__": rowcls=' class="now-row"'; cells=r[1]
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
def code(label,lang,lines):
    return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><span class="code-lang">{esc(lang)}</span><pre>'+"\n".join(lines)+'</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="The Reddit GEO Playbook"
DECK="Reddit is the single largest third-party source shaping B2B answers in generative search. Which threads get pulled, why the low-upvote ones win, and how to participate without getting nuked."
DESC=("Reddit drives 20.8% of B2B AI citations, more than every review directory combined. A playbook on which Reddit threads AI "
      "actually cites (80% have under 20 upvotes), how each engine reads Reddit differently, the format signature of cited threads, "
      "and the 9:1, three-comment, 30-day workflow to earn citations without getting banned.")
DATANOTE=("A data-led playbook on Reddit's role in generative search, drawn from published studies: AirOps x Foundation Inc. (57.2M "
          "citations, 60 days), Semrush (248,000 cited Reddit URLs), Tinuiti Q1 2026 and Profound x Semrush. Figures are from those "
          "sources and cited at the foot of this report. June 2026.")

REFS=[
 ("Foundation Inc. x AirOps, Reddit accounts for 21% of third-party citations (60-day study)","https://foundationinc.co/lab/reddit-ai-citations"),
 ("EMGI, The Reddit citation study: subreddits cited by AI search","https://emgigroup.com/blog/reddit-citations-saas-ai-search/"),
 ("Discovered Labs, Reddit content types LLMs cite most","https://discoveredlabs.com/blog/the-reddit-content-types-that-llms-cite-most-data-backed-breakdown"),
 ("CMSWire, Reddit's rise in AI citations and AEO strategy","https://www.cmswire.com/digital-marketing/reddits-rise-in-ai-citations-what-marketers-must-know-about-aeo-strategy/"),
 ("Single Grain, Avoiding Reddit's spam filters","https://www.singlegrain.com/social-media-management/best-practices/avoiding-reddits-spam-filters-best-practices-for-promotion/"),
 ("OptimizeGEO, How to optimize for AI search: the 2026 playbook","https://www.optimizegeo.ai/blog/how-to-optimize-for-ai-search"),
]

out=[]
out.append('<p class="lead">'+norm("Search has reorganized itself underneath us. The job is no longer ranking a page on a results screen, it is becoming a citation inside a generated answer, and generated answers are built from somewhere your marketing team does not control. As buyers move evaluation into ChatGPT, Perplexity, Gemini and Copilot, those models reach for third-party, peer-validated platforms to establish consensus, and Reddit sits at the top of that pile.")+'</p>')
out.append(p("Two licensing deals turned that into infrastructure. Reddit's roughly $60M/year agreement with Google and $70M/year agreement with OpenAI wired its repository of human discussion directly into both training corpora and live retrieval indexes. After Google's indexing integration, Reddit's search visibility grew 342%, making it the second most visible domain on the web behind Wikipedia."))

# 01
out.append(sec("01","homepage","Why did your homepage stop being the answer?","Because models cite third-party consensus, not your own marketing copy, and Reddit is the biggest source of it.",
  "When a buyer prompts an AI engine, the model queries a live index, pulls candidate documents, and extracts the segments most relevant to the question. Reddit threads, structured around the same questions buyers ask, sit at the top of that candidate set again and again. Appear positively inside them and you are folded into the recommendation; absent, and you are invisible at the moment of evaluation."))
out.append(chart("rpDiscovery",170,"Figure 1 - share of external citations during unbranded, high-intent discovery prompts. Reddit dwarfs the review directories most B2B teams obsess over. Source: AirOps x Foundation Inc., 57.2M citations"))
out.append(pull("If a brand has no active, positive footprint across its category's subreddits, it is systematically excluded from the shortlist a buyer's AI builds for them."))

# 02
out.append(sec("02","engines","How does each engine read Reddit?","Perplexity treats it as the primary knowledge base; Gemini routes around it almost entirely.",
  "There is no single \"AI citation\" behavior. Retrieval architectures diverge sharply by index, licensing and design philosophy. To get cited by Perplexity, threads must be engineered for real-time extraction; to show up in Gemini, you essentially cannot rely on Reddit at all."))
out.append(chart("rpEngines",240,"Figure 2 - Reddit citation share by engine, top-10 citations. Perplexity behaves like a forum-discovery engine; Gemini like an encyclopedia. Source: Tinuiti Q1 2026, Profound x Semrush"))
out.append(table("Reddit citation behavior by engine",["Engine / surface","Reddit share","Ingestion & retrieval hook","Operator stance"],[
 ("__hl__",("Perplexity","46.7% top-10","Real-time RAG; heavily weights community-forum nodes","Forums are the primary knowledge base; needs continuous participation")),
 ("Google AI Overviews","21.0% top-10","Deep Search-index integration + live Google-Reddit API","Pulled from top organic rankings and discussion blocks"),
 ("ChatGPT","11.3% top","Hybrid: OpenAI-Reddit API + Bing-indexed web","High parametric reliance; seed brand mentions in historical threads"),
 ("Google AI Mode","~9.0% social","Conversational layer for long-tail intent","Matches experiential problem-solution narrative blocks"),
 ("Google Gemini","~0.1%","Structured knowledge graphs; on-domain authority","Low community dependency; anchor authority on owned domains"),
], cls=lambda j,c:"label" if j==0 else ("up" if j==1 and ("46" in c or "21" in c) else ("mute" if j==1 and "0.1" in c else ""))))
out.append(p("The contrast is mechanical, not stylistic. Perplexity runs roughly a 25% lower source-duplication rate than Google and actively hunts unique, conversational human input, pulling from Reddit or Quora 41% of the time on commercial queries. Gemini sits at the opposite pole, routing toward structured databases and formal editorial. ChatGPT is a third case: its hybrid ingestion leans on parametric memory, so a thread that lands early and persists can be absorbed into the next training cycle, not just retrieved live. The split, "+L("which is why engines recommend different vendors","/blogs/why-engines-recommend-different-vendors")+", forces a split budget: conversational forum seeding for Perplexity and "+L("AI Overviews","/blogs/ai-mode-vs-ai-overviews")+", owned structured assets for Gemini."))

# 03
out.append(sec("03","structure","What makes a thread AI-favored?","Structural readability and factual density, not karma. The cited threads collapse onto a few shapes.",
  "An LLM is indifferent to drama, awards and karma. It rewards structure, factual density and semantic alignment with the prompt. When Semrush analyzed 248,000 cited Reddit URLs, the distribution collapsed onto a handful of conversation shapes."))
out.append(chart("rpFormats",170,"Figure 3 - share of Reddit citations by thread format. Question-headed Q&A threads alone account for more than half of every Reddit citation. Source: Semrush, 248,000 cited URLs"))
out.append(p("The structural signature is sharper than the format split. Across cited threads, 98% are text-based self-posts rather than link shares, 76% of titles end in a question mark, and 69% open with an interrogative word (what, best, which, is, how). That is the exact natural-language shape of the prompts buyers type into a chat window."))
out.append(statgrid([("98%","Cited threads are text self-posts"),("76%","Titles end in a question mark"),("69%","Open with an interrogative word")]))
out.append(h3("The low-upvote citation paradox"))
out.append(p("The most counterintuitive, and most exploitable, finding is that social validation barely matters. In B2B SaaS categories, 80% of cited threads have fewer than 20 upvotes, with a median of just 5 to 8. Teams gaming Reddit's upvote algorithm are optimizing the wrong number entirely."))
out.append(compare("512 upvotes, viral, NOT cited",
  ["High-engagement thread buried in off-topic banter and jokes","Low semantic density, no clean extractable answer","Retrieval score: 0.18"],
  "6 upvotes, quiet, CITED",
  ["Clear question title, a direct structured answer in the first paragraph","Named entities and a concrete metric, high semantic match","Retrieval score: 0.91"]))
out.append(p("The reason is in the math. A RAG system scores candidates by "+L("vector similarity","/blogs/how-rag-actually-works")+", semantic density and answer directness, not native popularity. It converts both the question and every candidate passage into embeddings and surfaces the tightest semantic match. A clean five-upvote explanation is a safer, higher-scoring retrieval target than a 500-upvote thread full of noise. To quantify weight once retrieved, GEO researchers use a Position-Adjusted Word Count: clean, factual paragraphs placed early accumulate the highest scores regardless of votes."))
out.append(code("Position-Adjusted Word Count (PAWC)","retrieval-scoring",[
 'PAWC(s) = <span class="kw">&#931;</span><sub>i</sub>  w<sub>i</sub> &#183; c<sub>i</sub>(s)',
 '',
 '<span class="cm">  c_i(s)  word count contributed by source s at position i in the answer</span>',
 '<span class="cm">  w_i     positional weight; attention decays on a power-law, so earlier</span>',
 '<span class="cm">          and more prominent placement is worth disproportionately more</span>',
]))

# 04
out.append(sec("04","threads","Which threads are getting pulled right now?","Purchase-intent question titles with blunt, balanced, first-person answers, not marketing copy.",
  "The selection criteria are visible in the wild. Across verticals the cited threads share a profile: a purchase-intent question in the title, and top comments that trade polished marketing for honest, first-person comparison. These are the real titles RAG engines lift from."))
out.append(table("Cited threads in the wild",["Thread title","Subreddit","Intent","Cited by"],[
 ("Best and inexpensive CRM for small business","r/crm","purchase intent","Google AIO"),
 ("Best CRM for a bootstrapped startup (NOT Salesforce)?","r/crm","vendor-exclusion","Perplexity"),
 ("Best open source, self-hosted CRM?","r/selfhosted","technical","ChatGPT"),
 ("Terraform state-locking error, AWS S3 backend","r/devops","problem to solution","Claude"),
 ("Best way to automate lead routing in HubSpot?","r/salesforce","entity-dense comparison","Perplexity"),
], cls=lambda j,c:"label" if j==0 else ("mute" if j==1 else ("up" if j==3 else ""))))
out.append(p("CRM queries trigger exceptionally high citation rates, AI Overviews quotes Reddit in 31.5% of CRM searches, bypassing corporate sales pages to lift raw recommendations from r/crm precisely because the top comments are balanced rather than promotional. The DevOps example is cited for its precise problem-solution shape: a specific permissions error in the title, with code snippets and IAM configs in the comments. The marketing example wins on entity density, named products, endpoints and version numbers that hand the model a structured, verifiable dataset."))

# 05
out.append(sec("05","participate","How do you participate without getting nuked?","A 9:1 value-to-promotion ratio, a 30-day warm-up, and a three-comment framework.",
  "Reddit is hostile terrain for B2B operators by design. Communities have an immune response to marketing, and flagged accounts face permanent bans and domain blacklisting. A sustainable motion runs on nine genuine contributions for every brand mention, and you have to clear four layers of spam defense first."))
out.append(table("Reddit's four-layer spam architecture",["Layer","Defense","What it monitors"],[
 ("1","Site-wide algorithmic filters","Account age, karma balance, posting frequency. New accounts posting too fast are silently shadowbanned."),
 ("2","Subreddit AutoMod rules","Per-community rules flag trigger words, repetitive external links, bot-like formatting."),
 ("3","Domain reputation scores","Reddit tracks link drops at the domain level; a flagged URL gets auto-blocked platform-wide."),
 ("4","Manual moderator flags","Mods audit post histories; a profile dominated by one brand gets banned and scrubbed."),
], cls=lambda j,c:"label" if j==0 else ("down" if j==0 else "")))
out.append(p("The cruelest part is that it rarely tells you when you have tripped it. A new account that posts links too early gets shadowbanned, its contributions silently removed and invisible to everyone but the author. That single failure mode is why the warm-up is non-negotiable: it banks the comment karma that clears the automated thresholds before you ever attach a brand."))
out.append(table("The 30-day account warm-up protocol",["Phase","Horizon","Target activity","Compliance"],[
 ("1, Presence","Days 1-14","Subscribe to 10-15 industry subreddits; 2-3 comments/day","Zero links, zero promotion, zero brand mentions"),
 ("2, Engagement","Days 15-30","3-5 comments/day on rising and hot threads","Accumulate 50-200 karma; vary sentence structure"),
 ("3, Seeding","Month 2+","1-2 original threads/month; max 1 brand link/week","Strip all UTM params; hold the 9:1 ratio"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(h3("The three-comment framework"))
out.append(p("When you enter a live evaluation thread, introduce brand context across three moves, never in one."))
out.append(table("Three-comment framework",["Move","Comment","What to do"],[
 ("Comment 1","Pure value","Answer the user's question directly and thoroughly. No links, no brand, no promotional phrasing."),
 ("Comment 2","Contextual experience","Add technical detail, product constraints or operational limits from genuine first-person experience."),
 ("Comment 3","Natural recommendation","Name the brand only if truly relevant. Say who it is for, who it is not for, and disclose affiliation."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(h3("The 3-step GEO workflow"))
out.append(p("To run this at scale, chain three models, each doing the job it is best at."))
out.append(pipeline([("ChatGPT, profile & filter","question titles, 30-100 reply sweet spot"),("Perplexity, map the gap","find high-intent queries with no citation yet"),("Claude, format & write","answer-first, 40-60 words, fact every 100")],2,
  "The 3-step workflow: filter for question-form threads in the 30-100 reply sweet spot, map the answer gap, then draft for extraction with a direct answer in the first 30% of the text."))

# 06
out.append(sec("06","onsite","How do you anchor discovery to your own domain?","With schema and crawler access, so engines can corroborate your Reddit footprint on your site.",
  "Off-site authority does not stand alone. Generative engines validate a claim across multiple independent nodes, so your website has to match the structural and semantic context of your Reddit footprint. Two layers do most of the work: schema, and crawler access."))
out.append(p("Structured data tells AI agents exactly how to parse a page. In controlled tests, adding "+L("JSON-LD","/blogs/schema-markup-ai-citations-2026")+" lifted precise information-extraction rates from 16% to 54%, more than tripling how reliably a model could pull the right fact. Brands with rich aggregate-review schema are cited for \"best of\" queries at 2.3x the rate of competitors with incomplete structured data. Go hyper-specific on applicationCategory: MasterDataManagementSoftware, not a vague BusinessSoftware."))
out.append(code("software-application.jsonld","JSON-LD",[
 '<span class="kw">{</span>',
 '  <span class="st">"@context"</span>: <span class="st">"https://schema.org"</span>,',
 '  <span class="st">"@type"</span>: <span class="st">"SoftwareApplication"</span>,',
 '  <span class="st">"applicationCategory"</span>: <span class="st">"MasterDataManagementSoftware"</span>,',
 '  <span class="st">"aggregateRating"</span>: <span class="kw">{</span>',
 '    <span class="st">"@type"</span>: <span class="st">"AggregateRating"</span>,',
 '    <span class="st">"ratingValue"</span>: <span class="st">"4.6"</span>, <span class="st">"reviewCount"</span>: <span class="st">"218"</span>, <span class="st">"author"</span>: <span class="st">"G2"</span>',
 '  <span class="kw">}</span>',
 '<span class="kw">}</span>',
]))
out.append(p("None of it matters if crawlers cannot reach the page. Publish an "+L("llms.txt","/blogs/internal-linking-for-ai-retrieval")+" at your root as a high-priority index to your most fact-dense pages, and make sure "+L("robots.txt admits the real-time retrieval agents","/blogs/how-ai-crawlers-index-your-site")+". Then round it out with dedicated integration pages (\"does product X connect with HubSpot?\") carrying HowTo schema, which covers ChatGPT, Perplexity and Gemini at once."))
out.append(code("/robots.txt","config",[
 '<span class="cm"># Admit real-time RAG crawlers explicitly</span>',
 '<span class="kw">User-agent:</span> GPTBot',
 '<span class="kw">Allow:</span> /',
 '<span class="kw">User-agent:</span> PerplexityBot',
 '<span class="kw">Allow:</span> /',
 '<span class="kw">User-agent:</span> ClaudeBot',
 '<span class="kw">Allow:</span> /',
]))

# 07
out.append(sec("07","measure","How do you measure the generative-search motion?","Three citation metrics on a fixed cadence, not keyword density or backlink volume.",
  "Keyword density and backlink volume are losing meaning in an ecosystem governed by real-time RAG. Track three metrics instead, on a fixed cadence rather than a vanity dashboard."))
out.append(table("The generative search scorecard",["Metric","Name","What it tracks"],[
 ("AICF","AI Citation Frequency","How often your domain or threads are cited across ChatGPT, Perplexity, Gemini and AI Overviews for a defined query set."),
 ("SOV","AI Share of Voice","Your citation frequency relative to named competitors for unbranded discovery prompts, the shortlist battle, quantified."),
 ("PVR","Prompt-Level Visibility","Run your 20 highest-priority commercial prompts weekly; track which platforms cite you and which threads serve as the source."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Finally, stop letting AI-driven traffic hide inside \"Direct.\" Build a regex-based custom channel in GA4 so you can attribute trial signups and pipeline back to the generative-search motion, the same "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+" discipline applied to revenue."))
out.append(code("GA4 - custom channel group, AI Search","regex",[
 '<span class="cm"># Session source matches -></span>',
 '.*chatgpt.*|.*openai.*|.*perplexity.*|.*gemini.*google.*|',
 '.*copilot.*|.*claude.*|.*mistral.*|.*phind.*|.*you\\.com.*',
]))
out.append(pull("Stop optimizing keywords on a domain you own. Start cultivating a verified, multi-node paper trail across the platforms your buyers already trust."))
out.append(p("The brands that win the generative era are not the ones with the most content. They are the ones with the most corroboration, a consistent, structured, community-compliant footprint an AI can assemble into an answer and cite with confidence. Reddit is where that footprint starts. Build it deliberately, hold the ratio, and earn the threads the models actually quote."))
out.append(callout("Run the off-site audit",[
 "Reddit is one tier of the off-site authority stack engines pull from. Score your full presence, review sites, analysts, community and entity schema, with the free "+L("Off-Site Authority Stack Scorecard","/tools/off-site-authority-scorecard")+", or check a single page against the extraction window with the "+L("Answer Block Optimizer","/tools/answer-block-optimizer")+".",
]))

FAQ=[
 ("What share of AI citations come from Reddit?","Reddit is the largest single third-party source in B2B generative search: about 20.8% of the top-50 external citation domains across 57.2M citations tracked over 60 days, more than every review directory combined. During unbranded discovery prompts (when a buyer asks a model to recommend a category leader with no vendor named), Reddit's share climbs to 30.9%."),
 ("Why do low-upvote Reddit threads get cited by AI?","Because retrieval systems score candidates by vector similarity, semantic density and answer directness, not by upvotes. A clean five-upvote explanation with a question title and a direct answer scores higher than a 500-upvote thread full of off-topic banter. In B2B SaaS categories, 80% of cited threads have fewer than 20 upvotes, with a median of 5 to 8."),
 ("Which AI engines cite Reddit the most?","Perplexity leads at 46.7% of top-10 citations (it behaves like a forum-discovery engine), followed by Google AI Overviews at 21.0%, ChatGPT at 11.3%, and Google AI Mode around 9%. Gemini is the outlier at roughly 0.1%, it routes toward structured knowledge graphs and editorial authority instead of forums, so Reddit seeding does almost nothing for it."),
 ("How do you post on Reddit for AI visibility without getting banned?","Hold a 9:1 value-to-promotion ratio and run a 30-day warm-up before any brand mention: days 1-14 build presence with link-free comments, days 15-30 accumulate 50-200 karma to clear AutoMod thresholds, then from month two seed sparingly (max one brand link a week, UTM params stripped). In live threads, use the three-comment framework: pure value, then experience, then a transparent recommendation."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
refli="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in REFS)
out.append(f'<div class="about-block"><div class="about-label">Sources &amp; further reading</div><ol style="margin:0;padding-left:18px;font-family:var(--f-mono);font-size:11.5px;line-height:1.7;color:var(--mute)">{refli}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven playbooks and teardowns on how AI search decides what to recommend, pulling citation and SEO data to show exactly where the visibility gaps are. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("20.8%","Reddit's share of B2B AI citations"),("30.9%","Reddit's share during discovery prompts"),("80%","Of cited threads have under 20 upvotes")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#homepage"><span class="toc-num">01</span>Off-site authority</a></li>'
     '<li><a href="#engines"><span class="toc-num">02</span>Every engine reads Reddit</a></li>'
     '<li><a href="#structure"><span class="toc-num">03</span>What AI-favored looks like</a></li>'
     '<li><a href="#threads"><span class="toc-num">04</span>Threads getting pulled</a></li>'
     '<li><a href="#participate"><span class="toc-num">05</span>The playbook</a></li>'
     '<li><a href="#onsite"><span class="toc-num">06</span>Anchor to your domain</a></li>'
     '<li><a href="#measure"><span class="toc-num">07</span>The scorecard</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["Reddit","GEO","generative engine optimization","AI citations","Perplexity","off-site authority","B2B SaaS","RAG","AI search"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="The Reddit GEO Playbook: Which Threads AI Actually Cites &middot; rawmktg."
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

  var dc=document.getElementById('rpDiscovery');
  if(dc){new Chart(dc,{type:'bar',data:{labels:['Reddit','Review directories (G2, Capterra, TrustRadius)'],datasets:[{data:[30.9,4.0],backgroundColor:[signal,neutral],borderRadius:4,barThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of discovery-prompt citations';}}}},
      scales:{x:{beginAtZero:true,max:35,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var en=document.getElementById('rpEngines');
  if(en){var ev=[46.7,21.0,11.3,9.0,0.1];var ec=[signal,signal,signal,neutral,neutral];
    new Chart(en,{type:'bar',data:{labels:['Perplexity','Google AI Overviews','ChatGPT','Google AI Mode','Gemini'],datasets:[{data:ev,backgroundColor:ec,borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of top-10 citations are Reddit';}}}},
      scales:{x:{beginAtZero:true,max:50,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var fm=document.getElementById('rpFormats');
  if(fm){new Chart(fm,{type:'bar',data:{labels:['Q&A (question title)','Comparison (X vs Y)','Discussion','Other (links, media)'],datasets:[{data:[50,25,15,10],backgroundColor:[signal,rgba(signal,0.6),neutral,rgba(faint,0.25)],borderRadius:4,barThickness:22}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of Reddit citations';}}}},
      scales:{x:{beginAtZero:true,max:55,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Content &amp; Authority &middot; Off-Site</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Jun 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/reddit_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/reddit_cb.js"],capture_output=True,text=True)
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC SLOPE:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),
 "| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| compare:",hh.count('class="compare-grid"'),"| pipeline:",hh.count('class="pipeline"'),"| code:",hh.count('class="code-block"'),"| callout:",hh.count('class="callout-box"'),"| statgrid:",hh.count('class="stat-grid"'),"| listitem:",hh.count('role="listitem"'))
