#!/usr/bin/env python3
"""SCRATCH one-off: add one concrete callout (example / research data point / common
mistake) to each glossary entry. Idempotent. Not part of the build. Do NOT commit."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CSS = """
    .gloss-callout{margin:34px 0 8px;padding:18px 20px;background:var(--paper-2);border:1px solid var(--rule);border-left:3px solid var(--signal);border-radius:8px;}
    .gloss-callout .cl-label{font-family:var(--f-mono);font-size:10px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:var(--signal);margin-bottom:10px;}
    .gloss-callout p{font-family:var(--f-prose);font-size:15px;line-height:1.7;color:var(--ink-2);margin-bottom:0;}
    .gloss-callout p+p{margin-top:12px;}
    .gloss-callout code{font-family:var(--f-mono);font-size:13px;background:var(--paper);padding:1px 5px;border-radius:4px;color:var(--ink);}
    .gloss-callout pre{font-family:var(--f-mono);font-size:12.5px;line-height:1.6;background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:12px 14px;overflow-x:auto;margin:0 0 10px;color:var(--ink);white-space:pre;}
"""

# slug -> (LABEL, inner-HTML)
C = {
"ai-overviews": ("Common mistake",
 "<p>Treating AI Overviews as a new channel you can win on formatting alone. Because 96% of citations go to sources Google already trusts on E-E-A-T grounds, a page with no classic search authority almost never appears. The overview is won upstream, by earning trust, not by restructuring a single page.</p>"),
"ai-referral-traffic": ("Common mistake",
 "<p>Reading a flat or rising <code>Direct</code> bucket in GA4 as genuinely direct. A large share of AI-assistant referrals lands there because the engine passes no referrer, so the channel that converts best (about 4.4x organic) is often the one teams cannot see.</p>"),
"answer-capsule": ("Example",
 "<p>A capsule: <em>\"A prompt portfolio is a fixed set of buyer-intent prompts a brand runs across AI engines on a cadence to measure citation visibility.\"</em></p>"
 "<p>Not a capsule: <em>\"In this guide we will explore why measurement matters and, eventually, get to what a prompt portfolio is.\"</em> The first stands alone and can be quoted verbatim; the second cannot.</p>"),
"answer-engine-optimization": ("Common mistake",
 "<p>Winning the on-page answer and stopping there. Clean answer formatting makes you eligible, but if the wider web carries no consistent signals about the brand, the engine still has little reason to name you over a better-known competitor.</p>"),
"answer-lead-formatting": ("Example",
 "<p>Narrative lead: <em>\"Marketing has shifted a lot since 2023. To see why, we first need to look at how buyers now search...\"</em></p>"
 "<p>Answer lead: <em>\"Answer-lead formatting puts the direct answer in the first sentence; the context follows.\"</em> Only the second gives a model something to extract from the top of the page.</p>"),
"authority-seeding": ("Common mistake",
 "<p>Briefing PR and content to chase links and counting nothing else. For AI citation the unlinked mention often matters more (r=0.664 versus r=0.218 for backlinks), so a programme optimised only for links leaves the stronger signal on the table.</p>"),
"brand-hallucination": ("From our research",
 "<p>In our senior-living teardown, one brand was being misclassified by AI at the moment of highest buyer intent: the engine described it as the wrong kind of provider, because the clean, structured signals needed to place it correctly were not there for the model to draw on.</p>"),
"citation-gap": ("Common mistake",
 "<p>Assuming strong rankings mean you are cited. Being indexed and being named in an answer are different events: a brand can rank on page one for its own category and still appear in none of the AI answers buyers actually read.</p>"),
"common-crawl-ccbot": ("Common mistake",
 "<p>Shipping a blanket <code>Disallow: /</code> or a catch-all bot block to \"stop the scrapers,\" then wondering why the brand is absent from AI tools. That one line also removes you from Common Crawl, the corpus many downstream models reuse.</p>"),
"content-half-life": ("Common mistake",
 "<p>Bumping the visible \"updated\" date without changing the content. Engines weigh actual substantive change, not the timestamp, so a cosmetic date edit does not reset the decay. Pages untouched for 90 days were 3.2x more likely to lose their citations entirely.</p>"),
"domain-rating": ("Common mistake",
 "<p>Setting a DR target as the GEO goal. In our teardowns, higher DR did not reliably predict AI citations; brands with modest DR sometimes out-cited far stronger domains, because citation rewards topical depth and trust that the score does not capture.</p>"),
"e-e-a-t": ("Common mistake",
 "<p>Treating E-E-A-T as a checklist, adding an author box and a few outbound links, with no demonstrable experience behind the content. The signal models reward is real, shown expertise; the decorations alone do not move it.</p>"),
"entity-resolution": ("Common mistake",
 "<p>Referring to the brand inconsistently across the web (<code>Acme</code>, <code>Acme Inc</code>, <code>Acme.io</code>, <code>Acme Software</code>). Each variant fragments the entity, so the system struggles to connect the mentions into one identity it can confidently resolve and recommend.</p>"),
"generative-engine-optimization": ("Common mistake",
 "<p>Treating GEO as SEO with schema bolted on. The on-page layer makes you eligible, but GEO also turns on off-site trust. With 73% of B2B procurement managers already using AI for vendor discovery, the brands that win are the ones the wider web vouches for, not just the ones with clean markup.</p>"),
"generative-engine": ("Common mistake",
 "<p>Optimising for one engine and assuming the rest follow. They retrieve and rank differently: only 11% of domains were cited by both ChatGPT and Perplexity for the same query, so winning one is no guarantee of the others.</p>"),
"gptbot-vs-oai-searchbot": ("Example",
 "<pre>User-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: GPTBot\nDisallow: /</pre>"
 "<p>This robots.txt keeps you eligible for citations in ChatGPT search while keeping your content out of model-training collection. A blanket block of all OpenAI bots gives up the first to get the second.</p>"),
"graph-schema": ("Example",
 "<pre>\"@graph\": [\n  { \"@type\": \"Organization\", \"@id\": \"#org\",  \"name\": \"rawmktg.\" },\n  { \"@type\": \"Person\",       \"@id\": \"#author\", \"name\": \"Vinayak Ravi\" },\n  { \"@type\": \"Article\", \"author\": {\"@id\": \"#author\"},\n    \"publisher\": {\"@id\": \"#org\"} }\n]</pre>"
 "<p>The <code>@id</code> references let a machine read one connected identity, this article, by this author, from this organisation, instead of three unrelated snippets.</p>"),
"knowledge-graph": ("Common mistake",
 "<p>Assuming a Wikipedia page is the only way in. Consistent structured data, matching entity references across the web, and authoritative mentions can establish a brand as a resolved, well-connected entity without one.</p>"),
"link-intersect": ("From our research",
 "<p>Across six India cross-border payments brands we overlapped roughly 9,515 referring pages from about 1,788 unique domains. The intersect surfaced the shared linkers and the topics that actually win links in the category, developer and payment-gateway content, rather than the cross-border angle everyone assumed.</p>"),
"llm-citation": ("Common mistake",
 "<p>Saving the key claim for the conclusion at the foot of the page. Citations cluster at the top, roughly 55% came from the first 30% of the page, so the strongest line is the least likely to be cited when it is left for last.</p>"),
"llms-txt": ("Example",
 "<pre># Acme\n\n&gt; Acme builds X for Y teams.\n\n## Key pages\n- [What is X](https://acme.com/x): one-line summary\n- [Pricing](https://acme.com/pricing): one-line summary</pre>"
 "<p>A single static file at <code>/llms.txt</code>. In our AEC teardown, zero of six competitors had published one.</p>"),
"oai-searchbot": ("Common mistake",
 "<p>Relying on a framework that renders the main content in the browser. OAI-SearchBot does not execute JavaScript, so content that only appears after client-side rendering is invisible to it. Allow the bot all you like and it still sees an empty shell.</p>"),
"perplexitybot": ("Common mistake",
 "<p>Blocking it unintentionally at the CDN or WAF layer. Aggressive bot-mitigation rules often catch PerplexityBot by default, quietly removing you from a citation-first engine without anyone choosing to.</p>"),
"prompt-portfolio": ("Example",
 "<p>Segment by intent and fix the wording, then reuse it every cycle:</p>"
 "<pre>Money:   \"best [category] software for enterprise\"\nProblem: \"how to reduce [pain] in [workflow]\"\nProof:   \"is [brand] a good [category] tool\"</pre>"
 "<p>Keeping the set identical run to run is what makes the numbers comparable.</p>"),
"prompt-to-citation-tracking": ("Common mistake",
 "<p>Trying to read AI visibility out of GA4 alone. It misses roughly 30% of AI referrers and misclassifies many of the rest, so the only reliable read is to run a fixed prompt set against the engines and record the citations yourself.</p>"),
"proof-pairing-density": ("Example",
 "<p>Unpaired claim: <em>\"Fresh content does better in AI search.\"</em></p>"
 "<p>Paired claim: <em>\"Pages not updated in 90 days were 3.2x more likely to lose their AI citations.\"</em> The Princeton GEO study found adding statistics lifted visibility by ~41% and citing sources by up to 115%; the paired version is the one a model can extract and attribute.</p>"),
"referring-domains": ("Common mistake",
 "<p>Reporting total backlinks instead of unique referring domains. One partner site linking 200 times is 200 backlinks but a single referring domain, and the inflated number hides how few distinct sources actually endorse the brand.</p>"),
"retrieval-augmented-generation": ("Common mistake",
 "<p>Investing in page-level authority while burying the answer mid-article. RAG competes at the passage level: if there is no clean, self-contained passage near the top, a strong page can still be passed over for a weaker one that is easier to retrieve.</p>"),
"schema-markup": ("Common mistake",
 "<p>Marking up content that is not actually visible on the page, or whose claims the body does not support. Engines cross-check schema against on-page content; mismatched markup reads as low-trust and can do more harm than shipping none.</p>"),
"share-of-model": ("Example",
 "<p>Compute it as a simple share. Across a fixed prompt set run on a cadence:</p>"
 "<pre>Share of Model = answers that name your brand / total answers</pre>"
 "<p>measured against your competitive set. A move from 2 of 50 to 12 of 50 is a tracked, reportable gain.</p>"),
"topical-authority": ("Example",
 "<p>A cluster, not a page: one hub on the core topic plus linked entries on each sub-question, so the engine reads one coherent body of expertise. This glossary is built that way, a hub plus 32 connected entries, each linking to the deeper article behind it.</p>"),
"unlinked-brand-mentions": ("Common mistake",
 "<p>Measuring a PR or content programme only by links earned. The unlinked mention, the brand named in a trusted article with no hyperlink, correlated about 3x more strongly with AI citation than backlinks (r=0.664 versus r=0.218), so a links-only scorecard undercounts the work that matters most.</p>"),
}

def block(label, inner):
    return (f'      <div class="gloss-callout">\n'
            f'        <div class="cl-label">{label}</div>\n'
            f'        {inner}\n'
            f'      </div>\n')

done = 0; missing = []
for path in sorted(glob.glob("glossary/*.html")):
    slug = os.path.basename(path)[:-5]
    if slug not in C:
        missing.append(slug); continue
    h = open(path, encoding="utf-8").read()
    if "gloss-callout" in h:
        continue  # idempotent
    if "</style>" in h and ".gloss-callout{" not in h:
        h = h.replace("</style>", CSS + "  </style>", 1)
    label, inner = C[slug]
    foot = '<div class="gloss-foot">'
    assert foot in h, f"no gloss-foot in {slug}"
    h = h.replace(foot, block(label, inner) + "      " + foot, 1)
    open(path, "w", encoding="utf-8").write(h)
    done += 1

print(f"enriched {done} entries; no-content slugs: {missing or 'none'}; "
      f"callouts defined: {len(C)}")
em = 0
for p in glob.glob("glossary/*.html"):
    em += open(p, encoding="utf-8").read().count("—")
print("em dashes across entries:", em)
