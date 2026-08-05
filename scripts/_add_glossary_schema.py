#!/usr/bin/env python3
"""SCRATCH: add BreadcrumbList + Organization + Person JSON-LD to glossary entries
and the hub. Idempotent. Do NOT commit."""
import glob, re, json, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

ORG = {"@context":"https://schema.org","@type":"Organization","@id":"https://rawmktg.com/#organization",
       "name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
PERSON = {"@context":"https://schema.org","@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com",
          "sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}

def crumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u}
                               for i,(n,u) in enumerate(items)]}

def blocks(*objs):
    return "".join('  <script type="application/ld+json">'+json.dumps(o)+'</script>\n' for o in objs)

ICON = '  <link rel="icon" type="image/x-icon" href="/favicon.ico" />'

def inject(path, extra):
    h = open(path, encoding="utf-8").read()
    if '"@type": "BreadcrumbList"' in h or '"@type":"BreadcrumbList"' in h:
        return False
    assert ICON in h, f"icon anchor missing in {path}"
    h = h.replace(ICON, extra + ICON, 1)
    open(path, "w", encoding="utf-8").write(h)
    return True

# entries
n=0
for p in sorted(glob.glob("glossary/*.html")):
    h = open(p, encoding="utf-8").read()
    m = re.search(r'"@type": "DefinedTerm", "name": "(.*?)", "description".*?"url": "(https://rawmktg.com/glossary/[a-z0-9-]+)"', h)
    if not m:
        print("WARN no DefinedTerm in", p); continue
    name, url = m.group(1), m.group(2)
    bc = crumb([("rawmktg.","https://rawmktg.com/"),("Glossary","https://rawmktg.com/glossary"),(name,url)])
    if inject(p, blocks(bc, ORG, PERSON)): n+=1
print("entries with schema added:", n)

# hub
hub_bc = crumb([("rawmktg.","https://rawmktg.com/"),("Glossary","https://rawmktg.com/glossary")])
print("hub schema added:", inject("glossary.html", blocks(hub_bc, ORG, PERSON)))

# validate all JSON-LD parses
bad=0
for p in glob.glob("glossary/*.html")+["glossary.html"]:
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', open(p).read(), re.S):
        try: json.loads(blk)
        except Exception as e: print("BAD JSON",p,e); bad+=1
print("invalid JSON-LD blocks:", bad)
print("em dashes (glossary):", sum(open(p).read().count("—") for p in glob.glob("glossary/*.html"))+open("glossary.html").read().count("—"))
