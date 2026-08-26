#!/usr/bin/env python3
"""SCRATCH: build 2 digital-PR tool pages (CSD scorer, Dark AI revenue estimator). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
T=open("tools/page-citability-analyzer.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
STYLE=sl("<style>","</style>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
ADSENSE=''
def esc(t): return H.escape(t,quote=False)
def escq(t): return H.escape(t,quote=True)

def page(slug,title,desc,eyebrow,headline,deck,body,method,script,faqs):
    URL=f"https://rawmktg.com/tools/{slug}"
    schema=[
      {"@context":"https://schema.org","@type":"WebApplication","name":headline,"url":URL,"description":desc,"applicationCategory":"BusinessApplication","operatingSystem":"Web, all browsers","browserRequirements":"Requires JavaScript","isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"}},
      {"@context":"https://schema.org","@type":"WebPage","name":headline,"url":URL,"description":desc,"isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://rawmktg.com/tools"},{"@type":"ListItem","position":3,"name":headline,"item":URL}]},
      {"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
    ]
    sj="\n  ".join('<script type="application/ld+json">'+json.dumps(o)+'</script>' for o in schema)
    head=(f'<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8" />\n  {GA}\n'
      '  <meta name="google-adsense-account" content="ca-pub-5952288317022852" />\n  <meta name="robots" content="index, follow" />\n'
      f'  <title>{esc(title)}</title>\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
      f'  <meta name="description" content="{escq(desc)}" />\n  <meta name="author" content="Vinayak Ravi" />\n'
      '  <link rel="icon" type="image/x-icon" href="/favicon.ico" />\n'
      '  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png" />\n'
      '  <link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16.png" />\n'
      '  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/favicon-180.png" />\n'
      f'  <link rel="canonical" href="{URL}" />\n'
      f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
      '  <meta property="og:type" content="website" />\n'
      f'  <meta property="og:url" content="{URL}" />\n  <meta property="og:title" content="{escq(headline)}" />\n'
      f'  <meta property="og:description" content="{escq(desc)}" />\n  <meta property="og:site_name" content="rawmktg." />\n'
      '  <meta property="og:image" content="https://rawmktg.com/assets/images/og-default.png" />\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />\n'
      '  <meta name="twitter:card" content="summary_large_image" />\n'
      f'  <meta name="twitter:title" content="{escq(headline)}" />\n  <meta name="twitter:description" content="{escq(desc)}" />\n'
      '  <meta name="twitter:image" content="https://rawmktg.com/assets/images/og-default.png" />\n'
      f'  {sj}\n'
      '  <link rel="alternate" type="application/rss+xml" title="rawmktg." href="https://rawmktg.com/feed.xml" />\n  '
      +FONTS+'\n  ')
    hdr=(f'<div class="page">\n  <header class="article-header">\n'
      f'    <div class="article-eyebrow"><span class="eyebrow-tag">{eyebrow}</span><span class="eyebrow-sep">&middot;</span><span class="eyebrow-date">Updated Aug 2026</span></div>\n'
      f'    <h1 class="article-headline">{esc(headline)}</h1>\n    <p class="article-deck">{esc(deck)}</p>\n  </header>\n</div>\n')
    html=(head+STYLE+'\n  <link rel="stylesheet" href="/assets/tools.css" />\n  '+ADSENSE+'\n</head>\n<body>\n\n'
      +NAV+'\n\n'+hdr+'\n<main class="toolpage" id="article-main">\n  <div class="page">\n'
      +body+'\n'+method+'\n  </div>\n</main>\n\n'+NEWS+'\n\n'+FOOT+'\n'+script+'\n</body>\n</html>\n')
    open(f"tools/{slug}.html","w",encoding="utf-8").write(html)
    return html

def method(h2,intro,steps,faqs,related):
    ol="".join(f"<li>{s}</li>" for s in steps)
    fq="".join(f'<h3>{esc(q)}</h3><p>{esc(a)}</p>' for q,a in faqs)
    rel="".join(f'<a href="{u}">{esc(t)} &rarr;</a>' for t,u in related)
    return (f'<section class="method"><h2>{esc(h2)}</h2><p>{intro}</p>'
      f'<h3>How to use it</h3><ol>{ol}</ol>{fq}'
      f'<div class="srcs">{rel}</div></section>')

REL=[("Digital PR and data studies: the link play AI cites","/blogs/mentions-beat-links"),
     ("The anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page")]

# ============ TOOL 1: CITABLE STAT DENSITY SCORER ============
SAMPLE=("41% of B2B marketing teams published zero original research in 2025, up from 28% the year before.\n"
 "Source: RawMktg Original Research Census 2026, n=1,204, margin of error +/- 2.8pp.\n"
 "Most teams say research is important but few actually invest in it.\n"
 "\"Teams cut research first because it is the only line item with no weekly dashboard,\" said Priya Menon, VP Demand Generation at Northwind.\n"
 "Onboarding takes a significant amount of time for most mid-market accounts.\n"
 "Companies over 1,000 staff were 5x more likely to publish 3+ studies a year than those under 200, per the same survey.")
t1_body=('<section class="card" id="csd">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Paste your research draft</div>'
  '<div class="fld"><div class="lab">One claim per line. The scorer rates each and computes density.</div>'
  '<textarea class="ta" id="csdIn" rows="10" placeholder="Paste your findings, one claim or sentence per line"></textarea></div>'
  '<div class="btn-row" style="margin-top:8px"><button class="tbtn" id="csdSample" type="button">Load sample</button></div>'
  '<p class="hint" style="margin:10px 0 0">Each line scores +2 for a precise number, +2 for a named method (n=, sample, margin of error), +2 for attribution (said, according to), -1 for a hedge (most, many, significant), +1 for fitting a chunk (45 words or fewer). 5+ is citable. A research hub should clear a density of 4 per 1,000 words.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Citable stat density</div>\n'
  '      <div class="scorewrap"><span class="score" id="csdScore">0</span><span class="score-d">/ 1,000 words</span></div>\n'
  '      <span class="scoreband" id="csdBand" style="background:rgba(255,255,255,.1);color:#fff">Paste a draft</span>\n'
  '      <div class="gauge"><div class="gfill" id="csdFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">Line by line</div><div id="csdNote"><p class="hint">Per-claim verdicts appear here.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t1_method=method(
  "What citable stat density measures",
  "A generative engine does not lift your study. It lifts a stat unit: the smallest self-contained block carrying a precise number, a named methodology, and an attributed quote. Citable stat density counts how many of those extractable units your document holds per thousand words. A general blog post scores under 1. A well-built research hub clears 4. Below 2 you have written an essay with numbers in it, which a model can read but will not confidently repeat.",
  ["Paste your draft, one claim or sentence per line.",
   "Read the per-line verdict: CITABLE, WEAK (add a method or attribution), or REWRITE.",
   "Fix the WEAK and REWRITE lines first, usually a missing methodology or a hedge word that should be a number.",
   "Watch the density figure climb as you tighten claims. Aim to clear 4 per 1,000 words before the study ships."],
  [("What is a good citable stat density?","Clear 4 extractable units per 1,000 words for a research hub. A general blog post scores under 1, and below 2 the document reads as narrative with numbers rather than a set of liftable facts. The number matters less than the per-line verdicts: every WEAK or REWRITE line is a finding a model cannot confidently quote."),
   ("How is each line scored?","Plus 2 for a precise number, plus 2 for a named method (n=, sample, surveyed, margin of error), plus 2 for attribution (said, according to, per, told), minus 1 for a qualitative hedge (most, many, significant, leading), and plus 1 if the line is 45 words or fewer so it fits a retrieval chunk. Five or more is citable; three to four is weak; below three needs a rewrite."),
   ("Why do hedge words lower the score?","Because a model cannot repeat most teams or a significant share as a fact. Retrieval weights precise, verifiable claims and discounts qualitative filler, so a hedge is a missed stat unit. Replace the hedge with the number it is standing in for, and add the methodology that makes the number trustworthy."),
   ("Does my draft leave the browser?","No. Every line is scored entirely in your browser with simple pattern matching. Nothing you paste is uploaded, stored or sent to any server.")],
  REL+[("Page Citability Analyzer","/tools/page-citability-analyzer")])
t1_script=r'''<script>
(function(){
  var root=document.getElementById('csd'); if(!root) return;
  var SAMPLE="41% of B2B marketing teams published zero original research in 2025, up from 28% the year before.\nSource: RawMktg Original Research Census 2026, n=1,204, margin of error +/- 2.8pp.\nMost teams say research is important but few actually invest in it.\n\"Teams cut research first because it is the only line item with no weekly dashboard,\" said Priya Menon, VP Demand Generation at Northwind.\nOnboarding takes a significant amount of time for most mid-market accounts.\nCompanies over 1,000 staff were 5x more likely to publish 3+ studies a year than those under 200, per the same survey.";
  var NUM=/\b\d+(?:\.\d+)?\s?(?:%|pp|x|bn|m|k)?\b/i;
  var ATTR=/\b(said|according to|per|told)\b/i;
  var HEDGE=/\b(many|most|some|often|significant|leading|robust)\b/i;
  var METHOD=/\b(n\s?=|sample|surveyed|fielded|margin of error)\b/i;
  function scoreLine(t){
    var s=0;
    if(NUM.test(t)) s+=2;
    if(METHOD.test(t)) s+=2;
    if(ATTR.test(t)) s+=2;
    if(HEDGE.test(t)) s-=1;
    if(t.split(/\s+/).filter(Boolean).length<=45) s+=1;
    return s;
  }
  function verdict(s){ return s>=5?'CITABLE':(s>=3?'WEAK':'REWRITE'); }
  function compute(){
    var raw=document.getElementById('csdIn').value.split('\n').map(function(x){return x.trim();}).filter(Boolean);
    var sEl=document.getElementById('csdScore'),band=document.getElementById('csdBand'),fill=document.getElementById('csdFill'),note=document.getElementById('csdNote');
    if(!raw.length){sEl.textContent='0';band.textContent='Paste a draft';band.style.background='rgba(255,255,255,.1)';band.style.color='#fff';fill.style.width='0%';note.innerHTML='<p class="hint">Per-claim verdicts appear here.</p>';return;}
    var words=0, citable=0, rows=[];
    raw.forEach(function(t){
      var s=scoreLine(t), v=verdict(s); words+=t.split(/\s+/).filter(Boolean).length;
      if(s>=5) citable++;
      rows.push([s,v,t]);
    });
    var csd = words? citable/(words/1000) : 0;
    sEl.textContent=csd.toFixed(1);
    var pct=Math.min(csd/6*100,100); fill.style.width=pct+'%';
    var lbl,col; if(csd>=4){lbl='Research-hub grade';col='var(--up)';}else if(csd>=2){lbl='Thin, tighten it';col='#C9922E';}else{lbl='Essay with numbers';col='var(--signal)';}
    band.textContent=lbl;band.style.background=col;band.style.color='#0b0b0c';fill.style.background=col;
    var vc={CITABLE:'var(--up)',WEAK:'#C9922E',REWRITE:'var(--signal)'};
    var html='<div class="lt-stat"><span>Citable units</span><strong>'+citable+' of '+raw.length+'</strong></div>'
      +'<div class="lt-stat"><span>Words</span><strong>'+words.toLocaleString()+'</strong></div>'
      +'<div class="gaps-h" style="margin-top:12px">Claims</div>';
    rows.forEach(function(r){
      var t=r[2]; if(t.length>60) t=t.slice(0,58)+'..';
      html+='<div class="lt-stat"><span style="color:rgba(255,255,255,.62)">'+t.replace(/</g,'&lt;')+'</span><strong style="color:'+vc[r[1]]+'">'+r[1]+' '+r[0]+'</strong></div>';
    });
    note.innerHTML=html;
  }
  document.getElementById('csdIn').addEventListener('input',compute);
  document.getElementById('csdSample').addEventListener('click',function(){document.getElementById('csdIn').value=SAMPLE;compute();});
  compute();
})();
</script>'''

# ============ TOOL 2: DARK AI REVENUE ESTIMATOR ============
t2_body=('<section class="card" id="dai">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Pull three numbers from GA4</div>'
  '<div class="fld"><div class="lab">Monthly Direct sessions</div><input class="tin" id="daiSess" inputmode="numeric" placeholder="e.g. 84000"></div>'
  '<div class="fld"><div class="lab">Conversions from the Direct bucket</div><input class="tin" id="daiConv" inputmode="numeric" placeholder="e.g. 3120"></div>'
  '<div class="fld"><div class="lab">Average order value or ACV ($)</div><input class="tin" id="daiAcv" inputmode="numeric" placeholder="e.g. 9400"></div>'
  '<p class="hint" style="margin:8px 0 0">About 70.6% of AI referrals arrive with the referrer stripped and land in Direct. Dark-AI sessions convert near 10.21% against a 2.46% genuine-direct baseline, so an inflated Direct conversion rate is the tell. This is a model, not a measurement. Label it as one in any deck.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Hidden AI revenue (monthly)</div>\n'
  '      <div class="scorewrap"><span class="score" id="daiRev" style="font-size:38px">$0</span></div>\n'
  '      <span class="scoreband" id="daiBand" style="background:rgba(255,255,255,.1);color:#fff">Enter your Direct numbers</span>\n'
  '      <div class="gauge"><div class="gfill" id="daiFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">What is hiding in Direct</div><div id="daiNote"><p class="hint">The decomposition appears here.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t2_method=method(
  "What the Dark AI estimator does",
  "Roughly 70.6% of generative AI referral sessions arrive with the HTTP referrer header stripped, so GA4 files them under Direct. Those sessions convert at around 10.21% against a 2.46% genuine-direct baseline, which means a Direct bucket with an unusually high conversion rate is hiding your highest-intent AI traffic. This tool solves the mix: given your Direct sessions and conversions, it backs out how many are likely dark AI and what revenue that represents, then cross-checks the count against the 70.6% referrer-stripped share.",
  ["Pull monthly Direct sessions and the conversions attributed to Direct from GA4.",
   "Enter your average order value or annual contract value.",
   "Read the implied dark-AI session count, the hidden conversions, and the monthly revenue they represent.",
   "Treat the output as a directional model, and confirm it by tagging placed URLs and cohorting Direct by landing page."],
  [("How does it separate dark AI from genuine direct?","It solves one equation: your total Direct conversions equal dark-AI sessions at a 10.21% rate plus genuine-direct sessions at a 2.46% rate. Given the totals, only one split of the bucket fits, which yields the implied dark-AI session count. It then divides by 0.706 to estimate total AI sessions, since only about 29% arrive with the referrer intact."),
   ("Where do the 10.21% and 2.46% rates come from?","Published 2026 measurement: Dark AI sessions convert at roughly 10.21%, a 4.1x premium over the 2.46% baseline for genuine direct traffic. Your own rates will differ, so treat the output as a direction. If you can measure your visible AI-referral conversion rate, substitute it for a tighter estimate."),
   ("Why is this a model and not a measurement?","Because the referrer is genuinely gone, so you cannot observe these sessions directly. The estimate assumes your conversion rates match the published benchmarks and that the Direct bucket is only dark AI plus genuine direct. Label it as an estimate in any deck, and reduce the guesswork by tagging every URL you place and cohorting Direct traffic by landing page, since dark AI lands on deep informational pages, not the homepage."),
   ("Does my data leave the browser?","No. The decomposition runs entirely in your browser. Nothing you enter is uploaded, stored or sent to any server.")],
  REL+[("Zero-Click Traffic Risk Estimator","/tools/zero-click-traffic-risk")])
t2_script=r'''<script>
(function(){
  var root=document.getElementById('dai'); if(!root) return;
  var PHI=0.706, C_DARK=0.1021, C_BASE=0.0246;
  function num(id){var v=parseFloat((document.getElementById(id).value||'').replace(/[,$\s]/g,''));return isNaN(v)?null:v;}
  function money(x){return '$'+Math.round(x).toLocaleString();}
  function compute(){
    var sess=num('daiSess'), conv=num('daiConv'), acv=num('daiAcv');
    var rev=document.getElementById('daiRev'),band=document.getElementById('daiBand'),fill=document.getElementById('daiFill'),note=document.getElementById('daiNote');
    if(sess===null||conv===null||acv===null||sess<=0){rev.textContent='$0';band.textContent='Enter your Direct numbers';band.style.background='rgba(255,255,255,.1)';band.style.color='#fff';fill.style.width='0%';note.innerHTML='<p class="hint">The decomposition appears here.</p>';return;}
    var dark=(conv - sess*C_BASE)/(C_DARK - C_BASE);
    dark=Math.max(0,Math.min(dark,sess));
    var totalAi=dark/PHI, hiddenConv=dark*C_DARK, hiddenRev=hiddenConv*acv, share=dark/sess;
    var blendRate=conv/sess;
    rev.textContent=money(hiddenRev);
    fill.style.width=Math.min(share*100,100)+'%';
    var lbl,col; if(share>=0.35){lbl='Large hidden channel';col='var(--signal)';}else if(share>=0.12){lbl='Material, investigate';col='#C9922E';}else{lbl='Small or none';col='var(--up)';}
    band.textContent=lbl;band.style.background=col;band.style.color='#0b0b0c';fill.style.background=col;
    note.innerHTML='<div class="lt-stat"><span>Blended Direct conversion</span><strong>'+(blendRate*100).toFixed(2)+'%</strong></div>'
      +'<div class="lt-stat"><span>Implied dark-AI sessions</span><strong style="color:'+col+'">'+Math.round(dark).toLocaleString()+'</strong></div>'
      +'<div class="lt-stat"><span>Dark share of Direct</span><strong>'+(share*100).toFixed(1)+'%</strong></div>'
      +'<div class="lt-stat"><span>Implied total AI sessions</span><strong>'+Math.round(totalAi).toLocaleString()+'</strong></div>'
      +'<div class="lt-stat"><span>Hidden conversions / mo</span><strong>'+Math.round(hiddenConv).toLocaleString()+'</strong></div>'
      +'<div class="lt-stat"><span>Hidden revenue / mo</span><strong style="color:var(--up)">'+money(hiddenRev)+'</strong></div>'
      +'<p class="hint" style="margin-top:8px">A model, not a measurement. Confirm by tagging placed URLs and cohorting Direct by landing page.</p>';
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

TOOLS=[
 ("citable-stat-density-scorer",
  "Citable Stat Density Scorer &middot; Free Tool &middot; rawmktg.",
  "Paste a research draft and score each claim as citable, weak or rewrite, then get the citable stat density per 1,000 words a research hub needs.",
  "Content &amp; Authority &middot; Analyzer","Citable Stat Density Scorer",
  "A model lifts stat units, not studies. Paste your draft to score each claim on number, method and attribution, and get the citable density a research hub should clear.",
  t1_body,t1_method,t1_script,
  [("What is a good citable stat density?","Clear 4 extractable units per 1,000 words for a research hub. A general blog post scores under 1, and below 2 the document reads as narrative with numbers rather than liftable facts. Every WEAK or REWRITE line is a finding a model cannot confidently quote."),
   ("How is each line scored?","Plus 2 for a precise number, plus 2 for a named method (n=, sample, margin of error), plus 2 for attribution (said, according to, per), minus 1 for a hedge (most, many, significant), and plus 1 if the line is 45 words or fewer. Five or more is citable, three to four is weak, below three needs a rewrite."),
   ("Why do hedge words lower the score?","Because a model cannot repeat most teams or a significant share as a fact. Retrieval weights precise verifiable claims and discounts qualitative filler, so a hedge is a missed stat unit. Replace it with the number it stands in for and add the methodology that makes the number trustworthy."),
   ("Does my draft leave the browser?","No. Every line is scored entirely in your browser with simple pattern matching. Nothing you paste is uploaded, stored or sent to any server.")]),
 ("dark-ai-revenue-estimator",
  "Dark AI Revenue Estimator &middot; Free Tool &middot; rawmktg.",
  "Estimate the high-intent AI traffic hiding in your GA4 Direct bucket. Enter Direct sessions, conversions and ACV to back out dark-AI sessions and hidden revenue.",
  "Ranking Signals &middot; Estimator","Dark AI Revenue Estimator",
  "About 70.6% of AI referrals land in Direct with the referrer stripped, converting at 4x baseline. Enter three GA4 numbers to back out the hidden sessions and revenue.",
  t2_body,t2_method,t2_script,
  [("How does it separate dark AI from genuine direct?","It solves one equation: total Direct conversions equal dark-AI sessions at a 10.21% rate plus genuine-direct sessions at 2.46%. Given the totals, only one split fits, yielding the implied dark-AI session count. It then divides by 0.706 to estimate total AI sessions, since only about 29% arrive with the referrer intact."),
   ("Where do the 10.21% and 2.46% rates come from?","Published 2026 measurement: Dark AI sessions convert at roughly 10.21%, a 4.1x premium over the 2.46% baseline for genuine direct traffic. Your own rates will differ, so treat the output as a direction. If you can measure your visible AI-referral conversion rate, substitute it for a tighter estimate."),
   ("Why is this a model and not a measurement?","Because the referrer is genuinely gone, so you cannot observe these sessions directly. It assumes your rates match the benchmarks and that Direct is only dark AI plus genuine direct. Label it as an estimate, and reduce the guesswork by tagging placed URLs and cohorting Direct by landing page, since dark AI lands on deep informational pages."),
   ("Does my data leave the browser?","No. The decomposition runs entirely in your browser. Nothing you enter is uploaded, stored or sent to any server.")]),
]
built=[]
for t in TOOLS:
    html=page(*t); built.append((t[0],html))

for slug,html in built:
    ms=re.findall(r'<script>(?!window\.dataLayer).*?</script>', html, re.S)
    logic=[s for s in ms if 'getElementById' in s]
    ok="n/a"
    if logic:
        open("/tmp/pt.js","w").write(logic[-1][8:-9])
        r=subprocess.run(["node","--check","/tmp/pt.js"],capture_output=True,text=True)
        ok="OK" if r.returncode==0 else "FAIL "+r.stderr[:300]
    hc=html.split('</head>')[0]
    jc=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hc,re.S) if (json.loads(b) or True))
    amp="BAD" if "&amp;middot;" in html.split('</head>')[1] else "clean"
    dash="DASH" if ("—" in html or "–" in html) else "clean"
    print(f"{slug:32} node:{ok:6} jsonld:{jc} h1:{html.count('<h1')} faq:{'FAQPage' in html} dash:{dash}")
