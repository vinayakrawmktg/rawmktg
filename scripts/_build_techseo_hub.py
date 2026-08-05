#!/usr/bin/env python3
"""SCRATCH: rebuild /glossary hub as a unified, filterable hub with two collections
(AI Search & GEO + Technical SEO). Do NOT commit."""
import re, json, html as H

ROOT="/sessions/optimistic-youthful-planck/mnt/rawmktg"
import os; os.chdir(ROOT)

# --- parse the uploaded index for ordered tech groups ---
idx=open("/tmp/seoglossary/nested/index.md",encoding="utf-8").read()
groups=[]  # (label, [(name, slug, shortdef)])
cur=None
for line in idx.splitlines():
    if line.startswith("## "):
        cur=(line[3:].strip(), []); groups.append(cur)
    elif line.startswith("- ") and cur is not None:
        m=re.match(r'- \*\*\[(.+?)\]\(([^)]+)\)\*\*\s*(?:→|->)\s*(.+)', line)
        if m:
            name=m.group(1).strip()
            slug=m.group(2).split("/")[-1].strip()
            sd=m.group(3).strip().replace("—",", ").replace("–","-")
            cur[1].append((name,slug,sd))

def esc(t): return H.escape(t, quote=False)

h=open("glossary.html",encoding="utf-8").read()

# --- 1. hero rebrand ---
h=h.replace('<div class="eyebrow">AI-Search Glossary</div>','<div class="eyebrow">rawmktg. Glossary</div>')
h=h.replace('<h1>The vocabulary of AI search, defined.</h1>','<h1>The B2B search glossary, defined.</h1>')
h=h.replace('AI search introduced a new working vocabulary, and most of it is still being defined in real time. This glossary is our attempt to define it plainly and accurately: what each term means, how the mechanism actually works, and why it matters for a B2B brand trying to get cited.',
 'Two connected vocabularies in one place: the language of AI search and GEO, and the technical SEO foundations underneath it. Pick a collection or search to filter; without JavaScript every term still shows, so crawlers and readers always get the full list.')

# --- 2. CSS ---
css='''    .collection-head{margin:8px 0 4px;padding-top:8px;}
    .collection-head .ch-kicker{font-family:var(--f-mono);font-size:10px;font-weight:600;letter-spacing:0.20em;text-transform:uppercase;color:var(--signal);margin-bottom:8px;}
    .collection-head h2{font-family:var(--f-display);font-weight:700;font-size:26px;letter-spacing:-0.02em;color:var(--ink);padding-bottom:14px;border-bottom:2px solid var(--ink);}
    .gloss-filter{position:sticky;top:60px;z-index:90;background:var(--paper);border-bottom:1px solid var(--rule);padding:16px 0;margin-bottom:8px;}
    .gloss-filter .gf-inner{display:flex;flex-wrap:wrap;align-items:center;gap:12px;}
    .gf-search{flex:1;min-width:200px;padding:11px 14px;background:var(--paper-2);border:1px solid var(--rule-2);border-radius:6px;font-family:var(--f-prose);font-size:14px;color:var(--ink);outline:none;transition:border-color .15s;}
    .gf-search::placeholder{color:var(--mute);}
    .gf-search:focus{border-color:var(--signal);}
    .gf-pills{display:flex;gap:8px;flex-wrap:wrap;}
    .gf-pill{font-family:var(--f-mono);font-size:11px;font-weight:600;letter-spacing:0.10em;text-transform:uppercase;color:var(--ink-2);background:var(--paper);border:1px solid var(--rule-2);border-radius:999px;padding:8px 16px;cursor:pointer;transition:all .15s;}
    .gf-pill:hover{border-color:var(--ink);}
    .gf-pill.active{background:var(--ink);color:var(--paper);border-color:var(--ink);}
    .gf-count{font-family:var(--f-mono);font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:var(--mute);white-space:nowrap;}
    .gf-empty{display:none;font-family:var(--f-prose);font-size:15px;color:var(--mute);padding:32px 0;}
'''
h=h.replace('</style>', css+'  </style>',1)

# --- 3. tag existing AI groups ---
h=h.replace('<div class="gloss-group">','<div class="gloss-group" data-collection="ai">')

# --- 4. filter bar + AI collection head before first group ---
bar='''<div class="gloss-filter">
        <div class="gf-inner">
          <input type="search" class="gf-search" placeholder="Search terms..." aria-label="Search glossary terms" />
          <div class="gf-pills">
            <button class="gf-pill active" data-filter="all">All</button>
            <button class="gf-pill" data-filter="ai">AI Search &amp; GEO</button>
            <button class="gf-pill" data-filter="tech">Technical SEO</button>
          </div>
          <span class="gf-count"></span>
        </div>
      </div>
      <div class="collection-head" data-collection="ai">
        <div class="ch-kicker">Collection 01</div>
        <h2>AI Search &amp; GEO</h2>
      </div>
      '''
h=h.replace('<div class="gloss-group" data-collection="ai">', bar+'<div class="gloss-group" data-collection="ai">',1)

# --- 5. build Technical SEO collection ---
tech=['      <div class="collection-head" data-collection="tech">',
      '        <div class="ch-kicker">Collection 02</div>',
      '        <h2>Technical SEO</h2>','      </div>']
for label, terms in groups:
    tech.append('      <div class="gloss-group" data-collection="tech">')
    tech.append(f'        <div class="gloss-group-label">{esc(label)}</div>')
    for name,slug,sd in terms:
        tech.append(f'        <a href="/glossary/{slug}" class="term-row">')
        tech.append(f'          <span class="term-name">{esc(name)} <span class="term-arrow" aria-hidden="true">&rarr;</span></span>')
        tech.append(f'          <div class="term-def">{esc(sd)}</div>')
        tech.append('        </a>')
    tech.append('      </div>')
tech.append('      <div class="gf-empty">No terms match your search.</div>')
techhtml="\n".join(tech)+"\n"
h=h.replace('    </div>\n  </div>\n</main>', '    </div>\n'+techhtml+'  </div>\n</main>',1)

# --- 6. filter JS before </body> ---
js='''<script>
(function(){
  var s=document.querySelector('.gf-search'),pills=[].slice.call(document.querySelectorAll('.gf-pill')),
      groups=[].slice.call(document.querySelectorAll('.gloss-group')),
      heads=[].slice.call(document.querySelectorAll('.collection-head')),
      count=document.querySelector('.gf-count'),empty=document.querySelector('.gf-empty'),
      active='all',q='';
  function apply(){
    var shown=0;
    groups.forEach(function(g){
      var col=g.getAttribute('data-collection'),byPill=(active==='all'||active===col),any=false;
      [].slice.call(g.querySelectorAll('.term-row')).forEach(function(r){
        var ok=byPill&&(q===''||r.textContent.toLowerCase().indexOf(q)>-1);
        r.style.display=ok?'':'none'; if(ok){any=true;shown++;}
      });
      g.style.display=any?'':'none';
    });
    heads.forEach(function(hd){
      var col=hd.getAttribute('data-collection'),byPill=(active==='all'||active===col),
          has=groups.some(function(g){return g.getAttribute('data-collection')===col&&g.style.display!=='none';});
      hd.style.display=(byPill&&has)?'':'none';
    });
    count.textContent=shown+' term'+(shown===1?'':'s');
    empty.style.display=shown===0?'block':'none';
  }
  pills.forEach(function(p){p.addEventListener('click',function(){pills.forEach(function(x){x.classList.remove('active');});p.classList.add('active');active=p.getAttribute('data-filter');apply();});});
  s.addEventListener('input',function(){q=s.value.trim().toLowerCase();apply();});
  apply();
})();
</script>
'''
h=h.replace('</body>', js+'</body>',1)

# --- 7. rebuild DefinedTermSet from all term-rows ---
rows=re.findall(r'<a href="(/glossary/[a-z0-9-]+)" class="term-row">\s*<span class="term-name">(.+?) <span', h)
terms_json=[{"@type":"DefinedTerm","name":H.unescape(n.strip()),"url":"https://rawmktg.com"+u} for u,n in rows]
dts={"@context":"https://schema.org","@type":"DefinedTermSet","name":"rawmktg. Glossary",
     "url":"https://rawmktg.com/glossary",
     "description":"Definitions of the vocabulary of AI search, GEO, and technical SEO for B2B brands.",
     "hasDefinedTerm":terms_json}
h=re.sub(r'<script type="application/ld\+json">\{"@context"[^<]*?DefinedTermSet.*?</script>',
         '<script type="application/ld+json">'+json.dumps(dts)+'</script>', h, count=1, flags=re.S)

# --- 8. hub title/meta update ---
h=h.replace('<title>The AI-Search Glossary','<title>The B2B Search Glossary')
h=re.sub(r'(<title>)[^<]*(</title>)', r'\1The B2B Search Glossary &middot; rawmktg.\2', h, count=1)

open("glossary.html","w",encoding="utf-8").write(h)
print("hub rebuilt. tech groups:",len(groups),"| total terms in DefinedTermSet:",len(terms_json))
print("em dashes in hub:", h.count("—"))
