#!/usr/bin/env python3
"""SCRATCH: build blogs/winning-google-isnt-winning-ai.html. Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="winning-google-isnt-winning-ai"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-13"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/why-ai-cites-razorpay-over-airpay.html",encoding="utf-8").read()
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
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Winning Google Isn't Winning AI"
DECK="Who AI engines actually cite in the deck-tools race, a teardown of the AI presentation-software market on Google versus inside AI answers."
DESC=("A GEO and SEO teardown of the AI presentation-tools market: why Gamma dominates Google but Canva, Deckary and Beautiful.ai "
      "win AI answers. The split discovery paths, who ranks versus who gets named, why AI cites brands on niche questions (60% for "
      "consulting) but not broad ones (0%), and the authority layer behind both.")
DATANOTE=("A neutral, data-led teardown of how buyers find AI presentation and deck software, and why the Google leaders are not the "
          "leaders inside AI answers. Based on a one-day snapshot of live search data plus 40 real buyer questions across four AI "
          "engines (ChatGPT, Google AI, Claude, Gemini), 160 question-and-engine runs, June 2026. Figures are estimates; AI outputs "
          "vary by run. The point is the pattern, not the decimal place.")

out=[]
out.append('<p class="lead">'+norm("The market for AI tools that build slides and decks has gone from a handful of names to a crowded field in under two years. Gamma, Beautiful.ai, Plus AI, SlideSpeak, Deckary, Canva and consultant-focused tools like Prezent now compete for the same buyers. This teardown looks at how those buyers actually find a tool today, who is winning on Google, who is winning inside AI assistants, and why those are no longer the same question.")+'</p>')
out.append(p("We pulled a one-day snapshot of live search data: the terms buyers use and how hard they are to win, who ranks where on Google, the links each player has earned, and the answers four AI assistants give to 40 real buyer questions. Three patterns stand out: discovery has split in two; the Google leader is not the AI leader; and the niche is winnable."))

# 01
out.append(sec("01","find","How do buyers find a deck tool now?","Two paths feed the same shortlist: the Google results page, and a single AI answer.",
  "For two decades, finding software meant typing into Google and comparing blue links. A second path now sits next to it: buyers ask an assistant a plain-language question and get back a short, ranked answer naming two to five tools."))
out.append(pipeline([("Buyer query","types into Google"),("Page of links","ten blue links"),("Opens several","compares tabs"),("Shortlist","buyer decides")],-1,
  "The Google path: a page of links, and the buyer does the comparing. A tool ranked sixth still gets seen."))
out.append(pipeline([("Asks assistant","plain-language question"),("One answer","names 2-5 tools"),("AI compares","for the buyer"),("Shortlist","named tools only")],1,
  "The AI path: one answer that does the comparing. A tool not in the short list of names is invisible, there is no second page."))
out.append(callout("Why this matters for a category like this one",[
 "Slide and deck tools are a fast, low-commitment purchase. Many buyers sign up for a free trial the same hour they first hear the name. That makes the moment of discovery, the AI answer or the Google result, unusually close to the moment of purchase. Being named is often the whole game.",
]))

# 02
out.append(sec("02","searching","What are buyers searching for?","Large, commercial demand, but the biggest terms are the hardest to win.",
  "Buyers do not just search for ideas, they search for a tool to use right now: \"ai ppt maker\", \"ai presentation maker\", \"pitch deck\". The catch is that the highest-volume terms are also the hardest to rank for, because incumbents already sit at the top."))
out.append(chart("deckDifficulty",300,"Figure 1 - monthly searches against how hard each term is to win on Google. Green is easier, red is harder. The head terms sit top-right, where difficulty is highest."))
out.append(p("The genuinely easy terms are either smaller or are brand and comparison searches like \"canva alternative\". For a newer entrant, the realistic plan is to win a cluster of easier, on-topic terms first, then push at the head terms once the site has earned enough trust."))
out.append(table("Difficulty spread across category search terms (rounded)",["Difficulty band","Share of terms","What it means"],[
 ("Easy (0 to 10)","62%","Mostly long-tail and brand terms. Winnable with focused pages."),
 ("Low to medium (11 to 50)","14%","The sweet spot. Real intent, still reachable."),
 ("Hard (51 to 100)","23%","The head terms. Owned by incumbents, slow to win."),
], cls=lambda j,c:"label" if j==0 else ("up" if j==1 and c.startswith("62") else ("neg" if j==1 and c.startswith("23") else ""))))

# 03
out.append(sec("03","google","Who wins on Google?","Gamma, by a wide margin, by publishing many focused pages and earning the links.",
  "On classic Google search, the category has a clear front-runner. Gamma ranks for far more buyer terms than any rival and sits in the top three for hundreds. Beautiful.ai, SlideSpeak and Plus AI form a chasing pack. Deckary, which barely registers on Google, is the outlier to remember."))
out.append(chart("deckGoogle",260,"Figure 2 - category search terms each player ranks for, in the top 10 and top 3. Gamma ranks for 673 terms (349 in the top 3); Deckary just 62."))
out.append(p("Gamma's lead did not come from a single page. It came from publishing many focused, fast, clearly structured pages, each aimed at one buyer question, and earning the links to back them. That is the textbook way to win Google, and the lesson for challengers is not that Google is closed, it is that Google rewards "+L("depth","/blogs/topical-authority-cluster-ai-shortlists")+", and depth takes time."))
out.append(callout("The takeaway from Google",[
 "Gamma owns the broad \"make a presentation\" terms. A new entrant rarely beats that head-on. The faster route is to win a defensible niche, then expand. Hold that thought, because the AI data points to exactly which niche is open.",
]))

# 04
out.append(sec("04","ai-answers","Who wins inside AI answers?","A different roll call: Canva, Deckary and Beautiful.ai, not Gamma.",
  "We asked four AI assistants 40 real buyer questions, from broad (\"best AI tools for presentations?\") to narrow (\"what helps consultants build pitch decks?\"), and recorded which brands each named. The picture is very different from Google."))
out.append(chart("deckNamed",300,"Figure 3 - how often each brand was named across 160 question-and-assistant runs. Canva leads at 37, with Deckary (36) and Beautiful.ai (35) close behind; Gamma trails at 26."))
out.append(p("Two things jump out. The incumbent Canva is named most, a reminder that AI answers lean on well-known names. And the AI-native tools Deckary and Beautiful.ai are named almost as often, clearly more than Gamma, despite Gamma's Google lead. The order inside AI answers is not the order on Google."))
out.append(h3("Winning Google does not mean winning AI"))
out.append(p("Plot each player's Google footprint against how often AI names them and the divergence is stark."))
out.append(chart("deckDivergence",320,"Figure 4 - Google footprint (across) versus AI reach (up). The two do not line up: Gamma is huge on Google but mid-pack in AI; Deckary is tiny on Google yet named most in AI."))
out.append(p("Gamma sits far to the right, huge on Google, yet only mid-pack in AI. Deckary sits top-left: almost nothing on Google, yet named more than anyone in AI answers. Beautiful.ai is the rare player strong on both. SlideSpeak and Plus AI have a solid Google footprint but a thin AI presence. The signals that win each channel are not the same, the reason "+L("engines recommend different vendors","/blogs/why-engines-recommend-different-vendors")+" than Google ranks."))
out.append(h3("AI names brands on narrow questions, not broad ones"))
out.append(p("The single most useful pattern is where AI cites a real brand at all. On broad questions, assistants give generic advice without backing a specific tool. On narrow, high-intent questions, they cite specific players. Grouping the 40 questions by theme shows it clearly."))
out.append(chart("deckThemes",300,"Figure 5 - share of questions in each theme where an assistant cited a brand's own site. Consulting tools hit 60%; broad \"best tool\", alternatives and pitch-deck questions sit at 0%."))
out.append(p("Questions about consultants and specific industries are where assistants reach for a named tool and a link. Broad \"best AI presentation tool\", \"best alternative\" and \"pitch deck\" questions stay generic. For a challenger, that is the opening: the broad terms are crowded and generic, but the niche, high-intent questions are still up for grabs, exactly where a focused tool can become the named answer."))
out.append(h3("Each assistant sources differently"))
out.append(p("The four assistants do not behave the same way. Google's AI cited brand websites most often, pulling from live pages. Gemini and ChatGPT cited far less, and Claude rarely linked a brand site at all in this set. A tool that wants to be cited has to earn it across several systems, each with its own habits."))
out.append(chart("deckSources",230,"Figure 6 - of 40 questions, how many each assistant backed with a link to a brand's own site. Google AI linked 6; Claude, none."))

# 05
out.append(sec("05","authority","What about links and trust (the authority layer)?","The same quiet engine behind both Google rank and AI citations, and it is uneven here.",
  "Behind both Google rankings and AI citations sits the same engine: trust signals from other websites. Links from respected sites, directory listings, reviews and press all tell engines and AI models that a tool is real and worth recommending."))
out.append(p("The established players sit inside the places buyers and AI models both look: AI tool directories, software review sites and tech media. Newer entrants often show a large raw number of linking sites, but most are low-value auto-generated or "+L("scraper pages","/blogs/cross-border-backlinks")+" that add little trust. The gap that matters is not the count of links, it is the count of links from places that carry weight."))
out.append(table("The link sources that move the needle in this category",["Source type","Why it carries weight","Examples in this space"],[
 ("AI tool directories","Both buyers and AI models pull shortlists from them.","Product Hunt, Toolify, aitools.inc"),
 ("Software review sites","Reviews are a core trust signal for AI answers.","G2, Capterra, software lists"),
 ("Tech media and newsletters","Fresh, cited coverage feeds live AI retrieval.","Substack, Medium, tech newsletters"),
 ("Audience-specific sites","Narrow relevance wins narrow, high-intent answers.","Consulting and industry publications"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(callout("The compounding effect",[
 "These signals stack. A strong directory listing helps Google ranking, which helps AI retrieval, which earns reviews and press, which feed back into both. One well-placed asset, such as an original data report, can lift Google rank, links and AI citations at once. That is why the players who started early keep pulling ahead.",
]))

# 06
out.append(sec("06","decide","How do AI engines decide what to name?","Three layers, each on its own timeline: training, live retrieval, reinforcement.",
  "It helps to know why the AI picture looks the way it does. Three layers decide whether an assistant names a brand, and each moves on its own clock."))
out.append(pipeline([("Training data","what the model learned"),("Live retrieval","fresh pages, fetched now"),("Reinforcement","tuned over time")],1,
  "The three layers behind an AI recommendation. Training is slow but durable; live retrieval is the fastest lever; reinforcement compounds with reviews and citations."))
out.append(p("The practical reading is simple. Classic SEO has not gone away, it feeds all three layers. Fast, clearly structured, well-linked pages are what AI engines retrieve and trust. The work that earns a Google ranking is much of the same work that earns an AI citation. The difference is that AI rewards clarity and "+L("freshness","/blogs/30-day-content-half-life-recency-ai-ranking-signal")+" even more, and it rewards being the obvious answer to a specific question."))

# 07
out.append(sec("07","heading","Where is this heading?","The two channels keep diverging, niches get claimed first, and freshness becomes a moat.",
  "The category is still young and the rules are settling in real time. A few directions look likely from the data."))
out.append(p("<strong>The two channels keep diverging.</strong> Expect more cases where the Google leader and the AI-answer leader are different companies. Tools that treat AI visibility as a separate discipline, not a byproduct of SEO, will pull ahead inside assistants."))
out.append(p("<strong>Niches get claimed first.</strong> Broad terms stay crowded and generic in AI answers. The brands that win specific, high-intent questions, by industry or job role, will be named first and defended longest."))
out.append(p("<strong>Freshness becomes a moat.</strong> Because assistants favor recent, well-structured pages, tools that publish and update steadily will be cited more than those that ship a page and forget it. And when several tools fit a question, reviews, directory presence and credible press tip which one the assistant names."))
out.append(pull("Buyers in this category now ask AI as often as they ask Google, and AI answers a different roll call of names. The brands that understand that difference, and build for it, will own the next phase of the market."))
out.append(callout("Method & data",[
 "A neutral analysis, not an endorsement of any tool. Based on a one-day snapshot of live Google and AI search data, June 2026: category search terms and difficulty, Google rankings, referring domains, and 40 real buyer questions run across four AI engines (ChatGPT, Google AI, Claude, Gemini) for 160 question-and-engine runs. Search volumes and difficulty are estimates; AI outputs vary by run. No tool named here sponsored or reviewed this report.",
]))

FAQ=[
 ("Why is the Google leader not the AI leader for presentation tools?","Because Google ranking and AI citation reward different signals. Gamma wins Google by publishing a huge depth of focused pages (it ranks for 673 category terms, 349 in the top 3), but AI answers lean on well-known names and fresh, narrowly-relevant pages. So Canva (named in 37 of 160 runs), Deckary (36) and Beautiful.ai (35) all out-name Gamma (26) inside AI answers despite Gamma's Google dominance."),
 ("Which AI presentation tool is named most by AI assistants?","Across 160 question-and-engine runs, Canva was named most (37), followed closely by Deckary (36) and Beautiful.ai (35). Gamma, the Google leader, trailed at 26, then Prezent (17), Plus AI and Slideworks (15 each), Presentations.ai (12) and SlideSpeak (8). AI answers favour familiar incumbents and AI-native tools over the pure SEO leader."),
 ("Do AI assistants recommend a specific deck tool, or stay generic?","It depends on the question. On broad questions like \"best AI presentation tool\", \"best alternative\" and \"pitch deck\", assistants cited a named brand's site 0% of the time, they stay generic. On narrow, high-intent questions they cite real brands: 60% of consulting-tool questions and 40% of industry-specific questions backed a named brand. The niche is where AI names a winner."),
 ("How can a new presentation tool get cited by AI?","Win a defensible niche first. Publish fast, clearly structured, answer-shaped pages aimed at specific, high-intent questions (by industry or job role) rather than the crowded broad terms. Earn links from the sources AI models trust, AI tool directories, review sites like G2 and Capterra, and tech media, and keep pages fresh, since live retrieval favours recent content. Deckary did exactly this: tiny on Google, yet named most in AI."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Data source: a one-day snapshot of live Google and AI search data, June 2026, covering category search terms, Google rankings, referring domains, and 40 buyer questions run across ChatGPT, Google AI, Claude and Gemini. Independent analysis; no tool named here sponsored or reviewed it.</p></div>')

body="\n".join(out)

SIDEBAR=[("37","Times Canva, the most-named tool, appears in AI answers"),("0%","Of broad \"best tool\" answers name a brand"),("60%","Of consulting-tool answers cite a named brand")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#find"><span class="toc-num">01</span>How buyers find a tool</a></li>'
     '<li><a href="#searching"><span class="toc-num">02</span>What buyers search for</a></li>'
     '<li><a href="#google"><span class="toc-num">03</span>Who wins on Google</a></li>'
     '<li><a href="#ai-answers"><span class="toc-num">04</span>Who wins inside AI</a></li>'
     '<li><a href="#authority"><span class="toc-num">05</span>Links & trust</a></li>'
     '<li><a href="#decide"><span class="toc-num">06</span>How AI decides</a></li>'
     '<li><a href="#heading"><span class="toc-num">07</span>Where this is heading</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["AI presentation tools","deck software","Gamma","Canva","Deckary","Beautiful.ai","GEO","SEO teardown","AI citations","generative engine optimization"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Winning Google Isn't Winning AI: The AI Presentation-Tools Teardown &middot; rawmktg."
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
  var neutral=rgba(faint,0.45), blue=rgba(faint,0.3);

  // scatter label plugin factory
  function labelPlugin(id){return {id:'lbl_'+id,afterDatasetsDraw:function(ch){var ctx=ch.ctx;ch.data.datasets.forEach(function(ds,di){var meta=ch.getDatasetMeta(di);meta.data.forEach(function(pt,i){var lab=ds.data[i].label;if(!lab)return;ctx.save();ctx.fillStyle=text;ctx.font='11px '+mono;ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(lab,pt.x+10,pt.y);ctx.restore();});});}};}

  // Fig 1: difficulty vs volume scatter
  var dd=document.getElementById('deckDifficulty');
  if(dd){var pts=[{x:5,y:1500,label:'canva alternative',c:up},{x:22,y:2000,label:'ai ppt maker',c:up},{x:54,y:2100,label:'pitch deck',c:amber},{x:81,y:8300,label:'ppt maker ai',c:signal},{x:75,y:2500,label:'ai presentation maker',c:signal},{x:71,y:1100,label:'ai slides',c:signal},{x:78,y:700,label:'ppt generator',c:signal}];
    new Chart(dd,{type:'scatter',data:{datasets:[{data:pts,pointBackgroundColor:pts.map(function(p){return p.c;}),pointRadius:7,pointHoverRadius:9}]},
    options:{responsive:true,maintainAspectRatio:false,layout:{padding:{right:40}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.label+': vol '+c.raw.y+', difficulty '+c.raw.x;}}}},
      scales:{x:{min:0,max:100,title:{display:true,text:'Difficulty to rank (0 easy - 100 hard)',color:text,font:{family:mono,size:10}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{beginAtZero:true,title:{display:true,text:'Monthly searches',color:text,font:{family:mono,size:10}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}},plugins:[labelPlugin('dd')]});}

  // Fig 2: Google footprint grouped bar (top10 / top3)
  var gg=document.getElementById('deckGoogle');
  if(gg){new Chart(gg,{type:'bar',data:{labels:['Gamma','SlideSpeak','Plus AI','Beautiful.ai','Deckary'],
    datasets:[{label:'Top 10 terms',data:[673,277,221,213,62],backgroundColor:blue,borderRadius:3,barPercentage:0.8,categoryPercentage:0.7},
              {label:'Top 3 terms',data:[349,94,63,105,19],backgroundColor:signal,borderRadius:3,barPercentage:0.8,categoryPercentage:0.7}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{color:text,font:{family:mono,size:10},boxWidth:10,boxHeight:10,padding:12}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+': '+c.raw+' terms';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  // Fig 3: AI named horizontal bar
  var nm=document.getElementById('deckNamed');
  if(nm){var lab=['Canva','Deckary','Beautiful.ai','Gamma','Prezent','Plus AI','Slideworks','Presentations.ai','SlideSpeak'];var val=[37,36,35,26,17,15,15,12,8];
    var cols=val.map(function(v,i){return i===0?neutral:(v>=30?signal:(v>=20?up:blue));});
    new Chart(nm,{type:'bar',data:{labels:lab,datasets:[{data:val,backgroundColor:cols,borderRadius:4,barThickness:16}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' named in '+c.raw+' of 160 runs';}}}},
      scales:{x:{beginAtZero:true,max:40,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  // Fig 4: divergence scatter
  var dv=document.getElementById('deckDivergence');
  if(dv){var p2=[{x:62,y:36,label:'Deckary'},{x:213,y:35,label:'Beautiful.ai'},{x:673,y:26,label:'Gamma'},{x:221,y:15,label:'Plus AI'},{x:277,y:8,label:'SlideSpeak'}];
    new Chart(dv,{type:'scatter',data:{datasets:[{data:p2,pointBackgroundColor:signal,pointRadius:8,pointHoverRadius:10}]},
    options:{responsive:true,maintainAspectRatio:false,layout:{padding:{right:50}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.label+': Google '+c.raw.x+', AI '+c.raw.y;}}}},
      scales:{x:{beginAtZero:true,title:{display:true,text:'Google footprint (terms in top 10)',color:text,font:{family:mono,size:10}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{beginAtZero:true,title:{display:true,text:'AI reach (answers naming the brand)',color:text,font:{family:mono,size:10}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}},plugins:[labelPlugin('dv')]});}

  // Fig 5: theme citation share
  var th=document.getElementById('deckThemes');
  if(th){var tl=['Consulting tools','Industry-specific','Slide creation','Enterprise & integration','Learning & how-to','Generic "AI presentation"','Best-tool / alternatives','Pitch decks'];var tv=[60,40,20,20,20,0,0,0];
    var tc=tv.map(function(v){return v>=40?up:(v>=20?amber:signal);});
    new Chart(th,{type:'bar',data:{labels:tl,datasets:[{data:tv,backgroundColor:tc,borderRadius:4,barThickness:16}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% cited a named brand';}}}},
      scales:{x:{beginAtZero:true,max:70,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  // Fig 6: per-assistant brand links
  var sr=document.getElementById('deckSources');
  if(sr){new Chart(sr,{type:'bar',data:{labels:['Google AI','Gemini','ChatGPT','Claude'],datasets:[{data:[6,2,1,0],backgroundColor:[up,blue,blue,signal],borderRadius:4,barThickness:34}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' of 40 questions linked a brand site';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,max:7,ticks:{color:text,font:{family:mono,size:10},stepSize:1},grid:{color:grid}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">GEO &amp; SEO Teardown &middot; Presentation Tools</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Jun 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

# validate chart JS parse with node
import subprocess,re as _re
hh=open(f"blogs/{SLUG}.html").read()
m=_re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, _re.S)
open("/tmp/deck_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/deck_cb.js"],capture_output=True,text=True)
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC SLOPE:",len(_re.findall(r'epic ?slope|epicslope',hh,_re.I)),
 "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| pipelines:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| listitem:",hh.count('role="listitem"'))
