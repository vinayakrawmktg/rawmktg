#!/usr/bin/env python3
"""SCRATCH: reorder tools.html tiles newest-first by git add-date (stable ties)."""
import os, re, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
s=open("tools.html",encoding="utf-8").read()

tile_re=re.compile(r'<a class="tool-tile"[^>]*href="/tools/([a-z0-9-]+)"[\s\S]*?</a>')
matches=list(tile_re.finditer(s))
assert matches, "no tiles"
start=matches[0].start(); end=matches[-1].end()
# ensure the gaps between tiles are whitespace only (safe to rewrite the whole span)
prev=None
for m in matches:
    if prev is not None:
        gap=s[prev:m.start()]
        assert gap.strip()=="", f"non-whitespace between tiles: {gap!r}"
    prev=m.end()
print("tiles:", len(matches))

def added(slug):
    for args in (["git","log","--diff-filter=A","--format=%at","--","tools/"+slug+".html"],
                 ["git","log","--format=%at","--","tools/"+slug+".html"]):
        out=subprocess.run(args,capture_output=True,text=True).stdout.strip().splitlines()
        if out: return int(out[-1])
    return 0

items=[]
for i,m in enumerate(matches):
    items.append((added(m.group(1)), i, m.group(1), m.group(0)))
items.sort(key=lambda x:(-x[0], x[1]))  # newest first, stable on ties

new_span="\n".join("      "+blk for *_,blk in [(a,b,c,d) for a,b,c,d in items])
s2=s[:start]+new_span+s[end:]
open("tools.html","w",encoding="utf-8").write(s2)

print("=== NEW ORDER (top 12) ===")
for a,b,slug,_ in items[:12]: print("  ",slug)
print("tile count after:", s2.count('class=\"tool-tile\"'),
      "| unique:", len(set(re.findall(r'href="/tools/([a-z0-9-]+)"', s2))))