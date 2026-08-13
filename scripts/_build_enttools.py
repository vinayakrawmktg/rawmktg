#!/usr/bin/env python3
"""SCRATCH: build 3 entity tool pages under /tools. Do NOT commit as content."""
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

# ==================================================== TOOL 1: ENTITY HOME JSON-LD
g_body='''<section class="card" id="ehg">
  <div class="grid calc">
    <div class="controls">
      <div class="num-grid">
        <div class="fld"><div class="lab">Entity type</div>
          <select class="sel-input" id="eType"><option>Organization</option><option>Corporation</option><option>LocalBusiness</option><option>OnlineBusiness</option><option>EducationalOrganization</option><option>GovernmentOrganization</option><option>NGO</option></select></div>
        <div class="fld"><div class="lab">Founding date</div><input type="date" class="sel-input" id="eFounded"></div>
        <div class="fld"><div class="lab">Logo URL <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">opt</span></div><input class="tin" id="eLogo" placeholder="https://example.com/logo.png"></div>
      </div>
      <div class="fld"><div class="lab">Name</div><input class="tin" id="eName" placeholder="Enterprise Quantum Systems"></div>
      <div class="fld"><div class="lab">Legal name <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">opt</span></div><input class="tin" id="eLegal" placeholder="Enterprise Quantum Systems Inc."></div>
      <div class="fld"><div class="lab">Primary URL</div><input class="tin" id="eUrl" placeholder="https://example.com"></div>
      <div class="fld"><div class="lab">Entity Home page URL <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">your About page</span></div><input class="tin" id="eHome" placeholder="https://example.com/about"></div>
      <div class="fld"><div class="lab">Founder(s) <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">one per line</span></div><textarea class="ta" id="eFounders" style="min-height:70px" placeholder="Dr. John Smith"></textarea></div>
      <div class="fld"><div class="lab">sameAs profiles <span class="val" style="color:rgba(255,255,255,.5);font-size:12px">one URL per line</span></div>
        <textarea class="ta" id="eSames" style="min-height:110px" placeholder="https://www.wikidata.org/wiki/Q11223344&#10;https://www.crunchbase.com/organization/your-co&#10;https://www.linkedin.com/company/your-co"></textarea>
        <p class="hint">These become your sameAs bridges. For the echo to work, each of those profiles must link back to your Entity Home URL. Nothing is uploaded.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Your Entity Home JSON-LD</div>
      <div class="codeout" style="margin:12px 0 0"><div class="code-block"><pre id="ehOut">{}</pre></div></div>
      <div class="btn-row"><button class="tbtn primary" id="ehCopy" type="button">Copy</button><button class="tbtn" id="ehDl" type="button">Download .json</button></div>
      <p class="caveat">Nested @graph with explicit @id URIs and reciprocal mainEntity / mainEntityOfPage binding, the three things most implementations get wrong. Paste into the &lt;head&gt; of your Entity Home only, referenced by @id elsewhere.</p>
    </div>
  </div>
</section>'''
g_method=('<section class="method"><h2>How to use it</h2>'
  '<p>An Entity Home is the one canonical URL that states machine-readable facts about you. This generator emits nested <strong>@graph</strong> JSON-LD with explicit <strong>@id</strong> URIs (so parsers do not treat your nodes as anonymous blank nodes) and the reciprocal <strong>mainEntity</strong> / <strong>mainEntityOfPage</strong> binding that ties the page to the entity.</p>'
  '<p>Deploy it once, on the Entity Home. Reference the same @id from other pages rather than duplicating the block. Then make sure every sameAs profile links back.</p>'
  '<div class="srcs"><a href="/blogs/becoming-an-entity">Becoming an Entity &rarr;</a><a href="/tools/entity-readiness-scorecard">Entity Readiness Scorecard &rarr;</a><a href="/blogs/schema-markup-ai-citations-2026">Schema markup for AI citations &rarr;</a></div></section>')
g_script=r'''<script>
(function(){
  var root=document.getElementById('ehg'); if(!root) return;
  function v(id){return (document.getElementById(id).value||'').trim();}
  function lines(id){return (document.getElementById(id).value||'').split(/\r?\n/).map(function(s){return s.trim();}).filter(Boolean);}
  function build(){
    var name=v('eName')||'Your Organization';
    var type=v('eType')||'Organization';
    var url=v('eUrl'); var base=(url||'https://example.com').replace(/\/+$/,'');
    var home=v('eHome')||(base+'/about');
    var homeBase=home.replace(/#.*$/,'');
    var orgId=base+'/#organization';
    var pageId=homeBase+'#webpage';
    var org={"@type":type,"@id":orgId,"name":name};
    if(v('eLegal')) org.legalName=v('eLegal');
    if(url) org.url=url;
    if(v('eLogo')) org.logo=v('eLogo');
    if(v('eFounded')) org.foundingDate=v('eFounded');
    var fs=lines('eFounders');
    if(fs.length){ org.founders=fs.map(function(n,i){return {"@type":"Person","@id":base+'/#founder-'+(i+1),"name":n};}); }
    var sames=lines('eSames');
    if(sames.length) org.sameAs=sames;
    org.mainEntityOfPage={"@type":"WebPage","@id":pageId};
    var page={"@type":"WebPage","@id":pageId,"url":home,"name":('About '+name),"mainEntity":{"@id":orgId}};
    var graph={"@context":"https://schema.org","@graph":[org,page]};
    document.getElementById('ehOut').textContent=JSON.stringify(graph,null,2);
  }
  ['eType','eFounded','eLogo','eName','eLegal','eUrl','eHome','eFounders','eSames'].forEach(function(id){
    document.getElementById(id).addEventListener('input',build);
    document.getElementById(id).addEventListener('change',build);
  });
  document.getElementById('ehCopy').addEventListener('click',function(){var b=this,t=document.getElementById('ehOut').textContent;
    function d(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(d,d);}else{d();}});
  document.getElementById('ehDl').addEventListener('click',function(){var t=document.getElementById('ehOut').textContent;
    var blob=new Blob([t],{type:'application/json'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='entity-home.jsonld';document.body.appendChild(a);a.click();document.body.removeChild(a);});
  build();
})();
</script>'''

# ==================================================== TOOL 2: READINESS SCORECARD
s_body='''<section class="card" id="ers">
  <div class="grid score">
    <div class="controls" id="ersItems"></div>
    <div class="panel-out">
      <div class="o-eyebrow">Entity readiness</div>
      <div class="scorewrap"><span class="score" id="ersScore">0</span><span class="score-d">/100</span></div>
      <span class="scoreband" id="ersBand" style="background:rgba(255,255,255,.1);color:#fff">Answer the checks</span>
      <div class="gauge"><div class="gfill" id="ersFill" style="width:0%;background:var(--signal)"></div></div>
      <div class="gscale"><span>At risk</span><span>Emerging</span><span>Established</span></div>
      <div class="gaps"><div class="gaps-h">Biggest gaps</div><div id="ersGaps"></div></div>
    </div>
  </div>
</section>'''
s_method=('<section class="method"><h2>What it scores</h2>'
  '<p>Entity data is evaluated through three sequential gates, <strong>Understandability</strong> (can a machine parse who you are), <strong>Credibility</strong> (do ~3 independent sources agree), and <strong>Deliverability</strong> (can crawlers actually reach it), sitting on top of NEEATT notability. Fail gate one and the rest is irrelevant.</p>'
  '<p>Answer honestly. The lowest-scoring items are ranked as your biggest gaps, work them top-down.</p>'
  '<div class="srcs"><a href="/blogs/becoming-an-entity">Becoming an Entity &rarr;</a><a href="/tools/entity-home-generator">Entity Home JSON-LD Generator &rarr;</a><a href="/tools/fact-consistency-checker">Fact-Consistency Checker &rarr;</a></div></section>')
s_script=r'''<script>
(function(){
  var root=document.getElementById('ers'); if(!root) return;
  var CATS=[
    ['Understandability',[
      ['A single canonical Entity Home URL exists (not the marketing homepage)','Create one About/organisation URL to carry your facts.'],
      ['Each entity has one explicit @id (no blank nodes)','Add @id URIs to every node in your JSON-LD.'],
      ['@type is declared for the org and its key people','Declare Organization/Person types explicitly.'],
      ['Body copy states plain facts, not marketing','Rewrite to say what you are: function, parent, founding, people.']
    ]],
    ['Credibility',[
      ['A Wikidata item exists for the entity','Mint a Wikidata item; it has no notability wall for structured data.'],
      ['Facts are corroborated by 3+ independent secondary sources','Earn coverage in reliable, independent outlets.'],
      ['Listed on authoritative databases (Crunchbase, registries, D&B)','Claim and complete the major database profiles.'],
      ['Core facts match across every profile (name, founding date, HQ)','Harmonise every fact to the Entity Home exactly.']
    ]],
    ['Deliverability',[
      ['The Entity Home renders for crawlers without JavaScript','Server-render or pre-render the canonical page.'],
      ['sameAs is bidirectional (external profiles link back)','Configure the return link on every profile you control.'],
      ['One organisation declaration, referenced by @id (not duplicated)','Declare the org once; reference it by @id elsewhere.'],
      ['robots.txt / sitemap let AI and search crawlers reach it','Unblock citation crawlers and expose a clean sitemap.']
    ]],
    ['Notability (NEEATT)',[
      ['The entity resolves to a distinct node (Knowledge Panel or KG MID)','Audit the Knowledge Graph API for your MID.'],
      ['Independent, notable coverage exists (not press releases)','Earn genuine third-party coverage, not syndicated PR.']
    ]]
  ];
  var state={};
  var wrap=document.getElementById('ersItems');
  wrap.innerHTML=CATS.map(function(c,ci){
    return '<div class="cat"><div class="cat-h">'+c[0]+'<span id="ch'+ci+'"></span></div>'+
      c[1].map(function(it,ii){var key=ci+'-'+ii;state[key]=null;
        return '<div class="item"><span class="iname">'+it[0]+'</span><span class="iseg" data-k="'+key+'">'
          +'<button data-m="1" type="button">Yes</button><button data-m="0.5" type="button">Partial</button><button data-m="0" type="button">No</button></span></div>';
      }).join('')+'</div>';
  }).join('');
  var FIX={}; CATS.forEach(function(c,ci){c[1].forEach(function(it,ii){FIX[ci+'-'+ii]={t:it[0],f:it[1]};});});
  function compute(){
    var vals=Object.keys(state).map(function(k){return state[k];}).filter(function(x){return x!==null;});
    var total=Object.keys(state).length;
    var sum=vals.reduce(function(a,b){return a+b;},0);
    var score=Math.round((sum/total)*100);
    document.getElementById('ersScore').textContent=score;
    document.getElementById('ersFill').style.width=score+'%';
    var band=document.getElementById('ersBand');
    var b=score>=80?['Established','var(--up)']:score>=55?['Emerging','#D4A34A']:['At risk','var(--signal)'];
    band.textContent=b[0]; band.style.background='transparent'; band.style.color=b[1]; band.style.border='1px solid '+b[1];
    document.getElementById('ersFill').style.background=b[1];
    var gaps=Object.keys(state).filter(function(k){return state[k]!==null&&state[k]<1;})
      .sort(function(a,b){return state[a]-state[b];}).slice(0,5);
    document.getElementById('ersGaps').innerHTML=gaps.length?gaps.map(function(k,i){
      return '<div class="gap"><span class="rk">'+(i+1)+'</span><span style="flex:1"><span class="gt">'+FIX[k].t+'</span><span class="ga">'+FIX[k].f+'</span></span><span class="pts">'+(state[k]===0?'+full':'+half')+'</span></div>';
    }).join(''):'<div class="allset">No gaps flagged. Strong entity posture, now govern it against drift.</div>';
    // category rollups
    CATS.forEach(function(c,ci){var ks=c[1].map(function(_,ii){return ci+'-'+ii;});
      var done=ks.filter(function(k){return state[k]!==null;}).length;
      document.getElementById('ch'+ci).textContent=done+'/'+ks.length;});
  }
  root.addEventListener('click',function(e){var b=e.target.closest('.iseg button'); if(!b)return;
    var seg=b.closest('.iseg'), k=seg.getAttribute('data-k');
    seg.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});
    b.classList.add('sel'); state[k]=parseFloat(b.getAttribute('data-m')); compute();});
  compute();
})();
</script>'''

# ==================================================== TOOL 3: FACT-CONSISTENCY
f_body='''<section class="card" id="fcc">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Entity Home, the canonical truth</div>
        <div class="num-grid" style="margin-top:4px">
          <input class="tin" id="fcName" placeholder="Legal name">
          <input class="tin" id="fcDate" placeholder="Founding date">
          <input class="tin" id="fcHq" placeholder="HQ (city)">
        </div></div>
      <div class="fld"><div class="lab">Profiles to check against it</div>
        <div id="fcRows"></div>
        <div class="btn-row"><button class="tbtn" id="fcAdd" type="button">+ Add profile</button></div>
        <p class="hint">Enter the same three facts as they appear on each third-party profile (Crunchbase, LinkedIn, G2, a registry). Leave a cell blank if the profile does not state it. Nothing is uploaded.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Digital Brand Echo</div>
      <div class="o-lift" id="fcScore">100</div>
      <div class="o-sub" id="fcSub">add profiles to check</div>
      <div class="flags" id="fcFlags"></div>
      <p class="caveat">Drift across profiles fragments your entity node and erodes algorithmic confidence. Fix every conflict at the Entity Home first, then correct outward. Dates compare on the year.</p>
    </div>
  </div>
</section>'''
f_method=('<section class="method"><h2>Why consistency is the lever</h2>'
  '<p>When your Entity Home asserts a fact, crawlers look for that exact fact elsewhere. If registries, Wikidata and directories <strong>echo</strong> it, confidence rises and you earn stable nodes and Knowledge Panels. If they <strong>contradict</strong>, the node fragments and generative models start improvising, aligning your legal name across nine directories is the highest-leverage afternoon in the whole project.</p>'
  '<p>This checker flags where your profiles disagree with the canonical values. It runs entirely in your browser.</p>'
  '<div class="srcs"><a href="/blogs/becoming-an-entity">Becoming an Entity &rarr;</a><a href="/tools/entity-home-generator">Entity Home JSON-LD Generator &rarr;</a></div></section>')
f_script=r'''<script>
(function(){
  var root=document.getElementById('fcc'); if(!root) return;
  var wrap=document.getElementById('fcRows');
  function row(nm){
    var el=document.createElement('div'); el.className='lrow';
    el.innerHTML='<div class="lrow-top"><input class="tin pn" placeholder="Profile name (e.g. Crunchbase)" style="max-width:220px" value="'+(nm||'')+'"><button class="rm-x" type="button" aria-label="Remove">&times;</button></div>'
      +'<div class="num-grid"><input class="tin pName" placeholder="Legal name"><input class="tin pDate" placeholder="Founding date"><input class="tin pHq" placeholder="HQ (city)"></div>';
    el.querySelector('.rm-x').addEventListener('click',function(){el.remove();run();});
    el.querySelectorAll('input').forEach(function(i){i.addEventListener('input',run);});
    wrap.appendChild(el);
  }
  function norm(s){return (s||'').trim().toLowerCase().replace(/\s+/g,' ').replace(/[.,]/g,'');}
  function yr(s){var m=(s||'').match(/\d{4}/);return m?m[0]:null;}
  function run(){
    var canon={name:document.getElementById('fcName').value,date:document.getElementById('fcDate').value,hq:document.getElementById('fcHq').value};
    var rows=[].slice.call(wrap.querySelectorAll('.lrow'));
    var checks=0, matches=0, flags=[];
    var FIELDS=[['name','Legal name'],['date','Founding date'],['hq','HQ']];
    rows.forEach(function(r){
      var pn=r.querySelector('.pn').value.trim()||'a profile';
      var pv={name:r.querySelector('.pName').value,date:r.querySelector('.pDate').value,hq:r.querySelector('.pHq').value};
      FIELDS.forEach(function(f){
        var c=canon[f[0]], p=pv[f[0]];
        if(!c||!p) return;              // only compare when both present
        checks++;
        if(f[0]==='date'){
          var yc=yr(c), yp=yr(p);
          if(yc&&yp&&yc===yp){ if(norm(c)===norm(p)){matches++;} else {matches++; flags.push(['minor',f[1]+' on '+pn+' matches the year but differs in precision: "'+p+'" vs "'+c+'".']);} }
          else { flags.push(['conflict',f[1]+' on '+pn+' conflicts: "'+p+'" vs Entity Home "'+c+'".']); }
        } else {
          if(norm(c)===norm(p)) matches++;
          else flags.push(['conflict',f[1]+' on '+pn+' conflicts: "'+p+'" vs Entity Home "'+c+'".']);
        }
      });
    });
    var score=checks? Math.round((matches/checks)*100):100;
    document.getElementById('fcScore').textContent=score;
    document.getElementById('fcSub').textContent=checks? (score>=100?'in harmony':(score>=70?'minor drift':'fragmenting'))+' · '+checks+' facts compared':'add profiles to check';
    var F=document.getElementById('fcFlags');
    if(!checks){F.innerHTML='';return;}
    if(!flags.length){F.innerHTML='<div class="flag ok">Every stated fact matches the Entity Home. That is exactly the echo you want.</div>';return;}
    F.innerHTML=flags.map(function(x){return '<div class="flag'+(x[0]==='minor'?' ok':'')+'">'+x[1]+'</div>';}).join('');
  }
  document.getElementById('fcAdd').addEventListener('click',function(){row();run();});
  ['fcName','fcDate','fcHq'].forEach(function(id){document.getElementById(id).addEventListener('input',run);});
  row('Crunchbase'); row('LinkedIn'); run();
})();
</script>'''

page("entity-home-generator","Entity Home JSON-LD Generator &middot; Free GEO Tool &middot; rawmktg.",
  "Generate nested @graph Entity Home JSON-LD, Organization + WebPage, with explicit @id URIs, reciprocal mainEntity/mainEntityOfPage binding, and a sameAs array. Copy or download.",
  "Free Tool &middot; Generator","Entity Home JSON-LD Generator",
  "Build the nested @graph JSON-LD for your Entity Home, with explicit @id URIs and the reciprocal bindings most implementations miss. Copy or download.",
  g_body,g_method,g_script)
page("entity-readiness-scorecard","Entity Readiness Scorecard &middot; Free GEO Tool &middot; rawmktg.",
  "Score your readiness to be a recognized entity across the three gates, Understandability, Credibility, Deliverability, plus NEEATT notability, with your biggest gaps ranked.",
  "Free Tool &middot; Diagnostic","Entity Readiness Scorecard",
  "Score your entity posture across the three gates and NEEATT notability, and get your biggest gaps ranked in order.",
  s_body,s_method,s_script)
page("fact-consistency-checker","Fact-Consistency Checker &middot; Free GEO Tool &middot; rawmktg.",
  "Check whether your legal name, founding date and HQ match across third-party profiles. Drift fragments your entity node, this flags every conflict against the Entity Home.",
  "Free Tool &middot; Analyzer","Fact-Consistency Checker",
  "Check whether your core facts match across every profile. Drift fragments your node, this flags every conflict against your Entity Home.",
  f_body,f_method,f_script)

allok=True
for slug in ["entity-home-generator","entity-readiness-scorecard","fact-consistency-checker"]:
    hh=open(f"tools/{slug}.html").read()
    js=re.findall(r'<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', hh, re.S)[-1][8:-9]
    open("/tmp/e.js","w").write(js)
    r=subprocess.run(["node","--check","/tmp/e.js"],capture_output=True,text=True)
    print(slug,"| NODE:","OK" if r.returncode==0 else "FAIL "+r.stderr[:300],"| jsonld:",hh.count("application/ld+json"),"| bytes:",len(hh))
    if r.returncode!=0: allok=False
print("ALL OK" if allok else "FAILURES")
