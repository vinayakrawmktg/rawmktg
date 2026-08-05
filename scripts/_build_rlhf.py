#!/usr/bin/env python3
"""SCRATCH: build blogs/rlhf-and-your-brand.html (native figures + calculator). Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="rlhf-and-your-brand"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-06-12"

def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'")
        .replace("“",'"').replace("”",'"').replace("…","...").replace(" "," "))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)

T=open("blogs/property-vista-authority-paradox.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'

# extra CSS for the calculator (rawmktg dark terminal)
CALCCSS = """
    /* GEO lift calculator */
    .calc-wrap{background:#1A1815;border-radius:8px;padding:26px 24px 22px;margin:28px 0 8px;}
    .calc-head{font-family:var(--f-mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--signal);margin-bottom:5px;}
    .calc-subt{font-family:var(--f-display);font-weight:600;font-size:17px;letter-spacing:-.01em;color:#fff;margin-bottom:20px;}
    .calc-grid{display:grid;grid-template-columns:1fr 290px;gap:26px;}
    .calc-base label{display:flex;justify-content:space-between;font-family:var(--f-mono);font-size:11px;color:rgba(255,255,255,.72);margin-bottom:10px;}
    .calc-baseval{color:var(--signal);font-weight:600;}
    input.calc-range{width:100%;accent-color:var(--signal);height:4px;}
    .calc-hint{font-family:var(--f-mono);font-size:10px;color:rgba(255,255,255,.4);margin:8px 0 6px;line-height:1.5;}
    .calc-tactic{border-top:1px solid rgba(255,255,255,.10);padding:15px 0 4px;}
    .calc-tactic.off{opacity:.42;}
    .calc-trow{display:flex;align-items:center;gap:11px;margin-bottom:10px;}
    .calc-switch{width:34px;height:18px;border-radius:9px;border:0;background:rgba(255,255,255,.22);position:relative;cursor:pointer;flex:0 0 auto;padding:0;}
    .calc-switch.on{background:var(--signal);}
    .calc-switch::after{content:"";position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:#fff;transition:left .15s;}
    .calc-switch.on::after{left:18px;}
    .calc-tname{font-family:var(--f-prose);font-size:13px;color:#fff;flex:1;}
    .calc-band{font-family:var(--f-mono);font-size:10px;color:rgba(255,255,255,.5);}
    .calc-seg{display:inline-flex;gap:5px;margin-left:45px;}
    .calc-seg button{font-family:var(--f-mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.1em;padding:5px 13px;border:1px solid rgba(255,255,255,.16);background:transparent;color:rgba(255,255,255,.6);border-radius:4px;cursor:pointer;}
    .calc-seg button.sel{background:var(--signal);border-color:var(--signal);color:#fff;}
    .calc-output{background:rgba(255,255,255,.04);border-radius:8px;padding:22px 20px;align-self:start;}
    .calc-out-eyebrow{font-family:var(--f-mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.5);}
    .calc-lift{font-family:var(--f-display);font-weight:700;font-size:50px;letter-spacing:-.03em;color:var(--signal);line-height:1.02;margin:6px 0 2px;}
    .calc-liftsub{font-family:var(--f-mono);font-size:10px;color:rgba(255,255,255,.5);margin-bottom:20px;}
    .calc-barrow{display:flex;align-items:center;gap:9px;margin-bottom:11px;}
    .calc-barrow .lbl{font-family:var(--f-mono);font-size:9px;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.5);width:64px;}
    .calc-track{flex:1;height:8px;background:rgba(255,255,255,.10);border-radius:4px;overflow:hidden;}
    .calc-fill{height:100%;border-radius:4px;transition:width .2s;}
    .calc-fill.now{background:rgba(255,255,255,.42);}
    .calc-fill.proj{background:var(--signal);}
    .calc-barrow b{font-family:var(--f-mono);font-size:11px;color:#fff;width:40px;text-align:right;}
    .calc-break{display:flex;flex-wrap:wrap;gap:6px;margin:15px 0 4px;}
    .calc-chip{font-family:var(--f-mono);font-size:9.5px;background:rgba(208,74,42,.20);color:var(--signal);padding:4px 9px;border-radius:4px;}
    .calc-chip.muted{background:rgba(255,255,255,.08);color:rgba(255,255,255,.5);}
    .calc-caveat{font-family:var(--f-mono);font-size:9.5px;line-height:1.65;color:rgba(255,255,255,.4);margin-top:12px;}
    /* sources list */
    .sources-block{border-top:1px solid var(--rule);margin:40px 0 0;padding-top:22px;}
    .sources-label{font-family:var(--f-mono);font-size:10px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--mute);margin-bottom:14px;}
    .sources-list{list-style:none;padding:0;margin:0;display:grid;gap:9px;}
    .sources-list li{font-family:var(--f-mono);font-size:11.5px;line-height:1.5;color:var(--ink-2);padding-left:16px;position:relative;}
    .sources-list li::before{content:"-";position:absolute;left:0;color:var(--faint);}
    .sources-list a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--signal);}
    @media(max-width:680px){.calc-grid{grid-template-columns:1fr;}.calc-seg{margin-left:0;}}
  """
STYLE=STYLE.replace("</style>", CALCCSS+"</style>")

# renderers
def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest
         else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def code(label,body,lang=None):
    lng=f'<span class="code-lang">{esc(lang)}</span>' if lang else ''
    return (f'<div class="code-wrap"><div class="code-label">{esc(label)}</div>'
            f'<div class="code-block">{lng}<pre>{H.escape(body)}</pre></div></div>')
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return (f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div>'
            f'<table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')
def chart(cid,height,caption):
    return (f'<div class="chart-wrap"><canvas id="{cid}" height="{height}"></canvas></div>'
            f'<div class="chart-caption">{esc(caption)}</div>')
def donut(cid,caption):
    return (f'<div class="chart-wrap"><div class="donut-box" style="max-width:320px;margin:6px auto;">'
            f'<canvas id="{cid}" height="260"></canvas></div></div>'
            f'<div class="chart-caption">{esc(caption)}</div>')
def pipeline(nodes,goal_idx,caption,loop=False):
    parts=['<div class="pipeline">']
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal_idx else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(caption)}</div>'
def callout(label,body):
    return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div><p>{norm(body)}</p></div>'
def L(text,url,ext=True):
    a=f' target="_blank" rel="noopener"' if ext else ""
    return f'<a href="{url}"{a}>{norm(text)}</a>'

HEADLINE="RLHF and Your Brand"
DECK=("How human rater preferences are quietly deciding who AI recommends, and why your share of voice now lives "
      "in the alignment layer, not the index.")
DESC=("How RLHF and DPO post-training quietly decide which brands AI recommends. The mathematics of preference, "
      "why it compounds into a moat, who the raters were trained to trust, and the GEO playbook to win Share of Model.")
DATANOTE=("Synthesis of post-training research (RLHF, DPO, and newer methods), the Princeton GEO citation-lift "
          "coefficients, and the Muck Rack 'What Is AI Reading?' citation study, June 2026. Example code and the "
          "lift calculator are illustrative.")

out=[]
out.append('<p class="lead">'+norm("For twenty years the job was simple to describe even if it was hard to do: rank on the results page, earn the click. Search has quietly changed shape underneath that job. The interface is moving from Boolean lexical retrieval to neural generative synthesis, the model reads, decides, and writes one answer, and most of the time the user never sees a list of links at all.")+'</p>')
out.append(p("That shift produced what analysts call the Great Decoupling: conversational search volume is climbing while referral traffic to the open web collapses. Roughly "+L("58% of Google searches now end without a click","https://www.cracklepr.com/insights/ai-search-runs-on-earned-media")+", rising to 83% when AI Overviews fire and 93% inside AI Mode. With traditional search volume projected to fall about 25%, the place where your brand gets chosen is no longer the index. It is the model."))
out.append(chart("rlhfDecouplingChart",230,"Figure 1 - the Great Decoupling: share of searches that end without a click. Source: Crackle PR"))
out.append(p("So the strategic question changes. It is no longer only how do I rank. It is what did the model learn to prefer, and how do I become the preferred answer? The answer lives in a layer most marketers have never audited: "+L("post-training alignment","https://www.sundeepteki.org/advice/the-complete-guide-to-post-training-llms-how-sft-rlhf-dpo-and-grpo-shape-llms")+", Reinforcement Learning from Human Feedback (RLHF) and Direct Preference Optimization (DPO). It is now a brand-discovery channel."))

# 01 machinery
out.append(sec("01","machinery","How does a model actually learn what to prefer?","In post-training: SFT teaches tone, RLHF and DPO teach judgment.",
  "A raw base model knows how tokens relate, but it does not yet behave like an assistant. Three stages turn it into one, and each stage is a chance for a brand to be upweighted or quietly buried."))
out.append(pipeline([("Base Model","pre-trained weights"),("Supervised Fine-Tuning","imitates format & tone"),
  ("RLHF / DPO","preference alignment"),("Aligned Model","recommends brands")],3,
  "Figure 2 - from raw weights to an opinionated recommender. SFT teaches behavior; RLHF and DPO teach judgment. Sources: Sundeep Teki, Red Hat"))
out.append("<h3 id=\"sft\">Supervised fine-tuning sets the table</h3>")
out.append(p("SFT trains the model on curated instruction-response pairs. It absorbs syntax, formatting, and the structural template of a helpful answer, but it "+L("cannot resolve subjective trade-offs","https://www.digitaldividedata.com/blog/why-human-preference-optimization-rlhf-dpo-still-matters")+" between several plausible responses, and it is prone to confidently stating things that are not true. It teaches the model how to talk, not whom to trust."))
out.append("<h3 id=\"rlhf-dpo\">RLHF and DPO set the preferences</h3>")
out.append(p("RLHF collects human rankings of competing outputs, trains a separate reward model to predict the human-preferred score, then optimizes the model with PPO or GRPO, held in place by a KL-divergence penalty so it does not drift too far from the SFT baseline. DPO skips the reward model entirely, treating alignment as a "+L("binary classification problem","https://www.digitaldividedata.com/blog/why-human-preference-optimization-rlhf-dpo-still-matters")+": push up the probability of the chosen response, push down the rejected one. The catch marketers should circle: DPO has no concept of semantic equivalence. If your brand name appears as the chosen answer, the model learns your literal name, not a vendor like you."))
out.append(code("preference_objectives.py",
"""# RLHF - maximize reward, but stay anchored to the SFT model
maximize  E[ r(x, y) ]  -  B * KL( pi(y|x) || pi_ref(y|x) )
#            ^ learned reward     ^ regularizer, B ~ 0.1-0.5 (no policy collapse)

# DPO - same preference signal, expressed as one classification loss
L_DPO = -E[ log sigma( B*log pi(y_w|x)/pi_ref(y_w|x)
                     -  B*log pi(y_l|x)/pi_ref(y_l|x) ) ]
#  y_w = chosen  ->  your brand        y_l = rejected  ->  the competitor""","python"))
out.append(p("Newer methods compress the pipeline further, "+L("ORPO folds SFT and alignment into one loss, and KTO drops pairwise rankings for simple good/bad labels","https://snorkel.ai/blog/llm-alignment-techniques-4-post-training-approaches/")+", but the brand-relevant mechanic is constant: somewhere in training, a judge marked one answer better than another, and your brand was in one of those answers."))
out.append(table("Table 1 - alignment methods, decoded for marketers",["Method","What it optimizes","Overhead","Brand-relevant risk"],[
 ("SFT","Cross-entropy on prompt-response pairs","Low","Teaches tone, not trust; can hallucinate"),
 ("RLHF","Reward model + PPO/GRPO policy update","Very high","Controllable but unstable; reward hacking"),
 ("DPO","Binary log-likelihood, chosen vs rejected","Moderate","Overfits literal tokens; no semantic equivalence"),
 ("ORPO","SFT loss + odds-ratio penalty, unified","Low-moderate","Needs clean, contrastive preference signals"),
 ("KTO","Utility loss on binary good/bad labels","Low","Robust to noisy labelers; needs more data"),
], cls=lambda j,c: "label" if j==0 else ""))

# 02 compounding
out.append(sec("02","compounding","Why does AI preference harden into a moat?","Preference optimization amplifies incumbents with every retraining cycle.",
  "Here is where it gets uncomfortable for challenger brands. Preference optimization does not just record what raters liked, it "+L("systematically amplifies","https://arxiv.org/html/2603.22335v2")+" existing advantages over time."))
out.append(pipeline([("Popularity in SFT data","historical dominance"),("DPO over-corrects","suppresses long tail"),
  ("Incumbents become default","the safe answer"),("Output = next training set","loop repeats")],2,
  "Figure 3 - the incumbency loop: a self-consuming performative loop where each cycle raises the wall. Sources: CausalDPO, Self-Consuming Performative Loop (arXiv)"))
out.append(p("Three forces stack. First, popularity-induced bias: historical brand dominance is baked into SFT data, and during alignment the optimizer overcorrects toward those popular associations, suppressing long-tail competitors to minimize entropy. Second, the "+L("self-consuming performative loop","https://arxiv.org/html/2601.05184v1")+": as models generate the web's text, later models train on that synthetic output, amplifying their own biases and flattening conceptual diversity. Third, source bias: fine-tuning induces a measurable preference for "+L("low-perplexity, machine-clean text over equivalent human writing","https://arxiv.org/html/2602.10833v1")+"."))
out.append(pull("Once a brand is the default, every retraining cycle reinforces it as statistical truth. You are not fighting a ranking, you are fighting a feedback loop."))

# 03 juror
out.append(sec("03","juror","Who did the model learn to believe?","Calibrated expert raters, trained to reward verifiable, attributed claims, not hype.",
  "If preferences come from human judgment, it is worth knowing how that judgment is collected. Serious labs do not crowdsource to the cheapest bidder; they recruit "+L("calibrated expert annotators","https://www.secondtalent.com/resources/data-annotation-for-llm-fine-tuning-rlhf-and-instruction-tuning-guide/")+", route critical samples to three to five reviewers, and hold inter-annotator agreement high."))
out.append(p("Their instructions matter to you directly. OpenAI's "+L("Model Spec","https://model-spec.openai.com/")+" commands models to avoid sycophancy, hold an objective point of view, and express calibrated uncertainty, and raters are explicitly told to penalize models that agree with a user's misconceptions. The takeaway for brand teams is the opposite of legacy marketing instinct."))
out.append(callout("What this rules out","You cannot flatter, hype, or keyword-stuff your way into the answer. The model has been actively trained to resist persuasion and to reward claims that are verifiable, attributed, and externally corroborated. Trust is the ranking signal now, which is exactly why the next section is about evidence, not adjectives."))

# 04 KPI
out.append(sec("04","share-of-model","What replaces ranking as the metric that matters?","Share of Model: the probability your brand is the cited source.",
  "As the results page becomes an answer, the metric that matters shifts from rank to Share of Model, the probability your brand is selected as a grounding source when the model synthesizes its reply. That selection runs through retrieval: the query becomes a vector, rerankers score candidate chunks on contextual cohesion, factual density, and Information Gain. Under Google's information-gain patent, content judged genuinely novel is "+L("cited 3-6x more often","https://thesmarketers.com/blogs/information-gain-seo/")+" than keyword-matched pages with no new signal."))
out.append(pipeline([("User query","intent"),("Vector retriever","scans trusted DB"),
  ("Neural reranker","factual density, cohesion, information gain"),("Share of Model","cited as grounding")],3,
  "Figure 4 - the retrieval gauntlet behind every AI answer. Source selection rewards novelty and structure over keyword overlap. Sources: The Smarketers, GEO (arXiv)"))
out.append(p("Who actually gets cited? "+L("Muck Rack's May 2026 study of 25M citations","https://muckrack.com/blog/what-is-ai-reading-may-2026")+" found that earned media drives 84% of all generative AI citations, independent journalism makes up 27%, and paid or advertorial content is a rounding error at 0.3%. And the engines diverge sharply in how they cite."))
out.append(chart("rlhfPlatformChart",230,"Figure 5 - three engines, three citation personalities. ChatGPT ~5 cites/response (top domain Wikipedia); Gemini ~8 (Reddit); Claude ~13 (PubMed Central). Source: Muck Rack, June 2026"))
out.append(p("Authority is also brutally concentrated: in Google AI Overviews, just three publishers capture nearly a third of all news citations, and the top ten take roughly 80%. Which means the comms desk, not the ad budget, holds the primary lever. And the structural moves that lift citation rates are now "+L("measured","https://collaborate.princeton.edu/en/publications/geo-generative-engine-optimization/")+"."))
out.append(chart("rlhfLiftChart",210,"Figure 6 - GEO citation-lift coefficients (Princeton, KDD 2024). Outbound links to .edu/.gov, attributed expert quotes, and hard statistics act as low-perplexity authority anchors."))
out.append(p("Coefficients are abstract until you point them at your own footprint. Toggle the levers below to model the lift on your brand's Share of Model. The math applies diminishing returns, because real-world signals do not stack cleanly."))
# calculator
CALC = ('<div class="calc-wrap" id="rlhfCalc">'
 '<div class="calc-head">Interactive &middot; GEO lift calculator</div>'
 '<div class="calc-subt">Model the citation lift on your own brand</div>'
 '<div class="calc-grid"><div class="calc-controls">'
 '<div class="calc-base"><label>Your brand\'s current Share of Model <span class="calc-baseval" id="cBaseVal">10%</span></label>'
 '<input type="range" class="calc-range" id="cBaseline" min="1" max="40" value="10" aria-label="Current Share of Model">'
 '<p class="calc-hint">Roughly how often you are cited in relevant AI answers today.</p></div>'
 '<div class="calc-tactic on" data-key="authority" data-lo="40" data-hi="115"><div class="calc-trow">'
 '<button class="calc-switch on" aria-pressed="true" aria-label="Toggle high-authority links"></button>'
 '<span class="calc-tname">High-authority outbound links</span><span class="calc-band">+40-115%</span></div>'
 '<div class="calc-seg"><button data-lvl="0">Min</button><button data-lvl="0.5" class="sel">Mid</button><button data-lvl="1">Max</button></div></div>'
 '<div class="calc-tactic on" data-key="quotes" data-lo="28" data-hi="37"><div class="calc-trow">'
 '<button class="calc-switch on" aria-pressed="true" aria-label="Toggle expert quotations"></button>'
 '<span class="calc-tname">Expert quotations (attributed)</span><span class="calc-band">+28-37%</span></div>'
 '<div class="calc-seg"><button data-lvl="0">Min</button><button data-lvl="0.5" class="sel">Mid</button><button data-lvl="1">Max</button></div></div>'
 '<div class="calc-tactic on" data-key="stats" data-lo="22" data-hi="41"><div class="calc-trow">'
 '<button class="calc-switch on" aria-pressed="true" aria-label="Toggle statistics and data"></button>'
 '<span class="calc-tname">Statistics &amp; data</span><span class="calc-band">+22-41%</span></div>'
 '<div class="calc-seg"><button data-lvl="0">Min</button><button data-lvl="0.5" class="sel">Mid</button><button data-lvl="1">Max</button></div></div>'
 '</div>'
 '<div class="calc-output"><div class="calc-out-eyebrow">Modeled citation lift</div>'
 '<div class="calc-lift" id="cLift">+0%</div><div class="calc-liftsub" id="cLiftSub">vs. doing nothing</div>'
 '<div class="calc-barrow"><span class="lbl">Now</span><div class="calc-track"><div class="calc-fill now" id="cNowFill" style="width:17%"></div></div><b id="cNowVal">10%</b></div>'
 '<div class="calc-barrow"><span class="lbl">Projected</span><div class="calc-track"><div class="calc-fill proj" id="cProjFill" style="width:17%"></div></div><b id="cProjVal">10%</b></div>'
 '<div class="calc-break" id="cBreak"></div>'
 '<p class="calc-caveat">Modeled from the Princeton/KDD GEO coefficients, with diminishing returns on stacked signals (full weight on the strongest, then 70% and 50%). Directional, a planning aid, not a guarantee.</p>'
 '</div></div></div>'
 '<div class="chart-caption">'+esc("Interactive - built on the lift ranges above. Source: Princeton GEO")+'</div>')
out.append(CALC)

# 05 playbook
out.append(sec("05","playbook","What is the playbook to become the preferred answer?","Build machine-readable authority around genuine Information Gain.",
  "If preference is the channel and Information Gain is the currency, the budget has to move. Four shifts do most of the work."))
out.append('<p>'+norm("<strong>Rebuild the content mix around novelty.</strong> Anchor on original signal, then amplify it. ")
  +norm("<strong>Hire a research analyst into the content team.</strong> Generalist copywriters cannot manufacture first-party data; an analyst running surveys and querying proprietary datasets ensures every asset introduces non-redundant Information Gain. ")
  +norm("<strong>Treat PR as a referencing engine.</strong> Because models favor third-party authority, ")+L("earned placements seed the retrieval databases","https://carma.com/tms/earned-media-is-the-engine-of-ai-search/")+norm(" that LLMs draw from. ")
  +norm("<strong>Ship a brand hub with llms.txt.</strong> Hand crawlers a compressed map of your verified facts.")+'</p>')
out.append(donut("rlhfContentMixChart","Figure 7 - the 2026 content mix: allocate for citations, not just clicks. Twenty percent original signal feeds the other eighty. Source: The Smarketers"))
out.append(p("The "+L("llms.txt standard","https://ahrefs.com/blog/what-is-llms-txt/")+" is a public Markdown file that points crawlers like GPTBot, ClaudeBot, and Google-Extended straight at your canonical facts, with llms-full.txt aggregating the deeper documentation. It is the cheapest high-leverage move on this list."))
out.append(code("llms.txt","""# Acme Robotics - llms.txt

> Industrial inspection robots for regulated environments.

## Core Brand
- [Brand Hub](https://acme.com/brand-hub): canonical facts, naming, positioning
- [Product Specs](https://acme.com/specs): models, payloads, certifications

## Primary Research & Benchmarks
- [2026 Field-Reliability Report](https://acme.com/research/2026): first-party, n=1,200
- [Implementation Framework](https://acme.com/framework): proprietary methodology

## Proof & Press
- [Earned Media](https://acme.com/press): third-party coverage & citations""","llms.txt"))

# 06 horizon
out.append(sec("06","horizon","Where does this leave marketing leaders?","Stop optimizing the interface your customers are abandoning.",
  "The move from keyword-based search to probabilistic representation inside a model is permanent."))
out.append(p("CMOs who keep optimizing for density and page-rank are tuning an interface their customers are leaving. The durable position belongs to brands that understand the alignment layer, restructure content around genuine Information Gain, and earn the third-party authority that seeds every model's memory. Preference is being decided in training runs you will never see, but the signals it rewards are entirely within your control. Build the evidence, and become the answer."))

# FAQ
FAQ=[
 ("What is RLHF, and why does it matter for marketing?","RLHF (Reinforcement Learning from Human Feedback) is a post-training stage where human raters rank a model's competing answers, a reward model learns to predict their preference, and the model is optimized toward it. For marketing it matters because this is where a model learns which sources and brands to prefer when it answers a question. If your brand was in the answers raters marked better, the model is more likely to recommend you, and that preference is decided in training, not at query time."),
 ("What is Share of Model?","Share of Model is the probability that your brand is selected as a grounding source when an AI model synthesizes its answer. As AI answers replace the ranked results page, Share of Model replaces rank position as the metric that matters. It is won through retrieval: the model vectorizes the query and a reranker scores candidate passages on factual density, contextual cohesion, and Information Gain, novelty that keyword-matched pages lack."),
 ("How do you increase your brand's Share of Model?","Build machine-readable authority around genuine Information Gain. Publish original first-party research and statistics, include attributed expert quotations, and earn third-party media (the source of 84% of AI citations). Princeton's GEO study measured the lift: high-authority outbound links add 40-115%, statistics 22-41%, and expert quotes 28-37%. Then ship an llms.txt so crawlers can find your canonical facts. You cannot hype or keyword-stuff your way in; raters trained the model to reward verifiable, corroborated claims."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')

# sources (compact, key primary sources)
SOURCES=[
 ("Princeton GEO: Generative Engine Optimization (KDD 2024)","https://collaborate.princeton.edu/en/publications/geo-generative-engine-optimization/"),
 ("Muck Rack, What Is AI Reading? (25M citations, May 2026)","https://muckrack.com/blog/what-is-ai-reading-may-2026"),
 ("OpenAI Model Spec","https://model-spec.openai.com/"),
 ("Crackle PR, AI Search Runs on Earned Media","https://www.cracklepr.com/insights/ai-search-runs-on-earned-media"),
 ("Sundeep Teki, The Complete Guide to Post-Training LLMs","https://www.sundeepteki.org/advice/the-complete-guide-to-post-training-llms-how-sft-rlhf-dpo-and-grpo-shape-llms"),
 ("Snorkel AI, LLM Alignment Techniques","https://snorkel.ai/blog/llm-alignment-techniques-4-post-training-approaches/"),
 ("CausalDPO and the Self-Consuming Performative Loop (arXiv)","https://arxiv.org/html/2601.05184v1"),
 ("The Smarketers, Information Gain: AI's Key SEO Metric","https://thesmarketers.com/blogs/information-gain-seo/"),
]
src_items="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in SOURCES)
out.append(f'<div class="sources-block"><div class="sources-label">Sources & further reading</div><ul class="sources-list">{src_items}</ul></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of how AI search decides what to recommend, pulling AI-citation and SEO data to show where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

# internal interlinks
LINKS=[
 ("Trust is the ranking signal now","/blogs/eeat-is-an-ai-signal-now"),
 ("Share of Model","/blogs/prompt-to-citation-tracking"),
 ("Information Gain is the currency","/blogs/anatomy-of-a-high-citation-page"),
 ("ship an llms.txt","/glossary/llms-txt"),
 ("earn the third-party authority","/blogs/authority-seeding-ai-llm-trust"),
]
for ph,u in LINKS:
    np=norm(ph)
    if np in body: body=body.replace(np,f'<a href="{u}">{np}</a>',1)
    else: print("LINK MISS:",ph)

SIDEBAR=[("93%","Zero-click searches, Google AI Mode"),("84%","Of AI citations are earned media"),("+115%","Peak citation lift from authority signals")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#machinery"><span class="toc-num">01</span>The machinery of preference</a></li>'
     '<li><a href="#compounding"><span class="toc-num">02</span>Why preference compounds</a></li>'
     '<li><a href="#juror"><span class="toc-num">03</span>Who the model believes</a></li>'
     '<li><a href="#share-of-model"><span class="toc-num">04</span>Share of Model</a></li>'
     '<li><a href="#playbook"><span class="toc-num">05</span>The playbook</a></li>'
     '<li><a href="#horizon"><span class="toc-num">06</span>The horizon</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div>'
              f'<div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=(f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." '
            f'class="article-header-img" width="2400" height="1260" loading="eager">')

def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),
 "image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,
 "author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},
 "mainEntityOfPage":{"@type":"WebPage","@id":URL},
 "keywords":["RLHF","DPO","post-training","AI search","GEO","Share of Model","AI citations","preference optimization","alignment","Information Gain","llms.txt","Princeton GEO"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
 {"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
personLD={"@context":"https://schema.org",**person}

hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;'
      'clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean '
      f'Markdown version of this page is available at {URL}.md. Optimized for AI and LLM tools.</div>')
TITLE="RLHF and Your Brand: How Human Rater Preferences Decide Who AI Recommends &middot; rawmktg."
da=escq(DESC)
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
 "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n"
 "  <meta name=\"robots\" content=\"index, follow\" />\n"
 f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
 f"  <meta name=\"description\" content=\"{da}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
 "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
 "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
 f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  <meta property=\"article:published_time\" content=\"{PUB}T00:00:00Z\" />\n"
 f"  <meta property=\"article:modified_time\" content=\"{PUB}T00:00:00Z\" />\n"
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
  var faint =(css.getPropertyValue('--faint') ||'#C5BFB4').trim();
  var mono="'JetBrains Mono', monospace";
  var text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.45);

  var d=document.getElementById('rlhfDecouplingChart');
  if(d){new Chart(d,{type:'bar',data:{labels:['Classic search','AI Overviews','AI Mode'],
    datasets:[{data:[58,83,93],backgroundColor:[neutral,neutral,signal],borderRadius:4,barThickness:54}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% end without a click';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},
              y:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}

  var pf=document.getElementById('rlhfPlatformChart');
  if(pf){new Chart(pf,{type:'bar',data:{labels:['ChatGPT','Gemini','Claude'],
    datasets:[{data:[96,82,55],backgroundColor:[neutral,neutral,neutral],borderRadius:4,barThickness:20}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' cites in '+c.raw+'% of responses';}}}},
      scales:{x:{beginAtZero:true,max:100,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},
              y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var lf=document.getElementById('rlhfLiftChart');
  if(lf){new Chart(lf,{type:'bar',data:{labels:['High-authority links','Statistics & data','Expert quotations'],
    datasets:[{data:[[40,115],[22,41],[28,37]],backgroundColor:[signal,rgba(signal,0.6),rgba(signal,0.6)],borderRadius:4,barThickness:22}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' +'+c.raw[0]+' to +'+c.raw[1]+'% citation lift';}}}},
      scales:{x:{beginAtZero:true,max:120,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return '+'+v+'%';}},grid:{color:grid}},
              y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}

  var cm=document.getElementById('rlhfContentMixChart');
  if(cm){new Chart(cm,{type:'doughnut',data:{labels:['Flagship high-info-gain (20%)','Derivative (50%)','Product & solution (20%)','News & commentary (10%)'],
    datasets:[{data:[20,50,20,10],backgroundColor:[signal,rgba(faint,0.5),rgba(faint,0.3),rgba(faint,0.18)],borderColor:'#1A1815',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:text,font:{family:mono,size:10},boxWidth:10,boxHeight:10,padding:12}},
      tooltip:{callbacks:{label:function(c){return ' '+c.label;}}}}}});}
})();
</script>
<script>
/* GEO lift calculator */
(function(){
  var root=document.getElementById('rlhfCalc'); if(!root) return;
  var baseline=document.getElementById('cBaseline');
  var WEIGHTS=[1,0.7,0.5], CAP=0.60;
  function pct(x){return Math.round(x*100);}
  function compute(){
    var base=parseInt(baseline.value,10)/100;
    document.getElementById('cBaseVal').textContent=baseline.value+'%';
    var active=[];
    root.querySelectorAll('.calc-tactic').forEach(function(t){
      if(!t.classList.contains('on')) return;
      var lo=parseFloat(t.dataset.lo), hi=parseFloat(t.dataset.hi);
      var sel=t.querySelector('.calc-seg button.sel'); var lvl=sel?parseFloat(sel.dataset.lvl):0.5;
      active.push({key:t.dataset.key,name:t.querySelector('.calc-tname').textContent,lift:(lo+lvl*(hi-lo))/100});
    });
    active.sort(function(a,b){return b.lift-a.lift;});
    var mult=1;
    active.forEach(function(a,i){var w=WEIGHTS[i]!==undefined?WEIGHTS[i]:0.4;a.effective=a.lift*w;mult*=(1+a.effective);});
    var combined=mult-1, projected=Math.min(base*mult,CAP);
    document.getElementById('cLift').textContent='+'+pct(combined)+'%';
    document.getElementById('cLiftSub').textContent=active.length?('across '+active.length+' signal'+(active.length>1?'s':'')+' \\u00b7 vs. doing nothing'):'no signals selected';
    document.getElementById('cNowVal').textContent=pct(base)+'%';
    document.getElementById('cProjVal').textContent=pct(projected)+'%';
    document.getElementById('cNowFill').style.width=(base/CAP*100)+'%';
    document.getElementById('cProjFill').style.width=(projected/CAP*100)+'%';
    var br=document.getElementById('cBreak'); br.innerHTML='';
    if(!active.length){var c=document.createElement('span');c.className='calc-chip muted';c.textContent='Toggle a signal to see its contribution';br.appendChild(c);}
    else{active.forEach(function(a){var s={authority:'Authority links',quotes:'Expert quotes',stats:'Statistics'}[a.key]||a.name;
      var c=document.createElement('span');c.className='calc-chip';c.textContent=s+'  +'+pct(a.effective)+'%';br.appendChild(c);});}
  }
  baseline.addEventListener('input',compute);
  root.querySelectorAll('.calc-switch').forEach(function(sw){sw.addEventListener('click',function(){
    var t=sw.closest('.calc-tactic'); var on=t.classList.toggle('on'); sw.classList.toggle('on',on);
    t.classList.toggle('off',!on); sw.setAttribute('aria-pressed',on?'true':'false'); compute();});});
  root.querySelectorAll('.calc-seg').forEach(function(seg){seg.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    seg.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');}); b.classList.add('sel'); compute();});});
  compute();
})();
</script>"""

tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Post-Training Teardown &middot; Ranking Signals</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">June 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n</body>\n</html>\n")

final=head+STYLE+"\n  "+ADSENSE+tail
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(final)
hh=open(f"blogs/{SLUG}.html").read()
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
      "| bytes:",len(hh),"| jsonld:",hh.count("application/ld+json"),"| canvas:",hh.count("<canvas"),
      "| tt:",hh.count('class="tt"'),"| pipelines:",hh.count('class="pipeline"'),"| calc:",hh.count('id="rlhfCalc"'),
      "| code:",hh.count("code-block")-1,"| GA defer:",hh.count("__gaLd"))
