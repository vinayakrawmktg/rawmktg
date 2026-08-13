#!/usr/bin/env python3
"""SCRATCH: build 3 retrieval tool pages under /tools. Do NOT commit as content."""
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

# ================================================= TOOL 1: CHUNK RETRIEVABILITY
a_body='''<section class="card" id="cra">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Primary topic / entity <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">optional</span></div>
        <input class="tin" id="craKw" placeholder="e.g. Acme onboarding"></div>
      <div class="fld"><div class="lab">Paste your page content</div>
        <textarea class="ta" id="craText" placeholder="Paste your article text or HTML. It gets split into passages, then each is scored as a retriever sees it, alone. Nothing is uploaded."></textarea>
        <p class="hint">Simulates fixed-size chunking (~150 words). Each passage is scored in isolation, with no title and no surrounding text, exactly the object that competes in the vector index.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Retrievability</div>
      <div class="lt-stats" id="craStats" style="margin-top:12px"></div>
      <div id="craChunks" style="max-height:420px;overflow:auto"></div>
      <p class="caveat">Heuristic scan for the failure modes in the article: unnamed subject, dangling pronouns, vague time anchors, buried answers, and low specificity. An orphaned chunk is one that never says what it is about.</p>
    </div>
  </div>
</section>'''
a_method=('<section class="method"><h2>What it checks</h2>'
  '<p>No model reads your page, it reads passages of it, scored alone. A passage that carries its meaning through pronouns or references to earlier paragraphs (\"the division\", \"this approach\", \"last year\") loses its subject when cut, and its vector drifts out of range of the query it should answer. This tool splits your content into passages and flags the <strong>orphaned</strong> ones, chunks that never name their own subject.</p>'
  '<p>It runs entirely in your browser, using transparent heuristics rather than a real embedding model.</p>'
  '<div class="srcs"><a href="/blogs/how-your-page-gets-retrieved">How your page gets retrieved &rarr;</a><a href="/tools/retrieval-readiness-checklist">Retrieval-Readiness Checklist &rarr;</a><a href="/tools/answer-block-optimizer">Answer Block Optimizer &rarr;</a></div></section>')
a_script=r'''<script>
(function(){
  var root=document.getElementById('cra'); if(!root) return;
  var ta=document.getElementById('craText'), kwEl=document.getElementById('craKw');
  var DANG=/^(it|its|this|that|these|those|they|their|the platform|the company|the division|the above|this approach|the tool|the method|the product|the feature|the team|he|she)\b/i;
  var VAGUE=/\b(last year|prior year|the prior quarter|prior fiscal|the previous (year|quarter|month)|next year|recently|currently|nowadays|these days)\b/i;
  function toText(raw){
    if(/<[a-z][\s\S]*>/i.test(raw)){ try{var d=new DOMParser().parseFromString(raw,'text/html'); return (d.body.innerText||d.body.textContent||raw);}catch(e){} }
    return raw;
  }
  function chunkize(text){
    var words=text.replace(/\s+/g,' ').trim().split(' ').filter(Boolean);
    var out=[], SIZE=150;
    for(var i=0;i<words.length;i+=SIZE){ out.push(words.slice(i,i+SIZE).join(' ')); }
    return out;
  }
  function scoreChunk(txt,kw){
    var lc=txt.toLowerCase();
    var first=(txt.split(/(?<=[.!?])\s+/)[0]||txt);
    var sentences=txt.split(/(?<=[.!?])\s+/).filter(function(s){return s.trim();});
    var propers=(txt.match(/\b[A-Z][a-zA-Z]{2,}\b/g)||[]).filter(function(w){return !/^(The|This|That|These|Those|It|They|A|An|And|But|For|When|Where|Why|How|What|If|In|On|At|To|Of|As|Is|Are)$/.test(w);});
    var hasEntity=(kw && lc.indexOf(kw)>=0) || propers.length>=2;
    var dangling=0; sentences.forEach(function(s){ if(DANG.test(s.trim())) dangling++; });
    var vague=VAGUE.test(txt);
    var explicit=/\b(20\d{2}|Q[1-4]\b|January|February|March|April|May|June|July|August|September|October|November|December)\b/.test(txt);
    var nums=(txt.match(/\b\d+(\.\d+)?%?\b|\$\d/g)||[]).length;
    var frontLoaded=/\d/.test(first) || (kw && first.toLowerCase().indexOf(kw)>=0) || propers.some(function(p){return first.indexOf(p)>=0;});
    var pts=0;
    pts += hasEntity?30:0;
    pts += dangling===0?24:(dangling===1?11:0);
    pts += (vague && !explicit)?0:16;
    pts += nums>=1?15:0;
    pts += frontLoaded?15:0;
    var issues=[];
    if(!hasEntity) issues.push('never names its subject');
    if(dangling) issues.push(dangling+' dangling reference'+(dangling>1?'s':'')+' (“it”, “this”...)');
    if(vague && !explicit) issues.push('vague time anchor, no explicit date');
    if(nums<1) issues.push('no concrete numbers or specifics');
    if(!frontLoaded) issues.push('answer not front-loaded');
    return {score:Math.round(pts),issues:issues};
  }
  function run(){
    var kw=(kwEl.value||'').trim().toLowerCase();
    var text=toText(ta.value||'');
    var S=document.getElementById('craStats'), C=document.getElementById('craChunks');
    if(!text.trim()){S.innerHTML='';C.innerHTML='';return;}
    var chunks=chunkize(text);
    var scored=chunks.map(function(c){var r=scoreChunk(c,kw); r.text=c; return r;});
    var orph=scored.filter(function(s){return s.score<45;}).length;
    var atrisk=scored.filter(function(s){return s.score>=45&&s.score<70;}).length;
    var avg=Math.round(scored.reduce(function(a,b){return a+b.score;},0)/scored.length);
    S.innerHTML=''
     +'<div class="lt-stat"><div class="n">'+scored.length+'</div><div class="k">passages</div></div>'
     +'<div class="lt-stat"><div class="n '+(orph?'warn':'good')+'">'+orph+'</div><div class="k">orphaned (&lt;45)</div></div>'
     +'<div class="lt-stat"><div class="n">'+atrisk+'</div><div class="k">at risk (45-69)</div></div>'
     +'<div class="lt-stat"><div class="n '+(avg>=70?'good':avg>=45?'':'warn')+'">'+avg+'</div><div class="k">avg score / 100</div></div>';
    C.innerHTML=scored.map(function(s,i){
      var vd=s.score>=70?'good':(s.score>=45?'warn':'bad');
      var lab=vd==='good'?'retrievable':(vd==='warn'?'at risk':'orphaned');
      var ex=s.text.slice(0,110).replace(/</g,'&lt;')+(s.text.length>110?'...':'');
      return '<div class="metric" style="margin-bottom:9px"><div class="metric-top"><span class="metric-name">Passage '+(i+1)+' <span style="color:rgba(255,255,255,.4);font-weight:400">'+s.text.split(" ").length+' words &middot; '+s.score+'/100</span></span><span class="verdict '+vd+'">'+lab+'</span></div>'
        +'<div class="metric-fix" style="margin-top:8px;color:rgba(255,255,255,.4);font-style:italic">“'+ex+'”</div>'
        +(s.issues.length?'<div class="metric-fix" style="margin-top:6px"><b>Fix:</b> '+s.issues.join('; ')+'.</div>':'<div class="metric-fix" style="margin-top:6px;color:var(--up)">Self-contained. Reads fine alone.</div>')+'</div>';
    }).join('');
  }
  ta.addEventListener('input',run); kwEl.addEventListener('input',run); run();
})();
</script>'''

# ================================================= TOOL 2: READINESS CHECKLIST
c_body='''<section class="card" id="rrc">
  <div class="grid score">
    <div class="controls" id="rrcItems"></div>
    <div class="panel-out">
      <div class="o-eyebrow">Retrieval readiness</div>
      <div class="scorewrap"><span class="score" id="rrcScore">0</span><span class="score-d">/100</span></div>
      <span class="scoreband" id="rrcBand" style="background:rgba(255,255,255,.1);color:#fff">Answer the checks</span>
      <div class="gauge"><div class="gfill" id="rrcFill" style="width:0%;background:var(--signal)"></div></div>
      <div class="gscale"><span>At risk</span><span>Survivable</span><span>Citable</span></div>
      <div class="gaps"><div class="gaps-h">Biggest gaps</div><div id="rrcGaps"></div></div>
    </div>
  </div>
</section>'''
c_method=('<section class="method"><h2>What it scores</h2>'
  '<p>Every AI engine splits your page into passages and scores each one alone. This checklist is the pre-publish version of that test, eight properties that decide whether a passage survives chunking, retrieval and reranking. Each maps to a specific failure mode: unnamed subjects and dangling pronouns cause vector drift; buried answers lose the reranker; renamed categories cause lexical mismatch.</p>'
  '<p>Score a single article honestly. The lowest items are your biggest gaps.</p>'
  '<div class="srcs"><a href="/blogs/how-your-page-gets-retrieved">How your page gets retrieved &rarr;</a><a href="/tools/chunk-retrievability-analyzer">Chunk Retrievability Analyzer &rarr;</a></div></section>')
c_script=r'''<script>
(function(){
  var root=document.getElementById('rrc'); if(!root) return;
  var ITEMS=[
    ['Section independence','Every H2 section makes full sense read alone, with no prior paragraph.','Write each section as a standalone answer; do not lean on the paragraph above.'],
    ['Entity naming','The subject is named by name at least once inside every section.','Replace “it” / “the platform” with the actual noun once per section.'],
    ['Temporal anchors','Dates and periods are stated explicitly, never “last year”.','State the year or quarter in the sentence, not by reference.'],
    ['Answer position','The core claim appears in the first two sentences of the section.','Front-load the answer, then support it.'],
    ['Vocabulary match','Uses the literal category, competitor and version terms buyers type.','Add the unglamorous exact terms; drop clever renames of known categories.'],
    ['Markup integrity','Real H2 / H3 tags in a clean, consistent hierarchy.','Use heading tags, not bold text pretending to be headings.'],
    ['Table framing','A one-line summary above each table; subjects repeated in row labels.','Make tables self-describing so a severed fragment still carries meaning.'],
    ['Specificity','Concrete numbers and named entities, not general characterisation.','Add the figures, dates and names; vague content is unciteable.']
  ];
  var state={};
  document.getElementById('rrcItems').innerHTML='<div class="cat"><div class="cat-h">Pre-publish checklist<span id="rrcDone"></span></div>'
    + ITEMS.map(function(it,i){ state[i]=null;
      return '<div class="item"><span class="iname">'+it[0]+'</span><span class="iseg" data-k="'+i+'"><button data-m="1" type="button">Yes</button><button data-m="0.5" type="button">Partial</button><button data-m="0" type="button">No</button></span></div>';
    }).join('')+'</div>';
  function compute(){
    var vals=Object.keys(state).map(function(k){return state[k];}).filter(function(x){return x!==null;});
    var total=ITEMS.length, sum=vals.reduce(function(a,b){return a+b;},0);
    var score=Math.round((sum/total)*100);
    document.getElementById('rrcScore').textContent=score;
    document.getElementById('rrcFill').style.width=score+'%';
    var b=score>=80?['Citable','var(--up)']:score>=55?['Survivable','#D4A34A']:['At risk','var(--signal)'];
    var band=document.getElementById('rrcBand'); band.textContent=b[0]; band.style.background='transparent'; band.style.color=b[1]; band.style.border='1px solid '+b[1];
    document.getElementById('rrcFill').style.background=b[1];
    document.getElementById('rrcDone').textContent=vals.length+'/'+total;
    var gaps=Object.keys(state).filter(function(k){return state[k]!==null&&state[k]<1;}).sort(function(a,b){return state[a]-state[b];}).slice(0,5);
    document.getElementById('rrcGaps').innerHTML=gaps.length?gaps.map(function(k,i){
      return '<div class="gap"><span class="rk">'+(i+1)+'</span><span style="flex:1"><span class="gt">'+ITEMS[k][0]+'</span><span class="ga">'+ITEMS[k][2]+'</span></span><span class="pts">'+(state[k]===0?'+full':'+half')+'</span></div>';
    }).join(''):'<div class="allset">No gaps flagged. Your passages should survive the cut.</div>';
  }
  root.addEventListener('click',function(e){var b=e.target.closest('.iseg button'); if(!b)return;
    var seg=b.closest('.iseg'), k=seg.getAttribute('data-k');
    seg.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});
    b.classList.add('sel'); state[k]=parseFloat(b.getAttribute('data-m')); compute();});
  compute();
})();
</script>'''

# ================================================= TOOL 3: RRF CALCULATOR
r_body='''<section class="card" id="rrf">
  <div class="grid calc">
    <div class="controls">
      <div class="num-grid">
        <div class="fld"><div class="lab">Dense weight</div><input class="tin" id="rrfWd" value="0.8"></div>
        <div class="fld"><div class="lab">Keyword weight</div><input class="tin" id="rrfWs" value="0.2"></div>
        <div class="fld"><div class="lab">k (smoothing)</div><input class="tin" id="rrfK" value="60"></div>
      </div>
      <div class="fld"><div class="lab">Dense ranking <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">one item per line, best first</span></div>
        <textarea class="ta" id="rrfDense" style="min-height:150px" placeholder="chunk-A&#10;chunk-C&#10;chunk-B"></textarea></div>
      <div class="fld"><div class="lab">Keyword (BM25) ranking <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">one item per line, best first</span></div>
        <textarea class="ta" id="rrfSparse" style="min-height:150px" placeholder="chunk-B&#10;chunk-A&#10;chunk-D"></textarea>
        <p class="hint">Reciprocal Rank Fusion throws away raw scores and merges on rank alone: each list adds weight / (k + rank). The winner is usually good on both, not best on either.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Fused ranking</div>
      <div id="rrfOut" style="margin-top:12px"></div>
      <p class="caveat">Production stacks commonly weight dense 0.8 and keyword 0.2 with k=60. Items appearing in only one list still score, but rarely beat items ranked respectably in both.</p>
    </div>
  </div>
</section>'''
r_method=('<section class="method"><h2>How fusion works</h2>'
  '<p>Dense cosine scores are bounded; BM25 scores are unbounded, so you cannot average them. Reciprocal Rank Fusion sidesteps it by operating on rank positions alone: each system contributes <strong>weight / (k + rank)</strong> for every candidate, with k usually 60. The smoothing constant stops one pipeline’s top result from dominating, so the chunks that win rank respectably in both lists.</p>'
  '<p>Paste two rankings to see the merged order, and why “good on both” beats “best on one”.</p>'
  '<div class="srcs"><a href="/blogs/how-your-page-gets-retrieved">How your page gets retrieved &rarr;</a><a href="/blogs/internal-linking-for-ai-retrieval">Internal linking for AI retrieval &rarr;</a></div></section>')
r_script=r'''<script>
(function(){
  var root=document.getElementById('rrf'); if(!root) return;
  function lines(id){return (document.getElementById(id).value||'').split(/\r?\n/).map(function(s){return s.trim();}).filter(Boolean);}
  function num(id,d){var v=parseFloat(document.getElementById(id).value); return isFinite(v)?v:d;}
  function run(){
    var K=num('rrfK',60), wd=num('rrfWd',0.8), ws=num('rrfWs',0.2);
    var dense=lines('rrfDense'), sparse=lines('rrfSparse');
    var scores={}, dr={}, sr={};
    dense.forEach(function(id,i){scores[id]=(scores[id]||0)+wd/(K+i+1); dr[id]=i+1;});
    sparse.forEach(function(id,i){scores[id]=(scores[id]||0)+ws/(K+i+1); sr[id]=i+1;});
    var ids=Object.keys(scores);
    var out=document.getElementById('rrfOut');
    if(!ids.length){out.innerHTML='';return;}
    ids.sort(function(a,b){return scores[b]-scores[a];});
    var rows=ids.map(function(id,i){
      return '<tr><td class="up">'+(i+1)+'</td><td class="label">'+id.replace(/</g,'&lt;')+'</td><td>'+(dr[id]||'—')+'</td><td>'+(sr[id]||'—')+'</td><td>'+scores[id].toFixed(4)+'</td></tr>';
    }).join('');
    out.innerHTML='<div class="tt-wrap" style="margin:0"><table class="tt"><thead><tr><th>Rank</th><th>Item</th><th>Dense</th><th>Keyword</th><th>RRF score</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  }
  ['rrfWd','rrfWs','rrfK','rrfDense','rrfSparse'].forEach(function(id){document.getElementById(id).addEventListener('input',run);});
  run();
})();
</script>'''

page("chunk-retrievability-analyzer","Chunk Retrievability Analyzer &middot; Free GEO Tool &middot; rawmktg.",
  "Paste a page to see how a retriever splits it into passages, then score each chunk in isolation and flag the orphaned ones that never name their own subject.",
  "Free Tool &middot; Analyzer","Chunk Retrievability Analyzer",
  "See your page the way a retriever does: split into passages, each scored alone. Flags orphaned chunks, dangling pronouns, vague dates and buried answers.",
  a_body,a_method,a_script)
page("retrieval-readiness-checklist","Retrieval-Readiness Checklist &middot; Free GEO Tool &middot; rawmktg.",
  "Score an article against the eight properties that decide whether its passages survive chunking, retrieval and reranking, with your biggest gaps ranked.",
  "Free Tool &middot; Diagnostic","Retrieval-Readiness Checklist",
  "Score a page against the eight-point pre-publish checklist for surviving chunking and reranking, and get your biggest gaps ranked.",
  c_body,c_method,c_script)
page("rrf-rank-fusion-calculator","RRF Rank-Fusion Calculator &middot; Free GEO Tool &middot; rawmktg.",
  "Enter a dense ranking and a keyword (BM25) ranking and see the Reciprocal Rank Fusion merge with k=60, why good-on-both beats best-on-one.",
  "Free Tool &middot; Calculator","RRF Rank-Fusion Calculator",
  "Merge a dense ranking and a keyword ranking with Reciprocal Rank Fusion and see why the chunk that wins is good on both, not best on either.",
  r_body,r_method,r_script)

allok=True
for slug in ["chunk-retrievability-analyzer","retrieval-readiness-checklist","rrf-rank-fusion-calculator"]:
    hh=open(f"tools/{slug}.html").read()
    js=re.findall(r'<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', hh, re.S)[-1][8:-9]
    open("/tmp/rt.js","w").write(js)
    r=subprocess.run(["node","--check","/tmp/rt.js"],capture_output=True,text=True)
    print(slug,"| NODE:","OK" if r.returncode==0 else "FAIL "+r.stderr[:300],"| jsonld:",hh.count("application/ld+json"),"| bytes:",len(hh))
    if r.returncode!=0: allok=False
print("ALL OK" if allok else "FAILURES")
