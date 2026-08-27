#!/usr/bin/env python3
"""SCRATCH: append an auto-load-example + Clear demo bar to the 14 empty-on-load tools."""
import os, re, json
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

CVR_RAW="<h1>Acme Pricing</h1>\n<p>Choose a plan that fits your team.</p>"
CVR_REN=("<h1>Acme Pricing</h1>\n<p>Choose a plan that fits your team.</p>\n"
 "<div>Starter is $29 per seat per month with API access and email support. Pro is $99 per seat per month adding SSO, "
 "audit logs, and priority support. Enterprise is custom priced with a dedicated CSM, SAML, and a 99.9% uptime SLA. "
 "All plans include a 14 day free trial, unlimited projects, and no credit card required to start.</div>")
CSD_SAMPLE=("41% of B2B marketing teams published zero original research in 2025, up from 28% the year before.\n"
 "Source: RawMktg Original Research Census 2026, n=1,204, margin of error +/- 2.8pp.\n"
 "Most teams say research is important but few actually invest in it.\n"
 "\"Teams cut research first because it is the only line item with no weekly dashboard,\" said Priya Menon, VP Demand Generation at Northwind.\n"
 "Onboarding takes a significant amount of time for most mid-market accounts.\n"
 "Companies over 1,000 staff were 5x more likely to publish 3+ studies a year than those under 200, per the same survey.")
SDY_SAMPLE=("HOPS=0 STATUS=200  https://example.com/docs/architecture\n"
 "HOPS=2 STATUS=301  https://example.com/docs/rate-limits\n"
 "HOPS=3 STATUS=301  https://example.com/legacy/page\n"
 "HOPS=1 STATUS=302  https://example.com/promo\n"
 "HOPS=0 STATUS=404  https://example.com/removed")
LLMS_SAMPLE=("# Example\n\n> Example is a B2B analytics platform for product teams.\n\n"
 "## Docs\n- [Getting started](https://example.com/docs): Setup and your first dashboard\n"
 "- [API reference](https://example.com/api)\n- Pricing\n")
PSA_SAMPLE=('{"@context":"https://schema.org","@type":"Product",'
 '"name":"Acme Widget Pro","description":"A widget for teams.",'
 '"offers":{"@type":"Offer","price":"29.00","priceCurrency":"USD","availability":"https://schema.org/InStock"}}')
INB_URLS="https://example.com/docs/rate-limits\nhttps://example.com/blog/sitemap-audit"

CONFIGS={
 "sitemap-discovery-yield-auditor":{"root":"sdy","textareas":{"sdyIn":SDY_SAMPLE}},
 "citable-stat-density-scorer":{"root":"csd","textareas":{"csdIn":CSD_SAMPLE}},
 "content-visibility-ratio-checker":{"root":"cvr","textareas":{"cvrRaw":CVR_RAW,"cvrRen":CVR_REN}},
 "dark-ai-revenue-estimator":{"root":"dai","inputs":{"daiSess":"84000","daiConv":"3120","daiAcv":"9400"}},
 "lastmod-timestamp-trust-calculator":{"root":"ltt","inputs":{"lttStamp":"12000","lttReal":"500"}},
 "fan-out-content-brief-generator":{"root":"fbg","inputs":{"fbgTerm":"best container tracking software","fbgComp":"project44, FourKites"}},
 "indexnow-payload-builder":{"root":"inb","inputs":{"inbHost":"example.com","inbKey":"fa8c0a469da44e9b8f6a769f291829f5"},"textareas":{"inbUrls":INB_URLS}},
 "llms-txt-validator":{"root":"val","textareas":{"valIn":LLMS_SAMPLE}},
 "product-schema-auditor":{"root":"psa","textareas":{"psaText":PSA_SAMPLE}},
 "comparison-page-extractability-scorer":{"root":"cpe","inputs":{"cpeD":"7","cpeH":"80"},
    "clicks":['.iseg[data-f="P"] button[data-v="1"]','.iseg[data-f="N"] button[data-v="1"]']},
 "comparison-schema-generator":{"root":"csg","inputs":{"csgTitle":"Best CRM for startups","csgCat":"CRM software",
    "csgAName":"Acme CRM","csgAPrice":"29","csgAUnit":"seat/mo","csgARate":"4.6","csgARev":"812",
    "csgBName":"Rival CRM","csgBPrice":"49","csgBUnit":"seat/mo","csgBRate":"4.4","csgBRev":"540",
    "csgCName":"Budget CRM","csgCPrice":"15","csgCUnit":"seat/mo","csgCRate":"4.1","csgCRev":"305"}},
 "remediation-priority-scorer":{"root":"rps","inputs":{"rps_0_v":"0.08","rps_1_v":"0.2","rps_2_v":"0.35","rps_3_v":"0.9","rps_4_v":"0.95"}},
 "rendering-remediation-advisor":{"root":"rra","clicks":[
    '.iseg[data-f="freq"] button[data-v="realtime"]','.iseg[data-f="code"] button[data-v="modern"]','.iseg[data-f="scale"] button[data-v="small"]']},
 "ai-visibility-signal-diagnostic":{"root":"sd","clicks":[
    '.iseg[data-q="q1"] button[data-v="yes"]','.iseg[data-q="q2"] button[data-v="no"]','.iseg[data-q="q3"] button[data-v="no"]']},
}

TEMPLATE = """
<script>
/* demo: auto-load a worked example + clear */
(function(){
  var CFG=__CFG__;
  var CARD=document.getElementById(CFG.root); if(!CARD) return;
  if(CARD.querySelector('.demo-bar')) return;
  function fire(e){['input','change'].forEach(function(ev){try{e.dispatchEvent(new Event(ev,{bubbles:true}));}catch(x){}});}
  function loadExample(){
    var i,e;
    for(i in (CFG.inputs||{})){e=document.getElementById(i);if(e){e.value=CFG.inputs[i];fire(e);}}
    for(i in (CFG.textareas||{})){e=document.getElementById(i);if(e){e.value=CFG.textareas[i];fire(e);}}
    (CFG.clicks||[]).forEach(function(sel){var b=CARD.querySelector(sel);if(b)b.click();});
    setBar(true);
  }
  function clearAll(){
    CARD.querySelectorAll('input,textarea').forEach(function(e){var t=(e.type||'').toLowerCase();if(t==='button'||t==='submit')return;e.value='';fire(e);});
    CARD.querySelectorAll('.iseg button.on').forEach(function(b){b.classList.remove('on');});
    setBar(false);
  }
  var bar=document.createElement('div');
  bar.className='demo-bar';
  bar.style.cssText='display:flex;align-items:center;gap:8px;margin:0 0 14px;font-family:var(--f-mono,monospace);font-size:11.5px;flex-wrap:wrap;';
  function setBar(loaded){
    bar.innerHTML='';
    var lab=document.createElement('span');
    lab.style.cssText='color:var(--mute,#8a8a8a);';
    lab.textContent = loaded? 'Loaded with a worked example, edit it or' : 'Inputs cleared,';
    var btn=document.createElement('button');
    btn.type='button'; btn.className='tbtn';
    btn.textContent = loaded? 'Clear' : 'Load example';
    btn.addEventListener('click', loaded? clearAll : loadExample);
    bar.appendChild(lab); bar.appendChild(btn);
  }
  var host=CARD.querySelector('.controls .cat')||CARD.querySelector('.controls')||CARD;
  host.insertBefore(bar, host.firstChild);
  loadExample();
})();
</script>
"""

count=0
for slug,cfg in CONFIGS.items():
    f=f"tools/{slug}.html"
    s=open(f,encoding="utf-8").read()
    if 'demo: auto-load a worked example' in s:
        print("skip (already):",slug); continue
    cfg_json=json.dumps(cfg).replace("</","<\\/")  # keep any data value from closing the <script> tag
    snippet=TEMPLATE.replace("__CFG__", cfg_json)
    assert "</body>" in s
    s=s.replace("</body>", snippet+"\n</body>", 1)
    open(f,"w",encoding="utf-8").write(s)
    count+=1
    print("injected:",slug)
print("total injected:",count)
