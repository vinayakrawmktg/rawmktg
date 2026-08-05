#!/usr/bin/env python3
"""SCRATCH: build blogs/noterro-ai-search-teardown.html. Do NOT commit."""
import os, re, json, html as H
from PIL import Image
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="noterro-ai-search-teardown"; URL=f"https://rawmktg.com/blogs/{SLUG}"; IMG=f"/assets/images/{SLUG}-header"

def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'")
        .replace("“",'"').replace("”",'"').replace("…","..."))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)

T=open("blogs/aec-ai-visibility-gap.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>")
ADSENSE=sl("<script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js","></script>")
GA=sl("<!-- Google tag (gtag.js) -->","gtag('config','G-4B3LL6MJKN');</script>")
FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>")
NEWS=sl('<section class="newsletter-section"',"</section>")
FOOT=sl('<footer class="site-foot"',"</footer>")
FIGCSS="""
    .article-figure{margin:30px 0 10px;}
    .article-figure img{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:8px;background:#fff;}
    .figcap{font-family:var(--f-mono);font-size:9.5px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--mute);text-align:center;margin:12px 0 30px;line-height:1.55;}
  """
STYLE=STYLE.replace("</style>",FIGCSS+"</style>")

def dim(name):
    return Image.open("."+f"/assets/images/{name}.webp").size
def fig(name,cap):
    w,h=dim(name); full=f"/assets/images/{name}.webp"
    return (f'<figure class="article-figure"><img src="{full}" '
            f'srcset="/assets/images/{name}-760.webp 760w, {full} {w}w" '
            f'sizes="(max-width:768px) calc(100vw - 40px), 652px" width="{w}" height="{h}" '
            f'loading="lazy" alt="{escq(cap)}" /><figcaption class="figcap">{esc(cap)}</figcaption></figure>')
def p(t): return f"<p>{norm(t)}</p>"
def h2(i,t): return f'<h2 id="{i}">{esc(t)}</h2>'
def h3(i,t): return f'<h3 id="{i}">{esc(t)}</h3>'
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def code(label,body):
    return (f'<div class="code-wrap"><div class="code-label">{esc(label)}</div>'
            f'<div class="code-block"><pre>{H.escape(body)}</pre></div></div>')
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers)
    body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            klass=cls(j,c) if cls else ""
            attr=(' class="'+klass+'"') if klass else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return (f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div>'
            f'<table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')

# ---- content ----
HEADLINE="What Noterro Gets Right About AI Search"
DECK="And the gaps even strong brands should close. A bootstrapped allied-health software company has quietly become one of the most AI-visible brands in its category, here is how it happened, and what every software team can copy."
DESC=("A single-brand GEO teardown of Noterro, a bootstrapped allied-health SaaS cited on all 7 AI engines. "
      "What it gets right (breadth, structured data, llms.txt, clean fundamentals, real authority) and the gaps "
      "to close (82% branded traffic, thin non-brand content, 29% spam links, no hreflang).")
DATANOTE=("Based on Ahrefs Brand Radar AI-citation data across seven engines plus an SEO and structured-data audit "
          "of noterro.com, captured June 2026. Noterro is a practice-management platform for allied-health clinics.")

out=[]
out.append(p("Search is splitting in two. One half still looks like the ten blue links we have used for twenty years. The other half is a chat window: a person asks ChatGPT, Gemini, or Perplexity which practice-management tool they should buy, and an answer comes back already filtered, summarized, and recommended. For most software companies, that second half is a blind spot. They have no idea whether the models can see them, and most of the time the answer is that they cannot."))
out.append(p("Noterro is an exception, and an instructive one. It is a practice-management platform for allied-health clinics: physiotherapists, massage therapists, chiropractors, and naturopaths. It is bootstrapped, profitable, and has taken no outside capital. It is not the kind of company you would expect to be winning a technology race against venture-funded competitors. Yet when we mapped its footprint across the AI surfaces that increasingly mediate buying decisions, Noterro was cited on every single one."))
out.append(p("Getting cited is not magic; it is a pipeline. A page has to be crawlable, then self-describing, then authoritative, before a model will name it in an answer."))
out.append(fig("noterro-fig1-citation-pipeline","Figure 1: The path from a page on your site to a citation in an AI answer."))
out.append(p("The things Noterro did right along that pipeline are not expensive, not proprietary, and not dependent on a large marketing budget. They are choices any disciplined team can copy. The things it has not yet done are equally instructive, because they show where the frontier is moving next. We will take the wins first."))

# Part One
out.append(h2("part-one","Part One: What Noterro Gets Right"))
out.append(h3("win-1","1. It shows up everywhere the models look"))
out.append(p("The single most striking finding is breadth. Noterro is cited across all seven AI surfaces we track, and the volume is real, not token."))
out.append(fig("noterro-fig2-citations-by-platform","Figure 2: Citation counts across the major AI platforms."))
out.append(p("Most SaaS companies of comparable size appear on one or two platforms, and plenty appear on none. Breadth matters more than depth here, because different audiences live on different assistants and you do not get to choose which one your next customer opens. A clinic owner researching software in ChatGPT and a developer-minded founder asking Grok are two different buyers, and Noterro is present for both. The lesson for other companies is to stop treating “AI search” as a single channel to be won, and start treating it as presence across a fragmented set of engines, each of which assembles its answers from slightly different signals."))
out.append(h3("win-2","2. It treats structured data as a first-class citizen"))
out.append(p("The reason Noterro is so legible to machines is not luck. Its homepage carries three blocks of JSON-LD structured data, and each one does a specific job: an Organization block (who the company is), a WebApplication block (what the product is, plus an aggregate rating), and a FAQPage block that mirrors a twelve-question on-page FAQ in machine-readable form. That last one is the quiet masterstroke, because question-and-answer markup maps almost perfectly onto how people query assistants:"))
out.append(code("FAQPage JSON-LD","""<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Is Noterro HIPAA compliant?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Yes. Noterro follows HIPAA and PIPEDA protocols, with encrypted storage and 2FA."
    }
  }]
}
</script>"""))
out.append(p("When someone asks whether Noterro is HIPAA compliant, the model already has a clean, sourced answer to surface. The transferable lesson: schema is not a nice-to-have for SEO specialists, it is the primary interface between your site and the models. An Organization type, a FAQPage type, and a product or WebApplication type are the minimum, and they pay for themselves quickly."))
out.append(h3("win-3","3. It shipped an llms.txt before most teams knew it existed"))
out.append(p("Noterro serves a valid llms.txt file: a plain-text document, modeled loosely on robots.txt, that summarizes the product and indexes the pages the company most wants surfaced. It looks roughly like this:"))
out.append(code("llms.txt","""# Noterro
Practice management software for allied health clinics.

## Product
- [Noterro GO](/mobile-clinic-management-software): clinic management for mobile therapists
- [Pricing](/pricing): plans and pricing

## Resources
- [Help Center](https://help.noterro.com)"""))
out.append(p("The striking thing is not that Noterro implemented it perfectly, but that the company bothered at all. It signals a team paying attention to where discovery is heading rather than only optimizing for where it has been. The lesson is less about the file itself and more about posture: the companies that win in AI search treat it as a live, fast-moving surface and ship small experiments early, rather than waiting for a settled best practice that may never fully arrive."))
out.append(h3("win-4","4. The fundamentals are boringly, completely correct"))
out.append(p("It is easy to get excited about llms.txt and forget that AI visibility still rests on traditional technical hygiene. Noterro's is close to flawless."))
out.append(table("Fig. 4a: Technical hygiene audit, noterro.com",["Element","Status","Detail"],[
 ("robots.txt","PASS","Valid, points to the sitemap"),
 ("XML sitemap","PASS","Well-formed, 1,270 URLs"),
 ("Heading structure","PASS","Exactly one H1, clean hierarchy"),
 ("Canonical tags","PASS","Present"),
 ("Open Graph / Twitter","PASS","Complete metadata sets"),
 ("HTTPS","PASS","Served securely"),
], cls=lambda j,c: "up" if (j==1 and c=="PASS") else ("label" if j==0 else "")))
out.append(p("None of this is glamorous, and that is the point. The reason Noterro's structured data and llms.txt actually work is that they sit on top of a site the crawlers can navigate without friction. A brilliant schema block on a site with a broken sitemap and three competing H1s is a stereo in a car with no engine. Do the unglamorous foundational work first, then layer the AI-specific signals on top."))
out.append(h3("win-5","5. It earned authority the legitimate way"))
out.append(p("Noterro carries a Domain Rating of 80, high for a vertical SaaS company, and its strongest backlinks come from places that genuinely matter:"))
out.append(table("Fig. 4b: Highest-value referring domains",["Source","DR","Why it matters for AI"],[
 ("youtube.com","99","Hosts tutorials and the Crash Course; heavily cited for how-to answers"),
 ("g2.com","91","The review platform models lean on when users ask which tool to choose"),
 ("fresha.com","91","Wellness/booking ecosystem; high topical relevance"),
 ("globenewswire.com","91","Press distribution; news-grade co-citation signals"),
], cls=lambda j,c: "label" if j==0 else ("up" if j==1 else "")))
out.append(p("These are exactly the sources assistants cite when they recommend a product, so the authority compounds: the same links that help rankings also feed the models' confidence. The lesson is quality over volume. A handful of links from YouTube, G2, and a credible industry directory will do more for AI citation than hundreds of low-grade directory links."))
out.append(pull("A brilliant schema block on a site the crawlers cannot navigate is a stereo in a car with no engine. Do the unglamorous work first."))

# Part Two
out.append(h2("part-two","Part Two: The Gaps Worth Closing"))
out.append(p("If the story stopped there, the takeaway would be simple: do the fundamentals, add schema and llms.txt, earn good links. But Noterro is interesting precisely because a company can do all of that and still leave its biggest opportunity on the table. The gaps below are not failures. They are the natural next frontier for a brand that has already won the technical race."))
out.append(h3("gap-1","1. The brand is doing almost all the work"))
out.append(p("Here is the number that reframes everything: roughly 82% of Noterro's organic traffic comes from branded searches. People typing “noterro” or “noterro login” account for about 11,900 of its 14,500 monthly organic visits."))
out.append(fig("noterro-fig3-branded-traffic","Figure 3: Branded queries dominate Noterro's organic traffic."))
out.append(p("Everything non-branded, the entire universe of people searching “practice management software” or “SOAP note software” without knowing Noterro exists, adds up to only about 2,600 visits. This is a wonderful problem to have, because it means the brand is strong and customers are loyal. But it also means Noterro is mostly found by people who already know the name. The much larger pool of buyers still comparing options, the exact moment an assistant gets asked which clinic software is best for a physiotherapy practice, is largely uncaptured. And brand demand has a ceiling; you can only own your own name so many times. Read the branded-versus-non-branded split as a leading indicator: a high branded share looks healthy on a dashboard, but it can disguise the fact that you are not winning the category-level queries where new customers, and now AI assistants, actually make decisions."))
out.append(h3("gap-2","2. There is not enough content for the models to cite on competitive questions"))
out.append(p("This gap is the direct cause of the first one. AI assistants can only cite a brand for a non-branded question if the brand has published something worth citing on that topic. Noterro's homepage is excellent, but a homepage cannot answer how to choose chiropractic software. Those answers need dedicated pages, and the depth data shows the shortfall:"))
out.append(table("Fig. 5a: Citable pages by platform (depth, not breadth)",["Platform","Pages Cited","Read"],[
 ("Google AI Mode","67","Deep"),
 ("Grok (xAI)","89","Deep"),
 ("Google AI Overviews","45","Solid"),
 ("ChatGPT","7","Shallow"),
 ("Microsoft Copilot","3","Shallow"),
], cls=lambda j,c: "label" if j==0 else ("up" if c=="Deep" else ("mid" if c=="Solid" else ("neg" if c=="Shallow" else "")))))
out.append(p("The breadth of presence is there; the depth of citable content is not yet, especially on ChatGPT and Copilot. This is the most important lesson in the article: technical optimization makes you eligible for AI citation, but content is what gets you cited. Schema tells a model what a page is. It cannot manufacture a page that does not exist. The companies that pull ahead from here will pair Noterro-grade infrastructure with a steady stream of genuinely useful, non-branded answer content."))
out.append(h3("gap-3","3. The backlink profile needs a cleanup"))
out.append(p("Authority cuts both ways. Alongside the genuinely strong links, about 29% of Noterro's referring domains are flagged as spam: link-farm directories and low-quality auto-listings of the kind that accrue to almost any domain once it reaches a certain size."))
out.append(fig("noterro-fig4-spam-domains","Figure 4: Nearly a third of referring domains are spam-flagged."))
out.append(p("Most were probably never built by Noterro at all. The risk is not a sudden penalty; it is slow erosion of the trust signals both search engines and models rely on. The fix is unglamorous and cheap: assemble the list and submit a disavow file through Search Console:"))
out.append(code("disavow.txt","""# disavow.txt - submit via Google Search Console
# Spam directories and link farms
domain:buybacklinks.agency
domain:kingranks.com
domain:topbilliondirectory.com
domain:rankyour.website"""))
out.append(p("The broader lesson is that authority needs maintenance, not just accumulation. A link profile is a garden, not a trophy case."))
out.append(h3("gap-4","4. A multi-market product with a single-market setup"))
out.append(p("Noterro serves clinics across Canada, the United States, the United Kingdom, Australia, and beyond, and its pricing even differs by region. Today the traffic is concentrated at home:"))
out.append(table("Fig. 5b: Traffic by market",["Market","Share of traffic","Monthly visits"],[
 ("Canada","61.1%","8,900"),
 ("United States","34.3%","5,000"),
 ("United Kingdom","1.3%","185"),
 ("Australia","1.0%","146"),
], cls=lambda j,c: "label" if j==0 else ""))
out.append(p("Yet the site carries no hreflang markup, the signal that tells search and AI engines which regional version of a page to serve to whom. A few lines would help the models stop guessing:"))
out.append(code("hreflang","""<link rel="alternate" hreflang="en-ca" href="https://www.noterro.com/" />
<link rel="alternate" hreflang="en-us" href="https://www.noterro.com/us/" />
<link rel="alternate" hreflang="en-gb" href="https://www.noterro.com/uk/" />
<link rel="alternate" hreflang="x-default" href="https://www.noterro.com/" />"""))
out.append(p("The lesson generalizes to any company selling across borders: if your product is global, your technical setup should say so. Otherwise you are asking the models to guess which version of you to recommend in London versus Toronto, and they will not always guess in your favor."))
out.append(pull("Technical optimization makes you eligible for AI citation. Content is what gets you cited."))

# Synthesis
out.append(h2("synthesis","The Synthesis"))
out.append(p("The most useful way to read Noterro is as a company that has finished the first half of the AI-search playbook better than almost anyone, with the entire second half still in front of it."))
out.append(fig("noterro-fig5-playbook-halves","Figure 5: The two halves of the AI-search playbook."))
out.append(p("The first half is infrastructure: clean fundamentals, rich structured data, an llms.txt, and legitimately earned authority. That work is necessary, it is copyable, and it is where most companies should start, because without it nothing else registers. But infrastructure is increasingly table stakes. As more companies implement schema and tidy their sitemaps, the differentiator shifts to the second half: depth of content and strength of entity authority. The brand that publishes the clearest answer to which software is best for a mental-health practice, backs it with a completed G2 profile and a well-structured FAQ, and keeps its link profile clean, is the brand the assistant will name when a buyer asks. That position is sticky once established, which is exactly why the companies investing in it now will be hard to dislodge later."))
out.append(p("For Noterro, the path forward is unusually clear, because the hard, foundational part is already done. For everyone else, the lesson is twofold. Copy the fundamentals Noterro got right, because they are the price of admission. Then do the thing Noterro has not yet done, and build the content and authority that turn visibility into citations. The first makes the models able to see you. The second makes them recommend you."))

# FAQ
FAQ=[
 ("Why is Noterro so visible in AI search?","Noterro is cited across all seven AI engines tracked because it pairs clean technical fundamentals with three blocks of JSON-LD structured data (Organization, WebApplication, and a FAQPage that mirrors its on-page FAQ), a published llms.txt file, and a high-quality backlink profile (DR 80) from sources models trust, such as YouTube and G2. Those signals make its pages crawlable, self-describing, and authoritative, the three conditions a page must meet before a model will name it."),
 ("What is the biggest gap in Noterro's AI-search strategy?","Content depth on non-branded, competitive questions. About 82% of Noterro's organic traffic is branded, and it has few dedicated pages answering category-level queries like which practice-management software is best, so assistants have little to cite when buyers compare options. ChatGPT and Copilot cite only 7 and 3 of its pages respectively. Technical optimization makes a brand eligible for citation; published answer content is what actually gets it cited."),
 ("What can other software companies copy from Noterro?","The infrastructure half of the playbook, all of which is low-cost and non-proprietary: correct technical fundamentals (valid robots.txt, clean sitemap, a single H1, canonicals, HTTPS), Organization plus FAQPage plus WebApplication schema, a published llms.txt, and a small number of high-authority backlinks rather than many low-grade ones. Then go beyond Noterro by publishing non-branded answer content and cleaning up spam links with a disavow file."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns of B2B verticals and brands, pulling AI-citation and SEO data to show exactly where the visibility gaps are. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Data source: Ahrefs (organic keywords, referring domains, Brand Radar AI citations) and a manual structured-data and technical audit of noterro.com, captured June 2026.</p></div>')

body="\n".join(out)
# interlinks
LINKS=[
 ("structured data is not a nice-to-have","/blogs/schema-markup-ai-citations-2026"),
 ("the same links that help rankings also feed the models' confidence","/blogs/authority-seeding-ai-llm-trust"),
 ("content is what gets you cited","/blogs/anatomy-of-a-high-citation-page"),
 ("82% of Noterro's organic traffic comes from branded searches","/blogs/hr-saas-ai-visibility-gap"),
 ("crawlable, then self-describing, then authoritative","/blogs/how-rag-actually-works"),
 ("referring domains are flagged as spam","/glossary/referring-domains"),
]
for ph,u in LINKS:
    np=norm(ph)
    if np in body: body=body.replace(np,f'<a href="{u}">{np}</a>',1)

# sidebar
SIDEBAR=[("7/7","AI engines citing Noterro"),("82%","Of organic traffic is its own brand name"),("DR 80","Domain Rating, top-tier authority")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc='<li><a href="#part-one"><span class="toc-num">01</span>What Noterro gets right</a></li><li><a href="#part-two"><span class="toc-num">02</span>The gaps worth closing</a></li><li><a href="#synthesis"><span class="toc-num">03</span>The synthesis</a></li>'
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div>'
              f'<div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this teardown</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=(f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - rawmktg." '
            f'class="article-header-img" width="2400" height="1260" loading="eager">')

# schema
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),
 "image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":"2026-06-10","dateModified":"2026-06-10",
 "author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},
 "mainEntityOfPage":{"@type":"WebPage","@id":URL},
 "keywords":["Noterro","AI search","GEO","AI citations","llms.txt","schema","structured data","practice management software","allied health","Ahrefs Brand Radar"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},
 {"@type":"ListItem","position":2,"name":"What Noterro Gets Right About AI Search","item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/"]}
personLD={"@context":"https://schema.org",**person}

hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;'
      'clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean '
      f'Markdown version of this page is available at {URL}.md. Optimized for AI and LLM tools.</div>')
TITLE="What Noterro Gets Right About AI Search &middot; rawmktg."
da=escq(DESC)
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
 "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n"
 "  <meta name=\"robots\" content=\"index, follow\" />\n"
 f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
 f"  <meta name=\"description\" content=\"{da}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
 "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
 "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
 f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 "  <meta property=\"article:published_time\" content=\"2026-06-10T00:00:00Z\" />\n"
 "  <meta property=\"article:modified_time\" content=\"2026-06-10T00:00:00Z\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{H.escape(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  {jb(blog)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/blogs/{SLUG}.md\" />\n  "+FONTS+"\n  ")
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">GEO Teardown &middot; Allied-Health SaaS</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">June 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n</body>\n</html>\n")
final=head+STYLE+"\n  "+ADSENSE+">\n  "+ADSENSE.replace("<script async src=","")  # placeholder fix below
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'+tail)
hh=open(f"blogs/{SLUG}.html").read()
print("wrote",SLUG,"| em:",hh.count("—"),"en:",hh.count("–"),"bytes:",len(hh),
      "| jsonld:",hh.count("application/ld+json"),"| figs:",hh.count("article-figure")-2,"| tables:",hh.count('class="tt"'),"| code:",hh.count("code-block")-1)
