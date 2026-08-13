#!/usr/bin/env python3
"""SCRATCH: build 2 new tools (crawl-depth estimator, off-site authority scorecard) + embed + rebuild hub(11). Do NOT commit."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
os.makedirs("tools", exist_ok=True)
T=open("blogs/property-vista-authority-paradox.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE=''  # AdSense removed: no ad units, hurts TBT
def esc(t): return H.escape(t,quote=False)
def escq(t): return H.escape(t,quote=True)
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
ORG={"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
OG="https://rawmktg.com/assets/images/og-default.png"

# ---------------- tool definitions ----------------
CD_CARD = """<section class="card" id="cdTool">
  <div class="grid calc">
    <div class="controls">
      <div class="fld"><div class="lab">Clicks from the homepage <span class="val" id="cdDepthVal">3 hops</span></div>
        <input type="range" id="cdDepth" min="0" max="6" value="3">
        <p class="hint">How many clicks a crawler needs to reach this page from your homepage.</p></div>
      <div class="tactic on" id="cdMappedWrap"><div class="trow">
        <button class="switch on" id="cdMapped" aria-pressed="true" aria-label="In sitemap and llms.txt"></button>
        <span class="tname">Page is in your sitemap &amp; llms.txt</span></div>
        <p class="hint" style="margin-top:8px">Discovery files help real-time agents reach deeper pages, worth roughly one hop.</p></div>
    </div>
    <div class="output">
      <div class="o-eyebrow">Real-time retrieval probability</div>
      <div class="o-lift" id="cdProb">70%</div>
      <div class="o-sub" id="cdSub">depth 3 from the homepage</div>
      <div style="margin:2px 0 16px"><span class="verdict warn" id="cdVerdict">AT RISK</span></div>
      <div class="barrow"><span class="l">Reachability</span><div class="track"><div class="fill proj" id="cdFill"></div></div></div>
      <div class="chips" id="cdChips"></div>
      <p class="caveat">Models real-time retrieval probability by crawl depth (100 / 96 / 88 / 70 / 42 / 20% at depths 0-5), grounded in the internal-linking-for-AI-retrieval research. Real-time agents have seconds to fetch a URL; past depth 3 retrieval falls off a cliff. Directional.</p>
    </div>
  </div>
</section>"""
CD_JS = """(function(){
  var root=document.getElementById('cdTool'); if(!root) return;
  var depth=document.getElementById('cdDepth');
  var CURVE={0:100,1:96,2:88,3:70,4:42,5:20,6:8};
  function verdict(p){if(p>=95)return['REACHED','good'];if(p>=85)return['SAFE','good'];if(p>=60)return['AT RISK','warn'];if(p>=35)return['TIMEOUT','warn'];return['DROPPED','bad'];}
  function compute(){
    var d=parseInt(depth.value,10);
    document.getElementById('cdDepthVal').textContent=d+(d===1?' hop':' hops');
    var mapped=document.getElementById('cdMapped').classList.contains('on');
    document.getElementById('cdMappedWrap').classList.toggle('off',!mapped);
    var eff=Math.max(0,d-(mapped?1:0));
    var p=CURVE[eff]!==undefined?CURVE[eff]:Math.max(2,Math.round(8*Math.pow(0.5,eff-6)));
    document.getElementById('cdProb').textContent=p+'%';
    var v=verdict(p); var pill=document.getElementById('cdVerdict'); pill.textContent=v[0]; pill.className='verdict '+v[1];
    document.getElementById('cdFill').style.width=p+'%';
    document.getElementById('cdSub').textContent=mapped?('effective depth '+eff+' with sitemap + llms.txt'):('depth '+d+' from the homepage');
    var br=document.getElementById('cdChips'); br.innerHTML='';
    function chip(t,m){var c=document.createElement('span');c.className='chip'+(m?' muted':'');c.textContent=t;br.appendChild(c);}
    if(d>3) chip('Flatten to 3 hops or fewer'); else chip('Within the safe zone');
    if(!mapped) chip('Add to sitemap + llms.txt', true);
  }
  depth.addEventListener('input',compute);
  document.getElementById('cdMapped').addEventListener('click',function(){this.classList.toggle('on');compute();});
  compute();
})();"""
CD_METHOD = ('<section class="method"><h2>How this works</h2>'
 '<p>Real-time AI retrieval agents (OAI-SearchBot, PerplexityBot) have only seconds to discover and fetch a URL before the model answers. The deeper a page sits from your homepage, the less likely it is reached in time. This tool maps your page\'s click-depth onto a modeled retrieval-probability curve, and a working sitemap plus llms.txt effectively shortens that path by about one hop.</p>'
 '<p>Keep every key asset within 2-3 hops. Directional, not a crawl simulation.</p>'
 '<div class="srcs"><a href="/blogs/internal-linking-for-ai-retrieval">Internal linking for AI retrieval &rarr;</a><a href="/blogs/how-ai-crawlers-index-your-site">How AI crawlers index your site &rarr;</a></div></section>')

OS_ITEMS=[
 ("Tier 1, review ecosystem","40 pts",[
   (15,"G2 profile complete & review-rich","Fill your G2 profile with descriptive, metric-rich reviews, the material engines lift directly."),
   (13,"Profiles across G2, Capterra, TrustRadius, Clutch","Multi-platform consensus can make a model up to 3x more likely to cite you."),
   (12,"Mapped to the right (and newest) G2 categories","Engines use G2 category mappings to retrieve the competitor set for category prompts."),
 ]),
 ("Tier 2, analyst relations","25 pts",[
   (13,"Open, crawlable analyst review profiles kept fresh","96% of analyst citations come from open review directories, not gated flagship reports."),
   (12,"Vendor-hosted, structured accolade pages","Publish declarative accolade summaries on your own crawlable site so models can verify them."),
 ]),
 ("Tier 3, community presence","20 pts",[
   (10,"Authentic, aged Reddit presence","Reddit drives 46.7% of Perplexity citations; aged expert accounts, not brand-new profiles."),
   (10,"Citation-ready, structured comments","Answer-first, credentialed, with numbers and an honest caveat, the shape engines extract."),
 ]),
 ("Entity & consistency","15 pts",[
   (8,"Entity schema with sameAs to off-site profiles","Link your entity to G2, LinkedIn, Crunchbase and Wikidata so mentions resolve to you."),
   (7,"Consistent metrics across every surface","Inconsistent pricing or specs make models skip you to avoid error."),
 ]),
]
def os_card():
    cats=""
    for title,pts,items in OS_ITEMS:
        rows=""
        for w,name,act in items:
            rows+=(f'<div class="item" data-w="{w}" data-act="{escq(act)}"><span class="iname">{esc(name)}</span>'
                   '<div class="iseg"><button data-m="0" class="sel">No</button><button data-m="0.5">Partial</button><button data-m="1">Yes</button></div></div>')
        cats+=f'<div class="cat"><div class="cat-h">{esc(title)} <span>{esc(pts)}</span></div>{rows}</div>'
    return ('<section class="card"><div class="grid score">'
      f'<div class="checklist" id="osChecklist">{cats}</div>'
      '<div class="panel-out"><div class="o-eyebrow">Off-site authority score</div>'
      '<div class="scorewrap"><span class="score" id="osScore">0</span><span class="score-d">/100</span></div>'
      '<span class="scoreband" id="osBand">-</span>'
      '<div class="gauge"><div class="gfill" id="osFill"></div></div>'
      '<div class="gscale"><span>Invisible</span><span>Developing</span><span>Cited-ready</span></div>'
      '<div class="gaps" id="osGaps"></div>'
      '<p class="caveat">A weighted self-assessment across the off-site authority stack AI engines pull from: review ecosystem, analyst relations, community presence, and entity consistency. Weights reflect each tier\'s pull on AI citations; real results depend on execution and competitive context.</p>'
      '</div></div></section>')
OS_JS = """(function(){
  var list=document.getElementById('osChecklist'); if(!list) return;
  var BANDS=[{max:40,label:'Invisible',color:'#BC3F1D'},{max:70,label:'Developing',color:'#8A8278'},{max:100,label:'Cited-ready',color:'#3E9B6A'}];
  function bandFor(s){for(var i=0;i<BANDS.length;i++){if(s<=BANDS[i].max)return BANDS[i];}return BANDS[2];}
  function hexToRgb(h){h=h.replace('#','');return [parseInt(h.substr(0,2),16),parseInt(h.substr(2,2),16),parseInt(h.substr(4,2),16)].join(',');}
  function compute(){
    var score=0,gaps=[];
    list.querySelectorAll('.item').forEach(function(it){
      var w=parseFloat(it.dataset.w),sel=it.querySelector('.iseg button.sel'),m=sel?parseFloat(sel.dataset.m):0;
      score+=w*m; var un=w*(1-m); if(un>0) gaps.push({name:it.querySelector('.iname').textContent,act:it.dataset.act,pts:un});
    });
    score=Math.round(score); var band=bandFor(score);
    document.getElementById('osScore').textContent=score;
    var b=document.getElementById('osBand'); b.textContent=band.label; b.style.background='rgba('+hexToRgb(band.color)+',.18)'; b.style.color=band.color;
    var f=document.getElementById('osFill'); f.style.width=score+'%'; f.style.background=band.color;
    gaps.sort(function(a,b){return b.pts-a.pts;}); var top=gaps.slice(0,3); var g=document.getElementById('osGaps');
    if(!top.length){g.innerHTML='<div class="gaps-h">Priority fixes</div><div class="allset">Every tier covered. Maintain the lead, refresh reviews and community presence quarterly.</div>';return;}
    var html='<div class="gaps-h">Priority fixes, biggest unrealized points</div>';
    top.forEach(function(gp,i){html+='<div class="gap"><span class="rk">'+(i+1)+'</span><div style="flex:1"><div class="gt">'+gp.name+'</div><div class="ga">'+gp.act+'</div></div><span class="pts">+'+Math.round(gp.pts)+'</span></div>';});
    g.innerHTML=html;
  }
  list.addEventListener('click',function(e){var b=e.target.closest('.iseg button');if(!b)return;b.parentElement.querySelectorAll('button').forEach(function(x){x.classList.remove('sel');});b.classList.add('sel');compute();});
  compute();
})();"""
OS_METHOD=('<section class="method"><h2>How this works</h2>'
 '<p>AI engines are consensus engines: they corroborate your claims across the off-site authority stack before recommending you. Review sites alone drive up to 85% of B2B category citations. This scorecard weights the four tiers, the review ecosystem, analyst relations, community presence, and entity consistency, by their pull on AI citations, then ranks your biggest unrealized points.</p>'
 '<div class="srcs"><a href="/blogs/why-ai-cites-reddit-g2-analysts">Why AI cites Reddit, G2 &amp; analysts &rarr;</a><a href="/blogs/authority-seeding-ai-llm-trust">Authority seeding for AI trust &rarr;</a></div></section>')

NEW=[
 {"slug":"crawl-depth-retrieval-estimator","title":"Crawl-Depth Retrieval Estimator","cat":"Free Tool · Estimator","grid":"calc","appcat":"BusinessApplication",
  "deck":"Enter a page's click-depth from your homepage and see how likely real-time AI agents are to reach it before they time out.",
  "desc":"Estimate a page's real-time AI retrieval probability by crawl depth, grounded in the depth curve where retrieval falls off a cliff past 3 hops.",
  "card":CD_CARD,"js":CD_JS,"method":CD_METHOD,
  "embed":{"blog":"blogs/internal-linking-for-ai-retrieval.html","eyebrow":"Free interactive tool","title":"Estimate your page's retrieval probability","deck":"Enter how many clicks a page sits from your homepage to see whether real-time AI agents can reach it in time."}},
 {"slug":"off-site-authority-scorecard","title":"Off-Site Authority Stack Scorecard","cat":"Free Tool · Diagnostic","grid":"score","appcat":"BusinessApplication",
  "deck":"Score your presence across the off-site authority stack AI engines pull from, review sites, analysts, Reddit, and entity schema, and get your gaps ranked.",
  "desc":"Rate your off-site authority across review sites, analyst relations, community presence, and entity consistency, with your biggest citation gaps ranked.",
  "card":os_card(),"js":OS_JS,"method":OS_METHOD,
  "embed":{"blog":"blogs/why-ai-cites-reddit-g2-analysts.html","eyebrow":"Free interactive tool","title":"Score your off-site authority stack","deck":"Rate your presence across review sites, analysts, Reddit and entity schema to find the gaps capping your AI citations."}},
]

def shell(t):
    URL=f"https://rawmktg.com/tools/{t['slug']}"; title=t["title"]; desc=t["desc"]; deck=t["deck"]
    webapp={"@context":"https://schema.org","@type":"WebApplication","name":title,"url":URL,"description":desc,"applicationCategory":t["appcat"],"operatingSystem":"Web, all browsers","browserRequirements":"Requires JavaScript","isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"}}
    webpage={"@context":"https://schema.org","@type":"WebPage","name":title,"url":URL,"description":desc,"isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://rawmktg.com/tools"},{"@type":"ListItem","position":3,"name":title,"item":URL}]}
    head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
      "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
      f"  <title>{esc(title)} &middot; Free GEO Tool &middot; rawmktg.</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
      f"  <meta name=\"description\" content=\"{escq(desc)}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
      "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
      "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
      "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
      "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
      f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
      f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en-IN" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
      "  <meta property=\"og:type\" content=\"website\" />\n"
      f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{escq(title)}\" />\n"
      f"  <meta property=\"og:description\" content=\"{escq(desc)}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
      f'  <meta property="og:image" content="{OG}" />\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />\n'
      "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
      f"  <meta name=\"twitter:title\" content=\"{escq(title)}\" />\n  <meta name=\"twitter:description\" content=\"{escq(desc)}\" />\n  <meta name=\"twitter:image\" content=\"{OG}\" />\n"
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
    e=t["embed"]; path=e["blog"]; h=open(path,encoding="utf-8").read()
    if 'href="/assets/tools.css"' not in h: h=h.replace("</head>",'  <link rel="stylesheet" href="/assets/tools.css" />\n</head>',1)
    frag=('\n<section class="toolpage tool-embed">\n  <div class="embed-head">'
      f'<div class="embed-eyebrow">{esc(e["eyebrow"])}</div><div class="embed-title">{esc(e["title"])}</div>'
      f'<div class="embed-deck">{esc(e["deck"])}</div></div>\n'+t["card"]+
      f'\n  <div class="embed-foot">A free rawmktg tool. <a href="/tools/{t["slug"]}">Open the full tool &rarr;</a> &middot; <a href="/tools">see all tools</a></div>\n</section>\n<script>\n'+t["js"]+'\n</script>\n')
    idx=h.find('<div class="faq-section"')
    if idx==-1: idx=h.find("</main>")
    h=h[:idx]+frag+"\n"+h[idx:]; open(path,"w",encoding="utf-8").write(h); return "faq" if '<div class="faq-section"' in h else "main"

for t in NEW:
    em=shell(t); pl=embed(t); print(f"  built tools/{t['slug']}.html (em:{em}) embedded->{t['embed']['blog'].split('/')[-1]} @ {pl}")

# rebuild hub with all 11
HUB=[{"slug":t["slug"],"title":t["title"],"cat":t["cat"],"desc":t["desc"]} for t in NEW]+[
 {"slug":"content-recency-decay","title":"Content Recency Decay Estimator","cat":"Free Tool · Estimator","desc":"Estimate how fast a page's AI citations decay by engine, and get a refresh-by date."},
 {"slug":"page-citability-analyzer","title":"Page Citability Analyzer","cat":"Free Tool · Analyzer","desc":"Paste a page and score its citability against high-citation benchmarks; get the fixes that matter."},
 {"slug":"claim-anchoring-validator","title":"Claim-Anchoring Validator","cat":"Free Tool · Validator","desc":"Validate a page against the four-part Claim-Anchoring framework and get a hallucination-risk score."},
 {"slug":"ai-platform-optimizer","title":"AI Platform Optimization Matrix","cat":"Free Tool · Matrix","desc":"Pick your target AI engines and content type for per-engine structure, schema and cadence."},
 {"slug":"saas-funnel-gap-analyzer","title":"B2B SaaS Funnel Gap Analyzer","cat":"Free Tool · Analyzer","desc":"See your TOFU/MOFU/BOFU balance against a citation-optimized split and the gaps to close."},
 {"slug":"geo-readiness-scorecard","title":"GEO Readiness Scorecard","cat":"Free Tool · Diagnostic","desc":"Score your brand's readiness to be cited by AI across crawlability, authority, Information Gain, and structure."},
 {"slug":"content-mix-planner","title":"GEO Content-Mix Planner","cat":"Free Tool · Planner","desc":"Turn your monthly content capacity into a citation-optimized mix: flagship, derivative, product, news."},
 {"slug":"zero-click-traffic-risk","title":"Zero-Click Traffic-at-Risk Estimator","cat":"Free Tool · Estimator","desc":"Estimate how much organic traffic is exposed to zero-click erosion as AI answers expand."},
 {"slug":"geo-lift-calculator","title":"GEO Lift Calculator","cat":"Free Tool · Calculator","desc":"Model the AI citation lift on your Share of Model using the Princeton/KDD GEO coefficients."},
]
HUBURL="https://rawmktg.com/tools"
tiles="".join(f'<a class="tool-tile" href="/tools/{x["slug"]}"><div class="tt-cat">{esc(x["cat"])}</div><div class="tt-name">{esc(x["title"])}</div><div class="tt-desc">{esc(x["desc"])}</div><div class="tt-go">Open tool &rarr;</div></a>\n      ' for x in HUB)
itemlist={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"https://rawmktg.com/tools/{x['slug']}","name":x["title"]} for i,x in enumerate(HUB)]}
coll={"@context":"https://schema.org","@type":"CollectionPage","name":"Free GEO & AI-search tools","url":HUBURL,"description":"Free interactive tools to measure and improve your brand's visibility in AI search.","isPartOf":{"@type":"WebSite","name":"rawmktg.","url":"https://rawmktg.com"}}
crumbH={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":"Tools","item":HUBURL}]}
HDESC="Free interactive tools to measure and improve your brand's visibility in AI search: readiness, content mix, zero-click risk, citation lift, recency decay, page citability, hallucination risk, engine optimization, funnel balance, crawl depth, and off-site authority."
oldhub=open("tools.html",encoding="utf-8").read()
newgrid='<div class="tools-grid">\n      '+tiles+'\n    </div>'
hub=re.sub(r'<div class="tools-grid">.*?</div>\s*</div>\s*</main>', newgrid+'\n  </div>\n</main>', oldhub, count=1, flags=re.S)
hub=re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m:m.group(1)+escq(HDESC)+m.group(2), hub, count=1)
# refresh ItemList schema in hub
hub=re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "ItemList".*?</script>', jb(itemlist), hub, count=1, flags=re.S)
open("tools.html","w",encoding="utf-8").write(hub)
print("  hub tiles now:",hub.count("tool-tile"))

# sitemap + llms
s=open("sitemap.xml").read()
for t in NEW:
    u=f"https://rawmktg.com/tools/{t['slug']}"
    if u+"<" not in s:
        a=s.find("<loc>https://rawmktg.com/tools/"); us=s.rfind("<url>",0,a)
        s=s[:us]+f"<url>\n    <loc>{u}</loc>\n    <lastmod>2026-06-13</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>\n  "+s[us:]
open("sitemap.xml","w").write(s)
l=open("llms.txt").read()
idx=l.find("- [All tools]")
add=""
for t in NEW:
    u=f"https://rawmktg.com/tools/{t['slug']}"
    if u+")" not in l: add+=f"- [{t['title']}]({u}) - {t['desc']}\n"
l=l[:idx]+add+l[idx:]; open("llms.txt","w").write(l)
print("  sitemap + llms updated. DONE")
