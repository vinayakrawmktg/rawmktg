#!/usr/bin/env python3
"""Enhance /tools pages: add How-to + FAQ (+FAQPage schema) + Related block + meta fixes. Reusable per batch."""
import os, re, json, html as H, sys
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

def _meta(h, desc):
    for pat in [r'(<meta name="description" content=")(.*?)(" />)',
                r'(<meta property="og:description" content=")(.*?)(" />)',
                r'(<meta name="twitter:description" content=")(.*?)(" />)']:
        h=re.sub(pat, lambda m:m.group(1)+desc+m.group(3), h, count=1)
    return h

def enhance(slug, name, steps, faqs_custom, related, new_title=None, new_meta=None, url_slug=None):
    f=f"tools/{slug}.html"; h=open(f,encoding="utf-8").read()
    URL=f"https://rawmktg.com/tools/{slug}"
    if new_title: h=re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', h, count=1)
    if new_meta: h=_meta(h, new_meta)
    faqs = list(faqs_custom) + [
        (f"Is the {name} free to use?", f"Yes. The {name} is completely free, with no sign-up, no usage limits and no watermark on the output."),
        ("Is my data private?", f"Yes. The {name} runs entirely in your browser. Nothing you paste or enter is uploaded, stored or sent to any server."),
    ]
    # FAQPage schema
    faqschema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    fs='  <script type="application/ld+json">'+json.dumps(faqschema)+'</script>\n'
    if 'FAQPage' not in h:
        h=h.replace('  <link rel="alternate" type="application/rss+xml"', fs+'  <link rel="alternate" type="application/rss+xml"', 1)
    # content sections
    steps_html='<ol class="howto">'+''.join(f'<li>{H.escape(s,quote=False)}</li>' for s in steps)+'</ol>'
    faq_html=''.join(f'<h3>{H.escape(q,quote=False)}</h3><p>{H.escape(a,quote=False)}</p>' for q,a in faqs)
    rel_html='<div class="srcs">'+''.join(f'<a href="{u}">{H.escape(l,quote=False)} &rarr;</a>' for l,u in related)+'</div>'
    EXTRA=(f'\n<section class="method"><h2>How to use it</h2>{steps_html}</section>'
           f'\n<section class="method" id="faq"><h2>Frequently asked questions</h2>{faq_html}</section>'
           f'\n<section class="method"><h2>Related tools and reading</h2><p>Keep going with the playbooks and tools behind this one.</p>{rel_html}</section>')
    if 'id="faq"' not in h:
        assert '\n  </div>\n</main>' in h, f"main anchor missing in {slug}"
        h=h.replace('\n  </div>\n</main>', EXTRA+'\n  </div>\n</main>', 1)
    open(f,"w",encoding="utf-8").write(h)
    return slug

# ============ BATCH 1 ============
BATCH1=[
 dict(slug="agentic-commerce-readiness-scorecard", name="Agentic Commerce Readiness Scorecard",
  steps=["Answer each of the ten readiness checks for one store or catalog.",
         "Watch your score and band update as you go.",
         "Work the ranked gaps top-down, highest-leverage first."],
  faqs_custom=[
   ("What does the agentic commerce readiness score measure?","It scores your store against the ten infrastructure requirements AI shopping agents depend on, sub-200ms catalog latency, machine-readable product data, unified incentives, OAuth identity linking, MACH architecture and the risk controls that keep you eligible, then ranks your biggest gaps."),
   ("How do I improve a low readiness score?","Start with the gaps ranked highest: profile catalog p95 latency, model your catalog into JSON-LD with explicit attributes, expose one incentives endpoint, and confirm your platform advertises capabilities. Each fix moves you from considered to purchasable by an agent.")],
  related=[("When the buyer is a bot","/blogs/when-the-buyer-is-a-bot"),("Product Schema Auditor","/tools/product-schema-auditor"),("Product/Offer JSON-LD Generator","/tools/product-offer-jsonld-generator")]),
 dict(slug="ai-bot-log-analyzer", name="AI Bot Log Analyzer",
  steps=["Paste an excerpt of your access log (Common or Combined format).",
         "See per-agent hit counts, status codes and llms.txt reads.",
         "Fix any 403 or 429 blocks hitting citation crawlers."],
  faqs_custom=[
   ("Which AI crawlers does the log analyzer detect?","It flags the major citation and training crawlers, GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended and CCBot, and shows each one's hit count, status codes and whether it reached your llms.txt."),
   ("What should I do if bots are getting 403 or 429 responses?","A 403 or 429 to a named citation crawler means your firewall or rate limiter is silently blocking the bots that quote you. Verify the user-agent by reverse DNS, then allow-list the real crawlers in robots.txt and your WAF.")],
  related=[("How AI crawlers index your site","/blogs/how-ai-crawlers-index-your-site"),("Robots.txt AI Generator","/tools/robots-txt-ai-generator"),("llms.txt Validator","/tools/llms-txt-validator")]),
 dict(slug="ai-platform-optimizer", name="AI Platform Optimization Matrix",
  steps=["Select your target AI engines.",
         "Pick your content type.",
         "Apply the per-engine structure, schema and freshness recommendations."],
  faqs_custom=[
   ("Why optimise differently for each AI engine?","ChatGPT, Perplexity, Gemini, Claude and Google AI Overviews retrieve and cite differently, different index sources, schema weighting, freshness sensitivity and citation depth. The matrix gives the structure and cadence each one rewards for your content type."),
   ("Which engines should I prioritise?","Weight the engines your buyers actually use. For most B2B, Google's AI surfaces and ChatGPT carry the most citation volume, while Perplexity rewards clean question-and-answer formatting and recency. The tool tailors its recommendations to the engines and content type you pick.")],
  related=[("Why engines recommend different vendors","/blogs/why-engines-recommend-different-vendors"),("AI Mode vs AI Overviews","/blogs/ai-mode-vs-ai-overviews"),("Dual-Track Visibility Scorecard","/tools/dual-track-visibility-scorecard")]),
 dict(slug="ai-visibility-signal-diagnostic", name="AI Visibility Signal Diagnostic",
  steps=["Answer three questions about one prompt set.",
         "The tool isolates the first broken signal, mention, citation or recommendation.",
         "Follow the specific fix and the linked playbook."],
  faqs_custom=[
   ("What are the three AI-visibility signals?","Mention (does the model know you exist, from parametric memory), citation (does it use your page as evidence, from retrieval) and recommendation (does it name you as the pick, at synthesis). Each fails differently and needs a different fix."),
   ("How does the diagnostic decide which signal is broken?","It reads your symptoms top-down: absent even without live search points to a mention problem; named but never cited points to a citation problem; cited while a competitor is recommended points to a recommendation problem. It isolates the first broken signal and its fix.")],
  related=[("Citation vs Mention vs Recommendation","/blogs/citation-vs-mention-vs-recommendation"),("How your page gets retrieved","/blogs/how-your-page-gets-retrieved"),("Platform-Weighted Visibility Calculator","/tools/platform-weighted-visibility-calculator")]),
 dict(slug="answer-block-optimizer", name="Answer Block Optimizer",
  new_meta="Paste the answer that leads your H2 and check what AI engines extract: the 40-55 word window, leading with the answer, a statistic, and sentence economy.",
  steps=["Paste the answer that leads your H2.",
         "See the word-window, answer-first, statistic and filler checks.",
         "Rewrite until the block passes all four."],
  faqs_custom=[
   ("What makes an answer block extractable by AI?","A self-contained answer of roughly 40 to 55 words that leads with the answer (not a windup), states a concrete statistic or fact, and stays free of filler. AI engines lift the first such block after a heading, so it has to make sense read in isolation."),
   ("Why 40 to 55 words?","That is about one 128-token chunk, the unit retrievers score. Shorter can miss context; much longer gets split mid-argument across chunks. The window keeps your answer inside a single scored passage.")],
  related=[("Anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page"),("Query fan-out explained","/blogs/query-fan-out-how-one-prompt-becomes-ten-searches"),("Chunk Retrievability Analyzer","/tools/chunk-retrievability-analyzer")]),
 dict(slug="chunk-retrievability-analyzer", name="Chunk Retrievability Analyzer",
  steps=["Paste your page or section.",
         "See how it splits into passages, each scored alone.",
         "Fix the orphaned chunks it flags."],
  faqs_custom=[
   ("How do AI engines chunk a page?","Retrievers split your HTML into uniform passages of roughly 100 to 300 words (often about 128 tokens), then score each chunk in isolation against the query. Your page is represented by its single best chunk, so every passage has to name its own subject."),
   ("What is an orphaned chunk?","A passage that only makes sense with the context above it, a dangling pronoun (it, this), a vague date (last year), or an answer buried below the heading that promised it. Orphaned chunks score poorly because they read as being about nothing.")],
  related=[("How your page gets retrieved","/blogs/how-your-page-gets-retrieved"),("Query fan-out explained","/blogs/query-fan-out-how-one-prompt-becomes-ten-searches"),("Answer Block Optimizer","/tools/answer-block-optimizer")]),
 dict(slug="claim-anchoring-validator", name="Claim-Anchoring Validator",
  steps=["Paste a page you are about to publish.",
         "Read the four-part anchoring score and hallucination risk.",
         "Pair the exposed claims with proof before shipping."],
  faqs_custom=[
   ("What is the Claim-Anchoring framework?","A four-part check that predicts whether AI will quote your page accurately: answer capsules (self-contained answers), section autonomy (each section stands alone), proof-pairing ratio (claims backed by evidence) and brand association (your name near the claim). Weak anchoring is where hallucinations start."),
   ("What is a good proof-pairing ratio?","Aim for most factual claims paired with a nearby statistic, source or example. Unpaired claims are the ones engines paraphrase loosely or attribute to someone else. The validator scores your ratio and flags the exposed claims.")],
  related=[("Hallucination-proofing your brand","/blogs/hallucination-proofing-your-brand"),("Anatomy of a high-citation page","/blogs/anatomy-of-a-high-citation-page"),("Fact-Consistency Checker","/tools/fact-consistency-checker")]),
 dict(slug="content-mix-planner", name="GEO Content-Mix Planner",
  new_meta="Turn your monthly content capacity into a citation-optimized mix of flagship research, derivative, product and news, weighted toward the original research AI engines actually cite.",
  steps=["Set your monthly content capacity.",
         "Get a citation-optimised mix across flagship, derivative, product and news.",
         "Rebalance toward the original research that gets cited."],
  faqs_custom=[
   ("What content mix do AI engines cite most?","Original research and data get cited far above their share of output, while derivative posts get produced most and cited least. The planner turns your monthly capacity into a mix weighted toward the flagship research and comparison content engines actually quote."),
   ("How much original research should I publish?","Most programs under-produce it. Even one flagship data study a quarter earns links and citations across many downstream pieces. The planner shows the ratio of flagship, derivative, product and news that fits your capacity.")],
  related=[("Authority seeding for AI","/blogs/authority-seeding-ai-llm-trust"),("The topical authority cluster","/blogs/topical-authority-cluster-ai-shortlists"),("GEO Readiness Scorecard","/tools/geo-readiness-scorecard")]),
]

if __name__=="__main__":
    for t in BATCH1: enhance(**t); print("enhanced",t["slug"])
