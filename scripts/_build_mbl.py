#!/usr/bin/env python3
"""SCRATCH: build blogs/mentions-beat-links.html (Digital PR / original research). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="mentions-beat-links"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-08-26"
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

HEADLINE="Digital PR and Data Studies: The Link Play AI Cites"
DECK=("Your own domain accounts for less than a tenth of the sources a generative engine pulls into an answer. Everything else has "
      "to be earned, and the asset that earns it best is the one most teams cut first.")
DESC=("Digital PR for AI search: your domain is under 10% of citation sources. Original research seeded off-site is what generative engines cite. The data, the study spec, distribution, and a 90-day play.")
DATANOTE=("Grounded in the Princeton/Georgia Tech/AI2/IIT Delhi GEO experiment (ACM SIGKDD 2024), an Ahrefs analysis of ~75,000 brands, "
          "McKinsey source-mix data, and 2026 citation benchmarks. Correlations are directional, not causal; magnitudes from mixed bases.")

# ---- formulas (ASCII, bypass norm) ----
FORM_STACK=r'''lift_combined  =  1  -  Π (1 - lift_i)  +  δ_overlap

  lift_i     measured single-strategy delta (e.g. quotes +0.41)
  δ_overlap  negative correction for shared signal
  Two levers at +41% and +31% do NOT stack to +85%. Model ~50%,
  treat anything above as upside.'''

FORM_CSD=r'''CSD  =  ( Σ_{u∈U}  n_u · m_u )  /  (W / 1000)

  U   candidate claim units in the document
  n   1 if the unit carries a precise numeric value
  m   1 if it carries a named methodology or attribution
  W   total word count
  Blog post < 1.   Research hub should clear 4.   Below 2 = an essay with numbers.'''

FORM_ECI=r'''ECI  =  Σ_j  w_j · log(1 + m_j)

  m_j  mention count on domain j
  w_j  retrieval-trust weight for domain j, 0 to 1
  The log is the point: your 4th mention on one site adds little.
  Two mentions across two domains beat four on one. Independence, not volume.'''

FORM_BMS=r'''BMS  =  ( 1 / (P·R) )  Σ_p Σ_r  [ brand ∈ A_{p,r} ]

  P   prompts in the fixed set     R   runs per prompt
  A   answer text for one run
  One run per prompt swings several points for no reason.
  Five runs is a floor. Ten is better. See the methodology.'''

FORM_DARK=r'''hidden_revenue  ≈  D · φ · c · V

  D    unsegmented monthly Direct sessions
  φ    0.706  share of AI referrals with the referrer header stripped
  c    0.1021 observed Dark-AI conversion rate
  V    average order value / annual contract value
  A model, not a measurement. Label it as one in any deck.'''

FORM_CPC=r'''cost_per_point  =  total_campaign_cost  /  Δ brand_mention_share

  Δ in percentage points, same prompt set before and after.
  Looks bad after one study. Reasonable after three.
  That is the asset behaving honestly, not a presentation trick.'''

# ---- code blocks (re-indented) ----
CODE_YAML=r'''# study-spec.yaml  --  write the headline before you write the survey
study:
  title: "B2B Original Research Census 2026"
  entity: "RawMktg"                    # the brand the citation should name
  field_window: "2026-03-01/2026-03-21"

  # Every question maps to one intended stat unit.
  # If a question cannot produce a publishable sentence, cut it.
  targets:
    - id: research_frequency
      headline: "{pct}% of B2B teams run zero original research per year"
      question: "How many original research studies did your team publish in 2025?"
      scale: [0, 1, 2, "3-5", "6+"]
      stat_unit: true
      quote_prompt: "Why did your team publish that number?"   # sources the quote

    - id: budget_share
      headline: "Original research takes {pct}% of median content budget"
      question: "What share of your content budget went to original research?"
      scale: percent
      stat_unit: true
      segment_by: [company_size, acv_band]     # segment cuts = extra stat units

    - id: attribution_confidence
      headline: "Only {pct}% can attribute pipeline to a research asset"
      question: "Can you attribute closed-won pipeline to a research asset?"
      scale: [yes, no, unsure]
      stat_unit: true

  methodology:
    n: 1204
    population: "B2B marketing decision makers, 50-5000 employees"
    sampling: "panel, quota-balanced on company size and region"
    margin_of_error: 2.8          # publish this. models weight verifiable claims.
    weighting: "none"
    raw_data_url: "https://example.com/research/census-2026/data.csv"'''

CODE_SCORE=r'''# score_stat_units.py  --  crude filter, catches most of what ships broken
import re
from dataclasses import dataclass

NUM    = re.compile(r"\b\d+(?:\.\d+)?\s?(?:%|pp|x|bn|m|k)?\b", re.I)
ATTR   = re.compile(r"\b(said|according to|per|told)\b", re.I)
HEDGE  = re.compile(r"\b(many|most|some|often|significant|leading|robust)\b", re.I)
METHOD = re.compile(r"\b(n\s?=|sample|surveyed|fielded|margin of error)\b", re.I)

@dataclass
class Unit:
    text: str

    @property
    def score(self) -> int:
        s = 0
        s += 2 if NUM.search(self.text)    else 0   # precise number
        s += 2 if METHOD.search(self.text) else 0   # verifiable method
        s += 2 if ATTR.search(self.text)   else 0   # named attribution
        s -= 1 if HEDGE.search(self.text)  else 0   # qualitative hedge
        s += 1 if len(self.text.split()) <= 45 else 0   # fits a chunk boundary
        return s

    @property
    def verdict(self) -> str:
        if self.score >= 5: return "CITABLE"
        if self.score >= 3: return "WEAK - add method or attribution"
        return "REWRITE"

def audit(paragraphs):
    units = [Unit(p.strip()) for p in paragraphs if p.strip()]
    citable = [u for u in units if u.score >= 5]
    words = sum(len(u.text.split()) for u in units)
    csd = len(citable) / (words / 1000) if words else 0
    for u in units:
        print(f"{u.score:>2}  {u.verdict:<32} {u.text[:64]}")
    print(f"\nCitable stat density: {csd:.2f} per 1,000 words")
    return csd'''

CODE_BLOCK=r'''## Headline finding
**41% of B2B marketing teams published zero original research in 2025**,
up from 28% in 2024.

Source: RawMktg Original Research Census 2026. n=1,204 B2B marketing
decision makers at companies of 50 to 5,000 employees. Fielded 1 to 21
March 2026. Margin of error +/- 2.8pp at 95% confidence.

## Attributed comment
> "Teams cut research first because it is the only line item with no
> weekly dashboard. The cost shows up eighteen months later as a
> category conversation you are not part of."
>
> Priya Menon, VP Demand Generation, Northwind

## Segment cuts
| Segment          | Zero studies | 3+ studies |
|------------------|--------------|------------|
| Under 200 staff  | 58%          | 6%         |
| 200 to 1,000     | 39%          | 14%        |
| Over 1,000       | 24%          | 31%        |

## Raw data
Full dataset (CSV, CC BY 4.0): https://example.com/research/census-2026/data.csv'''

CODE_JSONLD=r'''{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://example.com/research/census-2026/#article",
      "headline": "41% of B2B teams published zero original research in 2025",
      "datePublished": "2026-04-08",
      "dateModified": "2026-04-08",
      "author": {
        "@type": "Person",
        "name": "Priya Menon",
        "jobTitle": "VP Demand Generation",
        "sameAs": ["https://www.linkedin.com/in/example"]
      },
      "publisher": { "@id": "https://example.com/#org" },
      "about":     { "@id": "https://example.com/research/census-2026/#data" },
      "isBasedOn": { "@id": "https://example.com/research/census-2026/#data" }
    },
    {
      "@type": "Dataset",
      "@id": "https://example.com/research/census-2026/#data",
      "name": "B2B Original Research Census 2026",
      "description": "Survey of 1,204 B2B marketers on original research output",
      "license": "https://creativecommons.org/licenses/by/4.0/",
      "creator": { "@id": "https://example.com/#org" },
      "temporalCoverage": "2026-03-01/2026-03-21",
      "variableMeasured": [
        "studies published per year",
        "share of content budget allocated to research",
        "pipeline attribution confidence"
      ],
      "distribution": [{
        "@type": "DataDownload",
        "encodingFormat": "text/csv",
        "contentUrl": "https://example.com/research/census-2026/data.csv"
      }]
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#org",
      "name": "Example",
      "sameAs": [
        "https://www.wikidata.org/wiki/Q000000",
        "https://www.linkedin.com/company/example",
        "https://www.crunchbase.com/organization/example"
      ]
    }
  ]
}'''

CODE_ROBOTS=r'''# robots.txt
# Live retrieval. Blocking these removes you from real-time AI answers.
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: Googlebot
Allow: /

# Training crawlers. Allow or block on IP strategy, not on GEO strategy.
User-agent: GPTBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://example.com/sitemap.xml'''

CODE_SCAN=r'''# scan_prompt_set.py  --  the cited domains are your outreach list
import json, statistics
from collections import defaultdict

PROMPTS = [
    "best container tracking software for freight forwarders",
    "how do freight forwarders track ocean containers",
    "terminal49 vs project44",
    "container visibility platforms compared",
]
BRAND       = "example"
COMPETITORS = ["rival-one", "rival-two"]
RUNS        = 8

def scan(client, prompt, runs=RUNS):
    """Return per-run mention and citation flags for one prompt."""
    out = []
    for _ in range(runs):
        answer, sources = client.ask(prompt)      # your provider wrapper
        low = answer.lower()
        out.append({
            "mentioned":   BRAND in low,
            "cited":       any(BRAND in s.lower() for s in sources),
            "competitors": [c for c in COMPETITORS if c in low],
            "sources":     sources,
        })
    return out

def summarise(client):
    runs, domains = [], defaultdict(int)
    for prompt in PROMPTS:
        for r in scan(client, prompt):
            runs.append(r)
            for s in r["sources"]:
                domains[s.split("/")[2]] += 1
    n = len(runs)
    bms = sum(r["mentioned"] for r in runs) / n
    cr  = sum(r["cited"]     for r in runs) / n
    rival = statistics.mean(
        sum(c in r["competitors"] for r in runs) / n for c in COMPETITORS
    )
    print(f"Brand mention share : {bms:.1%}")
    print(f"Citation rate       : {cr:.1%}")
    print(f"Mean competitor BMS : {rival:.1%}")
    print(f"Ratio vs rivals     : {bms / rival:.2f}x" if rival else "")
    print("\nTop cited domains (your citation surface):")
    for d, c in sorted(domains.items(), key=lambda kv: -kv[1])[:15]:
        print(f"  {c:>4}  {d}")'''

CODE_DARK=r'''# dark_ai_estimate.py  --  split a Direct bucket into dark-AI + genuine
PHI    = 0.706     # share of AI referrals arriving without a referrer header
C_DARK = 0.1021    # observed conversion rate of dark AI sessions
C_BASE = 0.0246    # baseline conversion rate of genuine direct traffic

def decompose(direct_sessions, direct_conversions, acv):
    """Solve: direct_conversions = d*C_DARK + (direct_sessions - d)*C_BASE
    for d, the implied dark-AI session count. Cross-check against PHI."""
    implied_dark = (direct_conversions - direct_sessions * C_BASE) / (C_DARK - C_BASE)
    implied_dark = max(0.0, min(implied_dark, direct_sessions))
    return {
        "implied_dark_sessions":     round(implied_dark),
        "implied_total_ai_sessions": round(implied_dark / PHI),
        "hidden_conversions":        round(implied_dark * C_DARK),
        "hidden_revenue":            round(implied_dark * C_DARK * acv),
        "dark_share_of_direct":      round(implied_dark / direct_sessions, 3),
    }

if __name__ == "__main__":
    # 84,000 direct sessions, 3,120 conversions, $9,400 ACV
    for k, v in decompose(84_000, 3_120, 9_400).items():
        print(f"{k:<28} {v:,}")'''

FAQ=[
 ("Do backlinks still matter for AI search?",
  "Yes, but they are no longer the dominant signal. An Ahrefs analysis of roughly 75,000 brands found web-wide brand mention frequency correlates with AI citation inclusion at a Spearman coefficient of 0.664, against 0.204 for backlink volume, so mentions are about three times the signal links are. Links have not stopped working: a 0.204 correlation is real, and the link graph still governs whether a crawler discovers your page at all. What changed is that an unlinked mention on an independent trusted site is now direct corroboration a retrieval system can use, and it often outweighs the link."),
 ("Why does my own website barely get cited?",
  "Because generative engines are aligned to discount corporate self-assertion. A model that trusted every homepage claiming category leadership would be trivially gameable, so your own domain accounts for only about 5% to 10% of the source citations in AI answers (McKinsey), and roughly 82% trace back to earned editorial media (Muck Rack). Your site saying you are the best is read as marketing; an independent publication saying it is read as evidence. The fix is not schema, it is third-party corroboration."),
 ("What is the single highest-yield digital PR asset for AI citations?",
  "An original data study. It is the only asset that natively produces both of the top two citation levers the GEO research identified: precise statistics (a model cannot invent a real number) and named attributed quotes (a self-contained unit of verifiable authority). It also produces claims that get requoted and aggregated for years, each restatement another independent node naming your brand. Media syndication of original studies has produced a median 239% lift in brand citations across generative engines."),
 ("How do I make my research extractable by AI?",
  "Build it in stat units: a precise number, a named methodology, and an attributed quote, in a block short enough to survive chunking (under about 45 words). Measure citable stat density (extractable units per 1,000 words); a research hub should clear 4. Front-load the finding, since 44.2% of LLM citations come from the first 30% of a document. Put the methodology directly under the number so anyone who copies the claim copies its verification, publish the raw dataset under a permissive licence, and mark it up with Article + Dataset + Organization JSON-LD."),
 ("Is a media mention without a link worth anything for AI?",
  "For AI retrieval it is close to a complete win. The engine reads the text, extracts the claim, and notes that an independent trusted domain asserted a fact naming your brand; the hyperlink is a convenience for humans, the mention is the evidence. So stop making a link the outreach objective, which is the ask most likely to get your pitch declined, and instead ask that the brand name and the methodology line survive the edit. Track unlinked mention volume per domain as a first-class metric, because corroboration rewards breadth across independent sites over repetition on one."),
 ("How many domains do I actually need to target?",
  "Fewer than a link campaign. Analysis by 5WPR across 680 million AI citations found the top fifteen publishing domains capture roughly 68% of total AI citation share, a steep power law. Thirty placements concentrated in the domains that generative engines already retrieve from will outperform three hundred spread across the long tail, because the long tail rarely enters the candidate set. Run a prompt scan on your own category first: the domains cited for your prompts are your outreach list, and the retrieval layer tells you what it trusts every time you run it."),
 ("How long before a digital PR campaign moves AI citations?",
  "Longer than the placements. Coverage goes live and mention counts climb, but the citation metric usually sits flat for weeks while crawlers refetch, indices update, and corroboration density crosses the retrieval layer's threshold. Set the expectation at kickoff that mentions are the leading indicator and citations the lagging one, and report both from week one. The most common failure is publishing one study, seeing mention lift without citation lift at day ninety, and concluding it does not work: the compounding runs on the retrieval layer's refresh cycle, not yours."),
]

out=[]
out.append(p("Run a prompt about your category through ChatGPT. Read the sources it lists. If your brand shows up at all, look at where the citation points. There is a good chance it is not your site. It is a trade publication, a review aggregator, a comparison roundup nobody on your team commissioned, or a five-year-old forum thread. Your homepage is not in there. Your product page is not in there. The gated report you spent six weeks on is definitely not in there."))
out.append(p("Enterprise research from McKinsey put a number on this worth sitting with. A brand's owned domain accounts for roughly 5% to 10% of source citations in AI-generated responses. The remaining 90% to 95% belongs to third-party editorial media, review platforms, industry aggregators, and community discussion you do not control and cannot buy your way into cleanly."))
out.append(chart("sourceChart",230,"Figure 1. Representative split of citation sources in generative answers. The proportions vary by category. The ceiling on owned content does not."))
out.append(p("This is not a rendering problem or a schema problem. It is a structural one. Generative engines are aligned to discount corporate self-assertion, because a model that trusted every homepage claiming category leadership would be trivially gameable. Your site saying you are the best platform for mid-market logistics is read as marketing. An independent publication saying it is read as evidence."))
out.append(pull("If 90% of the citable surface sits outside your domain, what actually puts you there?"))
out.append(p("The answer that keeps holding up across the data is original research, distributed by people whose job is placement. Not link building. Not brand awareness. Specifically: proprietary data, packaged into extractable units, seeded across third-party publications that generative engines already trust. This piece covers how that works, why it works, and how to build one without spending nine months on a survey nobody reads."))
out.append(callout("Scope",[
  "This is the off-site layer: what you publish, who else repeats it, and how corroboration turns into citation. On-page construction is covered in "+L("the anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page")+". The metric definitions are set out in "+L("Share of Model","/blogs/share-of-model-measurement")+" and the standard behind them at the "+L("measurement methodology","/methodology")+". Crawler identities and robots directives are in "+L("how AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site")+". None of that is repeated at length here."]))

# 1
out.append(sec("01","link-play","Why did the link play stop paying?",
 "Because mentions now outweigh links as an AI citation signal by roughly three to one.",
 "For twenty-five years off-site SEO had one currency: links carried authority, authority moved rankings. An Ahrefs analysis of ~75,000 brands found brand mention frequency correlates with AI citation inclusion at 0.664, against 0.204 for backlink volume. Links did not stop mattering; they stopped being the dominant term."))
out.append(p("The entire Digital PR industry was built on converting editorial coverage into followed links, and the coverage itself was almost incidental. A placement with no link was a failure you did not put in the report. That model inverted."))
out.append(chart("corrChart",230,"Figure 2. External signals ranked by correlation with AI citation inclusion. The classical link-graph metrics cluster well below mention density."))
out.append(p("Read that carefully, because it is easy to draw the wrong conclusion. Backlinks did not stop mattering. A 0.204 correlation is a real signal, and the link graph still governs whether a crawler finds your page in the first place. What changed is that links are no longer the dominant term. They are one input among several, and they are outweighed by something most PR reporting does not even track."))
out.append(p("The mechanism is straightforward once you stop thinking in ranking terms. A retrieval-augmented system assembling an answer about your category is not consulting a link graph. It is looking for the same claim, about the same entity, on multiple independent sources. That is corroboration. A link signals a relationship between two documents; a mention is direct evidence that an independent party asserted a fact about you. The taxonomy underneath this, citation versus mention versus recommendation, is covered in "+L("that piece","/blogs/citation-vs-mention-vs-recommendation")+"."))
out.append(table("Table 1. The two disciplines share vocabulary and almost nothing else.",
 ["Operational dimension","Traditional SEO","Generative engine optimisation"],
 [["Primary objective","Position on a linear rank list","Attribution inside a synthesised answer"],
  ["Retrieval target","Document-level index and keyword match","Passage-level extraction and semantic chunking"],
  ["Dominant authority signal","Backlink volume, domain authority, PageRank","Web-wide mention density and entity corroboration"],
  ["Winning format","Comprehensive keyword-targeted landing pages","High-density data points, expert quotes, structured facts"],
  ["Interaction model","Click-through to your domain","Zero-click consumption with selective attribution clicks"],
  ["PR success metric","Followed links from DR 50+ domains","Corroborated claims across independent trusted nodes"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(p("The decoupling shows up in the ranking data too. Longitudinal tracking suggests the overlap between top Google organic results and AI-cited sources has collapsed from around 70% to under 20%. Separate work found 83% of citations in Google AI Overviews come from pages sitting outside the organic top ten entirely. Winning position one no longer buys you a seat in the answer, the same disconnect described in "+L("ranking is not visibility","/blogs/ranking-isnt-visibility")+". For a challenger brand this is the best news in a decade, but it only helps you if you produce the thing the synthesis layer is actually looking for."))

# 2
out.append(sec("02","rewards","What does the synthesis layer actually reward?",
 "Precise statistics and named attributed quotes, above every other content property tested.",
 "The GEO paper from Princeton, Georgia Tech, the Allen Institute and IIT Delhi (ACM SIGKDD 2024) built a 10,000-query benchmark and tested nine content modifications against an unoptimised baseline. Attributed quotes (+41%) and precise statistics (+31%) topped the table; keyword stuffing came in negative."))
out.append(p("The researchers needed new metrics, because rank position is meaningless when the output is a paragraph. Position-adjusted word count measures how much of the answer is attributable to your source, with a decay weight for citations appearing later. Subjective impression scores attribution quality across relevance, influence, uniqueness, prominence, volume, click likelihood, and diversity. The results are the closest thing the field has to a controlled experiment."))
out.append(table("Table 2. GEO-bench results. Position-adjusted word count and subjective impression, measured against an unoptimised baseline of 19.3.",
 ["Strategy","What was modified","PAWC","Delta","Impression","Delta"],
 [["Quotation addition","Direct attributed quotes from named experts","27.2","+41%","24.7","+28%"],
  ["Statistics addition","Qualitative claims replaced with precise numbers","25.2","+31%","23.7","+23%"],
  ["Fluency optimisation","Clearer prose and syntax, no new data","24.7","+28%","21.9","+14%"],
  ["Cite sources","Explicit inline citations to primary references","24.6","+28%","21.9","+14%"],
  ["Technical terms","Domain-specific terminology and nomenclature","22.7","+18%","21.4","+11%"],
  ["Easy to understand","Simplified explanations of complex material","22.0","+14%","20.5","+6%"],
  ["Authoritative tone","Formal, definitive expert voice","21.3","+10%","22.9","+19%"],
  ["Unique words","Expanded vocabulary and token diversity","20.5","+6%","20.4","+6%"],
  ["Keyword stuffing","Repetitive insertion of target keyword strings","17.7","-8%","20.2","+5%"]],
 cls=lambda j,c: "label" if j==0 else ("down" if c.strip().startswith("-") else "")))
out.append(chart("geoChart",250,"Figure 3. The same data as a ranked lift chart. Note what sits at the bottom."))
out.append(p("The top two levers are attributed quotes and precise statistics, and both are things a content team cannot fake and a language model cannot generate. A model has no way to produce a real number from a real survey, and it carries a strong penalty for inventing one, so when a document offers a specific figure with a named methodology attached, retrieval weights it heavily because it resolves something the model cannot resolve alone. Attributed quotes work the same way: self-contained units of verifiable authority that reduce hallucination risk by anchoring a claim to a named human."))
out.append(p("The bottom of the table is equally instructive. Keyword stuffing produced an absolute 8% decline, because neural relevance models read repetition as low-information filler, which means a decade of habit is now actively negative. Vocabulary expansion and authoritative tone barely register. You cannot write your way to citation with style. You have to bring something."))
out.append(h3("Strategies stack, and the incumbent pays"))
out.append(p("The Princeton team also tested combinations. Fluency optimisation paired with statistics addition beat every isolated strategy by more than 5.5%, and cite-sources, mediocre alone, expanded significantly when paired with quotation or statistical additions. Lift compounds, but not cleanly, because the strategies overlap in what they signal."))
out.append(code("formula &middot; stacked lift with overlap",FORM_STACK))
out.append(p("In practice the overlap term is substantial. Do not model a 41% quote lift and a 31% statistics lift as an 85% combined gain; plan for something closer to 50% and treat anything above as upside. The more consequential finding is what happens when everyone optimises at once."))
out.append(chart("serpChart",230,"Figure 4. Visibility delta by original SERP position when all candidate sources for a query are simultaneously GEO-optimised."))
out.append(p("When every retrieved source for a query applies GEO principles, visibility redistributes downward. The site ranking fifth gained 115.1% through citation structuring; the incumbent at rank one lost 30.3%. Generative retrieval evaluates passage-level data density and attribution clarity rather than macro domain authority, so when the challenger's page becomes as extractable as the incumbent's, the incumbent's ranking advantage stops carrying the difference. If you are the challenger, that asymmetry is the entire strategic case. You are not trying to out-authority anyone. You are trying to out-cite them."))

# 3
out.append(sec("03","data-study","Why is a data study the highest-yield PR asset?",
 "Because it is the only asset that natively manufactures both of the top two citation levers at once.",
 "An original data study generates precise statistics by construction and attributed expert quotes because someone has to interpret the findings. It gives journalists a reason to write about you that is not your product, and its claims are inherently repeatable, so every publication that covers it restates your number under their masthead."))
out.append(p("That last property is the one that matters most and the one most teams miss. A product announcement gets covered once and dies. A statistic gets cited, requoted, aggregated into listicles, and pulled into other people's research for years. Each of those is another independent node asserting a fact that names your brand."))
out.append(chart("assetChart",240,"Figure 5. Relative citation yield by Digital PR asset type. The gap between original research and everything else is not marginal."))
out.append(p("Field data supports the ordering. Media syndication campaigns distributing original empirical studies have produced a median 239% lift in brand citations across generative engines. Wire-distributed releases carrying original data saw their share of AI citations grow roughly fivefold across the second half of 2025. Campaigns securing thirty or more placements on DR 60+ domains have delivered a 52% increase in referring domains alongside a 52% rise in branded search demand. Separately, analysis from Muck Rack found 82% of AI citations trace back to earned editorial media, while paid and owned content combined account for about 6%. The channel most B2B teams fund least is the one doing almost all the work."))
out.append(table("Table 3. What each PR asset actually contributes to the retrieval layer.",
 ["Asset type","Signal delivered","Ingestion surface","Observed impact"],
 [["Proprietary data study","Verifiable statistics, structured facts","Live retrieval and RAG indices","+239% median citation lift"],
  ["Expert byline and commentary","Named quotes, domain authority","Training corpora and editorial archives","+41% position-adjusted word count"],
  ["Reactive newsjacking","Temporal freshness, contextual alignment","High-frequency live crawlers","Primary driver for time-sensitive prompts"],
  ["Review platform roundups","Category sentiment, feature and pricing facts","Vertical databases and aggregators","Decisive for best-in-category queries"],
  ["Entity registry work","Machine-readable canonical identity","Knowledge graph grounding layers","Explains up to 49.9% of recommendation variance"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(h3("Four archetypes, one of which is nearly free"))
out.append(p("Original research does not have to mean a commissioned panel study with a five-figure invoice attached. There are four archetypes that all produce citable stat units, and they differ enormously in cost, speed, and defensibility."))
out.append(table("Table 4. Study archetypes. Cost and durability move in opposite directions to what most teams assume.",
 ["Archetype","What it is","Typical cost","Time to publish","Citation durability"],
 [["Survey","Commissioned or panel-fielded questionnaire","$8k to $40k","8 to 12 weeks","High, refresh annually"],
  ["Internal telemetry","Aggregated, anonymised data from your own product","Engineering time only","3 to 5 weeks","Very high, nobody can replicate it"],
  ["Index or benchmark","Repeatable scoring of a public dataset or market","$3k to $15k","6 to 10 weeks","Highest, becomes a recurring reference"],
  ["Meta-analysis","Synthesis of existing published research","Analyst time only","2 to 4 weeks","Low to medium, easily displaced"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(p("Internal telemetry is worth pausing on, because most B2B SaaS companies are sitting on a publishable study and do not know it. You already log how long onboarding takes, what percentage of accounts adopt a feature in ninety days, how support volume moves with team size, or the median time to first value across segments. Aggregate it, anonymise it properly, and you have a dataset nobody else on earth can produce. A survey can be replicated by a competitor with a bigger budget; your product data cannot. When a generative engine is looking for a number about onboarding time and exactly one source has ever published one, the corroboration problem solves itself."))
out.append(p("The legal and privacy work is real and it is the actual constraint, not the analysis. Aggregate to a level where no individual account is identifiable, run it past whoever owns your data processing agreements, and check customer contracts for clauses on aggregate reporting before anything ships. Index and benchmark studies are the other underrated option and they compound differently: a one-off survey is cited for eighteen months and goes stale, but an index published annually becomes the category reference point, so each edition inherits the citation surface of the last. The second edition is roughly half the work of the first. The fourth is a template."))
out.append(callout("The uncomfortable part",[
  "A data study is expensive, slow, and hard to justify in a quarter where pipeline is soft. It is also the only asset that manufactures both of the top two citation levers at once. Most teams cut it precisely when the compounding would have started to show."]))

# 4
out.append(sec("04","design","How do you design a study a model can lift?",
 "Build it out of stat units: a precise number, a named methodology, and an attributed quote, in a chunk-sized block.",
 "Most original research fails at citation for a reason that has nothing to do with the research. The findings are real and the methodology is sound, but the write-up buries every usable number inside a narrative paragraph that cannot be extracted without its surrounding context. The unit that travels is not the study. It is the stat unit."))
out.append(pipeline([("Precise number","Not a qualitative hedge. 41%, not most."),("Named methodology","n, sample, field window. Verifiable."),("Attributed quote","A real person with a real title. The 41% lever."),("Stat unit","The smallest block a model can lift whole with attribution intact.")],3,
 "Figure 6. A stat unit is the smallest block a generative engine can lift whole with attribution intact. Everything in your study should be built toward producing these."))
out.append(p("Three components, all mandatory. A precise number, not a qualitative hedge. A named methodology so the claim is verifiable and the model can assess it. An attributed quote from a real person with a real title, which is where the 41% lever lives. Miss any one and the block degrades into something a model can read but will not confidently repeat. You can measure how well a document does this: citable stat density counts the extractable units per thousand words."))
out.append(code("formula &middot; citable stat density",FORM_CSD))
out.append(p("A general blog post typically scores under 1. A well-built research hub should clear 4. Below 2 and you have written an essay with numbers in it, which is a different thing."))
out.append(h3("Design backward from the headline"))
out.append(p("The practical move is to write the press headline before you write the survey. If you cannot state the finding you are hoping for as a single sentence with a number in it, the study is not designed yet. This feels like cheating. It is not, provided you are honest about publishing the result whichever way it lands. What you are doing is making sure the instrument can produce an extractable claim at all, rather than a table of correlations that requires a paragraph to explain."))
out.append(code("study-spec.yaml",CODE_YAML))
out.append(p("Note the last line. Publishing the underlying dataset as a downloadable file is one of the cheapest credibility signals available, and it gives you something to mark up with Dataset schema later. Almost nobody does it, which is exactly why it works. Segment cuts are the other underused lever: one question segmented three ways produces four stat units instead of one, and segment findings tend to be more quotable than headline averages because they are specific. A journalist covering mid-market SaaS wants the mid-market number, not the blended one."))
out.append(h3("Score your own units before anyone else sees them"))
out.append(p("Once the data is in, run the draft through a scoring pass. This is a crude filter and it catches most of what would otherwise ship broken."))
out.append(code("score_stat_units.py",CODE_SCORE))
out.append(p("This will not catch everything and it is not meant to. What it catches reliably is the hedge sentence that felt fine in the draft, the finding that lost its methodology in an edit, and the forty-word claim that ballooned to ninety and no longer fits inside a retrieval chunk. The chunking mechanics behind that are covered in "+L("how your page gets retrieved","/blogs/how-your-page-gets-retrieved")+"."))

# 5
out.append(sec("05","distribution","How concentrated is AI citation distribution?",
 "Extremely. The top fifteen publishing domains capture about 68% of all AI citation share.",
 "A study nobody covers is a blog post with a methodology section. Distribution is where the citation gets made, and the target list is much shorter than a link-building list. Analysis by 5WPR across 680 million AI citations found the top fifteen domains capture roughly 68% of total citation share, a steep power law with an unusually concentrated head."))
out.append(chart("domainChart",230,"Figure 7. Cumulative AI citation share by publishing domain. The head of the curve is where your outreach list ends, not where it begins."))
out.append(p("This changes the shape of a campaign. Traditional Digital PR optimises for volume, because link equity accrues roughly linearly and a hundred DR 40 placements is a defensible outcome. Citation share does not work that way. Thirty placements concentrated in the domains generative engines already retrieve from will outperform three hundred spread across the long tail, because the long tail rarely enters the candidate set at all."))
out.append(p("The corollary is that placement quality has a specific technical meaning here, and it is not domain rating. What matters is whether a domain is already being retrieved for prompts in your category, and whether the placement carries extractable facts. A DR 85 national outlet that mentions you in a listicle with no numbers is worth less than a DR 55 trade publication that reprints your headline statistic with attribution."))
out.append(pipeline([("Retrieval trust","Is this domain already cited for your category prompts?"),("Citable fact density","Does the placement carry your number and methodology?"),("Upper-right quadrant","Retrieved AND factual. The only quadrant that converts."),("Citation","Coverage becomes a source the engine pulls into answers.")],2,
 "Figure 8. Placement types mapped against retrieval trust and citable fact density. The upper right is the only quadrant that reliably converts coverage into citation."))
out.append(p("You can formalise this. An entity corroboration index weights each mentioning domain by how much the retrieval layer trusts it, then takes a log of mention count to reflect diminishing returns from repeat coverage on the same site."))
out.append(code("formula &middot; entity corroboration index",FORM_ECI))
out.append(p("The log matters. Your fourth mention on the same publication adds very little compared to your first mention on a new one, because corroboration is about independence rather than volume. Two mentions across two domains beat four mentions on one."))
out.append(table("Table 5. Placement tiers and what each contributes. Sequence matters: the exclusive sets the framing everyone else inherits.",
 ["Tier","What you pitch","What it delivers","Realistic effort"],
 [["Tier 1 trade press","Embargoed exclusive on the headline finding","Highest retrieval trust in-category, sets the canonical framing","4 to 6 weeks lead, one outlet only"],
  ["Vertical analyst blogs","Segment cuts and methodology detail","Deep citable density, strong topical association","2 to 3 weeks, high hit rate"],
  ["Category review sites","Data relevant to their comparison tables","Decisive for best-in-category prompts","Ongoing relationship, slow to start"],
  ["National business press","The counterintuitive finding, framed broadly","Entity trust and knowledge graph reinforcement","Low hit rate, high payoff"],
  ["Community and forums","The dataset itself, no pitch","Human consensus signal, up to 83.8% variance in some personas","Cannot be forced, easily backfires"],
  ["Wire syndication","Full release with the stat block intact","Breadth and crawl surface, weak on its own","Same week, low cost"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(p("Sequencing is worth more than most teams realise. Give the headline finding to one tier-one outlet as an exclusive, let them frame it, then run broad outreach citing that coverage. The framing the first outlet chooses tends to propagate, so you get corroboration on a consistent claim rather than fifteen slightly different restatements of the same number. Consistency of claim is what makes corroboration legible to a retrieval system."))
out.append(h3("The mention with no link is not a failure"))
out.append(p("Under the old model, a placement without a followed link was a partial win at best. Agencies were compensated on links, reports counted links, and a journalist who covered your study, quoted your executive, and reproduced your headline statistic without linking had, in reporting terms, delivered almost nothing. In the retrieval layer that placement is close to a complete win. The engine is not traversing a link to find you; it is reading the text, extracting the claim, and noting that an independent trusted domain asserted a fact naming your brand. The hyperlink is a convenience for humans. The mention is the evidence."))
out.append("<ul>"
 "<li><strong>Stop treating link acquisition as the outreach objective.</strong> Asking an editor to add a link is the request most likely to get your pitch declined, and you are trading a high-friction ask for a low-value asset. Ask instead that the brand name and the methodology line survive the edit.</li>"
 "<li><strong>Do not conclude that links stopped mattering.</strong> A 0.204 correlation is still a real signal, and links remain how crawlers discover your research hub. The mention proves the claim; the link gets the crawler to the page holding your data, schema, and downloadable dataset. You want both. You should only fight for one.</li></ul>")
out.append(p("The reporting change that follows is straightforward and awkward. Add unlinked mention volume as a first-class metric alongside referring domains, and track it per domain rather than in aggregate, because the corroboration index rewards breadth and discounts repetition. A dashboard showing forty mentions across thirty-one domains is telling you something a dashboard showing forty mentions is not. The "+L("off-site authority scorecard","/tools/off-site-authority-scorecard")+" scores exactly this spread."))
out.append(h3("The stat block that goes in every pitch"))
out.append(p("Give every journalist the same extractable block. Not a press release. A block they can paste, edit lightly, and publish, with the attribution already correct."))
out.append(code("press-kit/stat-block.md",CODE_BLOCK))
out.append(p("Two details do disproportionate work here. The methodology sits directly under the number rather than in a footnote, so a publication that copies the claim copies the verification with it. And the licence on the raw data is permissive, which removes the friction that stops an editor from reproducing your table."))

# 6
out.append(sec("06","hub","How should you package the research hub?",
 "Front-loaded, deeply modular, and marked up with Article, Dataset and Organization schema.",
 "The off-site work generates corroboration; the owned hub is what everything points back at. Structural research finds 44.2% of all LLM citations are extracted from the first 30% of a document's word count, so front-loading is where the extraction happens, not a stylistic preference. Depth still matters: documents over 20,000 characters earn roughly 4.3x more citations, provided they keep modular headings."))
out.append(chart("posChart",230,"Figure 9. Relative citation density by position in a document. The secondary bump near the end corresponds to conclusion and summary blocks."))
out.append(p("This sounds contradictory until you separate the two mechanisms. Length gives you more chunks to be retrieved for; front-loading determines which of those chunks gets used when your page is picked. You need both. For a research hub, the running order that works is: the headline finding as the first sentence under the H1, a forty to sixty word definition block stating what was measured and how, the full methodology as a distinct section, then the findings one per H2 with the segment table adjacent, then the commentary. Resist the instinct to open with context. Nobody is reading your framing paragraph, and no retrieval system is chunking it usefully."))
out.append(pipeline([("Site level","robots.txt, sitemap, entity schema. Can the bot reach it?"),("Page level","Front-loaded finding, modular H2s, depth. Which chunk wins?"),("Passage level","The stat unit itself. What gets lifted into the answer?")],2,
 "Figure 10. The three structural levels, and which stage of the pipeline reads each one."))
out.append(h3("Schema for a research asset"))
out.append(p("Structured data is the part teams skip and then wonder why entity resolution is wrong. Sites with fully implemented JSON-LD achieve roughly 45% higher AI citation rates than unstructured domains. For a data study you want three types working together: Article for the write-up, Dataset for the underlying data, and Organization to bind the entity to its canonical identity. The full schema playbook is in "+L("schema markup for AI citations","/blogs/schema-markup-ai-citations-2026")+"."))
out.append(code("research-hub.jsonld",CODE_JSONLD))
out.append(p("The sameAs array on Organization is doing quiet but important work. It binds your domain to knowledge-graph nodes, and Wikidata entity presence alone has been observed to explain up to 49.9% of recommendation variance in B2B contexts. If you have no Wikidata entity, that is a separate project and it is worth starting, as covered in "+L("becoming an entity","/blogs/becoming-an-entity")+". Then confirm retrieval crawlers can actually reach the hub. Training crawlers and live retrieval crawlers are different bots with different consequences, and blocking the wrong one removes you from real-time answers entirely."))
out.append(code("robots.txt",CODE_ROBOTS))
out.append(callout("A common, expensive mistake",[
  "Blocking GPTBot to protect intellectual property, then discovering the research hub you built for AI visibility is absent from ChatGPT answers. GPTBot handles training. OAI-SearchBot handles live retrieval and citation. They are separate directives, and the second one is the one that matters for this campaign."]))

# 7
out.append(sec("07","measure","How do you measure this without fooling yourself?",
 "Instrument brand mention share across a fixed prompt set, run each prompt many times, and report the lag.",
 "Rank tracking cannot process a synthesised paragraph, so the measurement stack has to change with the strategy. Four metrics carry most of the load. Brand mention share is the one to instrument first, because it is most directly moved by off-site PR and cheapest to sample; the definitions and sampling are set out in Share of Model and the standard at the methodology page."))
out.append(table("Table 6. The four metrics that survive contact with a generative answer.",
 ["Metric","What it counts","What it tells you","Working benchmark"],
 [["AI answer inclusion rate","Share of prompt runs where you appear as a source at all","Macro discovery reach","Above 65% on category prompts"],
  ["Citation rate","Share of runs containing a clickable link to your domain","Direct attribution capture","Above 35%"],
  ["Brand mention share","Share of responses naming your brand across a competitive prompt set","Competitive share of voice","Beat your closest rival by 1.5x"],
  ["Sentiment delta","Whether you are recommended positively, neutrally, or conditionally","Commercial framing quality","Net positive above +0.75"]],
 cls=lambda j,c: "label" if j==0 else ""))
out.append(code("formula &middot; brand mention share",FORM_BMS))
out.append(p("Run count matters more than people expect. Generative outputs are stochastic, and a single run per prompt produces a number that moves several points between measurements for no reason at all. Five runs is a working minimum, ten is better if you can afford the calls, and the full sampling standard is on the "+L("measurement methodology","/methodology")+" page."))
out.append(code("scan_prompt_set.py",CODE_SCAN))
out.append(p("The last block of that output is the most useful part and the one people ignore. The domains being cited for your category prompts are your outreach list. You do not have to guess which publications the retrieval layer trusts. It tells you, every time you run the scan. The end-to-end version of this loop is "+L("prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")+"."))
out.append(h3("The lag will test your nerve"))
out.append(p("Citation lift does not arrive with the placements. Coverage goes live, mention counts climb, and the citation metric sits flat for weeks while crawlers refetch, indices update, and corroboration density crosses whatever threshold the retrieval layer applies."))
out.append(chart("campaignChart",230,"Figure 11. Indicative shape of a campaign. Placements lead mentions, mentions lead citations, and the gap between them is where campaigns get cancelled."))
out.append(p("Plan for this in the reporting cadence, not just the strategy deck. If the leadership review lands in week seven, you will be presenting a flat citation line with a healthy placement count and no way to connect them. Set the expectation at kickoff that mentions are the leading indicator and citations the lagging one, and report both from week one so the relationship is visible before anyone needs it to be."))
out.append(h3("The traffic you cannot see"))
out.append(p("Then there is the attribution problem, which is worse than most analytics teams realise. Roughly 70.6% of generative AI referral sessions arrive with the HTTP referrer header stripped, which means GA4 files them under Direct."))
out.append(chart("darkChart",240,"Figure 12. The Dark AI gap. Same traffic, same intent, same conversion rate, two entirely different lines in the report."))
out.append(p("The distortion compounds. Baseline direct traffic converts at around 2.46%. The Dark AI sessions hiding inside that bucket convert at roughly 10.21%, a 4.1x premium. Blended together, the Direct channel looks slightly better than usual and nobody investigates, while the PR campaign that produced the highest-intent traffic on the site reports almost nothing."))
out.append(table("Table 7. Three populations, two buckets. The middle row is the problem.",
 ["Channel as recorded","Share of AI sessions","Referrer header","Conversion rate","Attribution outcome"],
 [["Visible AI referral","29.4%","Intact","10.21%","Correctly credited"],
  ["Dark AI","70.6%","Stripped","10.21%","Filed as Direct"],
  ["Genuine direct","Not AI","None","2.46%","Correct, but now diluted"]],
 cls=lambda j,c: "label" if j==0 else ("down" if c=="Dark AI" else "")))
out.append(p("A rough estimate of the hidden revenue is better than no estimate."))
out.append(code("formula &middot; hidden Dark-AI revenue",FORM_DARK))
out.append(code("dark_ai_estimate.py",CODE_DARK))
out.append(p("Two ways to reduce the guesswork. Tag every URL you place in a press kit or syndicated release so at least the linked subset is unambiguous. And build a Direct-bucket cohort report segmented by landing page, because Dark AI sessions land disproportionately on deep informational pages rather than the homepage, which is not how genuine direct traffic behaves."))

# 8
out.append(sec("08","ninety","What does a 90-day sequence look like?",
 "Baseline first, field the study, distribute in sequence, then re-scan, and hold.",
 "The twelve-month enterprise version has four phases: infrastructure and audit, data asset production, PR distribution, then attribution and iteration. That framing is fine, but it is slower than a first study needs because the phases overlap more than the deck suggests. A compressed version that works looks like this."))
out.append(chart("timelineChart",230,"Figure 13. Ninety days from baseline scan to citation re-measurement. The workstreams overlap deliberately."))
out.append("<ul>"
 "<li><strong>Days 0 to 21.</strong> Baseline everything before you change anything. Run the prompt scan, record brand mention share and citation rate against two competitors, capture the cited-domain list. In parallel, verify crawler access and ship the schema. This is the only thing that lets you prove causation later.</li>"
 "<li><strong>Days 7 to 42.</strong> Design and field the study. Write the headline sentences first, cut every question that cannot produce one, and field on a panel unless your list is genuinely representative. Twenty-one days of fielding is enough for most B2B panels.</li>"
 "<li><strong>Days 42 to 59.</strong> Analysis, stat-unit extraction, and hub build. Score the draft for citable density before it ships. Front-load the finding. Publish the raw data.</li>"
 "<li><strong>Days 56 to 90.</strong> Distribution in sequence: exclusive to one tier-one outlet, then broad outreach citing that coverage, then wire syndication, then expert commentary on the outlets that covered it. Do not run these simultaneously.</li>"
 "<li><strong>Days 80 to 90.</strong> Mention harvest and citation re-scan against the same prompt set, same run count, same competitors. Expect mentions to have moved and citations to be only starting to.</li></ul>")
out.append(p("Then hold. The single most common failure mode is publishing one study, seeing mention lift without citation lift at day ninety, and concluding the strategy does not work. The compounding is real but it runs on the retrieval layer's refresh cycle, not yours. Cost per incremental citation point is the number to bring to the second budget conversation."))
out.append(code("formula &middot; cost per citation point",FORM_CPC))
out.append(p("It will look bad after one study and reasonable after three, which is an accurate reflection of how the asset behaves rather than a presentational trick. The compounding dynamics are the subject of "+L("the GEO compounding flywheel","/blogs/geo-compounding-flywheel")+"."))

# 9
out.append(sec("09","breaks","Where does this break?",
 "The correlations are not causal, the benchmarks come from mixed bases, and none of it works without a real finding.",
 "The numbers here come from a young field and some will not survive contact with your category. A few honest limits before you plan against any of them."))
out.append("<ul>"
 "<li><strong>The correlation figures are not causal.</strong> A 0.664 correlation between mention density and citation is strong, and still correlation. Brands that get mentioned a lot are also large, funded, and covered for reasons unrelated to their PR programme. Treat it as a direction, not a coefficient.</li>"
 "<li><strong>Benchmark figures come from mixed bases.</strong> The +239% lift, the 82% earned-media share, and the 68% domain concentration come from different studies with different methodologies and definitions. The ordering is consistent across sources; the absolute values are directional.</li>"
 "<li><strong>Hallucination is a live risk on your own data.</strong> A joint BBC and European Broadcasting Union study found 81% of AI assistant responses contained factual inaccuracies, 45% with significant errors. Your statistic will be misquoted. Publishing the methodology adjacent to the number is partial defence; monitoring for the misquote is the rest.</li>"
 "<li><strong>Category concentration varies enormously.</strong> The top-fifteen-domain figure is an aggregate. In technical B2B, community sources and documentation carry far more weight than trade press. Run the scan on your own prompt set before you buy anyone's target list.</li>"
 "<li><strong>This does not work without a real finding.</strong> A study designed purely as a link asset, with a thin sample and a predetermined conclusion, gets covered by the outlets that cover anything and cited by nothing. The extraction layer has no taste, but the journalists in the top fifteen domains do, and they are the gate.</li></ul>")
out.append(p("The strategic case survives all of that. Owned content has a hard ceiling of roughly a tenth of the citation surface. The synthesis layer rewards precise numbers and named attribution above every other content property tested. Third-party corroboration is the mechanism that converts one into the other, and original research is the only asset that produces all three at once."))
out.append(pull("Everything else in the Digital PR toolkit is a way of getting attention. This is a way of getting repeated. Those stopped being the same thing."))

# FAQ
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
out.append(faq_html)

# References
REFS=[
 ("GEO: Generative Engine Optimization. Aggarwal et al., ACM SIGKDD 2024.","https://arxiv.org/abs/2311.09735"),
 ("What the GEO paper shows for your business. Elementera.","https://www.elementera.com/blog/geo-generative-engine-optimization"),
 ("How Marketers Are Increasing GEO Traffic in 2026. The Digital Bloom.","https://thedigitalbloom.com/learn/generative-engine-optimization/"),
 ("Generative Engine Optimization Statistics 2026. Omnibound.","https://www.omnibound.ai/blog/generative-engine-optimization-statistics"),
 ("LLM Seeding: How Brands Build Visibility Before AI Tools Cite Them. Brandastic.","https://www.brandastic.com/blog/llm-seeding/"),
 ("How Digital PR Builds Your Brand in AI Overviews. StudioHawk.","https://studiohawk.com.au/blog/digital-pr-ai-overviews/"),
 ("What Is GEO? Generative Engine Optimization for AI Citations. AuthorityTech.","https://authoritytech.com/generative-engine-optimization/"),
 ("Generative Engine Optimization: Complete Guide to AI SEO. Navoto.","https://navoto.com/generative-engine-optimization/"),
 ("The Complete Guide to Generative Engine Optimization. Geol.ai.","https://geol.ai/guide-generative-engine-optimization"),
 ("GEO Knowledge Base. Metricus.","https://metricus.io/geo-knowledge-base/"),
 ("Schema Markup for AI Search: Complete Guide. Vryse.","https://vryse.io/blog/schema-markup-for-ai-search"),
 ("AI Crawlers Explained: GPTBot, ClaudeBot, PerplexityBot. Anagram.","https://www.anagram.com/blog/ai-crawlers-explained"),
 ("Robots.txt Guide: Essential Rules and Disallow Best Practices. Conductor.","https://www.conductor.com/academy/robots-txt/"),
 ("Robots.txt for AI Crawlers: 2026 Template. Cubitrek.","https://cubitrek.com/blog/robots-txt-for-ai-crawlers/"),
 ("What Is Digital PR? AI and SEO Visibility Guide 2026. Exposure Ninja.","https://exposureninja.com/blog/digital-pr/"),
 ("Why Digital PR Is Important and How to Build a Strategy. 2Point Agency.","https://2point.agency/blog/why-digital-pr-is-important"),
 ("Building AI Search Content Authority Beyond Rankings. Moonrank.","https://moonrank.io/blog/ai-search-content-authority"),
 ("What Is GEO? AI Search Visibility for Marketing Pros. GEO Tool.","https://geotool.ai/what-is-geo"),
 ("GEO official reference page. Grounding Page.","https://grounding.page/geo"),
 ("Methodology and Sources, AI Search Visibility Research. info.link.","https://info.link/ai-search-visibility-methodology"),
 ("Search Everywhere Optimization for 2026. Surfer.","https://surferseo.com/blog/search-everywhere-optimization/"),
 ("Perplexity Tracking and SEO for Brand Citations. LLM Pulse.","https://llmpulse.ai/blog/perplexity-tracking"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
out.append('<div class="about-block" id="references"><div class="about-label">References</div>'
           '<p style="margin-bottom:16px;">Figures 1 through 13 are original, built from the data in the sources below.</p>'
           f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Sources: the Princeton/Georgia Tech/AI2/IIT Delhi GEO experiment, an Ahrefs analysis of ~75,000 brands, McKinsey source-mix data, Muck Rack and 5WPR citation studies, and 2026 GEO benchmarks. Correlations are directional, not causal; magnitudes are drawn from mixed bases.</p></div>')

body="\n".join(out)

SIDEBAR=[("5-10%","of AI citation sources are your own domain"),("0.664","mention correlation vs 0.204 for backlinks"),("+239%","median citation lift from syndicated research"),("68%","of AI citations sit in fifteen domains")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#link-play"><span class="toc-num">01</span>The link play stopped paying</a></li>'
     '<li><a href="#rewards"><span class="toc-num">02</span>What the layer rewards</a></li>'
     '<li><a href="#data-study"><span class="toc-num">03</span>The data-study advantage</a></li>'
     '<li><a href="#design"><span class="toc-num">04</span>Designing a liftable study</a></li>'
     '<li><a href="#distribution"><span class="toc-num">05</span>Distribution concentration</a></li>'
     '<li><a href="#hub"><span class="toc-num">06</span>Packaging the hub</a></li>'
     '<li><a href="#measure"><span class="toc-num">07</span>Measuring it honestly</a></li>'
     '<li><a href="#ninety"><span class="toc-num">08</span>The ninety-day sequence</a></li>'
     '<li><a href="#breaks"><span class="toc-num">09</span>Where this breaks</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - mentions beat links - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["digital PR","original research","data study","AI citations","brand mentions","generative engine optimization","GEO","earned media","entity corroboration","off-site SEO"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Digital PR &amp; Data Studies: The Link Play AI Cites &middot; rawmktg."
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
  var neutral=rgba(faint,0.4), amber='#C9922E', blue='#5B8DB8';

  var sc=document.getElementById('sourceChart');
  if(sc){new Chart(sc,{type:'bar',data:{labels:['Earned editorial media','Owned + paid','Other third-party'],datasets:[{data:[82,6,12],backgroundColor:[up,signal,neutral],borderRadius:4,barThickness:56}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of AI citations';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var cc=document.getElementById('corrChart');
  if(cc){new Chart(cc,{type:'bar',data:{labels:['Brand mention frequency','Backlink volume','Domain rating','Referring domains'],datasets:[{data:[0.664,0.204,0.19,0.18],backgroundColor:[up,signal,rgba(signal,0.6),rgba(signal,0.5)],borderRadius:4,barThickness:38}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' r = '+c.raw+' (Spearman)';}}}},
      scales:{x:{beginAtZero:true,max:0.75,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var gc=document.getElementById('geoChart');
  if(gc){new Chart(gc,{type:'bar',data:{labels:['Quotations','Statistics','Fluency','Cite sources','Technical terms','Easy to read','Authoritative','Unique words','Keyword stuffing'],datasets:[{data:[41,31,28,28,18,14,10,6,-8],backgroundColor:['#3E9B6A',rgba(up,0.85),rgba(signal,0.6),rgba(signal,0.6),rgba(signal,0.5),rgba(signal,0.45),rgba(signal,0.4),rgba(signal,0.35),signal],borderRadius:4,barThickness:26}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+(c.raw>0?'+':'')+c.raw+'% position-adjusted word count';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{ticks:{color:text,font:{family:mono,size:10},callback:function(v){return (v>0?'+':'')+v+'%';}},grid:{color:grid}}}}});}

  var se=document.getElementById('serpChart');
  if(se){new Chart(se,{type:'bar',data:{labels:['Rank 1 (incumbent)','Rank 2','Rank 3','Rank 4','Rank 5 (challenger)'],datasets:[{data:[-30.3,-12,8,44,115.1],backgroundColor:[signal,rgba(signal,0.6),neutral,rgba(up,0.6),up],borderRadius:4,barThickness:36}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+(c.raw>0?'+':'')+c.raw+'% visibility';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{ticks:{color:text,font:{family:mono,size:10},callback:function(v){return (v>0?'+':'')+v+'%';}},grid:{color:grid}}}}});}

  var ac=document.getElementById('assetChart');
  if(ac){new Chart(ac,{type:'bar',data:{labels:['Proprietary data study','Expert byline','Review roundup','Reactive newsjacking','Entity registry'],datasets:[{data:[100,46,40,32,26],backgroundColor:[up,rgba(signal,0.6),rgba(signal,0.55),rgba(signal,0.45),rgba(signal,0.4)],borderRadius:4,barThickness:34}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' (relative citation yield, indexed)';}}}},
      scales:{x:{beginAtZero:true,max:110,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var dc=document.getElementById('domainChart');
  if(dc){new Chart(dc,{type:'line',data:{labels:['1','3','5','8','10','15','25','50','100','250'],datasets:[{data:[18,34,45,56,62,68,78,88,95,100],borderColor:signal,backgroundColor:rgba(signal,0.12),fill:true,tension:0.35,pointRadius:0,borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% cumulative citation share';},title:function(t){return 'Top '+t[0].label+' domains';}}}},
      scales:{x:{title:{display:true,text:'publishing domains (ranked)',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var pc=document.getElementById('posChart');
  if(pc){new Chart(pc,{type:'bar',data:{labels:['0-10%','10-20%','20-30%','30-40%','40-60%','60-80%','80-90%','90-100%'],datasets:[{data:[19,14,11,9,15,10,9,13],backgroundColor:['#3E9B6A','#3E9B6A',rgba(up,0.7),neutral,neutral,neutral,rgba(signal,0.5),rgba(signal,0.6)],borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of citations extracted here';}}}},
      scales:{x:{title:{display:true,text:'position in document',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var mc=document.getElementById('campaignChart');
  if(mc){new Chart(mc,{type:'line',data:{labels:['wk1','wk2','wk3','wk4','wk5','wk6','wk8','wk10','wk12','wk16'],datasets:[
    {label:'Placements',data:[5,18,32,40,42,42,42,42,42,42],borderColor:blue,backgroundColor:'transparent',tension:0.3,pointRadius:0,borderWidth:2},
    {label:'Mentions',data:[2,9,22,38,52,63,72,78,82,85],borderColor:amber,backgroundColor:'transparent',tension:0.3,pointRadius:0,borderWidth:2},
    {label:'Citations',data:[0,1,2,4,7,11,20,34,52,74],borderColor:up,backgroundColor:rgba(up,0.1),fill:true,tension:0.3,pointRadius:0,borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:11}}},tooltip:{mode:'index',intersect:false}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var kc=document.getElementById('darkChart');
  if(kc){new Chart(kc,{type:'bar',data:{labels:['Visible AI referral','Dark AI (filed as Direct)','Genuine direct'],datasets:[
    {label:'Share of AI sessions %',data:[29.4,70.6,0],backgroundColor:neutral,borderRadius:4},
    {label:'Conversion rate %',data:[10.21,10.21,2.46],backgroundColor:[up,signal,rgba(faint,0.5)],borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.dataset.label+': '+c.raw;}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var tc=document.getElementById('timelineChart');
  if(tc){new Chart(tc,{type:'bar',data:{labels:['Baseline + audit','Field the study','Analysis + hub','Distribution','Re-scan'],datasets:[{label:'start',data:[0,7,42,56,80],backgroundColor:'transparent'},{label:'duration',data:[21,35,17,34,10],backgroundColor:[blue,amber,rgba(up,0.7),signal,up],borderRadius:4,barThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){if(c.datasetIndex===0)return '';var s=c.chart.data.datasets[0].data[c.dataIndex];return ' day '+s+' to '+(s+c.raw);}}}},
      scales:{x:{stacked:true,beginAtZero:true,max:95,title:{display:true,text:'days',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:9}},grid:{color:grid}},y:{stacked:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Content &amp; Authority &middot; Digital PR</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/mbl_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/mbl_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faqitem:",hh.count('faq-item'),"| refs:",hh.count('id="references"'))
