#!/usr/bin/env python3
"""SCRATCH: build 4 agentic-commerce tool pages under /tools. Do NOT commit as content."""
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

# ================= TOOL 1: READINESS SCORECARD =================
s_body='''<section class="card" id="acr">
  <div class="grid score">
    <div class="controls" id="acrItems"></div>
    <div class="panel-out">
      <div class="o-eyebrow">Agentic readiness</div>
      <div class="scorewrap"><span class="score" id="acrScore">0</span><span class="score-d">/100</span></div>
      <span class="scoreband" id="acrBand" style="background:rgba(255,255,255,.1);color:#fff">Answer the checks</span>
      <div class="gauge"><div class="gfill" id="acrFill" style="width:0%;background:var(--signal)"></div></div>
      <div class="gscale"><span>At risk</span><span>Emerging</span><span>Agent-ready</span></div>
      <div class="gaps"><div class="gaps-h">Biggest gaps</div><div id="acrGaps"></div></div>
    </div>
  </div>
</section>'''
s_method=('<section class="method"><h2>What it scores</h2>'
  '<p>When the buyer is a bot, your storefront is bypassed and your catalog API becomes the product. This checklist scores the infrastructure that decides whether an agent can even consider you: sub-200ms latency, machine-readable product data, one incentives endpoint, identity linking, and the risk controls that keep you out of trouble.</p>'
  '<p>Answer honestly for one store or catalog. The lowest items are your first quarter of work.</p>'
  '<div class="srcs"><a href="/blogs/when-the-buyer-is-a-bot">When the buyer is a bot &rarr;</a><a href="/tools/product-schema-auditor">Product Schema Auditor &rarr;</a></div></section>')
s_script=r'''<script>
(function(){
  var root=document.getElementById('acr'); if(!root) return;
  var ITEMS=[
    ['Catalog API p95 latency under 200ms','Agents query merchants in parallel and time out slower ones. Profile p95, not average, and cut it below 200ms.'],
    ['Product data is machine-readable JSON-LD','Model your catalog into Schema.org with explicit attribute fields, not HTML description blobs.'],
    ['Real-time inventory and pricing sync','Stale price or stock that fails at checkout gets your domain down-ranked. Use event-driven sync.'],
    ['One unified promotions/incentives endpoint','Agents do not hunt for coupons. Expose every eligible incentive from a single API or you compete on list price.'],
    ['OAuth identity linking enabled','Link the customer account to the agent so you keep tier pricing, loyalty and the relationship (UCP/ACP).'],
    ['MACH architecture','Microservices, API-first, cloud-native, headless. Monoliths deploy AI at roughly half the success rate.'],
    ['Capability profile published or platform-handled','Publish /.well-known/ucp, or confirm your platform (Shopify, commercetools) advertises capabilities for you.'],
    ['Automated-agent clause in your Terms of Service','The legal position on third-party bot access is unsettled. Add the clause now.'],
    ['User-generated content sanitised at ingestion','Strip HTML comments and control sequences before storage; reviews are an executable surface for injection.'],
    ['Content refresh cadence set','AI citations have a ~13-week half-life. Set a cadence and update dateModified in schema.']
  ];
  var state={};
  document.getElementById('acrItems').innerHTML='<div class="cat"><div class="cat-h">Agentic commerce readiness<span id="acrDone"></span></div>'
    + ITEMS.map(function(it,i){ state[i]=null;
      return '<div class="item"><span class="iname">'+it[0]+'</span><span class="iseg" data-k="'+i+'"><button data-m="1" type="button">Yes</button><button data-m="0.5" type="button">Partial</button><button data-m="0" type="button">No</button></span></div>';
    }).join('')+'</div>';
  function compute(){
    var vals=Object.keys(state).map(function(k){return state[k];}).filter(function(x){return x!==null;});
    var total=ITEMS.length, sum=vals.reduce(function(a,b){return a+b;},0);
    var score=Math.round((sum/total)*100);
    document.getElementById('acrScore').textContent=score;
    document.getElementById('acrFill').style.width=score+'%';
    var b=score>=80?['Agent-ready','var(--up)']:score>=55?['Emerging','#D4A34A']:['At risk','var(--signal)'];
    var band=document.getElementById('acrBand'); band.textContent=b[0]; band.style.background='transparent'; band.style.color=b[1]; band.style.border='1px solid '+b[1];
    document.getElementById('acrFill').style.background=b[1];
    document.getElementById('acrDone').textContent=vals.length+'/'+total;
    var gaps=Object.keys(state).filter(function(k){return state[k]!==null&&state[k]<1;}).sort(function(a,b){return state[a]-state[b];}).slice(0,5);
    document.getElementById('acrGaps').innerHTML=gaps.length?gaps.map(function(k,i){
      return '<div class="gap"><span class="rk">'+(i+1)+'</span><span style="flex:1"><span class="gt">'+ITEMS[k][0]+'</span><span class="ga">'+ITEMS[k][1]+'</span></span><span class="pts">'+(state[k]===0?'+full':'+half')+'</span></div>';
    }).join(''):'<div class="allset">No gaps flagged. Your catalog is ready for agent traffic.</div>';
  }
  root.addEventListener('click',function(e){var b=e.target.closest('.iseg button'); if(!b)return;
    var seg=b.closest('.iseg'), k=seg.getAttribute('data-k');
    seg.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});
    b.classList.add('sel'); state[k]=parseFloat(b.getAttribute('data-m')); compute();});
  compute();
})();
</script>'''

# ================= TOOL 2: PRODUCT SCHEMA AUDITOR =================
a_body='''<section class="card" id="psa">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Paste your product page HTML or JSON-LD</div>
        <textarea class="ta" id="psaText" placeholder="Paste the full product page HTML, or just the Product JSON-LD block. Nothing is uploaded, parsing runs in your browser."></textarea>
        <p class="hint">It finds your Product/Offer JSON-LD and checks the fields an agent needs to evaluate and transact, the difference between being parsed and being skipped.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Agent-readiness of this product</div>
      <div class="o-lift" id="psaScore">0</div>
      <div class="o-sub" id="psaSub">paste a product page</div>
      <div class="metrics" id="psaMetrics"></div>
      <p class="caveat">Checks for the fields AI shopping agents read: identifiers, price, currency, availability, live inventory, granular specs, and a freshness timestamp. If a fact is not a distinct field, the agent cannot use it.</p>
    </div>
  </div>
</section>'''
a_method=('<section class="method"><h2>What it checks</h2>'
  '<p>AI reasoning engines evaluate products through structured data, not marketing copy. If your feed has unstructured blobs or missing attributes, agents skip your listing and pick a competitor whose data parses cleanly. This auditor extracts your Product/Offer JSON-LD and grades it against the fields agents actually need.</p>'
  '<p>It runs entirely in your browser. Build a compliant block with the generator, then confirm your server serves it fast.</p>'
  '<div class="srcs"><a href="/blogs/when-the-buyer-is-a-bot">When the buyer is a bot &rarr;</a><a href="/tools/product-offer-jsonld-generator">Product/Offer JSON-LD Generator &rarr;</a><a href="/blogs/schema-markup-ai-citations-2026">Schema for AI citations &rarr;</a></div></section>')
a_script=r'''<script>
(function(){
  var root=document.getElementById('psa'); if(!root) return;
  var ta=document.getElementById('psaText');
  function findProduct(raw){
    var objs=[];
    var blocks=raw.match(/<script[^>]*application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi);
    var jsons=[];
    if(blocks){ blocks.forEach(function(b){ jsons.push(b.replace(/<script[^>]*>/i,'').replace(/<\/script>/i,'')); }); }
    else { jsons.push(raw); }
    jsons.forEach(function(j){ try{ var o=JSON.parse(j); (Array.isArray(o)?o:[o]).forEach(function(x){ collect(x,objs); }); }catch(e){} });
    // find a Product
    for(var i=0;i<objs.length;i++){ var t=objs[i]['@type']; if(t==='Product'||(Array.isArray(t)&&t.indexOf('Product')>=0)) return objs[i]; }
    return null;
  }
  function collect(o,acc){ if(!o||typeof o!=='object')return; if(o['@graph']){o['@graph'].forEach(function(x){collect(x,acc);});} acc.push(o); }
  function has(v){ return v!==undefined&&v!==null&&v!==''; }
  function run(){
    var raw=ta.value||''; var out=document.getElementById('psaMetrics');
    if(!raw.trim()){document.getElementById('psaScore').textContent='0';document.getElementById('psaSub').textContent='paste a product page';out.innerHTML='';return;}
    var p=findProduct(raw);
    if(!p){document.getElementById('psaScore').textContent='0';document.getElementById('psaSub').textContent='no Product JSON-LD found';out.innerHTML='<div class="metric"><div class="metric-fix">No <b>@type: Product</b> block detected. Agents will fall back to parsing prose, or skip you. Add a Product JSON-LD block.</div></div>';return;}
    var off=p.offers||{}; if(Array.isArray(off)) off=off[0]||{};
    var checks=[
      ['name','Product name', has(p.name)],
      ['identifier','SKU / GTIN', has(p.sku)||has(p.gtin13)||has(p.gtin)||has(p.gtin12)||has(p.mpn)],
      ['brand','Brand', has(p.brand)],
      ['price','Price', has(off.price)],
      ['currency','Price currency', has(off.priceCurrency)],
      ['availability','Availability', has(off.availability)],
      ['inventory','Live inventory level', has(off.inventoryLevel)],
      ['specs','Granular attributes (additionalProperty)', Array.isArray(p.additionalProperty)&&p.additionalProperty.length>0],
      ['image','Image', has(p.image)],
      ['fresh','dateModified freshness stamp', has(p.dateModified)]
    ];
    var W={name:12,identifier:14,price:14,currency:8,availability:12,inventory:12,specs:14,image:6,brand:4,fresh:4};
    var score=0; checks.forEach(function(c){ if(c[2]) score+=W[c[0]]; });
    document.getElementById('psaScore').textContent=score;
    var got=checks.filter(function(c){return c[2];}).length;
    document.getElementById('psaSub').textContent=(score>=85?'agent-ready':(score>=60?'parseable, gaps remain':'will likely be skipped'))+' · '+got+'/'+checks.length+' fields';
    out.innerHTML=checks.map(function(c){var vd=c[2]?'good':'bad';
      var fix={identifier:'Add sku or gtin13 so the agent can match the exact item.',price:'Add offers.price, agents cannot transact without it.',currency:'Add offers.priceCurrency (e.g. USD, INR).',availability:'Add offers.availability (schema.org/InStock).',inventory:'Add offers.inventoryLevel so agents trust stock in real time.',specs:'Add additionalProperty entries for dimensions, material, compatibility, distinct fields, not prose.',fresh:'Add dateModified, freshness is a ranking input for retrieval.',image:'Add image.',brand:'Add brand.',name:'Add name.'};
      return '<div class="metric"><div class="metric-top"><span class="metric-name">'+c[1]+'</span><span class="verdict '+vd+'">'+(c[2]?'present':'missing')+'</span></div>'+(c[2]?'':'<div class="metric-fix">'+fix[c[0]]+'</div>')+'</div>';
    }).join('');
  }
  ta.addEventListener('input',run); run();
})();
</script>'''

# ================= TOOL 3: UGC INJECTION SCANNER =================
u_body='''<section class="card" id="ugc">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Paste a review or user-generated text</div>
        <textarea class="ta" id="ugcText" placeholder="Paste a product review, Q&A, or any user-submitted text as it is stored/rendered. Nothing is uploaded, scanning runs in your browser."></textarea>
        <p class="hint">When a shopping agent parses your page it reads user content verbatim. Attackers hide instructions inside it to hijack the agent, this flags the patterns before they reach an agent's context.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Injection risk</div>
      <div class="o-lift" id="ugcScore">clean</div>
      <div class="o-sub" id="ugcSub">paste text to scan</div>
      <div class="flags" id="ugcFlags"></div>
      <p class="caveat">Heuristic scan for instruction-shaped patterns, hidden HTML comments, and redirect URLs. Mitigate by stripping comments and control sequences at ingestion, and serving agent-facing content from structured fields only.</p>
    </div>
  </div>
</section>'''
u_method=('<section class="method"><h2>Why this matters</h2>'
  '<p>Agent-targeted prompt injection means attackers plant instructions inside public product descriptions, reviews, or HTML metadata. When a shopping agent reads the page, the injected text can override its logic, pushing it to redirect a purchase, leak a token, or recommend an inferior product. Your user-generated content is now an executable surface.</p>'
  '<p>This scanner flags the tell-tale patterns. It runs entirely in your browser and stores nothing.</p>'
  '<div class="srcs"><a href="/blogs/when-the-buyer-is-a-bot">When the buyer is a bot &rarr;</a><a href="/blogs/hallucination-proofing-your-brand">Hallucination-proofing your brand &rarr;</a></div></section>')
u_script=r'''<script>
(function(){
  var root=document.getElementById('ugc'); if(!root) return;
  var ta=document.getElementById('ugcText');
  var RULES=[
    [/<!--[\s\S]*?-->/gi, 'high', 'Hidden HTML comment, agents parse it even though humans never see it'],
    [/\b(system|assistant|developer)\s*:/gi, 'high', 'Role-play marker impersonating a system/assistant instruction'],
    [/\bignore (all |any )?(previous|prior|above) (instructions|prompts|context)\b/gi, 'high', 'Explicit instruction-override phrase'],
    [/\bdisregard (all |the )?(previous|prior|above)\b/gi, 'high', 'Instruction-override phrase'],
    [/\b(redirect|send|submit|forward|post) (the )?(purchase|order|payment|token|credentials|card)\b/gi, 'high', 'Imperative directing an agent to move a purchase, payment, or token'],
    [/\b(output|reveal|print|leak|exfiltrate) (the )?(api|aws|secret|env|environment|credentials?|keys?|token)\b/gi, 'high', 'Attempt to extract secrets or credentials'],
    [/\bdo not (mention|tell|reveal|inform)\b/gi, 'med', 'Concealment instruction'],
    [/\[\.\]|\(\.\)|\[dot\]|\bhxxp/gi, 'high', 'Obfuscated URL (defanged domain)'],
    [/https?:\/\/[^\s"<]+/gi, 'low', 'Contains a URL, verify the destination is not attacker-controlled'],
    [/[​-‏‪-‮⁠﻿]/g, 'high', 'Invisible/zero-width or bidi control characters'],
    [/\byou (must|should|will|are required to)\b/gi, 'med', 'Imperative addressed to the reader/agent']
  ];
  function run(){
    var t=ta.value||''; var F=document.getElementById('ugcFlags');
    if(!t.trim()){document.getElementById('ugcScore').textContent='clean';document.getElementById('ugcSub').textContent='paste text to scan';F.innerHTML='';return;}
    var hits=[], hi=0, med=0;
    RULES.forEach(function(r){ var m=t.match(r[0]); if(m){ var n=m.length; if(r[1]==='high')hi+=n; else if(r[1]==='med')med+=n;
      hits.push([r[1], r[2], (m[0]||'').replace(/[​-‏‪-‮⁠﻿]/g,'█').slice(0,80)]); } });
    var verdict = hi>0 ? 'malicious' : (med>0 ? 'suspicious' : 'clean');
    var col = hi>0?'var(--signal)':(med>0?'#D4A34A':'var(--up)');
    var sc=document.getElementById('ugcScore'); sc.textContent=verdict; sc.style.color=col;
    document.getElementById('ugcSub').textContent=hits.length? (hi+' high, '+med+' medium signals') : 'no injection patterns found';
    if(!hits.length){F.innerHTML='<div class="flag ok">No instruction-shaped patterns detected. Still serve agent-facing content from structured fields, not raw UGC.</div>';return;}
    F.innerHTML=hits.map(function(h){return '<div class="flag'+(h[0]==='low'?' ok':'')+'"><b>'+(h[0]==='high'?'HIGH':h[0]==='med'?'MEDIUM':'note')+':</b> '+h[1]+'<br><span style="color:rgba(255,255,255,.45)">matched: “'+h[2].replace(/</g,'&lt;')+'”</span></div>';}).join('');
  }
  ta.addEventListener('input',run); run();
})();
</script>'''

# ================= TOOL 4: PRODUCT/OFFER JSON-LD GENERATOR =================
g_body='''<section class="card" id="pog">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Product name</div><input class="tin" id="pgName" placeholder="TRK-42 Trail Runner"></div>
      <div class="num-grid">
        <div class="fld"><div class="lab">SKU</div><input class="tin" id="pgSku" placeholder="TRK-42-BLK-M"></div>
        <div class="fld"><div class="lab">GTIN-13 <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">opt</span></div><input class="tin" id="pgGtin" placeholder="8901234567890"></div>
        <div class="fld"><div class="lab">Brand</div><input class="tin" id="pgBrand" placeholder="Your Store"></div>
      </div>
      <div class="fld"><div class="lab">Product URL</div><input class="tin" id="pgUrl" placeholder="https://yourstore.com/p/trk-42"></div>
      <div class="num-grid">
        <div class="fld"><div class="lab">Price</div><input class="tin" id="pgPrice" placeholder="7990.00"></div>
        <div class="fld"><div class="lab">Currency</div><input class="tin" id="pgCur" placeholder="INR"></div>
        <div class="fld"><div class="lab">Inventory</div><input class="tin" id="pgInv" placeholder="34"></div>
      </div>
      <div class="fld"><div class="lab">Availability</div>
        <select class="sel-input" id="pgAvail"><option value="InStock">InStock</option><option value="OutOfStock">OutOfStock</option><option value="PreOrder">PreOrder</option><option value="BackOrder">BackOrder</option></select></div>
      <div class="fld"><div class="lab">Granular attributes <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">key: value, one per line</span></div>
        <textarea class="ta" id="pgAttrs" style="min-height:90px" placeholder="drop_mm: 8&#10;waterproof: false&#10;terrain: technical trail"></textarea></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Your Product + Offer JSON-LD</div>
      <div class="codeout" style="margin:12px 0 0"><div class="code-block"><pre id="pgOut">{}</pre></div></div>
      <div class="btn-row"><button class="tbtn primary" id="pgCopy" type="button">Copy</button><button class="tbtn" id="pgDl" type="button">Download .json</button></div>
      <p class="caveat">Emits agent-readable Product + Offer schema with explicit attributes, live inventory, and a dateModified stamp set to now. Paste into the &lt;head&gt; of the product page.</p>
    </div>
  </div>
</section>'''
g_method=('<section class="method"><h2>How to use it</h2>'
  '<p>Agents evaluate products on structured fields, not prose. This generator emits a <strong>Product</strong> plus <strong>Offer</strong> block with distinct attribute fields (dimensions, material, compatibility), a live <strong>inventoryLevel</strong>, and a <strong>dateModified</strong> stamp, the fields that decide whether an agent can transact with you or skips to a competitor.</p>'
  '<p>Deploy it on the product page, keep inventory and price in sync, and audit the result. Freshness matters: dateModified is a retrieval ranking input.</p>'
  '<div class="srcs"><a href="/blogs/when-the-buyer-is-a-bot">When the buyer is a bot &rarr;</a><a href="/tools/product-schema-auditor">Product Schema Auditor &rarr;</a></div></section>')
g_script=r'''<script>
(function(){
  var root=document.getElementById('pog'); if(!root) return;
  function v(id){return (document.getElementById(id).value||'').trim();}
  function build(){
    var name=v('pgName')||'Your Product';
    var url=v('pgUrl')||'https://yourstore.com/p/product';
    var base=url.replace(/#.*$/,'');
    var prod={"@context":"https://schema.org","@type":"Product","@id":base+"#product","name":name};
    if(v('pgSku')) prod.sku=v('pgSku');
    if(v('pgGtin')) prod.gtin13=v('pgGtin');
    if(v('pgBrand')) prod.brand={"@type":"Brand","name":v('pgBrand')};
    prod.url=url;
    var attrs=(v('pgAttrs')||'').split(/\r?\n/).map(function(l){return l.trim();}).filter(Boolean).map(function(l){
      var i=l.indexOf(':'); if(i<0) return null; var k=l.slice(0,i).trim(); var val=l.slice(i+1).trim();
      if(val==='true')val=true; else if(val==='false')val=false; else if(val!==''&&!isNaN(Number(val)))val=Number(val);
      return {"@type":"PropertyValue","name":k,"value":val};
    }).filter(Boolean);
    if(attrs.length) prod.additionalProperty=attrs;
    var off={"@type":"Offer"};
    if(v('pgPrice')) off.price=v('pgPrice');
    if(v('pgCur')) off.priceCurrency=v('pgCur');
    off.availability="https://schema.org/"+(document.getElementById('pgAvail').value||'InStock');
    if(v('pgInv')!=='') off.inventoryLevel={"@type":"QuantitativeValue","value":Number(v('pgInv'))||0};
    off.itemCondition="https://schema.org/NewCondition";
    prod.offers=off;
    prod.dateModified=new Date().toISOString();
    document.getElementById('pgOut').textContent='<script type="application/ld+json">\n'+JSON.stringify(prod,null,2)+'\n<\/script>';
  }
  ['pgName','pgSku','pgGtin','pgBrand','pgUrl','pgPrice','pgCur','pgInv','pgAvail','pgAttrs'].forEach(function(id){
    var el=document.getElementById(id); el.addEventListener('input',build); el.addEventListener('change',build);});
  document.getElementById('pgCopy').addEventListener('click',function(){var b=this,t=document.getElementById('pgOut').textContent;
    function d(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(d,d);}else{d();}});
  document.getElementById('pgDl').addEventListener('click',function(){var t=document.getElementById('pgOut').textContent;
    var blob=new Blob([t],{type:'application/json'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='product.jsonld';document.body.appendChild(a);a.click();document.body.removeChild(a);});
  build();
})();
</script>'''

page("agentic-commerce-readiness-scorecard","Agentic Commerce Readiness Scorecard &middot; Free Tool &middot; rawmktg.",
  "Score your store against the infrastructure agentic commerce demands, sub-200ms latency, machine-readable catalog, unified incentives, identity linking, MACH, with your biggest gaps ranked.",
  "Free Tool &middot; Diagnostic","Agentic Commerce Readiness Scorecard",
  "Score your catalog against what AI shopping agents require, latency, structured data, incentives, identity and risk controls, and get your biggest gaps ranked.",
  s_body,s_method,s_script)
page("product-schema-auditor","Product Schema (JSON-LD) Auditor &middot; Free Tool &middot; rawmktg.",
  "Paste a product page and audit its Product/Offer JSON-LD for the fields AI shopping agents need: SKU/GTIN, price, currency, availability, live inventory, granular specs and dateModified.",
  "Free Tool &middot; Analyzer","Product Schema (JSON-LD) Auditor",
  "Paste a product page or its JSON-LD and see whether an agent can evaluate and transact with it, or skips it for a competitor that parses cleanly.",
  a_body,a_method,a_script)
page("ugc-prompt-injection-scanner","UGC Prompt-Injection Scanner &middot; Free Tool &middot; rawmktg.",
  "Paste a review or user-generated text and flag the prompt-injection patterns, hidden HTML comments, and redirect URLs that hijack AI shopping agents parsing your page.",
  "Free Tool &middot; Security","UGC Prompt-Injection Scanner",
  "Paste user-generated text and flag the instruction-shaped patterns, hidden comments and obfuscated URLs that turn your reviews into an attack surface for AI agents.",
  u_body,u_method,u_script)
page("product-offer-jsonld-generator","Product/Offer JSON-LD Generator &middot; Free Tool &middot; rawmktg.",
  "Generate agent-readable Product + Offer JSON-LD with explicit attributes, live inventory and a dateModified stamp. Copy or download for your product pages.",
  "Free Tool &middot; Generator","Product/Offer JSON-LD Generator",
  "Build agent-readable Product + Offer schema, explicit attributes, availability, live inventory and a freshness stamp, then copy or download it.",
  g_body,g_method,g_script)

allok=True
for slug in ["agentic-commerce-readiness-scorecard","product-schema-auditor","ugc-prompt-injection-scanner","product-offer-jsonld-generator"]:
    hh=open(f"tools/{slug}.html").read()
    js=re.findall(r'<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', hh, re.S)[-1][8:-9]
    open("/tmp/bt.js","w").write(js)
    r=subprocess.run(["node","--check","/tmp/bt.js"],capture_output=True,text=True)
    print(slug,"| NODE:","OK" if r.returncode==0 else "FAIL "+r.stderr[:400],"| jsonld:",hh.count("application/ld+json"))
    if r.returncode!=0: allok=False
print("ALL OK" if allok else "FAILURES")
