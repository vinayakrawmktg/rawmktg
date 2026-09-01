# The Link Liability

> Forty-one funded companies in investing, wealth, and digital assets, the cohort we call Investing & Wealth, audited on one day with one method. Read as a single dataset, their backlink profiles are not an asset that was built. They are a liability that was allowed to accumulate.

*Source: https://rawmktg.com/blogs/the-link-liability · rawmktg. by Vinayak Ravi*


## 01. Why read 41 backlink audits as one dataset?

**One audit tells you whether a company is bad. Forty-one audited identically, on the same day, against the same peer set, tell you whether the whole category is,** and those two conclusions lead to completely different budgets.

Most backlink analysis is written for one company, by someone paid to make that company feel a specific way about its numbers. That makes it useless for pattern spotting. You cannot tell whether a profile is bad or whether the whole category is bad.

This cohort, which we call Investing & Wealth, removes that problem. Forty-one companies were pulled on the same date, using the same tool, with the same definitions, and each was compared against the same forty-company peer group. They span consumer crypto exchanges, digital-asset infrastructure, wealth management and financial advice, capital-markets plumbing, and finance operations software. They range from pre-seed to post-Series-C, and from Domain Rating 2 to Domain Rating 84.

Read individually, each audit reads like a company problem. Read together, they read like a category problem, and the specific shape of that problem is worth more than any single result.

Table 1. The cohort. Sub-segments are assigned for analysis only and are not the companies' own categorisations.

| Sub-segment | n | Companies in the cohort |
| --- | --- | --- |
| Digital-asset infrastructure | 11 | Blueprint Finance, Dexif, Dispatch, Metallicus, Multis, Phantom, Plasma, Prime Trust, Stablecore, Utila, Zebec Network |
| Exchange and consumer trading | 10 | CoinSwitch, Conio, Fun, GoSats, Juno, Okcoin, Transak, Unocoin, Uphold, VALR |
| Finance ops and compliance software | 9 | Cryptio, Eqvista, GetVantage, IVIX, Panax, Pulley, Taxbit, Uptempo, interVal |
| Wealth and advice | 6 | Arta Finance, Dakota, Facet, Harness, Origin, Range |
| Capital-markets infrastructure | 5 | Baton Systems, Integral Development Corp, PCR Financial Aggregation, PowerPlan Inc, Tassat |

How to read the numbers in this piece

Referring domains: the number of separate websites that link to you. One site linking a hundred times counts once.

Dofollow domains: the subset of those sites that actually pass authority. A nofollow link tells search engines to ignore the endorsement.

Domain Rating (DR): Ahrefs' 0 to 100 score for how strong a domain looks, built almost entirely from dofollow referring domains.

Ever linked: every domain that has ever pointed at the site, including ones that no longer do. The gap between this and referring domains is decay.

## 02. How much of a backlink profile is already dead?

**Across the cohort, 15,134 domains have linked to these 41 companies at some point. Today 2,126 still do, 1,044 pass authority, and only 567 sit at DR 50 or above,** the point at which a link starts to move anything. That is 3.7 percent of every relationship ever formed.

Start with the number that frames everything else. Across the cohort, 15,134 domains have linked to these 41 companies at some point in their history. Today, 2,126 of them still do. That is an 86 percent pooled loss rate.

It gets narrower. Of the 2,126 domains still linking, 1,044 pass authority. The rest are nofollow, which means the linking site has explicitly told search engines to ignore the endorsement. And of those 1,044, only 567 sit at DR 50 or above.

15,134 relationships were formed. 567 of them currently carry weight. That is 3.7 percent.

Figure 1. The four-step collapse from historical link relationships to links that actually carry authority. Pooled across all 41 companies.

Almost every marketing dashboard in this segment reports the first number and none report the last. A founder looking at 2,126 referring domains and a founder looking at 567 domains that pass real authority are looking at the same reality and will make different decisions about it. The gap is a factor of four between referring domains and domains that matter, and a factor of twenty-seven between total historical relationships and the same figure.

### This is not a small-company problem

The obvious explanation would be that the weak profiles are the young ones, and that scale fixes it. The data does not support that. The company with the highest Domain Rating in the cohort has lost 73 percent of its historical linking domains. The company with the most historical relationships, 4,400 of them, retains 146. Decay does not care how big you got.

## 03. Where does the average link actually come from?

**A site nobody reads. 58 percent of the cohort's live referring domains sit at DR 29 or below, and 36 percent sit below DR 10,** a band that is scraper sites, expired-domain networks, jobs aggregators, and directories nobody visits on purpose.

Figure 2. Domain Rating distribution of all live referring domains in the cohort. 58 percent sit at DR 29 or below.

Table 2. Where the cohort's link equity actually sits. Only 26.7 percent of all live referring domains clear DR 50.

| Strength of the linking site | Sites | Share of cohort | What a link from here is worth |
| --- | --- | --- | --- |
| Very strong (DR 70+) | 297 | 14.0% | Moves the needle. Rare and usually earned. |
| Strong (DR 50 to 69) | 270 | 12.7% | Meaningful. Trade press, real directories, real partners. |
| Middling (DR 30 to 49) | 321 | 15.1% | Marginal on its own. Useful in volume. |
| Weak (DR 10 to 29) | 466 | 21.9% | Close to zero. Costs the same to acquire. |
| Near zero (DR 0 to 9) | 772 | 36.3% | Zero, and often worse than zero. |

Thirty-six percent of every site linking to this cohort has a Domain Rating below 10. That band is not a mix of small blogs and niche publications. Read domain by domain, it is scraper sites, expired-domain networks, jobs aggregators that republish company descriptions, and directories nobody has visited on purpose.

The median company in the cohort has eight referring domains at DR 50 or above. Eleven of the 41 have zero domains at DR 70 or above. That is the real starting line, and it is much closer to zero than any referring domain count suggests.

## 04. Is Domain Rating a reliable scoreboard?

**No. Fit against live dofollow domains gives Pearson r = 0.45 with a 14.6-point residual spread, so DR predicts almost nothing about any single company.** It is computed from a link graph crawled on a delay, so equity decays slowly inside the model even after the link disappears.

Domain Rating is the number every board deck in this segment quotes. It is also the number that correlates worst with what the company currently has.

Figure 3. Domain Rating plotted against live dofollow referring domains, log scale. The fit is real but loose, and three companies sit far off it.

Formula 1. The fit, and why it is almost useless as a per-company predictor.

```
DR  ≈  13.6 × log₁₀(D_follow + 1)  +  32.9

  D_follow   live dofollow referring domains
  Pearson r = 0.45   ·   residual sd = 14.6 DR points
  A ~15-point residual spread means DR predicts almost nothing
  about any single company. It tells you where you have been.
```

A residual spread of nearly 15 DR points means the model is almost useless as a predictor for any individual company, and that is the point. Two companies in this cohort sit at DR 45 and DR 36 with zero live referring domains between them. Every link either of them ever had is gone, and their scores have not caught up. Another sits at DR 35 with 8 referring domains and 5,283 backlinks, because a single site links to it thousands of times from a sitewide footer.

The reason for the lag is structural. Third-party authority scores are computed from a link graph that is crawled on a delay, and historical equity decays slowly inside the model even after the underlying link disappears. [DR tells you where you have been; live visibility is a different question entirely](/blogs/ranking-isnt-visibility). It does not tell you where you are.

Code 1. Run this against your own export before you quote a referring domain count to anyone.

```
# Effective Authority Domains from an Ahrefs referring-domains export.
# The whole scoreboard, in nine lines.
import pandas as pd

rd     = pd.read_csv("referring_domains.csv")
live   = rd[rd["Lost status"].isna()]            # still linking today
follow = live[live["Dofollow links"] > 0]        # actually passes authority
ead    = follow[follow["Domain rating"] >= 50]   # from a site worth citing

print(f"Referring domains reported : {len(rd):>5}")
print(f"Still live                 : {len(live):>5}")
print(f"Passing authority          : {len(follow):>5}")
print(f"Effective Authority Domains: {len(ead):>5}")   # <- the real number
```

## 05. Why is decay the default state of a link profile?

**The median company has lost 74 percent of every domain that has ever linked to it, and nothing in the cohort suggested anyone was monitoring it.** Thirty-two of the 40 companies with a historical count have lost more than half.

Figure 4. Loss milestones across the cohort. Higher authority offers no protection: the highest-DR company has lost 73 percent, the largest profile 96.7 percent.

Decay is not one thing. Pulled apart across the cohort, it is four things, and only one of them is anybody's fault.

- **The page moved or was deleted.** A publisher redesigns, an article is archived, a URL changes. The link exists in nobody's intent to remove it and disappears anyway.
- **The publisher closed.** Trade sites in this category churn fast. A whole domain going offline removes every link it held.
- **The syndication window expired.** Newswire distribution places a release on dozens of sites. Many of those sites purge on a schedule.
- **The company changed its own URL.** Rebrands, path restructures, and www-to-apex migrations quietly break inbound links, and this is the one that is entirely self-inflicted.

The cost of ignoring decay compounds. A recovered link costs one email. An equivalent new link costs a pitch, a relationship, and usually a piece of content. Across this cohort, 13,037 lost relationships are sitting unworked while the same companies pay for new ones.

### A metric worth adopting: Live Equity Ratio

Formula 2. One number that separates a profile that was built from one that merely happened.

```
Live Equity Ratio  =  D_follow, live  ÷  D_ever

  D_follow, live   live dofollow referring domains
  D_ever           every domain that has ever linked
  Pooled cohort 6.9%.  Median company 13%.
  A retention measure, not a volume measure. Read it next to the count.
```

Figure 5. Live Equity Ratio, all 40 companies with historical data. Half the cohort has kept less than 13 percent of what it once had.

The pooled ratio across the cohort is 6.9 percent. The median company sits at 13 percent. Fifteen of the 40 companies with historical data sit below 10 percent, which means more than nine in ten relationships they ever formed are now doing nothing for them.

One caveat worth stating plainly. A high Live Equity Ratio is not automatically good. The company at 100 percent has eight referring domains and has never lost one, because it never acquired enough to lose any. The ratio is a retention measure, not a volume measure, and it should always be read next to the absolute count.

Code 2. Decay is invisible unless something diffs it on a schedule. Nothing in the cohort suggested anyone was doing this.

```
# Monthly decay monitor. Diffs this month's referring domains against last
# month's, and writes a recovery queue sorted by what the lost link was worth.
import pandas as pd

prev = pd.read_csv("rd_2026_07.csv").set_index("Domain")
curr = pd.read_csv("rd_2026_08.csv").set_index("Domain")

lost   = prev.index.difference(curr.index)
gained = curr.index.difference(prev.index)

queue = (prev.loc[lost]
             .query("`Dofollow links` > 0 and `Domain rating` >= 30")
             .sort_values("Domain rating", ascending=False)
             .loc[:, ["Domain rating", "Domain traffic", "Referring page URL"]])

queue.to_csv("recovery_queue.csv")
print(f"lost {len(lost)}  gained {len(gained)}  net {len(gained) - len(lost):+d}")
print(f"worth chasing: {len(queue)}")
```

## 06. Why do all the backlinks point at the homepage?

**Of the 37 companies where page-level concentration was measured, 31 send 95 percent or more of their backlinks to a single URL and 20 send 100 percent.** The median is 100 percent, which produces a site with exactly one strong page, and it is almost never the one a buyer needs to find.

Figure 6. Share of all backlinks pointing at the homepage, by concentration band. Twenty of 37 companies sit at 100 percent.

This is normal for a young profile and it is a serious constraint for a company trying to rank anything specific. Authority flows through a site from the pages that receive it. A profile where every link lands on the homepage produces a site with exactly one strong page, and that page is almost never the one a buyer needs to find.

It also caps what content marketing can do. Publishing a comparison page, a pricing explainer, or an integration guide is only half the work. If no external link ever points at it, it competes on [internal linking](/blogs/internal-linking-for-ai-retrieval) alone against pages that have external authority of their own.

The fix is not complicated and it is almost entirely a question of what you point people at. Original data goes on its own URL. A tool or calculator goes on its own URL. A [comparison or 'best X for Y' page that a buyer and an AI assistant both pull from](/blogs/comparison-pages-ai-shortlists) goes on its own URL. Then every pitch, every profile, and every release links there rather than to the front door.

Table 3. Link destination by link type. Only one row in this table belongs on the homepage.

| What earns the link | Where the link should land | Why the homepage is the wrong target |
| --- | --- | --- |
| Original data or a benchmark | A dedicated research URL | The citation is to the finding, not the company |
| A free tool or calculator | The tool's own page | Repeat linkers point at the utility |
| A funding or product announcement | Homepage is fine here | Brand-level news genuinely is brand-level |
| A category explainer or glossary | The glossary entry itself | Builds a rankable page, not a stronger front door |
| A comparison or alternatives page | The comparison page | This is the page buyers and AI assistants actually pull from |

## 07. Are the strongest links actually passing authority?

**Half are not. Of the 283 strongest placements in the cohort, 49 percent are nofollow,** because newswire syndication, jobs boards, company directories, and most large media default to nofollow on outbound links.

Figure 7. The 283 strongest placements in the cohort, split by whether they pass authority.

Each audit named the strongest placements a company had already earned. Across the cohort that is 283 links from 192 distinct domains, and it is the closest thing to a highlight reel this segment has. Forty-nine percent of them are nofollow. These are not bad links, and the traffic and credibility they carry is real. But in terms of the authority they transfer, they are decorative.

A press release that lands on twelve sites can produce twelve links and zero authority transfer. None of this is an argument against those placements, it is an argument against counting them as link building. And for AI search specifically the calculus shifts again: [an unlinked brand mention on a trusted site now corroborates a retrieval system directly](/blogs/mentions-beat-links), which is why the reach these placements carry is worth tracking on its own axis, just not in the link column.

The practical version is that the cohort's median profile has 3.1 links per referring domain and 22 percent of all links marked nofollow, and the top-of-profile links skew far more nofollow than the tail does. The strongest-looking part of the profile is the least load-bearing part.

## 08. Does the spam in a backlink profile look like spam?

**No. Across the cohort 651 flagged domains sit against 2,126 live referring domains, and 31 percent of the flagged ones carry DR 30 or above.** If your filter for a bad link is 'low DR', you will keep a third of them.

Figure 8. What the 194 named flagged domains are. A site with no readers and outright link farms account for nine in ten.

Table 4. Taxonomy of 194 named spam referring domains across 22 companies.

| Type of flagged domain | Count | Share | What it looks like in a report |
| --- | --- | --- | --- |
| A site with no readers | 99 | 51.0% | Real-looking domain, near-zero traffic, syndicated filler |
| A link farm | 78 | 40.2% | Hundreds of unrelated outbound links per page |
| A link selling site | 9 | 4.6% | Paid placement, often disclosed nowhere |
| A throwaway domain | 4 | 2.1% | Registered recently, no history, no purpose |
| Other flagged | 4 | 2.1% | Caught by the tool, unclassified on manual read |

Twenty-six of the 41 companies had at least one referring domain flagged as spam. The DR distribution is the part worth sitting with. Thirty-one percent of these flagged domains carry a Domain Rating of 30 or above and seven percent clear DR 50. One domain in the cohort appears as a flagged referrer for seven different companies, and nineteen distinct spam domains appear across more than one company. That is a signature: the same link networks are working the same target list, and several of these companies are receiving links they never asked for and are not aware of.

The part that gets missed

Two companies in this cohort have profiles that are 92 percent and 63 percent flagged spam by volume. Neither of them bought those links in any account anyone still has access to.

Negative SEO is rare. Inherited spam from an old agency, an old growth hack, or an unrelated network scraping funding announcements is not. Either way the cleanup is the same job.

## 09. Do competitor gap analyses find real link opportunities?

**They find the floor, not the ceiling. The cohort's 803 identified opportunities resolve to just 32 distinct domains, and 62 percent are directories and newswire hosts,** because commodity links are the ones every peer already has. Average pairwise overlap between any two companies' lists is 0.69.

Each audit produced a list of domains that link to several peers and not to the audited company. Across the cohort that is 803 identified opportunities. They resolve to 32 distinct domains. Nineteen of those 32 appear in 32 or more of the 41 audits. Pick two companies at random from this cohort, in different sub-segments, at different stages, on different continents, and roughly seven in ten of their link opportunities are the same domains.

Figure 9. The most frequently identified link opportunities, and how many of the 41 audits named each.

Figure 10. Composition of the 803 identified opportunities, by type of site. Directory listings and wire hosts are 62 percent of the total.

Sixty-two percent of what this segment calls a link opportunity sits in one bucket: company directories, profile pages, and newswire syndication hosts. Split that bucket and 40 percent of all opportunities are directory listings you can [claim yourself as part of an entity-home pass](/blogs/becoming-an-entity) in an afternoon, while 22 percent are wire distribution hosts that cost money rather than effort. Seventeen percent is trade or industry media, and nine percent is a publishing platform where you write the content yourself.

There are two honest readings and both are useful. The commodity layer is genuinely unclaimed: most of these companies have not done the free, permanent, thirty-minute version of link building, and closing it is the correct first move. But a gap analysis built from peer overlap will always converge on commodity links, because commodity links are the ones every peer has. [The link nobody in your category has earned yet](/blogs/authority-seeding-ai-llm-trust) will never appear in a competitor gap list. Claim the 32 domains because they are free. Do not mistake finishing that list for having a link strategy.

Table 5. Thirteen of the most repeated opportunities. Only two of them require a pitch. The rest need a form, a login, or a budget.

| Domain | Type | Named in | DR | Median peers with the link |
| --- | --- | --- | --- | --- |
| medium.com | Publishing platform | 38 of 41 | 94 | 3 |
| owler.com | Directory | 37 | 72 | 4 |
| substack.com | Publishing platform | 37 | 94 | 4 |
| newswire.com | Directory / wire | 37 | 87 | 4 |
| cortera.com | Directory | 37 | 54 | 4 |
| finopotamus.com | Trade media | 37 | 56 | 4 |
| crunchbase.com | Directory | 36 | 91 | 5 |
| rocketreach.co | Directory | 36 | 75 | 5 |
| fortune.com | Trade media | 36 | 91 | 5 |
| contactout.com | Directory | 35 | 74 | 6 |
| c212.net | Wire syndication | 34 | 90 | 7 |
| builtin.com | Directory | 34 | 86 | 7 |
| prnewswire.com | Wire | 29 | 92 | 12 |

## 10. Where do the sub-segments differ?

**The failure is universal; the shape of it is not. Exchanges acquired reach and kept almost none of it, so their fix is recovery.** Digital-asset infrastructure never acquired links at all, so its fix is straightforward acquisition. Same segment, opposite first moves.

Figure 11. Median position by sub-segment across three link measures. The Live Equity Ratio, in the table below, tells you whether the problem is acquisition or retention.

Table 6. Sub-segment medians. The Live Equity Ratio column tells you whether the problem is acquisition or retention.

| Sub-segment | Median DR | Median live ref domains | Median domains passing value | Median LER | The characteristic failure |
| --- | --- | --- | --- | --- | --- |
| Exchange and consumer trading | 54 | 43 | 20 | 6% | Acquired reach through wires and coverage, retained almost none of it |
| Finance ops and compliance software | 47 | 20 | 8 | 18% | Thin but clean. Nobody has been asked for a link. |
| Wealth and advice | 44 | 19 | 14 | 14% | Regulated caution has been read as a reason not to publish anything citable |
| Digital-asset infrastructure | 44 | 7 | 4 | 33% | Never acquired links at all. High retention of a very small base. |
| Capital-markets infrastructure | 37 | 21 | 13 | 5% | Long-established, and the links that built the profile have almost all expired |

Exchange and consumer trading has the highest median Domain Rating in the cohort and the second-lowest Live Equity Ratio. These companies did the acquisition work, then stopped maintaining any of it. Their correct first move is recovery, not acquisition, and it is cheap. Digital-asset infrastructure is the mirror image: median seven live referring domains and the highest retention rate in the cohort, because there was never anything to lose. Their correct first move is straightforward acquisition, starting with the free tier.

Capital-markets infrastructure is the group to watch. It has the highest median historical domain count in the cohort at 362, a 91 percent median loss rate, and the lowest median Domain Rating at 37. Time built these profiles and time dismantled them while nobody was looking at the numbers.

## 11. What should companies actually do about it?

**Nine specific things, in the order the data supports doing them.** Audit before you acquire, report Effective Authority Domains, diff monthly, and work the recovery queue before the acquisition queue.

Figure 13. The ninety-day sequence the audits converge on independently. The ordering carries more weight than the tactics.

Keep

Live, dofollow, DR-worthy. Leave it and protect it.

→

Recover

Lost from a live publisher. One email each.

→

Disavow

Flagged on a manual read. Filed, with a reason.

Figure 12. The triage pass. Every domain in the profile goes into exactly one of three columns before any new link is bought or pitched.

### 1. Audit before you acquire

Twenty-six of the 41 companies had flagged domains sitting in their profile, and in most the genuine layer underneath was thin. Adding links to a profile you have not sorted means the reporting stays broken and the cleanup gets more expensive. The triage pass is two weeks of manual work and it is the only step that must come first.

### 2. Report Effective Authority Domains, not Domain Rating

DR lags, it can be inflated by a single sitewide footer link, and in this cohort it correlates at r = 0.45 with what a company actually has. Count live dofollow domains at DR 50 or above. It is a smaller, harder, more honest number, and the [off-site authority scorecard](/tools/off-site-authority-scorecard) computes it from an export.

### 3. Diff your referring domains every month

The cohort's median loss rate is 74 percent. Nothing in the data suggested anyone was monitoring it. A monthly diff against last month's export takes minutes and produces a recovery queue that is cheaper to work than any acquisition list.

### 4. Work the recovery queue before the acquisition queue

A lost link from a live publisher is one email. Across this cohort there are 13,037 lost relationships, and a meaningful share are page moves that a single message would fix.

### 5. Claim the free tier once, properly

Forty percent of the identified opportunities are self-serve directory and profile listings. They are free, they are permanent, and almost nobody in this cohort had claimed them. Do it in one afternoon and then stop thinking about it. The 22 percent that are wire hosts are a separate budget decision, not a free win.

### 6. Stop counting nofollow placements as link building

Half the strongest placements in this cohort pass no authority. Count them as reach, count them as credibility, and keep them out of the link column.

### 7. Give links somewhere to land other than the homepage

The cohort median is 100 percent homepage concentration. Every piece of original data, every tool, and every methodology page you publish should be the destination of the pitch that promotes it.

### 8. Publish one thing per quarter that has no substitute

Original numbers from your own platform, a survey, or a benchmark. It is the only category of page in this analysis that reliably attracts links from sites you did not contact, because [there is nowhere else to get the data](/blogs/mentions-beat-links).

### 9. Re-run the same audit on a schedule

Same tool, same definitions, same date each quarter. Most of what is wrong in this cohort is not a strategy failure. It is the absence of anyone checking.

## 12. What scoreboard should replace Domain Rating?

**Four numbers, all computable from a single referring-domains export and all harder to game than the one most teams report.** Effective Authority Domains, Live Equity Ratio, Link Liability Ratio, and Page Concentration.

Table 7. Four metrics and the cohort baseline for each. Every one of them is worse than the number it replaces, which is the point.

| Metric | Definition | Cohort median | Read it as |
| --- | --- | --- | --- |
| Effective Authority Domains (EAD) | Live dofollow referring domains at DR 50+ | 8 | The real size of your link position |
| Live Equity Ratio (LER) | Live dofollow referring domains / domains ever acquired | 13% | Whether you retain what you win |
| Link Liability Ratio (LLR) | (nofollow-only + flagged domains) / live referring domains | 47% | How much of the profile is decoration |
| Page Concentration | Share of backlinks pointing at a single URL | 100% | Whether authority can reach anything but the homepage |

These four sit alongside the discipline that governs everything else RawMktg publishes: [measure the same thing the same way every time](/methodology), and read link position next to [share of model and citation measurement](/blogs/share-of-model-measurement) rather than in place of it. Run the scoreboard quarterly and you will know more about your link position than any DR chart will tell you.

Code 3. Fifteen lines. Run it quarterly and you will know more about your link position than any DR chart will tell you.

```
# The four-metric scoreboard, from one Ahrefs referring-domains export.
import pandas as pd

rd     = pd.read_csv("referring_domains.csv")   # includes lost rows = domains ever acquired
live   = rd[rd["Lost status"].isna()]
follow = live[live["Dofollow links"] > 0]

ead  = (follow["Domain rating"] >= 50).sum()
ler  = len(follow) / max(len(rd), 1)
llr  = ((len(live) - len(follow)) + live["Spam"].fillna(0).astype(bool).sum()) / max(len(live), 1)

bl   = pd.read_csv("backlinks.csv")
conc = bl["Target URL"].value_counts(normalize=True).iloc[0]

print(f"EAD  {ead:>6}      (cohort median 8)")
print(f"LER  {ler:>6.1%}      (cohort median 13%)")
print(f"LLR  {llr:>6.1%}      (cohort median 47%)")
print(f"Conc {conc:>6.1%}      (cohort median 100%)")
```

Code 4. Disavow format. Comments are ignored by Google and are the only record of why you filed each one, so write them.

```
# The disavow file Google Search Console expects. One domain per line.
# Only after a manual pass. Automated classification gets this wrong both ways.

# Flagged: link farm, 400+ unrelated outbound links per page, dofollow
domain:example-linkfarm.tld

# Flagged: syndicated filler, zero organic traffic, dofollow
domain:example-noreaders.tld

# Flagged: paid placement network, appears across 7 companies in one sector
domain:example-network.tld
```

## 13. What can this analysis not tell you?

**It establishes that a segment's link profiles are thin, decayed, and concentrated. It does not measure what that costs in traffic, pipeline, or AI-assistant citations,** because none of those were measured here. What it does show is that the cheapest available improvements are sitting unclaimed in front of everyone at once.

Every figure in this piece is computed from 41 backlink audits, the Investing & Wealth cohort, produced on 26 August 2026 from Ahrefs referring domains, backlinks, and link intersect data, each benchmarked against the same forty-company peer set. Sub-segment assignment is ours and is for analysis only. Four limitations are worth stating. A companion teardown scores the same Investing & Wealth cohort on exactly that: [clean sites, and zero AI citations](/blogs/clean-site-zero-citations).

- **Spam classification is partly manual.** Ahrefs' flag was the starting point and each list was read by hand. Another analyst would draw the line differently, particularly in the DR 30 to 50 band.
- **Ahrefs' index is not the web.** Referring domain counts, historical counts, and traffic estimates are one crawler's view. Directionally sound, not absolute.
- **This is a single point in time.** Decay rates here are cumulative history, not a measured rate per period. A monthly series would be a much stronger dataset and is the obvious follow-up.
- **Some figures exclude companies with missing data.** Four companies had no page-concentration figure and one had no historical domain count. Every chart states its own n.

The one-line version

Across the 41 funded companies in the Investing & Wealth cohort, 96.3 percent of every link relationship ever formed is currently doing nothing. The work required to change that is unglamorous, mostly free, and almost entirely unstarted.

## Frequently asked questions

### What is a healthy backlink profile size for a funded startup?

Count Effective Authority Domains, not referring domains. That is the number of live, dofollow referring domains at Domain Rating 50 or above. Across 41 audited companies in investing, wealth, and digital assets the median was 8 and the lower quartile was 2, with sixteen of 41 below five. A raw referring-domain count in the hundreds routinely collapses to single digits once you strip out lost links, nofollow links, and weak domains, so the honest starting line is almost always far lower than the dashboard number.

### Why is Domain Rating a misleading metric?

Domain Rating is computed from a link graph that is crawled on a delay, so historical equity decays slowly inside the score even after the underlying links disappear. Across this cohort DR correlated with live dofollow referring domains at Pearson r = 0.45 with a 14.6-point residual spread, which makes it almost useless as a per-company predictor. Companies in the cohort held DR 45 with zero live referring domains, and DR 35 inflated by a single sitewide footer link repeated thousands of times. DR tells you where you have been, not where you are.

### How do I find lost backlinks worth recovering?

Export your referring domains monthly and diff this month against last. Any domain present last month and absent this month is a lost link; filter those to the ones that were dofollow and at DR 30 or above, and sort by Domain Rating to get a recovery queue. Most losses are page moves or redesigns, and a recovered link from a live publisher costs one email, versus a pitch, a relationship, and a piece of content for an equivalent new one. Across the audited cohort there were 13,037 lost relationships sitting unworked.

### Are nofollow backlinks worthless?

For authority transfer, yes, a nofollow link tells search engines to ignore the endorsement, and 49 percent of the strongest placements in this cohort were nofollow. But they are not worthless: newswire, directories, and large media carry real reach and credibility, and for AI search an unlinked or nofollow brand mention on a trusted site now corroborates a retrieval system directly. Count them as reach, not as link building, and keep them out of the link column on your scoreboard.

### Should I disavow spammy backlinks?

Only after a manual pass, and only for clear link farms, paid-placement networks, and syndicated filler. A low-DR filter is not enough: 31 percent of the flagged domains in this cohort carried DR 30 or above and 7 percent cleared DR 50. Automated classification gets this wrong in both directions, so read the list by hand, write the reason for each entry as a comment in the disavow file, and remember that much of this spam is inherited rather than bought.

### Why do all my backlinks point at my homepage, and does it matter?

It is normal for a young profile, because announcements, directory listings, and social profiles all default to the front door, and the audited cohort median was 100 percent homepage concentration. It matters because authority flows through a site from the pages that receive links, so a profile where everything lands on the homepage produces exactly one strong page, and it is rarely the one a buyer or an AI assistant needs. Give original data, tools, and comparison pages their own URLs and point every pitch there.

### What should replace Domain Rating on our reporting?

Four numbers from a single referring-domains export: Effective Authority Domains (live dofollow domains at DR 50+, cohort median 8), Live Equity Ratio (live dofollow domains divided by domains ever acquired, median 13 percent), Link Liability Ratio (nofollow-only plus flagged domains over live referring domains, median 47 percent), and Page Concentration (share of backlinks on a single URL, median 100 percent). Each is smaller, harder to game, and more honest than DR.

References

Figures 1 through 13 are original, computed from 41 backlink audits (Ahrefs referring domains, backlinks, and link intersect, pulled 26 August 2026). The sources below cover the metrics and definitions used.

1. [Ahrefs' Domain Rating (DR): what it is and how it is calculated. Ahrefs.](https://ahrefs.com/blog/domain-rating/)
2. [Referring domains vs backlinks: what is the difference? Ahrefs.](https://ahrefs.com/blog/referring-domains-vs-backlinks/)
3. [What are nofollow links, and how do they work? Ahrefs.](https://ahrefs.com/blog/nofollow-links/)
4. [Link intersect: find who links to competitors but not you. Ahrefs.](https://ahrefs.com/blog/link-intersect/)
5. [How to find and reclaim lost backlinks. Ahrefs.](https://ahrefs.com/blog/lost-backlinks/)
6. [Link building for SEO: the beginner's guide. Ahrefs.](https://ahrefs.com/blog/link-building/)
7. [Disavow links to your site. Google Search Central Help.](https://support.google.com/webmasters/answer/2648487)
8. [Qualify your outbound links to Google (rel=nofollow, sponsored, ugc). Google Search Central.](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
9. [What is link equity (link juice) and how does it work? Moz.](https://moz.com/learn/seo/link-equity)
10. [Anchor text and the flow of PageRank through a site. Moz Beginner's Guide to SEO.](https://moz.com/beginners-guide-to-seo)
11. [The decay of backlinks over time. Search Engine Journal.](https://www.searchenginejournal.com/link-decay-seo/)
12. [Negative SEO and toxic link audits: what actually matters. Search Engine Land.](https://searchengineland.com/guide/what-is-link-building)
13. [Press release syndication and nofollow: what wire links are worth. PR Newswire resources.](https://www.prnewswire.com/resources/)
14. [Crunchbase, Owler and business directories as citable entity records. Crunchbase.](https://about.crunchbase.com/)

About rawmktg.

rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Sources: 41 Ahrefs backlink audits pulled 26 August 2026, each benchmarked against the same forty-company peer set; Ahrefs, Moz, and Google Search Central documentation on referring domains, Domain Rating, nofollow, link equity, and disavow. Correlations are directional, not causal; the index is one crawler's view of the web.
