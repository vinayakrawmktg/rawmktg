#!/usr/bin/env python3
"""SCRATCH: build 4 rendering/SSR tool pages under /tools. Do NOT commit as content."""
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

RELATED=[("Do AI crawlers render JavaScript?","/blogs/do-ai-crawlers-render-javascript"),("How AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site")]

# ============ TOOL 1: CONTENT VISIBILITY RATIO CHECKER ============
t1_body=('<section class="card" id="cvr">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Paste the two versions of your page</div>'
  '<div class="fld"><div class="lab">Raw fetch, no browser (curl output or View Source)</div>'
  '<textarea class="ta" id="cvrRaw" rows="7" placeholder="Paste the HTML a bot receives, curl -A GPTBot ... or View Source"></textarea></div>'
  '<div class="fld"><div class="lab">Rendered, in a browser (Inspect / copy the visible text or DOM)</div>'
  '<textarea class="ta" id="cvrRen" rows="7" placeholder="Paste the rendered DOM or the visible page text a human sees"></textarea></div>'
  '<p class="hint" style="margin:8px 0 0">CVR = visible words in the raw fetch / visible words in the rendered page. Scripts, styles, nav and boilerplate are stripped before counting. A commercial page should clear 0.85.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Content Visibility Ratio</div>\n'
  '      <div class="scorewrap"><span class="score" id="cvrScore">0</span><span class="score-d">/ 1.0</span></div>\n'
  '      <span class="scoreband" id="cvrBand" style="background:rgba(255,255,255,.1);color:#fff">Paste both versions</span>\n'
  '      <div class="gauge"><div class="gfill" id="cvrFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">What the bot sees</div><div id="cvrNote"><p class="hint">Word counts and the verdict appear here.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t1_method=method(
  "What the Content Visibility Ratio measures",
  "A page that looks perfect in Chrome can arrive at an AI crawler as an empty container. The Content Visibility Ratio quantifies the gap: the visible body text a non-rendering bot receives divided by the visible text a human sees after the JavaScript runs. A fully server-rendered page sits near 1.0; a pure client-rendered single-page app sits near 0.0. Most real sites are hybrids, and the commercial pages are usually the low scorers.",
  ["Fetch the page with a bot user agent (curl -A GPTBot ...) or open View Source, and paste that into the raw box.",
   "Open the live page in a browser, and paste the rendered DOM or the visible text into the rendered box.",
   "Read the ratio: 0.85 and above is safe, 0.5 to 0.85 is a hybrid at risk, below 0.5 means the bot sees almost nothing.",
   "Repeat for your pricing, product and comparison pages, and weight the site score by commercial value, not page count."],
  [("What is a good Content Visibility Ratio?","Treat 0.85 as the floor for any page that carries commercial weight. A fully server-rendered page scores near 1.0 and a pure client-rendered app near 0.0. The dangerous zone is the hybrid middle: a marketing shell that scores 0.9 while the pricing widget inside it scores 0.06."),
   ("Why compare raw fetch against rendered instead of just checking the page?","Because the whole problem is that the two differ. Nine of twelve major AI crawlers run no JavaScript, so they only ever see the raw fetch. Checking the page in your browser shows you the rendered version, which is exactly the view the bot does not get."),
   ("How do I get the raw (non-browser) version of my page?","Run curl with a crawler user agent, for example curl -A \"Mozilla/5.0 (compatible; GPTBot/1.4; +https://openai.com/gptbot)\" -s https://example.com/pricing, or open View Source (not Inspect) in your browser, which shows the initial HTML before scripts run."),
   ("Does my data leave the browser?","No. The text you paste is counted entirely in your browser. Nothing is uploaded, stored or sent to any server.")],
  RELATED+[("Rendering Remediation Advisor","/tools/rendering-remediation-advisor")])
t1_script=r'''<script>
(function(){
  var root=document.getElementById('cvr'); if(!root) return;
  function words(s){
    if(!s) return 0;
    var t=s;
    // if it looks like HTML, strip tags + drop non-content elements
    if(/</.test(t)){
      t=t.replace(/<(script|style|noscript|svg|nav|footer)[\s\S]*?<\/\1>/gi,' ');
      t=t.replace(/<[^>]+>/g,' ');
      t=t.replace(/&[a-z#0-9]+;/gi,' ');
    }
    t=t.replace(/\s+/g,' ').trim();
    return t?t.split(' ').length:0;
  }
  function compute(){
    var raw=words(document.getElementById('cvrRaw').value);
    var ren=words(document.getElementById('cvrRen').value);
    var sEl=document.getElementById('cvrScore'),bEl=document.getElementById('cvrBand'),fill=document.getElementById('cvrFill'),note=document.getElementById('cvrNote');
    if(ren<=0){sEl.textContent='0';bEl.textContent='Paste both versions';bEl.style.background='rgba(255,255,255,.1)';bEl.style.color='#fff';fill.style.width='0%';note.innerHTML='<p class="hint">Word counts and the verdict appear here.</p>';return;}
    var cvr=Math.min(raw/ren,1);
    sEl.textContent=cvr.toFixed(2); fill.style.width=(cvr*100)+'%';
    var lbl,col; if(cvr>=0.85){lbl='Readable';col='var(--up)';}else if(cvr>=0.5){lbl='Hybrid, at risk';col='#C9922E';}else{lbl='Invisible to bots';col='var(--signal)';}
    bEl.textContent=lbl;bEl.style.background=col;bEl.style.color='#0b0b0c';fill.style.background=col;
    var verdict = cvr>=0.85 ? 'A non-rendering bot sees essentially the same page a human does.'
      : cvr>=0.5 ? 'The bot sees the shell but misses content that only mounts after hydration. Find the client-loaded blocks.'
      : 'The bot receives almost nothing. Your content depends on a JavaScript runtime these crawlers do not run.';
    note.innerHTML='<div class="lt-stat"><span>Raw fetch (bot)</span><strong>'+raw.toLocaleString()+' words</strong></div>'
      +'<div class="lt-stat"><span>Rendered (human)</span><strong>'+ren.toLocaleString()+' words</strong></div>'
      +'<div class="lt-stat"><span>Missing to the bot</span><strong>'+Math.max(0,ren-raw).toLocaleString()+' words</strong></div>'
      +'<p class="hint" style="margin-top:8px">'+verdict+'</p>';
  }
  root.querySelectorAll('textarea').forEach(function(t){t.addEventListener('input',compute);});
  compute();
})();
</script>'''

# ============ TOOL 2: RENDERING REMEDIATION ADVISOR ============
t2_body=('<section class="card" id="rra">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Answer three questions</div>'
  '<div class="q"><div class="q-t"><strong>How often does this content change?</strong></div>'
  '<div class="iseg" data-f="freq"><button data-v="realtime">Real time / per user</button><button data-v="daily">Daily</button><button data-v="monthly">Weekly / monthly</button><button data-v="rare">Rarely</button></div></div>'
  '<div class="q"><div class="q-t"><strong>Can you change the application code?</strong></div>'
  '<div class="iseg" data-f="code"><button data-v="modern">Yes, modern framework</button><button data-v="legacy">Yes, but legacy</button><button data-v="none">No, untouchable</button></div></div>'
  '<div class="q"><div class="q-t"><strong>How big is the page set?</strong></div>'
  '<div class="iseg" data-f="scale"><button data-v="small">A handful of key pages</button><button data-v="large">A large catalogue</button></div></div>'
  '<p class="hint" style="margin:8px 0 0">The goal is the same for all four fixes: get the populated DOM into the initial HTTP response. The right one depends on change frequency and how much of the codebase you can touch.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Recommended fix</div>\n'
  '      <div class="scorewrap"><span class="score" id="rraFix" style="font-size:40px">&ndash;</span></div>\n'
  '      <span class="scoreband" id="rraBand" style="background:rgba(255,255,255,.1);color:#fff">Answer the three</span>\n'
  '      <div class="gaps"><div class="gaps-h">Why, and the cost</div><div id="rraNote"><p class="hint">Your recommendation appears here.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t2_method=method(
  "Matching the fix to your constraints",
  "There is no single right answer to a rendering problem, only four patterns with different cost curves: server-side rendering (SSR), incremental static regeneration (ISR), static generation (SSG) and edge prerendering. Four of them solve the problem; only SSR requires rewriting application logic. This advisor maps your change frequency, codebase freedom and page-set size to the cheapest pattern that works.",
  ["Set how often the content changes, from real-time per-user data to rarely.",
   "Say whether you can change the application code, and whether the framework is modern or legacy.",
   "Set the page-set size, a handful of key pages or a large catalogue.",
   "Read the recommended pattern and the reason, then confirm against the remediation matrix in the article."],
  [("When should I use SSR versus SSG?","Use SSR (or ISR) when the content changes in real time or daily, like pricing pulled from a billing API or a personalised feed. Use SSG when the content changes weekly or monthly, like docs, blogs and most marketing pages, because building the HTML once at deploy time is the cheapest readable option."),
   ("What is edge prerendering and when is it the answer?","Edge prerendering is a CDN worker that intercepts crawler requests, serves them a cached rendered snapshot, and passes humans through to the normal app. It is the retrofit for a legacy codebase you cannot or will not rewrite this quarter, because it changes nothing about your origin or build, only what bots receive."),
   ("Is serving bots a prerendered snapshot cloaking?","Only if the snapshot differs from what humans see. Serve bots the same content, rendered, and you are compliant; serve them different content and it is cloaking, a policy problem with search engines. Keep the snapshot TTL shorter than your pricing change cycle so a stale plan never gets served."),
   ("Does this tool send my inputs anywhere?","No. The recommendation is computed entirely in your browser from the three answers. Nothing is uploaded or stored.")],
  RELATED+[("Content Visibility Ratio Checker","/tools/content-visibility-ratio-checker")])
t2_script=r'''<script>
(function(){
  var root=document.getElementById('rra'); if(!root) return;
  var s={};
  var FIX={
    SSR:['SSR','Server-side rendering. The server assembles the full HTML per request, so real-time and personalised data is readable on arrival. Highest server cost: compute on every request.'],
    ISR:['ISR','Incremental static regeneration. Pages are pre-built and revalidated on a schedule (stale-while-revalidate), so a large catalogue stays fresh and cheap. Low to moderate cost.'],
    SSG:['SSG','Static generation. The HTML is built once at deploy time and served from the CDN. Cheapest readable option; best for content that changes weekly or monthly.'],
    EDGE:['Edge prerender','A CDN worker serves bots a cached rendered snapshot and passes humans to the SPA. The retrofit when you cannot touch the codebase. Moderate cost; watch the snapshot TTL.']
  };
  function decide(){
    var f=s.freq,c=s.code,sc=s.scale;
    if(!f||!c) return null;
    if(c==='none') return 'EDGE';
    if(f==='realtime') return 'SSR';
    if(f==='daily') return sc==='large'?'ISR':'SSR';
    if(f==='monthly') return sc==='large'?'ISR':'SSG';
    if(f==='rare') return 'SSG';
    return 'SSG';
  }
  function render(){
    var k=decide();
    var fixEl=document.getElementById('rraFix'),band=document.getElementById('rraBand'),note=document.getElementById('rraNote');
    if(!k){fixEl.textContent='–';band.textContent='Answer the three';band.style.background='rgba(255,255,255,.1)';band.style.color='#fff';note.innerHTML='<p class="hint">Your recommendation appears here.</p>';return;}
    var F=FIX[k];
    fixEl.textContent=F[0];
    band.textContent = (k==='EDGE'?'Retrofit':'Rebuild-light'); band.style.background='var(--up)';band.style.color='#0b0b0c';
    var extra = (s.code==='legacy'&&k!=='EDGE') ? '<p class="hint" style="margin-top:8px">Legacy stack: if a framework migration is not realistic this quarter, edge prerendering gets you readable pages without touching the origin.</p>' : '';
    note.innerHTML='<div class="lt-stat"><span>Pattern</span><strong>'+F[0]+'</strong></div><p class="hint" style="margin-top:8px">'+F[1]+'</p>'+extra;
  }
  root.querySelectorAll('.iseg').forEach(function(seg){
    var f=seg.getAttribute('data-f');
    seg.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        seg.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
        b.classList.add('on'); s[f]=b.getAttribute('data-v'); render();
      });
    });
  });
  render();
})();
</script>'''

# ============ TOOL 3: REMEDIATION PRIORITY SCORER ============
ROWS=[("Pricing","28"),("Product & specs","20"),("Comparison","9"),("Documentation","6"),("Blog","4")]
rrows=""
for i,(nm,share) in enumerate(ROWS):
    rrows+=(f'<div class="erow"><div class="ename">{nm}</div>'
      f'<div class="fld"><div class="lab">Citation share %</div><input class="tin" id="rps_{i}_c" inputmode="decimal" value="{share}"></div>'
      f'<div class="fld"><div class="lab">CVR (0-1)</div><input class="tin" id="rps_{i}_v" inputmode="decimal" placeholder="e.g. 0.1"></div></div>')
t3_body=('<section class="card" id="rps">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Score your commercial pages</div>'
  '<p class="hint" style="margin:6px 0 12px">Citation-share defaults are typical B2B figures, edit them for your category. Enter the Content Visibility Ratio for each page type (from the CVR checker). Leave CVR blank to skip a row.</p>'
  +rrows+'</div>\n    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Fix in this order</div>\n'
  '      <div class="gaps"><div class="gaps-h">Risk = citation share x (1 - CVR)</div><div id="rpsOut"><p class="hint">Enter a CVR for at least one row.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t3_method=method(
  "Fixing the right pages first",
  "You do not need to fix every page, only the intersection of high citation value and low visibility, which is usually five to fifteen URLs. This scorer multiplies each page type's share of AI citations by how much of it a non-rendering bot cannot read, and ranks the result. In almost every audit the order comes back the same: pricing first, product and specification pages second, comparison pages third.",
  ["Edit the citation-share percentages if your category differs from the B2B defaults.",
   "Enter the Content Visibility Ratio for each page type, measured with the CVR checker.",
   "Read the ranked list: the top rows are your first sprint.",
   "Stop where the risk score falls below your smallest meaningful number, and ship the fixes top to bottom."],
  [("How is the priority score calculated?","Risk = citation share x (1 - CVR). A page that earns a large share of AI citations but is mostly invisible to non-rendering bots scores highest. A page with a high CVR scores near zero no matter how important it is, because it is already readable."),
   ("Why are pricing and comparison pages usually first?","Because they carry the most commercial weight and are built most dynamically. Pricing tiers are fetched from a billing API on mount and comparison grids are interactive tables, so they tend to have the lowest CVR on the whole site while sitting closest to revenue."),
   ("Where do the default citation shares come from?","They are typical B2B figures from category teardowns: product and specification pages draw around 20% of AI citations and comparison and alternatives pages around 9%. Replace them with your own if you have measured them."),
   ("Does my data leave the browser?","No. The ranking is computed entirely in your browser. Nothing you enter is uploaded or stored.")],
  RELATED+[("Content Visibility Ratio Checker","/tools/content-visibility-ratio-checker")])
t3_script=r'''<script>
(function(){
  var root=document.getElementById('rps'); if(!root) return;
  var NAMES=["Pricing","Product & specs","Comparison","Documentation","Blog"];
  function num(id){var el=document.getElementById(id);if(!el)return null;var v=parseFloat(el.value);return isNaN(v)?null:v;}
  function compute(){
    var rows=[];
    for(var i=0;i<NAMES.length;i++){
      var c=num('rps_'+i+'_c'), v=num('rps_'+i+'_v');
      if(c===null||v===null) continue;
      v=Math.max(0,Math.min(v,1));
      rows.push([NAMES[i], c*(1-v), v, c]);
    }
    var out=document.getElementById('rpsOut');
    if(!rows.length){out.innerHTML='<p class="hint">Enter a CVR for at least one row.</p>';return;}
    rows.sort(function(a,b){return b[1]-a[1];});
    var max=rows[0][1]||1;
    out.innerHTML=rows.map(function(r,idx){
      var col = idx===0?'var(--signal)':(r[1]>=max*0.4?'#C9922E':'var(--up)');
      return '<div class="lt-stat"><span><strong style="color:#fff">'+(idx+1)+'. '+r[0]+'</strong> <span style="color:rgba(255,255,255,.4)">CVR '+r[2].toFixed(2)+'</span></span><strong style="color:'+col+'">'+r[1].toFixed(1)+'</strong></div>';
    }).join('')+'<p class="hint" style="margin-top:8px">Higher score = fix sooner. The number is citation share weighted by how much the bot cannot read.</p>';
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

# ============ TOOL 4: BOT-FETCH TEST COMMAND GENERATOR ============
t4_body=('<section class="card" id="bfc">\n  <div class="grid calc">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Your page and a content string</div>'
  '<div class="fld"><div class="lab">URL to test</div><input class="tin" id="bfcUrl" placeholder="https://example.com/pricing"></div>'
  '<div class="fld"><div class="lab">A string only your real content has</div><input class="tin" id="bfcNeedle" placeholder="per month"></div>'
  '<p class="hint" style="margin:8px 0 0">Generates a single-URL curl test and a multi-bot sweep. Run them from any terminal. If the string is missing from the raw HTML, it is missing from the model\'s view of your page.</p></div>\n'
  '    </div>\n'
  '    <div class="output">\n      <div class="o-eyebrow">Your test commands</div>\n'
  '      <div class="btn-row"><button class="tbtn primary" id="bfcCopy" type="button">Copy</button><button class="tbtn" id="bfcDl" type="button">Download .sh</button></div>\n'
  '      <pre class="codeout" id="bfcOut" style="margin-top:12px;white-space:pre-wrap">Enter a URL and a content string.</pre>\n'
  '    </div>\n  </div>\n</section>')
t4_method=method(
  "Testing the way a bot fetches, not the way you browse",
  "The only valid rendering test is a raw HTTP fetch with no browser, run against the URLs that carry commercial weight. This generator writes two: a one-line curl that greps for a string only your real content has, and a sweep that tests the whole AI-crawler fleet at once. The word-count column in the sweep is the tell, 40 words to every bot and 1,400 in a browser and you have found your ceiling.",
  ["Enter the URL you want to test, usually your pricing page first.",
   "Enter a string that only exists in the real content, a price, a plan name or a specific feature.",
   "Copy the single-URL curl to check one page, or the sweep to test the fleet.",
   "Run it from any terminal. No output from the grep means the string is not in the raw HTML, which means it is not in the model's view of your page."],
  [("Why test with curl instead of my browser?","Because your browser runs JavaScript and the AI crawlers do not. Opening the page in Chrome shows you the rendered version; a raw curl with a bot user agent shows you exactly what a non-rendering crawler receives, which is the view that decides whether you get cited."),
   ("What user agents does the sweep test?","GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot and PerplexityBot, the fleet that covers OpenAI, Anthropic and Perplexity. Different bots occasionally get different treatment because of an old CDN bot rule, which is exactly why testing the fleet beats testing one agent."),
   ("What does the word-count column tell me?","It is the fastest signal of a rendering gap. If a page returns 40 words to every bot but 1,400 in a browser, its content depends on a runtime the bots do not run. A healthy server-rendered page returns a similar word count to bots and browsers alike."),
   ("Is anything sent to a server?","No. The commands are generated in your browser and run on your machine. This tool uploads nothing.")],
  RELATED+[("Content Visibility Ratio Checker","/tools/content-visibility-ratio-checker")])
t4_script=r'''<script>
(function(){
  var root=document.getElementById('bfc'); if(!root) return;
  function esc(s){return (s||'').replace(/"/g,'\\"');}
  function build(){
    var url=(document.getElementById('bfcUrl').value||'').trim()||'https://example.com/pricing';
    var needle=(document.getElementById('bfcNeedle').value||'').trim()||'per month';
    var out=document.getElementById('bfcOut');
    var lines=[];
    lines.push('# 1. Single-URL curl test');
    lines.push('curl -A "Mozilla/5.0 (compatible; GPTBot/1.4; +https://openai.com/gptbot)" \\');
    lines.push('     -s "'+url+'" | grep -i "'+esc(needle)+'"');
    lines.push('# no output means the string is not in the raw HTML.');
    lines.push('');
    lines.push('# 2. Multi-bot sweep');
    lines.push('#!/usr/bin/env bash');
    lines.push('URL="'+url+'"');
    lines.push('NEEDLE="'+esc(needle)+'"');
    lines.push('declare -A AGENTS=(');
    lines.push('  [GPTBot]="Mozilla/5.0 (compatible; GPTBot/1.4; +https://openai.com/gptbot)"');
    lines.push('  [OAI-SearchBot]="Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"');
    lines.push('  [ChatGPT-User]="Mozilla/5.0 (compatible; ChatGPT-User/1.0; +https://openai.com/bot)"');
    lines.push('  [ClaudeBot]="Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"');
    lines.push('  [PerplexityBot]="Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/bot)"');
    lines.push(')');
    lines.push('for name in "${!AGENTS[@]}"; do');
    lines.push('  code=$(curl -A "${AGENTS[$name]}" -s -o /tmp/body -w "%{http_code}" --max-time 5 "$URL")');
    lines.push('  words=$(sed \'s/<[^>]*>/ /g\' /tmp/body | wc -w)');
    lines.push('  grep -qi "$NEEDLE" /tmp/body && hit="FOUND" || hit="MISSING"');
    lines.push('  printf "%-16s http=%s words=%-6s %s\\n" "$name" "$code" "$words" "$hit"');
    lines.push('done');
    out.textContent=lines.join('\n');
  }
  ['bfcUrl','bfcNeedle'].forEach(function(id){document.getElementById(id).addEventListener('input',build);});
  document.getElementById('bfcCopy').addEventListener('click',function(){
    var b=this,t=document.getElementById('bfcOut').textContent;
    function done(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,done);}else{done();}
  });
  document.getElementById('bfcDl').addEventListener('click',function(){
    var t=document.getElementById('bfcOut').textContent;
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([t],{type:'text/x-shellscript'})); a.download='bot-fetch-test.sh'; a.click();
  });
  build();
})();
</script>'''

TOOLS=[
 ("content-visibility-ratio-checker",
  "Content Visibility Ratio Checker · Free Tool · rawmktg.",
  "Paste your raw fetch and rendered page to compute the Content Visibility Ratio, how much of your content AI crawlers can actually read without running JavaScript.",
  "Technical Layer · Analyzer","Content Visibility Ratio Checker",
  "Nine of twelve AI crawlers run no JavaScript. Paste the raw fetch and the rendered page to see the Content Visibility Ratio, and how many words a non-rendering bot never sees.",
  t1_body,t1_method,t1_script,
  [("What is a good Content Visibility Ratio?","Treat 0.85 as the floor for any page that carries commercial weight. A fully server-rendered page scores near 1.0 and a pure client-rendered app near 0.0. The dangerous zone is the hybrid middle: a marketing shell that scores 0.9 while the pricing widget inside it scores 0.06."),
   ("Why compare raw fetch against rendered instead of just checking the page?","Because the whole problem is that the two differ. Nine of twelve major AI crawlers run no JavaScript, so they only ever see the raw fetch. Checking the page in your browser shows the rendered version, which is exactly the view the bot does not get."),
   ("How do I get the raw non-browser version of my page?","Run curl with a crawler user agent, or open View Source (not Inspect), which shows the initial HTML before scripts run."),
   ("Does my data leave the browser?","No. The text you paste is counted entirely in your browser. Nothing is uploaded, stored or sent to any server.")]),
 ("rendering-remediation-advisor",
  "Rendering Remediation Advisor · Free Tool · rawmktg.",
  "Answer three questions about your content and codebase and get the right rendering fix, SSR, SSG, ISR or edge prerendering, with the cost trade-off.",
  "Technical Layer · Advisor","Rendering Remediation Advisor",
  "Four fixes turn an invisible page readable: SSR, SSG, ISR and edge prerendering. Answer three questions and get the cheapest one that fits your change frequency and codebase.",
  t2_body,t2_method,t2_script,
  [("When should I use SSR versus SSG?","Use SSR or ISR when the content changes in real time or daily, like pricing from a billing API. Use SSG when it changes weekly or monthly, like docs and marketing pages, because building the HTML once at deploy time is the cheapest readable option."),
   ("What is edge prerendering and when is it the answer?","A CDN worker that serves crawlers a cached rendered snapshot and passes humans to the normal app. It is the retrofit for a legacy codebase you cannot rewrite this quarter, because it changes nothing about your origin or build."),
   ("Is serving bots a prerendered snapshot cloaking?","Only if the snapshot differs from what humans see. Serve bots the same content, rendered, and you are compliant. Keep the snapshot TTL shorter than your pricing change cycle."),
   ("Does this tool send my inputs anywhere?","No. The recommendation is computed entirely in your browser. Nothing is uploaded or stored.")]),
 ("remediation-priority-scorer",
  "Rendering Remediation Priority Scorer · Free Tool · rawmktg.",
  "Rank which pages to make AI-readable first: Risk = citation share x (1 - Content Visibility Ratio), across your commercial page types.",
  "Technical Layer · Diagnostic","Rendering Remediation Priority Scorer",
  "You do not need to fix everything, just the intersection of high citation value and low visibility. Enter each page type's CVR and get a ranked fix-first list.",
  t3_body,t3_method,t3_script,
  [("How is the priority score calculated?","Risk = citation share x (1 - CVR). A page that earns a large share of AI citations but is mostly invisible to non-rendering bots scores highest. A page with a high CVR scores near zero no matter how important it is, because it is already readable."),
   ("Why are pricing and comparison pages usually first?","Because they carry the most commercial weight and are built most dynamically. Pricing tiers fetched from an API and interactive comparison grids tend to have the lowest CVR while sitting closest to revenue."),
   ("Where do the default citation shares come from?","Typical B2B figures from category teardowns: product and specification pages draw around 20% of AI citations and comparison pages around 9%. Replace them with your own measured shares."),
   ("Does my data leave the browser?","No. The ranking is computed entirely in your browser. Nothing you enter is uploaded or stored.")]),
 ("bot-fetch-test-generator",
  "Bot-Fetch Test Command Generator · Free Tool · rawmktg.",
  "Generate the curl and multi-bot sweep commands to test whether AI crawlers can read your page without a browser. Copy or download.",
  "Technical Layer · Generator","Bot-Fetch Test Command Generator",
  "The only valid rendering test is a raw HTTP fetch with no browser. Enter a URL and a content string and get a ready-to-run curl test and a five-bot sweep.",
  t4_body,t4_method,t4_script,
  [("Why test with curl instead of my browser?","Because your browser runs JavaScript and the AI crawlers do not. A raw curl with a bot user agent shows exactly what a non-rendering crawler receives, which is the view that decides whether you get cited."),
   ("What user agents does the sweep test?","GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot and PerplexityBot, covering OpenAI, Anthropic and Perplexity. Testing the fleet beats testing one agent because an old CDN bot rule can treat them differently."),
   ("What does the word-count column tell me?","If a page returns 40 words to every bot but 1,400 in a browser, its content depends on a runtime the bots do not run. A healthy server-rendered page returns a similar word count to bots and browsers alike."),
   ("Is anything sent to a server?","No. The commands are generated in your browser and run on your machine. This tool uploads nothing.")]),
]
built=[]
for t in TOOLS:
    html=page(*t); built.append((t[0],html))

for slug,html in built:
    ms=re.findall(r'<script>(?!window\.dataLayer).*?</script>', html, re.S)
    logic=[s for s in ms if 'getElementById' in s]
    ok="n/a"
    if logic:
        open("/tmp/jt.js","w").write(logic[-1][8:-9])
        r=subprocess.run(["node","--check","/tmp/jt.js"],capture_output=True,text=True)
        ok="OK" if r.returncode==0 else "FAIL "+r.stderr[:300]
    hc=html.split('</head>')[0]
    jc=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hc,re.S) if (json.loads(b) or True))
    amp="BAD" if "&amp;middot;" in html else "clean"
    print(f"{slug:38} node:{ok:6} jsonld:{jc} title:{amp} h1:{html.count('<h1')} faq:{'FAQPage' in html}")
