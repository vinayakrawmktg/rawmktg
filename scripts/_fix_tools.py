#!/usr/bin/env python3
"""SCRATCH: apply section-9 fixes 1,2,3,4,7 to tool source. Do NOT commit as content."""
import os, re, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

def patch(path, edits):
    h=open(path,encoding="utf-8").read()
    for old,new in edits:
        assert old in h, f"NOT FOUND in {path}:\n{old[:80]}"
        assert h.count(old)==1, f"AMBIGUOUS in {path} ({h.count(old)}x):\n{old[:80]}"
        h=h.replace(old,new)
    open(path,"w",encoding="utf-8").write(h)

def nodecheck(path,cid):
    h=open(path,encoding="utf-8").read()
    m=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>',h,re.S) if "getElementById('"+cid+"')" in s][-1]
    open("/tmp/ft.js","w").write(m[8:-9])
    r=subprocess.run(["node","--check","/tmp/ft.js"],capture_output=True,text=True)
    return "OK" if r.returncode==0 else "FAIL "+r.stderr[:300]

# ---- FIX 1: retrieval-readiness-checklist (denominator = answered, not 8) ----
patch("tools/retrieval-readiness-checklist.html",[
 ("var total=ITEMS.length, sum=vals.reduce(function(a,b){return a+b;},0);\n    var score=Math.round((sum/total)*100);",
  "var answered=vals.length, sum=vals.reduce(function(a,b){return a+b;},0);\n    var score=answered?Math.round((sum/answered)*100):0;"),
 ("document.getElementById('rrcDone').textContent=vals.length+'/'+total;",
  "document.getElementById('rrcDone').textContent=vals.length+' / '+ITEMS.length+' answered';"),
])

# ---- FIX 2: entity-readiness-scorecard (weighted layers, not flat) ----
patch("tools/entity-readiness-scorecard.html",[
 ("var vals=Object.keys(state).map(function(k){return state[k];}).filter(function(x){return x!==null;});\n    var total=Object.keys(state).length;\n    var sum=vals.reduce(function(a,b){return a+b;},0);\n    var score=Math.round((sum/total)*100);",
  "var CW=[0.35,0.30,0.25,0.10], acc=0, covW=0;\n    CATS.forEach(function(c,ci){\n      var ks=c[1].map(function(_,ii){return ci+'-'+ii;}).filter(function(k){return state[k]!==null;});\n      if(!ks.length) return;\n      var s=ks.reduce(function(a,k){return a+state[k];},0)/ks.length;\n      acc+=CW[ci]*s; covW+=CW[ci];\n    });\n    var score=covW?Math.round((acc/covW)*100):0;"),
 ("three sequential gates, ","four weighted layers, "),
 ("Fail gate one and the rest is irrelevant.",
  "Understandability is weighted highest (0.35), then Credibility (0.30), Deliverability (0.25) and NEEATT Notability (0.10), because a machine that cannot parse who you are will not credit anything else."),
])

# ---- FIX 3: facet-coverage-auditor (wire fcaTopic into the briefs) ----
patch("tools/facet-coverage-auditor.html",[
 ("var state={};\n  function compute(){\n    var covered=0, gaps=[];",
  "var state={};\n  var topicEl=document.getElementById('fcaTopic');\n  function compute(){\n    var topic=(topicEl.value||'').trim();\n    var covered=0, gaps=[];"),
 ("<span style=\"color:rgba(255,255,255,.4)\">'+CORP[i]+'</span></span><strong style=\"color:var(--signal)\">write it</strong>",
  "<span style=\"color:rgba(255,255,255,.4)\">'+CORP[i]+(topic?' &middot; for &ldquo;'+topic+'&rdquo;':'')+'</span></span><strong style=\"color:var(--signal)\">write it</strong>"),
 ("  });\n  compute();\n})();\n</script>",
  "  });\n  topicEl.addEventListener('input',compute);\n  compute();\n})();\n</script>"),
])

# ---- FIX 4: claim-anchoring-validator (invert to an anchoring score) ----
patch("tools/claim-anchoring-validator.html",[
 ("var comp=capPct*0.28+autoPct*0.24+ratioScore*0.30+brandScore*0.18, risk=Math.round((1-comp)*100);",
  "var comp=capPct*0.28+autoPct*0.24+ratioScore*0.30+brandScore*0.18, score=Math.round(comp*100);"),
 ("document.getElementById('caScore').textContent=risk;",
  "document.getElementById('caScore').textContent=score;"),
 ("(risk<=35?'low risk':(risk<=60?'moderate risk':'high risk'))",
  "(score>=65?'well anchored':(score>=40?'partly anchored':'hallucination risk'))"),
 ('<div class="o-eyebrow">Hallucination-risk score</div>',
  '<div class="o-eyebrow">Claim-anchoring score</div>'),
])

# ---- FIX 7: sentiment-share-of-voice-calculator (keep competitor names) ----
patch("tools/sentiment-share-of-voice-calculator.html",[
 (r"""    var brand=n('ssBrand'),rivals=0,names=0;
    document.getElementById('ssComp').value.split('\n').forEach(function(line){
      line=line.trim(); if(!line) return;
      var m=line.match(/(-?\d+(\.\d+)?)\s*$/);
      if(m){rivals+=Math.max(0,parseFloat(m[1]));names++;}
    });""",
  r"""    var brand=n('ssBrand'),rivals=0,names=0,rlist=[];
    document.getElementById('ssComp').value.split('\n').forEach(function(line){
      line=line.trim(); if(!line) return;
      var m=line.match(/(-?\d+(\.\d+)?)\s*$/);
      if(m){var cnt=Math.max(0,parseFloat(m[1])),nm=line.slice(0,m.index).replace(/[\s,:;|\-]+$/,'').trim()||('Competitor '+(names+1));rivals+=cnt;names++;rlist.push([nm,cnt]);}
    });"""),
 ("if(sov!==null){ msgs.push('Share of voice '+sov.toFixed(1)+'% against '+names+' competitor'+(names===1?'':'s')+' ('+rivals+' mentions).'); }",
  "if(sov!==null){ msgs.push('Share of voice '+sov.toFixed(1)+'% against '+names+' competitor'+(names===1?'':'s')+' ('+rivals+' mentions).'); }\n    if(rlist.length){ rlist.sort(function(a,b){return b[1]-a[1];}); msgs.push('Competitor set (your alias table): '+rlist.map(function(r){return r[0]+' &middot; '+r[1];}).join(', ')+'.'); }"),
])

for cid,f in [("rrc","retrieval-readiness-checklist"),("ers","entity-readiness-scorecard"),("fca","facet-coverage-auditor"),("caTool","claim-anchoring-validator"),("ss","sentiment-share-of-voice-calculator")]:
    print(f"{f:38} node:{nodecheck('tools/'+f+'.html',cid)}")
