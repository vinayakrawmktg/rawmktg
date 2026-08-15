#!/usr/bin/env python3
"""SCRATCH: fix 6 - comparison-schema-generator to N products (3) + currency selector."""
import os, re, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
F="tools/comparison-schema-generator.html"
h=open(F,encoding="utf-8").read()

# 1) currency selector after applicationCategory field
old_cur='<input class="tin" id="csgCat" value="BusinessApplication"></div></div>'
new_cur=('<input class="tin" id="csgCat" value="BusinessApplication"></div>'
 '<div class="fld"><div class="lab">Currency</div><select class="tin" id="csgCur">'
 '<option>USD</option><option>EUR</option><option>GBP</option><option>INR</option>'
 '<option>CAD</option><option>AUD</option><option>JPY</option><option>SGD</option><option>BRL</option><option>ZAR</option>'
 '</select></div></div>')
assert h.count(old_cur)==1; h=h.replace(old_cur,new_cur)

# 2) Product C (optional) after the B-cat hint
old_c='Render it server-side, and make every value match the visible copy on the page exactly.</p></div>'
new_c=(old_c+'      <div class="cat"><div class="cat-h">Product C (position 3, optional)</div><div class="num-grid">'
 '<div class="fld"><div class="lab">Name</div><input class="tin" id="csgCName" placeholder=""></div>'
 '<div class="fld"><div class="lab">Price</div><input class="tin" id="csgCPrice" inputmode="decimal" placeholder=""></div>'
 '<div class="fld"><div class="lab">Per (unit text)</div><input class="tin" id="csgCUnit" placeholder="per user per month"></div>'
 '<div class="fld"><div class="lab">Rating (optional)</div><input class="tin" id="csgCRate" inputmode="decimal" placeholder=""></div>'
 '<div class="fld"><div class="lab">Review count (optional)</div><input class="tin" id="csgCRev" inputmode="numeric" placeholder=""></div>'
 '</div></div>')
assert h.count(old_c)==1; h=h.replace(old_c,new_c)

# 3) prod() takes a currency
old_prod='var off={"@type":"Offer","price":price,"priceCurrency":"USD"}; if(unit) off.unitText=unit; o.offers=off;'
new_prod='var off={"@type":"Offer","price":price,"priceCurrency":cur}; if(unit) off.unitText=unit; o.offers=off;'
assert h.count(old_prod)==1; h=h.replace(old_prod,new_prod)
h=h.replace('function prod(name,cat,price,unit,rate,rev){','function prod(name,cat,price,unit,rate,rev,cur){',1)

# 4) build() loops over A/B/C with dynamic count + currency
old_build='''  function build(){
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
    out.textContent='<script type="application/ld+json">\\n'+JSON.stringify(obj,null,2)+'\\n<\\/script>';
  }'''
new_build='''  function build(){
    var out=document.getElementById('csgOut');
    var cat=v('csgCat')||'BusinessApplication', cur=v('csgCur')||'USD';
    var items=[];
    ['A','B','C'].forEach(function(K){
      var nm=v('csg'+K+'Name'); if(!nm) return;
      items.push(prod(nm,cat,v('csg'+K+'Price'),v('csg'+K+'Unit'),v('csg'+K+'Rate'),v('csg'+K+'Rev'),cur));
    });
    if(items.length<2){out.textContent='Enter at least two product names to generate the schema.';return;}
    var names=items.map(function(it){return it.name;});
    var title=v('csgTitle')||(names.join(' vs ')+' Comparison');
    var list=items.map(function(it,i){return {"@type":"ListItem","position":i+1,"item":it};});
    var obj={"@context":"https://schema.org","@type":"WebPage","name":title,"dateModified":today(),
      "mainEntity":{"@type":"ItemList","numberOfItems":items.length,"itemListElement":list}};
    out.textContent='<script type="application/ld+json">\\n'+JSON.stringify(obj,null,2)+'\\n<\\/script>';
  }'''
assert h.count(old_build)==1, "build block not found"; h=h.replace(old_build,new_build)

# 5) light deck copy: two -> two or three
h=h.replace("Enter two products and generate the nested JSON-LD, ready to server-render on your page.",
            "Enter two or three products and generate the nested JSON-LD, in your currency, ready to server-render on your page.",1)

open(F,"w",encoding="utf-8").write(h)
m=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>',h,re.S) if "getElementById('csg')" in s][-1]
open("/tmp/csg.js","w").write(m[8:-9])
r=subprocess.run(["node","--check","/tmp/csg.js"],capture_output=True,text=True)
print("csg node:", "OK" if r.returncode==0 else "FAIL "+r.stderr[:300])
print("has csgCur:", h.count('id="csgCur"'), "| csgCName:", h.count('id="csgCName"'), "| numberOfItems dynamic:", 'numberOfItems":items.length' in h)
