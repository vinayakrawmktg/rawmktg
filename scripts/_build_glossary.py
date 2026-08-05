#!/usr/bin/env python3
"""Build the full AI-Search glossary: hub + per-term pages + .md twins + schema.
One-off generator. Content lives here so HTML and .md never drift."""
import os, re, glob, datetime, html as H, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = "2026-06-06"

# ── Term content ────────────────────────────────────────────────
# (slug, term, capsule, [hiw paras], (vs_heading, vs_para), why_para,
#  [(deeper_url,label)], [(rel_slug,label)])
GROUPS = [
 ("Core AI-search concepts", [
  ("generative-engine-optimization", "Generative Engine Optimization (GEO)",
   "Generative Engine Optimization (GEO) is the practice of structuring a brand's content and off-site signals so that AI systems like ChatGPT, Perplexity, Gemini and Google AI Overviews cite and recommend it when generating answers to buyer questions.",
   ["Traditional search returns a ranked list of links and lets the user choose. Generative engines return a single synthesised answer that names a handful of sources. GEO is the work of becoming one of those named sources: making content retrievable, quotable, and trusted by the retrieval systems that feed the model.",
    "In practice it spans three layers. The first is making pages machine-legible, through clean structure, schema markup, and answer-lead formatting. The second is making claims extractable, through self-contained definitions, statistics, and proof-pairing. The third is making the brand trusted off-site, through unlinked mentions and authority signals. It is measured in citations, not rankings."],
   ("GEO vs SEO vs AEO", "SEO optimises to rank a link in a results page. GEO optimises to be named inside a generated answer. AEO (Answer Engine Optimization) is often used interchangeably with GEO; where a distinction is drawn, AEO refers narrowly to winning direct-answer features, while GEO covers the full system of being cited across generative engines."),
   "B2B buyers increasingly ask an AI assistant which vendor to use, then act on the names it returns. In rawmktg's analysis, 73% of B2B procurement managers already use ChatGPT, Claude, or Perplexity for vendor discovery. The vendors named in the answer get the shortlist. The rest get no second look.",
   [("/blogs/how-rag-actually-works","How RAG Actually Works"),("/blogs/geo-compounding-flywheel","The GEO Compounding Flywheel")],
   [("answer-engine-optimization","Answer Engine Optimization"),("share-of-model","Share of Model"),("retrieval-augmented-generation","RAG")]),

  ("answer-engine-optimization", "Answer Engine Optimization (AEO)",
   "Answer Engine Optimization (AEO) is the practice of structuring content so it wins the single, direct answer that an answer engine or AI assistant returns to a question, rather than one position in a ranked list of links.",
   ["Answer engines collapse a query into one response. AEO is about being that response: leading with a clean, self-contained answer, using question-shaped headings and FAQ structure, and marking content up so a machine can identify the answer unambiguously.",
    "It grew out of voice search and featured snippets, where there is room for only one answer, and now applies directly to AI Overviews and chat assistants. The core move is the same: write the answer first, in a form a model can lift without the surrounding page."],
   ("AEO vs GEO", "AEO is often used as a synonym for GEO. Where they are separated, AEO is the narrower discipline of winning direct-answer features and single-answer responses, while GEO is the broader system of getting cited and recommended across generative engines, including the off-site authority work that AEO does not cover."),
   "Most B2B questions now resolve to a single answer somewhere in the buyer journey. If a competitor owns that answer, the buyer rarely looks further. AEO is how you become the answer rather than an option on a list the buyer never scrolls.",
   [("/blogs/why-engines-recommend-different-vendors","Why ChatGPT, Perplexity and Gemini Recommend Different Vendors"),("/blogs/schema-markup-ai-citations-2026","Schema Markup in 2026")],
   [("generative-engine-optimization","GEO"),("answer-capsule","Answer Capsule"),("ai-overviews","AI Overviews")]),

  ("ai-overviews", "AI Overviews",
   "AI Overviews are Google's AI-generated summaries that appear at the top of search results, answering a query directly and citing a small set of sources instead of only listing ranked links.",
   ["Google generates the overview by retrieving and synthesising content from pages it trusts, then names a few of them as sources. Appearing as one of those sources puts a brand above the traditional results, often before the user scrolls at all.",
    "Inclusion leans heavily on existing trust. In rawmktg's analysis, 96% of AI Overview citations go to sources Google already trusts on E-E-A-T grounds, which means classic search authority is largely a prerequisite for being cited here."],
   ("AI Overviews vs featured snippets", "A featured snippet lifts one passage verbatim from a single ranking page. An AI Overview synthesises an answer from multiple sources and cites several of them. The snippet rewards one well-formatted passage; the overview rewards being one of the trusted sources the model draws on."),
   "AI Overviews sit at the top of the page for a growing share of informational B2B queries, and they often answer the question without a click. Being cited inside them is one of the few ways to keep visibility as zero-click results expand.",
   [("/blogs/how-ai-crawlers-index-your-site","How AI Crawlers Actually Index Your Site"),("/blogs/eeat-is-an-ai-signal-now","E-E-A-T Is an AI Signal Now")],
   [("generative-engine","Generative engine"),("e-e-a-t","E-E-A-T"),("llm-citation","LLM citation")]),

  ("generative-engine", "Generative engine",
   "A generative engine is an AI system that answers a query by synthesising a single response from multiple retrieved sources, rather than returning a ranked list of links for the user to choose from.",
   ["ChatGPT, Perplexity, Gemini and Google AI Overviews are all generative engines. Each retrieves candidate content, reranks it, and generates an answer that names a few sources. The user reads the answer, not the underlying pages.",
    "Crucially, each engine retrieves and ranks differently, so they cite different sources for the same question. In rawmktg's analysis only 11% of domains were cited by both ChatGPT and Perplexity for the same query, which is why a single engine cannot be treated as the whole market."],
   ("Generative engine vs search engine", "A search engine indexes pages and returns a ranked list of links. A generative engine reads those pages and returns a synthesised answer with citations. The first sends you traffic by position; the second sends you influence by being named in the answer."),
   "Buyers increasingly start in a generative engine, not a search box. If your brand is not among the sources the engine names, you are not in the consideration set, regardless of how you rank in classic search.",
   [("/blogs/why-engines-recommend-different-vendors","Why ChatGPT, Perplexity and Gemini Recommend Different Vendors"),("/blogs/how-rag-actually-works","How RAG Actually Works")],
   [("retrieval-augmented-generation","RAG"),("ai-overviews","AI Overviews"),("llm-citation","LLM citation")]),

  ("retrieval-augmented-generation", "Retrieval-Augmented Generation (RAG)",
   "Retrieval-Augmented Generation (RAG) is the architecture most AI search systems use to answer a query: they retrieve relevant passages from an external source such as the web, then generate an answer grounded in and citing those passages.",
   ["Instead of answering only from what the model memorised in training, a RAG system runs a retrieval step first. It decomposes the query, fetches candidate passages, reranks them by relevance and authority, and feeds the best ones to the model as context for the answer.",
    "Because it competes at the passage level, your content is judged in fragments, not as a whole page. A clean, self-contained passage near the top of a page is far more likely to be retrieved and cited than the same point buried mid-article."],
   ("RAG vs a base language model", "A base language model answers from its training data, with a fixed knowledge cutoff and no sources. A RAG system retrieves live external content at query time and grounds its answer in it, which is what lets AI search cite current pages and name the brands in them."),
   "RAG is the mechanism that decides whether your content is even eligible to be cited. Understanding it tells you why structure and extractability, not just authority, determine whether a model can pull your page into an answer.",
   [("/blogs/how-rag-actually-works","How RAG Actually Works"),("/blogs/anatomy-of-a-high-citation-page","Anatomy of a High-Citation Page")],
   [("generative-engine","Generative engine"),("llm-citation","LLM citation"),("answer-capsule","Answer Capsule")]),

  ("llm-citation", "LLM citation",
   "An LLM citation is a reference to a source that an AI system names or links inside a generated answer, marking that source as one of the pages the model drew on to produce its response.",
   ["When a generative engine answers a question, it attributes parts of the answer to specific sources. Earning that attribution is the core goal of GEO, because the citation is what carries brand visibility into an AI answer.",
    "Citations are not evenly distributed, and they favour the top of a page. In rawmktg's analysis of high-citation pages, roughly 55% of citations came from the first 30% of the document, so where a claim sits on the page strongly affects whether it gets cited."],
   ("LLM citation vs backlink", "A backlink is a link from another site to yours, earned over time and counted by search engines. An LLM citation is a mention or link inside a generated answer, decided per query at answer time. One builds ranking authority; the other is the unit of visibility in AI search."),
   "Citations are the scoreboard for AI search. A page can rank well and still never be cited, so tracking which of your pages get named in answers is the most direct read on whether your GEO work is landing.",
   [("/blogs/anatomy-of-a-high-citation-page","Anatomy of a High-Citation Page"),("/blogs/prompt-to-citation-tracking","Prompt-to-Citation Tracking")],
   [("citation-gap","Citation gap"),("share-of-model","Share of Model"),("answer-capsule","Answer Capsule")]),

  ("citation-gap", "Citation gap",
   "A citation gap is the difference between how often AI systems cite one brand versus its competitors for the same set of buyer questions, exposing who owns the AI answer in a category and who is absent from it.",
   ["You measure it by running the questions a real buyer would ask across the target engines and recording which brands appear. The gap is the distance between the leaders and everyone else, and in most B2B categories it is severe.",
    "In rawmktg's teardowns the gaps were stark: a 39x ChatGPT citation gap in senior living, and 4 of 6 vendors in the AEC software space with fewer than two AI citations combined. The pattern repeats because almost no one is competing for these citations yet."],
   ("Citation gap vs ranking gap", "A ranking gap compares positions in the classic search results. A citation gap compares presence inside AI-generated answers. A brand can have a small ranking gap and a huge citation gap, because being indexed is not the same as being cited."),
   "The citation gap is usually the clearest picture of a category's AI visibility, and it is often wide open. For a brand willing to move first, it is less a problem to fix than a moat to claim before competitors notice it exists.",
   [("/blogs/aec-ai-visibility-gap","When Buyers Ask AI Which AEC Software to Use"),("/blogs/india-senior-living-ai-visibility-gap","India's Senior Living Sector Has an AI Problem")],
   [("share-of-model","Share of Model"),("llm-citation","LLM citation"),("generative-engine-optimization","GEO")]),

  ("share-of-model", "Share of Model",
   "Share of Model is a GEO metric that measures how often a brand is named or cited in AI-generated answers across a defined set of buyer prompts, relative to its competitors. It is the AI-era equivalent of share of voice.",
   ["You define a portfolio of prompts a real buyer would ask, run them across the target engines on a fixed cadence, and record which brands appear in each answer. Your share is the proportion of those answers that name you versus the competitive set.",
    "There is no public scoreboard for it. Share of Model is something you instrument yourself, because no analytics platform reports it by default and AI traffic is largely invisible to standard analytics; in rawmktg's testing, GA4 misses roughly 30% of AI referrers."],
   ("Share of Model vs Share of Voice", "Share of Voice measures presence across traditional channels such as search rankings, ad impressions and press. Share of Model measures presence inside generated answers specifically. As buyers shift discovery to AI assistants, the second increasingly predicts pipeline the first cannot see."),
   "It is the closest thing to a north-star metric for GEO. It turns the question are we showing up in AI answers from a vibe into a number you can track, benchmark against competitors, and tie to pipeline.",
   [("/blogs/prompt-to-citation-tracking","Prompt-to-Citation Tracking"),("/blogs/topical-authority-cluster-ai-shortlists","The Topical Authority Cluster")],
   [("prompt-portfolio","Prompt portfolio"),("ai-referral-traffic","AI referral traffic"),("citation-gap","Citation gap")]),
 ]),

 ("Coined at rawmktg.", [
  ("answer-capsule", "Answer Capsule",
   "An Answer Capsule is a self-contained block of content, usually the opening sentences of a page or section, that states a complete, quotable answer to a single question, formatted so an AI system can lift it directly into a generated response without needing the surrounding context.",
   ["AI systems retrieve and extract passages, not whole pages, and they lean heavily on the top of a document. In rawmktg's analysis of cited pages, roughly 55% of citations came from the first 30% of the page. An Answer Capsule exploits this by front-loading a clean, extractable answer.",
    "The format is strict: one question, one complete answer, no dependency on earlier text, no marketing preamble. The shape is the term, its category, and what it does. If a reader, or a model, can copy the first sentence and have it stand on its own, it is a capsule. If it needs the next paragraph to make sense, it is not."],
   ("Answer Capsule vs meta description", "A meta description summarises a page to earn a click from a search snippet. An Answer Capsule is the answer itself, written to be extracted and quoted verbatim inside an AI-generated response rather than to entice a click."),
   "It is the smallest unit of GEO. A page can have perfect schema and strong authority and still go uncited if the answer is buried three paragraphs down. The capsule is what gets pulled.",
   [("/blogs/hallucination-proofing-your-brand","Hallucination-Proofing Your Brand"),("/blogs/anatomy-of-a-high-citation-page","Anatomy of a High-Citation Page")],
   [("proof-pairing-density","Proof-Pairing Density"),("answer-lead-formatting","Answer-lead formatting"),("llm-citation","LLM citation")]),

  ("proof-pairing-density", "Proof-Pairing Density",
   "Proof-Pairing Density is the share of claims on a page that are paired with a verifiable proof point, such as a specific statistic, a cited source, or a named example, rather than left as unsupported assertions.",
   ["Generative engines favour content they can trust and verify. Pairing each claim with a concrete number or citation raises the page's credibility signal and gives the model an extractable, attributable fact rather than an opinion.",
    "The Princeton GEO study found this directly: adding statistics lifted AI visibility by roughly 41%, and citing authoritative sources lifted it by up to 115% for previously low-ranked content. Proof-Pairing Density is the discipline of doing this consistently, claim by claim, across a page."],
   ("Proof-Pairing Density vs keyword density", "Keyword density counts how often a target phrase appears, an old SEO heuristic that generative engines ignore. Proof-Pairing Density counts how often claims are backed by evidence, which is what actually correlates with getting cited."),
   "For a publication that sells rigor, it is also a reputational standard: every claim earns its place by being provable. It is the difference between content a model can safely quote and content it will pass over.",
   [("/blogs/hallucination-proofing-your-brand","Hallucination-Proofing Your Brand")],
   [("answer-capsule","Answer Capsule"),("brand-hallucination","Brand hallucination"),("e-e-a-t","E-E-A-T")]),
 ]),

 ("The technical layer", [
  ("llms-txt", "llms.txt",
   "llms.txt is a plain-text file placed at a website's root that gives AI systems a curated, Markdown-formatted map of the site's most important content, so models can find and parse it without crawling the full HTML.",
   ["The file lists key pages with short descriptions, in Markdown, in priority order: a deliberate, human-curated guide to what matters on the site. It was proposed by Jeremy Howard of Answer.AI in 2024 as a standard, and support depends on whether a given AI system chooses to read it.",
    "Adoption is still early, which is the opportunity. In rawmktg's AEC teardown, zero of six companies had published an llms.txt file. Being among the first in a category to ship one is a low-cost signal almost no competitor has matched."],
   ("llms.txt vs robots.txt", "robots.txt controls access: which crawlers may visit which paths. llms.txt guides attention: which content a model should prioritise and how to read it. One restricts, the other curates, and they are used together."),
   "It is one of the cheapest GEO moves available: a single static file that makes your best content easier for models to locate and parse, in a field where most competitors have not published one.",
   [("/blogs/how-ai-crawlers-index-your-site","How AI Crawlers Actually Index Your Site"),("/blogs/hallucination-proofing-your-brand","Hallucination-Proofing Your Brand")],
   [("oai-searchbot","OAI-SearchBot"),("schema-markup","Schema markup"),("common-crawl-ccbot","Common Crawl / CCBot")]),

  ("oai-searchbot", "OAI-SearchBot",
   "OAI-SearchBot is OpenAI's crawler for its search product: it fetches and indexes web pages so they can be retrieved and cited when ChatGPT search answers a user's query.",
   ["It is distinct from the crawler OpenAI uses to gather training data. OAI-SearchBot exists to build the live search index that feeds citations, which means allowing it is how you stay eligible to be cited in ChatGPT search results.",
    "Like other AI search crawlers, it does not execute JavaScript. In rawmktg's testing, none of the three major AI crawlers run JS, so any content that only appears after client-side rendering is effectively invisible to them."],
   ("OAI-SearchBot vs GPTBot", "GPTBot is OpenAI's crawler for collecting training data. OAI-SearchBot is its crawler for the live search index that powers citations. Blocking GPTBot protects content from training use; blocking OAI-SearchBot removes you from ChatGPT search results, which is usually the opposite of the goal."),
   "If you want to appear in ChatGPT's answers, OAI-SearchBot is the bot that has to be able to reach and read your pages. Confirming it is allowed, and that your content is in static HTML, is step zero.",
   [("/blogs/how-ai-crawlers-index-your-site","How AI Crawlers Actually Index Your Site")],
   [("gptbot-vs-oai-searchbot","GPTBot vs OAI-SearchBot"),("perplexitybot","PerplexityBot"),("llms-txt","llms.txt")]),

  ("perplexitybot", "PerplexityBot",
   "PerplexityBot is the crawler Perplexity uses to discover and index web pages so they can be retrieved and cited as sources in its AI-generated answers.",
   ["Perplexity is citation-first by design, surfacing the sources behind each answer, and PerplexityBot is what populates the index those citations are drawn from. Allowing it is the precondition for being cited there.",
    "It also does not render JavaScript, so static, server-delivered HTML is what it can actually read. Perplexity reflects on-page updates quickly, which makes content freshness a more immediate lever there than on slower-moving engines."],
   ("PerplexityBot vs OAI-SearchBot", "Both are AI search crawlers that feed citations, but for different engines and with different ranking logic. Perplexity weights real-time retrieval and freshness heavily; ChatGPT search leans on Bing's index. The robots.txt decision for each is the same: allow it if you want its citations."),
   "Perplexity is a fast-growing surface for B2B research, and its visible citations make it a place where being a named source is especially valuable. PerplexityBot access is what makes that possible.",
   [("/blogs/how-ai-crawlers-index-your-site","How AI Crawlers Actually Index Your Site")],
   [("oai-searchbot","OAI-SearchBot"),("common-crawl-ccbot","Common Crawl / CCBot"),("llms-txt","llms.txt")]),

  ("gptbot-vs-oai-searchbot", "GPTBot vs OAI-SearchBot",
   "GPTBot and OAI-SearchBot are two different OpenAI crawlers: GPTBot collects data used to train models, while OAI-SearchBot builds the live search index that lets ChatGPT retrieve and cite current web pages.",
   ["The distinction matters because the two serve opposite goals. Allowing OAI-SearchBot keeps you eligible for citations in ChatGPT search. Allowing GPTBot lets your content be used in future model training, which some publishers permit and others block.",
    "This is why a blanket block of all OpenAI bots can backfire: it is possible, and often preferable, to allow the citation crawler while restricting the training crawler, so you stay visible in answers without contributing to training corpora."],
   ("Training crawler vs citation crawler", "A training crawler gathers text to improve a model and affects what the model knows in general. A citation crawler builds a live index and affects whether your specific pages get named in answers today. They are configured separately in robots.txt."),
   "Getting this split right is the single most consequential robots.txt decision for AI visibility. Block the wrong bot and you either leak content to training or disappear from citations, when you can usually choose precisely.",
   [("/blogs/how-ai-crawlers-index-your-site","How AI Crawlers Actually Index Your Site")],
   [("oai-searchbot","OAI-SearchBot"),("common-crawl-ccbot","Common Crawl / CCBot"),("llms-txt","llms.txt")]),

  ("common-crawl-ccbot", "Common Crawl / CCBot",
   "Common Crawl is a large public dataset of crawled web pages, gathered by its crawler CCBot, that many AI models and tools use as a training and reference corpus.",
   ["Because Common Crawl is so widely reused, being present in it means your content can flow into many downstream models and datasets at once. CCBot is the bot that collects it, and your robots.txt decides whether it may.",
    "Allowing CCBot maximises how widely your content propagates into the AI ecosystem. Blocking it is a training-protection stance, the same trade-off as with GPTBot: wider footprint versus tighter control over training use."],
   ("CCBot vs a search crawler", "CCBot builds a general-purpose corpus reused across many models. A search crawler like OAI-SearchBot or PerplexityBot builds one engine's live citation index. One shapes broad training data; the other shapes whether you are cited in a specific product today."),
   "For a brand that wants the widest possible presence across AI systems, Common Crawl is a high-leverage corpus to be in. For one focused on controlling training use, CCBot is the bot to weigh most carefully.",
   [("/blogs/how-ai-crawlers-index-your-site","How AI Crawlers Actually Index Your Site")],
   [("oai-searchbot","OAI-SearchBot"),("gptbot-vs-oai-searchbot","GPTBot vs OAI-SearchBot"),("llms-txt","llms.txt")]),

  ("schema-markup", "Schema markup (structured data)",
   "Schema markup is structured data added to a page's code, using the Schema.org vocabulary, that labels what the content is, an organisation, an article, a FAQ, a product, so machines can interpret it unambiguously.",
   ["It does not change what a human sees; it adds a machine-readable layer that states the page's entities and relationships explicitly. This helps search and AI systems understand and confidently attribute the content.",
    "It correlates with being cited. In rawmktg's analysis, 53% of AI-cited pages carried valid schema, making cited pages markedly more likely to have structured data than uncited ones, though it supports rather than replaces clear on-page content."],
   ("Schema markup vs on-page content", "On-page content is what the model reads and quotes. Schema markup is metadata that tells the model what that content is and how its entities connect. The first earns the citation; the second reduces ambiguity about who and what is being cited."),
   "Schema is low-cost infrastructure that makes your pages easier for machines to classify and attribute correctly. In a field where misattribution is common, that clarity is a direct GEO advantage.",
   [("/blogs/schema-markup-ai-citations-2026","Schema Markup in 2026")],
   [("graph-schema","@graph"),("entity-resolution","Entity resolution"),("knowledge-graph","Knowledge graph")]),

  ("graph-schema", "@graph",
   "@graph is a Schema.org JSON-LD construct that lets a page declare multiple connected entities, such as an organisation, a person and an article, in a single structured-data block, with explicit relationships between them.",
   ["Instead of scattering separate, disconnected schema snippets across a page, an @graph groups them and links them by identifier. This lets a machine see that the article was written by this person, published by this organisation, as one connected model.",
    "That connectedness is what makes it powerful for AI: it resolves a coherent picture of who is behind the content and how the entities relate, which strengthens trust and accurate attribution."],
   ("@graph vs separate schema blocks", "Separate schema blocks describe entities in isolation and leave the relationships implicit. An @graph states the relationships explicitly in one place, so a machine does not have to guess how the organisation, author and content connect."),
   "For B2B brands, a well-built @graph ties the company, its author entities and its content into one machine-readable identity, which is the foundation of being recognised and cited as a consistent source.",
   [("/blogs/schema-markup-ai-citations-2026","Schema Markup in 2026")],
   [("schema-markup","Schema markup"),("entity-resolution","Entity resolution"),("knowledge-graph","Knowledge graph")]),

  ("entity-resolution", "Entity resolution",
   "Entity resolution is the process by which a search or AI system decides which real-world thing a name refers to, linking a brand, person or product to a single, disambiguated identity rather than treating mentions as loose strings of text.",
   ["When a model encounters your brand name, it has to determine which entity that is, and connect the scattered mentions of it across the web into one identity. Consistent naming, structured data and authoritative references all feed this.",
    "Gemini, in particular, resolves entities through Google's Knowledge Graph before it retrieves content, which means an unresolved or ambiguous brand can be skipped before the answer is even assembled."],
   ("Entity resolution vs keyword matching", "Keyword matching looks for the literal words on a page. Entity resolution identifies the thing those words refer to and links it to everything else known about it. The first is text; the second is identity, which is what modern engines reason over."),
   "If an engine cannot confidently resolve your brand as an entity, it is unlikely to recommend you, and may even confuse you with someone else. Clean, consistent entity signals are a precondition for being cited reliably.",
   [("/blogs/why-engines-recommend-different-vendors","Why ChatGPT, Perplexity and Gemini Recommend Different Vendors")],
   [("knowledge-graph","Knowledge graph"),("graph-schema","@graph"),("schema-markup","Schema markup")]),

  ("knowledge-graph", "Knowledge graph",
   "A knowledge graph is a structured network of entities, people, companies, products, places, and the relationships between them, that a search or AI system uses to understand and reason about the world rather than just match text.",
   ["Google's Knowledge Graph is the best-known example. Entities in it carry verified attributes and links to other entities, which lets a system answer questions about a thing and judge how trustworthy and well-connected it is.",
    "For AI search, the knowledge graph is often consulted before retrieval. If your brand is a resolved, well-connected entity, it is easier to surface and recommend; if it is absent, the engine has little structured basis to trust it."],
   ("Knowledge graph vs index", "An index is a list of pages a system can retrieve. A knowledge graph is a model of entities and how they relate. The index tells a system what pages exist; the knowledge graph tells it what things exist and which are trustworthy."),
   "Becoming a recognised entity in the knowledge graph, through consistent data, structured markup and authoritative mentions, is foundational: it is what lets AI systems treat your brand as a known, citable thing rather than an unknown string.",
   [("/blogs/hallucination-proofing-your-brand","Hallucination-Proofing Your Brand"),("/blogs/why-engines-recommend-different-vendors","Why ChatGPT, Perplexity and Gemini Recommend Different Vendors")],
   [("entity-resolution","Entity resolution"),("graph-schema","@graph"),("e-e-a-t","E-E-A-T")]),
 ]),

 ("Content & authority", [
  ("topical-authority", "Topical authority",
   "Topical authority is the depth and breadth of a brand's content across a subject area, which signals to search and AI systems that it is a credible source on that topic and makes it more likely to be cited for questions within it.",
   ["You build it by covering a topic comprehensively, with interlinked content that addresses the core question and its adjacent ones, rather than a single shallow page. Generative engines weigh this depth when deciding whom to trust on a subject.",
    "The practical structure is a cluster: a hub on the core topic plus connected entries on the sub-questions around it, linked together so the engine reads a coherent body of expertise rather than isolated articles."],
   ("Topical authority vs domain authority", "Domain authority is a site-wide score driven largely by backlinks. Topical authority is subject-specific depth. A site can have high domain authority overall and still lack topical authority on a given subject, which is why niche specialists often out-cite larger generalists."),
   "AI engines recommend sources they read as expert on the specific question asked. Concentrated topical authority is how a focused B2B brand becomes that source, even against bigger competitors with broader but shallower coverage.",
   [("/blogs/topical-authority-cluster-ai-shortlists","The Topical Authority Cluster")],
   [("authority-seeding","Authority seeding"),("e-e-a-t","E-E-A-T"),("content-half-life","Content half-life")]),

  ("e-e-a-t", "E-E-A-T",
   "E-E-A-T stands for Experience, Expertise, Authoritativeness and Trustworthiness: Google's framework for assessing content quality, which has now become a signal AI systems use when deciding which sources to cite.",
   ["Originally a set of human quality-rater guidelines, the same preferences have been wired into how models choose sources. Signals like clear authorship, demonstrated expertise, and corroboration from trusted sites all feed it.",
    "Its influence on AI citation is direct. In rawmktg's analysis, 96% of AI Overview citations went to sources Google already trusts on E-E-A-T grounds, which makes it close to a prerequisite for being cited."],
   ("E-E-A-T vs backlinks", "Backlinks are one input to authority. E-E-A-T is the broader judgement of whether content is experienced, expert, authoritative and trustworthy, including authorship, accuracy and reputation. A page can have backlinks and still fail E-E-A-T if it reads as low-trust."),
   "Because AI systems inherit these preferences, E-E-A-T is no longer just an SEO concern; it is a citation gatekeeper. Clear authorship, real expertise and verifiable claims are what get a B2B brand into the trusted set.",
   [("/blogs/eeat-is-an-ai-signal-now","E-E-A-T Is an AI Signal Now")],
   [("topical-authority","Topical authority"),("authority-seeding","Authority seeding"),("brand-hallucination","Brand hallucination")]),

  ("content-half-life", "Content half-life",
   "Content half-life is the rate at which a page loses its AI citations as it ages without being updated, reflecting that recency is now a hard ranking signal in AI search rather than a minor freshness bonus.",
   ["Generative engines, especially real-time ones, treat freshness as a retrieval factor. Content that is not refreshed decays out of the citation set even if it was once authoritative, because the engine prefers current sources.",
    "The decay is measurable. In rawmktg's analysis, pages not updated in 90 days were 3.2x more likely to lose their AI citations entirely, which reframes maintenance from optional polish to a core part of holding visibility."],
   ("Content half-life vs evergreen content", "Evergreen content assumes a topic stays valid for years with little change. Content half-life recognises that in AI search even durable topics need a refresh cadence to keep their citations, because the engine rewards recency regardless of how timeless the subject is."),
   "It turns maintenance into a ranking lever. A programmatic refresh cadence on your highest-value pages is often the cheapest way to defend AI visibility you have already earned.",
   [("/blogs/30-day-content-half-life-recency-ai-ranking-signal","The 30-Day Content Half-Life")],
   [("topical-authority","Topical authority"),("llm-citation","LLM citation"),("e-e-a-t","E-E-A-T")]),

  ("authority-seeding", "Authority seeding",
   "Authority seeding is the practice of building a brand's reputation across third-party sites, communities and publications so that AI systems encounter consistent, trusted signals about it off-site, not just on the brand's own pages.",
   ["Generative engines weigh how a brand is discussed across the wider web, not only what it says about itself. Seeding means earning mentions, contributions and references in the places models read and trust.",
    "Off-site signals can outweigh links. In rawmktg's analysis, unlinked brand mentions correlated with AI citation visibility far more strongly than traditional backlinks (r=0.664 versus r=0.218), which reframes where authority work should focus."],
   ("Authority seeding vs link building", "Link building chases backlinks as a ranking input. Authority seeding builds presence and mentions across trusted sources, linked or not, because for AI citation the mention itself, and the trust of the place it appears, carries the weight."),
   "AI engines recommend brands the wider web already vouches for. Seeding that off-site trust footprint is often the highest-leverage GEO work, and the one most on-page-focused competitors neglect.",
   [("/blogs/authority-seeding-ai-llm-trust","Authority Seeding for AI")],
   [("unlinked-brand-mentions","Unlinked brand mentions"),("e-e-a-t","E-E-A-T"),("topical-authority","Topical authority")]),

  ("unlinked-brand-mentions", "Unlinked brand mentions",
   "Unlinked brand mentions are references to a brand by name across the web that do not include a hyperlink, and which AI systems still read as trust and authority signals when deciding whom to cite.",
   ["Traditional SEO valued mentions mainly when they carried a link. AI systems parse the text itself, so a brand named in a trusted article counts as a signal even with no link attached.",
    "Their weight is striking. In rawmktg's analysis, unlinked mentions correlated with AI citation roughly three times more strongly than backlinks (r=0.664 versus r=0.218), which makes earning mentions, not just links, a primary objective."],
   ("Unlinked mentions vs backlinks", "A backlink is a clickable link counted by search engines. An unlinked mention is the brand named in text with no link. For classic ranking the link mattered most; for AI citation the mention itself is often the stronger signal."),
   "It changes what a PR or content effort should optimise for. Getting named in the right places, even without a link, builds the off-site trust that AI engines use to decide who belongs in an answer.",
   [("/blogs/authority-seeding-ai-llm-trust","Authority Seeding for AI")],
   [("authority-seeding","Authority seeding"),("e-e-a-t","E-E-A-T"),("citation-gap","Citation gap")]),

  ("brand-hallucination", "Brand hallucination",
   "A brand hallucination is when an AI system states something false or misleading about a brand, such as wrong features, wrong category or invented facts, because it lacks clear, consistent, machine-readable information to draw on.",
   ["Models generate the most probable answer from what they can find. Where a brand's information is thin, inconsistent or ambiguous, the model fills the gap with plausible but wrong details, sometimes at the exact moment a buyer is deciding.",
    "The fix is structural: clear claim-anchoring, consistent entity data, schema, and self-contained answers that leave little room for the model to guess. Pairing claims with proof and resolving the brand as a clean entity measurably reduces it."],
   ("Brand hallucination vs misinformation", "Misinformation is false content deliberately or carelessly published by people. A brand hallucination is false content generated by a model filling an information gap. The remedy for one is correction; the remedy for the other is supplying clear, structured, verifiable signals so the gap does not exist."),
   "An AI getting your brand wrong at the point of highest buyer intent is a direct revenue risk. Reducing hallucination is about controlling the inputs the model reasons from, so the answer it generates about you is accurate.",
   [("/blogs/hallucination-proofing-your-brand","Hallucination-Proofing Your Brand")],
   [("knowledge-graph","Knowledge graph"),("proof-pairing-density","Proof-Pairing Density"),("entity-resolution","Entity resolution")]),

  ("answer-lead-formatting", "Answer-lead formatting",
   "Answer-lead formatting is a content structure that puts the direct answer to a question first, at the top of a page or section, before any context or build-up, so an AI system can extract it without reading further.",
   ["Because engines extract from the top of a page, leading with the answer aligns the content with how retrieval actually works. The supporting detail, nuance and evidence follow the answer rather than preceding it.",
    "It is the formatting discipline behind the Answer Capsule. In rawmktg's analysis roughly 55% of citations came from the first 30% of the page, so an answer placed first is structurally far more likely to be the part that gets cited."],
   ("Answer-lead vs narrative formatting", "Narrative formatting builds context first and reveals the point later, which reads well for humans but buries the answer where a model is less likely to extract it. Answer-lead formatting inverts this, stating the conclusion first and the reasoning after."),
   "It is one of the simplest, highest-impact changes a B2B page can make for AI visibility: restructure so the answer comes first, and the part most likely to be cited is the part you most want quoted.",
   [("/blogs/anatomy-of-a-high-citation-page","Anatomy of a High-Citation Page")],
   [("answer-capsule","Answer Capsule"),("llm-citation","LLM citation"),("retrieval-augmented-generation","RAG")]),
 ]),

 ("Measurement", [
  ("prompt-to-citation-tracking", "Prompt-to-citation tracking",
   "Prompt-to-citation tracking is the practice of measuring AI visibility by running a fixed set of buyer prompts across AI engines on a cadence and recording which brands get cited, since standard web analytics cannot see most of it.",
   ["You build a representative set of prompts, run them across the target engines repeatedly, and log the citations. This produces a measurable read on whether you appear in AI answers and how that changes over time.",
    "It exists because AI traffic is largely invisible to default analytics. In rawmktg's testing, GA4 misses roughly 30% of AI referrers and misclassifies many of the rest, so a prompt-based method is the only reliable way to see AI presence."],
   ("Prompt-to-citation tracking vs rank tracking", "Rank tracking records where your pages sit in classic search results. Prompt-to-citation tracking records whether your brand is named in AI answers. The first measures position in a list; the second measures presence in the synthesised response, which is where AI-era visibility actually lives."),
   "It is how GEO becomes accountable. Without it, AI visibility is a guess; with it, you have a number you can benchmark, tie to pipeline, and report to the business.",
   [("/blogs/prompt-to-citation-tracking","Prompt-to-Citation Tracking")],
   [("prompt-portfolio","Prompt portfolio"),("share-of-model","Share of Model"),("ai-referral-traffic","AI referral traffic")]),

  ("prompt-portfolio", "Prompt portfolio",
   "A prompt portfolio is a curated, fixed set of buyer-intent prompts that a brand runs across AI engines on a regular cadence to measure its citation visibility consistently over time.",
   ["The prompts are chosen to mirror how real buyers ask, spanning the questions that matter across the funnel. Keeping the set fixed is what makes the measurement comparable from one run to the next.",
    "A good portfolio is segmented, for example by money, problem and proof intent, so you can see not just whether you appear but where in the buyer journey you appear and where you are absent."],
   ("Prompt portfolio vs keyword list", "A keyword list targets the short phrases people type into a search box. A prompt portfolio captures the longer, conversational questions people ask an AI assistant. The first drives classic SEO; the second is the measurement instrument for AI visibility."),
   "It is the backbone of any serious GEO measurement programme. A well-built prompt portfolio turns AI visibility from an anecdote into a repeatable, comparable metric you can act on.",
   [("/blogs/prompt-to-citation-tracking","Prompt-to-Citation Tracking")],
   [("prompt-to-citation-tracking","Prompt-to-citation tracking"),("share-of-model","Share of Model"),("ai-referral-traffic","AI referral traffic")]),

  ("ai-referral-traffic", "AI referral traffic",
   "AI referral traffic is the visits a website receives from AI assistants and answer engines, such as ChatGPT, Perplexity and Google AI Overviews, when a user follows a cited source into the site.",
   ["It is a distinct channel from organic search, and a high-intent one: a visitor arriving from an AI answer has often been pre-qualified by the model's reasoning before they click. In rawmktg's analysis, AI-sourced sessions converted at roughly 4.4x the organic rate.",
    "It is also hard to see. Standard analytics undercount and misclassify it; in rawmktg's testing GA4 misses around 30% of AI referrers, routing them into direct or referral buckets, so it needs deliberate measurement to track accurately."],
   ("AI referral traffic vs organic traffic", "Organic traffic comes from clicks on classic search results. AI referral traffic comes from clicks on citations inside AI answers. The volume is usually smaller, but the intent and conversion rate are typically much higher, and standard analytics see it far less reliably."),
   "It is the bottom-of-funnel payoff of GEO. Even at lower volume, its conversion rate means a small amount of AI referral traffic can outweigh a much larger amount of generic organic, which is why measuring it correctly matters.",
   [("/blogs/prompt-to-citation-tracking","Prompt-to-Citation Tracking")],
   [("prompt-to-citation-tracking","Prompt-to-citation tracking"),("share-of-model","Share of Model"),("llm-citation","LLM citation")]),
 ]),

 ("Bridging SEO terms", [
  ("link-intersect", "Link intersect",
   "Link intersect is a backlink-analysis technique that finds the domains linking to several of your competitors but not to you, surfacing the specific sites most likely to link to a brand in your category.",
   ["By overlapping the backlink profiles of multiple competitors, you isolate the sources that consistently link to players in your space. Those shared linkers are the highest-probability targets for your own outreach.",
    "rawmktg used exactly this method across India's cross-border payments brands, classifying tens of thousands of referring pages to find which topics and which domains actually win links in the category, rather than guessing."],
   ("Link intersect vs a backlink audit", "A backlink audit reviews the links you already have. A link intersect looks outward at the links your competitors have and you do not, turning competitor profiles into a prioritised target list rather than a report on your current state."),
   "It is one of the most efficient ways to plan link and authority building: instead of cold-guessing prospects, you start from the domains already proven to link to brands like yours.",
   [("/blogs/cross-border-backlinks","Beyond Cross-Border: Where India's Global-Payments Brands Earn Their Backlinks")],
   [("referring-domains","Referring domains"),("domain-rating","Domain Rating"),("authority-seeding","Authority seeding")]),

  ("domain-rating", "Domain Rating (DR)",
   "Domain Rating (DR) is a 0-to-100 score, popularised by Ahrefs, that estimates the strength of a website's backlink profile relative to other sites, used as a rough proxy for overall authority.",
   ["DR rises as a site earns links from other strong domains. It is comparative and logarithmic, so moving from a low DR to a mid DR is far easier than climbing at the top of the scale.",
    "It is a useful shorthand but a limited one for AI search. In rawmktg's teardowns, high DR did not reliably predict AI citation visibility; brands with modest DR sometimes out-cited far stronger domains, because citation depends on more than backlink strength."],
   ("Domain Rating vs topical authority", "Domain Rating measures site-wide backlink strength. Topical authority measures subject-specific depth. A site can have high DR overall and weak authority on a given topic, which is why DR alone is a poor predictor of who gets cited for a specific question."),
   "DR is a helpful benchmark for competitive context, but treating it as the goal misleads in AI search. It is an input to authority, not a substitute for the topical depth and trust signals that actually earn citations.",
   [("/blogs/container-tracking-saas-seo-geo-analysis","We Analysed 6 Container Tracking SaaS Companies")],
   [("referring-domains","Referring domains"),("link-intersect","Link intersect"),("topical-authority","Topical authority")]),

  ("referring-domains", "Referring domains",
   "Referring domains are the number of unique websites that link to a given site, a backlink metric that counts distinct linking sources rather than the total number of individual links.",
   ["One domain can link to you many times, but it still counts as a single referring domain. This makes the metric a better measure of breadth of endorsement than raw link count, which a single site can inflate.",
    "Gaps here are often large and revealing. In rawmktg's CX SaaS teardown, the spread ran to thousands of missing referring domains between leaders and laggards, marking exactly where the authority gap, and the opportunity, sat."],
   ("Referring domains vs backlinks", "Backlinks count every individual link, so one site linking ten times is ten backlinks. Referring domains count unique linking sites, so the same case is one referring domain. The second is the more honest measure of how many distinct sources vouch for you."),
   "Referring domains are a clean read on how broadly the web endorses a brand, which underpins both classic authority and the off-site trust AI engines weigh. Growing unique sources matters more than accumulating repeat links.",
   [("/blogs/cross-border-backlinks","Beyond Cross-Border: Where India's Global-Payments Brands Earn Their Backlinks"),("/blogs/cx-saas-seo-discoverability-analysis","We Analysed 6 CX SaaS Companies")],
   [("link-intersect","Link intersect"),("domain-rating","Domain Rating"),("unlinked-brand-mentions","Unlinked brand mentions")]),
 ]),
]

# flat list for schema / hub
ALL = [(g, t) for g, terms in GROUPS for t in terms]
print("Total terms:", len(ALL))

NAV = '''<nav class="site-nav" aria-label="Site navigation">
  <div class="page"><div class="nav-row">
    <a href="/" class="rm-logo" aria-label="rawmktg home">raw<span class="mktg">mktg</span><span class="dot">.</span></a>
    <div class="nav-links">
      <div class="nav-dropdown">
        <button class="nav-trigger" aria-haspopup="true" aria-expanded="false">Articles <span class="caret" aria-hidden="true">&#9662;</span></button>
        <div class="nav-menu" role="menu">
          <a role="menuitem" href="/topics/industry-teardowns"><span class="nm-num">01</span>The industry teardowns</a>
          <a role="menuitem" href="/topics/how-ai-search-works"><span class="nm-num">02</span>How AI search actually works</a>
          <a role="menuitem" href="/topics/technical-layer"><span class="nm-num">03</span>The technical layer</a>
          <a role="menuitem" href="/topics/content-authority"><span class="nm-num">04</span>Content &amp; authority architecture</a>
          <a role="menuitem" href="/topics/ranking-signals"><span class="nm-num">05</span>Ranking signals &amp; measurement</a>
        </div>
      </div>
      <a href="/glossary" class="active">Glossary</a>
      <a href="/#about">About</a>
      <a href="/#newsletter" class="cta">Subscribe</a>
    </div>
  </div></div>
</nav>'''

ADSENSE = '''<script>(function(){var l=false;function load(){if(l)return;l=true;var s=document.createElement('script');s.async=true;s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852';s.crossOrigin='anonymous';document.head.appendChild(s);}var ev=['scroll','mousemove','touchstart','keydown','click'];ev.forEach(function(e){window.addEventListener(e,load,{passive:true,once:true});});setTimeout(load,3000);})();</script>'''

ENTRY_STYLE = '''  <style>
    :root{--paper:#F2EFE8;--paper-2:#ECE7DD;--ink:#2A2722;--ink-2:#4D4742;--mute:#8A8278;--faint:#C5BFB4;--rule:#D6D0C5;--rule-2:#B4ADA2;--signal:#D04A2A;--signal-soft:#F1D9CC;--f-display:'Space Grotesk',system-ui,sans-serif;--f-prose:'Azeret Mono',ui-monospace,monospace;--f-mono:'JetBrains Mono',ui-monospace,monospace;--f-logo:'Geist',system-ui,sans-serif;}
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
    html{scroll-behavior:smooth;}
    body{background:var(--paper);color:var(--ink);font-family:var(--f-prose);font-size:16px;-webkit-font-smoothing:antialiased;min-height:100vh;display:flex;flex-direction:column;}
    a{color:inherit;text-decoration:none;}
    .page{max-width:1080px;margin:0 auto;padding:0 32px;}
    .site-nav{border-bottom:1px solid var(--rule);background:var(--paper);position:sticky;top:0;z-index:100;}
    .nav-row{height:60px;display:flex;align-items:center;justify-content:space-between;}
    .rm-logo{font-family:var(--f-logo);font-weight:800;font-size:20px;letter-spacing:-0.045em;display:inline-flex;align-items:baseline;line-height:1;color:var(--ink);}
    .rm-logo .mktg{color:var(--ink-2);}.rm-logo .dot{color:var(--signal);}
    .nav-links{display:flex;align-items:center;gap:24px;font-family:var(--f-mono);font-size:11px;font-weight:500;letter-spacing:0.14em;text-transform:uppercase;color:var(--mute);}
    .nav-links>a{transition:color 0.15s;}.nav-links>a:hover,.nav-links>a.active{color:var(--ink);}.nav-links a.cta{color:var(--signal);}
    .nav-dropdown{position:relative;}
    .nav-trigger{font:inherit;color:var(--mute);background:none;border:0;cursor:pointer;letter-spacing:0.14em;text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;padding:0;transition:color 0.15s;}
    .nav-trigger:hover,.nav-dropdown:hover .nav-trigger,.nav-dropdown:focus-within .nav-trigger{color:var(--ink);}
    .nav-trigger .caret{font-size:9px;color:var(--faint);}
    .nav-menu{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%) translateY(-6px);background:var(--paper);border:1px solid var(--rule);border-radius:10px;box-shadow:0 10px 30px rgba(42,39,34,0.12);padding:8px;min-width:300px;opacity:0;visibility:hidden;transition:opacity 0.15s,transform 0.15s;z-index:200;}
    .nav-menu::before{content:"";position:absolute;top:-14px;left:0;right:0;height:14px;}
    .nav-dropdown:hover .nav-menu,.nav-dropdown:focus-within .nav-menu{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0);}
    .nav-menu a{display:block;padding:10px 12px;border-radius:6px;font-family:var(--f-mono);font-size:10.5px;font-weight:500;letter-spacing:0.10em;text-transform:uppercase;color:var(--ink-2);transition:background 0.12s,color 0.12s;white-space:nowrap;}
    .nav-menu a:hover{background:var(--paper-2);color:var(--signal);}.nav-menu .nm-num{color:var(--faint);margin-right:8px;}
    .gloss{flex:1;padding:56px 0 80px;}
    .gloss-wrap{max-width:760px;}
    .gloss-crumb{font-family:var(--f-mono);font-size:11px;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:var(--mute);margin-bottom:18px;}
    .gloss-crumb a{color:var(--signal);}
    .gloss-eyebrow{font-family:var(--f-mono);font-size:11px;font-weight:600;letter-spacing:0.20em;text-transform:uppercase;color:var(--signal);margin-bottom:14px;}
    .gloss h1{font-family:var(--f-display);font-weight:700;font-size:clamp(28px,4vw,42px);line-height:1.08;letter-spacing:-0.03em;color:var(--ink);margin-bottom:24px;}
    .capsule{font-family:var(--f-prose);font-size:18px;line-height:1.6;color:var(--ink);padding:4px 0 4px 20px;border-left:3px solid var(--signal);margin-bottom:36px;}
    .gloss h2{font-family:var(--f-display);font-weight:700;font-size:20px;letter-spacing:-0.02em;color:var(--ink);margin:34px 0 12px;padding-top:24px;border-top:1px solid var(--rule);}
    .gloss p{font-family:var(--f-prose);font-size:15.5px;line-height:1.72;color:var(--ink-2);margin-bottom:16px;}
    .gloss strong{color:var(--ink);font-weight:600;}
    .gloss-foot{margin-top:40px;padding-top:24px;border-top:1px solid var(--rule);display:flex;flex-direction:column;gap:14px;}
    .gloss-foot .row-label{font-family:var(--f-mono);font-size:10px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:var(--faint);margin-bottom:8px;}
    .gloss-foot .links{display:flex;flex-wrap:wrap;gap:10px 18px;}
    .gloss-foot a{font-family:var(--f-prose);font-size:14px;color:var(--signal);border-bottom:1px solid var(--signal-soft);padding-bottom:1px;transition:border-color 0.15s;}
    .gloss-foot a:hover{border-color:var(--signal);}
    .gloss-foot .related a{color:var(--ink-2);border-bottom-color:var(--rule);}
    .site-foot{border-top:1px solid var(--rule);padding:28px 0 40px;}
    .foot-row{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;font-family:var(--f-mono);font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--mute);}
    .foot-row a:hover{color:var(--ink);}.foot-links{display:flex;gap:20px;}
    @media(max-width:768px){.page{padding:0 20px;}.nav-links{display:none;}}
  </style>'''

FONTS = '''  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Azeret+Mono:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" /></noscript>'''

FAVICONS = '''  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/favicon-180.png" />
  <link rel="alternate" type="application/rss+xml" title="rawmktg." href="https://rawmktg.com/feed.xml" />'''

def esc(s): return s.replace('"', "&quot;")

os.makedirs("glossary", exist_ok=True)

def render_entry(slug, term, capsule, hiw, vs, why, deeper, related):
    url = f"https://rawmktg.com/glossary/{slug}"
    desc = esc(capsule if len(capsule) <= 300 else capsule[:297] + "...")
    hiw_html = "\n      ".join(f"<p>{p}</p>" for p in hiw)
    deeper_html = "".join(f'<a href="{u}">{l}</a>' for u, l in deeper)
    related_html = "".join(f'<a href="/glossary/{s}">{l}</a>' for s, l in related)
    defined_term = {"@context":"https://schema.org","@type":"DefinedTerm","name":term,"description":capsule,"url":url,"inDefinedTermSet":"https://rawmktg.com/glossary","dateModified":TODAY}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f"What is {term}?","acceptedAnswer":{"@type":"Answer","text":capsule}}]}
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="robots" content="index, follow" />
  <title>What is {term}? &middot; rawmktg.</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{desc}" />
  <meta name="author" content="Vinayak Ravi" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="What is {term}? &middot; rawmktg." />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />
  <meta property="og:site_name" content="rawmktg." />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="What is {term}? &middot; rawmktg." />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />
  <script type="application/ld+json">{json.dumps(defined_term)}</script>
  <script type="application/ld+json">{json.dumps(faq)}</script>
{FAVICONS}
  <link rel="alternate" type="text/markdown" href="/glossary/{slug}.md" />
{FONTS}
{ENTRY_STYLE}
  {ADSENSE}
</head>
<body>
<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at https://rawmktg.com/glossary/{slug}.md. Optimized for AI and LLM tools.</div>

{NAV}

<main class="gloss">
  <div class="page">
    <div class="gloss-wrap">
      <div class="gloss-crumb"><a href="/">rawmktg.</a> / <a href="/glossary">Glossary</a></div>
      <div class="gloss-eyebrow">AI-Search Glossary</div>
      <h1>What is {term}?</h1>
      <p class="capsule">{capsule}</p>
      <h2>How it works</h2>
      {hiw_html}
      <h2>{vs[0]}</h2>
      <p>{vs[1]}</p>
      <h2>Why it matters for B2B</h2>
      <p>{why}</p>
      <div class="gloss-foot">
        <div><div class="row-label">Go deeper</div><div class="links">{deeper_html}</div></div>
        <div class="related"><div class="row-label">Related terms</div><div class="links">{related_html}</div></div>
      </div>
    </div>
  </div>
</main>

<footer class="site-foot" aria-label="Site footer">
  <div class="page"><div class="foot-row">
    <a href="/" style="font-family:'Geist',system-ui;font-weight:800;font-size:15px;letter-spacing:-0.04em;">raw<span style="color:var(--ink-2)">mktg</span><span style="color:var(--signal)">.</span></a>
    <div class="foot-links"><a href="/glossary">Glossary</a><a href="/#about">About</a><a href="mailto:vinayak@rawmktg.com">Contact</a></div>
    <span>&copy; 2026 rawmktg.</span>
  </div></div>
</footer>
</body>
</html>
'''

def render_md(slug, term, capsule, hiw, vs, why):
    parts = [f"# What is {term}?", "", capsule, "", "## How it works"]
    parts += hiw
    parts += ["", f"## {vs[0]}", vs[1], "", "## Why it matters for B2B", why, "",
              f"*Source: https://rawmktg.com/glossary/{slug} · rawmktg. by Vinayak Ravi*", ""]
    return "\n".join(parts)

for group, term in [(g, t) for g, ts in GROUPS for t in ts]:
    slug, name, capsule, hiw, vs, why, deeper, related = term
    open(f"glossary/{slug}.html", "w", encoding="utf-8").write(render_entry(*term))
    open(f"glossary/{slug}.md", "w", encoding="utf-8").write(render_md(slug, name, capsule, hiw, vs, why))
print("Wrote", len(ALL), "entry pages + .md twins")

# ── short def for hub rows (predicate of the capsule) ──
def shortdef(name, capsule):
    parts = re.split(r"\b(?:is|are)\b", capsule, maxsplit=1)
    s = (parts[1].strip() if len(parts) > 1 else capsule).strip()
    s = s[0].upper() + s[1:] if s else s
    if "." in s: s = s.split(".")[0]
    if len(s) > 165:
        s = s[:160].rsplit(" ", 1)[0]
    return s.rstrip(",;:") + "."

HUB_STYLE = '''  <style>
    :root{--paper:#F2EFE8;--paper-2:#ECE7DD;--ink:#2A2722;--ink-2:#4D4742;--mute:#8A8278;--faint:#C5BFB4;--rule:#D6D0C5;--rule-2:#B4ADA2;--signal:#D04A2A;--signal-soft:#F1D9CC;--f-display:'Space Grotesk',system-ui,sans-serif;--f-prose:'Azeret Mono',ui-monospace,monospace;--f-mono:'JetBrains Mono',ui-monospace,monospace;--f-logo:'Geist',system-ui,sans-serif;}
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
    html{scroll-behavior:smooth;}
    body{background:var(--paper);color:var(--ink);font-family:var(--f-prose);font-size:16px;-webkit-font-smoothing:antialiased;}
    a{color:inherit;text-decoration:none;}
    .page{max-width:1080px;margin:0 auto;padding:0 32px;}
    .site-nav{border-bottom:1px solid var(--rule);background:var(--paper);position:sticky;top:0;z-index:100;}
    .nav-row{height:60px;display:flex;align-items:center;justify-content:space-between;}
    .rm-logo{font-family:var(--f-logo);font-weight:800;font-size:20px;letter-spacing:-0.045em;display:inline-flex;align-items:baseline;line-height:1;color:var(--ink);}
    .rm-logo .mktg{color:var(--ink-2);}.rm-logo .dot{color:var(--signal);}
    .nav-links{display:flex;align-items:center;gap:24px;font-family:var(--f-mono);font-size:11px;font-weight:500;letter-spacing:0.14em;text-transform:uppercase;color:var(--mute);}
    .nav-links>a{transition:color 0.15s;}.nav-links>a:hover,.nav-links>a.active{color:var(--ink);}.nav-links a.cta{color:var(--signal);}
    .nav-dropdown{position:relative;}
    .nav-trigger{font:inherit;color:var(--mute);background:none;border:0;cursor:pointer;letter-spacing:0.14em;text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;padding:0;transition:color 0.15s;}
    .nav-trigger:hover,.nav-dropdown:hover .nav-trigger,.nav-dropdown:focus-within .nav-trigger{color:var(--ink);}
    .nav-trigger .caret{font-size:9px;color:var(--faint);}
    .nav-menu{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%) translateY(-6px);background:var(--paper);border:1px solid var(--rule);border-radius:10px;box-shadow:0 10px 30px rgba(42,39,34,0.12);padding:8px;min-width:300px;opacity:0;visibility:hidden;transition:opacity 0.15s,transform 0.15s;z-index:200;}
    .nav-menu::before{content:"";position:absolute;top:-14px;left:0;right:0;height:14px;}
    .nav-dropdown:hover .nav-menu,.nav-dropdown:focus-within .nav-menu{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0);}
    .nav-menu a{display:block;padding:10px 12px;border-radius:6px;font-family:var(--f-mono);font-size:10.5px;font-weight:500;letter-spacing:0.10em;text-transform:uppercase;color:var(--ink-2);transition:background 0.12s,color 0.12s;white-space:nowrap;}
    .nav-menu a:hover{background:var(--paper-2);color:var(--signal);}.nav-menu .nm-num{color:var(--faint);margin-right:8px;}
    .gloss-hero{padding:64px 0 44px;border-bottom:1px solid var(--rule);}
    .gloss-hero .eyebrow{font-family:var(--f-mono);font-size:11px;font-weight:600;letter-spacing:0.20em;text-transform:uppercase;color:var(--signal);margin-bottom:16px;}
    .gloss-hero h1{font-family:var(--f-display);font-weight:700;font-size:clamp(30px,4.5vw,48px);line-height:1.06;letter-spacing:-0.03em;color:var(--ink);margin-bottom:20px;max-width:760px;}
    .gloss-hero p{font-family:var(--f-prose);font-size:16px;line-height:1.7;color:var(--ink-2);max-width:680px;margin-bottom:16px;}
    .gloss-hero p:last-child{margin-bottom:0;}
    .gloss-body{padding:48px 0 80px;}
    .gloss-group{margin-bottom:44px;}
    .gloss-group-label{font-family:var(--f-mono);font-size:11px;font-weight:600;letter-spacing:0.20em;text-transform:uppercase;color:var(--mute);padding-bottom:12px;border-bottom:1px solid var(--rule);margin-bottom:6px;}
    .term-row{display:block;padding:18px 0;border-bottom:1px solid var(--rule);transition:padding 0.12s;}
    .term-row:hover{padding-left:6px;}
    .term-row .term-name{font-family:var(--f-display);font-weight:700;font-size:17px;letter-spacing:-0.01em;color:var(--ink);display:inline-flex;align-items:center;gap:8px;transition:color 0.15s;}
    .term-row:hover .term-name{color:var(--signal);}
    .term-row .term-arrow{color:var(--faint);font-family:var(--f-mono);font-size:14px;transition:color 0.15s,transform 0.15s;}
    .term-row:hover .term-arrow{color:var(--signal);transform:translateX(3px);}
    .term-row .term-def{font-family:var(--f-prose);font-size:14px;line-height:1.6;color:var(--mute);margin-top:6px;max-width:760px;}
    .site-foot{border-top:1px solid var(--rule);padding:28px 0 40px;}
    .foot-row{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;font-family:var(--f-mono);font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--mute);}
    .foot-row a:hover{color:var(--ink);}.foot-links{display:flex;gap:20px;}
    @media(max-width:768px){.page{padding:0 20px;}.nav-links{display:none;}}
  </style>'''

# ── hub page ──
groups_html = ""
hub_terms_schema = []
md_lines = ["# The AI-Search Glossary", "",
            "> Plain, sourced definitions of the vocabulary of AI search and GEO, by rawmktg. (Vinayak Ravi). Source: https://rawmktg.com/glossary", ""]
for group, terms in GROUPS:
    groups_html += f'\n    <div class="gloss-group">\n      <div class="gloss-group-label">{group}</div>\n'
    md_lines.append(f"## {group}")
    for slug, name, capsule, hiw, vs, why, deeper, related in terms:
        sd = shortdef(name, capsule)
        groups_html += (f'      <a href="/glossary/{slug}" class="term-row">\n'
                        f'        <span class="term-name">{name} <span class="term-arrow" aria-hidden="true">&rarr;</span></span>\n'
                        f'        <div class="term-def">{sd}</div>\n      </a>\n')
        hub_terms_schema.append({"@type":"DefinedTerm","name":name,"url":f"https://rawmktg.com/glossary/{slug}"})
        md_lines.append(f"- [{name}](https://rawmktg.com/glossary/{slug}): {sd}")
    groups_html += "    </div>\n"
    md_lines.append("")

dts = {"@context":"https://schema.org","@type":"DefinedTermSet","name":"rawmktg. AI-Search Glossary","url":"https://rawmktg.com/glossary","description":"Definitions of the vocabulary of AI search and Generative Engine Optimization.","hasDefinedTerm":hub_terms_schema}

hub = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="robots" content="index, follow" />
  <title>The AI-Search Glossary &middot; rawmktg.</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="Plain, sourced definitions of the vocabulary of AI search and GEO: Generative Engine Optimization, RAG, AI Overviews, Answer Capsule, Share of Model and more." />
  <meta name="author" content="Vinayak Ravi" />
  <link rel="canonical" href="https://rawmktg.com/glossary" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://rawmktg.com/glossary" />
  <meta property="og:title" content="The AI-Search Glossary &middot; rawmktg." />
  <meta property="og:description" content="Plain, sourced definitions of the vocabulary of AI search and GEO." />
  <meta property="og:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />
  <meta property="og:site_name" content="rawmktg." />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="The AI-Search Glossary &middot; rawmktg." />
  <meta name="twitter:description" content="Plain, sourced definitions of the vocabulary of AI search and GEO." />
  <meta name="twitter:image" content="https://rawmktg.com/assets/images/rawmktg-homepage-og.png" />
  <script type="application/ld+json">{json.dumps(dts)}</script>
{FAVICONS}
  <link rel="alternate" type="text/markdown" href="/glossary.md" />
{FONTS}
{HUB_STYLE}
  {ADSENSE}
</head>
<body>
<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at https://rawmktg.com/glossary.md. Optimized for AI and LLM tools.</div>

{NAV}

<header class="gloss-hero">
  <div class="page">
    <div class="eyebrow">AI-Search Glossary</div>
    <h1>The vocabulary of AI search, defined.</h1>
    <p>AI search introduced a new working vocabulary, and most of it is still being defined in real time. This glossary is our attempt to define it plainly and accurately: what each term means, how the mechanism actually works, and why it matters for a B2B brand trying to get cited.</p>
    <p>Every definition is built on the same research behind our deep articles, and every entry links to the work underneath it. Where a figure appears, it is drawn from our own published analyses. If a term changes, the entry changes with it.</p>
  </div>
</header>

<main class="gloss-body">
  <div class="page">{groups_html}  </div>
</main>

<footer class="site-foot" aria-label="Site footer">
  <div class="page"><div class="foot-row">
    <a href="/" style="font-family:'Geist',system-ui;font-weight:800;font-size:15px;letter-spacing:-0.04em;">raw<span style="color:var(--ink-2)">mktg</span><span style="color:var(--signal)">.</span></a>
    <div class="foot-links"><a href="/#about">About</a><a href="mailto:vinayak@rawmktg.com">Contact</a><a href="/llms.txt">llms.txt</a></div>
    <span>&copy; 2026 rawmktg.</span>
  </div></div>
</footer>
</body>
</html>
'''
# the nav on the hub should mark Glossary active (already class="active" in NAV)
open("glossary.html", "w", encoding="utf-8").write(hub)
open("glossary.md", "w", encoding="utf-8").write("\n".join(md_lines))
print("Wrote glossary.html hub + glossary.md")

# ── nav rollout: add Glossary link site-wide ──
import glob as _g
rolled = 0
for f in ["index.html","privacy.html","404.html"] + _g.glob("topics/*.html") + _g.glob("blogs/*.html"):
    h = open(f, encoding="utf-8").read()
    if ">Glossary</a>" in h: continue
    h2 = re.sub(r'(<a href="/?#about">About</a>)', '<a href="/glossary">Glossary</a>\n        \\1', h, count=1)
    if h2 != h: open(f, "w", encoding="utf-8").write(h2); rolled += 1
print("Added Glossary to nav on", rolled, "pages")

# ── sitemap ──
sm = open("sitemap.xml", encoding="utf-8").read()
if "/glossary<" not in sm and "/glossary</loc" not in sm and "rawmktg.com/glossary<" not in sm:
    entries = f"  <url>\n    <loc>https://rawmktg.com/glossary</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>\n"
    for slug, *_ in [(t[0],) for g,ts in GROUPS for t in ts]:
        entries += f"  <url>\n    <loc>https://rawmktg.com/glossary/{slug}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>\n"
    sm = sm.replace("</urlset>", entries + "</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("sitemap.xml: added /glossary + term URLs")
else:
    print("sitemap already has /glossary")

# ── netlify.toml: content-type for glossary .md + edge function coverage ──
toml = open("netlify.toml", encoding="utf-8").read()
add = ""
if '/glossary/*.md' not in toml:
    add += '\n[[headers]]\n  for = "/glossary/*.md"\n  [headers.values]\n    Content-Type = "text/markdown; charset=utf-8"\n'
    add += '\n[[headers]]\n  for = "/glossary.md"\n  [headers.values]\n    Content-Type = "text/markdown; charset=utf-8"\n'
if 'path = "/glossary"' not in toml:
    add += '\n[[edge_functions]]\n  path = "/glossary"\n  function = "md-negotiate"\n'
    add += '\n[[edge_functions]]\n  path = "/glossary/*"\n  function = "md-negotiate"\n'
if add:
    open("netlify.toml", "w", encoding="utf-8").write(toml + add)
    print("netlify.toml: added glossary headers + edge functions")
else:
    print("netlify.toml already wired for glossary")
print("GLOSSARY BUILD COMPLETE")
