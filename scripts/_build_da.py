#!/usr/bin/env python3
"""SCRATCH: build blogs/why-ai-cites-domo-over-databricks.html. Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="why-ai-cites-domo-over-databricks"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-13"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," "))
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
def h3(idv,t): return f'<h3 id="{idv}">{esc(t)}</h3>'
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
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Why AI Cites Domo Over Databricks"
DECK="The GEO hygiene gap deciding which data-analytics brands AI assistants surface when buyers ask, a six-platform teardown."
DESC=("A GEO and SEO teardown of six data-analytics SaaS platforms (Databricks, Splunk, Domo, Alteryx, Baremetrics, Sisense). "
      "Why a DR-70 brand out-cites a DR-88 one: the six-stage visibility engine, the citation leaderboard, per-brand forensic cards, "
      "and the llms.txt + FAQ-schema combination half the market has skipped.")
DATANOTE=("A competitive GEO/SEO teardown of six data-analytics SaaS brands, synthesizing a master competitive report and six "
          "individual audits. Data: Ahrefs Site Explorer and Brand Radar plus live technical crawl, June 2026. Figures are estimates.")

out=[]
out.append('<p class="lead">'+norm("Six data-analytics platforms, the same six-stage visibility engine, and a result that should reset how you think about authority: Domo, the lowest-authority brand here at DR 70, posts the highest aggregate AI citations, out-citing DR-88 Databricks, which blocks crawlers at the access layer. Authority and AI visibility are correlated but not the same engine, and the gap between them is where the opportunity sits.")+'</p>')
out.append(callout("The divergence that drives this teardown",[
 "Domo, the lowest-DR brand (70), posts the highest aggregate AI citations. Databricks, the highest-traffic brand, under-converts. The cause is GEO hygiene, not authority, and it builds directly on "+L("the authority paradox","/blogs/property-vista-authority-paradox")+" we documented in proptech.",
]))

# 01 engine
out.append(sec("01","engine","How does the visibility engine work?","Six stages gate demand; a failure low in the stack caps everything above.",
  "Every brand here runs the same six-stage engine. Demand is captured only if all six stages hold, which is why a DR-70 brand can out-cite a DR-88 brand that blocks crawlers at the access layer."))
out.append(pipeline([("Access","bot can reach the content"),("Discovery","llms.txt, sitemap, robots"),("Structured data","JSON-LD entity"),("Content","quotable non-branded material"),("Authority","trusted referring domains"),("Citation","surfaced & quoted by AI")],5,
  "Figure 1 - the GEO citation funnel. Each stage gates the next; a brand fails at the first broken link, and access/discovery gate everything above them."))

# 02 scoreboard
out.append(sec("02","scoreboard","What does the category scoreboard show?","Authority and AI-citation share diverge sharply across the six.",
  "Every brand normalized on one row. Traffic value is the monthly PPC-equivalent of organic visits; AI citations sum responses across six engines."))
out.append(table("The category scoreboard",["Company","DR","Traffic/mo","Value/mo","Ref dom","DR70+","Spam","AI cites"],[
 ("Databricks","88","1.3M","$2.3M","31.9K","2.8K","24.8%","629"),
 ("Splunk","91","847K","$1.41M","30.4K","3.2K","22.2%","1,131"),
 ("Domo","70","163K","$292K","14.6K","1.7K","38.4%","1,084"),
 ("Alteryx","79","153K","$363K","20.4K","1.6K","52.8%","139"),
 ("Baremetrics","77","34.8K","$31.2K","4.2K","605","23%","118"),
 ("Sisense","78","28.1K","$42.8K","8.6K","921","43.2%","75"),
], cls=lambda j,c: "label" if j==0 else ("up" if j==7 and c in("1,131","1,084") else "")))
out.append(chart("daCitations",260,"Figure 2 - aggregate AI citations across six engines. Domo and Splunk lead; Databricks is third despite far more traffic. Source: Ahrefs Brand Radar, June 2026"))
out.append(chart("daDR",260,"Figure 3 - Domain Rating benchmark. Domo (signal) is the lowest-authority brand yet leads on citations, the divergence in one chart."))

# 03 brand cards
out.append(sec("03","engines","The six engines, torn down","One forensic card per brand: how it works, what to copy, where to attack.",""))
def stat(d): return table("By the numbers",["DR","Traffic/mo","Value/mo","AI cites","Branded","Spam"],[[d["DR"],d["traffic"],d["value"],d["cites"],d["branded"],d["spam"]]],
  cls=lambda j,c:"")
def brand(idv,name,tag,oneliner,d,content,link,geo,kw,working,playbook,attack):
    o=[h3(idv,f"{name} - {tag}")]
    o.append(p("<strong>The engine.</strong> "+oneliner))
    o.append(stat(d))
    o.append(p("<strong>Content engine.</strong> "+content))
    o.append(p("<strong>Link engine.</strong> "+link))
    o.append(p("<strong>GEO configuration.</strong> "+geo))
    o.append(table("Evidence: top organic keywords",["Keyword","Volume","Traffic","Pos"],kw,cls=lambda j,c:"label" if j==0 else ""))
    o.append(p("<strong>What's working:</strong> "+"; ".join(working)+"."))
    o.append(p("<strong>Playbook, what to copy:</strong> "+"; ".join(playbook)+"."))
    o.append(callout("Attack angle, where to win",[attack]))
    return "\n".join(o)

out.append(brand("databricks","Databricks","Category Leader",
 "A definitional-content flywheel on an enormous, clean backlink base, partly throttled by a hostile WAF.",
 {"DR":"88","traffic":"1.3M","value":"$2.3M","cites":"629","branded":"58.6%","spam":"24.8%"},
 "The deepest definitional library in the set. It owns the canonical 'what is X' queries (data warehouse, vector database, data lake) and pairs them with product-led pages. 41% non-branded across 31.2K keywords, 13.3K in the top three, the exact content shape AI engines summarize.",
 "31.9K referring domains, 2,844 DR70+, at a clean 25% spam ratio. The differentiator is depth in developer ecosystems: GitHub links from over 2,000 pages, a co-citation moat no marketing campaign can fake.",
 "Strong on-page signals but two GEO holes: a WAF that returns 403 to non-browser agents on robots.txt and sitemap.xml, and no fetchable llms.txt. The result is an AI-citation share that under-indexes its traffic dominance.",
 [("databricks","485,660","455,720","1"),("what is a data warehouse","297,290","23,653","4.4"),("what is a vector database","320,000","19,228","4.2"),("machine learning models","161,610","20,221","2.6"),("databricks careers","20,350","16,947","1")],
 ["Definitional 'what is' pages that map 1:1 to AI-answer queries","A developer co-citation moat (2,000+ GitHub linking pages)","The largest, cleanest commercial footprint in the set"],
 ["Build a canonical 'what is X' library for every category concept","Pursue developer-ecosystem links for durable technical authority","Treat certification and community pages as link magnets"],
 "Databricks taxes itself at the access layer. Where it blocks GPTBot/PerplexityBot and skips llms.txt, a fully-open competitor shipping FAQ schema over the same definitional terms can intercept the long-tail AI citations it leaves unconverted. Hard to beat on authority, easy to out-cite on hygiene."))

out.append(brand("splunk","Splunk","Authority Leader",
 "A breadth-of-education content machine on the cleanest, highest-authority link base in the set.",
 {"DR":"91","traffic":"847K","value":"$1.41M","cites":"1,131","branded":"43.5%","spam":"22.2%"},
 "Publishes across the entire security and observability syllabus: risk frameworks, distributed systems, SIEM, hash functions. 56% non-branded, 38.4K keywords with 20.8K in positions 4-10, feeding a long tail of AI eligibility.",
 "The strongest profile here: ~30.4K referring domains, 3,193 DR70+, and the lowest spam exposure at 22%. Authority compounds because the profile stays clean.",
 "Technically the benchmark: valid robots.txt and sitemap, canonical, full Open Graph and Twitter, three JSON-LD blocks including VideoObject. Two blemishes: no llms.txt, and a templating bug leaking a broken hreflang token into the markup.",
 [("splunk","212,030","149,834","1.1"),("risk management frameworks","267,300","35,671","2.8"),("software testing basics","335,540","23,675","28.3"),("what is a distributed system","223,040","14,836","5"),("hash functions","165,490","10,876","5.4")],
 ["Syllabus-wide content covering the whole category vocabulary","The cleanest link base in the set (22% spam)","Benchmark technical hygiene"],
 ["Own the full category glossary, not just bottom-funnel pages","Protect link hygiene as a KPI","Add VideoObject and rich JSON-LD to multiply entity signals"],
 "Splunk is hard to displace on authority; the opening is GEO hygiene. No llms.txt and no FAQ schema over a massive glossary. A challenger that wraps the same definitional content in FAQPage markup and ships llms.txt can win definitional citations before Splunk closes the gap."))

out.append(brand("domo","Domo","GEO Overperformer",
 "A disciplined GEO configuration that converts modest authority into category-leading AI citations.",
 {"DR":"70","traffic":"163K","value":"$292K","cites":"1,084","branded":"31.3%","spam":"38.4%"},
 "Markets directly at the AI-agent buyer ('Governed Data for AI Agents') and ranks across BI terms plus a quirky high-traffic cluster (strip chart). 69% non-branded with a strong 6.6K Top-3 footprint on 12.6K keywords.",
 "14.6K referring domains, 1,686 DR70+, but a 38% spam ratio hinting at historic low-quality accumulation. Authority is the lowest here (DR 70), which makes its citation lead all the more notable.",
 "The reason it over-performs: the richest llms.txt in the set (16KB of curated description), which tracks with category-leading citations (432 Grok, 336 AI Overviews, 302 AI Mode). The irony is broken basic metadata: no canonical, no meta description, only og:type on the homepage, and a sitemap served as application/rss+xml.",
 [("domo","136,440","34,947","2.9"),("domo ai","51,860","9,527","2.5"),("strip chart data","26,000","5,816","1"),("business intelligence tools","261,090","2,233","4"),("strip chart meaning","41,350","5,478","1.3")],
 ["The richest llms.txt in the set, the clearest cause of its over-performance","Buyer-aligned positioning (AI agents, BI category)","A strong Top-3 footprint for a mid-authority domain"],
 ["Copy the llms.txt discipline, the single highest-ROI GEO move","Align positioning to the emerging buyer and build content around it","Use Domo as the internal case study: low DR, high citations"],
 "Do not fight Domo on GEO mechanics; fight it on authority. With only DR 70 and 38% spam, a competitor with cleaner DR70+ links can out-rank it on commercial BI queries while matching its schema discipline. Its broken homepage metadata is a quick credibility wedge."))

out.append(brand("alteryx","Alteryx","Branded-Dependent",
 "A powerful brand-SERP harvester with almost no non-branded discovery engine behind it.",
 {"DR":"79","traffic":"153K","value":"$363K","cites":"139","branded":"73.9%","spam":"52.8%"},
 "74% of traffic is branded (alteryx, certification, community, designer, download). The non-branded layer is thin and softening, a demand-harvesting engine, not a demand-generation one.",
 "Second-largest footprint (20.4K referring domains, 1,555 DR70+) but the worst spam exposure in the set at 53%; more than half its referring domains add risk rather than authority. A disavow program is overdue.",
 "WordPress with full Open Graph and clean headings, but two faults: no llms.txt, and the conventional /sitemap.xml returns 404 (the real index hides at /sitemap_index.xml), so crawlers probing standard paths can miss it.",
 [("alteryx","94,720","75,390","1.2"),("alteryx certification","3,910","3,588","1"),("alteryx community","2,900","2,638","1"),("trifacta","2,080","1,706","1.2"),("alteryx designer","2,780","1,589","1.1")],
 ["Total ownership of its brand SERP","Healthy traffic value ($363K/mo) and full Open Graph","A large raw link footprint to build on once cleaned"],
 ["Treat brand-SERP completeness as table stakes, then layer non-branded content","Use full Open Graph everywhere for rich entity signals"],
 "Alteryx is wide open on non-branded discovery. A competitor publishing strong how-to and comparison content for analytics-automation queries intercepts buyers Alteryx never reaches. Combine that with 53% spam and a missing/locked sitemap, and it is the most structurally exposed enterprise brand in the set."))

out.append(brand("baremetrics","Baremetrics","Niche Content Specialist",
 "A pure editorial content engine that ranks enormous finance terms but lacks the authority to fully cash them in.",
 {"DR":"77","traffic":"34.8K","value":"$31.2K","cites":"118","branded":"4.6%","spam":"23%"},
 "The most content-led model here: 95% non-branded. It ranks for genuinely huge educational terms (churn rate analysis at 263K, what is a burn rate at 180K, MRR, cohort analysis). Editorial depth is real and category-relevant.",
 "The smallest authority base: DR 77 but only 4.2K referring domains, 605 DR70+, at a clean 23% spam. Stripe, Shopify and Medium links lend ecosystem relevance, but the base is too thin to lift it past more authoritative sources.",
 "Clean foundations: valid llms.txt, sitemap, canonical, and JSON-LD including SoftwareApplication. The gap is a missing og:image, so widely-shared finance guides render without a preview card, suppressing the social amplification that builds AI authority.",
 [("churn rate analysis","263,200","10,392","4.3"),("what is a burn rate","180,200","4,856","10.4"),("baremetrics","1,290","1,357","1"),("startup financial modeling","38,000","742","12"),("mrr","37,930","444","8.8")],
 ["The purest content engine: ranks 263K-volume terms on a tiny domain","A clean technical base with llms.txt and commerce schema","Topically relevant ecosystem links (Stripe, Shopify)"],
 ["Target enormous-volume educational terms adjacent to the product","Add FAQ/HowTo schema to calculators and guides","Earn topically-relevant ecosystem links, not just high-DR links"],
 "Baremetrics wins on editorial depth and loses on authority. A competitor with more DR70+ links can out-rank its finance guides on the exact high-volume terms it depends on. Its missing og:image is a free amplification gap to exploit."))

out.append(brand("sisense","Sisense","Contracting Challenger",
 "A decent SQL-tutorial niche engine that is actively decaying because its crawl infrastructure is broken.",
 {"DR":"78","traffic":"28.1K","value":"$42.8K","cites":"75","branded":"28.5%","spam":"43.2%"},
 "Owns a focused SQL-tutorial niche (order of execution in sql, group by in sql, python data analysis) with a 72% non-branded mix. But the footprint is shrinking to just 2.1K keywords, the smallest active library in the set, and traffic is contracting.",
 "8.6K referring domains, 921 DR70+, but a 43% spam ratio (second-worst). DR 78 is respectable; the problem is decay, not raw authority.",
 "Has an llms.txt, but the rest of discovery is broken: /sitemap.xml returns a 301 to an empty 0-byte response, and there is no hreflang. Crawlers cannot enumerate the site, the mechanical reason the keyword footprint is collapsing.",
 [("sisense","9,730","6,944","1.1"),("order of execution in sql","2,880","1,820","1.5"),("python data analysis","92,100","1,051","13.3"),("group by in sql","12,390","616","5.1"),("mtd full form","8,340","814","1.3")],
 ["A focused SQL-tutorial niche with a good non-branded mix","A respectable DR 78 to rebuild from","It has published an llms.txt"],
 ["Even a struggling brand should ship llms.txt, discovery hygiene is cheap insurance","Defend a focused niche rather than spreading thin"],
 "Sisense is the most beatable peer: a declining curve plus a broken sitemap means crawlers cannot index it properly. Consistent publishing on a working crawl stack would overtake it on embedded-analytics queries within two quarters, the lowest-effort share grab in the set."))

# 04 cross-cutting
out.append(sec("04","cross-cutting","What do the cross-cutting patterns reveal?","GEO hygiene predicts citations more than authority, and the best combo is unclaimed.",
  "AI engines select sources, they do not rank pages, and the clearest predictor of selection here is GEO hygiene rather than raw authority. Grok and Google AI Overviews carry most citation volume; Gemini barely cites anyone. The "+L("llms.txt","/glossary/llms-txt")+" divide is the sharpest line in the data: only Domo, Sisense and Baremetrics publish one, and Domo's richest-in-set file tracks with its citation lead."))
out.append(chart("daSpam",260,"Figure 4 - spam exposure by brand. Alteryx (53%) and Sisense (43%) carry the dirtiest profiles, inviting algorithmic discounting."))
out.append(chart("daNonBranded",260,"Figure 5 - non-branded share of traffic. Alteryx harvests existing demand; Baremetrics generates it; Splunk and Databricks own the GEO-optimal definitional middle."))
out.append(p("Two opposite strategies bracket the set. Alteryx (74% branded) harvests existing demand; Baremetrics (95% non-branded) generates demand but cannot fully cash it without authority. The GEO-optimal middle is the "+L("definitional libraries","/blogs/internal-linking-for-ai-retrieval")+" of Splunk and Databricks. Nobody has yet layered FAQPage schema over those glossaries, the single softest spot in the category."))
out.append(table("The technical stack, scored",["Element","Databricks","Splunk","Domo","Alteryx","Baremetrics","Sisense"],[
 ("llms.txt","N","N","Y","N","Y","Y"),
 ("Valid sitemap.xml","~","Y","Y","~","Y","N"),
 ("AI-crawler access","N","Y","Y","Y","Y","Y"),
 ("JSON-LD schema","Y","Y","Y","Y","Y","Y"),
 ("Full Open Graph","Y","Y","N","Y","~","Y"),
 ("Canonical tag","Y","Y","N","Y","Y","Y"),
 ("hreflang","~","~","Y","Y","Y","N"),
 ("Meta description","Y","Y","N","Y","Y","Y"),
], cls=lambda j,c: ("label" if j==0 else ("up" if c=="Y" else ("neg" if c=="N" else "mid")))))
out.append(p("Legend: Y implemented, ~ partial or misconfigured, N missing or blocked. The three highest-leverage fixes across the set: add a canonical and meta description (Domo), allowlist AI crawlers at the WAF (Databricks), and wrap glossaries in FAQPage "+L("schema","/blogs/schema-markup-ai-citations-2026")+" (everyone)."))
out.append(code("High-leverage fixes, copy-paste ready",
"""<!-- 1. Canonical (Domo) -->
<link rel="canonical" href="https://www.example.com/" />

<!-- 2. AI-crawler allowlist in robots.txt (Databricks) -->
User-agent: GPTBot
Allow: /
User-agent: PerplexityBot
Allow: /

<!-- 3. FAQPage schema over glossary (everyone) -->
<script type="application/ld+json">{"@context":"https://schema.org",
 "@type":"FAQPage","mainEntity":[{"@type":"Question", ... }]}</script>""","html"))

# 05 playbook
out.append(sec("05","playbook","What's the synthesized playbook?","Eight reusable plays, ordered by leverage-to-effort.",
  "Pulled from what the leaders do and the gaps the laggards leave."))
out.append(table("The synthesized playbook",["Play","Why it works","Effort"],[
 ("Ship a rich llms.txt","Half the market has none; Domo proves it converts authority into citations","~2h"),
 ("Wrap glossaries in FAQPage schema","No one has done it; it is what engines extract for 'what is' answers","~3h"),
 ("Build a definitional 'what is X' library","Maps 1:1 to AI-answer queries; Splunk and Databricks win this way","Ongoing"),
 ("Allowlist GPTBot / PerplexityBot","Crawler blocking silently caps citation eligibility","~3h"),
 ("Fix canonical + meta + Open Graph","Cheap entity-signal hygiene","~2h"),
 ("Pursue developer-ecosystem links","GitHub/docs co-citation is a durable technical-trust moat","Ongoing"),
 ("Guard link hygiene as a KPI","Clean profiles compound; 22% beats 53% over time","Quarterly"),
 ("Track AI share-of-voice separately from rankings","Authority and citation share diverge","Monthly"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(code("llms.txt, the GEO file half this market is missing",
"""# <Company> - <one-line positioning>
> A concise description of what the company does and who it serves.

## Products
- [Platform](https://example.com/product): overview and core capabilities

## Learn
- [Glossary](https://example.com/glossary): definitions engines can quote
- [Guides](https://example.com/guides): how-to content for category queries""","llms.txt"))

# 06 attack plan
out.append(sec("06","attack","Where's the fastest share? (the attack plan)","Sisense and Alteryx are the cheapest share; Databricks and Splunk are hardest.",
  "Each competitor ranked by how cheaply share can be taken, with the specific weakness and the move that exploits it."))
out.append(table("The attack plan",["Target","Exposed weakness","The move","Ease"],[
 ("Sisense","Broken sitemap, contracting 2.1K-keyword footprint, 43% spam","Publish consistently on a working crawl stack; target SQL/embedded-analytics queries","Easiest"),
 ("Alteryx","74% branded, no llms.txt, sitemap 404s, 53% spam","Own non-branded analytics-automation how-to and comparison content","Easy"),
 ("Baremetrics","Smallest authority base; missing og:image","Out-authority it on the high-volume finance terms it ranks","Moderate"),
 ("Domo","DR 70 (lowest), 38% spam, broken homepage metadata","Out-rank on commercial BI queries with cleaner DR70+ links","Moderate"),
 ("Splunk","No llms.txt, no FAQ schema, broken hreflang","Win definitional security citations with FAQ content + llms.txt","Hard"),
 ("Databricks","WAF blocks crawlers; no llms.txt; under-converts","Be fully crawler-open and FAQ-structured to capture long-tail citations","Hard"),
], cls=lambda j,c:"label" if j==0 else ("up" if c in("Easiest","Easy") else ("neg" if c=="Hard" else ""))))
out.append(callout("Bottom line",[
 "<strong>Easiest share:</strong> Sisense (broken sitemap, contracting) and Alteryx (74% branded, dirtiest links, no llms.txt).",
 "<strong>Hardest to displace:</strong> Databricks and Splunk on authority, but both wide open on GEO hygiene.",
 "<strong>The universal opening:</strong> nobody pairs a definitional glossary with FAQPage schema and llms.txt. That combination is unclaimed, and non-branded definitional content plus flawless crawl infrastructure beats raw authority for AI citations.",
]))

# FAQ
FAQ=[
 ("Why does Domo out-cite Databricks despite far lower authority?","Because AI citation is gated by GEO hygiene, not just Domain Rating. Domo publishes the richest llms.txt in the set (16KB) and markets directly at the AI-agent buyer, while Databricks blocks simple crawlers at its WAF and ships no fetchable llms.txt. Domo (DR 70) posts 1,084 aggregate AI citations versus Databricks' 629 (DR 88), because access and discovery gate everything above them."),
 ("What is the single highest-ROI GEO move for a data-analytics brand?","Ship a rich llms.txt. Only three of the six brands publish one, and Domo's detailed file tracks directly with its citation lead. It is roughly two hours of work and converts existing authority into citations, especially for mid-authority domains that can't win on Domain Rating alone."),
 ("Which brand is the most exposed to competitive attack?","Sisense. Its /sitemap.xml returns a 301 to an empty response so crawlers can't enumerate the site, its keyword footprint is contracting to 2.1K terms, and 43% of its referring domains are spam. Consistent publishing on a working crawl stack could overtake it on embedded-analytics queries within one to two quarters."),
 ("What's the unclaimed opportunity across the whole category?","Pairing a definitional 'what is X' glossary with FAQPage schema and a working llms.txt. The leaders (Splunk, Databricks) own the definitional content but have no FAQ schema or llms.txt; the GEO-disciplined brands (Domo) lack the authority. No one has combined all three, so non-branded definitional content plus flawless crawl infrastructure is the fastest path to AI citations."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Data source: Ahrefs (organic keywords, referring domains, Brand Radar AI citations) plus a live technical crawl of all six domains, captured June 2026.</p></div>')

body="\n".join(out)

SIDEBAR=[("6","Data-analytics SaaS brands torn down"),("3/6","Publish a working llms.txt file"),("DR 70","Lowest authority, #1 in AI citations (Domo)")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#engine"><span class="toc-num">01</span>The visibility engine</a></li>'
     '<li><a href="#scoreboard"><span class="toc-num">02</span>The scoreboard</a></li>'
     '<li><a href="#engines"><span class="toc-num">03</span>The six engines</a></li>'
     '<li><a href="#cross-cutting"><span class="toc-num">04</span>Cross-cutting patterns</a></li>'
     '<li><a href="#playbook"><span class="toc-num">05</span>The playbook</a></li>'
     '<li><a href="#attack"><span class="toc-num">06</span>The attack plan</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["data analytics SaaS","GEO","SEO teardown","AI citations","Domo","Databricks","Splunk","llms.txt","FAQPage schema","domain rating","Ahrefs Brand Radar"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Why AI Cites Domo Over Databricks: A Data-Analytics SaaS GEO Teardown &middot; rawmktg."
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
  var faint=(css.getPropertyValue('--faint')||'#C5BFB4').trim();
  var up=(css.getPropertyValue('--up')||'#3E9B6A').trim();
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.45);
  function hbar(id,labels,data,colors,suffix,max){var e=document.getElementById(id);if(!e)return;
    new Chart(e,{type:'bar',data:{labels:labels,datasets:[{data:data,backgroundColor:colors,borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+(suffix||'');}}}},
      scales:{x:{beginAtZero:true,max:max,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}
  var BR=['Databricks','Splunk','Domo','Alteryx','Baremetrics','Sisense'];
  hbar('daCitations',['Splunk','Domo','Databricks','Alteryx','Baremetrics','Sisense'],[1131,1084,629,139,118,75],[up,up,neutral,neutral,neutral,signal],' AI citations',1200);
  hbar('daDR',BR,[88,91,70,79,77,78],[neutral,neutral,signal,neutral,neutral,neutral],' Domain Rating',100);
  hbar('daSpam',BR,[24.8,22.2,38.4,52.8,23,43.2],[neutral,neutral,neutral,signal,neutral,signal],'% spam referring domains',60);
  hbar('daNonBranded',BR,[41,56,69,26,95,72],[neutral,neutral,up,signal,up,up],'% non-branded traffic',100);
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">GEO &amp; SEO Teardown &middot; 6 Platforms</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">June 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)
hh=open(f"blogs/{SLUG}.html").read()
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
 "| tt:",hh.count('class="tt"'),"| pipelines:",hh.count('class="pipeline"'),"| code:",hh.count("code-block")-1,
 "| callout:",hh.count('class="callout-box"'),"| h3:",hh.count("<h3"),"| listitem:",hh.count('role="listitem"'))
