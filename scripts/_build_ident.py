#!/usr/bin/env python3
"""SCRATCH: build blogs/authority-isnt-demand.html (identity cohort teardown). Do NOT commit."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="authority-isnt-demand"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-07-09"
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
        rowcls=""; cells=r
        if isinstance(r,tuple) and len(r)==2 and r[0]=="__hl__": rowcls=' class="now-row"'; cells=r[1]
        tds=""
        for j,c in enumerate(cells):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr{rowcls}>{tds}</tr>"
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
def code(label,lang,lines):
    return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><span class="code-lang">{esc(lang)}</span><pre>'+"\n".join(lines)+'</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Authority Isn't Demand"
DECK="Eight identity companies, Okta to Cognito, fight for the same buyers on Google and inside AI answers. Who built a demand engine, who is renting traffic, and who is about to be re-sorted by AI search."
DESC=("A data-backed teardown of the B2B identity cohort (Okta, Auth0, Ping, WorkOS, Stytch, Frontegg, Descope, AWS Cognito): why an "
      "82x traffic gap and DR-75 authority still leave Descope with almost no buyer demand, why AI tools name MojoAuth and LoginRadius "
      "over Okta, and the demand engine that turns authority into pipeline.")
DATANOTE=("A category teardown of eight B2B identity vendors, built from Ahrefs Site Explorer (organic, paid and backlink data, pulled "
          "9 July 2026) and a 40-prompt AI visibility scan across ChatGPT, Google AI, Claude and Gemini. Traffic and spend figures are "
          "estimates and move over time; the pattern, not the decimal, is the point.")

out=[]
out.append('<p class="lead">'+norm("Customer identity is one of the most instructive categories in B2B software right now. It sits at the crossroads of two audiences that rarely overlap: developers who integrate authentication in an afternoon, and security and IT leaders who sign the enterprise contract. It has decades-old incumbents and venture-backed challengers fighting in the same search results, and it is being reshaped, in real time, by the shift from Google to AI answers.")+'</p>')
out.append(p("We pulled organic, paid and backlink data for eight players on 9 July 2026, the incumbents Okta, Auth0 (now owned by Okta) and Ping Identity; the developer-first challengers Stytch, WorkOS, Frontegg and Descope; and the platform-embedded outlier, AWS Cognito, then ran a 40-question AI visibility scan across ChatGPT, Google AI, Claude and Gemini. The picture that emerges is not big versus small. It is about who has built a demand engine, who is renting traffic, and who is about to be caught out by the next platform shift."))

# 01
out.append(sec("01","scoreboard","Who wins the identity search war?","Okta owns authority; WorkOS owns buyer intent; Descope and Cognito have authority but almost no demand.",
  "Free visits is estimated organic traffic. Top-3 terms is the count of search terms where a site holds one of the first three positions. Traffic value is what those visits would cost through ads, a fair proxy for commercial weight."))
out.append(table("The cohort scoreboard, monthly (Ahrefs, 9 Jul 2026)",["Company","Trust (DR)","Free visits","Top-3 terms","Traffic value","Ad spend"],[
 ("__hl__",("Okta [incumbent]","91","1,579,900","15,440","~$1.65M","~$133,800")),
 ("__hl__",("Auth0 [incumbent]","90","430,900","4,954","~$285,000","~$59,400")),
 ("__hl__",("Ping Identity [incumbent]","82","137,900","2,535","~$202,000","~$26,300")),
 ("Frontegg [challenger]","71","37,800","572","~$65,700","~$5,500"),
 ("Stytch [challenger]","74","37,200","410","~$22,600","$0"),
 ("WorkOS [challenger]","82","32,300","1,083","~$62,400","~$15,100"),
 ("Descope [challenger]","75","19,300","448","~$19,300","~$2,100"),
 ("AWS Cognito [embedded]","~96","17,400","72","~$17,000","$0"),
], cls=lambda j,c:"label" if j==0 else ("mute" if j==5 else "")))
out.append(p("Three things jump out. The gap between incumbents and everyone else is enormous, Okta alone pulls more free traffic than the other seven combined, several times over. Trust score does not decide the race among challengers: Descope (75) outscores Stytch (74) and Frontegg (71), yet earns the least buyer traffic of the three. And ad spend does not track with size."))
out.append(chart("identScatter",320,"Figure 1 - link authority (trust score) against monthly free visits, log scale. Okta and Auth0 sit top-right, strong on both. Descope and Cognito sit bottom-right: real authority, almost no buyer traffic. That quadrant is where stored potential goes to waste."))
out.append(pull("The clearest divide in the cohort is not big versus small. It is authority versus demand, and they are not the same thing."))

# 02
out.append(sec("02","teardown","What does each company do well, and not?","Auth0 owns the language; WorkOS owns buyer intent; Descope and Cognito banked authority they never converted.",
  "The cohort splits into distinct playbooks. Some own the vocabulary, some own the commercial phrases, and some have authority with no buyer-facing pages to spend it on."))
out.append(h3("Okta and Ping: the incumbents who own the shelf"))
out.append(p("Okta is the category's gravity well, 1.5 million-plus free visits a month and over 15,000 top-three terms, built over a decade across every identity topic a buyer could search. It owns the enterprise vocabulary: single sign-on, lifecycle management, zero trust. Ping plays a similar game one tier down on compliance-heavy terms. The weakness is inertia: incumbent content is broad but dated, and it ranks on accumulated authority, not because it is the clearest answer, which matters more now that AI answer engines reward the plainest answer, not the oldest, most-linked page. Okta's acquisition of Auth0 is a tell, it bought the developer demand engine it could not build organically."))
out.append(h3("Auth0: the content engine everyone should study"))
out.append(p("If you study one company here, make it Auth0: 11,000-plus ranking terms, nearly 5,000 in the top three, 430,000-plus free visits a month, all on developer education that compounds. It did not win by writing about Auth0, it won by owning the language of the category, what a JWT is, how OAuth works, what a magic link does, and built tools developers link to reflexively (nearly 34,000 referring domains from the real developer web). The move that built the moat is almost embarrassingly simple: take the concept every developer has to learn, and publish the clearest explanation on the internet."))
out.append(code("The page that anchors thousands of searches","jwt",[
 '<span class="cm">// A JSON Web Token is three base64 parts joined by dots:</span>',
 'header.payload.signature',
 '',
 '<span class="cm">// Decoded payload of a login token:</span>',
 '{',
 '  <span class="st">"sub"</span>: <span class="st">"user_8f3a9c"</span>,       <span class="cm">// who the user is</span>',
 '  <span class="st">"iss"</span>: <span class="st">"https://auth.acme.com"</span>,  <span class="cm">// who issued it</span>',
 '  <span class="st">"iat"</span>: <span class="kw">1752000000</span>,           <span class="cm">// issued-at</span>',
 '  <span class="st">"exp"</span>: <span class="kw">1752003600</span>            <span class="cm">// expires in one hour</span>',
 '}',
]))
out.append(p("Every developer who learns the concept on Auth0's page arrives at the buying decision already inside Auth0's frame. Educational content is not a cost center, it is a moat, the "+L("definitional library","/blogs/internal-linking-for-ai-retrieval")+" that wins citations. The risk now is the same one facing all the incumbents: much of that library was built for Google's ten blue links, not for an AI box that summarizes the concept without ever sending the click."))
out.append(h3("Stytch and WorkOS: the efficient challengers"))
out.append(p("Stytch and WorkOS are the clearest proof that focus beats volume. Stytch ranks for barely 1,000 terms yet earns 37,000 free visits a month on $0 of ads. WorkOS is sharper on commercial intent: of its ~2,000 ranking terms, more than half sit in the top three, a hit rate the incumbents cannot match, and it owns buyer phrases like \"sso provider\" at position one."))
out.append(chart("identTop3",240,"Figure 2 - top-3 hit rate: the share of a site's ranking terms that reach Google's top 3. WorkOS turns a small footprint into the highest quality-of-ranking in the cohort; Descope and Frontegg rank broad but shallow."))
out.append(p("The tradeoff is ceiling: a tightly focused footprint captures buyers who already know what they want but does less to create demand among developers still learning. The strongest position would combine WorkOS-style commercial discipline with an Auth0-style education layer. Right now, no challenger has both."))
out.append(h3("Frontegg and Descope: strong products, unfinished demand engines"))
out.append(p("Both have genuinely good products and healthy authority, yet neither has converted it into buyer-facing search presence. Descope is the sharpest example of the trap, "+L("the authority paradox","/blogs/property-vista-authority-paradox")+": a trust score of 75, higher than Stytch and Frontegg, but the least buyer traffic in the group. The reason is instructive, its single largest source of free traffic is a blog post about Claude versus ChatGPT, a topic with nothing to do with buying identity software."))
out.append(chart("identDescope",210,"Figure 3 - where Descope's visits actually come from. Nearly a third arrive from one off-topic \"claude vs chatgpt\" post; the high-intent buyer terms (sso, ciam) bring almost none."))
out.append(p("The authority is real; the buyer pages that would turn it into pipeline have not been built. This is the most common failure mode in B2B: mistaking traffic for demand, a visit from someone comparing chatbots is not a lead. Descope's paid strategy shows the same half-built pattern: it spends ~$2,100/month bidding on rival brand names with a clean \"try Descope instead\" message, but points those ads at a thin destination while the same terms sit wide open on free search where it ranks near zero. Conquest advertising only pays off when a strong comparison page and organic presence sit behind it."))
out.append(h3("AWS Cognito: distribution without a demand engine"))
out.append(p("Cognito ranks for ~125 terms and publishes almost no marketing content, yet still pulls 17,000 visits a month because it rides one of the highest-authority domains on the internet and shows up wherever a developer already lives inside AWS. Distribution, not marketing, does the work, until the AI scan exposes the ceiling. When buyers ask an AI tool which platform to choose, Cognito is largely absent, because it has published nothing to be cited. A distribution moat wins acquisition; it does not win preference."))

# 03
out.append(sec("03","reshuffle","How does AI search reshuffle the cohort?","It scrambles the Google hierarchy: AI names MojoAuth and LoginRadius over Okta, rewarding the clearest answer.",
  "The most forward-looking finding has nothing to do with Google rankings. Across 40 buyer questions on four engines, the brands the AI tools named most were not only the incumbents, smaller, sharper vendors appeared again and again, the same split behind "+L("why the Google leader is not the AI leader","/blogs/winning-google-isnt-winning-ai")+"."))
out.append(chart("identAI",300,"Figure 4 - brands named across the 40-prompt AI scan. MojoAuth, Oloid and LoginRadius are a fraction of Okta's size on Google, yet the AI tools recommend them more often. AI answers do not rank by domain authority."))
out.append(p("The pattern within a single brand makes the point concrete. Descope showed up in AI answers only where it had published direct, comparison-style content, and vanished everywhere else."))
out.append(table("Descope's AI visibility by buyer question type (out of 5 prompts each)",["Buyer question type","Appeared","Why"],[
 ("Pricing & packaging","40%","Its best topic; appeared for \"best passwordless login\""),
 ("Alternatives to vendors","20%","Appeared for \"alternatives to Auth0\""),
 ("Implementation / setup","20%","Appeared for \"integrating magic links\""),
 ("Proof & credibility","20%","One review-style mention"),
 ("Comparisons (X vs Y)","0%","No compare page for AI to lift"),
 ("Security & compliance","0%","A core buyer worry, absent"),
 ("Integrations / workflow fit","0%","Nothing published to cite"),
 ("Which tool to pick","0%","The final question; others named every time"),
], cls=lambda j,c:"label" if j==0 else ("up" if j==1 and c=="40%" else ("neg" if j==1 and c=="0%" else ("mid" if j==1 else "")))))
out.append(h3("How an AI engine decides who to cite"))
out.append(pipeline([("Buyer asks","best passwordless auth?"),("Engine retrieves","candidate pages, live web"),("Ranks by clarity","direct, answer-shaped text"),("Synthesizes","one answer, names a few"),("Cites the brand","clearest page wins")],4,
  "Domain authority barely enters at step 3. What matters is whether your page states the answer plainly enough for the model to quote it, which is why a DR-40 vendor can beat a DR-90 incumbent in an AI answer."))
out.append(h3("What answer-shaped content actually looks like"))
out.append(p("Pages should be built to be quoted, the "+L("anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page")+". Two moves do most of the work. First, lead each key page with the question as a heading and a tight, 40-to-60 word direct answer the model can lift verbatim."))
out.append(code("Lead with a liftable answer","html",[
 '<span class="kw">&lt;h2&gt;</span>What is an authentication service?<span class="kw">&lt;/h2&gt;</span>',
 '<span class="kw">&lt;p</span> <span class="st">class="answer"</span><span class="kw">&gt;</span>',
 '  An authentication service verifies that users are who they',
 '  claim to be, then issues a secure token their apps can trust.',
 '  It handles login, multi-factor, sessions, and social or SSO',
 '  sign-in, so teams do not build and maintain that themselves.',
 '<span class="kw">&lt;/p&gt;</span>',
]))
out.append(p("Second, wrap the page in "+L("structured data","/blogs/schema-markup-ai-citations-2026")+" so machines can parse the question-and-answer pairs without guessing. A small block of FAQ schema turns an ordinary page into a clean, citable source."))
out.append(code("FAQ schema makes a page citable","json-ld",[
 '{',
 '  <span class="st">"@context"</span>: <span class="st">"https://schema.org"</span>,',
 '  <span class="st">"@type"</span>: <span class="st">"FAQPage"</span>,',
 '  <span class="st">"mainEntity"</span>: [{',
 '    <span class="st">"@type"</span>: <span class="st">"Question"</span>,',
 '    <span class="st">"name"</span>: <span class="st">"How much does a passwordless auth platform cost?"</span>,',
 '    <span class="st">"acceptedAnswer"</span>: {',
 '      <span class="st">"@type"</span>: <span class="st">"Answer"</span>,',
 '      <span class="st">"text"</span>: <span class="st">"Priced per monthly active user, with a free tier to ~7,500 MAUs and paid plans from ~$0.02 to $0.05 per MAU beyond that."</span>',
 '    }',
 '  }]',
 '}',
]))
out.append(callout("The strategic window",[
 "For fifteen years, domain authority protected incumbents and made challenger content a slow, uphill grind. AI answers weaken that protection. A challenger that builds a disciplined library of clear comparison, pricing and security pages can be cited next to companies fifty times its size. The brands that recognize this in 2026 will look prescient in 2028.",
]))

# 04
out.append(sec("04","engine","What does the B2B demand engine look like?","One loop: own the language, build buyer pages, earn links, get AI-cited, and pipeline follows.",
  "Every company that wins this cohort runs some version of the same loop. The strivers are missing one or more links in it."))
out.append(pipeline([("Own the language","definitive explainers"),("Build buyer pages","category, pricing, vs"),("Earn real links","dev tools, data reports"),("Get AI-cited","answer-shaped pages"),("Pipeline","buyers in your frame")],4,
  "Where each sits: Auth0 nails 1 and 3; WorkOS nails 2; Descope and Frontegg have the authority for 3 but skipped 2, so the engine never turns over; Cognito relies on distribution and runs none of it."))
out.append(p("If you are the challenger reading this, the sequence matters as much as the parts. Fix the foundation first, then buyer pages, then trust, and you turn authority into demand inside a single quarter."))
out.append(table("The same engine, as a build order",["Step","Window","The work"],[
 ("1, Fix the foundation","Weeks 1-4","Clear the technical debt that blocks crawling and AI parsing: hidden pages, heavy assets, missing structured data, thin titles."),
 ("2, Ship buyer pages","Weeks 2-8","Build the category, pricing, alternatives and \"vs\" pages rivals already rank for. The step Descope and Frontegg skipped."),
 ("3, Make pages answer-shaped","Weeks 2-8","Lead with the question and a liftable answer, add FAQ schema, keep prose clean. This is what gets you AI-cited."),
 ("4, Earn expertise links","Weeks 6-12","Publish one flagship data report and a developer tool worth linking to. Lifts rank, backlinks and citations at once."),
 ("5, Measure demand, not traffic","Ongoing","Track buyer-intent rankings, AI mention rate and pipeline separately from vanity traffic. Re-run the scan quarterly."),
], cls=lambda j,c:"label" if j==0 else ""))

# 05
out.append(sec("05","lessons","What are the seven lessons for any B2B company?","Authority is table stakes; measure buyer traffic; own the language; focus beats breadth; treat AI as a reset.",
  "Strip away the identity specifics and this cohort teaches a set of lessons that apply to any B2B company competing for demand."))
out.append(table("Seven lessons",["#","Lesson","Why"],[
 ("1","Authority is table stakes, not a strategy","A strong trust score earns the right to compete, nothing more. Descope outranks peers on authority and still earns the least buyer traffic."),
 ("2","Measure buyer traffic, not total traffic","The most dangerous number in a dashboard is a big traffic figure made of the wrong visits. Segment by intent and judge each separately."),
 ("3","Own the language of your category","Auth0 built its position by teaching the concepts buyers search before they look for a vendor. Write the definitive page on each."),
 ("4","Focus beats breadth on a challenger budget","WorkOS holds half its terms in the top three by targeting commercial phrases with discipline. If you cannot outspend, out-focus."),
 ("5","Paid and organic must work as one system","Descope pays for rival-brand clicks that land on thin pages while the same terms sit unclaimed on free search. Build the page, then own it."),
 ("6","Distribution wins acquisition, not preference","Cognito's default-in-AWS advantage carries it until the buyer starts comparing, then absence from AI answers costs the deal."),
 ("7","Treat AI answers as a reset, and move first","AI rewards the clearest answer, not the biggest domain. A structured library written to be quoted gets cited beside far larger companies."),
], cls=lambda j,c:"label" if j==1 else ""))
out.append(pull("Authority is earned, demand is built, and the clearest answer, not the oldest one, is what gets chosen."))
out.append(callout("The bottom line",[
 "The identity cohort is not a story about who has the most links. It is about who has turned authority into demand, and who is about to be re-sorted by AI. Okta and Auth0 built demand engines that still lead but were designed for a search era that is ending. Stytch and WorkOS prove focus and clarity can beat scale. Descope, Frontegg and Cognito each have a real asset they have not yet converted into a buyer-facing presence.",
]))
out.append(callout("Method & data",[
 "Organic, paid and backlink metrics from Ahrefs Site Explorer (subdomains mode), pulled 9 July 2026; AWS Cognito measured at the aws.amazon.com/cognito path, its trust score inherited from the wider Amazon domain. AI visibility from a 40-prompt scan across ChatGPT, Google AI, Claude and Gemini. Traffic and spend figures are estimates and will move over time.",
]))

FAQ=[
 ("Why does Descope get so little buyer traffic despite high authority?","Because authority and demand are different things. Descope carries a DR of 75, higher than Stytch (74) and Frontegg (71), but earns the least buyer traffic of the three because it never built the buyer-intent pages, category, pricing, alternatives and \"vs\" pages, that turn authority into pipeline. Nearly a third of its free visits come from one off-topic \"claude vs chatgpt\" blog post, while high-intent terms like sso and ciam bring almost none. The authority is real; the demand engine is unfinished."),
 ("Which identity vendors do AI tools recommend most?","Across a 40-prompt scan of ChatGPT, Google AI, Claude and Gemini, the most-named identity vendors were MojoAuth (37), Oloid (24) and LoginRadius (22), all a fraction of Okta's size on Google, followed by ScaleKit (15), Ping Identity (14), FusionAuth and WorkOS (13 each), Stytch (12) and Okta (11). AI answers do not rank by domain authority; they reward the clearest, most structured answer to the exact question asked."),
 ("How can a challenger brand beat an incumbent in AI answers?","By writing the clearest, most structured answer to the specific question a buyer asks. AI engines barely weigh domain authority when they pick who to cite, they retrieve candidate pages, rank by clarity, and quote the page that states the answer plainly. A DR-40 vendor with a disciplined library of comparison, pricing and security pages (each leading with a 40-60 word direct answer and FAQ schema) can be cited beside a DR-90 incumbent. That window is open in most B2B categories right now."),
 ("What makes content 'answer-shaped' for AI?","Two moves. First, lead each key page with the buyer's question as a heading and a tight, 40-to-60 word self-contained answer the model can lift verbatim, before any narrative. Second, wrap the page in FAQ or Article schema so machines can parse the question-and-answer pairs without guessing. Together they turn a page an AI ignores into one an AI quotes with your name attached."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Data source: Ahrefs Site Explorer (organic, paid, referring domains) plus a 40-prompt AI visibility scan across ChatGPT, Google AI, Claude and Gemini for eight identity vendors, captured 9 July 2026.</p></div>')

body="\n".join(out)

SIDEBAR=[("82x","Free-traffic gap between Okta and Descope"),("54%","Of WorkOS terms rank in Google's top 3"),("5/40","Buyer questions where AI names Descope")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#scoreboard"><span class="toc-num">01</span>The scoreboard</a></li>'
     '<li><a href="#teardown"><span class="toc-num">02</span>Each company, torn down</a></li>'
     '<li><a href="#reshuffle"><span class="toc-num">03</span>The AI reshuffle</a></li>'
     '<li><a href="#engine"><span class="toc-num">04</span>The demand engine</a></li>'
     '<li><a href="#lessons"><span class="toc-num">05</span>Seven lessons</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["identity","authentication","Okta","Auth0","WorkOS","Stytch","Descope","AWS Cognito","GEO","SEO teardown","AI citations","B2B SaaS"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Authority Isn't Demand: The B2B Identity Cohort Teardown &middot; rawmktg."
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

  var sc=document.getElementById('identScatter');
  if(sc){var pts=[{x:91,y:1579900,label:'Okta',c:neutral},{x:90,y:430900,label:'Auth0',c:neutral},{x:82,y:137900,label:'Ping',c:neutral},{x:82,y:32300,label:'WorkOS',c:up},{x:74,y:37200,label:'Stytch',c:up},{x:71,y:37800,label:'Frontegg',c:up},{x:75,y:19300,label:'Descope',c:signal},{x:96,y:17400,label:'Cognito',c:signal}];
    var lp={id:'lpS',afterDatasetsDraw:function(ch){var ctx=ch.ctx;var m=ch.getDatasetMeta(0);m.data.forEach(function(pt,i){var t=pts[i].label;ctx.save();ctx.fillStyle=text;ctx.font='11px '+mono;ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(t,pt.x+9,pt.y);ctx.restore();});}};
    new Chart(sc,{type:'scatter',data:{datasets:[{data:pts,pointBackgroundColor:pts.map(function(p){return p.c;}),pointRadius:7,pointHoverRadius:9}]},
    options:{responsive:true,maintainAspectRatio:false,layout:{padding:{right:60}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.label+': DR '+c.raw.x+', '+c.raw.y.toLocaleString()+' visits';}}}},
      scales:{x:{min:68,max:100,title:{display:true,text:'Link authority (trust score)',color:text,font:{family:mono,size:10}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{type:'logarithmic',title:{display:true,text:'Monthly free visits (log)',color:text,font:{family:mono,size:10}},ticks:{color:text,font:{family:mono,size:9},callback:function(v){return (v>=1e6?(v/1e6)+'M':v>=1e3?(v/1e3)+'k':v);}},grid:{color:grid}}}},plugins:[lp]});}

  function hbar(id,labels,data,colors,max,suffix){var el=document.getElementById(id);if(!el)return;
    new Chart(el,{type:'bar',data:{labels:labels,datasets:[{data:data,backgroundColor:colors,borderRadius:4,barThickness:18}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+(suffix||'');}}}},
      scales:{x:{beginAtZero:true,max:max,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  hbar('identTop3',['WorkOS','Okta','Auth0','Ping Identity','Stytch','Descope','Frontegg'],[54,48,44,41,40,25,22],
    [up,neutral,neutral,neutral,neutral,signal,signal],60,'% of terms in top 3');
  hbar('identDescope',['"claude vs chatgpt"','otp / jwt explainers','"authentication"','"sso" (buyer)','"ciam" (buyer)'],[6000,1300,216,20,20],
    [signal,amber,neutral,rgba(signal,0.6),rgba(signal,0.6)],6500,' monthly visits');
  hbar('identAI',['MojoAuth','Oloid','LoginRadius','ScaleKit','Ping Identity','FusionAuth','WorkOS','Stytch','Okta'],[37,24,22,15,14,13,13,12,11],
    [signal,signal,signal,up,neutral,up,up,up,neutral],40,' of 40 prompts');
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">GEO &amp; SEO Teardown &middot; Identity</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Jul 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/id_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/id_cb.js"],capture_output=True,text=True)
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),
 "| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| pipeline:",hh.count('class="pipeline"'),"| code:",hh.count('class="code-block"'),"| callout:",hh.count('class="callout-box"'),"| listitem:",hh.count('role="listitem"'))
