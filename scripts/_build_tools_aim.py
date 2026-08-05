#!/usr/bin/env python3
"""SCRATCH: build 3 tools from the AI Mode vs AI Overviews article. Do NOT commit."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
TPL=open("tools/off-site-authority-scorecard.html",encoding="utf-8").read()
def sl(a,b):
    i=TPL.index(a); j=TPL.index(b,i)+len(b); return TPL[i:j]
GA=sl("<!-- Google tag (gtag.js) -->","})();</script>")
STYLE=sl("<style>","</style>")
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
TOOLSCSS=open("assets/tools.css",encoding="utf-8").read()
# inline tools.css into the base <style> so tool pages are fully self-contained
STYLE=STYLE.replace("</style>","\n/* ---- inlined tools.css ---- */\n"+TOOLSCSS+"\n</style>")

def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
def page(slug,title,desc,eyebrow,h1,deck,main_inner,script):
    URL=f"https://rawmktg.com/tools/{slug}"
    webapp={"@context":"https://schema.org","@type":"WebApplication","name":title,"url":URL,"description":desc,"applicationCategory":"BusinessApplication","operatingSystem":"Web, all browsers","browserRequirements":"Requires JavaScript","isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"}}
    webpage={"@context":"https://schema.org","@type":"WebPage","name":title,"url":URL,"description":desc,"isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://rawmktg.com/tools"},{"@type":"ListItem","position":3,"name":title,"item":URL}]}
    org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
    de=H.escape(desc,quote=True)
    head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
     "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
     f"  <title>{title} &middot; Free GEO Tool &middot; rawmktg.</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
     f"  <meta name=\"description\" content=\"{de}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
     "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
     "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
     "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
     "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
     f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
     f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en-IN" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
     "  <meta property=\"og:type\" content=\"website\" />\n"
     f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(title)}\" />\n"
     f"  <meta property=\"og:description\" content=\"{de}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
     "  <meta property=\"og:image\" content=\"https://rawmktg.com/assets/images/og-default.png\" />\n  <meta property=\"og:image:width\" content=\"1200\" />\n  <meta property=\"og:image:height\" content=\"630\" />\n"
     "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
     f"  <meta name=\"twitter:title\" content=\"{H.escape(title)}\" />\n  <meta name=\"twitter:description\" content=\"{de}\" />\n"
     "  <meta name=\"twitter:image\" content=\"https://rawmktg.com/assets/images/og-default.png\" />\n"
     f"  {jb(webapp)}\n  {jb(webpage)}\n  {jb(crumb)}\n  {jb(org)}\n"
     "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n  "
     +FONTS+"\n  "+STYLE+"\n  <link rel=\"stylesheet\" href=\"/assets/tools.css\" />\n  "+ADSENSE+"\n</head>\n<body>\n\n")
    hdr=("<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\"><span class=\"eyebrow-tag\">"+eyebrow+"</span><span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated June 2026</span></div>\n"
     f"    <h1 class=\"article-headline\">{H.escape(h1)}</h1>\n    <p class=\"article-deck\">{H.escape(deck)}</p>\n  </header>\n</div>\n\n")
    mn="<main class=\"toolpage\" id=\"article-main\">\n  <div class=\"page\">\n"+main_inner+"\n  </div>\n</main>\n\n"
    return head+NAV+"\n\n"+hdr+mn+NEWS+"\n\n"+FOOT+"\n"+script+"\n</body>\n</html>\n"

# ============================ TOOL 1: Dual-Track Visibility Scorecard ============================
def item(w,track,name,act):
    return (f'<div class="item" data-w="{w}" data-track="{track}" data-act="{H.escape(act,quote=True)}">'
            f'<span class="iname">{H.escape(name)}</span>'
            '<div class="iseg"><button data-m="0" class="sel">No</button><button data-m="0.5">Partial</button><button data-m="1">Yes</button></div></div>')
AIO=[(24,"Ranks in the organic top 10 for target terms","AI Overviews pulls ~38% of its citations from the top 10, ranking is the entry ticket."),
 (20,"40-55 word direct answer after each H2","Lead each H2 with a self-contained answer in Gemini's extraction window before any narrative."),
 (18,"FAQPage / Article / Product schema deployed","Structured data lets the summarizer parse and credit your claims."),
 (16,"Direct, comparative tables and scannable blocks","AI Overviews favours concise, comparative formatting it can lift verbatim."),
 (12,"A relevant on-page video","A relevant video raises AI Overviews citation odds by 156%."),
 (10,"Dense factual prose with stats and sources","Statistics with clear citations lift citation probability 40-70%.")]
MODE=[(22,"Deep, modular topic hubs beyond money pages","Only ~12% of AI Mode URLs match your top-10 page, it pulls the buried depth."),
 (20,"Proprietary research or original data worth citing","Original data resolves sub-queries nothing else can answer."),
 (18,"Off-site co-citation: Reddit, Quora, forums","Reddit citations rose 450%, UGC feeds fan-out retrieval."),
 (15,"Accurate G2, Capterra, Crunchbase, LinkedIn profiles","The Knowledge and Shopping Graphs verify entities from these."),
 (13,"YouTube presence with clean transcripts","Gemini reads transcripts as text and captures video sub-queries."),
 (12,"Questions-as-headings, each a standalone answer","Every H2 must resolve a distinct sub-query on its own.")]
aio_items="".join(item(w,"aio",n,a) for w,n,a in AIO)
mode_items="".join(item(w,"mode",n,a) for w,n,a in MODE)
DT_CARD=('<section class="card"><div class="grid score"><div class="checklist" id="dtChecklist">'
 '<div class="cat"><div class="cat-h">AI Overviews track, win the page <span>100 pts</span></div>'+aio_items+'</div>'
 '<div class="cat"><div class="cat-h">AI Mode track, win the brand <span>100 pts</span></div>'+mode_items+'</div>'
 '</div><div class="panel-out">'
 '<div class="o-eyebrow">AI Overviews track</div><div class="scorewrap"><span class="score" id="dtAio" style="font-size:48px">0</span><span class="score-d">/100</span></div><div class="gauge"><div class="gfill" id="dtAioFill"></div></div>'
 '<div class="o-eyebrow" style="margin-top:18px">AI Mode track</div><div class="scorewrap"><span class="score" id="dtMode" style="font-size:48px">0</span><span class="score-d">/100</span></div><div class="gauge"><div class="gfill" id="dtModeFill"></div></div>'
 '<span class="scoreband" id="dtVerdict" style="margin-top:18px">-</span>'
 '<div class="gaps" id="dtGaps"></div>'
 '<p class="caveat">A weighted self-assessment of the two tracks Google AI rewards separately. AI Overviews scores page-level ranking and extraction; AI Mode scores domain depth, off-site co-citation and freshness. Weights reflect each lever\'s pull on citations; real results depend on execution and competition.</p>'
 '</div></div></section>')
DT_METHOD=('<section class="method"><h2>How this works</h2><p>Google\'s two AI surfaces agree on sources just <strong>13.7%</strong> of the time, so they have to be earned separately. AI Overviews is a ranking game with a summary layer on top, win it with top-10 positions, schema and 40-55 word answer blocks. AI Mode is an authority game decided before a click that never comes, win it with depth, proprietary research and off-site co-citation. This scorecard scores both tracks, then ranks your biggest unrealized points across them.</p>'
 '<div class="srcs"><a href="/blogs/ai-mode-vs-ai-overviews">AI Mode vs AI Overviews &rarr;</a><a href="/blogs/why-ai-cites-reddit-g2-analysts">Why AI cites Reddit, G2 &amp; analysts &rarr;</a></div></section>')
DT_JS=r"""<script>
(function(){
  var list=document.getElementById('dtChecklist'); if(!list) return;
  function bandColor(s){return s<=40?'#BC3F1D':(s<=70?'#8A8278':'#3E9B6A');}
  function rgb(h){h=h.replace('#','');return parseInt(h.substr(0,2),16)+','+parseInt(h.substr(2,2),16)+','+parseInt(h.substr(4,2),16);}
  function verdict(a,m){
    if(a>=70&&m>=70) return ['Dual-track ready','#3E9B6A'];
    if(a>=55&&m<45) return ['Half-visible: you win the page, not the brand','#BC3F1D'];
    if(m>=55&&a<45) return ['Strong in AI Mode, thin in Overviews','#8A8278'];
    if(a<40&&m<40) return ['Largely invisible to Google AI','#BC3F1D'];
    return ['Developing on both tracks','#8A8278'];
  }
  function compute(){
    var aio=0,mode=0,gaps=[];
    list.querySelectorAll('.item').forEach(function(it){
      var w=parseFloat(it.dataset.w),tr=it.dataset.track,sel=it.querySelector('.iseg button.sel'),mv=sel?parseFloat(sel.dataset.m):0;
      if(tr==='aio')aio+=w*mv; else mode+=w*mv;
      var un=w*(1-mv); if(un>0) gaps.push({name:it.querySelector('.iname').textContent,act:it.dataset.act,pts:un,track:tr});
    });
    aio=Math.round(aio); mode=Math.round(mode);
    document.getElementById('dtAio').textContent=aio;
    document.getElementById('dtMode').textContent=mode;
    var af=document.getElementById('dtAioFill'); af.style.width=aio+'%'; af.style.background=bandColor(aio);
    var mf=document.getElementById('dtModeFill'); mf.style.width=mode+'%'; mf.style.background=bandColor(mode);
    var v=verdict(aio,mode); var b=document.getElementById('dtVerdict');
    b.textContent=v[0]; b.style.background='rgba('+rgb(v[1])+',.18)'; b.style.color=v[1];
    gaps.sort(function(a,b){return b.pts-a.pts;}); var top=gaps.slice(0,4); var g=document.getElementById('dtGaps');
    if(!top.length){g.innerHTML='<div class="gaps-h">Priority fixes</div><div class="allset">Both tracks covered. Maintain depth and refresh quarterly.</div>';return;}
    var html='<div class="gaps-h">Priority fixes, biggest unrealized points</div>';
    top.forEach(function(gp,i){var tag=gp.track==='aio'?'AIO':'Mode';html+='<div class="gap"><span class="rk">'+(i+1)+'</span><div style="flex:1"><div class="gt">'+gp.name+'</div><div class="ga"><b style="color:#BC3F1D">['+tag+']</b> '+gp.act+'</div></div><span class="pts">+'+Math.round(gp.pts)+'</span></div>';});
    g.innerHTML=html;
  }
  list.addEventListener('click',function(e){var b=e.target.closest('.iseg button');if(!b)return;b.parentElement.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});b.classList.add('sel');compute();});
  compute();
})();
</script>"""
T1=page("dual-track-visibility-scorecard","Dual-Track AI Visibility Scorecard",
 "Score your visibility on Google's two AI surfaces separately, AI Overviews (the page) and AI Mode (the brand), and get your biggest gaps on each track ranked.",
 "Free Tool · Diagnostic","Dual-Track AI Visibility Scorecard",
 "Google's two AI surfaces reward different work. Score the AI Overviews track and the AI Mode track separately, then see which gaps are costing you citations on each.",
 DT_CARD+"\n"+DT_METHOD, DT_JS)

# ============================ TOOL 2: Query Fan-Out Simulator ============================
FO_CARD=('<section class="card"><div class="controls">'
 '<div class="fld"><label for="foq">Enter a buyer query</label><div class="ipt"><input id="foq" type="text" value="best CRM for mid-market teams" autocomplete="off" /></div>'
 '<div class="chips" id="foEx"><span class="chip" data-q="best CRM for mid-market teams">best CRM for mid-market teams</span><span class="chip" data-q="Asana vs Monday for agencies">Asana vs Monday</span><span class="chip" data-q="how to reduce SaaS churn">how to reduce SaaS churn</span><span class="chip" data-q="best AI note taker">best AI note taker</span></div>'
 '<div class="hint">AI Mode decomposes your query into parallel sub-queries, up to 16, each hitting a different index. This shows an illustrative fan-out so you can see which content types resolve each branch.</div></div>'
 '<div class="output" style="margin-top:22px"><div class="o-eyebrow">Parallel sub-queries</div><div class="o-big" id="foCount" style="font-size:40px">0</div><div class="o-sub" id="foCap">of up to 16 concurrent sub-queries</div><div class="alloc" id="foRows"></div></div></section>')
FO_METHOD=('<section class="method"><h2>How this works</h2><p>Classic search maps one query to one retrieval path. <strong>AI Mode does not.</strong> It shreds the parent query into sub-queries by dimension, runs them in parallel across specialized indexes, then synthesizes one answer with inline citations. That is why it cites pages that never rank for the head term. This simulator infers the likely sub-queries from your query\'s shape, it is illustrative, not a live API call, but the lesson holds: ranking for the head term no longer guarantees you are in the room.</p>'
 '<div class="srcs"><a href="/blogs/ai-mode-vs-ai-overviews">AI Mode vs AI Overviews &rarr;</a><a href="/blogs/how-rag-actually-works">How RAG actually works &rarr;</a></div></section>')
FO_JS=r"""<script>
(function(){
  var inp=document.getElementById('foq'); if(!inp) return;
  function subject(q){
    var s=q.trim().replace(/\?+$/,'');
    s=s.replace(/^(what(\s+is|'s| are)?|which|the)\s+/i,'');
    s=s.replace(/^(best|top|cheapest|fastest|leading)\s+/i,'');
    s=s.replace(/\s+(for|in|to)\s+.*/i,'');
    s=s.replace(/\s+\d{4}.*$/,'');
    return s.trim()||'the tool';
  }
  function audience(q){var m=q.match(/\bfor\s+([a-z0-9 \-]+)/i);return m?m[1].trim():'';}
  function plan(q){
    var s=subject(q), aud=audience(q), suf=aud?(' for '+aud):'';
    if(/\bvs\b|\bversus\b/i.test(q)){
      var parts=q.split(/\s+vs\.?\s+|\s+versus\s+/i); var A=(parts[0]||'A').replace(/^(.*\b)?/, '').trim()||parts[0]; var B=(parts[1]||'B').split(/\s+for\s+/i)[0].trim();
      A=parts[0].trim();
      return ['Comparison', [
        ['Feature-by-feature','how do '+A+' and '+B+' compare on core features','comparison hubs, docs'],
        ['Pricing difference',A+' vs '+B+' pricing and plans','pricing pages, forums'],
        ['User reviews, each','real reviews of '+A+' and '+B,'G2, Capterra, Reddit'],
        ['Switching / migration','migrating from '+A+' to '+B,'help docs, community'],
        ['Which for whom','is '+A+' or '+B+' better'+suf,'analyst posts, blogs']
      ]];
    }
    if(/^how\s+(to|do|can|should|i)\b/i.test(q)||/\bhow\b/i.test(q)){
      return ['How-to', [
        ['Step sequence','steps to '+s,'how-to guides, docs'],
        ['Tools needed','best tools to '+s,'tool roundups, directories'],
        ['Best practices','best practices for '+s,'expert blogs, newsletters'],
        ['Common pitfalls','mistakes when trying to '+s,'Reddit, Q&A threads'],
        ['Real examples','examples of '+s,'case studies, YouTube']
      ]];
    }
    // best / general
    return ['Best / shortlist', [
      ['Feature / spec',s+' feature comparison'+suf,'spec pages, docs'],
      ['Pricing',s+' pricing'+suf,'pricing pages, forums'],
      ['User reviews','best '+s+suf+' reviews','G2, Capterra, Reddit'],
      ['Alternatives','top '+s+' alternatives','comparison hubs, listicles'],
      ['Integrations',s+' integrations','marketplace, docs'],
      ['Use-case fit','best '+s+suf,'analyst posts, blogs']
    ]];
  }
  function render(){
    var q=inp.value||''; var pl=plan(q); var rows=pl[1];
    document.getElementById('foCount').textContent=rows.length;
    document.getElementById('foCap').textContent=pl[0]+' query, '+rows.length+' of up to 16 concurrent sub-queries';
    var html='';
    rows.forEach(function(r,i){
      var n=(i+1<10?'0':'')+(i+1);
      html+='<div class="arow" style="--c:#BC3F1D"><div class="swatch"></div><div class="meta"><div class="nm">'+r[0]+'</div><div class="ds">&ldquo;'+r[1]+'&rdquo;</div></div><div class="cnt" style="min-width:120px"><div class="p" style="font-size:10px;color:rgba(255,255,255,.6)">resolves via</div><div class="p" style="color:#fff;font-size:11px;margin-top:2px">'+r[2]+'</div></div></div>';
    });
    document.getElementById('foRows').innerHTML=html;
  }
  inp.addEventListener('input',render);
  document.getElementById('foEx').addEventListener('click',function(e){var c=e.target.closest('.chip');if(!c)return;inp.value=c.dataset.q;render();});
  render();
})();
</script>"""
T2=page("query-fan-out-simulator","Query Fan-Out Simulator",
 "See how Google AI Mode shreds a buyer query into parallel sub-queries, and which content type resolves each branch. An illustrative GEO planning tool.",
 "Free Tool · Visualizer","Query Fan-Out Simulator",
 "Type a buyer query and watch it decompose the way AI Mode would, into parallel sub-queries by dimension, each mapped to the content that resolves it.",
 FO_CARD+"\n"+FO_METHOD, FO_JS)

# ============================ TOOL 3: Answer Block Optimizer ============================
AB_CARD=('<section class="card"><div class="grid mix"><div class="controls">'
 '<div class="fld"><label for="abIn">Paste the answer that leads your H2</label>'
 '<textarea class="ta" id="abIn" placeholder="Paste the 1-3 sentence answer block that opens a section. AI engines extract this window, so it should lead with the answer, stay in the 40-55 word range, and carry a number with its source."></textarea>'
 '<div class="chips" id="abEx"><span class="chip">Load example</span></div>'
 '<div class="hint">Gemini lifts the first self-contained answer after a heading. The 40-55 word window matches its single- and multi-pass extraction patterns.</div></div>'
 '<div class="output"><div class="o-eyebrow">Extraction score</div><div class="o-big" id="abScore">0</div><span class="scoreband" id="abBand" style="margin:2px 0 16px">-</span>'
 '<div class="metrics" id="abMetrics"></div></div></div></section>')
AB_METHOD=('<section class="method"><h2>How this works</h2><p>After every target H2, lead with a direct, self-contained answer of <strong>40 to 55 words</strong> before any narrative. This matches Gemini\'s extraction window, and statistics with clear source citations lift citation probability by 40-70%. This tool checks the mechanics of that block: length, whether it leads with the answer, whether it carries a number, sentence economy, and filler. It is a writing aid, not a guarantee of citation.</p>'
 '<div class="srcs"><a href="/blogs/ai-mode-vs-ai-overviews">AI Mode vs AI Overviews &rarr;</a><a href="/blogs/anatomy-of-a-high-citation-page">Anatomy of a high-citation page &rarr;</a></div></section>')
AB_JS=r"""<script>
(function(){
  var ta=document.getElementById('abIn'); if(!ta) return;
  var EX="Query fan-out is the technique behind Google AI Mode: it splits one query into as many as 16 sub-queries, runs them in parallel across separate indexes, and synthesizes one answer. Across 730,000 paired responses, AI Mode and AI Overviews share only 13.7% of their cited sources.";
  function words(t){return (t.trim().match(/\S+/g)||[]).length;}
  function sentences(t){return (t.trim().match(/[^.!?]+[.!?]+/g)||(t.trim()?[t]:[])).length;}
  function band(s){return s>=75?['Extraction-ready','#3E9B6A','good']:(s>=50?['Workable','#8A8278','warn']:['Hard to extract','#BC3F1D','bad']);}
  function metric(name,verd,vclass,bar,fix){
    return '<div class="metric"><div class="metric-top"><span class="metric-name">'+name+'</span><span class="verdict '+vclass+'">'+verd+'</span></div><div class="metric-bar"><i style="width:'+bar+'%"></i></div><div class="metric-fix">'+fix+'</div></div>';
  }
  function analyze(){
    var t=ta.value||''; var w=words(t); var sc=sentences(t)||1; var avg=w/sc;
    var lead=t.trim().slice(0,80); var filler=/^(in this section|this (article|section|post|guide)|when it comes to|there are many|in today'?s|nowadays|as we (all )?know)/i.test(lead.trim());
    var hasNum=/\d/.test(t); var fillers=(t.match(/\b(very|really|basically|just|actually|quite|simply|in order to|literally)\b/gi)||[]).length;
    // word-count score
    var wScore = (w>=40&&w<=55)?100:(w>=30&&w<=70?60:(w>=20&&w<=85?30:(w>0?10:0)));
    var wV=(w>=40&&w<=55)?['40-55 sweet spot','good']:((w>=30&&w<=70)?['close, '+(w<40?'add detail':'trim'),'warn']:['out of range','bad']);
    var leadScore=(!filler&&w>0)?100:0; var leadV=(!filler&&w>0)?['leads with answer','good']:['starts with filler','bad'];
    var numScore=hasNum?100:0; var numV=hasNum?['has a number','good']:['no statistic','bad'];
    var ecoScore=avg<=28?100:(avg<=36?55:20); var ecoV=avg<=28?['tight sentences','good']:(avg<=36?['a little long','warn']:['too dense','bad']);
    var filScore=fillers<=1?100:(fillers<=3?55:15); var filV=fillers<=1?['minimal filler','good']:(fillers<=3?[fillers+' filler words','warn']:[fillers+' filler words','bad']);
    var total=Math.round(wScore*0.30+leadScore*0.25+numScore*0.20+ecoScore*0.15+filScore*0.10);
    document.getElementById('abScore').textContent=total;
    var bd=band(total); var bb=document.getElementById('abBand'); bb.textContent=bd[0];
    var c=bd[1]; bb.style.background='rgba('+(c==='#3E9B6A'?'62,155,106':c==='#BC3F1D'?'188,63,29':'138,130,120')+',.18)'; bb.style.color=c;
    var html='';
    html+=metric('Word count, '+w,wV[0],wV[1],wScore,'<b>40-55 words</b> matches Gemini\'s extraction window. You have '+w+'.');
    html+=metric('Leads with the answer',leadV[0],leadV[1],leadScore,filler?'<b>Cut the warm-up.</b> Open with the answer itself, not "In this section...".':'Opens with the answer, engines can lift it directly.');
    html+=metric('Carries a statistic',numV[0],numV[1],numScore,hasNum?'A number with its source lifts citation odds 40-70%.':'<b>Add a number and source.</b> Stats with citations lift citation probability 40-70%.');
    html+=metric('Sentence economy, '+avg.toFixed(0)+' wpw',ecoV[0],ecoV[1],ecoScore,avg<=28?'Short sentences chunk cleanly for retrieval.':'<b>Split long sentences.</b> Aim under ~28 words each.');
    html+=metric('Filler words',filV[0],filV[1],filScore,fillers<=1?'Dense, factual prose, the shape engines extract.':'<b>Trim hedges.</b> Remove very, really, basically, just, actually.');
    document.getElementById('abMetrics').innerHTML=html;
  }
  ta.addEventListener('input',analyze);
  document.getElementById('abEx').addEventListener('click',function(){ta.value=EX;analyze();});
  analyze();
})();
</script>"""
T3=page("answer-block-optimizer","Answer Block Optimizer",
 "Paste the answer that leads your H2 and check the mechanics AI engines extract: the 40-55 word window, leading with the answer, a statistic, sentence economy and filler.",
 "Free Tool · Analyzer","Answer Block Optimizer",
 "AI engines lift the first self-contained answer after a heading. Paste yours and check the 40-55 word window, whether it leads with the answer, and whether it carries a stat.",
 AB_CARD+"\n"+AB_METHOD, AB_JS)

# write tool files
for slug,html_ in [("dual-track-visibility-scorecard",T1),("query-fan-out-simulator",T2),("answer-block-optimizer",T3)]:
    open(f"tools/{slug}.html","w",encoding="utf-8").write(html_)
    # node check the LAST <script> (compute)
    m=list(re.finditer(r'<script>\n\(function\(\)\{.*?\}\)\(\);\n</script>', html_, re.S))
    if m:
        open("/tmp/tool_cb.js","w").write(m[-1].group(0)[8:-9])
        r=subprocess.run(["node","--check","/tmp/tool_cb.js"],capture_output=True,text=True)
        print(slug,"NODE:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:500])
    hh=html_
    print("  em:",hh.count("—"),"curly:",hh.count("’")+hh.count("“"),"jsonld:",hh.count("application/ld+json"),"bytes:",len(hh))

# expose embed for article (Dual-Track)
EMBED=('<section class="toolpage tool-embed">\n'
 '  <div class="embed-head"><div class="embed-eyebrow">Free interactive tool</div><div class="embed-title">Score your dual-track AI visibility</div><div class="embed-deck">Rate the AI Overviews track and the AI Mode track separately to see which gaps are costing you citations on each surface.</div></div>\n'
 +DT_CARD+'\n'
 '  <div class="embed-foot">A free rawmktg tool. <a href="/tools/dual-track-visibility-scorecard">Open the full tool &rarr;</a> &middot; <a href="/tools">see all tools</a></div>\n'
 '</section>\n'+DT_JS+'\n')
open("/tmp/dt_embed.html","w").write(EMBED)
print("embed written to /tmp/dt_embed.html, bytes",len(EMBED))
print("DONE tools")
