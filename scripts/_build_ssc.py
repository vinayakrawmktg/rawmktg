#!/usr/bin/env python3
"""SCRATCH: build /tools/sample-size-confidence-planner. Do NOT commit as content."""
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

BODY=('<section class="card" id="ssc">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Plan the sample</div>'
  '<div class="num-grid">'
  '<div class="fld"><div class="lab">Expected inclusion rate (%)</div><input class="tin" id="sscP" inputmode="decimal" value="27"></div>'
  '<div class="fld"><div class="lab">Target margin of error (&plusmn; points)</div><input class="tin" id="sscE" inputmode="decimal" value="2"></div>'
  '<div class="fld"><div class="lab">Confidence (90 / 95 / 99)</div><input class="tin" id="sscZ" inputmode="numeric" value="95"></div>'
  '<div class="fld"><div class="lab">Runs per prompt per engine</div><input class="tin" id="sscR" inputmode="numeric" value="10"></div>'
  '</div>'
  '<p class="hint" style="margin:8px 0 0">n = z&sup2; &middot; p(1-p) / E&sup2;. Runs convert observations into a prompt count. Engines that re-retrieve on every call (Perplexity, Google AI Overviews) need the top of the 8-12 run range.</p></div>\n'
  '      <div class="cat"><div class="cat-h">Bound an observed rate (Wilson)</div>'
  '<div class="num-grid">'
  '<div class="fld"><div class="lab">Times the brand appeared</div><input class="tin" id="sscK" inputmode="numeric" value="54"></div>'
  '<div class="fld"><div class="lab">Total scored responses</div><input class="tin" id="sscN" inputmode="numeric" value="200"></div>'
  '</div>'
  '<p class="hint" style="margin:8px 0 0">The Wilson score interval is correct at the low rates most brands actually have, where the normal approximation breaks badly.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Observations needed</div>\n'
  '      <div class="scorewrap"><span class="score" id="sscN2">0</span><span class="score-d">obs</span></div>\n'
  '      <span class="scoreband" id="sscBand" style="background:rgba(255,255,255,.1);color:#fff">per brand, per engine</span>\n'
  '      <div class="gaps"><div class="gaps-h">The plan</div><div id="sscPlan"><p class="hint">Your prompt count appears here.</p></div></div>\n'
  '      <div style="margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,.08)">\n'
  '        <div class="o-eyebrow">Wilson 95% interval</div>\n'
  '        <div class="scorewrap"><span class="score" id="sscCI" style="font-size:34px">&ndash;</span></div>\n'
  '        <div id="sscCInote"><p class="hint">Enter appearances and total responses to bound the rate.</p></div>\n'
  '      </div>\n    </div>\n  </div>\n</section>')

METHOD=method(
 "Sample size is the part everyone skips",
 "Running each prompt once and reporting the result as a rate is not a measurement, it is a coin flip recorded as a fact. Language models are probabilistic: the same prompt, sent twice, returns a different brand set. This planner does the two calculations that make a Share of Model number trustworthy, how many observations you need for a target precision, and how wide the confidence interval is on a rate you already measured.",
 ["Enter your expected inclusion rate, the margin of error you want to hold, your confidence level and how many times you run each prompt.",
  "Read the observations needed and the prompt count, then round to a 250 to 500 prompt portfolio.",
  "For a rate you already measured, enter appearances and total responses to get the Wilson interval.",
  "Report the number with the interval attached, never a bare point estimate."],
 [("How many runs per prompt do I need?","Eight to twelve per prompt per engine, minimum. At one run your estimate is either 0% or 100%; at three runs it can still be off by 30 points. The estimate only settles into an actionable range around eight to twelve runs, and high live-retrieval engines like Perplexity and Google AI Overviews need the top of that range."),
  ("How many prompts make a decision-grade portfolio?","To hold a two-point margin at a 27% rate you need roughly 1,900 scored observations per brand per engine, about 190 prompts at ten runs. Decision-grade programmes land at a 250 to 500 prompt portfolio. Precision flattens hard after about 2,500 observations, so more engines usually beats more prompts on a tight budget."),
  ("Why the Wilson interval instead of the normal approximation?","Because the normal (Wald) approximation breaks badly at the low inclusion rates most brands actually have, producing intervals that can dip below zero or overstate precision. The Wilson score interval stays correct at small n and extreme p, which is exactly the regime AI-visibility measurement lives in."),
  ("Does my data leave the browser?","No. Every calculation runs entirely in your browser. Nothing you enter is uploaded, stored or sent to any server.")],
 [("Share of Model, measured properly","/blogs/share-of-model-measurement"),("Platform-Weighted Visibility & Share of Model Calculator","/tools/platform-weighted-visibility-calculator"),("Prompt-to-citation tracking","/blogs/prompt-to-citation-tracking")])

SCRIPT=r'''<script>
(function(){
  var root=document.getElementById('ssc'); if(!root) return;
  function num(id){var el=document.getElementById(id); if(!el) return null; var v=parseFloat(el.value); return isNaN(v)?null:v;}
  function zfor(c){ if(c>=99) return 2.576; if(c>=95) return 1.96; if(c>=90) return 1.645; return 1.96; }
  function compute(){
    var p=num('sscP'), E=num('sscE'), C=num('sscZ'), R=num('sscR');
    var n2=document.getElementById('sscN2'),band=document.getElementById('sscBand'),plan=document.getElementById('sscPlan');
    if(p===null||E===null||E<=0||C===null||R===null||R<=0){
      n2.textContent='0';band.textContent='per brand, per engine';plan.innerHTML='<p class="hint">Your prompt count appears here.</p>';
    } else {
      var pr=Math.min(Math.max(p,0),100)/100, Er=E/100, z=zfor(C);
      var n=z*z*pr*(1-pr)/(Er*Er);
      var prompts=Math.ceil(n/R);
      n2.textContent=Math.round(n).toLocaleString();
      band.textContent='at '+z.toFixed(3)+' z';band.style.background='rgba(255,255,255,.1)';band.style.color='#fff';
      var port = prompts<=250?'250': (prompts<=500?'250-500':'500+');
      plan.innerHTML='<div class="lt-stat"><span>Prompts at '+R+' runs/engine</span><strong>&asymp; '+prompts.toLocaleString()+'</strong></div>'
        +'<div class="lt-stat"><span>Round to a portfolio of</span><strong>'+port+'</strong></div>'
        +'<p class="hint" style="margin-top:8px">Precision flattens after ~2,500 observations. Past that, spend on more engines, not more prompts.</p>';
    }
    var k=num('sscK'), N=num('sscN');
    var ci=document.getElementById('sscCI'),note=document.getElementById('sscCInote');
    if(k===null||N===null||N<=0||k<0||k>N){
      ci.textContent='–';note.innerHTML='<p class="hint">Enter appearances and total responses to bound the rate.</p>';
    } else {
      var z=1.96, ph=k/N, den=1+z*z/N;
      var centre=(ph+z*z/(2*N))/den;
      var margin=z*Math.sqrt(ph*(1-ph)/N + z*z/(4*N*N))/den;
      var lo=Math.max(0,(centre-margin))*100, hi=Math.min(1,(centre+margin))*100;
      ci.textContent=lo.toFixed(1)+'–'+hi.toFixed(1)+'%';
      note.innerHTML='<div class="lt-stat"><span>Point estimate</span><strong>'+(ph*100).toFixed(1)+'%</strong></div>'
        +'<div class="lt-stat"><span>95% interval width</span><strong>&plusmn;'+((hi-lo)/2).toFixed(1)+' pts</strong></div>'
        +'<p class="hint" style="margin-top:8px">Report the interval, not the point. A wide interval means you have not run enough.</p>';
    }
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

FAQS=[("How many runs per prompt do I need?","Eight to twelve per prompt per engine, minimum. At one run your estimate is either 0% or 100%; at three runs it can still be off by 30 points. The estimate only settles into an actionable range around eight to twelve runs, and high live-retrieval engines like Perplexity and Google AI Overviews need the top of that range."),
 ("How many prompts make a decision-grade portfolio?","To hold a two-point margin at a 27% rate you need roughly 1,900 scored observations per brand per engine, about 190 prompts at ten runs. Decision-grade programmes land at a 250 to 500 prompt portfolio. Precision flattens hard after about 2,500 observations, so more engines usually beats more prompts on a tight budget."),
 ("Why the Wilson interval instead of the normal approximation?","Because the normal (Wald) approximation breaks badly at the low inclusion rates most brands actually have, producing intervals that can dip below zero or overstate precision. The Wilson score interval stays correct at small n and extreme p, which is exactly the regime AI-visibility measurement lives in."),
 ("Does my data leave the browser?","No. Every calculation runs entirely in your browser. Nothing you enter is uploaded, stored or sent to any server.")]

html=page("sample-size-confidence-planner",
  "Sample-Size & Confidence Planner · Free Tool · rawmktg.",
  "Plan a decision-grade AI-visibility sample: the observations and prompt count needed for a target margin of error, plus a Wilson confidence interval for any inclusion rate you have measured.",
  "Ranking & Measurement · Calculator","Sample-Size & Confidence Planner",
  "One run is a coin flip recorded as a fact. Compute the observations and prompts you need for a target margin, and put a Wilson confidence interval on any rate you have already measured.",
  BODY,METHOD,SCRIPT,FAQS)

ms=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', html, re.S) if "getElementById('ssc')" in s]
open("/tmp/ssc.js","w").write(ms[-1][8:-9])
r=subprocess.run(["node","--check","/tmp/ssc.js"],capture_output=True,text=True)
jc=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if (json.loads(b) or True))
print("NODE:", "OK" if r.returncode==0 else "FAIL "+r.stderr[:400], "| jsonld:",jc,"| h1:",html.count('<h1'),"| faq:",'FAQPage' in html,"| amp-middot:", '&amp;middot;' in html)
