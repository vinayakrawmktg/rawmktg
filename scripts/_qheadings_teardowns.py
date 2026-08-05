#!/usr/bin/env python3
"""SCRATCH: convert finding headings to question format across the 6 teardowns.
Folds the original heading into the bold lead of its answer capsule where one exists,
and updates the sidebar TOC. Do NOT commit."""
import re, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

# file -> list of (id, new_inner_heading, bold_lead_or_None)
CONFIG = {
"blogs/aec-ai-visibility-gap.html": [
  ("visibility-gap","How many AEC software vendors actually get cited by AI?","Wider than expected, and starkly concentrated."),
  ("organic-vs-ai","Does high organic traffic mean high AI visibility?","No, the two do not correlate."),
  ("platform-behavior","Which AI platforms cite AEC software the most?","The six platforms behave very differently."),
  ("visible-factors","What do the AEC vendors AI does cite have in common?","A shared set of off-site and content signals."),
  ("llms-txt","Why does llms.txt matter for AEC software vendors?","It is the missing infrastructure, and nobody had it."),
],
"blogs/india-senior-living-ai-visibility-gap.html": [
  ("benchmark","How do India's top senior-living brands compare on SEO and AI visibility?","We benchmarked the three most prominent players."),
  ("seo-gap","What is the real SEO gap for India's senior-living brands?","It is not about more content."),
  ("citation-quality","Why are some AI citations worth more than others?","Not all citations are equal."),
],
"blogs/autonomous-retail-ai-visibility-gap.html": [
  ("data","What does the autonomous-retail AI-visibility data actually show?","It is striking."),
  ("neuroshop","Which autonomous-retail company cracked AI visibility?","Neuroshop, a DR-16 underdog, figured it out."),
  ("ai-search","What is AI search doing to the autonomous-retail market?","It is concentrating visibility fast."),
],
"blogs/cx-saas-seo-discoverability-analysis.html": [
  ("f1","1. Which CX SaaS companies dominate organic traffic, and by how much?","Organic traffic is dramatically unequal, even within the same market."),
  ("f2","2. Is technical SEO undermining CX SaaS content investment?","Yes, across the board."),
  ("f3","3. Is the CX SaaS content funnel inverted?","Yes, everyone is playing at the top."),
  ("f4","4. Where are CX SaaS deals actually won in search?","In the MOFU layer, and it is almost empty."),
  ("f5","5. What is wrong with CX SaaS backlink profiles?","A gap problem and a quality problem."),
  ("f6","6. Is AI visibility the new CX SaaS moat?","Yes, and almost no one is building it."),
],
"blogs/cross-border-backlinks.html": [
  ("category-at-a-glance","How should you compare cross-border payments backlink profiles?","Not by raw counts."),
  ("link-quality","How much do spam links distort cross-border backlink counts?","Link quality is the hidden variable."),
  ("topic-spread","Which topics actually win links in cross-border payments?","Far more than just cross-border itself."),
  ("three-shapes","What are the three backlink-profile shapes in cross-border payments?","Scale, focus, and one outlier."),
  ("adjacent-topics","Which adjacent topics earn the links?","A handful of payment-adjacent subjects do the work."),
],
"blogs/container-tracking-saas-seo-geo-analysis.html": [
  ("f1","Finding 1: How bad is the AI visibility problem in container tracking?",None),
  ("f2","Finding 2: How concentrated is domain authority in container tracking?",None),
  ("f3","Finding 3: Why is every container-tracking site over-indexed on informational traffic?",None),
  ("f4","Finding 4: What carrier-tracking-page strategy do the winners use?",None),
  ("f5","Finding 5: Is container-tracking organic traffic geographically misaligned with the ICP?",None),
  ("f6","Finding 6: Why are container-tracking referring-domain profiles structurally weak?",None),
  ("f7","Finding 7: Is the container-tracking traffic gap accelerating?",None),
],
}

total_h=total_cap=total_toc=0
for path, items in CONFIG.items():
    h=open(path,encoding="utf-8").read()
    for sid,newinner,lead in items:
        # 1. replace h2 inner (preserve optional section-num span); capture old inner for TOC
        pat=re.compile(r'(<h2 id="'+re.escape(sid)+r'">)(<span class="section-num">\d+</span>)?(.*?)(</h2>)', re.S)
        mm=pat.search(h)
        if not mm:
            print("MISS h2", path, sid); continue
        old_inner=mm.group(3)
        h=pat.sub(lambda m: m.group(1)+(m.group(2) or '')+newinner+m.group(4), h, count=1)
        total_h+=1
        # 2. capsule lead (only if capsule follows this h2 and lead given)
        if lead:
            cpat=re.compile(r'(<h2 id="'+re.escape(sid)+r'">.*?</h2>\s*<div class="section-answer">)(?!<strong>)', re.S)
            h2c=cpat.sub(lambda m: m.group(1)+'<strong>'+lead+'</strong> ', h, count=1)
            if h2c!=h: total_cap+=1; h=h2c
        # 3. TOC: replace remaining occurrence of old_inner (now only in toc) with newinner
        old_plain=re.sub(r'<[^>]+>','',old_inner).strip()
        if old_plain and old_plain in h:
            h=h.replace(old_plain, re.sub(r'<[^>]+>','',newinner).strip(), 1); total_toc+=1
    open(path,"w",encoding="utf-8").write(h)

print(f"headings converted: {total_h} | capsule leads added: {total_cap} | toc updated: {total_toc}")
# em-dash check across edited files
em=sum(open(p).read().count("—") for p in CONFIG)
print("em dashes across edited teardowns:", em)
