#!/usr/bin/env python3
"""SCRATCH: build 3 tools from the Reddit GEO Playbook. Do NOT commit."""
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
ADSENSE=''  # AdSense removed: no ad units, hurts TBT
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
TOOLSCSS=open("assets/tools.css",encoding="utf-8").read()
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

# ============ TOOL 1: Reddit Thread Citability Scorer ============
def item(w,name,act):
    return (f'<div class="item" data-w="{w}" data-act="{H.escape(act,quote=True)}">'
            f'<span class="iname">{H.escape(name)}</span>'
            '<div class="iseg"><button data-m="0" class="sel">No</button><button data-m="0.5">Partial</button><button data-m="1">Yes</button></div></div>')
ITEMS=[(20,"Direct, structured answer in the first paragraph","Position-Adjusted Word Count rewards a clean answer placed early; it is the single biggest lever."),
 (18,"Question-form title (ends in ?, opens with what/best/which/how)","76% of cited titles end in a question mark; 69% open with an interrogative word, the shape of a prompt."),
 (16,"Named entities: products, versions, endpoints","Entity density hands the model a structured, verifiable dataset it can lift."),
 (14,"Text self-post, not a link or image share","98% of cited Reddit threads are text self-posts; link/media posts get discarded."),
 (14,"A concrete metric, number or stat","Quantified, verifiable claims raise retrieval and citation probability."),
 (10,"Low off-topic noise, high semantic density","RAG scores vector similarity, not karma; banter and jokes dilute the match."),
 (8,"Clear purchase or problem-solution intent","Cited threads carry buyer intent, best X, X vs Y, or a specific error to solve.")]
items="".join(item(w,n,a) for w,n,a in ITEMS)
RT_CARD=('<section class="card"><div class="grid score"><div class="checklist" id="rtChecklist">'
 '<div class="cat"><div class="cat-h">Cited-thread signature <span>100 pts</span></div>'+items+'</div>'
 '</div><div class="panel-out"><div class="o-eyebrow">Thread citability</div>'
 '<div class="scorewrap"><span class="score" id="rtScore">0</span><span class="score-d">/100</span></div>'
 '<span class="scoreband" id="rtBand">-</span><div class="gauge"><div class="gfill" id="rtFill"></div></div>'
 '<div class="gscale"><span>Skipped</span><span>Borderline</span><span>Cited-ready</span></div>'
 '<div class="gaps" id="rtGaps"></div>'
 '<p class="caveat">A weighted check of the structural signature AI engines reward in Reddit threads. Upvotes are deliberately excluded: 80% of cited B2B threads have under 20 upvotes. Real citation depends on engine, recency and competition.</p>'
 '</div></div></section>')
RT_METHOD=('<section class="method"><h2>How this works</h2><p>An LLM does not read a Reddit thread the way a human does. It is indifferent to karma and awards; it scores candidates by <strong>semantic density and answer directness</strong>. Across 248,000 cited Reddit URLs, the winners share a signature: a question title, a text self-post, a direct answer placed early, and named entities with a metric. This scorecard weights those factors and ranks your biggest fixes. Votes are not on the list on purpose, 80% of cited threads have fewer than 20 upvotes.</p>'
 '<div class="srcs"><a href="/blogs/reddit-geo-playbook">The Reddit GEO Playbook &rarr;</a><a href="/blogs/how-rag-actually-works">How RAG actually works &rarr;</a></div></section>')
RT_JS=r"""<script>
(function(){
  var list=document.getElementById('rtChecklist'); if(!list) return;
  var BANDS=[{max:40,label:'Skipped',color:'#BC3F1D'},{max:70,label:'Borderline',color:'#8A8278'},{max:100,label:'Cited-ready',color:'#3E9B6A'}];
  function bandFor(s){for(var i=0;i<BANDS.length;i++){if(s<=BANDS[i].max)return BANDS[i];}return BANDS[2];}
  function rgb(h){h=h.replace('#','');return parseInt(h.substr(0,2),16)+','+parseInt(h.substr(2,2),16)+','+parseInt(h.substr(4,2),16);}
  function compute(){
    var score=0,gaps=[];
    list.querySelectorAll('.item').forEach(function(it){
      var w=parseFloat(it.dataset.w),sel=it.querySelector('.iseg button.sel'),m=sel?parseFloat(sel.dataset.m):0;
      score+=w*m; var un=w*(1-m); if(un>0) gaps.push({name:it.querySelector('.iname').textContent,act:it.dataset.act,pts:un});
    });
    score=Math.round(score); var band=bandFor(score);
    document.getElementById('rtScore').textContent=score;
    var b=document.getElementById('rtBand'); b.textContent=band.label; b.style.background='rgba('+rgb(band.color)+',.18)'; b.style.color=band.color;
    var f=document.getElementById('rtFill'); f.style.width=score+'%'; f.style.background=band.color;
    gaps.sort(function(a,b){return b.pts-a.pts;}); var top=gaps.slice(0,3); var g=document.getElementById('rtGaps');
    if(!top.length){g.innerHTML='<div class="gaps-h">Priority fixes</div><div class="allset">Full cited-thread signature. This is the shape engines lift, votes or not.</div>';return;}
    var html='<div class="gaps-h">Priority fixes, biggest unrealized points</div>';
    top.forEach(function(gp,i){html+='<div class="gap"><span class="rk">'+(i+1)+'</span><div style="flex:1"><div class="gt">'+gp.name+'</div><div class="ga">'+gp.act+'</div></div><span class="pts">+'+Math.round(gp.pts)+'</span></div>';});
    g.innerHTML=html;
  }
  list.addEventListener('click',function(e){var b=e.target.closest('.iseg button');if(!b)return;b.parentElement.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});b.classList.add('sel');compute();});
  compute();
})();
</script>"""
T1=page("reddit-thread-citability-scorer","Reddit Thread Citability Scorer",
 "Score how likely AI is to cite a Reddit thread, against the signature engines actually reward: question title, self-post, direct answer, named entities. Upvotes excluded on purpose.",
 "Free Tool · Diagnostic","Reddit Thread Citability Scorer",
 "AI engines cite Reddit threads on structure, not karma. Score a thread against the cited-thread signature and see the highest-leverage fixes.",
 RT_CARD+"\n"+RT_METHOD, RT_JS)

# ============ TOOL 2: Reddit Warm-Up & Compliance Planner ============
WU_CARD=('<section class="card"><div class="grid calc"><div class="controls">'
 '<div class="fld"><label for="wuAge">Account age <span class="val" id="wuAgeV">9 days</span></label><input id="wuAge" type="range" min="0" max="90" value="9"></div>'
 '<div class="fld"><label for="wuKarma">Comment karma <span class="val" id="wuKarmaV">22</span></label><input id="wuKarma" type="range" min="0" max="400" value="22"></div>'
 '<div class="fld"><label for="wuVal">Value contributions this cycle <span class="val" id="wuValV">7</span></label><input id="wuVal" type="range" min="0" max="50" value="7"></div>'
 '<div class="fld"><label for="wuPromo">Brand mentions this cycle <span class="val" id="wuPromoV">1</span></label><input id="wuPromo" type="range" min="0" max="20" value="1"></div>'
 '<div class="hint">A planning aid for the 30-day warm-up and the 9:1 value-to-promotion rule. It does not read your account, it just maps your inputs to the protocol.</div></div>'
 '<div class="output"><div class="o-eyebrow">Current phase</div><div class="o-big" id="wuPhase" style="font-size:34px">-</div><span class="scoreband" id="wuRisk" style="margin:2px 0 16px">-</span>'
 '<div class="metrics" id="wuMetrics"></div></div></div></section>')
WU_METHOD=('<section class="method"><h2>How this works</h2><p>Reddit runs a four-layer spam defense, and it rarely tells you when you have tripped it, post links too early and you get silently shadowbanned. The fix is a disciplined warm-up: <strong>Presence</strong> (days 1-14, no links), <strong>Engagement</strong> (days 15-30, bank 50-200 karma), then <strong>Seeding</strong> (month 2+, max one brand link a week) on a strict 9:1 value-to-promotion ratio. This planner maps your inputs to that protocol and flags when it is safe to attach a brand.</p>'
 '<div class="srcs"><a href="/blogs/reddit-geo-playbook">The Reddit GEO Playbook &rarr;</a></div></section>')
WU_JS=r"""<script>
(function(){
  var age=document.getElementById('wuAge'); if(!age) return;
  var karma=document.getElementById('wuKarma'),val=document.getElementById('wuVal'),promo=document.getElementById('wuPromo');
  function metric(name,verd,vclass,fix){return '<div class="metric"><div class="metric-top"><span class="metric-name">'+name+'</span><span class="verdict '+vclass+'">'+verd+'</span></div><div class="metric-fix">'+fix+'</div></div>';}
  function run(){
    var a=+age.value,k=+karma.value,v=+val.value,pr=+promo.value;
    document.getElementById('wuAgeV').textContent=a+' day'+(a===1?'':'s');
    document.getElementById('wuKarmaV').textContent=k;
    document.getElementById('wuValV').textContent=v;
    document.getElementById('wuPromoV').textContent=pr;
    var phase = a<=14?'Presence':(a<=30?'Engagement':'Seeding');
    document.getElementById('wuPhase').textContent=phase;
    var linkOK = (a>30 && k>=50);
    var ratio = pr>0?(v/pr):v;
    var ratioStr = pr>0?(ratio.toFixed(1)+' : 1'):(v+' : 0');
    // shadowban risk
    var risk,rc;
    if(a<15 && pr>0){risk='HIGH';rc='#BC3F1D';}
    else if(!linkOK && pr>0){risk='ELEVATED';rc='#8A8278';}
    else if(linkOK && ratio>=9){risk='LOW';rc='#3E9B6A';}
    else {risk='MODERATE';rc='#8A8278';}
    var rb=document.getElementById('wuRisk'); rb.textContent='Shadowban risk: '+risk; rb.style.background='rgba('+(rc==='#3E9B6A'?'62,155,106':rc==='#BC3F1D'?'188,63,29':'138,130,120')+',.18)'; rb.style.color=rc;
    var html='';
    html+=metric('Brand link allowed?',linkOK?'yes':'not yet',linkOK?'good':'bad',linkOK?'You are past day 30 with enough karma. Hold one brand link per week, max.':'<b>Not yet.</b> Need day 31+ and 50+ comment karma. You have day '+a+', '+k+' karma.');
    var rv = ratio>=9?'on target':(pr===0?'no promo yet':'too promotional'); var rcl = ratio>=9||pr===0?'good':'bad';
    html+=metric('Value : promotion ratio, '+ratioStr,rv,rcl,ratio>=9||pr===0?'Holding the 9:1 rule. Keep nine genuine contributions per brand mention.':'<b>Add value first.</b> At '+v+':'+pr+' you are under 9:1; contribute '+Math.max(0,(9*pr)-v)+' more before another mention.');
    var kv = k>=50?'cleared':'building';
    html+=metric('AutoMod karma threshold',kv,k>=50?'good':'warn',k>=50?'Past the 50-200 karma band that clears most AutoMod filters.':'<b>Keep commenting.</b> Reach 50+ comment karma before seeding; you have '+k+'.');
    var next = a<=14?'Subscribe to 10-15 subreddits; post 2-3 link-free comments a day.':(a<=30?'Comment 3-5x/day on rising and hot threads; bank karma. No links.':(linkOK?'Seed 1-2 original threads/month; one brand link/week, UTM stripped.':'Keep engaging until you clear 50 karma, then seed.'));
    html+=metric('Next action, '+phase+' phase','do this','warn',next);
    document.getElementById('wuMetrics').innerHTML=html;
  }
  [age,karma,val,promo].forEach(function(el){el.addEventListener('input',run);});
  run();
})();
</script>"""
T2=page("reddit-warmup-compliance-planner","Reddit Warm-Up & Compliance Planner",
 "Map your Reddit account to the 30-day warm-up protocol and 9:1 rule: which phase you're in, whether you can drop a brand link yet, your value-to-promotion ratio, and shadowban risk.",
 "Free Tool · Planner","Reddit Warm-Up & Compliance Planner",
 "Reddit shadowbans accounts that promote too early. Enter your account age, karma and activity to see your phase, your link gate, and your shadowban risk.",
 WU_CARD+"\n"+WU_METHOD, WU_JS)

# ============ TOOL 3: Engine Reddit-Reliance Planner ============
ER_CARD=('<section class="card"><div class="controls">'
 '<div class="fld"><label>Which engines are you targeting?</label>'
 '<div class="ptoggles" id="erTogs">'
 '<button class="ptog on" data-k="Perplexity" data-r="46.7">Perplexity</button>'
 '<button class="ptog on" data-k="Google AI Overviews" data-r="21.0">Google AI Overviews</button>'
 '<button class="ptog" data-k="ChatGPT" data-r="11.3">ChatGPT</button>'
 '<button class="ptog" data-k="Google AI Mode" data-r="9.0">Google AI Mode</button>'
 '<button class="ptog" data-k="Gemini" data-r="0.1">Gemini</button>'
 '</div><div class="hint">Each engine reads Reddit differently. Toggle your targets to get the recommended split between forum seeding and owned structured assets.</div></div>'
 '<div class="output" style="margin-top:22px"><div class="o-eyebrow">Recommended channel split</div>'
 '<div class="stacked" id="erStack" style="margin-top:10px"></div><div class="o-sub" id="erSplit" style="margin-top:10px">-</div>'
 '<div class="mx-grid" id="erRows" style="margin-top:12px"></div></div></section>')
ER_METHOD=('<section class="method"><h2>How this works</h2><p>Reddit citation share swings wildly by engine: Perplexity pulls Reddit in <strong>46.7%</strong> of top-10 citations, Google AI Overviews 21%, ChatGPT 11.3%, and Gemini almost never (~0.1%). So the channel mix depends entirely on who you are optimizing for: heavy forum seeding for the Reddit-reliant engines, owned structured assets and schema for Gemini. This planner averages the Reddit reliance of your selected engines and recommends a split.</p>'
 '<div class="srcs"><a href="/blogs/reddit-geo-playbook">The Reddit GEO Playbook &rarr;</a><a href="/blogs/ai-mode-vs-ai-overviews">AI Mode vs AI Overviews &rarr;</a></div></section>')
ER_JS=r"""<script>
(function(){
  var togs=document.getElementById('erTogs'); if(!togs) return;
  function band(r){return r>=30?['Reddit-led','#BC3F1D','seed forums hard']:(r>=10?['Reddit-assisted','#D4A34A','seed forums + owned']:(r>=5?['Light','#8A8278','some forum, mostly owned']:['Reddit-resistant','#3E9B6A','owned structured assets']));}
  function run(){
    var sel=[].slice.call(togs.querySelectorAll('.ptog.on'));
    var stack=document.getElementById('erStack'),split=document.getElementById('erSplit'),rows=document.getElementById('erRows');
    if(!sel.length){stack.innerHTML='';split.textContent='Select at least one engine.';rows.innerHTML='';return;}
    var avg=sel.reduce(function(a,b){return a+parseFloat(b.dataset.r);},0)/sel.length;
    var forum=Math.max(10,Math.min(75,Math.round(avg*1.4)));
    var owned=100-forum;
    stack.innerHTML='<span style="width:'+forum+'%;background:var(--signal)"></span><span style="width:'+owned+'%;background:rgba(255,255,255,.22)"></span>';
    split.innerHTML='<b style="color:#fff">'+forum+'% forum seeding</b> &middot; '+owned+'% owned structured assets &middot; avg Reddit reliance '+avg.toFixed(1)+'%';
    var html='';
    sel.sort(function(a,b){return parseFloat(b.dataset.r)-parseFloat(a.dataset.r);}).forEach(function(t){
      var r=parseFloat(t.dataset.r),bd=band(r);
      html+='<div class="mx-card"><div class="mx-h"><span class="mx-name">'+t.dataset.k+'</span><span class="mx-badge" style="color:'+bd[1]+'">'+bd[0]+'</span></div>'
        +'<div class="mx-row"><span class="k">Reddit share</span><span class="v">'+r+'% of top-10 citations</span></div>'
        +'<div class="mx-row"><span class="k">Play</span><span class="v">'+bd[2]+'</span></div></div>';
    });
    rows.innerHTML=html;
  }
  togs.addEventListener('click',function(e){var b=e.target.closest('.ptog');if(!b)return;b.classList.toggle('on');run();});
  run();
})();
</script>"""
T3=page("engine-reddit-reliance-planner","Engine Reddit-Reliance Planner",
 "Pick your target AI engines and get the recommended split between Reddit forum seeding and owned structured assets, based on each engine's Reddit citation share.",
 "Free Tool · Planner","Engine Reddit-Reliance Planner",
 "Reddit citation share swings from 46.7% (Perplexity) to 0.1% (Gemini). Select your target engines to get the right split between forum seeding and owned assets.",
 ER_CARD+"\n"+ER_METHOD, ER_JS)

for slug,html_ in [("reddit-thread-citability-scorer",T1),("reddit-warmup-compliance-planner",T2),("engine-reddit-reliance-planner",T3)]:
    open(f"tools/{slug}.html","w",encoding="utf-8").write(html_)
    m=list(re.finditer(r'<script>\n\(function\(\)\{.*?\}\)\(\);\n</script>', html_, re.S))
    if m:
        open("/tmp/tr.js","w").write(m[-1].group(0)[8:-9])
        r=subprocess.run(["node","--check","/tmp/tr.js"],capture_output=True,text=True)
        print(slug,"NODE:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:500])
    print("  styletags:",html_.count("<style>"),"jsonld:",html_.count("application/ld+json"),"em:",html_.count("—"),"curly:",html_.count("’")+html_.count("“"))

# embed thread scorer for the article
EMBED=('<section class="toolpage tool-embed">\n'
 '  <div class="embed-head"><div class="embed-eyebrow">Free interactive tool</div><div class="embed-title">Score a Reddit thread\'s citability</div><div class="embed-deck">Check any thread against the signature AI engines reward, question title, self-post, direct answer, named entities, and see the fixes. Votes excluded on purpose.</div></div>\n'
 +RT_CARD+'\n'
 '  <div class="embed-foot">A free rawmktg tool. <a href="/tools/reddit-thread-citability-scorer">Open the full tool &rarr;</a> &middot; <a href="/tools">see all tools</a></div>\n'
 '</section>\n'+RT_JS+'\n')
open("/tmp/rt_embed.html","w").write(EMBED)
print("embed bytes",len(EMBED)); print("DONE")
