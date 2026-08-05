#!/usr/bin/env python3
"""SCRATCH: build 5 new tools (standalone + embed in blogs) + rebuild hub. Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
os.makedirs("tools", exist_ok=True)

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
if 'href="/tools"' not in NAV:
    NAV=NAV.replace('<a href="/glossary">Glossary</a>','<a href="/glossary">Glossary</a>\n        <a href="/tools">Tools</a>',1)

def esc(t): return H.escape(t,quote=False)
def escq(t): return H.escape(t,quote=True)
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
ORG={"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}

# ============================ TOOL DEFINITIONS ============================
RC_CARD = """<section class="card" id="rcTool">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Page last updated</div>
        <input type="date" id="rcDate">
        <p class="hint">When the page's main content (and its dateModified) last changed.</p></div>
      <div class="fld"><div class="lab">AI engine</div>
        <div class="seg" id="rcEngine"><button data-h="90" class="sel">ChatGPT</button><button data-h="75">Google AIO</button><button data-h="60">Gemini</button><button data-h="30">Perplexity</button></div>
        <p class="hint">Each engine weights freshness differently. Perplexity has the tightest window (~30 days); ChatGPT the widest (~90).</p></div>
      <div class="fld"><div class="lab">Current monthly AI citations <span class="val" style="color:rgba(255,255,255,.5)">optional</span></div>
        <div class="ipt"><input type="number" id="rcCites" value="40" min="0" step="1"></div>
        <p class="hint">Used to translate retention into citations at risk.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Citation retention today</div>
      <div class="o-lift" id="rcRet">100%</div>
      <div class="o-sub" id="rcSub">freshness still in window</div>
      <div class="barrow"><span class="l">Now</span><div class="track"><div class="fill proj" id="rcF0"></div></div><b id="rcV0">100%</b></div>
      <div class="barrow"><span class="l">+30 days</span><div class="track"><div class="fill proj" id="rcF30"></div></div><b id="rcV30">-</b></div>
      <div class="barrow"><span class="l">+60 days</span><div class="track"><div class="fill proj" id="rcF60"></div></div><b id="rcV60">-</b></div>
      <div class="barrow"><span class="l">+90 days</span><div class="track"><div class="fill proj" id="rcF90"></div></div><b id="rcV90">-</b></div>
      <div class="chips" id="rcChips"></div>
      <p class="caveat">Models an exponential freshness half-life per engine (Perplexity ~30d, Gemini ~60d, Google AIO ~75d, ChatGPT ~90d), grounded in the 30-day-half-life research: pages unrefreshed for 90+ days are ~3.2x more likely to lose citations. Directional, not a forecast.</p>
    </div>
  </div>
</section>"""
RC_JS = """(function(){
  var root=document.getElementById('rcTool'); if(!root) return;
  var dateEl=document.getElementById('rcDate'), citesEl=document.getElementById('rcCites');
  var d=new Date(); d.setDate(d.getDate()-60); dateEl.value=d.toISOString().slice(0,10);
  function H(){var s=root.querySelector('#rcEngine button.sel');return s?parseFloat(s.dataset.h):90;}
  function ageDays(){var t=new Date(dateEl.value); if(isNaN(t)) return 0; return Math.max(0,Math.round((Date.now()-t)/86400000));}
  function ret(age,h){return Math.pow(0.5, age/h);}
  function setBar(f,v,val){document.getElementById(f).style.width=Math.round(val*100)+'%';document.getElementById(v).textContent=Math.round(val*100)+'%';}
  function compute(){
    var h=H(), age=ageDays();
    var r0=ret(age,h), r30=ret(age+30,h), r60=ret(age+60,h), r90=ret(age+90,h);
    document.getElementById('rcRet').textContent=Math.round(r0*100)+'%';
    setBar('rcF0','rcV0',r0); setBar('rcF30','rcV30',r30); setBar('rcF60','rcV60',r60); setBar('rcF90','rcV90',r90);
    var urgency=Math.max(1,Math.min(10,Math.round((1-r0)*12)));
    var sub=r0>=0.7?'fresh, comfortably in window':(r0>=0.45?'decaying, refresh soon':'stale, refresh now');
    document.getElementById('rcSub').textContent=sub+' \\u00b7 age '+age+'d';
    var cites=Math.max(0,parseFloat(citesEl.value)||0), lost30=Math.round(cites*(r0-r30));
    var br=document.getElementById('rcChips'); br.innerHTML='';
    function chip(t,m){var c=document.createElement('span');c.className='chip'+(m?' muted':'');c.textContent=t;br.appendChild(c);}
    chip('Refresh urgency '+urgency+'/10');
    if(cites>0) chip('~'+lost30+' citations lost in 30d', true);
    var nd=new Date(dateEl.value); nd.setDate(nd.getDate()+Math.round(0.7*h));
    chip('Refresh by '+nd.toISOString().slice(0,10), true);
  }
  dateEl.addEventListener('input',compute); citesEl.addEventListener('input',compute);
  root.querySelector('#rcEngine').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;this.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});b.classList.add('sel');compute();});
  compute();
})();"""

PC_CARD = """<section class="card" id="pcTool">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Primary topic / keyword <span class="val" style="color:rgba(255,255,255,.5)">optional</span></div>
        <div class="ipt"><input type="text" id="pcKw" placeholder="e.g. chiropractic software"></div></div>
      <div class="fld"><div class="lab">Paste your page content</div>
        <textarea class="ta" id="pcText" placeholder="Paste your article HTML or plain text, including your headings..."></textarea>
        <p class="hint">Works with HTML or plain text. For plain text, keep each heading on its own line. Nothing is uploaded, analysis runs in your browser.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Citability score</div>
      <div class="o-lift" id="pcScore">0</div>
      <div class="o-sub" id="pcSub">paste content to analyze</div>
      <div class="metrics" id="pcMetrics"></div>
      <p class="caveat">Heuristic analysis against high-citation benchmarks: ~55% of AI citations come from the first 30% of a page, ~60% of cited pages use question-format headings, and cited sections pair a statistic with a quote. Directional.</p>
    </div>
  </div>
</section>"""
PC_JS = """(function(){
  var root=document.getElementById('pcTool'); if(!root) return;
  var ta=document.getElementById('pcText'), kw=document.getElementById('pcKw');
  var QW=/^(how|what|why|when|which|where|who|does|do|is|are|can|should|will)\\b/i;
  function parse(raw){
    raw=(raw||'').trim(); if(!raw) return null;
    var headings=[], text=raw;
    if(/<h[1-6]/i.test(raw)){ try{var doc=new DOMParser().parseFromString(raw,'text/html');
      doc.querySelectorAll('h1,h2,h3').forEach(function(h){var t=h.textContent.trim(); if(t) headings.push(t);});
      text=doc.body.textContent||raw;}catch(e){} }
    else { raw.split(/\\n+/).forEach(function(ln){var t=ln.trim().replace(/^#+\\s*/,'');
      if(t && t.split(/\\s+/).length<=12 && !/[.!?:]$/.test(t)) headings.push(t);}); }
    return {headings:headings, text:text};
  }
  function compute(){
    var p=parse(ta.value), out=document.getElementById('pcMetrics');
    if(!p){document.getElementById('pcScore').textContent='0';document.getElementById('pcSub').textContent='paste content to analyze';out.innerHTML='';return;}
    var words=p.text.split(/\\s+/).filter(Boolean), wc=words.length;
    var qh=p.headings.length? p.headings.filter(function(h){return /\\?$/.test(h)||QW.test(h);}).length/p.headings.length : 0;
    var first=words.slice(0,Math.max(1,Math.round(wc*0.3))).join(' ').toLowerCase();
    var statRe=/\\d+(\\.\\d+)?%|\\$\\d|\\b\\d{2,}\\b/;
    var kwv=(kw.value||'').trim().toLowerCase();
    var front=Math.min(1,(statRe.test(first)?0.6:0)+(kwv?(first.indexOf(kwv)>=0?0.4:0):0.4));
    var stats=(p.text.match(/\\d+(\\.\\d+)?%|\\$\\d[\\d,\\.]*|\\b\\d{2,}\\b/g)||[]).length;
    var statScore=Math.min(1,(wc?stats/(wc/100):0)/1.5);
    var quotes=(p.text.match(/["\\u201c\\u201d]/g)||[]).length/2+(p.text.match(/according to|says|said/gi)||[]).length;
    var quoteScore=Math.min(1,quotes/Math.max(1,p.headings.length||3));
    var avgSec=p.headings.length? wc/p.headings.length : wc;
    var secScore=(avgSec>=90&&avgSec<=320)?1:(avgSec<90?0.5:0.4);
    var scan=/(^|\\n)\\s*[-*\\u2022]|\\|.*\\|/.test(ta.value)?1:0.3;
    var M=[
      {n:'Question-format headings',v:qh,b:'60%+ of headings',f:'Rewrite section headings as the questions buyers ask ("How does X work for enterprise?").'},
      {n:'Front-loaded key claim',v:front,b:'claim/stat in first 30%',f:'Put your core answer and a hard number up top, ~55% of citations come from the first third.'},
      {n:'Statistic density',v:statScore,b:'~1+ stat / 100 words',f:'Add concrete figures, dates and percentages throughout.'},
      {n:'Quotes & attribution',v:quoteScore,b:'a quote per section',f:'Add attributed expert quotes; they measurably lift citation rates.'},
      {n:'Section length',v:secScore,b:'~120-300 words / section',f:'Keep sections self-contained and citable, neither thin nor sprawling.'},
      {n:'Scannable structure',v:scan,b:'lists / tables present',f:'Add bullet lists or comparison tables an engine can lift cleanly.'}
    ];
    var W=[22,22,18,14,12,12], score=0; M.forEach(function(m,i){score+=m.v*W[i];}); score=Math.round(score);
    document.getElementById('pcScore').textContent=score;
    document.getElementById('pcSub').textContent=(score>=70?'cited-ready':(score>=45?'developing':'at risk'))+' \\u00b7 '+wc+' words \\u00b7 '+p.headings.length+' headings';
    out.innerHTML=M.map(function(m){var v=Math.round(m.v*100);var vd=m.v>=0.7?'good':(m.v>=0.4?'warn':'bad');
      return '<div class="metric"><div class="metric-top"><span class="metric-name">'+m.n+'</span><span class="verdict '+vd+'">'+(vd==='good'?'strong':vd==='warn'?'partial':'weak')+'</span></div><div class="metric-bar"><i style="width:'+v+'%"></i></div><div class="metric-fix"><b>'+m.b+'.</b> '+m.f+'</div></div>';}).join('');
  }
  ta.addEventListener('input',compute); kw.addEventListener('input',compute); compute();
})();"""

CA_CARD = """<section class="card" id="caTool">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Your brand / product name</div><div class="ipt"><input type="text" id="caBrand" placeholder="e.g. Acme Robotics"></div></div>
      <div class="fld"><div class="lab">Paste your page content</div>
        <textarea class="ta" id="caText" placeholder="Paste your article HTML or plain text..."></textarea>
        <p class="hint">Checks the four parts of the Claim-Anchoring framework. Runs in your browser.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Hallucination-risk score</div>
      <div class="o-lift" id="caScore">-</div>
      <div class="o-sub" id="caSub">paste content to analyze</div>
      <div class="metrics" id="caMetrics"></div>
      <div class="flags" id="caFlags"></div>
      <p class="caveat">Scores content against the Claim-Anchoring framework: answer capsules (40-60 words under each heading), self-contained sections (120-180 words), a proof-pairing ratio of 0.70+ (evidence per claim), and brand-name co-location with key claims. Heuristic and directional.</p>
    </div>
  </div>
</section>"""
CA_JS = """(function(){
  var root=document.getElementById('caTool'); if(!root) return;
  var ta=document.getElementById('caText'), brandEl=document.getElementById('caBrand');
  function sections(raw){
    raw=(raw||'').trim(); var secs=[];
    if(/<h[1-6]/i.test(raw)){ try{var doc=new DOMParser().parseFromString(raw,'text/html');
      var cur=null; doc.body.querySelectorAll('h1,h2,h3,p,li').forEach(function(n){
        if(/^H[1-3]$/.test(n.tagName)){ if(cur)secs.push(cur); cur={h:n.textContent.trim(),t:''};}
        else if(cur){cur.t+=' '+n.textContent.trim();}});
      if(cur)secs.push(cur);}catch(e){} }
    if(!secs.length){ raw.split(/\\n\\s*\\n/).forEach(function(b){var lines=b.split(/\\n/),h='',t=b;
      if(lines[0]&&lines[0].trim().split(/\\s+/).length<=12&&!/[.!?]$/.test(lines[0].trim())){h=lines[0].trim().replace(/^#+\\s*/,'');t=lines.slice(1).join(' ');}
      secs.push({h:h,t:t.trim()});}); }
    return secs.filter(function(s){return s.t||s.h;});
  }
  function wc(s){return (s||'').split(/\\s+/).filter(Boolean).length;}
  function compute(){
    var raw=(ta.value||'').trim(), brand=(brandEl.value||'').trim();
    var mEl=document.getElementById('caMetrics'), fEl=document.getElementById('caFlags');
    if(!raw){document.getElementById('caScore').textContent='-';document.getElementById('caSub').textContent='paste content to analyze';mEl.innerHTML='';fEl.innerHTML='';return;}
    var secs=sections(raw), capOK=0, autoOK=0, brOK=0, flags=[];
    secs.forEach(function(s){
      var w=wc(s.t), fs=((s.t.split(/[.!?]\\s/)[0])||'').split(/\\s+/).filter(Boolean).length;
      var cap=fs>=25&&fs<=70; if(cap)capOK++;
      var auto=w>=80&&w<=260&&!/^\\s*(this|that|it|these|those|here|they)\\b/i.test(s.t); if(auto)autoOK++;
      var hb=brand&&((s.t+' '+s.h).toLowerCase().indexOf(brand.toLowerCase())>=0); if(hb)brOK++;
      if(s.h&&!cap) flags.push('No clear answer capsule under: "'+s.h+'"');
      else if(s.h&&!auto) flags.push('Section not self-contained: "'+s.h+'"');
    });
    var n=Math.max(1,secs.length);
    var sents=raw.replace(/<[^>]+>/g,' ').split(/[.!?]+\\s+/).filter(function(x){return x.split(/\\s+/).length>3;});
    var evid=sents.filter(function(x){return /\\d+(\\.\\d+)?%|\\b\\d{2,}\\b|\\$\\d|according to|["\\u201c\\u201d]|https?:\\/\\//i.test(x);}).length;
    var ratio=sents.length?evid/sents.length:0;
    var capPct=capOK/n, autoPct=autoOK/n;
    var ratioScore=Math.min(1,ratio/0.7), brandScore=brand?Math.min(1,(brOK/n)/0.6):0.5;
    var comp=capPct*0.28+autoPct*0.24+ratioScore*0.30+brandScore*0.18, risk=Math.round((1-comp)*100);
    document.getElementById('caScore').textContent=risk;
    document.getElementById('caSub').textContent=(risk<=35?'low risk':(risk<=60?'moderate risk':'high risk'))+' \\u00b7 '+secs.length+' sections';
    var M=[
      {n:'Answer capsules',v:capPct,f:'Open each section with a 40-60 word direct answer to its heading.'},
      {n:'Section autonomy',v:autoPct,f:'Make each section 120-180 words and self-contained; avoid "this/it" openings.'},
      {n:'Proof-pairing ratio',v:ratioScore,f:'Pair every claim with a stat, quote or source. Target 0.70+ ('+(Math.round(ratio*100)/100)+' now).'},
      {n:'Brand association',v:brandScore,f:brand?'Name the brand alongside each key claim.':'Enter your brand name to score co-location.'}
    ];
    mEl.innerHTML=M.map(function(m){var v=Math.round(m.v*100);var vd=m.v>=0.7?'good':(m.v>=0.4?'warn':'bad');
      return '<div class="metric"><div class="metric-top"><span class="metric-name">'+m.n+'</span><span class="verdict '+vd+'">'+(vd==='good'?'solid':vd==='warn'?'partial':'weak')+'</span></div><div class="metric-bar"><i style="width:'+v+'%"></i></div><div class="metric-fix">'+m.f+'</div></div>';}).join('');
    fEl.innerHTML=flags.slice(0,4).map(function(f){return '<div class="flag">'+f.replace(/</g,'&lt;')+'</div>';}).join('')||'<div class="flag ok">No structural flags, sections are well anchored.</div>';
  }
  ta.addEventListener('input',compute); brandEl.addEventListener('input',compute); compute();
})();"""

AM_CARD = """<section class="card" id="amTool">
  <div class="controls" style="margin-bottom:22px">
    <div class="fld"><div class="lab">Content type</div>
      <div class="seg" id="amType"><button data-k="product" class="sel">Product page</button><button data-k="guide">Educational guide</button><button data-k="compare">Comparison</button><button data-k="news">News</button></div></div>
    <div class="fld"><div class="lab">Target engines</div>
      <div class="ptoggles" id="amPlat"><button class="ptog on" data-p="chatgpt">ChatGPT</button><button class="ptog on" data-p="perplexity">Perplexity</button><button class="ptog on" data-p="gemini">Gemini</button><button class="ptog on" data-p="claude">Claude</button><button class="ptog on" data-p="aio">Google AIO</button></div></div>
  </div>
  <div class="mx-grid" id="amOut"></div>
  <p class="caveat">Recommendations synthesize per-engine retrieval behavior from the RAG and recency research: citation depth, freshness windows, and structure/schema preferences. Directional guidance, not engine documentation.</p>
</section>"""
AM_JS = """(function(){
  var root=document.getElementById('amTool'); if(!root) return;
  var P={
    chatgpt:{name:'ChatGPT',depth:'~5 citations / response',recency:'~90-day freshness window',structure:'Comparison & scenario tables, broad consensus',schema:'FAQPage, Product',top:'Wikipedia-grade consensus'},
    perplexity:{name:'Perplexity',depth:'~8 citations / response',recency:'Near real-time (~30 days)',structure:'Fresh, dated data tables & updated stats',schema:'dateModified, Article',top:'Recent news & forums'},
    gemini:{name:'Gemini',depth:'~8 citations / response',recency:'~60-day window',structure:'Community sentiment & clear summaries',schema:'FAQPage, HowTo',top:'Reddit & community'},
    claude:{name:'Claude',depth:'~13 citations / response',recency:'~6-month window',structure:'Long-form depth (2,000+ words), methodology',schema:'Article, citations',top:'PubMed / primary sources'},
    aio:{name:'Google AI Overviews',depth:'High, schema-dependent',recency:'Driven by dateModified',structure:'Scannable, direct answers',schema:'FAQPage (+lift), HowTo, dateModified',top:'Top-10 authority publishers'}
  };
  var TYPE={product:'Lead with specs, pricing and a comparison table; add Product + FAQPage schema.',
    guide:'Open with a 40-60 word answer, use question headings, pair one stat + one quote per section.',
    compare:'Use an "A vs B" table with explicit criteria, engines lift comparison structures directly.',
    news:'Stamp a visible date + dateModified; prioritise Perplexity and AI Overviews for recency.'};
  function compute(){
    var tBtn=root.querySelector('#amType button.sel'), type=tBtn.dataset.k;
    var on={}; root.querySelectorAll('#amPlat .ptog').forEach(function(b){on[b.dataset.p]=b.classList.contains('on');});
    var cards=Object.keys(P).filter(function(k){return on[k];}).map(function(k){var p=P[k];
      return '<div class="mx-card"><div class="mx-h"><span class="mx-name">'+p.name+'</span><span class="mx-badge">'+p.depth+'</span></div>'+
      '<div class="mx-row"><span class="k">Freshness</span><span class="v">'+p.recency+'</span></div>'+
      '<div class="mx-row"><span class="k">Structure</span><span class="v">'+p.structure+'</span></div>'+
      '<div class="mx-row"><span class="k">Schema</span><span class="v">'+p.schema+'</span></div>'+
      '<div class="mx-row"><span class="k">Leans on</span><span class="v">'+p.top+'</span></div></div>';}).join('');
    document.getElementById('amOut').innerHTML='<div class="flag ok" style="margin-bottom:4px">For a '+tBtn.textContent.toLowerCase()+': '+TYPE[type]+'</div>'+(cards||'<div class="flag">Select at least one engine.</div>');
  }
  root.querySelector('#amType').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;this.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});b.classList.add('sel');compute();});
  root.querySelector('#amPlat').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;b.classList.toggle('on');compute();});
  compute();
})();"""

FG_CARD = """<section class="card" id="fgTool">
  <div class="grid calc">
    <div class="controls">
      <p class="hint" style="margin-top:0">How many published pages/assets do you have at each funnel stage?</p>
      <div class="num-grid">
        <div class="fld"><div class="lab">TOFU</div><div class="ipt"><input type="number" id="fgT" value="40" min="0"></div></div>
        <div class="fld"><div class="lab">MOFU</div><div class="ipt"><input type="number" id="fgM" value="12" min="0"></div></div>
        <div class="fld"><div class="lab">BOFU</div><div class="ipt"><input type="number" id="fgB" value="6" min="0"></div></div>
      </div>
      <p class="hint">TOFU = awareness/explainer, MOFU = comparison/consideration, BOFU = pricing/decision. Most SaaS sites over-index TOFU and starve BOFU, the exact layer where AI sends ready-to-buy queries.</p>
    </div>
    <div class="output">
      <div class="o-eyebrow">Funnel balance</div>
      <div class="o-big" id="fgVerdict">-</div>
      <div class="o-sub" id="fgSub"></div>
      <div class="funnel-row"><div class="funnel-lab"><span>Your mix (T / M / B)</span><span id="fgYourTxt"></span></div><div class="stacked" id="fgYour"></div></div>
      <div class="funnel-row"><div class="funnel-lab"><span>Recommended</span><span>40 / 35 / 25</span></div><div class="stacked" id="fgRec"></div></div>
      <div class="chips" id="fgChips"></div>
      <p class="caveat">Benchmarked against a citation-optimized SaaS split (TOFU 40 / MOFU 35 / BOFU 25). The CX SaaS analysis found every player over-built awareness content and left ~430,000 monthly searches of MOFU/BOFU demand largely uncaptured. Directional.</p>
    </div>
  </div>
</section>"""
FG_JS = """(function(){
  var root=document.getElementById('fgTool'); if(!root) return;
  var T=document.getElementById('fgT'),M=document.getElementById('fgM'),B=document.getElementById('fgB');
  var REC=[40,35,25], COL=['#8A8278','#B4ADA2','#BC3F1D'];
  function bars(el,arr){el.innerHTML='';arr.forEach(function(v,i){var s=document.createElement('span');s.style.background=COL[i];s.style.width=v+'%';el.appendChild(s);});}
  function compute(){
    var t=Math.max(0,parseFloat(T.value)||0),m=Math.max(0,parseFloat(M.value)||0),b=Math.max(0,parseFloat(B.value)||0);
    var tot=t+m+b||1, pc=[t/tot*100,m/tot*100,b/tot*100];
    bars(document.getElementById('fgYour'),pc); bars(document.getElementById('fgRec'),REC);
    document.getElementById('fgYourTxt').textContent=Math.round(pc[0])+' / '+Math.round(pc[1])+' / '+Math.round(pc[2]);
    var need=[Math.round(REC[0]/100*tot),Math.round(REC[1]/100*tot),Math.round(REC[2]/100*tot)];
    var defM=Math.max(0,need[1]-m), defB=Math.max(0,need[2]-b), inverted=pc[0]>55;
    document.getElementById('fgVerdict').textContent=inverted?'Inverted':(pc[2]>=20?'Balanced':'Bottom-light');
    document.getElementById('fgSub').textContent=inverted?'too top-heavy for AI buying queries':(pc[2]>=20?'healthy decision-stage coverage':'thin at the decision stage');
    var br=document.getElementById('fgChips'); br.innerHTML='';
    function chip(x,m){var c=document.createElement('span');c.className='chip'+(m?' muted':'');c.textContent=x;br.appendChild(c);}
    if(defB>0) chip('Add ~'+defB+' BOFU pieces'); else chip('BOFU coverage on target');
    if(defM>0) chip('Add ~'+defM+' MOFU pieces', true);
    chip(Math.round(tot)+' pages total', true);
  }
  [T,M,B].forEach(function(el){el.addEventListener('input',compute);}); compute();
})();"""

def method(body, srcs):
    s="".join(f'<a href="{u}">{esc(t)} &rarr;</a>' for t,u in srcs)
    return f'<section class="method"><h2>How this works</h2>{body}<div class="srcs">{s}</div></section>'

NEW=[
 {"slug":"content-recency-decay","title":"Content Recency Decay Estimator","cat":"Free Tool · Estimator","appcat":"BusinessApplication",
  "deck":"Your AI citations have a shelf life. Estimate how fast a page's freshness, and its citations, decay on each engine, and when to refresh.",
  "desc":"Estimate how fast a page's AI citations decay by engine (Perplexity ~30d to ChatGPT ~90d) and get a refresh-by date, grounded in the 30-day content half-life research.",
  "card":RC_CARD,"js":RC_JS,
  "method":method("<p>AI engines increasingly weight <strong>freshness</strong>. Pages left unrefreshed for 90+ days are roughly <strong>3.2x more likely</strong> to lose their AI citations, and over 80% of citations on commercial queries come from pages updated within the prior 30 days. Each engine applies a different window, so this tool models an exponential freshness half-life per engine and projects retention forward.</p><p>Use the recommended refresh date as a trigger to update one statistic, the dateModified field, and one section heading, enough to re-enter the citation window.</p>",[("The 30-day content half-life","/blogs/30-day-content-half-life-recency-ai-ranking-signal")]),
  "embed":{"blog":"blogs/30-day-content-half-life-recency-ai-ranking-signal.html","eyebrow":"Free interactive tool","title":"Estimate your content's citation decay","deck":"Enter a page's last-updated date and engine to see how fast its AI citations fade, and when to refresh."}},
 {"slug":"page-citability-analyzer","title":"Page Citability Analyzer","cat":"Free Tool · Analyzer","appcat":"BusinessApplication",
  "deck":"Paste a page and score it against the structural fingerprint of high-citation content, then get the fixes that matter most.",
  "desc":"Paste a page and score its citability against high-citation benchmarks: question headings, front-loaded claims, statistic density, quotes, and structure.",
  "card":PC_CARD,"js":PC_JS,
  "method":method("<p>Cited pages share a structural fingerprint. About <strong>55%</strong> of AI citations come from the first 30% of a page, roughly <strong>60%</strong> of high-citation pages use question-format headings, and cited sections pair a statistic with a quote. This tool parses your content and scores it against those benchmarks, then ranks the fixes.</p><p>It runs entirely in your browser, paste the real page text for the most accurate read.</p>",[("Anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page"),("Topical authority","/blogs/topical-authority-cluster-ai-shortlists")]),
  "embed":{"blog":"blogs/anatomy-of-a-high-citation-page.html","eyebrow":"Free interactive tool","title":"Score your page's citability","deck":"Paste your content to see how it measures up against the high-citation benchmarks in this article."}},
 {"slug":"claim-anchoring-validator","title":"Claim-Anchoring Validator","cat":"Free Tool · Validator","appcat":"BusinessApplication",
  "deck":"Find the content that AI will mis-quote before you publish. Validate a page against the four-part Claim-Anchoring framework.",
  "desc":"Validate a page against the Claim-Anchoring framework, answer capsules, section autonomy, proof-pairing ratio, brand association, and get a hallucination-risk score.",
  "card":CA_CARD,"js":CA_JS,
  "method":method("<p>When AI mis-states a brand, it is usually filling a gap left by ambiguous content. The Claim-Anchoring framework closes those gaps with four moves: a 40-60 word <strong>answer capsule</strong> under each heading, <strong>self-contained sections</strong> (120-180 words), a <strong>proof-pairing ratio of 0.70+</strong> (evidence per claim), and the brand name beside every key claim. This validator scores all four and flags the riskiest sections.</p>",[("Hallucination-proofing your brand","/blogs/hallucination-proofing-your-brand")]),
  "embed":{"blog":"blogs/hallucination-proofing-your-brand.html","eyebrow":"Free interactive tool","title":"Validate your content against hallucination risk","deck":"Paste a page to score it on the four Claim-Anchoring signals and see which sections AI is most likely to mis-quote."}},
 {"slug":"ai-platform-optimizer","title":"AI Platform Optimization Matrix","cat":"Free Tool · Matrix","appcat":"BusinessApplication",
  "deck":"ChatGPT, Perplexity, Gemini, Claude and Google AI Overviews don't cite the same way. Get the structure, schema and cadence each one rewards.",
  "desc":"Pick your target AI engines and content type to get per-engine recommendations on structure, schema, freshness cadence, and citation depth.",
  "card":AM_CARD,"js":AM_JS,
  "method":method("<p>The major engines do not retrieve or cite the same way. Claude cites deeply (~13 sources) and rewards long-form methodology; Perplexity is near real-time and rewards fresh data; ChatGPT favors broad consensus and comparison structures; Google AI Overviews are schema-driven. Pick your targets and content type to get the structure, schema and refresh cadence each engine rewards.</p>",[("How RAG actually works","/blogs/how-rag-actually-works"),("Why engines recommend different vendors","/blogs/why-engines-recommend-different-vendors")]),
  "embed":{"blog":"blogs/how-rag-actually-works.html","eyebrow":"Free interactive tool","title":"Optimize for each AI engine","deck":"Choose your target engines and content type to see the structure and schema each one rewards."}},
 {"slug":"saas-funnel-gap-analyzer","title":"B2B SaaS Funnel Gap Analyzer","cat":"Free Tool · Analyzer","appcat":"BusinessApplication",
  "deck":"Most SaaS content is inverted, heavy on awareness, thin where AI sends buyers. See your funnel balance and what to build next.",
  "desc":"Enter your content counts by funnel stage to see your TOFU/MOFU/BOFU balance against a citation-optimized split and the gaps to close.",
  "card":FG_CARD,"js":FG_JS,
  "method":method("<p>AI sends a lot of <strong>decision-stage</strong> traffic, the best-X, X-vs-Y, and pricing queries that resolve in an answer. Yet most SaaS content programs are inverted: heavy on awareness, thin on the middle and bottom of the funnel. Our CX SaaS analysis found <strong>~430,000 monthly searches</strong> of MOFU/BOFU demand left largely uncaptured. Enter your page counts to see your balance against a citation-optimized split and what to build next.</p>",[("The CX SaaS discoverability analysis","/blogs/cx-saas-seo-discoverability-analysis")]),
  "embed":{"blog":"blogs/cx-saas-seo-discoverability-analysis.html","eyebrow":"Free interactive tool","title":"Analyze your content funnel balance","deck":"Enter your page counts by stage to see how your funnel compares to a citation-optimized SaaS split."}},
]

def shell(t):
    URL=f"https://rawmktg.com/tools/{t['slug']}"; title=t["title"]; desc=t["desc"]; deck=t["deck"]
    webapp={"@context":"https://schema.org","@type":"WebApplication","name":title,"url":URL,"description":desc,
      "applicationCategory":t["appcat"],"operatingSystem":"Web, all browsers","browserRequirements":"Requires JavaScript",
      "isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
      "publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"}}
    webpage={"@context":"https://schema.org","@type":"WebPage","name":title,"url":URL,"description":desc,
      "isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
      {"@type":"ListItem","position":2,"name":"Tools","item":"https://rawmktg.com/tools"},
      {"@type":"ListItem","position":3,"name":title,"item":URL}]}
    TITLE=f"{esc(title)} &middot; Free GEO Tool &middot; rawmktg."
    head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
      "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
      f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
      f"  <meta name=\"description\" content=\"{escq(desc)}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
      "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
      "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
      "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
      "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
      f"  <link rel=\"canonical\" href=\"{URL}\" />\n  <meta property=\"og:type\" content=\"website\" />\n"
      f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{escq(title)}\" />\n"
      f"  <meta property=\"og:description\" content=\"{escq(desc)}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
      "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
      f"  <meta name=\"twitter:title\" content=\"{escq(title)}\" />\n  <meta name=\"twitter:description\" content=\"{escq(desc)}\" />\n"
      f"  {jb(webapp)}\n  {jb(webpage)}\n  {jb(crumb)}\n  {jb({'@context':'https://schema.org',**ORG})}\n"
      "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n  "+FONTS+"\n  ")
    header=('<div class="page">\n  <header class="article-header">\n    <div class="article-eyebrow">'
      f'<span class="eyebrow-tag">{esc(t["cat"])}</span><span class="eyebrow-sep">&middot;</span><span class="eyebrow-date">Updated June 2026</span></div>\n'
      f'    <h1 class="article-headline">{esc(title)}</h1>\n    <p class="article-deck">{esc(deck)}</p>\n  </header>\n</div>\n')
    out=(head+STYLE+'\n  <link rel="stylesheet" href="/assets/tools.css" />\n  '+ADSENSE+
      "\n</head>\n<body>\n\n"+NAV+"\n\n"+header+
      '\n<main class="toolpage" id="article-main">\n  <div class="page">\n'+t["card"]+'\n'+t["method"]+'\n  </div>\n</main>\n\n'
      +NEWS+"\n\n"+FOOT+"\n\n<script>\n"+t["js"]+"\n</script>\n</body>\n</html>\n")
    open(f"tools/{t['slug']}.html","w",encoding="utf-8").write(out)
    return out.count(chr(8212))

def embed(t):
    e=t["embed"]; path=e["blog"]
    h=open(path,encoding="utf-8").read()
    if 'href="/assets/tools.css"' not in h:
        h=h.replace("</head>", '  <link rel="stylesheet" href="/assets/tools.css" />\n</head>',1)
    frag=('\n<section class="toolpage tool-embed">\n  <div class="embed-head">'
      f'<div class="embed-eyebrow">{esc(e["eyebrow"])}</div>'
      f'<div class="embed-title">{esc(e["title"])}</div>'
      f'<div class="embed-deck">{esc(e["deck"])}</div></div>\n'
      +t["card"]+
      f'\n  <div class="embed-foot">A free rawmktg tool. <a href="/tools/{t["slug"]}">Open the full tool &rarr;</a> &middot; <a href="/tools">see all tools</a></div>\n</section>\n'
      '<script>\n'+t["js"]+'\n</script>\n')
    # insertion point (always inside <main>): before FAQ, else about-block, else </main>
    placed=None
    for anchor in ['<div class="faq-section"','<div class="about-block"']:
        idx=h.find(anchor)
        if idx!=-1:
            h=h[:idx]+frag+"\n"+h[idx:]; placed=anchor; break
    if not placed:
        idx=h.find("</main>"); h=h[:idx]+frag+"\n"+h[idx:]; placed="</main>"
    open(path,"w",encoding="utf-8").write(h)
    return placed

for t in NEW:
    em=shell(t); placed=embed(t)
    print(f"  {t['slug']:26} standalone(em:{em}) embedded->{t['embed']['blog'].split('/')[-1]} @ {placed}")

# ---- rebuild hub with all 9 ----
EXIST=[
 {"slug":"geo-readiness-scorecard","title":"GEO Readiness Scorecard","cat":"Free Tool · Diagnostic","desc":"Score your brand's readiness to be cited by AI engines across crawlability, authority, Information Gain, and structure, with your top gaps ranked."},
 {"slug":"content-mix-planner","title":"GEO Content-Mix Planner","cat":"Free Tool · Planner","desc":"Turn your monthly content capacity into a citation-optimized mix: flagship research, derivative, product, and news."},
 {"slug":"zero-click-traffic-risk","title":"Zero-Click Traffic-at-Risk Estimator","cat":"Free Tool · Estimator","desc":"Estimate how much of your organic traffic is exposed to zero-click erosion as AI Overviews and AI Mode expand."},
 {"slug":"geo-lift-calculator","title":"GEO Lift Calculator","cat":"Free Tool · Calculator","desc":"Model the AI citation lift on your brand's Share of Model using the Princeton/KDD GEO coefficients."},
]
HUB=[{"slug":t["slug"],"title":t["title"],"cat":t["cat"],"desc":t["desc"]} for t in NEW]+EXIST
HUBURL="https://rawmktg.com/tools"
tiles="".join(f'<a class="tool-tile" href="/tools/{x["slug"]}"><div class="tt-cat">{esc(x["cat"])}</div><div class="tt-name">{esc(x["title"])}</div><div class="tt-desc">{esc(x["desc"])}</div><div class="tt-go">Open tool &rarr;</div></a>\n      ' for x in HUB)
itemlist={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"https://rawmktg.com/tools/{x['slug']}","name":x["title"]} for i,x in enumerate(HUB)]}
coll={"@context":"https://schema.org","@type":"CollectionPage","name":"Free GEO & AI-search tools","url":HUBURL,"description":"Free interactive tools to measure and improve your brand's visibility in AI search.","isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
crumbH={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":"Tools","item":HUBURL}]}
HDESC="Free interactive tools to measure and improve your brand's visibility in AI search: GEO readiness, content mix, zero-click risk, citation lift, recency decay, page citability, hallucination risk, engine optimization, and funnel balance."
hubhead=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
  "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
  "  <title>Free GEO &amp; AI-Search Tools &middot; rawmktg.</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
  f"  <meta name=\"description\" content=\"{escq(HDESC)}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
  "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
  "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
  "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
  "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
  f"  <link rel=\"canonical\" href=\"{HUBURL}\" />\n  <meta property=\"og:type\" content=\"website\" />\n"
  f"  <meta property=\"og:url\" content=\"{HUBURL}\" />\n  <meta property=\"og:title\" content=\"Free GEO &amp; AI-Search Tools\" />\n"
  f"  <meta property=\"og:description\" content=\"{escq(HDESC)}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
  f"  {jb(coll)}\n  {jb(itemlist)}\n  {jb(crumbH)}\n  {jb({'@context':'https://schema.org',**ORG})}\n"
  "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n  "+FONTS+"\n  ")
hub=(hubhead+STYLE+'\n  <link rel="stylesheet" href="/assets/tools.css" />\n  '+ADSENSE+
  "\n</head>\n<body>\n\n"+NAV+"\n\n"
  '<div class="page">\n  <header class="article-header">\n    <div class="article-eyebrow"><span class="eyebrow-tag">Free Tools</span><span class="eyebrow-sep">&middot;</span><span class="eyebrow-date">AI Search Intelligence</span></div>\n'
  '    <h1 class="article-headline">GEO &amp; AI-search tools</h1>\n    <p class="article-deck">Free, no-signup tools to measure and improve how often AI engines cite your brand. Built on the same research behind our teardowns.</p>\n  </header>\n</div>\n\n'
  '<main class="toolpage" id="article-main">\n  <div class="page">\n    <div class="tools-grid">\n      '+tiles+'\n    </div>\n  </div>\n</main>\n\n'
  +NEWS+"\n\n"+FOOT+"\n</body>\n</html>\n")
open("tools.html","w",encoding="utf-8").write(hub)
print("  hub rebuilt with",len(HUB),"tools")

# ---- sitemap + llms ----
s=open("sitemap.xml",encoding="utf-8").read()
anchor=s.find("<loc>https://rawmktg.com/glossary</loc>"); us=s.rfind("<url>",0,anchor)
add="".join(f"<url>\n    <loc>https://rawmktg.com/tools/{t['slug']}</loc>\n    <lastmod>2026-06-12</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>\n  " for t in NEW if f"/tools/{t['slug']}<" not in s)
s=s[:us]+add+s[us:]; open("sitemap.xml","w",encoding="utf-8").write(s)
print("  sitemap new tool urls added:", sum(1 for t in NEW if f"/tools/{t['slug']}</loc>" in s))

l=open("llms.txt",encoding="utf-8").read()
idx=l.find("- [All tools]")
lines="".join(f"- [{t['title']}](https://rawmktg.com/tools/{t['slug']}) - {t['desc']}\n" for t in NEW if f"/tools/{t['slug']})" not in l)
l=l[:idx]+lines+l[idx:]; open("llms.txt","w",encoding="utf-8").write(l)
print("  llms.txt new tool lines added")
print("DONE")
