#!/usr/bin/env python3
"""SCRATCH: build blogs/clean-site-zero-citations.html (Investing & Wealth AI-visibility teardown)."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="clean-site-zero-citations"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-09-01"
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

HEADLINE="Clean Site, Zero Citations"
DECK=("Forty-one companies in the Investing & Wealth cohort were scored against the same 48 buyer questions on the same four AI tools. "
      "Thirty-six came back at zero. The five that showed up carried, on the median, twice the technical debt of the ones that never appeared once.")
DESC=("41 investing and wealth companies scored on ChatGPT, Google AI Overviews, Claude and Gemini: 36 of 41 got zero AI citations, and the five visible ones had twice the site problems of the invisible 36. Why retrieval is a gate not a ranking factor, the empty Alternatives page, and the four numbers to report instead of 'AI visibility'.")
DATANOTE=("Computed from 41 category audits in the Investing & Wealth cohort, collected on 25 August 2026: 7,872 scored AI answers (48 buyer "
          "questions x 4 tools x 41 companies) and 23,870 crawled URLs across 35 live site crawls. With five non-zero outcomes out of 41, every "
          "correlation here is directional, not conclusive; where a number is weak, the piece says so.")

# ---------- formulas ----------
FORM_HHI=r'''Answer Concentration  (HHI-style, top 10)
  = Σ (share_i)²
  = 8² + 6² + 5² + 4² + 3² + 3² + 2² + 2² + 2² + 2²
  = 175

  An even split across fifty domains scores 200 across all fifty.
  Here ten domains alone reach 175. The slot is captured, not crowded.'''

FORM_AS=r'''AS   =  answers naming or linking the brand  /  (questions × tools)

  Answer Share. The base rate. Segment mean 0.46%.'''

FORM_SCI=r'''SCI  =  stages with AS > 0  /  total stages tested

  Stage Coverage Index. Breadth. 0.00 for 36 of 41 companies.'''

FORM_DSP=r'''DSP  =  mean(AS_comparisons, AS_alternatives, AS_pricing, AS_buyer_intent)

  Decision-Stage Presence. The number that predicts revenue.
  Segment mean 0.31%. Non-zero for one of forty-one companies.'''

FORM_CSR=r'''CSR  =  losses with a cited source  /  total losses

  Citable Surface Ratio. Which job you are doing. Segment 0.789.
  The remaining 0.211 is a corroboration problem, not a content one.'''

# ---------- code blocks ----------
CODE_GATES=r'''def probability_of_citation(page, query):
    """
    Three multiplicative gates. Failing any one returns zero.
    Most of this segment fails gate 2, then optimises gate 1.
    """
    # Gate 1, RETRIEVABILITY. Binary. Cheap to fix. Weeks of work.
    if page.blocked_by_robots or page.noindex or page.status != 200:
        return 0.0
    if not page.title or not page.h1:
        return 0.0                       # heavily discounted, treat as fail

    # Gate 2, ANSWER MATCH. Continuous. This is where the segment dies.
    match = semantic_overlap(page.body, query.intent)
    if match < RETRIEVAL_FLOOR:
        return 0.0                       # no page answers this question

    # Gate 3, CORROBORATION. Continuous. Slowest to move.
    trust = f(third_party_mentions, entity_consistency, original_data)
    return match * trust'''

CODE_SCORE=r'''import pandas as pd

DECISION = ["comparisons", "alternatives", "pricing_roi", "buyer_intent"]

def scorecard(answers: pd.DataFrame, losses: pd.DataFrame) -> dict:
    """
    answers: one row per (question, tool) with columns stage, tool, hit (bool)
    losses:  one row per lost question with column cited_source (str or None)
    """
    by_stage = answers.groupby("stage")["hit"].mean()
    return {
        "answer_share": round(answers["hit"].mean(), 4),
        "sci":          round((by_stage > 0).sum() / by_stage.size, 3),
        "dsp":          round(by_stage.reindex(DECISION).fillna(0).mean(), 4),
        "csr":          round(losses["cited_source"].notna().mean(), 3),
        "by_tool":      answers.groupby("tool")["hit"].mean().round(4).to_dict(),
        "empty_stages": sorted(by_stage[by_stage == 0].index.tolist()),
    }'''

CODE_HTML=r'''<article>
  <h1>Best alternatives to [Incumbent] for [specific buyer]</h1>

  <!-- The answer block. Plain, complete, above everything else.
       This is the chunk a retriever lifts. -->
  <p class="answer">
    The main alternatives to [Incumbent] for [buyer] are [A], [B], and [C].
    [A] fits teams that need [X] and starts at $N per month. [B] fits [Y].
    [C] fits [Z]. [Incumbent] remains the better choice when [honest condition].
  </p>

  <h2>Comparison at a glance</h2>
  <table><!-- real numbers, not checkmarks --></table>

  <h2>When [Incumbent] is still the right call</h2>
  ...
</article>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What are the best alternatives to [Incumbent]?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "The main alternatives are [A], [B], and [C]..."
    }
  }]
}
</script>'''

CODE_SHELL=r'''# Gate 1 sanity pass. Run against the buyer-path URL list, not the whole site.
while read -r url; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -L "$url")
  html=$(curl -s -L "$url")
  title=$(grep -o -m1 '<title>[^<]*' <<<"$html" | cut -c8-)
  h1=$(grep -o -m1 '<h1[^>]*>[^<]*' <<<"$html")
  robots=$(grep -o -m1 'name="robots"[^>]*' <<<"$html")
  [[ "$code" != 200         ]] && echo "STATUS  $code  $url"
  [[ -z   "$title"          ]] && echo "NOTITLE       $url"
  [[ -z   "$h1"             ]] && echo "NOH1          $url"
  [[ "$robots" == *noindex* ]] && echo "NOINDEX       $url"
done < buyer-path-urls.txt'''

out=[]; A=out.append

# ===== 01 =====
A(sec("01","dataset","What is this teardown built on?",
      "Forty-one companies in one category, scored against the same 48 buyer questions on four AI tools,",
      "7,872 answers in all, with 35 live site crawls on the same day. Because the question set is shared, the losing and winning sides are measured off one denominator."))
A(p("Between them, the forty-one audits are a single controlled experiment that nobody set out to run. Every audit used the same standardised prompt set for the category: 48 buyer questions, spread across eight buying stages, run on ChatGPT, Google AI Overviews, Claude, and Gemini. That is 192 question-and-tool pairs per company. For each pair, one binary check: was the brand named, or was a page on its domain linked. Either one counts."))
A(p("Thirty-five of the forty-one also carry a live crawl of the production website on the same day: 23,870 URLs in total, checked for the usual retrieval blockers plus content and template defects. This is the same "+L("Investing &amp; Wealth cohort audited for backlinks in the link liability","/blogs/the-link-liability")+", read here through a different lens: what actually wins the AI answer slot."))
A(table("Table 1. The dataset.",["Item","Value"],
  [["Companies audited","41"],["Category","Investing, wealth, and digital-asset infrastructure"],
   ["Buyer questions per company","48"],["AI tools tested","4 (ChatGPT, Google AI Overviews, Claude, Gemini)"],
   ["Answers scored per company","192"],["Total answers scored","7,872"],["Companies with a live site crawl","35"],
   ["URLs crawled in total","23,870"],["Distinct defect classes observed","57 max on a single site, 41 median"],
   ["Data collected","Single day, 25 August 2026"]]))
A(p("Three limits worth stating up front. The prompt set is category-level, not brand-level: it asks the questions a buyer types when they describe a problem rather than a vendor, so these scores are a floor, not a ceiling. It is one day, which catches a distribution, not a trend. And n is 41 with only five non-zero outcomes, so any correlation is directional. Where a number is weak, this piece says so."))

# ===== 02 =====
A(sec("02","zero","How visible is the segment in AI answers?",
      "It is a zero. Thirty-six of forty-one companies were never named or linked in a single one of their 192 answers,",
      "on any tool, for any question, at any stage. Only five appeared at all, and the segment collectively occupies 19% of the slot only by counting every overlap twice."))
A(chart("rankChart",280,"Figure 1. Overall Answer Share by company, all 41 sorted. One company clears 12%; four sit at 1-2%; thirty-six are flat zero."))
A(p("The five exceptions: Range at 12%, then Cryptio, Pulley, and Taxbit at 2%, and Utila at 1%. Add all forty-one together, counting every overlap twice and giving each brand full credit for every answer it appeared in, and the segment collectively occupies 19% of the answer slot."))
A(table("Table 2. The five companies with any presence, by tool.",
  ["Company","Overall","ChatGPT","Google AIO","Claude","Gemini","Stages covered"],
  [["Range","12%","6%","8%","17%","17%","7 of 8"],
   ["Cryptio","2%","4%","2%","0%","0%","3 of 8"],
   ["Pulley","2%","4%","4%","0%","0%","2 of 8"],
   ["Taxbit","2%","2%","2%","2%","2%","1 of 8"],
   ["Utila","1%","0%","2%","0%","0%","1 of 8"]],
  cls=lambda j,c:("num" if j in (1,2,3,4,5) else "")))
A(p("There is a detail most teardowns would skip. Pulley appears twice in this dataset: as one of the forty-one audited companies at 2% visibility, and as a source domain the AI tools quoted against thirty-eight of the other forty. A company can be simultaneously under-cited for its own category and the thing that beats its neighbours. Publishing is not a scoreboard position. It is a supply-side act."))

# ===== 03 =====
A(sec("03","slot","Who actually owns the AI answer slot?",
      "Ten domains take 37% of it across all 7,872 answers, and a third of that is held by trade media, niche publishers, and adjacent vendors",
      "that do not sell what these companies sell. They just have pages that answer the question."))
A(table("Table 3. Who the tools actually return.",["Domain","Share of 192 pairs","What it is"],
  [["fireblocks.com","8%","Category incumbent"],["bitgo.com","6%","Category incumbent"],["cobo.com","5%","Category incumbent"],
   ["anchorage.com","4%","Category incumbent"],["ripple.com","3%","Adjacent infrastructure"],["openfort.io","3%","Adjacent infrastructure"],
   ["finextra.com","2%","Trade media"],["fidelity.com","2%","Incumbent brand, different segment"],
   ["stablecoininsider.org","2%","Niche publisher"],["eco.com","2%","Adjacent vendor"]],
  cls=lambda j,c:("num" if j==1 else "")))
A(chart("domainChart",300,"Figure 2. The ten domains that own the answer slot. Eleven of the thirty-seven concentration points sit on sites that do not compete with the cohort."))
A(code("Formula 1. A concentration measure makes the shape clearer, squaring each domain's share.",FORM_HHI))
A(p("When the audits recorded which specific pages beat the audited brand, the winners were pages like a 'best crypto wallet and custody' blog on cregis.com and a '5 infrastructure bets' post on finextra.com. Blog posts. List pages. Not category-defining assets. The slot is captured by a small set, and mostly by content rather than by product superiority."))

# ===== 04 =====
A(sec("04","inversion","Do cleaner sites get cited more?",
      "No, the opposite. Split the 35 crawled companies into the five that appear in AI answers and the thirty that do not, and on every technical-health measure the visible cohort is worse,",
      "carrying twice the median high-priority problems of the companies that never appear."))
A(chart("inversionChart",260,"Figure 3. Median high-priority site problems: the companies AI cites carry twice the technical debt of the ones it ignores."))
A(table("Table 4. Site health, visible cohort vs invisible cohort.",
  ["Measure (median)","Never appears (n=30)","Appears at all (n=5)"],
  [["High-priority site problems","3","6"],["Distinct defect classes","40.5","50"],["Pages crawled","552","1,032"]],
  cls=lambda j,c:("num" if j in (1,2) else "")))
A(p("Two of the five visible companies sit in the top four messiest sites in the entire sample. Pulley carries 10 high-priority problems across 53 defect classes and still gets quoted. Range carries 7 high-priority problems, 618 images with no alt text, 25 pages set to stay out of search results, and 8 URLs blocked by its own robots file, and it is the most visible brand in the category at 12%. Meanwhile the cleanest site in the sample by high-priority count is Juno, at one problem. Juno's crawl found six URLs. Six. Its AI visibility is zero, because there is essentially nothing there to retrieve."))
A(p("The correlation between high-priority problems and AI visibility is +0.25, and between pages crawled and visibility also +0.25. Both point the wrong way for a hygiene-first model, and neither is significant at n=35 (t = 1.48). Controlling for site size, the partial correlation drops to +0.19 and the effect plausibly collapses into one confound: bigger, older, more published sites accumulate more defects and more citations at the same time. The honest reading is not 'hygiene hurts.' It is that "+L("hygiene does not appear anywhere in the signal","/blogs/ranking-isnt-visibility")+". Thirty companies did the tidy-up and got nothing for it, because tidiness was never the constraint."))

# ===== 05 =====
A(sec("05","why","Why does the clean-site inversion happen?",
      "Because retrieval is a gate, not a ranking factor. It is binary and it comes first, and once a page is through it, cleanliness contributes almost nothing to whether a model quotes it.",
      "A workable model has three gates that multiply. The segment optimises gate 1 and dies at gate 2."))
A(pipeline([("Gate 1: Retrievable","Binary. Robots, noindex, status, title, H1. Cheap. Weeks of work."),
            ("Gate 2: Answer match","Continuous. Does a page answer the question in the shape it was asked? This is where the segment dies."),
            ("Gate 3: Corroborated","Continuous. Third-party mentions, entity consistency, original data. Slowest to move.")],1,
           "Figure 4. Three multiplicative gates. Failing any one returns zero. Most of the cohort passed gate 1 and never built for gate 2."))
A(code("Code 1. The three-gate model as a function. Failing any gate returns zero.",CODE_GATES))
A(p("Gate 1 is what a site crawl measures. It is necessary, it is cheap, and it is the only gate most of these companies have touched. Thirty of the thirty-five crawled sites passed it well enough to be readable and still scored zero, because they failed gate 2. There was no page. "+L("Gate 2 is a supply problem, not a quality problem","/blogs/how-your-page-gets-retrieved")+": it does not ask whether your page is better, it asks whether a page exists that addresses the question in the shape the question was asked. Gate 3 is why fireblocks.com holds 8% and a cleaner site holds nothing. The segment has been optimising a gate it already passed."))

# ===== 06 =====
A(sec("06","stages","Which buying stages is the segment missing?",
      "Almost all of them. Of 328 vendor-stage cells, 314 are empty, and Alternatives is a clean zero:",
      "forty-one companies, four tools, and not one appearance on the single question type a buyer asks immediately before they choose."))
A(chart("emptyChart",240,"Figure 5. 314 of 328 vendor-stage cells are empty. One company covers seven of eight stages; four cover one to three; thirty-six cover none."))
A(table("Table 5. Mean visibility by buying stage, all 41 companies.",
  ["Buying stage","Mean visibility","Companies with any presence","Stage type"],
  [["Best-of / rankings","0.90%","4","Mid"],["Pricing & ROI","0.80%","1","Decision"],["Features & capabilities","0.71%","3","Mid"],
   ["Category discovery","0.39%","3","Early"],["Buyer intent / evaluation","0.32%","1","Decision"],["Integrations & stack","0.20%","1","Mid"],
   ["Comparisons","0.12%","1","Decision"],["Alternatives","0.00%","0","Decision"]],
  cls=lambda j,c:("num" if j in (1,2) else "")))
A(chart("stageChart",280,"Figure 5b. Mean visibility by buying stage across all 41 companies. Alternatives, the last question before a purchase, is a clean zero."))
A(p("'Best alternatives to X' is not a hard page to write. It is a page nobody in this category has written from their own point of view. The tools will answer that question regardless, using somebody else's page. Averaged across the four decision stages, the segment's Decision-Stage Presence is 0.31%, and exactly one company, Range, has a non-zero value."))
A(h3("What the one outlier actually did"))
A(chart("rangeChart",260,"Figure 6. Range's Answer Share by stage. Pricing sits at 33%, more than four times its overall share; Alternatives is zero, like everybody else."))
A(p("Range is the only non-trivial signal available. Its profile is lopsided in a specific way: Pricing & ROI sits at 33%, more than four times its overall Answer Share; Features & capabilities is 17%; Buyer intent is 13%; category discovery, best-of, integrations and comparisons sit at 5% to 8%. The pattern is not 'Range is visible.' It is that Range has a small number of pages that answer cost and capability questions in the words a buyer uses, and those pages get lifted repeatedly. One page type, answered concretely, quoted repeatedly."))
A(p("It is worth saying what Range did not do. It did not clean its site first: seven high-priority problems, 618 images with no alt text, 25 pages deliberately kept out of search, and 8 more blocked in robots. It is the messiest of the visible group by defect class count after Pulley, and four times more visible than anyone else. A company that spent the same quarter clearing those seven problems and published nothing would have moved from zero to zero. This argues for sequencing, not for leaving a site broken."))

# ===== 07 =====
A(sec("07","tools","Do the four AI tools agree?",
      "No, and that breaks single-tool reporting. Range scores 17% on Claude and Gemini but 6% and 8% on ChatGPT and Google AI Overviews;",
      "Cryptio and Pulley are the mirror image. There is no stable ordering of tools in this segment."))
A(chart("toolChart",300,"Figure 7. The five visible companies across all four tools. Three different shapes from five data points."))
A(p("A brand that measures visibility on one tool is measuring one retrieval stack, one index, and one set of grounding rules. Range's number is 6% or 17% depending entirely on which tool you happened to open. "+L("Any dashboard that reports 'our AI visibility' as a single figure","/blogs/share-of-model-measurement")+" without naming the tool and the prompt set is reporting noise. The unit that survives is the tuple: (prompt set, tool, date, binary named-or-linked). Everything above that is aggregation you chose."))

# ===== 08 =====
A(sec("08","nosource","What happens when AI cites no source at all?",
      "One in five losses had no page to beat. In 204 recorded question-and-loss rows, 43 came back with no citable source,",
      "the model answered from parametric memory. That 21% is a corroboration problem, not a content problem, and it needs a different tactic."))
A(chart("sourceChart",260,"Figure 8. Of recorded losses, 78.9% cited a real page you can outrank; 21.1% cited nothing, the model answered from memory."))
A(p("This splits the problem into two jobs. In the 78.9% case a page exists and it beats you: a competitive content problem where you know the URL, can read it, and can publish something better shaped to the question. The winners here were blog posts on cregis.com, finextra.com, blockfills.com, jump.ai, and pulley.com. Reachable."))
A(p("In the 21.1% case no page exists that the model considered worth citing. There is nothing to outrank. Here the lever is not the page. It is whether your brand is present in the corpora that shape the model's priors: "+L("category roundups, trade media, directories, review sites, and other people's writing","/blogs/mentions-beat-links")+". You are competing for the model's unsourced recall. Most content plans in this segment only address the first case, because the first case is the one that shows up in a tool. The second case is invisible until you scan for it, which is the argument for scanning at all."))

# ===== 09 =====
A(sec("09","crawl","What does the crawl data actually say?",
      "That site health is uniform and template-level, not the constraint on visibility. Five template defects accounted for over 12,000 affected pages,",
      "and site size (6 to 1,540 URLs) predicts nothing. Volume without decision-stage coverage is just volume."))
A(table("Table 6. Defect prevalence across 35 crawled sites.",
  ["Defect","Sites affected","Median pages per affected site","Total pages"],
  [["Pages with very little text","83%","9","505"],["Images heavy enough to slow the page","83%","68","3,106"],
   ["Titles cut off in results","80%","49","1,591"],["Titles too long to show in full","80%","47","1,657"],
   ["Broken pages (404 and similar)","77%","2","534"],["Images with no alt text","77%","96","3,951"],
   ["No canonical declared","71%","19","1,779"],["No section headings","71%","14","928"],
   ["Images with no set size","71%","123","5,129"],["Duplicate H1 across pages","69%","10","912"],
   ["Duplicate title across pages","69%","7","588"],["No H1 at all","63%","6","565"],
   ["Points Google to a different page","63%","8","328"],["Duplicate meta description","60%","20","703"]],
  cls=lambda j,c:("num" if j in (1,2,3) else "")))
A(chart("defectChart",320,"Figure 9. Defect prevalence across the 35 crawled sites. Nothing exotic, these are template defaults nobody revisited."))
A(p("Above roughly twenty affected pages per site, the defect is template-level: unsized images, missing alt text, heavy images, truncated titles, duplicate meta descriptions. One change to a layout file clears hundreds of pages at once. Below the line the defects are page-level and small: missing H1s at a median of six pages, broken links at two, insecure pages at two."))
A(p("The exceptions are worth naming because they actually shut a gate. Arta Finance carries 304 pages with no title tag. Transak and Facet carry 191 and 185 broken pages. CoinSwitch blocks 61 URLs in its own robots file. Range sets 25 pages to noindex and blocks 8 more; Facet sets 50 to noindex. Every one of those is a page that can never be quoted, by Google or any AI tool, by the site's own instruction. Gate 1, failed deliberately, usually by accident."))

# ===== 10 =====
A(sec("10","numbers","What four numbers should you report instead?",
      "Answer Share, Stage Coverage Index, Decision-Stage Presence, and Citable Surface Ratio,",
      "each cheap to compute from the audit data and each mapping directly onto a decision. Domain Rating and a single 'AI visibility' percentage are both too blunt to act on."))
A(code("Formula 2. Answer Share (AS), the base rate.",FORM_AS))
A(code("Formula 3. Stage Coverage Index (SCI), breadth.",FORM_SCI))
A(code("Formula 4. Decision-Stage Presence (DSP), the number that predicts revenue.",FORM_DSP))
A(code("Formula 5. Citable Surface Ratio (CSR), which job you are doing.",FORM_CSR))
A(code("Code 2. All four metrics from one answers-and-losses frame. Report them with the prompt set, tool list, and date attached.",CODE_SCORE))
A(table("Table 7. What each number tells you to do.",
  ["Metric","Segment value","If it is low, the fix is"],
  [["Answer Share","0.46% mean","Nothing on its own. Read the other three first."],
   ["Stage Coverage Index","0.00 for 36 of 41","Publish. There is no page to retrieve."],
   ["Decision-Stage Presence","0.31% mean","Alternatives page, comparison page, pricing page with real numbers."],
   ["Citable Surface Ratio","0.789","Below ~0.7, stop writing pages and go earn mentions."]],
  cls=lambda j,c:("num" if j==1 else "")))
A(p("A number without the prompt set, the tool, and the date attached is not comparable to anything, including its own value last quarter. This is the same measurement discipline set out in "+L("the RawMktg methodology","/methodology")+" and the "+L("prompt-to-citation tracking stack","/blogs/prompt-to-citation-tracking")+"."))

# ===== 11 =====
A(sec("11","order","What order does the data argue for?",
      "Clear the retrieval blockers in two weeks because they are cheap, not because they move the number. Then publish the decision pages, Alternatives first,",
      "then earn the outside mention in parallel, then re-measure the same prompts at day 90."))
A(chart("seqChart",300,"Figure 10. The sequence the findings argue for. Gate-1 cleanup is a fortnight; the number comes from the pages that follow."))
A(p("Weeks 1 to 2, clear the retrieval blockers, only the ones that shut gate 1: robots-blocked URLs, noindex on pages that should be indexed, missing titles and H1s, broken pages in the buyer path. Median across the sample is three high-priority problems per site, a fortnight for one engineer. Weeks 2 to 8, publish the decision pages. "+L("Alternatives first, because it is a segment-wide zero and therefore uncontested","/blogs/comparison-pages-ai-shortlists")+"; then a comparison page against the rival sales names first; then a pricing page with real numbers. Weeks 4 to 12, earn the outside mention, in parallel, targeting the trade media and niche publishers already holding the answer slot. Day 90, re-measure the same prompts. The scan is the control, not the report."))
A(p("Here is the page-level pattern the gate-2 work needs. Every decision page carries a direct answer above the marketing copy, and marks itself up so the facts do not have to be inferred, "+L("the shape of a high-citation page","/blogs/anatomy-of-a-high-citation-page")+"."))
A(code("Code 3. The decision-page shape: an answer block above everything, plus FAQ schema so the facts are not inferred.",CODE_HTML))
A(code("Code 4. The gate-1 check, short enough that there is no excuse for it being a quarterly project.",CODE_SHELL))

# ===== 12 =====
A(sec("12","takeaways","What can any segment take from this?",
      "Measure supply before quality, treat a clean site as table stakes rather than a strategy, write the uncontested Alternatives page,",
      "use trade media and niche publishers as a third of the answer slot, and never report AI visibility as one number."))
A('<ul>'
  '<li><strong>Measure supply before you measure quality.</strong> 36 of 41 companies were absent because no page of theirs answered the question, not because their pages were worse. Count how many of your buyer\'s actual questions have a page at all before commissioning a quality review.</li>'
  '<li><strong>A clean site is table stakes, not a strategy.</strong> The five visible companies carried a median of six high-priority problems and got quoted anyway. The three cleanest sites were quoted zero times between them.</li>'
  '<li><strong>The Alternatives page is the cheapest uncontested asset.</strong> Forty-one companies, zero coverage. It has no competition and sits one question away from a purchase.</li>'
  '<li><strong>Trade media and niche publishers are a third of the answer slot.</strong> Not competitors, publishers. A contributed piece or a directory listing puts your name inside the source before the answer is written, and it works on the 21% of questions where nothing is cited.</li>'
  '<li><strong>Never report AI visibility as one number.</strong> Report Answer Share, Stage Coverage Index, Decision-Stage Presence, and Citable Surface Ratio, each with the prompt set, tool, and date. Range is a 6% brand and a 17% brand at the same time.</li>'
  '<li><strong>Fix templates, not pages.</strong> Above roughly twenty affected pages, the defect lives in a layout file. Five template-level defects accounted for over 12,000 affected pages here. Five commits.</li>'
  '</ul>')

# ===== 13 =====
A(sec("13","method","Method and honest limits?",
      "A fixed 48-question category prompt set across eight buying stages, run on four tools and scored binary named-or-linked, 192 pairs per company.",
      "With five non-zero outcomes out of 41, every correlation is directional. The 314-of-328 empty-cell count is not a correlation, it is a count."))
A(p("Site crawls covered every reachable URL on the production domain on the same day, checking status codes, robots directives, canonicals, titles, headings, meta descriptions, images, duplicate content, and readability. Six of the forty-one companies have no crawl in the dataset; cohort comparisons use the 35 that do."))
A(p("What this data cannot tell you: whether visibility converts, because there is no downstream revenue attached; what any score was a month earlier; or whether invisibility is brand-specific or category-level model behaviour, since the prompt set is shared. The hygiene inversion in section 4 is a real pattern in this sample, and it would take a much larger sample to call it a law. The finding that needs no statistics is in section 6: 314 of 328 vendor-stage cells are empty. That is a count."))
A(callout("The one-line version",
  ["Across 41 companies in the Investing &amp; Wealth cohort, 36 are invisible in AI answers because no page of theirs answers the buyer's question, not because their sites are broken. The five that appear are among the messiest. Retrieval is a gate you pass, then stop thinking about; the citations come from the pages you publish after it."]))

# ===== FAQ =====
FAQ=[
 ("Why does a clean, technically healthy website get zero AI citations?",
  "Because technical health is a gate you pass, not a ranking factor. In a study of 41 investing and wealth companies, 30 of 35 crawled sites were clean enough to be readable and still scored zero AI visibility, because no page on them answered the buyer's actual question. Retrieval works in three multiplicative gates: retrievability (robots, noindex, status, title, H1), answer match (does a page address the question in the shape it was asked), and corroboration (third-party mentions). Most of the segment fixed gate 1 and never built for gate 2, so cleanliness contributed nothing to whether a model chose to quote them."),
 ("What is the most common reason a brand is invisible in AI answers?",
  "A supply problem, not a quality problem. Across the cohort, 314 of 328 vendor-stage cells were empty, meaning no page existed that answered the question for that buying stage. The tools answered anyway, using someone else's page. Before you commission a content quality review, count how many of your buyer's actual questions have a page at all, because the constraint is almost always the missing page, not a worse one."),
 ("Why does an Alternatives page matter so much for AI visibility?",
  "Because 'best alternatives to X' is a decision-stage question a buyer asks immediately before choosing, and in this cohort of 41 companies it was a clean zero: not one appeared on it, on any of four tools. The tools answer the question regardless, using a competitor's or a publisher's page. An Alternatives page written from your own point of view, with a plain answer block and real comparison numbers, is the cheapest uncontested asset in most categories and sits one question away from a purchase."),
 ("How should you measure AI visibility instead of a single percentage?",
  "Report four numbers, each with the prompt set, the tool, and the date attached: Answer Share (share of question-and-tool pairs that name or link you), Stage Coverage Index (how many buying stages register any presence), Decision-Stage Presence (mean Answer Share across comparisons, alternatives, pricing and buyer-intent questions), and Citable Surface Ratio (share of losses where a real page was quoted, versus nothing). A single 'AI visibility' figure hides which of these is the actual problem."),
 ("Do ChatGPT, Google AI Overviews, Claude and Gemini agree on which brands to cite?",
  "No. In this cohort the four tools produced three different shapes from five data points: one brand scored 17% on Claude and Gemini but 6% and 8% on ChatGPT and Google AI Overviews, while two others registered only on ChatGPT and Google and were invisible on Claude and Gemini. Each tool is a different retrieval stack, index, and set of grounding rules, so any single-tool 'AI visibility' number is noise unless you name the tool and the prompt set."),
 ("Does fixing technical SEO improve AI visibility?",
  "It removes a blocker, it does not produce visibility. Clearing robots-blocked URLs, noindex on pages that should rank, missing titles and H1s, and broken pages in the buyer path is necessary and cheap, roughly a fortnight of work. But in this sample the correlation between site cleanliness and AI visibility pointed the wrong way: the visible companies carried twice the median high-priority problems of the invisible ones. Fix the retrieval blockers because they are cheap, then publish the decision pages, because the citations come from the pages, not the cleanup."),
 ("What do you do when an AI answer cites no source at all?",
  "Treat it as a corroboration problem, not a content problem. In this dataset 21% of losses had no citable source: the model answered from its own priors with nothing linked. You cannot outrank a page that does not exist, so the lever is presence in the corpora that shape the model's recall, category roundups, trade media, directories, review sites, and other people's writing. That is cheaper than outranking an incumbent and it is the only thing that moves the fifth of questions where nothing is cited."),
]
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
A(faq_html)

# ===== References =====
REFS=[
 ("Generative Engine Optimization. Aggarwal et al., ACM SIGKDD 2024.","https://arxiv.org/abs/2311.09735"),
 ("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Lewis et al.","https://arxiv.org/abs/2005.11401"),
 ("How Google AI Overviews select and link sources. Google Search Central.","https://developers.google.com/search/docs/appearance/ai-features"),
 ("Block or allow AI crawlers: robots.txt and noindex. Google Search Central.","https://developers.google.com/search/docs/crawling-indexing/robots/intro"),
 ("Control what content appears in search with noindex. Google Search Central.","https://developers.google.com/search/docs/crawling-indexing/block-indexing"),
 ("FAQPage structured data reference. Schema.org.","https://schema.org/FAQPage"),
 ("Intro to structured data markup for AI and search. Google Search Central.","https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data"),
 ("How Perplexity retrieves and cites sources. Perplexity Help Center.","https://www.perplexity.ai/hub"),
 ("How ChatGPT search picks and cites web sources. OpenAI.","https://help.openai.com/en/articles/9237897-chatgpt-search"),
 ("Core Web Vitals and page experience signals. Google Search Central.","https://developers.google.com/search/docs/appearance/core-web-vitals"),
 ("Canonicalization and duplicate URLs. Google Search Central.","https://developers.google.com/search/docs/crawling-indexing/canonicalization"),
 ("Answer Engine Optimization: writing for extractable answers. Search Engine Land.","https://searchengineland.com/library/generative-engine-optimization"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
A('<div class="about-block" id="references"><div class="about-label">References</div>'
  '<p style="margin-bottom:16px;">Figures 1 through 10 are original, computed from 41 category audits (7,872 scored AI answers and 23,870 crawled URLs, collected 25 August 2026). The sources below cover the retrieval, schema, and crawl concepts referenced.</p>'
  f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
A('<div class="about-block"><div class="about-label">About rawmktg.</div>'
  '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
  '<p>Sources: 41 category audits in the Investing &amp; Wealth cohort collected 25 August 2026 (7,872 scored answers across ChatGPT, Google AI Overviews, Claude and Gemini; 23,870 crawled URLs across 35 sites). With five non-zero outcomes, correlations are directional, not conclusive.</p></div>')

body="\n".join(out)

SIDEBAR=[("36 of 41","companies never appear in a single AI answer"),
         ("314/328","vendor-stage cells are completely empty"),
         ("0%","of the segment appears on 'Alternatives' questions"),
         ("10 domains","take 37% of the whole answer slot")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#dataset"><span class="toc-num">01</span>What it is built on</a></li>'
     '<li><a href="#zero"><span class="toc-num">02</span>The segment is a zero</a></li>'
     '<li><a href="#slot"><span class="toc-num">03</span>Ten domains own the slot</a></li>'
     '<li><a href="#inversion"><span class="toc-num">04</span>Clean sites, zero citations</a></li>'
     '<li><a href="#why"><span class="toc-num">05</span>Why the inversion happens</a></li>'
     '<li><a href="#stages"><span class="toc-num">06</span>The stages are empty</a></li>'
     '<li><a href="#tools"><span class="toc-num">07</span>The four tools disagree</a></li>'
     '<li><a href="#nosource"><span class="toc-num">08</span>Losses with no source</a></li>'
     '<li><a href="#crawl"><span class="toc-num">09</span>What the crawl says</a></li>'
     '<li><a href="#numbers"><span class="toc-num">10</span>Four numbers to report</a></li>'
     '<li><a href="#order"><span class="toc-num">11</span>The order that works</a></li>'
     '<li><a href="#takeaways"><span class="toc-num">12</span>What any segment can take</a></li>'
     '<li><a href="#method"><span class="toc-num">13</span>Method and limits</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - Investing and Wealth AI visibility teardown - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["AI visibility","generative engine optimization","GEO","AI answer citations","ChatGPT","Google AI Overviews","Claude","Gemini","answer share","alternatives page","retrieval","technical SEO","B2B SaaS","investing and wealth"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Clean Site, Zero Citations: An Investing &amp; Wealth AI-Visibility Teardown &middot; rawmktg."
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
  var neutral=rgba(faint,0.4), amber='#C9922E', blue='#5B8DB8', purple='#8E7CC3';

  var f1=document.getElementById('rankChart');
  if(f1){new Chart(f1,{type:'bar',data:{labels:['Range','Cryptio','Pulley','Taxbit','Utila','36 others'],datasets:[{data:[12,2,2,2,1,0],backgroundColor:[signal,rgba(signal,0.55),rgba(signal,0.55),rgba(signal,0.55),rgba(signal,0.45),neutral],borderRadius:4,barThickness:44}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% Answer Share';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,max:14,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var f2=document.getElementById('domainChart');
  if(f2){new Chart(f2,{type:'bar',data:{labels:['fireblocks.com','bitgo.com','cobo.com','anchorage.com','ripple.com','openfort.io','finextra.com','fidelity.com','stablecoininsider.org','eco.com'],datasets:[{data:[8,6,5,4,3,3,2,2,2,2],backgroundColor:[signal,signal,signal,signal,blue,blue,amber,rgba(signal,0.5),amber,blue],borderRadius:3,barThickness:16}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of answer slot';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}}}}});}

  var f3=document.getElementById('inversionChart');
  if(f3){new Chart(f3,{type:'bar',data:{labels:['Never appears (n=30)','Appears in AI answers (n=5)'],datasets:[{data:[3,6],backgroundColor:[neutral,signal],borderRadius:4,barThickness:70}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' median high-priority problems';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid},title:{display:true,text:'median high-priority site problems',color:text,font:{family:mono,size:9}}}}}});}

  var f5=document.getElementById('emptyChart');
  if(f5){new Chart(f5,{type:'doughnut',data:{labels:['Empty vendor-stage cells','Cells with any presence'],datasets:[{data:[314,14],backgroundColor:[neutral,signal],borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'64%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.label+': '+c.raw+' of 328';}}}}}});}

  var f4=document.getElementById('stageChart');
  if(f4){new Chart(f4,{type:'bar',data:{labels:['Best-of / rankings','Pricing & ROI','Features & capabilities','Category discovery','Buyer intent / evaluation','Integrations & stack','Comparisons','Alternatives'],datasets:[{data:[0.90,0.80,0.71,0.39,0.32,0.20,0.12,0.00],backgroundColor:[rgba(signal,0.7),rgba(signal,0.65),rgba(signal,0.6),rgba(signal,0.5),rgba(signal,0.45),rgba(signal,0.4),rgba(signal,0.35),signal],borderRadius:3,barThickness:18}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.toFixed(2)+'% mean visibility';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}}}}});}

  var fr=document.getElementById('rangeChart');
  if(fr){new Chart(fr,{type:'bar',data:{labels:['Pricing & ROI','Features','Buyer intent','Best-of','Category','Integrations','Comparisons','Alternatives'],datasets:[{data:[33,17,13,8,7,6,5,0],backgroundColor:[signal,rgba(signal,0.7),rgba(signal,0.6),rgba(signal,0.45),rgba(signal,0.45),rgba(signal,0.4),rgba(signal,0.4),neutral],borderRadius:3,barThickness:20}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' Range: '+c.raw+'% on this stage';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:8}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var f7=document.getElementById('toolChart');
  if(f7){new Chart(f7,{type:'bar',data:{labels:['Range','Cryptio','Pulley','Taxbit','Utila'],datasets:[
    {label:'ChatGPT',data:[6,4,4,2,0],backgroundColor:blue,borderRadius:2},
    {label:'Google AIO',data:[8,2,4,2,2],backgroundColor:amber,borderRadius:2},
    {label:'Claude',data:[17,0,0,2,0],backgroundColor:up,borderRadius:2},
    {label:'Gemini',data:[17,0,0,2,0],backgroundColor:purple,borderRadius:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:10}}},tooltip:{mode:'index',intersect:false}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var f8=document.getElementById('sourceChart');
  if(f8){new Chart(f8,{type:'doughnut',data:{labels:['Cited a real page (outrankable)','Cited nothing (corroboration gap)'],datasets:[{data:[78.9,21.1],backgroundColor:[blue,signal],borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.label+': '+c.raw+'%';}}}}}});}

  var f9=document.getElementById('defectChart');
  if(f9){new Chart(f9,{type:'bar',data:{labels:['Very little text','Heavy images','Titles cut off','Titles too long','Broken pages','No alt text','No canonical','No headings','Images no size','Duplicate H1','Duplicate title','No H1','Wrong canonical','Duplicate meta'],datasets:[{data:[83,83,80,80,77,77,71,71,71,69,69,63,63,60],backgroundColor:rgba(signal,0.65),borderRadius:2,barThickness:13}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of sites affected';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:9},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:8}},grid:{color:'transparent'}}}}});}

  var f10=document.getElementById('seqChart');
  if(f10){new Chart(f10,{type:'bar',data:{labels:['Clear retrieval blockers','Publish decision pages','Earn outside mentions','Re-measure same prompts'],datasets:[{label:'start',data:[0,14,28,90],backgroundColor:'transparent'},{label:'duration',data:[14,42,56,4],backgroundColor:[blue,signal,amber,up],borderRadius:4,barThickness:24}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){if(c.datasetIndex===0)return '';var s=c.chart.data.datasets[0].data[c.dataIndex];return ' day '+s+' to '+(s+c.raw);}}}},
      scales:{x:{stacked:true,beginAtZero:true,max:96,title:{display:true,text:'days',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:9}},grid:{color:grid}},y:{stacked:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Industry Teardowns &middot; Investing &amp; Wealth</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Sep 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/csz_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/csz_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| codeblk:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faqitem:",len(re.findall('faq-item',hh)),"| refs:",hh.count('id="references"'),
 "| outlinks:",len(re.findall(r'href="/(blogs|tools|methodology)',hh)))
