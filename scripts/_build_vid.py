#!/usr/bin/env python3
"""SCRATCH: build blogs/video-ai-citation-source.html"""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="video-ai-citation-source"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}"; PUB="2026-09-16"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x").replace("−","-"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav',"</nav>"); NEWS=sl('<section class="newsletter-section',"</section>"); FOOT=sl('<footer class="site-foot',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
CBCOPY=open("blogs/schema-markup-ai-citations-2026.html",encoding="utf-8").read()
mcb=re.search(r'<style id="cb-copy-css">.*?</script>', CBCOPY, re.S); CB=mcb.group(0) if mcb else ""

def p(t): return f"<p>{norm(t)}</p>"
def pull(t): return f'<div class="pull-quote">{esc(t)}</div>'
def sec(num,sid,q,strong,rest=""):
    cap=(f'<div class="section-answer"><strong>{esc(strong)}</strong> {norm(rest)}</div>' if rest else f'<div class="section-answer"><strong>{esc(strong)}</strong></div>')
    return f'<h2 id="{sid}"><span class="section-num">{num}</span>{esc(q)}</h2>\n{cap}'
def h3(t): return f"<h3>{esc(t)}</h3>"
def table(label,headers,rows,cls=None):
    th="".join(f"<th>{esc(c)}</th>" for c in headers); body=""
    for r in rows:
        tds=""
        for j,c in enumerate(r):
            k=cls(j,c) if cls else ""; attr=(' class="'+k+'"') if k else ""
            tds+="<td"+attr+">"+esc(c)+"</td>"
        body+=f"<tr>{tds}</tr>"
    return f'<div class="tt-wrap"><div class="tt-label">{esc(label)}</div><table class="tt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def chart(cid,h,cap): return f'<div class="chart-wrap"><canvas id="{cid}" height="{h}"></canvas></div><div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="YouTube, Video and the AI Citation"
DECK=("AI engines cannot watch your video, but they read everything around it, and they cite it. YouTube is now the fourth most-quoted domain "
      "in AI answers. Here is how a model reads a video it can't play, and how to make yours the source it pulls.")
DESC=("Video is now a major AI citation source: YouTube is the fourth most-cited domain in AI answers and overtook Reddit as the top social source. Since models read the transcript, title, description, chapters and VideoObject schema, not the pixels, this is how to make your video the one ChatGPT, Perplexity and Google AI quote.")
DATANOTE=("Figures are drawn from 2026 studies of AI citation sources (GEO Metrics' 200,000-response analysis across eight engines, and Otterly's "
          "March 2026 YouTube citation study). Shares vary by engine, category and study; treat them as directional, and confirm your own with a scan.")

CODE_VIDEOOBJECT=r'''<!-- VideoObject schema with the full corrected transcript pasted in.
     This gives the model a deterministic text source, no reliance on YouTube's HTML. -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How query fan-out works, in 4 minutes",
  "description": "A plain-English walkthrough of how one prompt becomes 8-16 hidden searches, with examples.",
  "thumbnailUrl": ["https://example.com/thumb.jpg"],
  "uploadDate": "2026-09-16",
  "duration": "PT4M12S",
  "contentUrl": "https://example.com/video.mp4",
  "embedUrl": "https://www.youtube.com/embed/XXXXXXXXXXX",
  "hasPart": [
    {"@type":"Clip","name":"What query fan-out is","startOffset":0,"url":"...&t=0s"},
    {"@type":"Clip","name":"How many sub-queries fire","startOffset":72,"url":"...&t=72s"}
  ],
  "transcript": "Query fan-out is the technique behind AI Mode: the engine takes one prompt and rewrites it into eight to sixteen sub-queries... [full corrected transcript here]"
}
</script>'''

CODE_EMBED=r'''<!-- The embed page: the video, an answer block, and the transcript, all in server-side HTML. -->
<article>
  <h1>How does query fan-out work?</h1>

  <p class="answer">
    Query fan-out is how AI search turns one prompt into 8-16 parallel sub-queries,
    retrieves passages for each, and fuses them into one answer. Breadth of coverage,
    not a single keyword ranking, decides which sources get cited.
  </p>

  <div class="video"><iframe src="https://www.youtube.com/embed/XXXX" title="..."></iframe></div>

  <h2>Full transcript</h2>
  <div class="transcript">
    <p><a href="#t=0">00:00</a> Query fan-out is the technique behind AI Mode...</p>
    <p><a href="#t=72">01:12</a> A single prompt fires eight to sixteen sub-queries...</p>
    <!-- the corrected transcript, in text, is the asset a model extracts -->
  </div>
</article>'''

out=[]; A=out.append

A(sec("01","cite","Do AI engines actually cite video?",
      "Yes, and increasingly. YouTube is now roughly the fourth most-cited domain in AI answers (around 8.5% of citations in one 200,000-response study) and has overtaken Reddit as the single most-cited social platform across Google AI Overviews, ChatGPT and Perplexity.",
      "Video is no longer a brand-awareness channel that happens to sit outside search. It is a first-class citation source engines pull into answers."))
A(p("For a decade, video was treated as the medium you measured in views and watch-time, adjacent to search but not part of it. That has changed. Across large samples of AI answers, YouTube shows up as a top-tier cited domain, and it dwarfs every other video platform, one analysis put YouTube at roughly 20% citation share across AI platforms, orders of magnitude ahead of the next video source."))
A(p("The reason is not that engines love video. It is that YouTube is the one video platform that is comprehensively indexed, auto-transcribed, and, being Google-owned, deeply integrated into the surfaces that generate AI answers. When a model assembles an answer, it is not choosing a video, it is choosing the text attached to one. Understanding that distinction is the whole game."))

A(sec("02","read","How does a model 'read' a video it cannot watch?",
      "It does not watch anything. Language models cannot play back or analyse audio and pixels in real time; they read the indexed text around the video, the transcript, title, description, chapter titles, and schema.",
      "Every optimisation that follows is about making that text complete, correct, and extractable, because the text is the only thing the model ever sees."))
A(p("ChatGPT Search, Perplexity and Google AI Overviews all work from the same raw material: the words associated with a video, not the video itself. That means the auto-transcript in the page HTML, the title, the description, the timestamped chapter titles, and any VideoObject schema. A brilliant video with a garbled auto-transcript and a one-line description is, to a model, a brilliant video it cannot read."))
A(table("Table 1. What a model actually reads from a video, and how to optimise each part.",
        ["Element","Why it matters","How to optimise"],
        [["Transcript","The main body text a model extracts; usually auto-generated and error-prone","Correct it; lead with a spoken answer; publish it as text"],
         ["Title","The headline the model matches to the query","Phrase it as the question a buyer asks"],
         ["Description","Secondary context and links","Summarise the answer; include the key facts and a link"],
         ["Chapter titles","Structure; lets a model lift the relevant segment","Name chapters as sub-questions with timestamps"],
         ["VideoObject schema","A deterministic, machine-readable source of truth","Add it, with the corrected transcript inside"]]))

A(sec("03","which","Which engines cite video, and how differently?",
      "Very differently. In one 2026 study of YouTube citations, Perplexity drove about 38.7% and Google AI Overviews about 36.6%, while ChatGPT contributed only around 4.4%.",
      "If your buyers live on Perplexity and Google's AI answers, video is a major lever; if they live on ChatGPT, it is a minor one. Measure before you invest."))
A(chart("engineChart",280,"Figure 1. Share of YouTube citations by engine (Otterly, March 2026). Perplexity and Google AI Overviews do almost all of the video citing; ChatGPT does very little."))
A(p("This split matters more than the headline 'video gets cited' number, because it tells you where the effort pays off. A B2B brand whose buyers use Perplexity for research, or who cares about Google AI Overviews, should treat video as a serious channel. A brand whose audience lives primarily in ChatGPT should weight it lower and lean on the "+L("off-site and on-page levers that ChatGPT favours","/blogs/why-engines-recommend-different-vendors")+" instead. The engines disagree; your strategy should too."))

A(sec("04","citable","What makes a video citable?",
      "A spoken answer in the first 15 to 30 seconds, a clean corrected transcript, question-shaped chapters, and a description that states the facts, so the extractable text leads with the answer, just like a page.",
      "The same answer-first principle that governs a high-citation page governs a high-citation video, because both are read as text."))
A(p("Think of the video as a page whose body copy is the transcript. Everything that makes "+L("a page get cited","/blogs/anatomy-of-a-high-citation-page")+" applies: lead with the answer, keep each segment self-contained, use specific numbers, and structure it so a retriever can lift one relevant chunk. The difference is that your 'body copy' is spoken, so you have to say the answer out loud, early, and then make sure the transcript captures it cleanly."))
A(p("Concretely: open the video by answering the question in a sentence or two, before the intro animation and the 'hit subscribe'. Name each section out loud so the auto-transcript segments cleanly. Put the key numbers in speech and in the description. A video that buries its answer four minutes in, behind a personality intro, gives a model nothing to extract from the part it is most likely to read."))

A(sec("05","transcript","Why is the transcript the real asset?",
      "Because it is the only full-text representation of the video a model can read, and the auto-generated version is almost always wrong on exactly the words that matter, product names, numbers, and technical terms.",
      "Correcting the transcript and publishing it as text is the single highest-leverage thing you can do for video citations."))
A(p("Auto-transcription mangles brand names, mishears figures, and drops punctuation, which is fatal when those are the facts a model would cite. Export the auto-transcript, correct it (especially proper nouns, prices and stats), and treat it as publishable copy. Then do the thing most brands skip: publish that corrected transcript as real text, both inside VideoObject schema and, ideally, as a visible transcript on a page you control."))
A(callout("Own the transcript, own the citation",
    ["A transcript that lives only inside YouTube is at the mercy of YouTube's HTML and Google's indexing. A corrected transcript you also publish on your own page, in server-side text and in VideoObject schema, gives every engine a clean, deterministic source, and it earns the citation for a URL you own, not just for youtube.com.",
     "This is the video version of the rule that runs through all of GEO: the citation goes to the extractable text, so put the extractable text where you want the credit to land."]))

A(sec("06","schema","How do you mark up a video for AI?",
      "With VideoObject schema, including name, description, uploadDate, duration, chapter Clips with timestamps, and, most importantly, the full corrected transcript pasted into the JSON-LD.",
      "Schema turns the video from something a model has to interpret into something it can read directly."))
A(p("VideoObject is the most powerful mechanism for giving an engine a deterministic source of truth about a video. The load-bearing fields are the transcript (paste the full corrected text), hasPart Clips (your chapters, with startOffset and titles), and the basics (name, description, uploadDate, duration). The "+L("wider schema playbook","/blogs/schema-markup-ai-citations-2026")+" covers the rest of the stack; for video, the transcript field is the one that changes outcomes."))
A(code("Code 1. VideoObject schema with chapters and the full corrected transcript inside.",CODE_VIDEOOBJECT))

A(sec("07","embed","Where should the video live to earn you the citation?",
      "Embedded on a page you own, wrapped in an answer block and a visible transcript, not left to float on YouTube alone.",
      "A YouTube-only video can earn youtube.com a citation; a video embedded on your page with the transcript in text can earn your domain the citation."))
A(p("Publishing to YouTube gets you into the pool engines cite from, and you should do it, because that pool is where the video citations come from. But if the only place the transcript exists is YouTube, the citation credit tends to accrue to youtube.com. Embed the same video on a page on your own site, put an "+L("answer block above it","/blogs/anatomy-of-a-high-citation-page")+", and publish the corrected transcript as visible, server-side text below it. Now the extractable text sits on a URL you control, and "+L("a non-rendering crawler can read it","/blogs/how-your-page-gets-retrieved")+"."))
A(code("Code 2. The embed page: answer block, the video, and the transcript, all in server-side text.",CODE_EMBED))

A(sec("08","beyond","Does this only work for YouTube?",
      "YouTube is where the citations concentrate today, but the underlying rule, models cite the text attached to media, applies to any video, podcast or webinar you can transcribe and publish.",
      "Treat every piece of spoken content as a transcript-in-waiting."))
A(p("The same mechanism means your webinars, product demos, conference talks and podcast episodes are all latent citation sources, if you transcribe them and publish the text. A podcast with a clean, published transcript is a text asset an engine can read; a podcast that exists only as audio in a player is invisible. Prioritise YouTube because that is where the measured citations are, but run every spoken asset through the same pipeline: transcribe, correct, publish as text, add schema."))

A(sec("09","measure","How do you know it's working?",
      "Run a prompt set of the questions your video answers across Perplexity, Google AI and ChatGPT, several times each, and check whether the answer cites your video, your embed page, or youtube.com, and whether the facts match your transcript.",
      "Because video citations concentrate on Perplexity and Google AI, weight your measurement there."))
A(p("The measurement discipline is the same as everywhere else: a portfolio of real questions, "+L("multiple runs per prompt because one run is noise","/blogs/share-of-model-measurement")+", every result tagged with engine and date. The video-specific twist is what you log: not just whether you are named, but which URL is credited, youtube.com or your own embed page, because that tells you whether the transcript-on-your-domain work is paying off. Concentrate the scan on Perplexity and Google AI Overviews, where the video citations actually happen."))

A(sec("10","checklist","The citable-video checklist",
      "Nine checks that turn a video from an unreadable asset into a citation source. Most brands fail on the transcript.",
      "Run it on your best-performing existing videos first, they already have the reach, they just need to be made readable."))
A(table("Table 2. The AI-citable video checklist.",
        ["#","Check","Pass looks like"],
        [["1","Spoken answer early","The question is answered out loud in the first 15-30 seconds"],
         ["2","Corrected transcript","Auto-transcript fixed for names, numbers and terms"],
         ["3","Transcript published as text","Visible, server-side transcript on a page you own"],
         ["4","Question-shaped title","Title matches the query a buyer types"],
         ["5","Factual description","Key facts and the answer summarised, with a link"],
         ["6","Chapters with timestamps","Sections named as sub-questions"],
         ["7","VideoObject schema","With chapters and the full transcript inside"],
         ["8","Embedded on your domain","Answer block + video + transcript on your URL"],
         ["9","Measured","Prompt set run on Perplexity and Google AI, citations verified"]],
        cls=lambda j,c:("num" if j==0 else "")))

A(sec("11","limits","What video won't do",
      "It won't help evenly across engines, and it won't carry a weak message. Video earns citations mainly on Perplexity and Google AI, and only if the spoken content actually answers the question.",
      "It is a powerful lever in the right channel mix, not a universal one."))
A(p("Two honest limits. First, the engine split is real: if your buyers are ChatGPT-first, video is a minor lever and your budget is better spent on "+L("the off-site and on-page signals ChatGPT weights","/blogs/why-engines-recommend-different-vendors")+". Second, this is a readability and distribution playbook, not a content one, it makes a good, answer-first video legible to machines. It cannot rescue a video that never says anything quotable, any more than schema can rescue a page with no answer on it."))

FAQ=[
 ("Do AI search engines cite YouTube videos?",
  "Yes. YouTube is now among the most-cited domains in AI answers, roughly the fourth most-cited in one 200,000-response study (about 8.5% share), and it has overtaken Reddit as the single most-cited social platform across Google AI Overviews, ChatGPT and Perplexity. It also dominates video specifically, one analysis put it near 20% citation share, far ahead of any other video platform."),
 ("How do AI models read a video they can't watch?",
  "They do not watch it. Language models cannot analyse audio or pixels in real time; they read the indexed text around the video, the transcript (auto or manual), the title, the description, the timestamped chapter titles, and any VideoObject schema. Every video optimisation for AI is really about making that text complete, correct and extractable, because the text is all the model ever sees."),
 ("Which AI engine cites video the most?",
  "Perplexity and Google AI Overviews do almost all of the video citing. In Otterly's March 2026 study of YouTube citations, Perplexity drove about 38.7% and Google AI Overviews about 36.6%, while ChatGPT contributed only around 4.4%. So video is a major lever if your buyers use Perplexity or Google's AI answers, and a minor one if they are ChatGPT-first."),
 ("What is the most important thing to optimise on a video for AI?",
  "The transcript. It is the only full-text representation of the video a model can read, and the auto-generated version is almost always wrong on exactly the words that matter, product names, numbers and technical terms. Export it, correct it, and publish it as real text, both inside VideoObject schema and, ideally, as a visible transcript on a page you own."),
 ("How do you use VideoObject schema for AI citations?",
  "Add VideoObject JSON-LD to the page where the video is embedded, with name, description, uploadDate, duration, hasPart Clips for your chapters (with startOffset and titles), and, most importantly, the full corrected transcript pasted into the transcript field. This gives the engine a deterministic, machine-readable source of truth instead of forcing it to parse YouTube's HTML."),
 ("Should I put the video on YouTube or my own site?",
  "Both. Publish to YouTube because that is where the measured video citations concentrate, but also embed the video on a page you own, with an answer block above it and the corrected transcript published as server-side text below. A YouTube-only video tends to earn youtube.com the citation; the same video with the transcript on your domain can earn your URL the citation."),
 ("Does video help AI visibility for every brand?",
  "No. Video earns citations mainly on Perplexity and Google AI Overviews, so it pays off most when your buyers use those engines, and much less for a ChatGPT-first audience. It is also a readability and distribution lever, not a content one: it makes an answer-first video legible to machines, but cannot make an unquotable video quotable. Measure where your buyers are before investing heavily."),
]
faq_html='<section class="faq-section" id="faq"><h2>Frequently asked questions</h2>'
for q,a in FAQ:
    faq_html+=f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><div class="faq-a">{p(a)}</div></div>'
faq_html+='</section>'
A(faq_html)

REFS=[
 ("YouTube AI Citation Study 2026. OtterlyAI.","https://otterly.ai/blog/youtube-ai-citation-study-2026/"),
 ("YouTube and AI Search: How Brands Earn AI Overview Citations. vidIQ.","https://vidiq.com/blog/post/youtube-ai-search-visibility/"),
 ("YouTube and GEO: How to optimise videos to be cited in AI search. GEO Metrics.","https://www.trygeometrics.com/blog/youtube-geo-optimize-videos-for-ai"),
 ("How YouTube Became the #1 Social Source for AI Overviews in 2026. AIO Copilot.","https://www.aiocopilot.com/blog/youtube-ai-citations-aio-strategy-2026"),
 ("Do YouTube transcripts influence AI search summaries? Contently.","https://contently.com/2025/11/25/do-youtube-transcripts-influence-ai-search-summaries/"),
 ("VideoObject structured data. Schema.org.","https://schema.org/VideoObject"),
 ("Video (VideoObject) structured data. Google Search Central.","https://developers.google.com/search/docs/appearance/structured-data/video"),
]
refs_items="".join(f'<li style="font-family:var(--f-mono);font-size:12px;line-height:1.55;color:var(--mute);padding-left:4px;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);">{esc(t)}</a></li>' for t,u in REFS)
A('<div class="about-block" id="references"><div class="about-label">References</div>'
  '<p style="margin-bottom:16px;">Citation-share figures are from the 2026 studies below; shares vary by engine, category and study, so treat them as directional.</p>'
  f'<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:9px;">{refs_items}</ol></div>')
A('<div class="about-block"><div class="about-label">About rawmktg.</div>'
  '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, agentic commerce and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p></div>')

body="\n".join(out)

SIDEBAR=[("~8.5%","of AI citations point to youtube.com (top-4 domain)"),("#1","most-cited social source, ahead of Reddit"),("38.7% / 36.6%","of YouTube citations: Perplexity / Google AI"),("4.4%","of YouTube citations from ChatGPT")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#cite"><span class="toc-num">01</span>Does AI cite video?</a></li>'
     '<li><a href="#read"><span class="toc-num">02</span>How a model reads video</a></li>'
     '<li><a href="#which"><span class="toc-num">03</span>Which engines cite it</a></li>'
     '<li><a href="#citable"><span class="toc-num">04</span>What makes a video citable</a></li>'
     '<li><a href="#transcript"><span class="toc-num">05</span>The transcript is the asset</a></li>'
     '<li><a href="#schema"><span class="toc-num">06</span>VideoObject schema</a></li>'
     '<li><a href="#embed"><span class="toc-num">07</span>Where the video should live</a></li>'
     '<li><a href="#beyond"><span class="toc-num">08</span>Beyond YouTube</a></li>'
     '<li><a href="#measure"><span class="toc-num">09</span>Measuring it</a></li>'
     '<li><a href="#checklist"><span class="toc-num">10</span>The checklist</a></li>'
     '<li><a href="#limits"><span class="toc-num">11</span>What it won\'t do</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - video as an AI citation source - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":norm(HEADLINE),"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["video AI citations","YouTube AI search","VideoObject schema","transcript optimization","GEO for video","Perplexity YouTube","AI Overviews video","answer engine optimization"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":norm(HEADLINE),"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="YouTube, Video and the AI Citation &middot; rawmktg."
da=escq(DESC)
head=("<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  "+GA+"\n"
 "  <meta name=\"google-adsense-account\" content=\"ca-pub-5952288317022852\" />\n  <meta name=\"robots\" content=\"index, follow\" />\n"
 f"  <title>{TITLE}</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
 f"  <meta name=\"description\" content=\"{da}\" />\n  <meta name=\"author\" content=\"Vinayak Ravi\" />\n"
 "  <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/images/favicon-32.png\" />\n"
 "  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/assets/images/favicon-16.png\" />\n"
 "  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/assets/images/favicon-180.png\" />\n"
 f"  <link rel=\"canonical\" href=\"{URL}\" />\n"
 f'  <link rel="alternate" hreflang="en-US" href="{URL}" />\n  <link rel="alternate" hreflang="en" href="{URL}" />\n  <link rel="alternate" hreflang="x-default" href="{URL}" />\n'
 "  <meta property=\"og:type\" content=\"article\" />\n"
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{escq(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n  <meta property=\"og:image:width\" content=\"2400\" />\n  <meta property=\"og:image:height\" content=\"1260\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{escq(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
 f"  <meta name=\"twitter:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n"
 f"  {jb(blog)}\n  {jb(speak)}\n  {jb(crumb)}\n  {jb(faqpage)}\n  {jb(personLD)}\n  {jb(org)}\n"
 "  <link rel=\"alternate\" type=\"application/rss+xml\" title=\"rawmktg.\" href=\"https://rawmktg.com/feed.xml\" />\n"
 f"  <link rel=\"alternate\" type=\"text/markdown\" href=\"/blogs/{SLUG}.md\" />\n  "+FONTS+"\n  ")

CHARTS=r"""
<!-- Chart.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
(function(){
  if(typeof Chart==='undefined') return;
  var css=getComputedStyle(document.documentElement);
  var signal=(css.getPropertyValue('--signal')||'#D04A2A').trim();
  var faint=(css.getPropertyValue('--faint')||'#C5BFB4').trim();
  var up=(css.getPropertyValue('--up')||'#3E9B6A').trim();
  var mono="'JetBrains Mono', monospace", text='rgba(255,255,255,0.55)', grid='rgba(255,255,255,0.08)';
  function rgba(hex,a){var n=hex.replace('#','');return 'rgba('+parseInt(n.substr(0,2),16)+','+parseInt(n.substr(2,2),16)+','+parseInt(n.substr(4,2),16)+','+a+')';}
  var neutral=rgba(faint,0.4);
  var ec=document.getElementById('engineChart');
  if(ec){new Chart(ec,{type:'bar',data:{labels:['Perplexity','Google AI Overviews','Other engines','ChatGPT'],datasets:[{data:[38.7,36.6,20.3,4.4],backgroundColor:[signal,rgba(signal,0.75),neutral,rgba(up,0.6)],borderRadius:4,barThickness:44}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of YouTube citations';}}}},
      scales:{x:{beginAtZero:true,max:45,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}},y:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Content &amp; Authority &middot; Off-Page</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Sep 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/vid_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/vid_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:600])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| jsonld_ok:",ok,"| h1:",hh.count("<h1"),"| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),
 "| code:",hh.count('class="code-block"'),"| callout:",hh.count('callout-box"'),"| faq:",len(re.findall('faq-item',hh)),"| outlinks:",len(re.findall(r'href="/(blogs|tools|methodology|features)',hh)))
