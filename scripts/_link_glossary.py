#!/usr/bin/env python3
"""SCRATCH one-off: add inline contextual links from glossary entries to the relevant
blogs (body + callout), on top of the Go-deeper footer. Idempotent. Do NOT commit."""
import glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

LINK_CSS = """    .gloss-wrap p a,.gloss-callout a{color:var(--signal);border-bottom:1px solid var(--signal-soft);padding-bottom:0.5px;transition:border-color 0.15s;}
    .gloss-wrap p a:hover,.gloss-callout a:hover{border-color:var(--signal);}
"""

# slug -> list of (exact anchor text already in the page, blog slug to link to)
LINKS = {
"ai-overviews": [("96% of AI Overview citations go to sources Google already trusts on E-E-A-T grounds", "eeat-is-an-ai-signal-now")],
"ai-referral-traffic": [("AI-sourced sessions converted at roughly 4.4x the organic rate", "prompt-to-citation-tracking")],
"answer-capsule": [("roughly 55% of citations came from the first 30% of the page", "anatomy-of-a-high-citation-page")],
"answer-engine-optimization": [("the off-site authority work that AEO does not cover", "authority-seeding-ai-llm-trust")],
"answer-lead-formatting": [("roughly 55% of citations came from the first 30% of the page", "anatomy-of-a-high-citation-page")],
"authority-seeding": [("unlinked brand mentions correlated with AI citation visibility far more strongly than traditional backlinks", "authority-seeding-ai-llm-trust")],
"brand-hallucination": [("clear claim-anchoring", "hallucination-proofing-your-brand"),
                        ("senior-living teardown", "india-senior-living-ai-visibility-gap")],
"citation-gap": [("39x ChatGPT citation gap in senior living", "india-senior-living-ai-visibility-gap"),
                 ("4 of 6 vendors in the AEC software space", "aec-ai-visibility-gap")],
"common-crawl-ccbot": [("your robots.txt decides whether it may", "how-ai-crawlers-index-your-site")],
"content-half-life": [("pages not updated in 90 days were 3.2x more likely to lose their AI citations entirely", "30-day-content-half-life-recency-ai-ranking-signal")],
"domain-rating": [("high DR did not reliably predict AI citation visibility", "container-tracking-saas-seo-geo-analysis")],
"e-e-a-t": [("96% of AI Overview citations went to sources Google already trusts on E-E-A-T grounds", "eeat-is-an-ai-signal-now")],
"entity-resolution": [("resolves entities through Google's Knowledge Graph before it retrieves content", "why-engines-recommend-different-vendors")],
"generative-engine-optimization": [("73% of B2B procurement managers already use ChatGPT, Claude, or Perplexity for vendor discovery", "geo-compounding-flywheel")],
"generative-engine": [("only 11% of domains were cited by both ChatGPT and Perplexity for the same query", "why-engines-recommend-different-vendors")],
"gptbot-vs-oai-searchbot": [("configured separately in robots.txt", "how-ai-crawlers-index-your-site")],
"graph-schema": [("a single structured-data block", "schema-markup-ai-citations-2026")],
"knowledge-graph": [("the knowledge graph is often consulted before retrieval", "why-engines-recommend-different-vendors")],
"link-intersect": [("India's cross-border payments brands", "cross-border-backlinks")],
"llm-citation": [("roughly 55% of citations came from the first 30% of the document", "anatomy-of-a-high-citation-page")],
"llms-txt": [("In rawmktg's AEC teardown, zero of six companies had published an llms.txt file", "aec-ai-visibility-gap")],
"oai-searchbot": [("none of the three major AI crawlers run JS", "how-ai-crawlers-index-your-site")],
"perplexitybot": [("It also does not render JavaScript", "how-ai-crawlers-index-your-site")],
"prompt-portfolio": [("money, problem and proof intent", "prompt-to-citation-tracking")],
"prompt-to-citation-tracking": [("GA4 misses roughly 30% of AI referrers and misclassifies many of the rest", "prompt-to-citation-tracking")],
"proof-pairing-density": [("The Princeton GEO study found this directly", "hallucination-proofing-your-brand")],
"referring-domains": [("In rawmktg's CX SaaS teardown, the spread ran to thousands of missing referring domains", "cx-saas-seo-discoverability-analysis")],
"retrieval-augmented-generation": [("fetches candidate passages, reranks them by relevance and authority", "how-rag-actually-works")],
"schema-markup": [("53% of AI-cited pages carried valid schema", "schema-markup-ai-citations-2026")],
"share-of-model": [("GA4 misses roughly 30% of AI referrers", "prompt-to-citation-tracking")],
"topical-authority": [("a hub on the core topic plus connected entries on the sub-questions around it", "topical-authority-cluster-ai-shortlists")],
"unlinked-brand-mentions": [("unlinked mentions correlated with AI citation roughly three times more strongly than backlinks", "authority-seeding-ai-llm-trust")],
}

total = 0; problems = []
for path in sorted(glob.glob("glossary/*.html")):
    slug = os.path.basename(path)[:-5]
    h = open(path, encoding="utf-8").read()
    if ".gloss-wrap p a{" not in h and "</style>" in h:
        h = h.replace("</style>", LINK_CSS + "  </style>", 1)
    for anchor, blog in LINKS.get(slug, []):
        target = f'<a href="/blogs/{blog}">{anchor}</a>'
        if target in h:
            continue  # already linked (idempotent)
        n = h.count(anchor)
        if n == 0:
            problems.append(f"{slug}: ANCHOR NOT FOUND -> {anchor!r}"); continue
        h = h.replace(anchor, target, 1)
        total += 1
    open(path, "w", encoding="utf-8").write(h)

print(f"inline links added: {total}")
print("problems:", problems or "none")
em = sum(open(p, encoding="utf-8").read().count("—") for p in glob.glob("glossary/*.html"))
print("em dashes across entries:", em)
