#!/usr/bin/env python3
"""SCRATCH: build 4 llms.txt tool pages under /tools. Do NOT commit as content."""
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

# ============================================================ TOOL 1: GENERATOR
g_body='''<section class="card" id="gen">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Brand or project name <span class="val" style="color:rgba(255,255,255,.5)">the single H1</span></div>
        <input class="tin" id="gName" placeholder="Acme Payments"></div>
      <div class="fld"><div class="lab">One-line summary <span class="val" style="color:rgba(255,255,255,.5)">blockquote</span></div>
        <input class="tin" id="gSum" placeholder="Acme Payments is a B2B payment API for marketplaces: split payouts, escrow, KYC."></div>
      <div class="fld"><div class="lab">Processing instruction <span class="val" style="color:rgba(255,255,255,.5)">optional</span></div>
        <input class="tin" id="gInstr" placeholder="Fetch the API Reference before generating code. v4 differs from v3."></div>
      <div class="fld"><div class="lab">Links</div>
        <div id="gLinks"></div>
        <div class="btn-row"><button class="tbtn" id="gAdd" type="button">+ Add link</button></div>
        <p class="hint">Group links by section. Anything in a section named "Optional" is marked low-priority, an agent on a tight context budget may drop it. Write descriptions with real facts (versions, limits, retry counts).</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Your llms.txt</div>
      <div class="codeout" style="margin:12px 0 0"><div class="code-block"><pre id="gOut">#</pre></div></div>
      <div class="btn-row"><button class="tbtn primary" id="gCopy" type="button">Copy</button><button class="tbtn" id="gDl" type="button">Download llms.txt</button></div>
      <p class="caveat">Spec-compliant output: one H1, a third-person blockquote, sectioned links in - [Title](URL): Description format. Runs entirely in your browser, nothing is uploaded.</p>
    </div>
  </div>
</section>'''
g_method=('<section class="method"><h2>How to use it</h2>'
  '<p>llms.txt is a curated Markdown index at your domain root that tells a coding agent where your best docs live. The value is in the <strong>descriptions</strong>: pack them with concrete facts so an agent can often answer without a second fetch. Keep sections broad (four good ones beat twenty), and reserve <strong>Optional</strong> for changelogs and deprecated guides, never your core API reference.</p>'
  '<p>This generator enforces the structural rules; validate an existing file with the linter, and read the evidence on where the file actually helps.</p>'
  '<div class="srcs"><a href="/blogs/does-llms-txt-do-anything-yet">Does llms.txt do anything yet? &rarr;</a><a href="/tools/llms-txt-validator">llms.txt Validator &rarr;</a><a href="/tools/robots-txt-ai-generator">robots.txt for AI &rarr;</a></div></section>')
g_script=r'''<script>
(function(){
  var root=document.getElementById('gen'); if(!root) return;
  var SECTIONS=['Core Documentation','API Reference','Integrations','Guides','Pricing','Optional'];
  var seed=[
    {sec:'Core Documentation',t:'Quickstart',u:'https://acme.dev/docs/quickstart.md',d:'Install the SDK, authenticate with a test key, process a first payment.'},
    {sec:'API Reference',t:'Payments API',u:'https://acme.dev/docs/api/payments.md',d:'All v4 /payments endpoints, request/response schemas, error codes.'},
    {sec:'Optional',t:'Changelog',u:'https://acme.dev/docs/changelog.md',d:'Release history. Safe to skip unless debugging a version mismatch.'}
  ];
  var wrap=document.getElementById('gLinks');
  function opts(v){return SECTIONS.map(function(s){return '<option'+(s===v?' selected':'')+'>'+s+'</option>';}).join('');}
  function row(l){
    l=l||{sec:'Core Documentation',t:'',u:'',d:''};
    var el=document.createElement('div'); el.className='lrow';
    el.innerHTML='<div class="lrow-top"><select class="tin sec" style="max-width:190px">'+opts(l.sec)+'</select><button class="rm-x" type="button" aria-label="Remove link">&times;</button></div>'
      +'<div class="lrow-grid"><input class="tin t" placeholder="Title" value="'+esc(l.t)+'"><input class="tin u" placeholder="https://...md" value="'+esc(l.u)+'"><input class="tin d full" placeholder="Description with concrete facts" value="'+esc(l.d)+'"></div>';
    el.querySelector('.rm-x').addEventListener('click',function(){el.remove();build();});
    el.querySelectorAll('input,select').forEach(function(i){i.addEventListener('input',build);});
    wrap.appendChild(el);
  }
  function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
  function build(){
    var name=(document.getElementById('gName').value||'').trim()||'Your Product';
    var sum=(document.getElementById('gSum').value||'').trim();
    var instr=(document.getElementById('gInstr').value||'').trim();
    var rows=[].slice.call(wrap.querySelectorAll('.lrow')).map(function(r){
      return {sec:r.querySelector('.sec').value,t:r.querySelector('.t').value.trim(),u:r.querySelector('.u').value.trim(),d:r.querySelector('.d').value.trim()};
    }).filter(function(r){return r.t||r.u;});
    var order=[]; rows.forEach(function(r){if(order.indexOf(r.sec)<0)order.push(r.sec);});
    order.sort(function(a,b){var ao=/^optional$/i.test(a)?1:0, bo=/^optional$/i.test(b)?1:0; return ao-bo;});
    var out='# '+name+'\n';
    if(sum){out+='\n> '+sum+'\n';}
    if(instr){out+='\n'+instr+'\n';}
    order.forEach(function(sec){
      out+='\n## '+sec+'\n';
      rows.filter(function(r){return r.sec===sec;}).forEach(function(r){
        var title=r.t||'Untitled', url=r.u||'https://example.com/page.md', desc=r.d||'';
        out+='- ['+title+']('+url+')'+(desc?': '+desc:'')+'\n';
      });
    });
    document.getElementById('gOut').textContent=out.replace(/\n+$/,'\n');
  }
  document.getElementById('gAdd').addEventListener('click',function(){row();build();});
  ['gName','gSum','gInstr'].forEach(function(id){document.getElementById(id).addEventListener('input',build);});
  document.getElementById('gCopy').addEventListener('click',function(){var b=this,t=document.getElementById('gOut').textContent;
    function done(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,done);}else{done();}});
  document.getElementById('gDl').addEventListener('click',function(){var t=document.getElementById('gOut').textContent;
    var blob=new Blob([t],{type:'text/markdown'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='llms.txt';document.body.appendChild(a);a.click();document.body.removeChild(a);});
  seed.forEach(row); build();
})();
</script>'''

# ============================================================ TOOL 2: LOG ANALYZER
la_body='''<section class="card" id="log">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Paste your access log</div>
        <textarea class="ta" id="logIn" placeholder="Paste raw nginx/Apache access-log lines (combined log format). Nothing is uploaded, parsing runs in your browser."></textarea>
        <p class="hint">Works with standard combined log format. It detects named AI user agents, tallies status codes, and flags 403/429s hitting your citation bots, the silent cause of missing AI citations.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">AI bot traffic</div>
      <div class="lt-stats" id="logStats" style="margin-top:12px"></div>
      <div id="logAgents"></div>
      <div class="flags" id="logFlags" style="margin-top:14px"></div>
      <p class="caveat">Heuristic parse of user-agent and status fields. Citation bots blocked with 403/429 lose you visibility no llms.txt can recover, fix those first.</p>
    </div>
  </div>
</section>'''
la_method=('<section class="method"><h2>What it checks</h2>'
  '<p>Across one 515-million-event dataset, only <strong>408</strong> requests ever touched /llms.txt. The requests that matter, and that are often silently blocked, are the citation crawlers: OAI-SearchBot, PerplexityBot, Claude-SearchBot, Googlebot. This tool tallies your AI-bot traffic, shows the status codes each agent receives, and raises a flag when a citation bot is getting 403s or 429s.</p>'
  '<p>It runs entirely in your browser. Paste a representative slice of your access log for the clearest read.</p>'
  '<div class="srcs"><a href="/blogs/does-llms-txt-do-anything-yet">Does llms.txt do anything yet? &rarr;</a><a href="/blogs/how-ai-crawlers-index-your-site">How AI crawlers index your site &rarr;</a></div></section>')
la_script=r'''<script>
(function(){
  var root=document.getElementById('log'); if(!root) return;
  var ta=document.getElementById('logIn');
  var AGENTS=['OAI-SearchBot','ChatGPT-User','Claude-SearchBot','ClaudeBot','PerplexityBot','Perplexity-User','GPTBot','Google-Extended','Googlebot','Applebot-Extended','Amazonbot','Bytespider','CCBot','meta-externalagent'];
  var CITATION={'OAI-SearchBot':1,'PerplexityBot':1,'Claude-SearchBot':1,'Googlebot':1,'Perplexity-User':1,'ChatGPT-User':1};
  function agentOf(line){var low=line.toLowerCase();for(var i=0;i<AGENTS.length;i++){if(low.indexOf(AGENTS[i].toLowerCase())>=0)return AGENTS[i];}return null;}
  function statusOf(line){var m=line.match(/"\s+(\d{3})\s/); if(m) return m[1];
    m=line.match(/"[A-Z]+\s[^"]*"\s(\d{3})/); if(m) return m[1];
    m=line.match(/\s(\d{3})\s\d+\s/); return m?m[1]:null;}
  function pathOf(line){var m=line.match(/"[A-Z]+\s(\S+)\s+HTTP/); return m?m[1]:'';}
  function run(){
    var lines=(ta.value||'').split(/\r?\n/).filter(function(l){return l.trim();});
    var stats={total:0,llms:0,blocked403:0,blocked429:0};
    var byAgent={};
    lines.forEach(function(ln){
      var a=agentOf(ln); if(!a) return;
      stats.total++;
      var st=statusOf(ln)||'---', pth=pathOf(ln);
      if(pth.indexOf('/llms.txt')===0||pth.indexOf('/llms-full.txt')===0) stats.llms++;
      if(!byAgent[a]) byAgent[a]={n:0,st:{},cit:CITATION[a]?1:0};
      byAgent[a].n++; byAgent[a].st[st]=(byAgent[a].st[st]||0)+1;
      if(CITATION[a]&&st==='403') stats.blocked403++;
      if(CITATION[a]&&st==='429') stats.blocked429++;
    });
    var S=document.getElementById('logStats');
    if(!stats.total){S.innerHTML='';document.getElementById('logAgents').innerHTML='';document.getElementById('logFlags').innerHTML='<div class="flag">Paste log lines to analyze.</div>';return;}
    S.innerHTML=''
     +'<div class="lt-stat"><div class="n">'+stats.total.toLocaleString()+'</div><div class="k">AI bot requests</div></div>'
     +'<div class="lt-stat"><div class="n'+(stats.llms?'':'')+'">'+stats.llms.toLocaleString()+'</div><div class="k">hits to /llms.txt</div></div>'
     +'<div class="lt-stat"><div class="n '+(stats.blocked403?'warn':'good')+'">'+stats.blocked403+'</div><div class="k">403s to citation bots</div></div>'
     +'<div class="lt-stat"><div class="n '+(stats.blocked429?'warn':'good')+'">'+stats.blocked429+'</div><div class="k">429s to citation bots</div></div>';
    var names=Object.keys(byAgent).sort(function(a,b){return byAgent[b].n-byAgent[a].n;});
    document.getElementById('logAgents').innerHTML=names.map(function(a){
      var d=byAgent[a]; var bad=(d.st['403']||0)+(d.st['429']||0);
      var codes=Object.keys(d.st).sort().map(function(c){return c+'×'+d.st[c];}).join('  ');
      var tag = d.cit ? (bad? '<span class="as blocked">'+bad+' blocked</span>':'<span class="as ok">reaching</span>') : '';
      return '<div class="agrow"><span class="an">'+a+'<br><span style="color:rgba(255,255,255,.4);font-size:10px">'+codes+'</span></span>'+tag+'<span class="ac">'+d.n+'</span></div>';
    }).join('');
    var flags=[];
    if(stats.blocked403||stats.blocked429){flags.push('<div class="flag">Citation bots are being blocked ('+(stats.blocked403+stats.blocked429)+' 403/429 responses). Your WAF or rate limiter is a direct, usually invisible cause of missing AI citations, fix this before anything else.</div>');}
    else{flags.push('<div class="flag ok">No citation bots are being blocked in this sample. Good.</div>');}
    if(stats.llms===0){flags.push('<div class="flag">Zero requests to /llms.txt in this sample, consistent with the data that public search crawlers bypass the file. Focus on crawlable HTML and clean status codes.</div>');}
    document.getElementById('logFlags').innerHTML=flags.join('');
  }
  ta.addEventListener('input',run); run();
})();
</script>'''

# ============================================================ TOOL 3: VALIDATOR
v_body='''<section class="card" id="val">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Paste your llms.txt</div>
        <textarea class="ta" id="valIn" placeholder="Paste the contents of your llms.txt file. Nothing is uploaded, validation runs in your browser."></textarea>
        <p class="hint">Checks the seven structural rules plus description quality. It cannot verify the file's live MIME type or 200 status, confirm those on your server.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Spec compliance</div>
      <div class="o-lift" id="valScore">0</div>
      <div class="o-sub" id="valSub">paste a file to validate</div>
      <div class="metrics" id="valMetrics"></div>
      <p class="caveat">Structural linter based on the llms.txt spec: single H1, third-person blockquote, broad H2 sections, and the mandatory - [Title](URL): Description syntax.</p>
    </div>
  </div>
</section>'''
v_method=('<section class="method"><h2>The rules it enforces</h2>'
  '<p>A valid llms.txt parses the same way every time: exactly one <strong>#</strong> H1 (your entity name, no tagline), a <strong>&gt;</strong> blockquote summary right after it, resources under broad <strong>##</strong> sections, and every link as <code>- [Title](URL): Description</code> with the mandatory colon. Descriptions should carry real facts, generic ones waste the format.</p>'
  '<p>Build a compliant file with the generator, then confirm your server returns it as text/markdown with a 200.</p>'
  '<div class="srcs"><a href="/tools/llms-txt-generator">llms.txt Generator &rarr;</a><a href="/blogs/does-llms-txt-do-anything-yet">Read the log evidence &rarr;</a></div></section>')
v_script=r'''<script>
(function(){
  var root=document.getElementById('val'); if(!root) return;
  var ta=document.getElementById('valIn');
  function run(){
    var raw=(ta.value||''); var lines=raw.split(/\r?\n/);
    var out=document.getElementById('valMetrics');
    if(!raw.trim()){document.getElementById('valScore').textContent='0';document.getElementById('valSub').textContent='paste a file to validate';out.innerHTML='';return;}
    var h1=lines.filter(function(l){return /^#\s+\S/.test(l);});
    var h2=lines.filter(function(l){return /^##\s+\S/.test(l);});
    var bq=lines.filter(function(l){return /^>\s*\S/.test(l);});
    var h1idx=lines.findIndex(function(l){return /^#\s+\S/.test(l);});
    var bqidx=lines.findIndex(function(l){return /^>\s*\S/.test(l);});
    var linkLines=lines.filter(function(l){return /^\s*-\s*\[/.test(l);});
    var goodLink=/^\s*-\s*\[[^\]]+\]\((https?:\/\/|\/)[^)]+\)\s*:\s*\S/;
    var okLinks=linkLines.filter(function(l){return goodLink.test(l);});
    var badLinks=linkLines.filter(function(l){return !goodLink.test(l);});
    var weak=okLinks.filter(function(l){var d=(l.split('):').slice(1).join('):')||'').trim();return d.split(/\s+/).length<5||/^(information about|learn more|details|docs|info)\b/i.test(d);});
    var h1txt=h1.length?h1[0].replace(/^#\s+/,'').trim():'';
    var h1words=h1txt?h1txt.split(/\s+/).length:0;
    var optIdx=lines.findIndex(function(l){return /^##\s+optional\b/i.test(l);});
    var coreUnderOpt=false;
    if(optIdx>=0){for(var i=optIdx+1;i<lines.length;i++){if(/^##\s/.test(lines[i]))break;if(/\/(api|reference|auth)/i.test(lines[i])&&/^\s*-\s*\[/.test(lines[i]))coreUnderOpt=true;}}
    function m(name,val,pass,fix){return {n:name,v:val,p:pass,f:fix};}
    var M=[
      m('Single H1 (entity name)', h1.length===1?1:0, h1.length===1, h1.length===0?'Add exactly one # header with your product or org name.':h1.length>1?'You have '+h1.length+' H1 lines, keep exactly one.':''),
      m('H1 is a name, not a tagline', (h1words&&h1words<=6)?1:(h1words?0.5:0), h1words>0&&h1words<=6, h1words>6?'Your H1 has '+h1words+' words. Use just the name, marketing slogans corrupt entity resolution.':'Add the H1 first.'),
      m('Blockquote summary', bq.length? (bqidx===h1idx+1||bqidx<=h1idx+2?1:0.5):0, bq.length>0, bq.length===0?'Add a > blockquote (third person) right after the H1.':bqidx>h1idx+2?'Move the > blockquote to immediately after the H1.':''),
      m('Has ## sections', h2.length>=1?1:0, h2.length>=1, h2.length===0?'Group your links under ## section headers (Core Documentation, API Reference...).':''),
      m('Broad, not deep sectioning', h2.length? (h2.length<=7?1:0.5):0, h2.length>=1&&h2.length<=7, h2.length>7?'You have '+h2.length+' sections, agents parse 4-7 broad ones more efficiently.':''),
      m('Valid link syntax', linkLines.length? okLinks.length/linkLines.length : 0, badLinks.length===0&&linkLines.length>0, linkLines.length===0?'Add links as - [Title](URL): Description.':badLinks.length?badLinks.length+' link(s) miss the mandatory colon or a description.':''),
      m('Descriptions carry facts', okLinks.length? 1-(weak.length/okLinks.length) : 0, weak.length===0&&okLinks.length>0, weak.length?weak.length+' description(s) are thin or generic. Add versions, limits, retry counts.':'Add fact-rich descriptions.'),
      m('Optional used correctly', optIdx<0?1:(coreUnderOpt?0:1), !coreUnderOpt, coreUnderOpt?'You placed API/reference links under ## Optional, agents may drop them. Move core docs out of Optional.':'')
    ];
    var W=[16,10,14,12,8,20,12,8], score=0; M.forEach(function(x,i){score+=x.v*W[i];}); score=Math.round(score);
    document.getElementById('valScore').textContent=score;
    document.getElementById('valSub').textContent=(score>=80?'spec-compliant':(score>=55?'needs work':'invalid'))+' · '+linkLines.length+' links · '+h2.length+' sections';
    out.innerHTML=M.map(function(x){var v=Math.round(x.v*100);var vd=x.p?'good':(x.v>=0.5?'warn':'bad');
      return '<div class="metric"><div class="metric-top"><span class="metric-name">'+x.n+'</span><span class="verdict '+vd+'">'+(vd==='good'?'pass':vd==='warn'?'warn':'fail')+'</span></div>'
        +'<div class="metric-bar"><i style="width:'+v+'%"></i></div>'+(x.f?'<div class="metric-fix">'+x.f+'</div>':'')+'</div>';}).join('');
  }
  ta.addEventListener('input',run); run();
})();
</script>'''

# ============================================================ TOOL 4: ROBOTS
r_body='''<section class="card" id="rob">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Site domain <span class="val" style="color:rgba(255,255,255,.5)">for the sitemap line</span></div>
        <input class="tin" id="rDomain" placeholder="example.com"></div>
      <div class="fld"><div class="lab">AI search &amp; citation crawlers <span class="val" style="color:var(--up)">keep allowed</span></div>
        <div id="rSearch"></div></div>
      <div class="fld"><div class="lab">Foundation-model training crawlers <span class="val" style="color:rgba(255,255,255,.5)">your call</span></div>
        <div id="rTrain"></div>
        <p class="hint">Keeping citation and training permissions separate is the point: it is how brands avoid accidentally opting out of being cited while trying to opt out of being trained on. Toggle on = Allow, off = Disallow.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Your robots.txt</div>
      <div class="codeout" style="margin:12px 0 0"><div class="code-block"><pre id="rOut">#</pre></div></div>
      <div class="btn-row"><button class="tbtn primary" id="rCopy" type="button">Copy</button><button class="tbtn" id="rDl" type="button">Download robots.txt</button></div>
      <p class="caveat">Directives follow each vendor's published user-agent tokens. robots.txt is honoured by convention, not enforced, verify with your logs.</p>
    </div>
  </div>
</section>'''
r_method=('<section class="method"><h2>Why two lists</h2>'
  '<p>Search/citation crawlers (OAI-SearchBot, Claude-SearchBot, PerplexityBot) are how AI answers cite you, you almost always want them <strong>allowed</strong>. Training crawlers (GPTBot, ClaudeBot, Google-Extended, CCBot) harvest data for model training, a separate decision. Conflating them is how companies accidentally disappear from citations while trying to opt out of training.</p>'
  '<p>After deploying, confirm nothing else (a WAF, a CDN rule) is silently blocking the bots you just allowed.</p>'
  '<div class="srcs"><a href="/tools/ai-bot-log-analyzer">AI Bot Log Analyzer &rarr;</a><a href="/blogs/how-ai-crawlers-index-your-site">How AI crawlers index your site &rarr;</a></div></section>')
r_script=r'''<script>
(function(){
  var root=document.getElementById('rob'); if(!root) return;
  var SEARCH=[['OAI-SearchBot',1],['Claude-SearchBot',1],['PerplexityBot',1],['ChatGPT-User',1],['Perplexity-User',1]];
  var TRAIN=[['GPTBot',0],['ClaudeBot',0],['Google-Extended',0],['CCBot',0],['Bytespider',0],['Applebot-Extended',0],['meta-externalagent',0]];
  function render(list,host){document.getElementById(host).innerHTML=list.map(function(a,i){
    return '<div class="tactic'+(a[1]?'':' off')+'" data-a="'+a[0]+'"><div class="trow"><span class="tname">'+a[0]+'</span><span class="band">'+(a[1]?'Allow':'Disallow')+'</span><button class="switch'+(a[1]?' on':'')+'" type="button" aria-label="Toggle"></button></div></div>';
  }).join('');}
  render(SEARCH,'rSearch'); render(TRAIN,'rTrain');
  function build(){
    var dom=(document.getElementById('rDomain').value||'').trim().replace(/^https?:\/\//,'').replace(/\/.*$/,'');
    var out='';
    function block(title,host){out+='# '+title+'\n';
      [].slice.call(document.getElementById(host).querySelectorAll('.tactic')).forEach(function(t){
        var on=t.querySelector('.switch').classList.contains('on');
        out+='User-agent: '+t.getAttribute('data-a')+'\n'+(on?'Allow: /':'Disallow: /')+'\n\n';
      });
    }
    block('AI search & citation crawlers','rSearch');
    block('Foundation-model training crawlers','rTrain');
    out+='Sitemap: https://'+(dom||'example.com')+'/sitemap.xml\n';
    document.getElementById('rOut').textContent=out;
  }
  root.addEventListener('click',function(e){var b=e.target.closest('.switch'); if(!b)return;
    var t=b.closest('.tactic'); var on=b.classList.toggle('on'); t.classList.toggle('off',!on);
    t.querySelector('.band').textContent=on?'Allow':'Disallow'; build();});
  document.getElementById('rDomain').addEventListener('input',build);
  document.getElementById('rCopy').addEventListener('click',function(){var b=this,t=document.getElementById('rOut').textContent;
    function done(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,done);}else{done();}});
  document.getElementById('rDl').addEventListener('click',function(){var t=document.getElementById('rOut').textContent;
    var blob=new Blob([t],{type:'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='robots.txt';document.body.appendChild(a);a.click();document.body.removeChild(a);});
  build();
})();
</script>'''

page("llms-txt-generator","llms.txt Generator &middot; Free GEO Tool &middot; rawmktg.",
  "Generate a spec-compliant llms.txt file: one H1, a third-person blockquote, and sectioned links in the mandatory - [Title](URL): Description format. Copy or download.",
  "Free Tool &middot; Generator","llms.txt Generator",
  "Build a spec-compliant llms.txt in the browser, single H1, blockquote summary, sectioned links, then copy or download it.",
  g_body,g_method,g_script)
page("ai-bot-log-analyzer","AI Bot Log Analyzer &middot; Free GEO Tool &middot; rawmktg.",
  "Paste your access log to see AI-crawler traffic, per-agent status codes, /llms.txt hits, and 403/429 flags where citation bots are being silently blocked.",
  "Free Tool &middot; Analyzer","AI Bot Log Analyzer",
  "Paste your server access log and see which AI crawlers hit your site, what status codes they get, and whether your citation bots are being blocked.",
  la_body,la_method,la_script)
page("llms-txt-validator","llms.txt Validator &middot; Free GEO Tool &middot; rawmktg.",
  "Paste your llms.txt and check it against the seven structural spec rules plus description quality: single H1, blockquote, broad sections, and correct link syntax.",
  "Free Tool &middot; Validator","llms.txt Validator",
  "Paste your llms.txt and lint it against the spec: single H1, blockquote, broad sections, the mandatory link colon, and fact-rich descriptions.",
  v_body,v_method,v_script)
page("robots-txt-ai-generator","robots.txt for AI Generator &middot; Free GEO Tool &middot; rawmktg.",
  "Generate a robots.txt that keeps AI search and citation crawlers allowed while controlling foundation-model training crawlers, separately. Copy or download.",
  "Free Tool &middot; Generator","robots.txt for AI Generator",
  "Toggle allow/disallow per AI crawler and get a correct robots.txt, keeping citation bots in while controlling training bots, separately.",
  r_body,r_method,r_script)

# node-check each script
import glob
allok=True
for slug in ["llms-txt-generator","ai-bot-log-analyzer","llms-txt-validator","robots-txt-ai-generator"]:
    hh=open(f"tools/{slug}.html").read()
    m=re.findall(r'<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', hh, re.S)
    js=m[-1][8:-9]
    open("/tmp/t.js","w").write(js)
    r=subprocess.run(["node","--check","/tmp/t.js"],capture_output=True,text=True)
    jc=hh.count("application/ld+json")
    print(slug,"| NODE:","OK" if r.returncode==0 else "FAIL "+r.stderr[:300],"| jsonld:",jc,"| bytes:",len(hh))
    if r.returncode!=0: allok=False
print("ALL OK" if allok else "HAD FAILURES")
