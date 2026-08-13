#!/usr/bin/env python3
"""SCRATCH: build 3 query-fan-out tool pages under /tools. Do NOT commit as content."""
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
ADSENSE=''  # AdSense removed: no ad units, hurts TBT
def esc(t): return H.escape(t,quote=False)
def escq(t): return H.escape(t,quote=True)

def page(slug,title,desc,eyebrow,headline,deck,body,method,script):
    URL=f"https://rawmktg.com/tools/{slug}"
    schema=[
      {"@context":"https://schema.org","@type":"WebApplication","name":headline,"url":URL,"description":desc,"applicationCategory":"BusinessApplication","operatingSystem":"Web, all browsers","browserRequirements":"Requires JavaScript","isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"}},
      {"@context":"https://schema.org","@type":"WebPage","name":headline,"url":URL,"description":desc,"isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://rawmktg.com/tools"},{"@type":"ListItem","position":3,"name":headline,"item":URL}]},
      {"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]},
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

FACETS=[("Specification","the core features and what it actually does"),
        ("Compatibility","integrations, platforms and what it works with"),
        ("Compliance","security, certifications and regulatory fit"),
        ("Capability","specific workflows and how deep the automation goes"),
        ("Price","plans, tiers and total cost, in server-side HTML"),
        ("Comparison","head-to-head vs named competitors and alternatives"),
        ("Sentiment","real reviews and community proof (off your domain)"),
        ("Edge case","the awkward constraint a buyer asks about last")]

# ============ TOOL 1: FACET COVERAGE AUDITOR ============
rows=""
for i,(name,desc) in enumerate(FACETS):
    rows+=(f'<div class="q"><div class="q-t"><strong>{name}.</strong> {desc}</div>'
      f'<div class="iseg" data-f="{i}"><button data-v="yes">Covered in &lt;100 words</button><button data-v="no">Missing / buried</button></div></div>')
t1_body=('<section class="card" id="fca">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Your topic or head term</div>'
  '<div class="fld"><input class="tin" id="fcaTopic" placeholder="e.g. field service management software"></div>'
  '<p class="hint" style="margin:8px 0 14px">For each of the eight facets a fan-out targets, mark whether a single passage on your site answers it in under a hundred words. Buried in paragraph four does not count, the chunker does not read ahead.</p>'
  +rows+'</div>\n    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Facet coverage</div>\n'
  '      <div class="scorewrap"><span class="score" id="fcaScore">0</span><span class="score-d">/8</span></div>\n'
  '      <span class="scoreband" id="fcaBand" style="background:rgba(255,255,255,.1);color:#fff">Mark the facets</span>\n'
  '      <div class="gauge"><div class="gfill" id="fcaFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">Briefs to write next</div><div id="fcaGaps"></div></div>\n'
  '    </div>\n  </div>\n</section>')
t1_method=('<section class="method"><h2>Why facet coverage, not keywords</h2>'
  '<p>AI search decomposes one prompt into eight to sixteen hidden sub-queries, each aimed at a different facet, and a page is evaluated once per sub-query. Ranking #1 for the head term buys a 13% edge inside one list; appearing at all in a second facet buys close to 100%. So the prioritisation metric is no longer search volume, it is how many facets you answer better than anyone.</p>'
  '<p>The eight-facet frame reproduces most commercial fan-outs. Score honestly: a facet only counts if a self-contained passage answers it in under a hundred words, in server-side HTML.</p>'
  '<div class="srcs"><a href="/blogs/query-fan-out-how-one-prompt-becomes-ten-searches">Query fan-out explained &rarr;</a><a href="/tools/query-fan-out-simulator">Query Fan-Out Simulator &rarr;</a></div></section>')
t1_script=r'''<script>
(function(){
  var root=document.getElementById('fca'); if(!root) return;
  var NAMES=['Specification','Compatibility','Compliance','Capability','Price','Comparison','Sentiment','Edge case'];
  var CORP=['product & feature pages','docs & app exchanges','trust centre & security page','product guides','pricing page (server-side)','comparison & alternatives pages','Reddit, G2, community','FAQ & knowledge base'];
  var state={};
  function compute(){
    var covered=0, gaps=[];
    for(var i=0;i<8;i++){ if(state[i]==='yes') covered++; else if(state[i]==='no') gaps.push(i); }
    var answered=Object.keys(state).length;
    var pct=covered/8*100;
    var sEl=document.getElementById('fcaScore'),bEl=document.getElementById('fcaBand'),fill=document.getElementById('fcaFill'),g=document.getElementById('fcaGaps');
    sEl.textContent=covered; fill.style.width=pct+'%';
    if(answered<8){bEl.textContent='Mark the facets ('+answered+'/8)';bEl.style.background='rgba(255,255,255,.1)';bEl.style.color='#fff';}
    else{var lbl,col; if(covered>=7){lbl='Strong coverage';col='var(--up)';}else if(covered>=4){lbl='Building';col='#C9922E';}else{lbl='At risk';col='var(--signal)';}
      bEl.textContent=lbl;bEl.style.background=col;bEl.style.color='#0b0b0c';fill.style.background=col;}
    if(gaps.length){ g.innerHTML=gaps.map(function(i){return '<div class="lt-stat"><span><strong style="color:#fff">'+NAMES[i]+'</strong> <span style="color:rgba(255,255,255,.4)">'+CORP[i]+'</span></span><strong style="color:var(--signal)">write it</strong></div>';}).join(''); }
    else if(answered===8){ g.innerHTML='<p class="hint">Full coverage. Now make each passage monosemantic and served in plain HTML.</p>'; }
    else { g.innerHTML='<p class="hint">Missing facets appear here as briefs.</p>'; }
  }
  root.querySelectorAll('.iseg').forEach(function(seg){
    var f=seg.getAttribute('data-f');
    seg.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        seg.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
        b.classList.add('on'); state[f]=b.getAttribute('data-v'); compute();
      });
    });
  });
  compute();
})();
</script>'''

# ============ TOOL 2: EXPECTED-CITATION ESTIMATOR ============
t2_body=('<section class="card" id="ece">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Your topic\'s fan-out</div>'
  '<div class="num-grid">'
  '<div class="fld"><div class="lab">Facets in the fan-out</div><input class="tin" id="eceTotal" inputmode="numeric" value="8"></div>'
  '<div class="fld"><div class="lab">Facets you cover</div><input class="tin" id="eceCov" inputmode="numeric" value="5"></div>'
  '<div class="fld"><div class="lab">Avg selection strength (0-1)</div><input class="tin" id="eceSel" inputmode="decimal" value="0.4"></div>'
  '</div>'
  '<p class="hint" style="margin:10px 0 0">Retrieval probability is a coverage problem (do you have a passage that can win facet i at all). Selection strength is a quality and authority problem (given you were retrieved, does your audition chunk beat the others). Expected citation = the average of retrieval x selection across the fan-out.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Expected citation rate</div>\n'
  '      <div class="scorewrap"><span class="score" id="eceScore">0</span><span class="score-d">%</span></div>\n'
  '      <span class="scoreband" id="eceBand" style="background:rgba(255,255,255,.1);color:#fff">Enter your fan-out</span>\n'
  '      <div class="gauge"><div class="gfill" id="eceFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">Where the lift is</div><div id="eceNote"><p class="hint">Your estimate updates as you type.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t2_method=('<section class="method"><h2>The formula that replaces rank tracking</h2>'
  '<p>Rank tracking answers a question the engine no longer asks. Expected citation decomposes into two probabilities you can influence: retrieval (coverage) and selection (quality plus authority). Most teams spent a decade optimising selection for a handful of queries while leaving retrieval at zero for most of the fan-out. This estimator shows why covering one more facet usually beats polishing an existing one.</p>'
  '<div class="srcs"><a href="/blogs/query-fan-out-how-one-prompt-becomes-ten-searches">Query fan-out explained &rarr;</a><a href="/tools/platform-weighted-visibility-calculator">Measure actual citations &rarr;</a></div></section>')
t2_script=r'''<script>
(function(){
  var root=document.getElementById('ece'); if(!root) return;
  function n(id){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?null:v;}
  function compute(){
    var total=n('eceTotal'),cov=n('eceCov'),sel=n('eceSel');
    var sEl=document.getElementById('eceScore'),bEl=document.getElementById('eceBand'),fill=document.getElementById('eceFill'),note=document.getElementById('eceNote');
    if(total===null||total<=0||cov===null||sel===null){sEl.textContent='0';bEl.textContent='Enter your fan-out';bEl.style.background='rgba(255,255,255,.1)';bEl.style.color='#fff';fill.style.width='0%';note.innerHTML='<p class="hint">Your estimate updates as you type.</p>';return;}
    cov=Math.max(0,Math.min(cov,total)); sel=Math.max(0,Math.min(sel,1));
    var e=(cov/total)*sel*100;                      // E[cited] across the fan-out
    sEl.textContent=e.toFixed(1); fill.style.width=Math.min(100,e)+'%';
    var lbl,col; if(e>=40){lbl='Strong';col='var(--up)';}else if(e>=20){lbl='Building';col='#C9922E';}else{lbl='At risk';col='var(--signal)';}
    bEl.textContent=lbl;bEl.style.background=col;bEl.style.color='#0b0b0c';fill.style.background=col;
    var msgs=[];
    if(cov<total){
      var e2=((cov+1)/total)*sel*100;
      msgs.push('Cover 1 more facet: '+e.toFixed(1)+'% &rarr; <strong style="color:var(--up)">'+e2.toFixed(1)+'%</strong> (+'+(e2-e).toFixed(1)+' pts).');
    }
    var eSel=(cov/total)*Math.min(1,sel+0.1)*100;
    msgs.push('Raise selection by 0.1 (better audition chunk): +'+(eSel-e).toFixed(1)+' pts.');
    if(cov<total) msgs.push('Coverage is usually the cheaper lever: '+(total-cov)+' facet'+((total-cov)===1?'':'s')+' are currently at zero retrieval.');
    note.innerHTML=msgs.map(function(m){return '<div class="lt-stat"><span>'+m+'</span></div>';}).join('');
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

# ============ TOOL 3: FAN-OUT CONTENT BRIEF GENERATOR ============
t3_body=('<section class="card" id="fbg">\n  <div class="grid calc">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Your head term</div>'
  '<div class="fld"><input class="tin" id="fbgTerm" placeholder="e.g. field service management software"></div>'
  '<div class="fld"><div class="lab">A named competitor (optional)</div><input class="tin" id="fbgComp" placeholder="e.g. ServiceTitan"></div>'
  '<p class="hint" style="margin:8px 0 0">Enter a head term and get an eight-facet brief: one question-style H2 per facet, plus the corpus each sub-query targets. Answer each in the first forty words, in server-side HTML.</p></div>\n'
  '    </div>\n'
  '    <div class="output">\n      <div class="o-eyebrow">Your fan-out brief</div>\n'
  '      <div class="btn-row"><button class="tbtn primary" id="fbgCopy" type="button">Copy</button><button class="tbtn" id="fbgDl" type="button">Download .md</button></div>\n'
  '      <pre class="codeout" id="fbgOut" style="margin-top:12px;white-space:pre-wrap">Enter a head term to generate the brief.</pre>\n'
  '    </div>\n  </div>\n</section>')
t3_method=('<section class="method"><h2>From head term to eight briefs</h2>'
  '<p>Five focused pages produce five audition chunks, five title tags and five shots at the fusion pool, where one monster guide produces one of each. This generator turns a head term into the eight facet questions a fan-out will ask, so you can ship a cluster instead of a hero page. Rewrite each as an H2 and answer it in the first forty words.</p>'
  '<div class="srcs"><a href="/blogs/query-fan-out-how-one-prompt-becomes-ten-searches">Query fan-out explained &rarr;</a><a href="/tools/facet-coverage-auditor">Audit your facet coverage &rarr;</a></div></section>')
t3_script=r'''<script>
(function(){
  var root=document.getElementById('fbg'); if(!root) return;
  var FRAME=[
    ['Specification','What are the core features of {T}, and who is it for?','product & feature pages'],
    ['Compatibility','What does {T} integrate with (CRM, accounting, mobile)?','docs & app exchanges'],
    ['Compliance','Is {T} SOC 2, HIPAA or GDPR compliant, and on which tiers?','trust centre & security page'],
    ['Capability','Does {T} support [your key workflow] end to end?','product guides'],
    ['Price','How much does {T} cost, by plan and per user?','pricing page, server-side HTML'],
    ['Comparison','{T} vs {C}: which is better for [segment]?','comparison & alternatives pages'],
    ['Sentiment','Is {T} any good? What do real users say?','Reddit, G2, Capterra, forums'],
    ['Edge case','Does {T} work for [the awkward constraint buyers ask last]?','FAQ & knowledge base']
  ];
  function build(){
    var term=(document.getElementById('fbgTerm').value||'').trim();
    var comp=(document.getElementById('fbgComp').value||'').trim()||'[competitor]';
    var out=document.getElementById('fbgOut');
    if(!term){out.textContent='Enter a head term to generate the brief.';return;}
    var lines=['# Fan-out content brief: '+term,'# Eight facets, one focused page (or section) each. Answer in the first 40 words.',''];
    FRAME.forEach(function(f,i){
      var q=f[1].replace(/\{T\}/g,term).replace(/\{C\}/g,comp);
      lines.push((i+1)+'. '+f[0]);
      lines.push('   H2: '+q);
      lines.push('   Target corpus: '+f[2]);
      lines.push('');
    });
    lines.push('Rule: one self-contained answer per H2, in server-side HTML, plus JSON-LD for the machine-readable facts.');
    out.textContent=lines.join('\n');
  }
  ['fbgTerm','fbgComp'].forEach(function(id){document.getElementById(id).addEventListener('input',build);});
  document.getElementById('fbgCopy').addEventListener('click',function(){
    var b=this,t=document.getElementById('fbgOut').textContent;
    function done(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,done);}else{done();}
  });
  document.getElementById('fbgDl').addEventListener('click',function(){
    var t=document.getElementById('fbgOut').textContent, term=(document.getElementById('fbgTerm').value||'brief').trim().replace(/[^a-z0-9]+/gi,'-').toLowerCase();
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([t],{type:'text/markdown'})); a.download='fanout-brief-'+term+'.md'; a.click();
  });
  build();
})();
</script>'''

TOOLS=[
 ("facet-coverage-auditor",
  "Facet Coverage Auditor · Free Tool · rawmktg.",
  "Audit your content against the eight facets a query fan-out targets, specification, compatibility, compliance, capability, price, comparison, sentiment, edge case, and get a ranked list of the briefs you are missing.",
  "Query Fan-Out · Diagnostic","Facet Coverage Auditor",
  "AI search decomposes one prompt into eight to sixteen hidden sub-queries, each aimed at a facet. Mark which facets your content answers in under a hundred words and see your coverage score and the briefs to write next.",
  t1_body,t1_method,t1_script),
 ("expected-citation-estimator",
  "Expected-Citation Estimator · Free Tool · rawmktg.",
  "Estimate your expected AI-citation rate from facet coverage and selection strength, the measurement that replaces rank tracking under query fan-out.",
  "Query Fan-Out · Calculator","Expected-Citation Estimator",
  "Rank tracking answers a question the engine no longer asks. Enter your facet count, coverage and selection strength to estimate expected citations, and see why covering one more facet usually beats polishing an existing page.",
  t2_body,t2_method,t2_script),
 ("fan-out-content-brief-generator",
  "Fan-Out Content Brief Generator · Free Tool · rawmktg.",
  "Turn a head term into an eight-facet content brief: one question-style H2 per facet plus the corpus each sub-query targets. Copy or download.",
  "Query Fan-Out · Generator","Fan-Out Content Brief Generator",
  "Five focused pages beat one monster guide, because each produces its own audition chunk and title tag. Enter a head term and get the eight facet questions a fan-out will ask, as a ready-to-write brief.",
  t3_body,t3_method,t3_script),
]
built=[]
for t in TOOLS:
    html=page(*t); built.append((t[0],html))

import json as J
for slug,html in built:
    ms=re.findall(r'<script>(?!window\.dataLayer).*?</script>', html, re.S)
    logic=[s for s in ms if 'getElementById' in s]
    ok="n/a"
    if logic:
        open("/tmp/ft.js","w").write(logic[-1][8:-9])
        r=subprocess.run(["node","--check","/tmp/ft.js"],capture_output=True,text=True)
        ok="OK" if r.returncode==0 else "FAIL "+r.stderr[:300]
    jc=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if (J.loads(b) or True))
    amp="BAD &amp;middot;" if "&amp;middot;" in html else "clean"
    print(f"{slug:36} node:{ok:6} jsonld:{jc} title:{amp} h1:{html.count('<h1')}")
