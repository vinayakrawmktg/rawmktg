#!/usr/bin/env python3
"""SCRATCH: extend platform-weighted-visibility-calculator with a Share of Model output."""
import os, re, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
F="tools/platform-weighted-visibility-calculator.html"
h=open(F,encoding="utf-8").read()

ENG=[("chatgpt","ChatGPT"),("gemini","Gemini"),("perplexity","Perplexity"),("claude","Claude"),("grok","Grok")]

# 1) add a "Field mentions" input per engine, right after the weight fld / before the erow closes
for e,E in ENG:
    old=f'value="0.30" aria-label="Pv {e} w"></div></div>' if e=="chatgpt" else None
# generic: match the weight input for each engine and add the field fld before the erow closing </div>
for e,E in ENG:
    pat=re.compile(r'(id="pv_'+e+r'_w"[^>]*></div>)</div>')
    add=(f'<div class="fld"><div class="lab">Field mentions (all vendors)</div>'
         f'<input class="tin" id="pv_{e}_f" inputmode="numeric" value="" aria-label="Pv {e} field mentions"></div></div>')
    h2=pat.sub(lambda m: m.group(1)+add, h, count=1)
    assert h2!=h, f"field input not added for {e}"
    h=h2

# 2) update the intro hint to mention the optional field column
h=h.replace('Default weights are market-share estimates; edit them for your market.',
            'Default weights are market-share estimates; edit them for your market. "Field mentions" is optional, the total brand-mentions across every vendor in the same responses; fill it to also get your Share of Model.',1)

# 3) add a Share of Model output block after the per-engine breakdown, inside panel-out
somblock=('<div id="pvBreak"></div></div>\n'
  '      <div style="margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,.08)">\n'
  '        <div class="o-eyebrow">Share of Model <span style="color:rgba(255,255,255,.4);text-transform:none;letter-spacing:0">, share of the field</span></div>\n'
  '        <div class="scorewrap"><span class="score" id="pvSom">&ndash;</span><span class="score-d">%</span></div>\n'
  '        <div class="gaps"><div id="pvSomNote"><p class="hint">Add "field mentions" per engine to compute your weighted share of the whole competitive field.</p></div></div>\n'
  '      </div>')
h=h.replace('<div id="pvBreak"></div></div>', somblock, 1)

# 4) replace the compute script with a version that also computes Share of Model
new_script=r'''<script>
(function(){
  var root=document.getElementById('pv'); if(!root) return;
  var ENG=[['chatgpt','ChatGPT'],['gemini','Gemini'],['perplexity','Perplexity'],['claude','Claude'],['grok','Grok']];
  function num(id){var el=document.getElementById(id); if(!el) return null; var v=parseFloat(el.value);return isNaN(v)?null:v;}
  function compute(){
    var score=0,covered=0,rows=[];
    var somScore=0,somCov=0,somRows=[];
    ENG.forEach(function(e){
      var m=num('pv_'+e[0]+'_m'),q=num('pv_'+e[0]+'_q'),w=num('pv_'+e[0]+'_w'),f=num('pv_'+e[0]+'_f');
      if(q===null||q<=0||w===null||w<0){return;}
      var mm=(m===null?0:m); var pct=Math.max(0,Math.min(100,100*mm/q));
      score+=w*pct; covered+=w; rows.push([e[1],pct,w]);
      if(f!==null&&f>0){var sp=Math.max(0,Math.min(100,100*mm/f)); somScore+=w*sp; somCov+=w; somRows.push([e[1],sp]);}
    });
    var out=covered>0?score/covered:0;
    var scoreEl=document.getElementById('pvScore'),bandEl=document.getElementById('pvBand'),fill=document.getElementById('pvFill'),br=document.getElementById('pvBreak');
    if(covered<=0){scoreEl.textContent='0';bandEl.textContent='Enter counts';bandEl.style.background='rgba(255,255,255,.1)';bandEl.style.color='#fff';fill.style.width='0%';br.innerHTML='<p class="hint">Per-engine numbers appear here.</p>';}
    else{
      scoreEl.textContent=out.toFixed(1); fill.style.width=Math.min(100,out)+'%';
      var lbl,col;
      if(out>=50){lbl='Strong';col='var(--up)';}else if(out>=25){lbl='Building';col='#C9922E';}else{lbl='At risk';col='var(--signal)';}
      bandEl.textContent=lbl; bandEl.style.background=col; bandEl.style.color='#0b0b0c'; fill.style.background=col;
      rows.sort(function(a,b){return b[1]-a[1];});
      br.innerHTML=rows.map(function(r){
        return '<div class="lt-stat"><span>'+r[0]+' <span style="color:rgba(255,255,255,.4)">(w '+r[2]+')</span></span><strong>'+r[1].toFixed(1)+'%</strong></div>';
      }).join('');
    }
    var somEl=document.getElementById('pvSom'),somNote=document.getElementById('pvSomNote');
    if(somEl){
      if(somCov<=0){somEl.textContent='–';somNote.innerHTML='<p class="hint">Add "field mentions" per engine to compute your weighted share of the whole competitive field.</p>';}
      else{
        var som=somScore/somCov; somEl.textContent=som.toFixed(1);
        somRows.sort(function(a,b){return b[1]-a[1];});
        var note=somRows.map(function(r){return '<div class="lt-stat"><span>'+r[0]+'</span><strong>'+r[1].toFixed(1)+'%</strong></div>';}).join('');
        somNote.innerHTML=note+'<p class="hint" style="margin-top:8px">Your weighted presence as a share of total field presence. Weight the engines your buyers use; report the per-engine cut alongside the headline.</p>';
      }
    }
  }
  root.querySelectorAll('input').forEach(function(i){i.addEventListener('input',compute);});
  compute();
})();
</script>'''
old_script=re.search(r"<script>\s*\(function\(\)\{\s*var root=document\.getElementById\('pv'\);.*?\}\)\(\);\s*</script>", h, re.S)
assert old_script, "pv script not found"
h=h[:old_script.start()]+new_script+h[old_script.end():]

# 5) copy refresh: title, headline, deck, description, eyebrow, method
h=h.replace('<title>Platform-Weighted Visibility Calculator &middot; Free Tool &middot; rawmktg.</title>',
            '<title>Platform-Weighted Visibility &amp; Share of Model Calculator &middot; rawmktg.</title>',1)
h=h.replace('<h1 class="article-headline">Platform-Weighted Visibility Calculator</h1>',
            '<h1 class="article-headline">Platform-Weighted Visibility &amp; Share of Model Calculator</h1>',1)
h=h.replace('Pooling every engine into one average hides where you actually win. Enter your counts per engine and get a weighted visibility score that renormalises over the engines you track, plus the per-engine breakdown.',
            'Pooling every engine into one average hides where you actually win. Enter your counts per engine for a weighted visibility score that renormalises over the engines you track, and add field mentions to get your Share of Model, your weighted presence as a share of the whole competitive field.',1)
h=h.replace('content="Enter per-engine mention and prompt counts and compute a weighted AI-visibility score with renormalisation and a per-engine breakdown."',
            'content="Compute a platform-weighted AI-visibility score and your Share of Model (weighted presence as a share of the competitive field), with per-engine renormalisation and breakdown."',1)
h=h.replace('<span class="eyebrow-tag">Measurement Taxonomy &middot; Calculator</span>',
            '<span class="eyebrow-tag">Ranking &amp; Measurement &middot; Calculator</span>',1)
# method: add a Share of Model paragraph + cross-link
h=h.replace('<p>Run a fixed prompt set 3 to 5 times per engine and average before entering counts, single runs are noisy.</p><div class="srcs"><a href="/blogs/citation-vs-mention-vs-recommendation">The measurement taxonomy &rarr;</a><a href="/blogs/prompt-to-citation-tracking">Prompt-to-citation tracking &rarr;</a></div>',
            '<p>Visibility is your rate; Share of Model is your <em>share of the field</em>. Enter the total brand-mentions across every vendor in the same responses as "field mentions", and the tool divides your weighted presence by the weighted field presence. Run a fixed prompt set 8 to 12 times per engine and average before entering counts, single runs are noisy.</p><div class="srcs"><a href="/blogs/share-of-model-measurement">Share of Model, measured properly &rarr;</a><a href="/blogs/citation-vs-mention-vs-recommendation">The measurement taxonomy &rarr;</a><a href="/blogs/prompt-to-citation-tracking">Prompt-to-citation tracking &rarr;</a></div>',1)

open(F,"w",encoding="utf-8").write(h)

# verify
ms=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', h, re.S) if "getElementById('pv')" in s]
open("/tmp/pv.js","w").write(ms[-1][8:-9])
r=subprocess.run(["node","--check","/tmp/pv.js"],capture_output=True,text=True)
print("NODE:", "OK" if r.returncode==0 else "FAIL "+r.stderr[:400])
print("field inputs:", sum(h.count(f'id="pv_{e}_f"') for e,_ in ENG), "| pvSom:", h.count('id="pvSom"'),
      "| som link:", h.count('/blogs/share-of-model-measurement'), "| title has SoM:", 'Share of Model Calculator &middot; rawmktg' in h)
