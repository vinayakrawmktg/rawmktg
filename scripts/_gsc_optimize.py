#!/usr/bin/env python3
"""SCRATCH: apply GSC query-match FAQ + schema + meta edits. Do NOT commit as content."""
import os, re, json, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

def add_faqs(path, items):
    h=open(path,encoding="utf-8").read()
    # visible: old format, prepend before first faq-item
    block=""
    for q,a in items:
        block+=(f'<div class="faq-item">\n        <h3 class="faq-q">{H.escape(q,quote=False)}</h3>\n'
                f'        <p class="faq-a">{H.escape(a,quote=False)}</p>\n      </div>\n        ')
    anchor='<div class="faq-item">'
    assert anchor in h, f"no faq-item in {path}"
    h=h.replace(anchor, block+anchor, 1)
    # schema: FAQPage block
    blocks=list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S))
    done=False
    for m in blocks:
        if '"FAQPage"' in m.group(1):
            obj=json.loads(m.group(1))
            new=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]
            obj["mainEntity"]=new+obj["mainEntity"]
            h=h[:m.start()]+'<script type="application/ld+json">'+json.dumps(obj)+'</script>'+h[m.end():]
            done=True; break
    assert done, f"no FAQPage schema in {path}"
    open(path,"w",encoding="utf-8").write(h)
    return len(items)

def repl(path, old, new):
    h=open(path,encoding="utf-8").read()
    assert old in h, f"NOT FOUND in {path}: {old[:60]}"
    open(path,"w",encoding="utf-8").write(h.replace(old,new,1))

B="blogs/"
# 1. schema-markup
add_faqs(B+"schema-markup-ai-citations-2026.html",[
 ("How does schema impact AI citations?","Schema does not directly rank a page, but it removes ambiguity: it tells a parser that a number is a price, a block is an FAQ answer, or an entity is your organization, so a model can extract and attribute the fact cleanly. About 53% of pages cited in AI answers carry valid structured data while many commercial pages carry none, so schema is the difference between a machine inferring your content and being told it."),
 ("What schema markup do you need for AI search citations?","Ship Organization and Article or BlogPosting on every page, FAQPage on any Q&A block, and a single consolidated @graph so a parser resolves the relationships in one pass. For product and comparison pages add SoftwareApplication and ItemList. Match every value in schema to the visible copy exactly, or you risk a structured-data penalty."),
 ("How can poor page structure hurt AI citation potential?","A page with no headings, no schema and content buried in client-rendered blocks forces the retriever to guess what each passage is about, and it usually guesses wrong. Unstructured HTML fragments the entity relationships a model needs, so the page loses to a competitor whose pricing, features and FAQs are cleanly marked up and answer-first."),
 ("Which article schema should a B2B site use?","Use Article or BlogPosting with author, datePublished and dateModified, wrapped in an @graph alongside your Organization node so the model ties the piece to a known entity. Add FAQPage for any question block. Avoid stacking disconnected script tags, a single @graph block improves crawl efficiency over fragmented markup."),
])
# 2. how-ai-crawlers  (+ meta)
add_faqs(B+"how-ai-crawlers-index-your-site.html",[
 ("What are crawler directives?","Crawler directives are the instructions that tell a bot what it may fetch, index or train on. They live in three places: robots.txt rules (User-agent, Allow, Disallow), the robots meta tag and X-Robots-Tag HTTP header (index/noindex, follow/nofollow), and access tokens like Google-Extended that govern AI-training use. Granting access is separate from being readable, a bot you allow can still receive an empty page."),
 ("What does a crawler directive mean?","A crawler directive is a single instruction to a specific user agent, for example Disallow: /admin for GPTBot or noindex on a thin page. Each directive targets one behaviour, crawl, index, or training, for one bot, so an effective policy is a set of directives rather than one switch. Check your robots.txt is not blocking GPTBot, ClaudeBot, PerplexityBot or Google-Extended by accident."),
])
repl(B+"how-ai-crawlers-index-your-site.html",
 "and the robots.txt configuration that maximises AI citation share.",
 "and the crawler directives and robots.txt configuration that maximise AI citation share.")
# 3. authority-seeding (+ meta)
add_faqs(B+"authority-seeding-ai-llm-trust.html",[
 ("What is LLM seeding?","LLM seeding, also called authority seeding, is placing consistent, corroborating information about your brand across the third-party sources a language model already trusts, so the model associates your entity with your category. Because roughly 97% of AI citations point off your own domain, seeding review sites, communities and analyst coverage moves visibility more than anything you publish on your own site."),
 ("What does LLM seeding mean?","It means teaching a model who you are through repetition across independent, high-trust sources rather than through links. Getting your brand named alongside established competitors in the same articles, directories and forums builds the co-citation and entity prominence a model retains in its weights, which is what gets you into the answer when a buyer asks."),
])
repl(B+"authority-seeding-ai-llm-trust.html",
 "LLM SEO through authority seeding: unlinked brand mentions",
 "LLM seeding, a.k.a. authority seeding: unlinked brand mentions")
# 4. eeat
add_faqs(B+"eeat-is-an-ai-signal-now.html",[
 ("Why are E-E-A-T and LLM optimization the new ranking signals?","Because the same experience, expertise, authoritativeness and trust signals Google rewards were baked into language models during reinforcement learning from human feedback, so a model prefers sources that read as credible. About 96% of AI Overview citations go to sources Google already trusts for E-E-A-T, which means optimizing for LLMs and optimizing for E-E-A-T are increasingly the same job."),
])
# 5. traditional-seo
add_faqs(B+"why-traditional-seo-is-no-longer-enough.html",[
 ("How do you transition from traditional SEO to GEO?","Keep the technical SEO foundation, crawlability, structured data and clean information architecture, then shift the content brief from keyword-matching to answer-first passages a model can lift. Add FAQ and comparison content that names competitors honestly, publish structured facts in server-side HTML, and measure AI citations and Share of Model alongside rankings. The transition is additive, not a teardown."),
])
# 6. cx-saas (+ meta)
add_faqs(B+"cx-saas-seo-discoverability-analysis.html",[
 ("What is CX SEO, and why do CX software vendors struggle with it?","CX SEO is search and AI-visibility work for customer-experience software, and vendors struggle with it for a consistent reason: they invest in brand and product pages while leaving the middle of the funnel, comparison, alternatives and use-case content, to review aggregators. The result is strong branded traffic and near-zero presence on the non-branded, problem-led queries buyers actually ask."),
])
repl(B+"cx-saas-seo-discoverability-analysis.html",
 "Six findings across six B2B CX SaaS companies:",
 "CX SEO teardown, six findings across six B2B CX SaaS companies:")
# 7. rlhf
add_faqs(B+"rlhf-and-your-brand.html",[
 ("Who provides the best expert human raters for RLHF?","The leading suppliers of expert human raters for RLHF are specialist data-labeling firms such as Surge AI, Scale AI and its Outlier network, Invisible Technologies, Toloka and Labelbox, alongside the in-house rater teams at the frontier labs. For domains like law, medicine or finance the differentiator is credentialed subject-matter experts rather than general crowdworkers, because rater quality sets the ceiling on model preference quality."),
])

print("FAQ + meta edits applied to 7 pages")
# validate all FAQPage schema still parse
for f in ["schema-markup-ai-citations-2026","how-ai-crawlers-index-your-site","authority-seeding-ai-llm-trust","eeat-is-an-ai-signal-now","why-traditional-seo-is-no-longer-enough","cx-saas-seo-discoverability-analysis","rlhf-and-your-brand"]:
    h=open(B+f+".html",encoding="utf-8").read()
    ok=all((json.loads(b) or True) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S))
    nq=[len(json.loads(b)["mainEntity"]) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S) if '"FAQPage"' in b][0]
    print(f"  {f:46} jsonld_ok:{ok} faq_qs:{nq} faq_items:{h.count('faq-item')}")
