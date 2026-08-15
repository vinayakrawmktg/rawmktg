#!/usr/bin/env python3
"""SCRATCH: build 2 comparison-page tool pages under /tools. Do NOT commit as content."""
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

# ============ TOOL 1: COMPARISON PAGE EXTRACTABILITY SCORER ============
t1_body=('<section class="card" id="cpe">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Score your comparison page</div>'
  '<div class="q"><div class="q-t"><strong>Answer position.</strong> Is there a verdict naming both products in the first 100 words?</div>'
  '<div class="iseg" data-f="P"><button data-v="1">Yes, up top</button><button data-v="0.5">Partly</button><button data-v="0">Context first</button></div></div>'
  '<div class="fld"><div class="lab">Fact density, verifiable facts per 100 words</div><input class="tin" id="cpeD" inputmode="decimal" value="1.5"></div>'
  '<div class="fld"><div class="lab">Heading match, % of H2s phrased as buyer questions</div><input class="tin" id="cpeH" inputmode="numeric" value="40"></div>'
  '<div class="q"><div class="q-t"><strong>Neutrality.</strong> Do you name where a competitor wins AND link out to 2+ independent sources?</div>'
  '<div class="iseg" data-f="N"><button data-v="1">Both</button><button data-v="0.5">One of them</button><button data-v="0">Neither</button></div></div>'
  '<p class="hint" style="margin:8px 0 0">Weights: 0.30 position, 0.30 density, 0.20 headings, 0.20 neutrality. Density is capped at 1.0 once the page averages 3.0 facts per 100 words. No engine exposes its weights, so treat this as a prioritisation heuristic: fix the lowest term, then re-score.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Extractability score</div>\n'
  '      <div class="scorewrap"><span class="score" id="cpeScore">0</span><span class="score-d">/100</span></div>\n'
  '      <span class="scoreband" id="cpeBand" style="background:rgba(255,255,255,.1);color:#fff">Set the four levers</span>\n'
  '      <div class="gauge"><div class="gfill" id="cpeFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">Fix this first</div><div id="cpeGaps"><p class="hint">Your weakest lever, and the fix, appears here.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t1_method=method(
  "Why score extractability, not rank",
  "A comparison page is not retrieved as a page, it is judged one passage at a time. This score rolls the four levers that decide whether those passages get quoted, answer position, fact density, question-style headings and neutrality, into a single 0 to 100 number so you can prioritise a backlog. The weights are a working heuristic, not a published ranking function. What matters is that all four get measured, because teams reliably optimise the one they find least uncomfortable and ignore the other three.",
  ["Set answer position: is a verdict naming both products inside the first 100 words?",
   "Enter fact density, the count of verifiable facts (numbers, prices, dates, named standards) per 100 words.",
   "Enter the share of your H2s phrased as the buyer's actual question.",
   "Set neutrality: a named competitor advantage plus two or more outbound citations earns full marks.",
   "Read the weakest lever, fix that one, and re-score."],
  [("Is this an official Google or OpenAI ranking score?","No. No engine publishes its retrieval weights. This is a practitioner heuristic that bundles four levers with strong experimental and observational support into one comparable number, so you can rank pages by how much retrieval work they are leaving on the table."),
   ("Why is fact density capped at 3.0 per 100 words?","Because returns flatten. A passage that runs one verifiable fact per 100 words has crossed from decoration into evidence; comparison pages that run 2.0 to 4.0 already sit in the range models reward, so the term maxes out at 3.0 to avoid over-rewarding stat-stuffing."),
   ("Does my data leave the browser?","No. The calculation runs entirely in your browser. Nothing you enter is sent to a server or stored."),
   ("What score should I aim for?","Treat 70 and above as retrieval-ready and below 40 as at risk, but the useful signal is the weakest term, not the total. A page at 55 with zero fact density will move further by adding evidence than by polishing anything else.")],
  [("The comparison-page playbook","/blogs/comparison-pages-ai-shortlists"),("Anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page"),("Comparison Schema Generator","/tools/comparison-schema-generator")])
t1_script=r'''<script>
(function(){
  var root=document.getElementById('cpe'); if(!root) return;
  var W={P:0.30,D:0.30,H:0.20,N:0.20};
  var seg={};
  function num(id){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?null:v;}
  function compute(){
    var D=num('cpeD'), Hp=num('cpeH');
    var P=seg.P, N=seg.N;
    var sEl=document.getElementById('cpeScore'),bEl=document.getElementById('cpeBand'),fill=document.getElementById('cpeFill'),g=document.getElementById('cpeGaps');
    var ready=(P!==undefined)&&(N!==undefined)&&(D!==null)&&(Hp!==null);
    if(!ready){sEl.textContent='0';bEl.textContent='Set the four levers';bEl.style.background='rgba(255,255,255,.1)';bEl.style.color='#fff';fill.style.width='0%';g.innerHTML='<p class="hint">Your weakest lever, and the fix, appears here.</p>';return;}
    var Dn=Math.max(0,Math.min(D/3,1)), Hn=Math.max(0,Math.min(Hp/100,1));
    var E=(W.P*P + W.D*Dn + W.H*Hn + W.N*N)*100;
    sEl.textContent=Math.round(E); fill.style.width=Math.min(100,E)+'%';
    var lbl,col; if(E>=70){lbl='Retrieval-ready';col='var(--up)';}else if(E>=40){lbl='Building';col='#C9922E';}else{lbl='At risk';col='var(--signal)';}
    bEl.textContent=lbl;bEl.style.background=col;bEl.style.color='#0b0b0c';fill.style.background=col;
    var FIX={
      P:['Answer position','Add a verdict that names both products, with two numbers and one honest competitor edge, inside the first 100 words.'],
      D:['Fact density','You are at '+D.toFixed(1)+' facts/100w. Replace adjectives with numbers, prices, dates and named standards until you clear 2.0.'],
      H:['Heading match','Only '+Math.round(Hp)+'% of H2s are buyer questions. Rewrite slogan headings as the exact question a buyer types.'],
      N:['Neutrality','Name two or three cases where a competitor wins, and link out to independent sources. This is the largest single lever for a small domain.']};
    var terms=[['P',P],['D',Dn],['H',Hn],['N',N]].sort(function(a,b){return a[1]-b[1];});
    var worst=terms[0][0], f=FIX[worst];
    g.innerHTML='<div class="lt-stat"><span><strong style="color:#fff">'+f[0]+'</strong> <span style="color:rgba(255,255,255,.55)">'+f[1]+'</span></span></div>';
  }
  root.querySelectorAll('.iseg').forEach(function(s){
    var f=s.getAttribute('data-f');
    s.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        s.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
        b.classList.add('on'); seg[f]=parseFloat(b.getAttribute('data-v')); compute();
      });
    });
  });
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

# ============ TOOL 2: COMPARISON SCHEMA GENERATOR ============
t2_body=('<section class="card" id="csg">\n  <div class="grid calc">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Comparison page</div>'
  '<div class="fld"><div class="lab">Page title</div><input class="tin" id="csgTitle" placeholder="e.g. Acme vs Rival Comparison (2026)"></div>'
  '<div class="fld"><div class="lab">Application category</div><input class="tin" id="csgCat" value="BusinessApplication"></div></div>'
  '      <div class="cat"><div class="cat-h">Product A (position 1)</div>'
  '<div class="num-grid">'
  '<div class="fld"><div class="lab">Name</div><input class="tin" id="csgAName" placeholder="Acme"></div>'
  '<div class="fld"><div class="lab">Price</div><input class="tin" id="csgAPrice" inputmode="decimal" placeholder="79.00"></div>'
  '<div class="fld"><div class="lab">Per (unit text)</div><input class="tin" id="csgAUnit" placeholder="per user per month"></div>'
  '<div class="fld"><div class="lab">Rating (optional)</div><input class="tin" id="csgARate" inputmode="decimal" placeholder="4.6"></div>'
  '<div class="fld"><div class="lab">Review count (optional)</div><input class="tin" id="csgARev" inputmode="numeric" placeholder="412"></div>'
  '</div></div>'
  '      <div class="cat"><div class="cat-h">Product B (position 2)</div>'
  '<div class="num-grid">'
  '<div class="fld"><div class="lab">Name</div><input class="tin" id="csgBName" placeholder="Rival"></div>'
  '<div class="fld"><div class="lab">Price</div><input class="tin" id="csgBPrice" inputmode="decimal" placeholder="115.00"></div>'
  '<div class="fld"><div class="lab">Per (unit text)</div><input class="tin" id="csgBUnit" placeholder="per user per month"></div>'
  '<div class="fld"><div class="lab">Rating (optional)</div><input class="tin" id="csgBRate" inputmode="decimal" placeholder=""></div>'
  '<div class="fld"><div class="lab">Review count (optional)</div><input class="tin" id="csgBRev" inputmode="numeric" placeholder=""></div>'
  '</div>'
  '<p class="hint" style="margin:10px 0 0">Generates a nested WebPage &rarr; ItemList &rarr; SoftwareApplication block. ItemList assigns explicit rank, which is what a Top-N answer is built from. Render it server-side, and make every value match the visible copy on the page exactly.</p></div>\n'
  '    </div>\n'
  '    <div class="output">\n      <div class="o-eyebrow">Your JSON-LD</div>\n'
  '      <div class="btn-row"><button class="tbtn primary" id="csgCopy" type="button">Copy</button><button class="tbtn" id="csgDl" type="button">Download .html</button></div>\n'
  '      <pre class="codeout" id="csgOut" style="margin-top:12px;white-space:pre-wrap">Enter at least two product names to generate the schema.</pre>\n'
  '    </div>\n  </div>\n</section>')
t2_method=method(
  "Turn your comparison table into a ranked list an engine can read",
  "On-page writing gets a comparison page retrieved; schema gets it understood. The class that matters is ItemList, which assigns explicit positions one through N to the products, so when an engine assembles a ranked answer the order is machine-readable rather than inferred from your visual layout. Each product is a SoftwareApplication carrying its category, price and rating. This generator produces the nested block, ready to paste into your page head.",
  ["Enter the page title and the application category (for example BusinessApplication or CustomerServiceApplication).",
   "Fill in Product A, position 1, with name, price and per-unit text; add a rating and review count if you have them.",
   "Do the same for Product B, position 2.",
   "Copy the generated JSON-LD and paste it into the page's server-rendered HTML, not injected by client-side JavaScript.",
   "Confirm every price, rating and name in the schema matches what a human can see on the page."],
  [("Why ItemList instead of two separate Product blocks?","Because a shortlist answer is built from explicit rank. ItemList assigns position 1 through N so the engine reads your ordering directly, rather than guessing it from the table layout. The two SoftwareApplication objects sit inside it as the ranked items."),
   ("Should I render this server-side?","Yes. JSON-LD injected by client-side JavaScript after load is unreliable for AI crawlers, several do not execute scripts. Put the block in the initial HTML response."),
   ("Can the schema contain prices or ratings not shown on the page?","No. Declaring a price, feature or rating in schema that a human cannot find on the page violates structured-data guidelines and can put the whole domain at risk. The schema must describe the visible page, not embellish it."),
   ("Does my data leave the browser?","No. The generator runs entirely client-side. Nothing you type is sent anywhere.")],
  [("The comparison-page playbook","/blogs/comparison-pages-ai-shortlists"),("Schema markup for AI citations","/blogs/schema-markup-ai-citations-2026"),("Comparison Page Extractability Scorer","/tools/comparison-page-extractability-scorer")])
t2_script=r'''<script>
(function(){
  var root=document.getElementById('csg'); if(!root) return;
  function v(id){return (document.getElementById(id).value||'').trim();}
  function today(){var d=new Date();return d.toISOString().slice(0,10);}
  function prod(name,cat,price,unit,rate,rev){
    var o={"@type":"SoftwareApplication","name":name,"applicationCategory":cat};
    if(price){var off={"@type":"Offer","price":price,"priceCurrency":"USD"}; if(unit) off.unitText=unit; o.offers=off;}
    if(rate&&rev){o.aggregateRating={"@type":"AggregateRating","ratingValue":rate,"reviewCount":rev};}
    return o;
  }
  function build(){
    var out=document.getElementById('csgOut');
    var an=v('csgAName'), bn=v('csgBName');
    if(!an||!bn){out.textContent='Enter at least two product names to generate the schema.';return;}
    var cat=v('csgCat')||'BusinessApplication';
    var title=v('csgTitle')||(an+' vs '+bn+' Comparison');
    var obj={"@context":"https://schema.org","@type":"WebPage","name":title,"dateModified":today(),
      "mainEntity":{"@type":"ItemList","numberOfItems":2,"itemListElement":[
        {"@type":"ListItem","position":1,"item":prod(an,cat,v('csgAPrice'),v('csgAUnit'),v('csgARate'),v('csgARev'))},
        {"@type":"ListItem","position":2,"item":prod(bn,cat,v('csgBPrice'),v('csgBUnit'),v('csgBRate'),v('csgBRev'))}
      ]}};
    out.textContent='<script type="application/ld+json">\n'+JSON.stringify(obj,null,2)+'\n<\/script>';
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',build);});
  document.getElementById('csgCopy').addEventListener('click',function(){
    var b=this,t=document.getElementById('csgOut').textContent;
    function done(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,done);}else{done();}
  });
  document.getElementById('csgDl').addEventListener('click',function(){
    var t=document.getElementById('csgOut').textContent, nm=(v('csgAName')||'comparison').replace(/[^a-z0-9]+/gi,'-').toLowerCase();
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([t],{type:'text/html'})); a.download='comparison-schema-'+nm+'.html'; a.click();
  });
  build();
})();
</script>'''

TOOLS=[
 ("comparison-page-extractability-scorer",
  "Comparison Page Extractability Scorer · Free Tool · rawmktg.",
  "Score a comparison page on the four levers that decide whether AI engines quote it, answer position, fact density, question-style headings and neutrality, in one 0 to 100 number, with your weakest lever flagged.",
  "Comparison Pages · Diagnostic","Comparison Page Extractability Scorer",
  "AI engines judge a comparison page one passage at a time. Set the four levers that control whether those passages get quoted and get a single extractability score, plus the one lever to fix first.",
  t1_body,t1_method,t1_script,
  [("Is this an official Google or OpenAI ranking score?","No. No engine publishes its retrieval weights. This is a practitioner heuristic that bundles four levers with strong experimental and observational support into one comparable number, so you can rank pages by how much retrieval work they are leaving on the table."),
   ("Why is fact density capped at 3.0 per 100 words?","Because returns flatten. A passage running one verifiable fact per 100 words has crossed from decoration into evidence; comparison pages that run 2.0 to 4.0 already sit in the range models reward, so the term maxes out at 3.0."),
   ("Does my data leave the browser?","No. The calculation runs entirely in your browser. Nothing you enter is sent to a server or stored."),
   ("What score should I aim for?","Treat 70 and above as retrieval-ready and below 40 as at risk, but the useful signal is the weakest term. A page at 55 with zero fact density will move further by adding evidence than by polishing anything else.")]),
 ("comparison-schema-generator",
  "Comparison Schema Generator · Free Tool · rawmktg.",
  "Generate nested ItemList + SoftwareApplication JSON-LD for a comparison page, so an AI engine reads your product ranking directly instead of inferring it. Copy or download.",
  "Comparison Pages · Generator","Comparison Schema Generator",
  "The ItemList class turns your comparison table into a ranked shortlist an engine can lift. Enter two products and generate the nested JSON-LD, ready to server-render on your page.",
  t2_body,t2_method,t2_script,
  [("Why ItemList instead of two separate Product blocks?","Because a shortlist answer is built from explicit rank. ItemList assigns position 1 through N so the engine reads your ordering directly rather than guessing it from the table layout. The two SoftwareApplication objects sit inside it as the ranked items."),
   ("Should I render this server-side?","Yes. JSON-LD injected by client-side JavaScript after load is unreliable for AI crawlers. Put the block in the initial HTML response."),
   ("Can the schema contain prices or ratings not shown on the page?","No. Declaring a price, feature or rating in schema that a human cannot find on the page violates structured-data guidelines and can put the whole domain at risk. The schema must describe the visible page, not embellish it."),
   ("Does my data leave the browser?","No. The generator runs entirely client-side. Nothing you type is sent anywhere.")]),
]
built=[]
for t in TOOLS:
    html=page(*t); built.append((t[0],html))

for slug,html in built:
    ms=re.findall(r'<script>(?!window\.dataLayer).*?</script>', html, re.S)
    logic=[s for s in ms if 'getElementById' in s]
    ok="n/a"
    if logic:
        open("/tmp/ct.js","w").write(logic[-1][8:-9])
        r=subprocess.run(["node","--check","/tmp/ct.js"],capture_output=True,text=True)
        ok="OK" if r.returncode==0 else "FAIL "+r.stderr[:400]
    jc=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if (json.loads(b) or True))
    amp="BAD" if "&amp;middot;" in html else "clean"
    print(f"{slug:42} node:{ok:6} jsonld:{jc} title:{amp} h1:{html.count('<h1')} faq:{'FAQPage' in html}")
