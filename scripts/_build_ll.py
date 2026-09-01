#!/usr/bin/env python3
"""SCRATCH: build blogs/the-link-liability.html (backlink cohort teardown). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="the-link-liability"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-08-27"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x").replace("−","-"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav',"</nav>")
NEWS=sl('<section class="newsletter-section',"</section>"); FOOT=sl('<footer class="site-foot',"</footer>")
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

HEADLINE="The Link Liability"
DECK=("Forty-one funded companies in investing, wealth, and digital assets, the cohort we call Investing & Wealth, audited on one day with one "
      "method. Read as a single dataset, their backlink profiles are not an asset that was built. They are a liability that was allowed to accumulate.")
DESC=("41 backlink audits across investing, wealth and digital assets, read as one dataset: only 3.7% of every link relationship ever formed still carries authority. The decay, the homepage trap, the spam that isn't low-DR, and the four-metric scoreboard that should replace Domain Rating.")
DATANOTE=("Every figure is computed from 41 backlink audits, the Investing & Wealth cohort, produced on 26 August 2026 from Ahrefs referring "
          "domains, backlinks, and link intersect data, each benchmarked against the same forty-company peer set. Sub-segment assignment is ours and is for analysis only. "
          "Correlations are directional, not causal; the index is one crawler's view of the web, not the web.")

# ---------- formulas (ASCII, bypass norm) ----------
FORM_DR=r'''DR  ≈  13.6 × log₁₀(D_follow + 1)  +  32.9

  D_follow   live dofollow referring domains
  Pearson r = 0.45   ·   residual sd = 14.6 DR points
  A ~15-point residual spread means DR predicts almost nothing
  about any single company. It tells you where you have been.'''

FORM_LER=r'''Live Equity Ratio  =  D_follow, live  ÷  D_ever

  D_follow, live   live dofollow referring domains
  D_ever           every domain that has ever linked
  Pooled cohort 6.9%.  Median company 13%.
  A retention measure, not a volume measure. Read it next to the count.'''

# ---------- code blocks ----------
CODE_EAD=r'''# Effective Authority Domains from an Ahrefs referring-domains export.
# The whole scoreboard, in nine lines.
import pandas as pd

rd     = pd.read_csv("referring_domains.csv")
live   = rd[rd["Lost status"].isna()]            # still linking today
follow = live[live["Dofollow links"] > 0]        # actually passes authority
ead    = follow[follow["Domain rating"] >= 50]   # from a site worth citing

print(f"Referring domains reported : {len(rd):>5}")
print(f"Still live                 : {len(live):>5}")
print(f"Passing authority          : {len(follow):>5}")
print(f"Effective Authority Domains: {len(ead):>5}")   # <- the real number'''

CODE_DECAY=r'''# Monthly decay monitor. Diffs this month's referring domains against last
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
print(f"worth chasing: {len(queue)}")'''

CODE_SCORE=r'''# The four-metric scoreboard, from one Ahrefs referring-domains export.
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
print(f"Conc {conc:>6.1%}      (cohort median 100%)")'''

CODE_DISAVOW=r'''# The disavow file Google Search Console expects. One domain per line.
# Only after a manual pass. Automated classification gets this wrong both ways.

# Flagged: link farm, 400+ unrelated outbound links per page, dofollow
domain:example-linkfarm.tld

# Flagged: syndicated filler, zero organic traffic, dofollow
domain:example-noreaders.tld

# Flagged: paid placement network, appears across 7 companies in one sector
domain:example-network.tld'''

out=[]
A=out.append

# ===== 01 =====
A(sec("01","cohort","Why read 41 backlink audits as one dataset?",
      "One audit tells you whether a company is bad. Forty-one audited identically, on the same day, against the same peer set, tell you whether the whole category is,",
      "and those two conclusions lead to completely different budgets."))
A(p("Most backlink analysis is written for one company, by someone paid to make that company feel a specific way about its numbers. That makes it useless for pattern spotting. You cannot tell whether a profile is bad or whether the whole category is bad."))
A(p("This cohort, which we call Investing &amp; Wealth, removes that problem. Forty-one companies were pulled on the same date, using the same tool, with the same definitions, and each was compared against the same forty-company peer group. They span consumer crypto exchanges, digital-asset infrastructure, wealth management and financial advice, capital-markets plumbing, and finance operations software. They range from pre-seed to post-Series-C, and from Domain Rating 2 to Domain Rating 84."))
A(p("Read individually, each audit reads like a company problem. Read together, they read like a category problem, and the specific shape of that problem is worth more than any single result."))
A(table("Table 1. The cohort. Sub-segments are assigned for analysis only and are not the companies' own categorisations.",
        ["Sub-segment","n","Companies in the cohort"],
        [["Digital-asset infrastructure","11","Blueprint Finance, Dexif, Dispatch, Metallicus, Multis, Phantom, Plasma, Prime Trust, Stablecore, Utila, Zebec Network"],
         ["Exchange and consumer trading","10","CoinSwitch, Conio, Fun, GoSats, Juno, Okcoin, Transak, Unocoin, Uphold, VALR"],
         ["Finance ops and compliance software","9","Cryptio, Eqvista, GetVantage, IVIX, Panax, Pulley, Taxbit, Uptempo, interVal"],
         ["Wealth and advice","6","Arta Finance, Dakota, Facet, Harness, Origin, Range"],
         ["Capital-markets infrastructure","5","Baton Systems, Integral Development Corp, PCR Financial Aggregation, PowerPlan Inc, Tassat"]]))
A(callout("How to read the numbers in this piece",
    ["Referring domains: the number of separate websites that link to you. One site linking a hundred times counts once.",
     "Dofollow domains: the subset of those sites that actually pass authority. A nofollow link tells search engines to ignore the endorsement.",
     "Domain Rating (DR): Ahrefs' 0 to 100 score for how strong a domain looks, built almost entirely from dofollow referring domains.",
     "Ever linked: every domain that has ever pointed at the site, including ones that no longer do. The gap between this and referring domains is decay."]))

# ===== 02 =====
A(sec("02","dead","How much of a backlink profile is already dead?",
      "Across the cohort, 15,134 domains have linked to these 41 companies at some point. Today 2,126 still do, 1,044 pass authority, and only 567 sit at DR 50 or above,",
      "the point at which a link starts to move anything. That is 3.7 percent of every relationship ever formed."))
A(p("Start with the number that frames everything else. Across the cohort, 15,134 domains have linked to these 41 companies at some point in their history. Today, 2,126 of them still do. That is an 86 percent pooled loss rate."))
A(p("It gets narrower. Of the 2,126 domains still linking, 1,044 pass authority. The rest are nofollow, which means the linking site has explicitly told search engines to ignore the endorsement. And of those 1,044, only 567 sit at DR 50 or above."))
A(pull("15,134 relationships were formed. 567 of them currently carry weight. That is 3.7 percent."))
A(chart("collapseChart",300,"Figure 1. The four-step collapse from historical link relationships to links that actually carry authority. Pooled across all 41 companies."))
A(p("Almost every marketing dashboard in this segment reports the first number and none report the last. A founder looking at 2,126 referring domains and a founder looking at 567 domains that pass real authority are looking at the same reality and will make different decisions about it. The gap is a factor of four between referring domains and domains that matter, and a factor of twenty-seven between total historical relationships and the same figure."))
A(h3("This is not a small-company problem"))
A(p("The obvious explanation would be that the weak profiles are the young ones, and that scale fixes it. The data does not support that. The company with the highest Domain Rating in the cohort has lost 73 percent of its historical linking domains. The company with the most historical relationships, 4,400 of them, retains 146. Decay does not care how big you got."))

# ===== 03 =====
A(sec("03","weak","Where does the average link actually come from?",
      "A site nobody reads. 58 percent of the cohort's live referring domains sit at DR 29 or below, and 36 percent sit below DR 10,",
      "a band that is scraper sites, expired-domain networks, jobs aggregators, and directories nobody visits on purpose."))
A(chart("drDistChart",300,"Figure 2. Domain Rating distribution of all live referring domains in the cohort. 58 percent sit at DR 29 or below."))
A(table("Table 2. Where the cohort's link equity actually sits. Only 26.7 percent of all live referring domains clear DR 50.",
        ["Strength of the linking site","Sites","Share of cohort","What a link from here is worth"],
        [["Very strong (DR 70+)","297","14.0%","Moves the needle. Rare and usually earned."],
         ["Strong (DR 50 to 69)","270","12.7%","Meaningful. Trade press, real directories, real partners."],
         ["Middling (DR 30 to 49)","321","15.1%","Marginal on its own. Useful in volume."],
         ["Weak (DR 10 to 29)","466","21.9%","Close to zero. Costs the same to acquire."],
         ["Near zero (DR 0 to 9)","772","36.3%","Zero, and often worse than zero."]],
        cls=lambda j,c:("num" if j in (1,2) else "")))
A(p("Thirty-six percent of every site linking to this cohort has a Domain Rating below 10. That band is not a mix of small blogs and niche publications. Read domain by domain, it is scraper sites, expired-domain networks, jobs aggregators that republish company descriptions, and directories nobody has visited on purpose."))
A(p("The median company in the cohort has eight referring domains at DR 50 or above. Eleven of the 41 have zero domains at DR 70 or above. That is the real starting line, and it is much closer to zero than any referring domain count suggests."))

# ===== 04 =====
A(sec("04","lagging","Is Domain Rating a reliable scoreboard?",
      "No. Fit against live dofollow domains gives Pearson r = 0.45 with a 14.6-point residual spread, so DR predicts almost nothing about any single company.",
      "It is computed from a link graph crawled on a delay, so equity decays slowly inside the model even after the link disappears."))
A(p("Domain Rating is the number every board deck in this segment quotes. It is also the number that correlates worst with what the company currently has."))
A(chart("drFitChart",300,"Figure 3. Domain Rating plotted against live dofollow referring domains, log scale. The fit is real but loose, and three companies sit far off it."))
A(code("Formula 1. The fit, and why it is almost useless as a per-company predictor.",FORM_DR))
A(p("A residual spread of nearly 15 DR points means the model is almost useless as a predictor for any individual company, and that is the point. Two companies in this cohort sit at DR 45 and DR 36 with zero live referring domains between them. Every link either of them ever had is gone, and their scores have not caught up. Another sits at DR 35 with 8 referring domains and 5,283 backlinks, because a single site links to it thousands of times from a sitewide footer."))
A(p("The reason for the lag is structural. Third-party authority scores are computed from a link graph that is crawled on a delay, and historical equity decays slowly inside the model even after the underlying link disappears. "+L("DR tells you where you have been; live visibility is a different question entirely","/blogs/ranking-isnt-visibility")+". It does not tell you where you are."))
A(code("Code 1. Run this against your own export before you quote a referring domain count to anyone.",CODE_EAD))

# ===== 05 =====
A(sec("05","decay","Why is decay the default state of a link profile?",
      "The median company has lost 74 percent of every domain that has ever linked to it, and nothing in the cohort suggested anyone was monitoring it.",
      "Thirty-two of the 40 companies with a historical count have lost more than half."))
A(chart("lossChart",280,"Figure 4. Loss milestones across the cohort. Higher authority offers no protection: the highest-DR company has lost 73 percent, the largest profile 96.7 percent."))
A(p("Decay is not one thing. Pulled apart across the cohort, it is four things, and only one of them is anybody's fault."))
A('<ul>'
  '<li><strong>The page moved or was deleted.</strong> A publisher redesigns, an article is archived, a URL changes. The link exists in nobody\'s intent to remove it and disappears anyway.</li>'
  '<li><strong>The publisher closed.</strong> Trade sites in this category churn fast. A whole domain going offline removes every link it held.</li>'
  '<li><strong>The syndication window expired.</strong> Newswire distribution places a release on dozens of sites. Many of those sites purge on a schedule.</li>'
  '<li><strong>The company changed its own URL.</strong> Rebrands, path restructures, and www-to-apex migrations quietly break inbound links, and this is the one that is entirely self-inflicted.</li>'
  '</ul>')
A(p("The cost of ignoring decay compounds. A recovered link costs one email. An equivalent new link costs a pitch, a relationship, and usually a piece of content. Across this cohort, 13,037 lost relationships are sitting unworked while the same companies pay for new ones."))
A(h3("A metric worth adopting: Live Equity Ratio"))
A(code("Formula 2. One number that separates a profile that was built from one that merely happened.",FORM_LER))
A(chart("lerChart",280,"Figure 5. Live Equity Ratio, all 40 companies with historical data. Half the cohort has kept less than 13 percent of what it once had."))
A(p("The pooled ratio across the cohort is 6.9 percent. The median company sits at 13 percent. Fifteen of the 40 companies with historical data sit below 10 percent, which means more than nine in ten relationships they ever formed are now doing nothing for them."))
A(p("One caveat worth stating plainly. A high Live Equity Ratio is not automatically good. The company at 100 percent has eight referring domains and has never lost one, because it never acquired enough to lose any. The ratio is a retention measure, not a volume measure, and it should always be read next to the absolute count."))
A(code("Code 2. Decay is invisible unless something diffs it on a schedule. Nothing in the cohort suggested anyone was doing this.",CODE_DECAY))

# ===== 06 =====
A(sec("06","homepage","Why do all the backlinks point at the homepage?",
      "Of the 37 companies where page-level concentration was measured, 31 send 95 percent or more of their backlinks to a single URL and 20 send 100 percent.",
      "The median is 100 percent, which produces a site with exactly one strong page, and it is almost never the one a buyer needs to find."))
A(chart("concChart",280,"Figure 6. Share of all backlinks pointing at the homepage, by concentration band. Twenty of 37 companies sit at 100 percent."))
A(p("This is normal for a young profile and it is a serious constraint for a company trying to rank anything specific. Authority flows through a site from the pages that receive it. A profile where every link lands on the homepage produces a site with exactly one strong page, and that page is almost never the one a buyer needs to find."))
A(p("It also caps what content marketing can do. Publishing a comparison page, a pricing explainer, or an integration guide is only half the work. If no external link ever points at it, it competes on "+L("internal linking","/blogs/internal-linking-for-ai-retrieval")+" alone against pages that have external authority of their own."))
A(p("The fix is not complicated and it is almost entirely a question of what you point people at. Original data goes on its own URL. A tool or calculator goes on its own URL. A "+L("comparison or 'best X for Y' page that a buyer and an AI assistant both pull from","/blogs/comparison-pages-ai-shortlists")+" goes on its own URL. Then every pitch, every profile, and every release links there rather than to the front door."))
A(table("Table 3. Link destination by link type. Only one row in this table belongs on the homepage.",
        ["What earns the link","Where the link should land","Why the homepage is the wrong target"],
        [["Original data or a benchmark","A dedicated research URL","The citation is to the finding, not the company"],
         ["A free tool or calculator","The tool's own page","Repeat linkers point at the utility"],
         ["A funding or product announcement","Homepage is fine here","Brand-level news genuinely is brand-level"],
         ["A category explainer or glossary","The glossary entry itself","Builds a rankable page, not a stronger front door"],
         ["A comparison or alternatives page","The comparison page","This is the page buyers and AI assistants actually pull from"]]))

# ===== 07 =====
A(sec("07","nofollow","Are the strongest links actually passing authority?",
      "Half are not. Of the 283 strongest placements in the cohort, 49 percent are nofollow,",
      "because newswire syndication, jobs boards, company directories, and most large media default to nofollow on outbound links."))
A(chart("placementChart",260,"Figure 7. The 283 strongest placements in the cohort, split by whether they pass authority."))
A(p("Each audit named the strongest placements a company had already earned. Across the cohort that is 283 links from 192 distinct domains, and it is the closest thing to a highlight reel this segment has. Forty-nine percent of them are nofollow. These are not bad links, and the traffic and credibility they carry is real. But in terms of the authority they transfer, they are decorative."))
A(p("A press release that lands on twelve sites can produce twelve links and zero authority transfer. None of this is an argument against those placements, it is an argument against counting them as link building. And for AI search specifically the calculus shifts again: "+L("an unlinked brand mention on a trusted site now corroborates a retrieval system directly","/blogs/mentions-beat-links")+", which is why the reach these placements carry is worth tracking on its own axis, just not in the link column."))
A(p("The practical version is that the cohort's median profile has 3.1 links per referring domain and 22 percent of all links marked nofollow, and the top-of-profile links skew far more nofollow than the tail does. The strongest-looking part of the profile is the least load-bearing part."))

# ===== 08 =====
A(sec("08","spam","Does the spam in a backlink profile look like spam?",
      "No. Across the cohort 651 flagged domains sit against 2,126 live referring domains, and 31 percent of the flagged ones carry DR 30 or above.",
      "If your filter for a bad link is 'low DR', you will keep a third of them."))
A(chart("spamChart",280,"Figure 8. What the 194 named flagged domains are. A site with no readers and outright link farms account for nine in ten."))
A(table("Table 4. Taxonomy of 194 named spam referring domains across 22 companies.",
        ["Type of flagged domain","Count","Share","What it looks like in a report"],
        [["A site with no readers","99","51.0%","Real-looking domain, near-zero traffic, syndicated filler"],
         ["A link farm","78","40.2%","Hundreds of unrelated outbound links per page"],
         ["A link selling site","9","4.6%","Paid placement, often disclosed nowhere"],
         ["A throwaway domain","4","2.1%","Registered recently, no history, no purpose"],
         ["Other flagged","4","2.1%","Caught by the tool, unclassified on manual read"]],
        cls=lambda j,c:("num" if j in (1,2) else "")))
A(p("Twenty-six of the 41 companies had at least one referring domain flagged as spam. The DR distribution is the part worth sitting with. Thirty-one percent of these flagged domains carry a Domain Rating of 30 or above and seven percent clear DR 50. One domain in the cohort appears as a flagged referrer for seven different companies, and nineteen distinct spam domains appear across more than one company. That is a signature: the same link networks are working the same target list, and several of these companies are receiving links they never asked for and are not aware of."))
A(callout("The part that gets missed",
    ["Two companies in this cohort have profiles that are 92 percent and 63 percent flagged spam by volume. Neither of them bought those links in any account anyone still has access to.",
     "Negative SEO is rare. Inherited spam from an old agency, an old growth hack, or an unrelated network scraping funding announcements is not. Either way the cleanup is the same job."]))

# ===== 09 =====
A(sec("09","shopping","Do competitor gap analyses find real link opportunities?",
      "They find the floor, not the ceiling. The cohort's 803 identified opportunities resolve to just 32 distinct domains, and 62 percent are directories and newswire hosts,",
      "because commodity links are the ones every peer already has. Average pairwise overlap between any two companies' lists is 0.69."))
A(p("Each audit produced a list of domains that link to several peers and not to the audited company. Across the cohort that is 803 identified opportunities. They resolve to 32 distinct domains. Nineteen of those 32 appear in 32 or more of the 41 audits. Pick two companies at random from this cohort, in different sub-segments, at different stages, on different continents, and roughly seven in ten of their link opportunities are the same domains."))
A(chart("oppChart",320,"Figure 9. The most frequently identified link opportunities, and how many of the 41 audits named each."))
A(chart("oppTypeChart",280,"Figure 10. Composition of the 803 identified opportunities, by type of site. Directory listings and wire hosts are 62 percent of the total."))
A(p("Sixty-two percent of what this segment calls a link opportunity sits in one bucket: company directories, profile pages, and newswire syndication hosts. Split that bucket and 40 percent of all opportunities are directory listings you can "+L("claim yourself as part of an entity-home pass","/blogs/becoming-an-entity")+" in an afternoon, while 22 percent are wire distribution hosts that cost money rather than effort. Seventeen percent is trade or industry media, and nine percent is a publishing platform where you write the content yourself."))
A(p("There are two honest readings and both are useful. The commodity layer is genuinely unclaimed: most of these companies have not done the free, permanent, thirty-minute version of link building, and closing it is the correct first move. But a gap analysis built from peer overlap will always converge on commodity links, because commodity links are the ones every peer has. "+L("The link nobody in your category has earned yet","/blogs/authority-seeding-ai-llm-trust")+" will never appear in a competitor gap list. Claim the 32 domains because they are free. Do not mistake finishing that list for having a link strategy."))
A(table("Table 5. Thirteen of the most repeated opportunities. Only two of them require a pitch. The rest need a form, a login, or a budget.",
        ["Domain","Type","Named in","DR","Median peers with the link"],
        [["medium.com","Publishing platform","38 of 41","94","3"],
         ["owler.com","Directory","37","72","4"],
         ["substack.com","Publishing platform","37","94","4"],
         ["newswire.com","Directory / wire","37","87","4"],
         ["cortera.com","Directory","37","54","4"],
         ["finopotamus.com","Trade media","37","56","4"],
         ["crunchbase.com","Directory","36","91","5"],
         ["rocketreach.co","Directory","36","75","5"],
         ["fortune.com","Trade media","36","91","5"],
         ["contactout.com","Directory","35","74","6"],
         ["c212.net","Wire syndication","34","90","7"],
         ["builtin.com","Directory","34","86","7"],
         ["prnewswire.com","Wire","29","92","12"]],
        cls=lambda j,c:("num" if j in (2,3,4) else "")))

# ===== 10 =====
A(sec("10","subsegments","Where do the sub-segments differ?",
      "The failure is universal; the shape of it is not. Exchanges acquired reach and kept almost none of it, so their fix is recovery.",
      "Digital-asset infrastructure never acquired links at all, so its fix is straightforward acquisition. Same segment, opposite first moves."))
A(chart("segChart",320,"Figure 11. Median position by sub-segment across three link measures. The Live Equity Ratio, in the table below, tells you whether the problem is acquisition or retention."))
A(table("Table 6. Sub-segment medians. The Live Equity Ratio column tells you whether the problem is acquisition or retention.",
        ["Sub-segment","Median DR","Median live ref domains","Median domains passing value","Median LER","The characteristic failure"],
        [["Exchange and consumer trading","54","43","20","6%","Acquired reach through wires and coverage, retained almost none of it"],
         ["Finance ops and compliance software","47","20","8","18%","Thin but clean. Nobody has been asked for a link."],
         ["Wealth and advice","44","19","14","14%","Regulated caution has been read as a reason not to publish anything citable"],
         ["Digital-asset infrastructure","44","7","4","33%","Never acquired links at all. High retention of a very small base."],
         ["Capital-markets infrastructure","37","21","13","5%","Long-established, and the links that built the profile have almost all expired"]],
        cls=lambda j,c:("num" if j in (1,2,3,4) else "")))
A(p("Exchange and consumer trading has the highest median Domain Rating in the cohort and the second-lowest Live Equity Ratio. These companies did the acquisition work, then stopped maintaining any of it. Their correct first move is recovery, not acquisition, and it is cheap. Digital-asset infrastructure is the mirror image: median seven live referring domains and the highest retention rate in the cohort, because there was never anything to lose. Their correct first move is straightforward acquisition, starting with the free tier."))
A(p("Capital-markets infrastructure is the group to watch. It has the highest median historical domain count in the cohort at 362, a 91 percent median loss rate, and the lowest median Domain Rating at 37. Time built these profiles and time dismantled them while nobody was looking at the numbers."))

# ===== 11 =====
A(sec("11","takeaways","What should companies actually do about it?",
      "Nine specific things, in the order the data supports doing them.",
      "Audit before you acquire, report Effective Authority Domains, diff monthly, and work the recovery queue before the acquisition queue."))
A(chart("seqChart",300,"Figure 13. The ninety-day sequence the audits converge on independently. The ordering carries more weight than the tactics."))
A(pipeline([("Keep","Live, dofollow, DR-worthy. Leave it and protect it."),
            ("Recover","Lost from a live publisher. One email each."),
            ("Disavow","Flagged on a manual read. Filed, with a reason.")],1,
           "Figure 12. The triage pass. Every domain in the profile goes into exactly one of three columns before any new link is bought or pitched."))
A(h3("1. Audit before you acquire"))
A(p("Twenty-six of the 41 companies had flagged domains sitting in their profile, and in most the genuine layer underneath was thin. Adding links to a profile you have not sorted means the reporting stays broken and the cleanup gets more expensive. The triage pass is two weeks of manual work and it is the only step that must come first."))
A(h3("2. Report Effective Authority Domains, not Domain Rating"))
A(p("DR lags, it can be inflated by a single sitewide footer link, and in this cohort it correlates at r = 0.45 with what a company actually has. Count live dofollow domains at DR 50 or above. It is a smaller, harder, more honest number, and the "+L("off-site authority scorecard","/tools/off-site-authority-scorecard")+" computes it from an export."))
A(h3("3. Diff your referring domains every month"))
A(p("The cohort's median loss rate is 74 percent. Nothing in the data suggested anyone was monitoring it. A monthly diff against last month's export takes minutes and produces a recovery queue that is cheaper to work than any acquisition list."))
A(h3("4. Work the recovery queue before the acquisition queue"))
A(p("A lost link from a live publisher is one email. Across this cohort there are 13,037 lost relationships, and a meaningful share are page moves that a single message would fix."))
A(h3("5. Claim the free tier once, properly"))
A(p("Forty percent of the identified opportunities are self-serve directory and profile listings. They are free, they are permanent, and almost nobody in this cohort had claimed them. Do it in one afternoon and then stop thinking about it. The 22 percent that are wire hosts are a separate budget decision, not a free win."))
A(h3("6. Stop counting nofollow placements as link building"))
A(p("Half the strongest placements in this cohort pass no authority. Count them as reach, count them as credibility, and keep them out of the link column."))
A(h3("7. Give links somewhere to land other than the homepage"))
A(p("The cohort median is 100 percent homepage concentration. Every piece of original data, every tool, and every methodology page you publish should be the destination of the pitch that promotes it."))
A(h3("8. Publish one thing per quarter that has no substitute"))
A(p("Original numbers from your own platform, a survey, or a benchmark. It is the only category of page in this analysis that reliably attracts links from sites you did not contact, because "+L("there is nowhere else to get the data","/blogs/mentions-beat-links")+"."))
A(h3("9. Re-run the same audit on a schedule"))
A(p("Same tool, same definitions, same date each quarter. Most of what is wrong in this cohort is not a strategy failure. It is the absence of anyone checking."))

# ===== 12 =====
A(sec("12","scoreboard","What scoreboard should replace Domain Rating?",
      "Four numbers, all computable from a single referring-domains export and all harder to game than the one most teams report.",
      "Effective Authority Domains, Live Equity Ratio, Link Liability Ratio, and Page Concentration."))
A(table("Table 7. Four metrics and the cohort baseline for each. Every one of them is worse than the number it replaces, which is the point.",
        ["Metric","Definition","Cohort median","Read it as"],
        [["Effective Authority Domains (EAD)","Live dofollow referring domains at DR 50+","8","The real size of your link position"],
         ["Live Equity Ratio (LER)","Live dofollow referring domains / domains ever acquired","13%","Whether you retain what you win"],
         ["Link Liability Ratio (LLR)","(nofollow-only + flagged domains) / live referring domains","47%","How much of the profile is decoration"],
         ["Page Concentration","Share of backlinks pointing at a single URL","100%","Whether authority can reach anything but the homepage"]],
        cls=lambda j,c:("num" if j==2 else "")))
A(p("These four sit alongside the discipline that governs everything else RawMktg publishes: "+L("measure the same thing the same way every time","/methodology")+", and read link position next to "+L("share of model and citation measurement","/blogs/share-of-model-measurement")+" rather than in place of it. Run the scoreboard quarterly and you will know more about your link position than any DR chart will tell you."))
A(code("Code 3. Fifteen lines. Run it quarterly and you will know more about your link position than any DR chart will tell you.",CODE_SCORE))
A(code("Code 4. Disavow format. Comments are ignored by Google and are the only record of why you filed each one, so write them.",CODE_DISAVOW))

# ===== 13 =====
A(sec("13","method","What can this analysis not tell you?",
      "It establishes that a segment's link profiles are thin, decayed, and concentrated. It does not measure what that costs in traffic, pipeline, or AI-assistant citations,",
      "because none of those were measured here. What it does show is that the cheapest available improvements are sitting unclaimed in front of everyone at once."))
A(p("Every figure in this piece is computed from 41 backlink audits, the Investing &amp; Wealth cohort, produced on 26 August 2026 from Ahrefs referring domains, backlinks, and link intersect data, each benchmarked against the same forty-company peer set. Sub-segment assignment is ours and is for analysis only. Four limitations are worth stating."))
A('<ul>'
  '<li><strong>Spam classification is partly manual.</strong> Ahrefs\' flag was the starting point and each list was read by hand. Another analyst would draw the line differently, particularly in the DR 30 to 50 band.</li>'
  '<li><strong>Ahrefs\' index is not the web.</strong> Referring domain counts, historical counts, and traffic estimates are one crawler\'s view. Directionally sound, not absolute.</li>'
  '<li><strong>This is a single point in time.</strong> Decay rates here are cumulative history, not a measured rate per period. A monthly series would be a much stronger dataset and is the obvious follow-up.</li>'
  '<li><strong>Some figures exclude companies with missing data.</strong> Four companies had no page-concentration figure and one had no historical domain count. Every chart states its own n.</li>'
  '</ul>')
A(callout("The one-line version",
    ["Across the 41 funded companies in the Investing &amp; Wealth cohort, 96.3 percent of every link relationship ever formed is currently doing nothing. The work required to change that is unglamorous, mostly free, and almost entirely unstarted."]))

# ===== FAQ =====
FAQ=[
 ("What is a healthy backlink profile size for a funded startup?",
  "Count Effective Authority Domains, not referring domains. That is the number of live, dofollow referring domains at Domain Rating 50 or above. Across 41 audited companies in investing, wealth, and digital assets the median was 8 and the lower quartile was 2, with sixteen of 41 below five. A raw referring-domain count in the hundreds routinely collapses to single digits once you strip out lost links, nofollow links, and weak domains, so the honest starting line is almost always far lower than the dashboard number."),
 ("Why is Domain Rating a misleading metric?",
  "Domain Rating is computed from a link graph that is crawled on a delay, so historical equity decays slowly inside the score even after the underlying links disappear. Across this cohort DR correlated with live dofollow referring domains at Pearson r = 0.45 with a 14.6-point residual spread, which makes it almost useless as a per-company predictor. Companies in the cohort held DR 45 with zero live referring domains, and DR 35 inflated by a single sitewide footer link repeated thousands of times. DR tells you where you have been, not where you are."),
 ("How do I find lost backlinks worth recovering?",
  "Export your referring domains monthly and diff this month against last. Any domain present last month and absent this month is a lost link; filter those to the ones that were dofollow and at DR 30 or above, and sort by Domain Rating to get a recovery queue. Most losses are page moves or redesigns, and a recovered link from a live publisher costs one email, versus a pitch, a relationship, and a piece of content for an equivalent new one. Across the audited cohort there were 13,037 lost relationships sitting unworked."),
 ("Are nofollow backlinks worthless?",
  "For authority transfer, yes, a nofollow link tells search engines to ignore the endorsement, and 49 percent of the strongest placements in this cohort were nofollow. But they are not worthless: newswire, directories, and large media carry real reach and credibility, and for AI search an unlinked or nofollow brand mention on a trusted site now corroborates a retrieval system directly. Count them as reach, not as link building, and keep them out of the link column on your scoreboard."),
 ("Should I disavow spammy backlinks?",
  "Only after a manual pass, and only for clear link farms, paid-placement networks, and syndicated filler. A low-DR filter is not enough: 31 percent of the flagged domains in this cohort carried DR 30 or above and 7 percent cleared DR 50. Automated classification gets this wrong in both directions, so read the list by hand, write the reason for each entry as a comment in the disavow file, and remember that much of this spam is inherited rather than bought."),
 ("Why do all my backlinks point at my homepage, and does it matter?",
  "It is normal for a young profile, because announcements, directory listings, and social profiles all default to the front door, and the audited cohort median was 100 percent homepage concentration. It matters because authority flows through a site from the pages that receive links, so a profile where everything lands on the homepage produces exactly one strong page, and it is rarely the one a buyer or an AI assistant needs. Give original data, tools, and comparison pages their own URLs and point every pitch there."),
 ("What should replace Domain Rating on our reporting?",
  "Four numbers from a single referring-domains export: Effective Authority Domains (live dofollow domains at DR 50+, cohort median 8), Live Equity Ratio (live dofollow domains divided by domains ever acquired, median 13 percent), Link Liability Ratio (nofollow-only plus flagged domains over live referring domains, median 47 percent), and Page Concentration (share of backlinks on a single URL, median 100 percent). Each is smaller, harder to game, and more honest than DR."),
]
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
A(faq_html)

# ===== References =====
REFS=[
 ("Ahrefs' Domain Rating (DR): what it is and how it is calculated. Ahrefs.","https://ahrefs.com/blog/domain-rating/"),
 ("Referring domains vs backlinks: what is the difference? Ahrefs.","https://ahrefs.com/blog/referring-domains-vs-backlinks/"),
 ("What are nofollow links, and how do they work? Ahrefs.","https://ahrefs.com/blog/nofollow-links/"),
 ("Link intersect: find who links to competitors but not you. Ahrefs.","https://ahrefs.com/blog/link-intersect/"),
 ("How to find and reclaim lost backlinks. Ahrefs.","https://ahrefs.com/blog/lost-backlinks/"),
 ("Link building for SEO: the beginner's guide. Ahrefs.","https://ahrefs.com/blog/link-building/"),
 ("Disavow links to your site. Google Search Central Help.","https://support.google.com/webmasters/answer/2648487"),
 ("Qualify your outbound links to Google (rel=nofollow, sponsored, ugc). Google Search Central.","https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links"),
 ("What is link equity (link juice) and how does it work? Moz.","https://moz.com/learn/seo/link-equity"),
 ("Anchor text and the flow of PageRank through a site. Moz Beginner's Guide to SEO.","https://moz.com/beginners-guide-to-seo"),
 ("The decay of backlinks over time. Search Engine Journal.","https://www.searchenginejournal.com/link-decay-seo/"),
 ("Negative SEO and toxic link audits: what actually matters. Search Engine Land.","https://searchengineland.com/guide/what-is-link-building"),
 ("Press release syndication and nofollow: what wire links are worth. PR Newswire resources.","https://www.prnewswire.com/resources/"),
 ("Crunchbase, Owler and business directories as citable entity records. Crunchbase.","https://about.crunchbase.com/"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
A('<div class="about-block" id="references"><div class="about-label">References</div>'
  '<p style="margin-bottom:16px;">Figures 1 through 13 are original, computed from 41 backlink audits (Ahrefs referring domains, backlinks, and link intersect, pulled 26 August 2026). The sources below cover the metrics and definitions used.</p>'
  f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
A('<div class="about-block"><div class="about-label">About rawmktg.</div>'
  '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
  '<p>Sources: 41 Ahrefs backlink audits pulled 26 August 2026, each benchmarked against the same forty-company peer set; Ahrefs, Moz, and Google Search Central documentation on referring domains, Domain Rating, nofollow, link equity, and disavow. Correlations are directional, not causal; the index is one crawler\'s view of the web.</p></div>')

body="\n".join(out)

SIDEBAR=[("3.7%","of link relationships ever formed still carry weight"),
         ("86%","of all historical linking domains have decayed"),
         ("100%","median homepage concentration across the cohort"),
         ("0.69","opportunity-list overlap between any two companies")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#cohort"><span class="toc-num">01</span>One cohort, one dataset</a></li>'
     '<li><a href="#dead"><span class="toc-num">02</span>Most of the profile is dead</a></li>'
     '<li><a href="#weak"><span class="toc-num">03</span>The average link is worthless</a></li>'
     '<li><a href="#lagging"><span class="toc-num">04</span>Domain Rating lags</a></li>'
     '<li><a href="#decay"><span class="toc-num">05</span>Decay is the default</a></li>'
     '<li><a href="#homepage"><span class="toc-num">06</span>Everything points home</a></li>'
     '<li><a href="#nofollow"><span class="toc-num">07</span>The best links are off</a></li>'
     '<li><a href="#spam"><span class="toc-num">08</span>The spam isn\'t low-DR</a></li>'
     '<li><a href="#shopping"><span class="toc-num">09</span>One shopping list</a></li>'
     '<li><a href="#subsegments"><span class="toc-num">10</span>Where sub-segments differ</a></li>'
     '<li><a href="#takeaways"><span class="toc-num">11</span>Nine moves, in order</a></li>'
     '<li><a href="#scoreboard"><span class="toc-num">12</span>The replacement scoreboard</a></li>'
     '<li><a href="#method"><span class="toc-num">13</span>Method and limits</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - what 41 backlink audits reveal - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["backlink audit","referring domains","Domain Rating","link equity","link decay","Effective Authority Domains","Live Equity Ratio","disavow","nofollow","off-site SEO","digital PR","B2B SaaS SEO"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="The Link Liability: What 41 Backlink Audits Reveal &middot; rawmktg."
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

  var f1=document.getElementById('collapseChart');
  if(f1){new Chart(f1,{type:'bar',data:{labels:['Ever linked','Still linking','Passing value','DR 50 or above'],datasets:[{data:[15134,2126,1044,567],backgroundColor:[neutral,rgba(signal,0.5),rgba(signal,0.7),signal],borderRadius:4,barThickness:44}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw.toLocaleString()+' domains';}}}},
      scales:{x:{type:'logarithmic',min:100,ticks:{color:text,font:{family:mono,size:9}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var f2=document.getElementById('drDistChart');
  if(f2){new Chart(f2,{type:'bar',data:{labels:['DR 0-9','DR 10-29','DR 30-49','DR 50-69','DR 70+'],datasets:[{data:[772,466,321,270,297],backgroundColor:[signal,rgba(signal,0.6),neutral,rgba(up,0.6),up],borderRadius:4,barThickness:46}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' live referring domains';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var f3=document.getElementById('drFitChart');
  if(f3){var fit=[];for(var d=0;d<=250;d+=5){fit.push({x:d,y:13.6*Math.log10(d+1)+32.9});}
    new Chart(f3,{data:{datasets:[
      {type:'line',label:'fit',data:fit,borderColor:signal,borderWidth:2,pointRadius:0,tension:0.2,fill:false},
      {type:'scatter',label:'off the line',data:[{x:0,y:45},{x:0,y:36},{x:8,y:35}],backgroundColor:up,pointRadius:5}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:10}}},tooltip:{callbacks:{label:function(c){return ' '+c.raw.x+' domains, DR '+Math.round(c.raw.y);}}}},
      scales:{x:{type:'logarithmic',min:0,title:{display:true,text:'live dofollow referring domains (log)',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:9}},grid:{color:grid}},y:{beginAtZero:true,max:90,title:{display:true,text:'Domain Rating',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var f4=document.getElementById('lossChart');
  if(f4){new Chart(f4,{type:'bar',data:{labels:['Cohort median','Highest-DR company','Capital-markets median','Largest profile (4,400 rels)'],datasets:[{data:[74,73,91,96.7],backgroundColor:[rgba(signal,0.6),rgba(signal,0.7),rgba(signal,0.85),signal],borderRadius:4,barThickness:36}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of linking domains lost';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var f5=document.getElementById('lerChart');
  if(f5){new Chart(f5,{type:'bar',data:{labels:['< 5%','5-10%','10-20%','20-40%','40%+'],datasets:[{data:[8,7,13,8,4],backgroundColor:[signal,rgba(signal,0.7),neutral,rgba(up,0.6),up],borderRadius:4,barThickness:46}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' companies';},title:function(t){return 'Live Equity Ratio '+t[0].label;}}}},
      scales:{x:{title:{display:true,text:'Live Equity Ratio band',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var f6=document.getElementById('concChart');
  if(f6){new Chart(f6,{type:'bar',data:{labels:['Below 80%','80-95%','95-99%','100%'],datasets:[{data:[6,0,11,20],backgroundColor:[rgba(up,0.6),neutral,rgba(signal,0.6),signal],borderRadius:4,barThickness:52}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' of 37 companies';}}}},
      scales:{x:{title:{display:true,text:'backlinks pointing at a single URL',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var f7=document.getElementById('placementChart');
  if(f7){new Chart(f7,{type:'doughnut',data:{labels:['Dofollow (passes authority)','Nofollow (decorative)'],datasets:[{data:[144,139],backgroundColor:[up,signal],borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:11}}},tooltip:{callbacks:{label:function(c){return ' '+c.label+': '+c.raw+' of 283';}}}}}});}

  var f8=document.getElementById('spamChart');
  if(f8){new Chart(f8,{type:'bar',data:{labels:['Site with no readers','Link farm','Link selling site','Throwaway domain','Other flagged'],datasets:[{data:[99,78,9,4,4],backgroundColor:[signal,rgba(signal,0.8),rgba(signal,0.55),rgba(signal,0.4),neutral],borderRadius:4,barThickness:30}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+' named domains';}}}},
      scales:{x:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}

  var f9=document.getElementById('oppChart');
  if(f9){new Chart(f9,{type:'bar',data:{labels:['medium.com','owler.com','substack.com','newswire.com','cortera.com','finopotamus.com','crunchbase.com','rocketreach.co','fortune.com','contactout.com','c212.net','builtin.com','prnewswire.com'],datasets:[{data:[38,37,37,37,37,37,36,36,36,35,34,34,29],backgroundColor:rgba(signal,0.7),borderRadius:3,barThickness:15}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' named in '+c.raw+' of 41 audits';}}}},
      scales:{x:{beginAtZero:true,max:41,ticks:{color:text,font:{family:mono,size:9}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}}}}});}

  var f10=document.getElementById('oppTypeChart');
  if(f10){new Chart(f10,{type:'doughnut',data:{labels:['Directory listings','Wire syndication hosts','Trade / industry media','Publishing platform','Other'],datasets:[{data:[40,22,17,9,12],backgroundColor:[signal,rgba(signal,0.7),amber,blue,neutral],borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'58%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:10}}},tooltip:{callbacks:{label:function(c){return ' '+c.label+': '+c.raw+'%';}}}}}});}

  var f11=document.getElementById('segChart');
  if(f11){new Chart(f11,{type:'bar',data:{labels:['Exchange & trading','Finance ops','Wealth & advice','Digital-asset infra','Capital-markets infra'],datasets:[
    {label:'Median DR',data:[54,47,44,44,37],backgroundColor:blue,borderRadius:3},
    {label:'Live ref domains',data:[43,20,19,7,21],backgroundColor:amber,borderRadius:3},
    {label:'Domains passing value',data:[20,8,14,4,13],backgroundColor:up,borderRadius:3}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:text,font:{family:mono,size:10}}},tooltip:{mode:'index',intersect:false}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:9}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:grid}}}}});}

  var f13=document.getElementById('seqChart');
  if(f13){new Chart(f13,{type:'bar',data:{labels:['Triage the profile','Recover lost links','Claim the free tier','Publish original data','Re-scan the audit'],datasets:[{label:'start',data:[0,14,14,30,80],backgroundColor:'transparent'},{label:'duration',data:[14,30,3,50,10],backgroundColor:[blue,up,amber,signal,rgba(up,0.7)],borderRadius:4,barThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){if(c.datasetIndex===0)return '';var s=c.chart.data.datasets[0].data[c.dataIndex];return ' day '+s+' to '+(s+c.raw);}}}},
      scales:{x:{stacked:true,beginAtZero:true,max:95,title:{display:true,text:'days',color:text,font:{family:mono,size:9}},ticks:{color:text,font:{family:mono,size:9}},grid:{color:grid}},y:{stacked:true,ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Content &amp; Authority &middot; Backlink research</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/ll_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/ll_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| faqitem:",hh.count('faq-item'),"| refs:",hh.count('id="references"'),
 "| outlinks:",len(re.findall(r'href="/(blogs|tools|methodology)',hh)))
