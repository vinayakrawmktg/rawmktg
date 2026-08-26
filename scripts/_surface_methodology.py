#!/usr/bin/env python3
"""SCRATCH: surface /methodology site-wide (footer, sitemap, llms) + build twin."""
import os, re, glob, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

# 1. footer link site-wide: insert Methodology between About and Contact (footer-specific sequence)
pat=re.compile(r'(<a href="/about">About</a>\s*)(<a href="/contact">Contact</a>)')
ins=r'\1<a href="/methodology">Methodology</a>\n        \2'
changed=0
for f in glob.glob("**/*.html", recursive=True):
    if f.startswith("research/") or f.startswith("design/"): continue
    s=open(f,encoding="utf-8").read()
    if 'href="/methodology">Methodology</a>' in s and pat.search(s) is None:
        continue
    ns,n=pat.subn(ins,s)
    if n:
        open(f,"w",encoding="utf-8").write(ns); changed+=1
print("footer link added to", changed, "files")

# 2. sitemap.xml (add near topics/tools with priority 0.8)
s=open("sitemap.xml",encoding="utf-8").read()
if "rawmktg.com/methodology" not in s:
    anc='  <url>\n    <loc>https://rawmktg.com/tools</loc>'
    assert anc in s, "tools anchor missing in sitemap"
    block=('  <url>\n    <loc>https://rawmktg.com/methodology</loc>\n    <lastmod>2026-08-26</lastmod>\n'
           '    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
    s=s.replace(anc, block+anc, 1)
    open("sitemap.xml","w",encoding="utf-8").write(s)
    print("sitemap: methodology added")
else:
    print("sitemap: already present")

# 3. llms.txt (add as a top-level line under the docs/optional section; put near top after first article group)
s=open("llms.txt",encoding="utf-8").read()
if "rawmktg.com/methodology" not in s:
    line="- [The rawmktg Measurement Methodology](https://rawmktg.com/methodology) - The canonical, versioned standard behind every visibility figure rawmktg publishes. Prompt portfolio tiers (baseline 50-150, decision-grade 250-500, enterprise 500+); a fixed 8 to 12 runs per prompt per engine (default 10) at every tier; per-engine reporting with evidence-based weights; 95% Wilson intervals and response-level bootstrap; a 200-observation per brand-engine cell reporting floor; monthly cadence on a frozen versioned portfolio; and a decision-grade vs directional labelling rule. Version 1.0, effective 26 August 2026, with a changelog.\n"
    anc="- [The Broken-Sitemap Tax: XML Sitemaps for AI Discovery]"
    assert anc in s
    s=s.replace(anc, line+anc, 1)
    open("llms.txt","w",encoding="utf-8").write(s)
    print("llms.txt: methodology added")
else:
    print("llms.txt: already present")
print("done")
