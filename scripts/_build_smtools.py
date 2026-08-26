#!/usr/bin/env python3
"""SCRATCH: build 3 sitemap/discovery tool pages under /tools. Do NOT commit as content."""
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

REL=[("XML sitemaps for AI discovery","/blogs/xml-sitemaps-for-ai-discovery"),
     ("How AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site")]

# ============ TOOL 1: SITEMAP DISCOVERY-YIELD AUDITOR ============
SAMPLE=("HOPS=0 STATUS=200  https://example.com/docs/architecture\n"
 "HOPS=2 STATUS=301  https://example.com/docs/rate-limits\n"
 "HOPS=3 STATUS=301  https://example.com/legacy/page\n"
 "HOPS=1 STATUS=302  https://example.com/promo\n"
 "HOPS=0 STATUS=404  https://example.com/removed")
t1_body=('<section class="card" id="sdy">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Paste your crawl results</div>'
  '<div class="fld"><div class="lab">One URL per line: the hop-sweep output, or url,status,hops CSV</div>'
  '<textarea class="ta" id="sdyIn" rows="9" placeholder="HOPS=2 STATUS=301 https://example.com/page\nor\nhttps://example.com/page,301,2"></textarea></div>'
  '<div class="btn-row" style="margin-top:8px"><button class="tbtn" id="sdySample" type="button">Load sample</button></div>'
  '<p class="hint" style="margin:10px 0 0">A URL passes only if it returns 200 and resolves inside the three-hop ceiling. Real-time AI indexers abandon anything at three hops or more. Get the input by running the hop-sweep from the article against your own sitemap.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Discovery yield</div>\n'
  '      <div class="scorewrap"><span class="score" id="sdyScore">0</span><span class="score-d">/ 1.0</span></div>\n'
  '      <span class="scoreband" id="sdyBand" style="background:rgba(255,255,255,.1);color:#fff">Paste your crawl</span>\n'
  '      <div class="gauge"><div class="gfill" id="sdyFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">Where the budget goes</div><div id="sdyNote"><p class="hint">The breakdown and worst offenders appear here.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t1_method=method(
  "What discovery yield measures",
  "Discovery yield is the share of the URLs you declare that a real-time AI indexer can actually resolve into a citable document in one pass. A URL counts only if it returns 200 and lands inside the three-hop redirect ceiling, because indexers like OAI-SearchBot, Claude-SearchBot and PerplexityBot abandon a request at three hops with no error you can see. Most sites score between 0.60 and 0.85 on their first measurement, and the gap is almost always redirect chains and stale 404s, not missing pages.",
  ["Run the hop-sweep bash script from the article against your sitemap, or build a url,status,hops CSV yourself.",
   "Paste the lines here, one URL per line. Both the HOPS=.. STATUS=.. format and plain CSV are parsed.",
   "Read the yield: 0.98 and above is healthy, 0.90 to 0.98 is at risk, below 0.90 is failing.",
   "Fix the worst offenders top to bottom: collapse multi-hop chains to a single 301, and purge non-200 URLs from the file."],
  [("What is a good discovery yield?","Treat 0.98 as the target and 0.90 as the floor. Below 0.90, a tenth of what you declare is unreadable to a non-rendering indexer, which quietly caps how much of your site can ever be cited. Most sites start between 0.60 and 0.85 before anyone has looked."),
   ("Why does a URL fail at three hops?","Because real-time AI indexers enforce a hard ceiling of one to three redirects and drop the request after it, unlike Googlebot which follows around ten. Scheme, host and trailing-slash normalisation can burn the whole budget before your content is served, so the crawler never arrives."),
   ("What formats does the box accept?","Two. The output of the hop-sweep (lines like HOPS=2 STATUS=301 https://...), and plain CSV as url,status,hops. Any line it cannot parse is skipped, so you can paste a raw log and it will pick out what it can."),
   ("Does my data leave the browser?","No. Every line is parsed and scored entirely in your browser. Nothing is uploaded, stored or sent to any server.")],
  REL+[("lastmod Timestamp-Trust Calculator","/tools/lastmod-timestamp-trust-calculator")])
t1_script=r'''<script>
(function(){
  var root=document.getElementById('sdy'); if(!root) return;
  var SAMPLE="HOPS=0 STATUS=200  https://example.com/docs/architecture\nHOPS=2 STATUS=301  https://example.com/docs/rate-limits\nHOPS=3 STATUS=301  https://example.com/legacy/page\nHOPS=1 STATUS=302  https://example.com/promo\nHOPS=0 STATUS=404  https://example.com/removed";
  function parse(line){
    var url=(line.match(/https?:\/\/[^\s,]+/)||[null])[0];
    var status=null,hops=null;
    var mS=line.match(/STATUS\s*=\s*(\d{3})/i), mH=line.match(/HOPS\s*=\s*(\d+)/i);
    if(mS) status=parseInt(mS[1],10);
    if(mH) hops=parseInt(mH[1],10);
    if(status===null||hops===null){
      var parts=line.split(',').map(function(x){return x.trim();});
      if(parts.length>=3){
        if(!url) url=parts[0];
        if(status===null){var s=parseInt(parts[1],10); if(!isNaN(s)) status=s;}
        if(hops===null){var h=parseInt(parts[2],10); if(!isNaN(h)) hops=h;}
      }
    }
    if(url===null||status===null) return null;
    if(hops===null) hops=0;
    return {url:url,status:status,hops:hops};
  }
  function compute(){
    var raw=document.getElementById('sdyIn').value.split('\n');
    var rows=[]; for(var i=0;i<raw.length;i++){ if(!raw[i].trim()) continue; var r=parse(raw[i]); if(r) rows.push(r); }
    var sEl=document.getElementById('sdyScore'),band=document.getElementById('sdyBand'),fill=document.getElementById('sdyFill'),note=document.getElementById('sdyNote');
    if(!rows.length){sEl.textContent='0';band.textContent='Paste your crawl';band.style.background='rgba(255,255,255,.1)';band.style.color='#fff';fill.style.width='0%';note.innerHTML='<p class="hint">The breakdown and worst offenders appear here.</p>';return;}
    var total=rows.length, direct=0, redirectOk=0, nonOk=0, overHop=0, fails=[];
    rows.forEach(function(r){
      var okStatus=(r.status===200), okHop=(r.hops<3);
      if(okStatus&&okHop){ if(r.hops===0) direct++; else redirectOk++; }
      else {
        if(!okStatus) nonOk++;
        if(!okHop) overHop++;
        fails.push(r);
      }
    });
    var pass=direct+redirectOk, yield_=pass/total;
    sEl.textContent=yield_.toFixed(2); fill.style.width=(yield_*100)+'%';
    var lbl,col; if(yield_>=0.98){lbl='Healthy';col='var(--up)';}else if(yield_>=0.90){lbl='At risk';col='#C9922E';}else{lbl='Failing';col='var(--signal)';}
    band.textContent=lbl;band.style.background=col;band.style.color='#0b0b0c';fill.style.background=col;
    function row(lbl,val,c){return '<div class="lt-stat"><span>'+lbl+'</span><strong'+(c?' style="color:'+c+'"':'')+'>'+val+'</strong></div>';}
    var html=row('URLs declared',total.toLocaleString())
      +row('200, zero hops',direct.toLocaleString(),'var(--up)')
      +row('200, resolved in budget',redirectOk.toLocaleString())
      +row('Non-200',nonOk.toLocaleString(), nonOk?'var(--signal)':null)
      +row('At or past the hop ceiling',overHop.toLocaleString(), overHop?'var(--signal)':null);
    if(fails.length){
      html+='<div class="gaps-h" style="margin-top:12px">Worst offenders</div>';
      fails.slice(0,8).forEach(function(r){
        var why = (r.status!==200? r.status+' ':'') + (r.hops>=3? r.hops+' hops':'');
        var short=r.url.replace(/^https?:\/\//,'');
        if(short.length>42) short=short.slice(0,40)+'..';
        html+='<div class="lt-stat"><span style="color:rgba(255,255,255,.62)">'+short+'</span><strong style="color:var(--signal)">'+why.trim()+'</strong></div>';
      });
      if(fails.length>8) html+='<p class="hint" style="margin-top:6px">and '+(fails.length-8)+' more.</p>';
    } else {
      html+='<p class="hint" style="margin-top:8px">Every declared URL resolves cleanly. This is where you want to be.</p>';
    }
    note.innerHTML=html;
  }
  document.getElementById('sdyIn').addEventListener('input',compute);
  document.getElementById('sdySample').addEventListener('click',function(){document.getElementById('sdyIn').value=SAMPLE;compute();});
  compute();
})();
</script>'''

# ============ TOOL 2: LASTMOD TIMESTAMP-TRUST CALCULATOR ============
t2_body=('<section class="card" id="ltt">\n  <div class="grid score">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Count two things from your last build</div>'
  '<div class="fld"><div class="lab">URLs whose lastmod changed this build</div><input class="tin" id="lttStamp" inputmode="numeric" placeholder="e.g. 12000"></div>'
  '<div class="fld"><div class="lab">URLs whose content actually changed</div><input class="tin" id="lttReal" inputmode="numeric" placeholder="e.g. 500"></div>'
  '<p class="hint" style="margin:8px 0 0">Timestamp trust = content-changed URLs / lastmod-changed URLs. If your build stamps today on every URL but only a handful changed, the indexer recrawls, finds nothing, and demotes the whole file. A false freshness signal is worse than none.</p></div>\n'
  '    </div>\n'
  '    <div class="panel-out">\n      <div class="o-eyebrow">Timestamp trust</div>\n'
  '      <div class="scorewrap"><span class="score" id="lttScore">0</span><span class="score-d">/ 1.0</span></div>\n'
  '      <span class="scoreband" id="lttBand" style="background:rgba(255,255,255,.1);color:#fff">Enter both counts</span>\n'
  '      <div class="gauge"><div class="gfill" id="lttFill" style="width:0%;background:var(--signal)"></div></div>\n'
  '      <div class="gaps"><div class="gaps-h">What to do about it</div><div id="lttNote"><p class="hint">Your score and verdict appear here.</p></div></div>\n'
  '    </div>\n  </div>\n</section>')
t2_method=method(
  "Why lastmod is the signal you probably lie with",
  "Real-time AI indexers lean on lastmod harder than Google does, because freshness is the strongest scheduling input they have. The failure is quiet: a build that stamps today on all 12,000 URLs tells the indexer everything changed, it recrawls, finds nothing changed on thousands of pages, and demotes the recrawl priority of the entire file. Timestamp trust is the ratio that catches this before the indexer does, content-changed URLs over lastmod-changed URLs. Fix a low score with hash-based lastmod: write a new timestamp only when the rendered body actually changes.",
  ["Count how many URLs got a new lastmod in your last build, usually the whole file if you build-stamp.",
   "Count how many URLs genuinely changed content, from a content-hash comparison or your CMS.",
   "Read the ratio: 0.7 and above is trustworthy, 0.2 to 0.7 is an engineering ticket, below 0.2 means you should publish no lastmod at all.",
   "If the score is low, switch to hash-based lastmod so timestamps only move when content moves."],
  [("What is a good timestamp trust score?","1.0 means every timestamp change was a real content change. Aim for 0.9 or above. Below 0.7 is an engineering ticket, and below 0.2 you are better off publishing no lastmod, because an absent signal is neutral while a false one is penalised."),
   ("How do I stop build-stamping every URL?","Hash the rendered body of each page with the volatile regions stripped, nav, footer, build IDs and rendered timestamps, compare against the stored hash, and write a new lastmod only when the hash differs. The article includes a Python implementation."),
   ("Is it better to omit lastmod than to get it wrong?","Yes, once trust drops below roughly 0.2. An absent lastmod is a neutral signal the indexer ignores, whereas a timestamp it has learned to distrust actively demotes your recrawl priority. Honest and present beats frequent and false."),
   ("Does this tool send my numbers anywhere?","No. The ratio is computed entirely in your browser. Nothing you enter is uploaded or stored.")],
  REL+[("Sitemap Discovery-Yield Auditor","/tools/sitemap-discovery-yield-auditor")])
t2_script=r'''<script>
(function(){
  var root=document.getElementById('ltt'); if(!root) return;
  function num(id){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?null:v;}
  function compute(){
    var stamp=num('lttStamp'), real=num('lttReal');
    var sEl=document.getElementById('lttScore'),band=document.getElementById('lttBand'),fill=document.getElementById('lttFill'),note=document.getElementById('lttNote');
    if(stamp===null||real===null||stamp<=0){sEl.textContent='0';band.textContent='Enter both counts';band.style.background='rgba(255,255,255,.1)';band.style.color='#fff';fill.style.width='0%';note.innerHTML='<p class="hint">Your score and verdict appear here.</p>';return;}
    var trust=Math.max(0,Math.min(real/stamp,1));
    sEl.textContent=trust.toFixed(2); fill.style.width=(trust*100)+'%';
    var lbl,col,verdict;
    if(trust>=0.7){lbl='Trustworthy';col='var(--up)';verdict='Your timestamps track real change. Keep it this way and the indexer keeps your recrawl priority high.';}
    else if(trust>=0.2){lbl='Engineering ticket';col='#C9922E';verdict='You are inflating freshness. The indexer will recrawl, find little changed, and start discounting your lastmod. Move to hash-based generation.';}
    else{lbl='Harmful, omit it';col='var(--signal)';verdict='You told the indexer '+stamp.toLocaleString()+' URLs changed when '+real.toLocaleString()+' did. Below 0.2, publishing no lastmod at all scores better than this.';}
    band.textContent=lbl;band.style.background=col;band.style.color='#0b0b0c';fill.style.background=col;
    var wasted=Math.max(0,stamp-real);
    note.innerHTML='<div class="lt-stat"><span>lastmod changed</span><strong>'+stamp.toLocaleString()+'</strong></div>'
      +'<div class="lt-stat"><span>Content changed</span><strong>'+real.toLocaleString()+'</strong></div>'
      +'<div class="lt-stat"><span>False freshness signals</span><strong style="color:'+col+'">'+wasted.toLocaleString()+'</strong></div>'
      +'<p class="hint" style="margin-top:8px">'+verdict+'</p>';
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''

# ============ TOOL 3: INDEXNOW PAYLOAD BUILDER ============
t3_body=('<section class="card" id="inb">\n  <div class="grid calc">\n    <div class="controls">\n'
  '      <div class="cat"><div class="cat-h">Your host, key and changed URLs</div>'
  '<div class="fld"><div class="lab">Host (bare domain, no https, no slash)</div><input class="tin" id="inbHost" placeholder="example.com"></div>'
  '<div class="fld"><div class="lab">Key (8 to 128 chars: a-z, A-Z, 0-9, hyphen)</div><input class="tin" id="inbKey" placeholder="fa8c0a469da44e9b8f6a769f291829f5"></div>'
  '<div class="fld"><div class="lab">Key location (optional, defaults to the root)</div><input class="tin" id="inbKeyLoc" placeholder="https://example.com/{key}.txt"></div>'
  '<div class="fld"><div class="lab">Changed URLs, one per line (up to 10,000)</div><textarea class="ta" id="inbUrls" rows="5" placeholder="https://example.com/docs/rate-limits\nhttps://example.com/blog/sitemap-audit"></textarea></div>'
  '<p class="hint" style="margin:8px 0 0">Submit only the URLs that genuinely changed, the same list your hash-based lastmod produces. Pushing your whole inventory on every deploy earns a 429 and a reputation you will not enjoy.</p></div>\n'
  '    </div>\n'
  '    <div class="output">\n      <div class="o-eyebrow">Your IndexNow payload</div>\n'
  '      <div id="inbWarn"></div>\n'
  '      <div class="btn-row"><button class="tbtn primary" id="inbCopy" type="button">Copy JSON</button><button class="tbtn" id="inbDl" type="button">Download .json</button></div>\n'
  '      <pre class="codeout" id="inbOut" style="margin-top:12px;white-space:pre-wrap">Enter a host, a key and at least one URL.</pre>\n'
  '    </div>\n  </div>\n</section>')
t3_method=method(
  "Building a valid IndexNow submission",
  "IndexNow inverts discovery from pull to push: when a page changes you notify participating engines directly, Bing, Yandex, Naver, Seznam and Yep, and the URL enters a recrawl queue in seconds instead of days. Most first-run failures come from two places: a host field that carries a protocol or a path when it must be a bare FQDN, and a key file that is missing, unreadable or does not match the key. This builder validates both, then writes the JSON POST body, a single-URL GET, and a curl command you can drop into a deploy hook.",
  ["Enter your host as a bare domain, no https and no trailing slash.",
   "Enter your IndexNow key, 8 to 128 characters, and host the same value in a text file at the key location.",
   "Paste the URLs that changed in this deploy, one per line.",
   "Copy the JSON body or the curl command into your deploy hook, after the sitemap validator passes."],
  [("Where does the key file go?","Write a UTF-8 text file named exactly {key}.txt at your site root, containing the key and nothing else. If you cannot write to the root, host it elsewhere and set the key location, but verification scope is then bounded to that directory, a key at /catalog/key.txt authorises submissions under /catalog/ only."),
   ("Do I submit to every engine separately?","No. Submit once to any participating endpoint. The receiving engine verifies your key and broadcasts the payload to every other participant within about ten seconds, and the fanout is cryptographically signed so nobody can spoof submissions on your behalf."),
   ("How many URLs can one submission carry?","Up to 10,000 per POST. Single URLs can also go over a simple GET. Either way, submit only what actually changed, the same hash-derived list your lastmod uses, not your whole inventory."),
   ("Does this tool send anything to IndexNow?","No. It only builds the payload and commands in your browser. You run the submission yourself from your server or deploy pipeline. Nothing here is uploaded.")],
  REL+[("Sitemap Discovery-Yield Auditor","/tools/sitemap-discovery-yield-auditor")])
t3_script=r'''<script>
(function(){
  var root=document.getElementById('inb'); if(!root) return;
  function build(){
    var host=(document.getElementById('inbHost').value||'').trim();
    var key=(document.getElementById('inbKey').value||'').trim();
    var keyLoc=(document.getElementById('inbKeyLoc').value||'').trim();
    var urls=(document.getElementById('inbUrls').value||'').split('\n').map(function(u){return u.trim();}).filter(Boolean);
    var out=document.getElementById('inbOut'), warn=document.getElementById('inbWarn');
    var warns=[];
    if(host && /^(https?:)?\/\//i.test(host)) warns.push('Host has a protocol. Use a bare domain like example.com.');
    if(host && /[\/:]/.test(host)) warns.push('Host has a slash, port or path. It must be the FQDN only.');
    if(key && !/^[a-zA-Z0-9-]{8,128}$/.test(key)) warns.push('Key must be 8 to 128 characters from a-z, A-Z, 0-9 and hyphen.');
    if(urls.length>10000) warns.push('Over 10,000 URLs. Split into batches of 10,000.');
    var badHost = host && (/[\/:]/.test(host)||/^(https?:)?\/\//i.test(host));
    warn.innerHTML = warns.length? warns.map(function(w){return '<p class="hint" style="color:var(--signal);margin:0 0 4px">'+w+'</p>';}).join('') : '';
    if(!host||!key||!urls.length){out.textContent='Enter a host, a key and at least one URL.';return;}
    var cleanHost = badHost? host.replace(/^(https?:)?\/\//i,'').split(/[\/:]/)[0] : host;
    var loc = keyLoc? keyLoc.replace('{key}',key) : ('https://'+cleanHost+'/'+key+'.txt');
    var body={host:cleanHost,key:key,keyLocation:loc,urlList:urls};
    var json=JSON.stringify(body,null,2);
    var enc=encodeURIComponent(urls[0]);
    var lines=[];
    lines.push('// 1. Bulk POST body (application/json)');
    lines.push(json);
    lines.push('');
    lines.push('// 2. Single-URL GET');
    lines.push('https://api.indexnow.org/indexnow?url='+enc+'&key='+key);
    lines.push('');
    lines.push('// 3. curl for your deploy hook');
    lines.push("curl -X POST 'https://api.indexnow.org/indexnow' \\");
    lines.push("  -H 'Content-Type: application/json; charset=utf-8' \\");
    lines.push("  -d '"+JSON.stringify(body)+"'");
    lines.push('');
    lines.push('// Key file: '+loc);
    lines.push('//   contents: '+key);
    out.textContent=lines.join('\n');
    out.setAttribute('data-json',json);
  }
  root.querySelectorAll('input,textarea').forEach(function(i){i.addEventListener('input',build);});
  document.getElementById('inbCopy').addEventListener('click',function(){
    var b=this,t=document.getElementById('inbOut').getAttribute('data-json')||document.getElementById('inbOut').textContent;
    function done(){b.textContent='Copied';b.classList.add('is-done');setTimeout(function(){b.textContent='Copy JSON';b.classList.remove('is-done');},1500);}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,done);}else{done();}
  });
  document.getElementById('inbDl').addEventListener('click',function(){
    var t=document.getElementById('inbOut').getAttribute('data-json')||document.getElementById('inbOut').textContent;
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([t],{type:'application/json'})); a.download='indexnow.json'; a.click();
  });
  build();
})();
</script>'''

TOOLS=[
 ("sitemap-discovery-yield-auditor",
  "Sitemap Discovery-Yield Auditor · Free Tool · rawmktg.",
  "Paste your sitemap crawl results to compute discovery yield: the share of declared URLs that return 200 and resolve inside the three-hop ceiling AI indexers enforce.",
  "Technical Layer · Auditor","Sitemap Discovery-Yield Auditor",
  "Real-time AI indexers abandon a URL after three redirect hops. Paste your hop-sweep results to see how many of your declared URLs they can actually resolve, and which ones fail.",
  t1_body,t1_method,t1_script,
  [("What is a good discovery yield?","Treat 0.98 as the target and 0.90 as the floor. Below 0.90, a tenth of what you declare is unreadable to a non-rendering indexer, which quietly caps how much of your site can ever be cited. Most sites start between 0.60 and 0.85."),
   ("Why does a URL fail at three hops?","Real-time AI indexers enforce a hard ceiling of one to three redirects and drop the request after it, unlike Googlebot which follows around ten. Scheme, host and trailing-slash normalisation can burn the whole budget before your content is served."),
   ("What formats does the box accept?","The output of the hop-sweep (lines like HOPS=2 STATUS=301 https://...), and plain CSV as url,status,hops. Any line it cannot parse is skipped, so you can paste a raw log."),
   ("Does my data leave the browser?","No. Every line is parsed and scored entirely in your browser. Nothing is uploaded, stored or sent to any server.")]),
 ("lastmod-timestamp-trust-calculator",
  "lastmod Timestamp-Trust Calculator · Free Tool · rawmktg.",
  "Measure whether your sitemap lastmod values are honest: content-changed URLs over lastmod-changed URLs. Below 0.2, publishing no lastmod scores better.",
  "Technical Layer · Calculator","lastmod Timestamp-Trust Calculator",
  "Build-stamping today on every URL tells the indexer everything changed, it checks, finds nothing, and demotes you. Enter two counts to see if your timestamps are trusted.",
  t2_body,t2_method,t2_script,
  [("What is a good timestamp trust score?","1.0 means every timestamp change was a real content change. Aim for 0.9 or above. Below 0.7 is an engineering ticket, and below 0.2 you are better off publishing no lastmod, because an absent signal is neutral while a false one is penalised."),
   ("How do I stop build-stamping every URL?","Hash the rendered body of each page with the volatile regions stripped, compare against the stored hash, and write a new lastmod only when the hash differs. The article includes a Python implementation."),
   ("Is it better to omit lastmod than to get it wrong?","Yes, once trust drops below roughly 0.2. An absent lastmod is a neutral signal the indexer ignores, whereas a timestamp it has learned to distrust actively demotes your recrawl priority."),
   ("Does this tool send my numbers anywhere?","No. The ratio is computed entirely in your browser. Nothing you enter is uploaded or stored.")]),
 ("indexnow-payload-builder",
  "IndexNow Payload Builder · Free Tool · rawmktg.",
  "Build a valid IndexNow submission: enter host, key and changed URLs to generate the JSON POST body, a single-URL GET, and a curl command, with host and key validation.",
  "Technical Layer · Generator","IndexNow Payload Builder",
  "IndexNow pushes changed URLs into a recrawl queue in seconds. Enter your host, key and changed URLs to get a validated JSON payload and curl command for your deploy hook.",
  t3_body,t3_method,t3_script,
  [("Where does the key file go?","Write a UTF-8 text file named exactly {key}.txt at your site root, containing the key and nothing else. If you cannot write to the root, host it elsewhere and set the key location, but verification scope is then bounded to that directory."),
   ("Do I submit to every engine separately?","No. Submit once to any participating endpoint. The receiving engine verifies your key and broadcasts the payload to every other participant within about ten seconds, and the fanout is cryptographically signed."),
   ("How many URLs can one submission carry?","Up to 10,000 per POST. Single URLs can also go over a simple GET. Submit only what actually changed, the same hash-derived list your lastmod uses, not your whole inventory."),
   ("Does this tool send anything to IndexNow?","No. It only builds the payload and commands in your browser. You run the submission yourself. Nothing here is uploaded.")]),
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
    dash="DASH" if ("—" in html or "–" in html) else "clean"
    print(f"{slug:38} node:{ok:6} jsonld:{jc} title:{amp} dash:{dash} h1:{html.count('<h1')} faq:{'FAQPage' in html}")
