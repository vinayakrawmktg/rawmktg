#!/usr/bin/env python3
"""SCRATCH: build 4 measurement-taxonomy tool pages under /tools. Do NOT commit as content."""
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

# ============ TOOL 1: SIGNAL DIAGNOSTIC ============
d1_body='''<section class="card" id="sd">
  <div class="grid score">
    <div class="controls">
      <div class="cat">
        <div class="cat-h">Answer three questions about one prompt set</div>
        <div class="q"><div class="q-t">1. On prompts where the engine does <strong>not</strong> search the live web, does your brand get named?</div>
          <div class="iseg" data-q="q1"><button data-v="yes">Yes, it appears</button><button data-v="no">No, absent</button></div></div>
        <div class="q"><div class="q-t">2. When your brand <strong>does</strong> appear in an answer, does your URL show up in the cited sources?</div>
          <div class="iseg" data-q="q2"><button data-v="yes">Yes, cited</button><button data-v="no">Never cited</button></div></div>
        <div class="q"><div class="q-t">3. When you are cited, are you the recommended pick, or does a competitor get named?</div>
          <div class="iseg" data-q="q3"><button data-v="yes">We are the pick</button><button data-v="no">Competitor wins</button></div></div>
      </div>
    </div>
    <div class="panel-out">
      <div class="o-eyebrow">Broken signal</div>
      <div class="scorewrap"><span class="score" id="sdSignal" style="font-size:30px;line-height:1.15">--</span></div>
      <span class="scoreband" id="sdLayer" style="background:rgba(255,255,255,.1);color:#fff">Answer the three checks</span>
      <div class="gaps"><div class="gaps-h">What to fix first</div><div id="sdFix"><p class="hint">Your result and the specific fix appear here.</p></div></div>
    </div>
  </div>
</section>'''
d1_method=('<section class="method"><h2>How the diagnostic works</h2>'
  '<p>AI visibility fails in three different places, and each has a different fix. This tool implements the diagnostic from the article: it reads your symptoms top-down and isolates the first broken signal, because a mention problem upstream masks everything below it.</p>'
  '<p><strong>Mention (parametric memory)</strong> is whether the model knows you exist at all, tested on prompts with no live search. <strong>Citation (retrieval)</strong> is whether your page gets selected as evidence. <strong>Recommendation (synthesis)</strong> is whether you get named as the pick. Fix them in that order.</p>'
  '<div class="srcs"><a href="/blogs/citation-vs-mention-vs-recommendation">Citation vs Mention vs Recommendation &rarr;</a><a href="/blogs/how-your-page-gets-retrieved">How your page gets retrieved &rarr;</a></div></section>')
d1_script=r'''<script>
(function(){
  var root=document.getElementById('sd'); if(!root) return;
  var ans={q1:null,q2:null,q3:null};
  var RESULT={
    mention:{sig:'Mention',layer:'Parametric memory · off-page & slow',
      fix:'The model does not reliably know you exist. This lives in the frozen weights, so the fix is off-page and slow: earn co-citation alongside category leaders, pursue comparison listicles, communities and reference sites, and build entity prominence. On-page work will not move it.',
      links:[['Off-page entity PR: authority seeding','/blogs/authority-seeding-ai-llm-trust'],['Becoming an entity','/blogs/becoming-an-entity']]},
    citation:{sig:'Citation',layer:'Retrieval · on-page & fast',
      fix:'You are known but your page is not being selected as evidence. This is the fastest fix: lead every section with a self-contained ~40-word answer, add precise statistics and named sources, and mark up entities with schema so a re-ranker can extract you cleanly.',
      links:[['Anatomy of a high-citation page','/blogs/anatomy-of-a-high-citation-page'],['Schema markup for AI citations','/blogs/schema-markup-ai-citations-2026']]},
    recommendation:{sig:'Recommendation',layer:'Synthesis · comparison & sentiment',
      fix:'You are cited as a source but a competitor gets named as the pick. The gap is at synthesis: get into the comparison roundups the engines cite for your category, fix negative or missing sentiment, and build share of voice against the named competitor set.',
      links:[['When the buyer is a bot','/blogs/when-the-buyer-is-a-bot'],['Why engines recommend different vendors','/blogs/why-engines-recommend-different-vendors']]},
    healthy:{sig:'All three healthy',layer:'Maintain & re-baseline',
      fix:'On this prompt set, all three signals are working: the model knows you, cites you, and picks you. Keep a fixed prompt set, re-measure every 30 days across engines, and watch for drift, nothing improves on its own and citations decay.',
      links:[['Prompt-to-citation tracking','/blogs/prompt-to-citation-tracking'],['The 30-day content half-life','/blogs/30-day-content-half-life-recency-ai-ranking-signal']]}
  };
  function pick(){
    if(ans.q1===null) return null;
    if(ans.q1==='no') return 'mention';
    if(ans.q2===null) return null;
    if(ans.q2==='no') return 'citation';
    if(ans.q3===null) return null;
    if(ans.q3==='no') return 'recommendation';
    return 'healthy';
  }
  function band(key){
    var c={mention:'var(--signal)',citation:'#C9922E',recommendation:'#C9922E',healthy:'var(--up)'}[key];
    return c;
  }
  function render(){
    var k=pick();
    var sigEl=document.getElementById('sdSignal'),layEl=document.getElementById('sdLayer'),fixEl=document.getElementById('sdFix');
    if(!k){sigEl.textContent='--';layEl.textContent='Answer the three checks';layEl.style.background='rgba(255,255,255,.1)';layEl.style.color='#fff';
      fixEl.innerHTML='<p class="hint">Your result and the specific fix appear here.</p>';return;}
    var r=RESULT[k],c=band(k);
    sigEl.textContent=r.sig; sigEl.style.color=c;
    layEl.textContent=r.layer; layEl.style.background=c; layEl.style.color='#0b0b0c';
    var ls=r.links.map(function(x){return '<a href="'+x[1]+'">'+x[0]+' &rarr;</a>';}).join('');
    fixEl.innerHTML='<p style="margin:0 0 10px">'+r.fix+'</p><div class="srcs">'+ls+'</div>';
  }
  root.querySelectorAll('.iseg').forEach(function(seg){
    var q=seg.getAttribute('data-q');
    seg.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        seg.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
        b.classList.add('on'); ans[q]=b.getAttribute('data-v'); render();
      });
    });
  });
  render();
})();
</script>'''

# ============ TOOL 2: PLATFORM-WEIGHTED VISIBILITY ============
ENG=[('chatgpt','ChatGPT','0.30'),('gemini','Gemini','0.20'),('perplexity','Perplexity','0.20'),('claude','Claude','0.20'),('grok','Grok','0.10')]
rows=""
for eid,name,w in ENG:
    rows+=(f'<div class="erow"><div class="ename">{name}</div>'
      f'<div class="fld"><div class="lab">Mentioned</div><input class="tin" id="pv_{eid}_m" inputmode="numeric" value=""></div>'
      f'<div class="fld"><div class="lab">Prompts issued</div><input class="tin" id="pv_{eid}_q" inputmode="numeric" value=""></div>'
      f'<div class="fld"><div class="lab">Weight</div><input class="tin" id="pv_{eid}_w" inputmode="decimal" value="{w}"></div></div>')
d2_body=('<section class="card" id="pv">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Enter your tracking counts per engine</div>'
  '<p class="hint" style="margin:6px 0 12px">Leave an engine blank to exclude it, the score renormalises across the engines you actually track. Default weights are market-share estimates; edit them for your market.</p>'
  +rows+'</div>\n    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Platform-weighted visibility</div>\n'
  '      <div class="scorewrap"><span class="score" id="pvScore">0</span><span class="score-d">%</span></div>\n'
  '      <span class="scoreband" id="pvBand" style="background:rgba(255,255,255,.1);color:#fff">Enter counts</span>\n'
  '      <div class="gauge"><div class="gfill" id="pvFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">Per-engine visibility</div><div id="pvBreak"></div></div>\n'
  '    </div>\n  </div>\n</section>')
d2_method=('<section class="method"><h2>The formula</h2>'
  '<p>Engines do not perform uniformly, so pooling them into one average hides the thing you need to see. Visibility is a weighted composite: for each engine, mentions divided by prompts issued, times a normalised platform weight. The score renormalises over the engines you actually track, so skipping two engines does not silently understate you.</p>'
  '<p>Run a fixed prompt set 3 to 5 times per engine and average before entering counts, single runs are noisy.</p>'
  '<div class="srcs"><a href="/blogs/citation-vs-mention-vs-recommendation">The measurement taxonomy &rarr;</a><a href="/blogs/prompt-to-citation-tracking">Prompt-to-citation tracking &rarr;</a></div></section>')
d2_script=r'''<script>
(function(){
  var root=document.getElementById('pv'); if(!root) return;
  var ENG=[['chatgpt','ChatGPT'],['gemini','Gemini'],['perplexity','Perplexity'],['claude','Claude'],['grok','Grok']];
  function num(id){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?null:v;}
  function compute(){
    var score=0,covered=0,rows=[];
    ENG.forEach(function(e){
      var m=num('pv_'+e[0]+'_m'),q=num('pv_'+e[0]+'_q'),w=num('pv_'+e[0]+'_w');
      if(q===null||q<=0||w===null||w<0){return;}
      var mm=(m===null?0:m); var pct=Math.max(0,Math.min(100,100*mm/q));
      score+=w*pct; covered+=w; rows.push([e[1],pct,w]);
    });
    var out=covered>0?score/covered:0;
    var scoreEl=document.getElementById('pvScore'),bandEl=document.getElementById('pvBand'),fill=document.getElementById('pvFill'),br=document.getElementById('pvBreak');
    if(covered<=0){scoreEl.textContent='0';bandEl.textContent='Enter counts';bandEl.style.background='rgba(255,255,255,.1)';bandEl.style.color='#fff';fill.style.width='0%';br.innerHTML='<p class="hint">Per-engine numbers appear here.</p>';return;}
    scoreEl.textContent=out.toFixed(1); fill.style.width=Math.min(100,out)+'%';
    var lbl,col;
    if(out>=50){lbl='Strong';col='var(--up)';}else if(out>=25){lbl='Building';col='#C9922E';}else{lbl='At risk';col='var(--signal)';}
    bandEl.textContent=lbl; bandEl.style.background=col; bandEl.style.color='#0b0b0c'; fill.style.background=col;
    rows.sort(function(a,b){return b[1]-a[1];});
    br.innerHTML=rows.map(function(r){
      return '<div class="lt-stat"><span>'+r[0]+' <span style="color:rgba(255,255,255,.4)">(w '+r[2]+')</span></span><strong>'+r[1].toFixed(1)+'%</strong></div>';
    }).join('');
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

# ============ TOOL 3: SENTIMENT + SHARE OF VOICE ============
d3_body=('<section class="card" id="ss">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Contextual sentiment</div>'
  '<div class="num-grid">'
  '<div class="fld"><div class="lab">Positive mentions</div><input class="tin" id="ssPos" inputmode="numeric" value=""></div>'
  '<div class="fld"><div class="lab">Neutral mentions</div><input class="tin" id="ssNeu" inputmode="numeric" value=""></div>'
  '<div class="fld"><div class="lab">Negative mentions</div><input class="tin" id="ssNeg" inputmode="numeric" value=""></div>'
  '</div></div>\n'
  '      <div class="cat" style="margin-top:16px"><div class="cat-h">Entity share of voice</div>'
  '<div class="fld"><div class="lab">Your brand mentions</div><input class="tin" id="ssBrand" inputmode="numeric" value=""></div>'
  '<div class="fld"><div class="lab">Competitor mentions <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">one per line: name, count</span></div>'
  '<textarea class="ta" id="ssComp" style="min-height:120px" placeholder="RivalA, 91&#10;RivalB, 55"></textarea>'
  '<p class="hint">Only include competitors you can resolve to a real domain. Engines invent plausible vendor names, and hallucinated rivals in the denominator quietly depress your score.</p></div></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Results</div>\n'
  '      <div class="metrics" id="ssMetrics">'
  '<div class="metric"><div class="m-val" id="ssSent">--</div><div class="m-lab">Sentiment index</div></div>'
  '<div class="metric"><div class="m-val" id="ssSov">--</div><div class="m-lab">Share of voice</div></div>'
  '</div>\n'
  '      <div class="gaps"><div class="gaps-h">Read-out</div><div id="ssNote"><p class="hint">Both scores update as you type.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
d3_method=('<section class="method"><h2>The two formulas</h2>'
  '<p>The sentiment index normalises tone to a 0 to 100 score: positive mentions count full, neutral count half, negative count zero. That 0.5 on neutral means a negative mention costs exactly twice what a neutral one does. Aim for 70 or above with no recurring negatives.</p>'
  '<p>Share of voice is your mentions over your mentions plus verified competitor mentions. Resolve every competitor to a real domain first, or a hallucinated name will drag your number down.</p>'
  '<div class="srcs"><a href="/blogs/citation-vs-mention-vs-recommendation">The measurement taxonomy &rarr;</a><a href="/blogs/why-engines-recommend-different-vendors">Why engines pick different vendors &rarr;</a></div></section>')
d3_script=r'''<script>
(function(){
  var root=document.getElementById('ss'); if(!root) return;
  function n(id){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?0:Math.max(0,v);}
  function compute(){
    var pos=n('ssPos'),neu=n('ssNeu'),neg=n('ssNeg'),tot=pos+neu+neg;
    var sentEl=document.getElementById('ssSent'),sovEl=document.getElementById('ssSov'),note=document.getElementById('ssNote');
    var sent=null;
    if(tot>0){sent=(pos+0.5*neu)/tot*100; sentEl.textContent=sent.toFixed(1);}else{sentEl.textContent='--';}
    var brand=n('ssBrand'),rivals=0,names=0;
    document.getElementById('ssComp').value.split('\n').forEach(function(line){
      line=line.trim(); if(!line) return;
      var m=line.match(/(-?\d+(\.\d+)?)\s*$/);
      if(m){rivals+=Math.max(0,parseFloat(m[1]));names++;}
    });
    var denom=brand+rivals, sov=denom>0?brand/denom*100:null;
    sovEl.textContent=(sov===null)?'--':sov.toFixed(1);
    var msgs=[];
    if(sent!==null){ if(sent>=70) msgs.push('Sentiment is healthy at '+sent.toFixed(1)+', at or above the 70 target.'); else if(sent>=50) msgs.push('Sentiment '+sent.toFixed(1)+' is neutral-leaning, look for recurring negative framings to fix.'); else msgs.push('Sentiment '+sent.toFixed(1)+' is a problem, a negative mention costs twice a neutral one.'); }
    if(sov!==null){ msgs.push('Share of voice '+sov.toFixed(1)+'% against '+names+' competitor'+(names===1?'':'s')+' ('+rivals+' mentions).'); }
    note.innerHTML = msgs.length? msgs.map(function(m){return '<p style="margin:0 0 8px">'+m+'</p>';}).join('') : '<p class="hint">Both scores update as you type.</p>';
  }
  root.querySelectorAll('input,textarea').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

# ============ TOOL 4: CROSS-ENGINE SOURCE OVERLAP ============
ENG4=[('a','ChatGPT'),('b','Gemini'),('c','Perplexity'),('d','Claude')]
tas=""
for eid,name in ENG4:
    tas+=(f'<div class="fld"><div class="lab">{name} <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">cited domains, one per line</span></div>'
      f'<textarea class="ta" id="jx_{eid}" style="min-height:120px" placeholder="reddit.com&#10;g2.com&#10;wikipedia.org"></textarea></div>')
d4_body=('<section class="card" id="jx">\n  <div class="grid calc">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Paste the domains each engine cited for one prompt</div>'
  '<p class="hint" style="margin:6px 0 12px">Use two or more engines. Domains are compared as sets, duplicates and protocol/paths are ignored, just the host matters.</p>'
  '<div class="num-grid">'+tas+'</div></div>\n'
  '    </div>\n'
  '    <div class="output">\n      <div class="o-eyebrow">Pairwise Jaccard overlap</div>\n'
  '      <div id="jxOut" style="margin-top:14px"><p class="hint">Overlap scores appear here once two engines have domains.</p></div>\n'
  '    </div>\n  </div>\n</section>')
d4_method=('<section class="method"><h2>What Jaccard overlap tells you</h2>'
  '<p>Engines do not share a retrieval index. For the same prompt, their cited domain sets typically overlap only 16 to 20 percent. This tool computes the Jaccard coefficient, the size of the intersection over the size of the union, for every pair of engines you paste.</p>'
  '<p>Low overlap is normal and it is the point: it means you cannot run one AI-search strategy. Each engine consults a different set of third-party domains, so your off-page targets differ by engine. Overlap above 0.35 usually means your prompt set is too narrow to generalise.</p>'
  '<div class="srcs"><a href="/blogs/citation-vs-mention-vs-recommendation">The measurement taxonomy &rarr;</a><a href="/blogs/why-engines-recommend-different-vendors">Why engines pick different vendors &rarr;</a></div></section>')
d4_script=r'''<script>
(function(){
  var root=document.getElementById('jx'); if(!root) return;
  var ENG=[['a','ChatGPT'],['b','Gemini'],['c','Perplexity'],['d','Claude']];
  function host(s){s=s.trim().toLowerCase();if(!s)return null;s=s.replace(/^https?:\/\//,'').replace(/^www\./,'');s=s.split('/')[0].split('?')[0];return s||null;}
  function setOf(id){var out={};document.getElementById('jx_'+id).value.split('\n').forEach(function(l){var h=host(l);if(h)out[h]=1;});return Object.keys(out);}
  function jac(a,b){var A={};a.forEach(function(x){A[x]=1;});var inter=0,uni={};a.forEach(function(x){uni[x]=1;});b.forEach(function(x){uni[x]=1;if(A[x])inter++;});var u=Object.keys(uni).length;return u?inter/u:0;}
  function compute(){
    var sets={},present=[];
    ENG.forEach(function(e){var s=setOf(e[0]);sets[e[0]]=s;if(s.length)present.push(e);});
    var out=document.getElementById('jxOut');
    if(present.length<2){out.innerHTML='<p class="hint">Overlap scores appear here once two engines have domains.</p>';return;}
    var rows=[],vals=[];
    for(var i=0;i<present.length;i++)for(var j=i+1;j<present.length;j++){
      var e1=present[i],e2=present[j],s=jac(sets[e1[0]],sets[e2[0]]);vals.push(s);
      var inter=sets[e1[0]].filter(function(x){return sets[e2[0]].indexOf(x)>-1;}).length;
      var col=s>0.35?'var(--signal)':(s>=0.16?'var(--up)':'#C9922E');
      rows.push('<div class="lt-stat"><span>'+e1[1]+' ∩ '+e2[1]+' <span style="color:rgba(255,255,255,.4)">('+inter+' shared)</span></span><strong style="color:'+col+'">'+s.toFixed(3)+'</strong></div>');
    }
    var avg=vals.reduce(function(a,b){return a+b;},0)/vals.length;
    var note=avg>0.35?'Average '+avg.toFixed(3)+' is high, your prompt set may be too narrow to generalise.':'Average '+avg.toFixed(3)+', in the expected 0.16 to 0.20 band means engines cite different domains, optimise each separately.';
    out.innerHTML=rows.join('')+'<p class="hint" style="margin-top:12px">'+note+'</p>';
  }
  root.querySelectorAll('textarea').forEach(function(t){t.addEventListener('input',compute);});
  compute();
})();
</script>'''

TOOLS=[
 ("ai-visibility-signal-diagnostic",
  "AI Visibility Signal Diagnostic · Free Tool · rawmktg.",
  "Answer three questions and find out which AI-search signal is broken, mention, citation, or recommendation, and the specific fix for each.",
  "Measurement Taxonomy · Diagnostic","AI Visibility Signal Diagnostic",
  "When AI visibility is bad, the taxonomy tells you where to look. Answer three questions and isolate the first broken signal, mention, citation, or recommendation, with the fix that actually applies.",
  d1_body,d1_method,d1_script),
 ("platform-weighted-visibility-calculator",
  "Platform-Weighted Visibility Calculator · Free Tool · rawmktg.",
  "Enter per-engine mention and prompt counts and compute a weighted AI-visibility score with renormalisation and a per-engine breakdown.",
  "Measurement Taxonomy · Calculator","Platform-Weighted Visibility Calculator",
  "Pooling every engine into one average hides where you actually win. Enter your counts per engine and get a weighted visibility score that renormalises over the engines you track, plus the per-engine breakdown.",
  d2_body,d2_method,d2_script),
 ("sentiment-share-of-voice-calculator",
  "Sentiment & Share-of-Voice Calculator · Free Tool · rawmktg.",
  "Compute a contextual sentiment index and entity share of voice from your AI-answer mention counts, with the hallucinated-competitor guardrail.",
  "Measurement Taxonomy · Calculator","Sentiment & Share-of-Voice Calculator",
  "Being mentioned is not automatically good. Turn your positive, neutral and negative mention counts into a bounded sentiment index, and your brand-versus-competitor counts into entity share of voice.",
  d3_body,d3_method,d3_script),
 ("cross-engine-source-overlap-calculator",
  "Cross-Engine Source Overlap Calculator · Free Tool · rawmktg.",
  "Paste the domains each AI engine cited for one prompt and compute the pairwise Jaccard overlap, showing how little engines agree on sources.",
  "Measurement Taxonomy · Diagnostic","Cross-Engine Source Overlap Calculator",
  "Engines barely agree on sources, overlap runs 16 to 20 percent for the same prompt. Paste each engine's cited domains and see the pairwise Jaccard overlap, so you know to optimise each engine separately.",
  d4_body,d4_method,d4_script),
]
built=[]
for t in TOOLS:
    html=page(*t); built.append((t[0],html))

# validate
import json as J
for slug,html in built:
    # node check the last <script> (tool logic)
    ms=re.findall(r'<script>(?!window\.dataLayer).*?</script>', html, re.S)
    logic=[s for s in ms if 'getElementById' in s]
    ok="n/a"
    if logic:
        open("/tmp/t.js","w").write(logic[-1][8:-9])
        r=subprocess.run(["node","--check","/tmp/t.js"],capture_output=True,text=True)
        ok="OK" if r.returncode==0 else "FAIL "+r.stderr[:300]
    jc=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if (J.loads(b) or True))
    amp="BAD &amp;middot;" if "&amp;middot;" in html else "clean"
    print(f"{slug:44} node:{ok:6} jsonld:{jc} title:{amp} h1:{html.count('<h1')}")
