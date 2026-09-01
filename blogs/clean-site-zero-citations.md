# Clean Site, Zero Citations

> Forty-one companies in the Investing & Wealth cohort were scored against the same 48 buyer questions on the same four AI tools. Thirty-six came back at zero. The five that showed up carried, on the median, twice the technical debt of the ones that never appeared once.

*Source: https://rawmktg.com/blogs/clean-site-zero-citations · rawmktg. by Vinayak Ravi*


## 01. What is this teardown built on?

**Forty-one companies in one category, scored against the same 48 buyer questions on four AI tools,** 7,872 answers in all, with 35 live site crawls on the same day. Because the question set is shared, the losing and winning sides are measured off one denominator.

Between them, the forty-one audits are a single controlled experiment that nobody set out to run. Every audit used the same standardised prompt set for the category: 48 buyer questions, spread across eight buying stages, run on ChatGPT, Google AI Overviews, Claude, and Gemini. That is 192 question-and-tool pairs per company. For each pair, one binary check: was the brand named, or was a page on its domain linked. Either one counts.

Thirty-five of the forty-one also carry a live crawl of the production website on the same day: 23,870 URLs in total, checked for the usual retrieval blockers plus content and template defects. This is the same [Investing & Wealth cohort audited for backlinks in the link liability](/blogs/the-link-liability), read here through a different lens: what actually wins the AI answer slot.

Table 1. The dataset.

| Item | Value |
| --- | --- |
| Companies audited | 41 |
| Category | Investing, wealth, and digital-asset infrastructure |
| Buyer questions per company | 48 |
| AI tools tested | 4 (ChatGPT, Google AI Overviews, Claude, Gemini) |
| Answers scored per company | 192 |
| Total answers scored | 7,872 |
| Companies with a live site crawl | 35 |
| URLs crawled in total | 23,870 |
| Distinct defect classes observed | 57 max on a single site, 41 median |
| Data collected | Single day, 25 August 2026 |

Three limits worth stating up front. The prompt set is category-level, not brand-level: it asks the questions a buyer types when they describe a problem rather than a vendor, so these scores are a floor, not a ceiling. It is one day, which catches a distribution, not a trend. And n is 41 with only five non-zero outcomes, so any correlation is directional. Where a number is weak, this piece says so.

## 02. How visible is the segment in AI answers?

**It is a zero. Thirty-six of forty-one companies were never named or linked in a single one of their 192 answers,** on any tool, for any question, at any stage. Only five appeared at all, and the segment collectively occupies 19% of the slot only by counting every overlap twice.

Figure 1. Overall Answer Share by company, all 41 sorted. One company clears 12%; four sit at 1-2%; thirty-six are flat zero.

The five exceptions: Range at 12%, then Cryptio, Pulley, and Taxbit at 2%, and Utila at 1%. Add all forty-one together, counting every overlap twice and giving each brand full credit for every answer it appeared in, and the segment collectively occupies 19% of the answer slot.

Table 2. The five companies with any presence, by tool.

| Company | Overall | ChatGPT | Google AIO | Claude | Gemini | Stages covered |
| --- | --- | --- | --- | --- | --- | --- |
| Range | 12% | 6% | 8% | 17% | 17% | 7 of 8 |
| Cryptio | 2% | 4% | 2% | 0% | 0% | 3 of 8 |
| Pulley | 2% | 4% | 4% | 0% | 0% | 2 of 8 |
| Taxbit | 2% | 2% | 2% | 2% | 2% | 1 of 8 |
| Utila | 1% | 0% | 2% | 0% | 0% | 1 of 8 |

There is a detail most teardowns would skip. Pulley appears twice in this dataset: as one of the forty-one audited companies at 2% visibility, and as a source domain the AI tools quoted against thirty-eight of the other forty. A company can be simultaneously under-cited for its own category and the thing that beats its neighbours. Publishing is not a scoreboard position. It is a supply-side act.

## 03. Who actually owns the AI answer slot?

**Ten domains take 37% of it across all 7,872 answers, and a third of that is held by trade media, niche publishers, and adjacent vendors** that do not sell what these companies sell. They just have pages that answer the question.

Table 3. Who the tools actually return.

| Domain | Share of 192 pairs | What it is |
| --- | --- | --- |
| fireblocks.com | 8% | Category incumbent |
| bitgo.com | 6% | Category incumbent |
| cobo.com | 5% | Category incumbent |
| anchorage.com | 4% | Category incumbent |
| ripple.com | 3% | Adjacent infrastructure |
| openfort.io | 3% | Adjacent infrastructure |
| finextra.com | 2% | Trade media |
| fidelity.com | 2% | Incumbent brand, different segment |
| stablecoininsider.org | 2% | Niche publisher |
| eco.com | 2% | Adjacent vendor |

Figure 2. The ten domains that own the answer slot. Eleven of the thirty-seven concentration points sit on sites that do not compete with the cohort.

Formula 1. A concentration measure makes the shape clearer, squaring each domain's share.

```
Answer Concentration  (HHI-style, top 10)
  = Σ (share_i)²
  = 8² + 6² + 5² + 4² + 3² + 3² + 2² + 2² + 2² + 2²
  = 175

  An even split across fifty domains scores 200 across all fifty.
  Here ten domains alone reach 175. The slot is captured, not crowded.
```

When the audits recorded which specific pages beat the audited brand, the winners were pages like a 'best crypto wallet and custody' blog on cregis.com and a '5 infrastructure bets' post on finextra.com. Blog posts. List pages. Not category-defining assets. The slot is captured by a small set, and mostly by content rather than by product superiority.

## 04. Do cleaner sites get cited more?

**No, the opposite. Split the 35 crawled companies into the five that appear in AI answers and the thirty that do not, and on every technical-health measure the visible cohort is worse,** carrying twice the median high-priority problems of the companies that never appear.

Figure 3. Median high-priority site problems: the companies AI cites carry twice the technical debt of the ones it ignores.

Table 4. Site health, visible cohort vs invisible cohort.

| Measure (median) | Never appears (n=30) | Appears at all (n=5) |
| --- | --- | --- |
| High-priority site problems | 3 | 6 |
| Distinct defect classes | 40.5 | 50 |
| Pages crawled | 552 | 1,032 |

Two of the five visible companies sit in the top four messiest sites in the entire sample. Pulley carries 10 high-priority problems across 53 defect classes and still gets quoted. Range carries 7 high-priority problems, 618 images with no alt text, 25 pages set to stay out of search results, and 8 URLs blocked by its own robots file, and it is the most visible brand in the category at 12%. Meanwhile the cleanest site in the sample by high-priority count is Juno, at one problem. Juno's crawl found six URLs. Six. Its AI visibility is zero, because there is essentially nothing there to retrieve.

The correlation between high-priority problems and AI visibility is +0.25, and between pages crawled and visibility also +0.25. Both point the wrong way for a hygiene-first model, and neither is significant at n=35 (t = 1.48). Controlling for site size, the partial correlation drops to +0.19 and the effect plausibly collapses into one confound: bigger, older, more published sites accumulate more defects and more citations at the same time. The honest reading is not 'hygiene hurts.' It is that [hygiene does not appear anywhere in the signal](/blogs/ranking-isnt-visibility). Thirty companies did the tidy-up and got nothing for it, because tidiness was never the constraint.

## 05. Why does the clean-site inversion happen?

**Because retrieval is a gate, not a ranking factor. It is binary and it comes first, and once a page is through it, cleanliness contributes almost nothing to whether a model quotes it.** A workable model has three gates that multiply. The segment optimises gate 1 and dies at gate 2.

Gate 1: Retrievable

Binary. Robots, noindex, status, title, H1. Cheap. Weeks of work.

→

Gate 2: Answer match

Continuous. Does a page answer the question in the shape it was asked? This is where the segment dies.

→

Gate 3: Corroborated

Continuous. Third-party mentions, entity consistency, original data. Slowest to move.

Figure 4. Three multiplicative gates. Failing any one returns zero. Most of the cohort passed gate 1 and never built for gate 2.

Code 1. The three-gate model as a function. Failing any gate returns zero.

```
def probability_of_citation(page, query):
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
    return match * trust
```

Gate 1 is what a site crawl measures. It is necessary, it is cheap, and it is the only gate most of these companies have touched. Thirty of the thirty-five crawled sites passed it well enough to be readable and still scored zero, because they failed gate 2. There was no page. [Gate 2 is a supply problem, not a quality problem](/blogs/how-your-page-gets-retrieved): it does not ask whether your page is better, it asks whether a page exists that addresses the question in the shape the question was asked. Gate 3 is why fireblocks.com holds 8% and a cleaner site holds nothing. The segment has been optimising a gate it already passed.

## 06. Which buying stages is the segment missing?

**Almost all of them. Of 328 vendor-stage cells, 314 are empty, and Alternatives is a clean zero:** forty-one companies, four tools, and not one appearance on the single question type a buyer asks immediately before they choose.

Figure 5. 314 of 328 vendor-stage cells are empty. One company covers seven of eight stages; four cover one to three; thirty-six cover none.

Table 5. Mean visibility by buying stage, all 41 companies.

| Buying stage | Mean visibility | Companies with any presence | Stage type |
| --- | --- | --- | --- |
| Best-of / rankings | 0.90% | 4 | Mid |
| Pricing & ROI | 0.80% | 1 | Decision |
| Features & capabilities | 0.71% | 3 | Mid |
| Category discovery | 0.39% | 3 | Early |
| Buyer intent / evaluation | 0.32% | 1 | Decision |
| Integrations & stack | 0.20% | 1 | Mid |
| Comparisons | 0.12% | 1 | Decision |
| Alternatives | 0.00% | 0 | Decision |

Figure 5b. Mean visibility by buying stage across all 41 companies. Alternatives, the last question before a purchase, is a clean zero.

'Best alternatives to X' is not a hard page to write. It is a page nobody in this category has written from their own point of view. The tools will answer that question regardless, using somebody else's page. Averaged across the four decision stages, the segment's Decision-Stage Presence is 0.31%, and exactly one company, Range, has a non-zero value.

### What the one outlier actually did

Figure 6. Range's Answer Share by stage. Pricing sits at 33%, more than four times its overall share; Alternatives is zero, like everybody else.

Range is the only non-trivial signal available. Its profile is lopsided in a specific way: Pricing & ROI sits at 33%, more than four times its overall Answer Share; Features & capabilities is 17%; Buyer intent is 13%; category discovery, best-of, integrations and comparisons sit at 5% to 8%. The pattern is not 'Range is visible.' It is that Range has a small number of pages that answer cost and capability questions in the words a buyer uses, and those pages get lifted repeatedly. One page type, answered concretely, quoted repeatedly.

It is worth saying what Range did not do. It did not clean its site first: seven high-priority problems, 618 images with no alt text, 25 pages deliberately kept out of search, and 8 more blocked in robots. It is the messiest of the visible group by defect class count after Pulley, and four times more visible than anyone else. A company that spent the same quarter clearing those seven problems and published nothing would have moved from zero to zero. This argues for sequencing, not for leaving a site broken.

## 07. Do the four AI tools agree?

**No, and that breaks single-tool reporting. Range scores 17% on Claude and Gemini but 6% and 8% on ChatGPT and Google AI Overviews;** Cryptio and Pulley are the mirror image. There is no stable ordering of tools in this segment.

Figure 7. The five visible companies across all four tools. Three different shapes from five data points.

A brand that measures visibility on one tool is measuring one retrieval stack, one index, and one set of grounding rules. Range's number is 6% or 17% depending entirely on which tool you happened to open. [Any dashboard that reports 'our AI visibility' as a single figure](/blogs/share-of-model-measurement) without naming the tool and the prompt set is reporting noise. The unit that survives is the tuple: (prompt set, tool, date, binary named-or-linked). Everything above that is aggregation you chose.

## 08. What happens when AI cites no source at all?

**One in five losses had no page to beat. In 204 recorded question-and-loss rows, 43 came back with no citable source,** the model answered from parametric memory. That 21% is a corroboration problem, not a content problem, and it needs a different tactic.

Figure 8. Of recorded losses, 78.9% cited a real page you can outrank; 21.1% cited nothing, the model answered from memory.

This splits the problem into two jobs. In the 78.9% case a page exists and it beats you: a competitive content problem where you know the URL, can read it, and can publish something better shaped to the question. The winners here were blog posts on cregis.com, finextra.com, blockfills.com, jump.ai, and pulley.com. Reachable.

In the 21.1% case no page exists that the model considered worth citing. There is nothing to outrank. Here the lever is not the page. It is whether your brand is present in the corpora that shape the model's priors: [category roundups, trade media, directories, review sites, and other people's writing](/blogs/mentions-beat-links). You are competing for the model's unsourced recall. Most content plans in this segment only address the first case, because the first case is the one that shows up in a tool. The second case is invisible until you scan for it, which is the argument for scanning at all.

## 09. What does the crawl data actually say?

**That site health is uniform and template-level, not the constraint on visibility. Five template defects accounted for over 12,000 affected pages,** and site size (6 to 1,540 URLs) predicts nothing. Volume without decision-stage coverage is just volume.

Table 6. Defect prevalence across 35 crawled sites.

| Defect | Sites affected | Median pages per affected site | Total pages |
| --- | --- | --- | --- |
| Pages with very little text | 83% | 9 | 505 |
| Images heavy enough to slow the page | 83% | 68 | 3,106 |
| Titles cut off in results | 80% | 49 | 1,591 |
| Titles too long to show in full | 80% | 47 | 1,657 |
| Broken pages (404 and similar) | 77% | 2 | 534 |
| Images with no alt text | 77% | 96 | 3,951 |
| No canonical declared | 71% | 19 | 1,779 |
| No section headings | 71% | 14 | 928 |
| Images with no set size | 71% | 123 | 5,129 |
| Duplicate H1 across pages | 69% | 10 | 912 |
| Duplicate title across pages | 69% | 7 | 588 |
| No H1 at all | 63% | 6 | 565 |
| Points Google to a different page | 63% | 8 | 328 |
| Duplicate meta description | 60% | 20 | 703 |

Figure 9. Defect prevalence across the 35 crawled sites. Nothing exotic, these are template defaults nobody revisited.

Above roughly twenty affected pages per site, the defect is template-level: unsized images, missing alt text, heavy images, truncated titles, duplicate meta descriptions. One change to a layout file clears hundreds of pages at once. Below the line the defects are page-level and small: missing H1s at a median of six pages, broken links at two, insecure pages at two.

The exceptions are worth naming because they actually shut a gate. Arta Finance carries 304 pages with no title tag. Transak and Facet carry 191 and 185 broken pages. CoinSwitch blocks 61 URLs in its own robots file. Range sets 25 pages to noindex and blocks 8 more; Facet sets 50 to noindex. Every one of those is a page that can never be quoted, by Google or any AI tool, by the site's own instruction. Gate 1, failed deliberately, usually by accident.

## 10. What four numbers should you report instead?

**Answer Share, Stage Coverage Index, Decision-Stage Presence, and Citable Surface Ratio,** each cheap to compute from the audit data and each mapping directly onto a decision. Domain Rating and a single 'AI visibility' percentage are both too blunt to act on.

Formula 2. Answer Share (AS), the base rate.

```
AS   =  answers naming or linking the brand  /  (questions × tools)

  Answer Share. The base rate. Segment mean 0.46%.
```

Formula 3. Stage Coverage Index (SCI), breadth.

```
SCI  =  stages with AS > 0  /  total stages tested

  Stage Coverage Index. Breadth. 0.00 for 36 of 41 companies.
```

Formula 4. Decision-Stage Presence (DSP), the number that predicts revenue.

```
DSP  =  mean(AS_comparisons, AS_alternatives, AS_pricing, AS_buyer_intent)

  Decision-Stage Presence. The number that predicts revenue.
  Segment mean 0.31%. Non-zero for one of forty-one companies.
```

Formula 5. Citable Surface Ratio (CSR), which job you are doing.

```
CSR  =  losses with a cited source  /  total losses

  Citable Surface Ratio. Which job you are doing. Segment 0.789.
  The remaining 0.211 is a corroboration problem, not a content one.
```

Code 2. All four metrics from one answers-and-losses frame. Report them with the prompt set, tool list, and date attached.

```
import pandas as pd

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
    }
```

Table 7. What each number tells you to do.

| Metric | Segment value | If it is low, the fix is |
| --- | --- | --- |
| Answer Share | 0.46% mean | Nothing on its own. Read the other three first. |
| Stage Coverage Index | 0.00 for 36 of 41 | Publish. There is no page to retrieve. |
| Decision-Stage Presence | 0.31% mean | Alternatives page, comparison page, pricing page with real numbers. |
| Citable Surface Ratio | 0.789 | Below ~0.7, stop writing pages and go earn mentions. |

A number without the prompt set, the tool, and the date attached is not comparable to anything, including its own value last quarter. This is the same measurement discipline set out in [the RawMktg methodology](/methodology) and the [prompt-to-citation tracking stack](/blogs/prompt-to-citation-tracking).

Free Tool · Scorecard

Score your own GEO readiness

Run the gate check before you publish. Tick what is true of your buyer-path pages and get a readiness score with the gaps that matter most.

Crawlability & access 25 pts

llms.txt + llms-full.txt published

NoPartialYes

Server-rendered, no JS walls for bots

NoPartialYes

Fast load / good first contentful paint

NoPartialYes

Authority signals 30 pts

Earned media / third-party citations

NoPartialYes

Outbound links to high-authority sources

NoPartialYes

Named expert quotes with credentials

NoPartialYes

Information Gain 28 pts

Original first-party data / surveys

NoPartialYes

Proprietary framework or benchmark

NoPartialYes

Hard statistics throughout content

NoPartialYes

Structure & entity 17 pts

Scannable formatting (headers, tables, TL;DRs)

NoPartialYes

Schema markup (FAQ, SoftwareApp)

NoPartialYes

Consistent entity naming across the web

NoPartialYes

GEO readiness score

0/100

, 

At riskDevelopingCited-ready

A weighted self-assessment across the signals that drive AI citation. Weights reflect each signal's relative pull on Share of Model; your real-world results depend on execution quality and competitive context.

## 11. What order does the data argue for?

**Clear the retrieval blockers in two weeks because they are cheap, not because they move the number. Then publish the decision pages, Alternatives first,** then earn the outside mention in parallel, then re-measure the same prompts at day 90.

Figure 10. The sequence the findings argue for. Gate-1 cleanup is a fortnight; the number comes from the pages that follow.

Weeks 1 to 2, clear the retrieval blockers, only the ones that shut gate 1: robots-blocked URLs, noindex on pages that should be indexed, missing titles and H1s, broken pages in the buyer path. Median across the sample is three high-priority problems per site, a fortnight for one engineer. Weeks 2 to 8, publish the decision pages. [Alternatives first, because it is a segment-wide zero and therefore uncontested](/blogs/comparison-pages-ai-shortlists); then a comparison page against the rival sales names first; then a pricing page with real numbers. Weeks 4 to 12, earn the outside mention, in parallel, targeting the trade media and niche publishers already holding the answer slot. Day 90, re-measure the same prompts. The scan is the control, not the report.

Here is the page-level pattern the gate-2 work needs. Every decision page carries a direct answer above the marketing copy, and marks itself up so the facts do not have to be inferred, [the shape of a high-citation page](/blogs/anatomy-of-a-high-citation-page).

Free Tool · Optimizer

Optimize your own answer block

The decision-page pattern above, made live. Paste a draft answer and see whether a retriever can lift it cleanly, and what is dragging the score down.

Paste the answer that leads your H2

Load example

Gemini lifts the first self-contained answer after a heading. The 40-55 word window matches its single- and multi-pass extraction patterns.

Extraction score

0

-

Code 3. The decision-page shape: an answer block above everything, plus FAQ schema so the facts are not inferred.

```
<article>
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
</script>
```

Code 4. The gate-1 check, short enough that there is no excuse for it being a quarterly project.

```
# Gate 1 sanity pass. Run against the buyer-path URL list, not the whole site.
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
done < buyer-path-urls.txt
```

## 12. What can any segment take from this?

**Measure supply before quality, treat a clean site as table stakes rather than a strategy, write the uncontested Alternatives page,** use trade media and niche publishers as a third of the answer slot, and never report AI visibility as one number.

- **Measure supply before you measure quality.** 36 of 41 companies were absent because no page of theirs answered the question, not because their pages were worse. Count how many of your buyer's actual questions have a page at all before commissioning a quality review.
- **A clean site is table stakes, not a strategy.** The five visible companies carried a median of six high-priority problems and got quoted anyway. The three cleanest sites were quoted zero times between them.
- **The Alternatives page is the cheapest uncontested asset.** Forty-one companies, zero coverage. It has no competition and sits one question away from a purchase.
- **Trade media and niche publishers are a third of the answer slot.** Not competitors, publishers. A contributed piece or a directory listing puts your name inside the source before the answer is written, and it works on the 21% of questions where nothing is cited.
- **Never report AI visibility as one number.** Report Answer Share, Stage Coverage Index, Decision-Stage Presence, and Citable Surface Ratio, each with the prompt set, tool, and date. Range is a 6% brand and a 17% brand at the same time.
- **Fix templates, not pages.** Above roughly twenty affected pages, the defect lives in a layout file. Five template-level defects accounted for over 12,000 affected pages here. Five commits.

## 13. Method and honest limits?

**A fixed 48-question category prompt set across eight buying stages, run on four tools and scored binary named-or-linked, 192 pairs per company.** With five non-zero outcomes out of 41, every correlation is directional. The 314-of-328 empty-cell count is not a correlation, it is a count.

Site crawls covered every reachable URL on the production domain on the same day, checking status codes, robots directives, canonicals, titles, headings, meta descriptions, images, duplicate content, and readability. Six of the forty-one companies have no crawl in the dataset; cohort comparisons use the 35 that do.

What this data cannot tell you: whether visibility converts, because there is no downstream revenue attached; what any score was a month earlier; or whether invisibility is brand-specific or category-level model behaviour, since the prompt set is shared. The hygiene inversion in section 4 is a real pattern in this sample, and it would take a much larger sample to call it a law. The finding that needs no statistics is in section 6: 314 of 328 vendor-stage cells are empty. That is a count.

The one-line version

Across 41 companies in the Investing & Wealth cohort, 36 are invisible in AI answers because no page of theirs answers the buyer's question, not because their sites are broken. The five that appear are among the messiest. Retrieval is a gate you pass, then stop thinking about; the citations come from the pages you publish after it.

## Frequently asked questions

### Why does a clean, technically healthy website get zero AI citations?

Because technical health is a gate you pass, not a ranking factor. In a study of 41 investing and wealth companies, 30 of 35 crawled sites were clean enough to be readable and still scored zero AI visibility, because no page on them answered the buyer's actual question. Retrieval works in three multiplicative gates: retrievability (robots, noindex, status, title, H1), answer match (does a page address the question in the shape it was asked), and corroboration (third-party mentions). Most of the segment fixed gate 1 and never built for gate 2, so cleanliness contributed nothing to whether a model chose to quote them.

### What is the most common reason a brand is invisible in AI answers?

A supply problem, not a quality problem. Across the cohort, 314 of 328 vendor-stage cells were empty, meaning no page existed that answered the question for that buying stage. The tools answered anyway, using someone else's page. Before you commission a content quality review, count how many of your buyer's actual questions have a page at all, because the constraint is almost always the missing page, not a worse one.

### Why does an Alternatives page matter so much for AI visibility?

Because 'best alternatives to X' is a decision-stage question a buyer asks immediately before choosing, and in this cohort of 41 companies it was a clean zero: not one appeared on it, on any of four tools. The tools answer the question regardless, using a competitor's or a publisher's page. An Alternatives page written from your own point of view, with a plain answer block and real comparison numbers, is the cheapest uncontested asset in most categories and sits one question away from a purchase.

### How should you measure AI visibility instead of a single percentage?

Report four numbers, each with the prompt set, the tool, and the date attached: Answer Share (share of question-and-tool pairs that name or link you), Stage Coverage Index (how many buying stages register any presence), Decision-Stage Presence (mean Answer Share across comparisons, alternatives, pricing and buyer-intent questions), and Citable Surface Ratio (share of losses where a real page was quoted, versus nothing). A single 'AI visibility' figure hides which of these is the actual problem.

### Do ChatGPT, Google AI Overviews, Claude and Gemini agree on which brands to cite?

No. In this cohort the four tools produced three different shapes from five data points: one brand scored 17% on Claude and Gemini but 6% and 8% on ChatGPT and Google AI Overviews, while two others registered only on ChatGPT and Google and were invisible on Claude and Gemini. Each tool is a different retrieval stack, index, and set of grounding rules, so any single-tool 'AI visibility' number is noise unless you name the tool and the prompt set.

### Does fixing technical SEO improve AI visibility?

It removes a blocker, it does not produce visibility. Clearing robots-blocked URLs, noindex on pages that should rank, missing titles and H1s, and broken pages in the buyer path is necessary and cheap, roughly a fortnight of work. But in this sample the correlation between site cleanliness and AI visibility pointed the wrong way: the visible companies carried twice the median high-priority problems of the invisible ones. Fix the retrieval blockers because they are cheap, then publish the decision pages, because the citations come from the pages, not the cleanup.

### What do you do when an AI answer cites no source at all?

Treat it as a corroboration problem, not a content problem. In this dataset 21% of losses had no citable source: the model answered from its own priors with nothing linked. You cannot outrank a page that does not exist, so the lever is presence in the corpora that shape the model's recall, category roundups, trade media, directories, review sites, and other people's writing. That is cheaper than outranking an incumbent and it is the only thing that moves the fifth of questions where nothing is cited.

References

Figures 1 through 10 are original, computed from 41 category audits (7,872 scored AI answers and 23,870 crawled URLs, collected 25 August 2026). The sources below cover the retrieval, schema, and crawl concepts referenced.

1. [Generative Engine Optimization. Aggarwal et al., ACM SIGKDD 2024.](https://arxiv.org/abs/2311.09735)
2. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Lewis et al.](https://arxiv.org/abs/2005.11401)
3. [How Google AI Overviews select and link sources. Google Search Central.](https://developers.google.com/search/docs/appearance/ai-features)
4. [Block or allow AI crawlers: robots.txt and noindex. Google Search Central.](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
5. [Control what content appears in search with noindex. Google Search Central.](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
6. [FAQPage structured data reference. Schema.org.](https://schema.org/FAQPage)
7. [Intro to structured data markup for AI and search. Google Search Central.](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
8. [How Perplexity retrieves and cites sources. Perplexity Help Center.](https://www.perplexity.ai/hub)
9. [How ChatGPT search picks and cites web sources. OpenAI.](https://help.openai.com/en/articles/9237897-chatgpt-search)
10. [Core Web Vitals and page experience signals. Google Search Central.](https://developers.google.com/search/docs/appearance/core-web-vitals)
11. [Canonicalization and duplicate URLs. Google Search Central.](https://developers.google.com/search/docs/crawling-indexing/canonicalization)
12. [Answer Engine Optimization: writing for extractable answers. Search Engine Land.](https://searchengineland.com/library/generative-engine-optimization)

About rawmktg.

rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Sources: 41 category audits in the Investing & Wealth cohort collected 25 August 2026 (7,872 scored answers across ChatGPT, Google AI Overviews, Claude and Gemini; 23,870 crawled URLs across 35 sites). With five non-zero outcomes, correlations are directional, not conclusive.
