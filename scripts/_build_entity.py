#!/usr/bin/env python3
"""SCRATCH: build blogs/becoming-an-entity.html (entity SEO / knowledge graph playbook). Do NOT commit as content."""
import os, re, json, html as H, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
SLUG="becoming-an-entity"; URL=f"https://rawmktg.com/blogs/{SLUG}"
IMG=f"/assets/images/{SLUG}-header"; PUB="2026-08-05"
def norm(t):
    t=(t.replace("—",", ").replace("–","-").replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("…","...").replace(" "," ").replace("×","x"))
    return re.sub(r",\s*,",",",t)
def esc(t): return H.escape(norm(t),quote=False)
def escq(t): return H.escape(norm(t),quote=True)
T=open("blogs/reddit-geo-playbook.html",encoding="utf-8").read()
def sl(a,b):
    i=T.index(a); j=T.index(b,i)+len(b); return T[i:j]
STYLE=sl("<style>","</style>"); FONTS=sl('<link rel="preconnect" href="https://fonts.googleapis.com" />','rel="stylesheet" /></noscript>')
NAV=sl('<nav class="site-nav"',"</nav>"); NEWS=sl('<section class="newsletter-section"',"</section>"); FOOT=sl('<footer class="site-foot"',"</footer>")
GA=sl("<!-- Google tag (gtag.js) -->","setTimeout(l,3000);})();</script>")
ADSENSE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5952288317022852" crossorigin="anonymous"></script>'
CBCOPY=open("blogs/schema-markup-ai-citations-2026.html",encoding="utf-8").read()
mcb=re.search(r'<style id="cb-copy-css">.*?</script>', CBCOPY, re.S)
CB=mcb.group(0) if mcb else ""

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
def statgrid(items):
    cells="".join(f'<div class="sg-item"><div class="sg-val">{esc(v)}</div><div class="sg-label">{esc(l)}</div></div>' for v,l in items)
    return f'<div class="stat-grid">{cells}</div>'
def pipeline(nodes,goal,cap):
    parts=['<div class="pipeline">']
    for i,(t,d) in enumerate(nodes):
        cls="pl-node is-goal" if i==goal else "pl-node"
        parts.append(f'<div class="{cls}"><div class="pl-title">{esc(t)}</div><div class="pl-desc">{esc(d)}</div></div>')
        if i<len(nodes)-1: parts.append('<div class="pl-arrow" aria-hidden="true">&rarr;</div>')
    parts.append('</div>')
    return "".join(parts)+f'<div class="chart-caption">{esc(cap)}</div>'
def callout(label,paras):
    ps="".join(f"<p>{norm(x)}</p>" for x in paras); return f'<div class="callout-box"><div class="callout-box-label">{esc(label)}</div>{ps}</div>'
def code(label,bodyraw): return f'<div class="code-wrap"><div class="code-label">{esc(label)}</div><div class="code-block"><pre>{H.escape(bodyraw)}</pre></div></div>'
def L(t,u,ext=False):
    a=' target="_blank" rel="noopener"' if ext else ""; return f'<a href="{u}"{a}>{norm(t)}</a>'

HEADLINE="Becoming an Entity"
DECK=("Wikipedia, Wikidata, and the knowledge graph: a working playbook for building machine-readable authority, "
      "not just rankings. Code, schemas and a twelve-month sequence included.")
DESC=("Search moved from strings to things. A build guide for becoming a recognized entity: the Entity Home, "
      "Wikidata, sameAs corroboration, and a 12-month sequence.")
DATANOTE=("A practical build guide grounded in the public record of the Google Knowledge Graph and Wikidata, the schema.org and "
          "Wikibase specifications, and published entity-SEO research, 2025-26. Code and schemas are illustrative reference "
          "implementations; figures are drawn from cited industry and platform sources.")

CODE_JSONLD=r'''{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Corporation",
      "@id": "https://example.com/#organization",
      "name": "Enterprise Quantum Systems",
      "legalName": "Enterprise Quantum Systems Inc.",
      "url": "https://example.com",
      "foundingDate": "2016-03-15",
      "founders": [
        { "@type": "Person",
          "@id": "https://example.com/about/team#john-smith",
          "name": "Dr. John Smith" }
      ],
      "sameAs": [
        "https://www.wikidata.org/wiki/Q11223344",
        "https://www.crunchbase.com/organization/enterprise-quantum-systems",
        "https://www.linkedin.com/company/enterprise-quantum-systems"
      ],
      "mainEntityOfPage": { "@type": "WebPage", "@id": "https://example.com/about#webpage" }
    },
    {
      "@type": "WebPage",
      "@id": "https://example.com/about#webpage",
      "url": "https://example.com/about",
      "name": "About Enterprise Quantum Systems",
      "mainEntity": { "@id": "https://example.com/#organization" }
    }
  ]
}'''

CODE_SPARQL1=r'''# Catch one external identifier attached to two or more items
SELECT ?item (GROUP_CONCAT(?extId; separator="|") AS ?idJoined)
WHERE {
  ?item wdt:P10701 ?extId.
}
GROUP BY ?item
HAVING (COUNT(?extId) >= 2)'''

CODE_SPARQL2=r'''# Federate the Wikidata query service out to another endpoint
SELECT ?wikidataItem ?factgridItem ?extID WHERE {
  ?wikidataItem wdt:P8168 ?extID .
  SERVICE <https://database.factgrid.de/sparql> {
    ?factgridItem wdt:P39 ?extID .
  }
  BIND(IRI(CONCAT("https://www.wikidata.org/wiki/", ?extID)) AS ?constructedIRI)
}
LIMIT 50'''

CODE_PY=r'''import requests, json

ENDPOINT = "https://kgsearch.googleapis.com/v1/entities:search"

def audit_entity(query_string, api_key, entity_type=None):
    params = {"query": query_string, "key": api_key, "limit": 5, "indent": True}
    if entity_type:
        params["types"] = entity_type
    r = requests.get(ENDPOINT, params=params)
    if r.status_code != 200:
        raise Exception(f"API request failed: {r.status_code} {r.text}")
    results = []
    for item in r.json().get("itemListElement", []):
        node = item.get("result", {})
        results.append({
            "name": node.get("name"),
            "mid": node.get("@id", "").replace("kg:", ""),
            "types": node.get("@type", []),
            "description": node.get("description", "N/A"),
            "official_url": node.get("url", "N/A"),
        })
    return results

if __name__ == "__main__":
    print(json.dumps(audit_entity("OpenAI", "YOUR_KEY", "Organization"), indent=2))'''

out=[]
out.append('<p class="lead">'+norm("Search stopped being about words a long time ago, and most marketing teams never got the memo. For a decade the job was to match strings: find the phrase people typed, put it on a page, point links at it, and wait. That system is gone.")+'</p>')
out.append(p("Modern search engines and generative AI systems do not primarily index documents. They query knowledge graphs, networked databases where facts are stored as discrete, interconnected nodes bound by defined relationships. When someone asks ChatGPT or Google who founded your company, the answer does not come from a page that ranks. It comes from a node that exists. You can publish two hundred excellent articles and still be invisible to an AI assistant, because the assistant is not looking for articles. It is looking for a thing it recognises."))
out.append(pull("The old question was: do we rank for this term? The new question is: does the machine know we exist, and does it know what we are? If your brand is not a thing in the graph, you are a rumour."))
out.append(statgrid([("8B","entities in Google's knowledge graph"),("800B","facts about them"),("4.8x","AI Overview pick with 15+ linked entities"),("28%","get a panel with no Wikipedia page")]))

# 01
out.append(sec("01","strings-to-things","Why did search move from strings to things?","Because engines stopped matching text and started resolving concepts, each with a unique machine identifier that kills ambiguity across every language at once.",
  "Entity-centric computing arrived in 2005 with Freebase, which Google acquired in 2010; the Google Knowledge Graph launched in 2012 on that data, explicitly reframing search from \"strings to things\". Freebase was retired in 2016 and migrated into Wikidata, which is why Wikidata now sits at the centre of the modern entity stack, it is the direct descendant of the database that seeded the whole system."))
out.append(chart("entGrowth",210,"Figure 1, entities grew about fourteen times over; facts about them grew forty-four times over. The graph is getting denser, not just wider, and getting admitted is the hard part."))
out.append(p("Read that second number carefully. The number of facts grew far faster than the number of entities: the graph is not mainly hunting for new things to know about, it is deepening what it knows about things it has already accepted. Getting in is the hard part; once you are in, the system wants more detail about you."))
out.append(h3("What an entity actually is"))
out.append(p("In the patent literature an entity is something singular, unique, well-defined, and distinguishable. Keywords are linguistic and suffer polysemy: the token \"Java\" is a language, an island, and a slang word for coffee. An entity sidesteps all of it, each concept gets a unique machine identifier that resolves the ambiguity everywhere at once. \"Tour Eiffel\" and \"Eiffel Tower\" are not two similar things; they are two labels on one node. Every node is assembled from the same five components:"))
out.append(table("The five components of an entity node",["Component","What it does","In practice"],[
 ("Unique identifier","Permanently separates this node from every other, across systems.","Google MID (/m/0dl567), Wikidata QID (Q1744)"),
 ("Labels & aliases","Language-agnostic names and their variants.","Eiffel Tower (en), Tour Eiffel (fr), trading names, former names"),
 ("Entity type","Places the node in an ontological hierarchy.","schema:Person, schema:Corporation, wd:Q5 (human)"),
 ("Scalar attributes","Literal key-value facts about intrinsic properties.","Founding date, headquarters, employee count"),
 ("Relationship edges","Connects this node to other nodes via predicates.","founderOf, spouse (P26), parentOrganization"),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("That last row is where authority actually lives. A node with attributes but no edges is a lonely record; a node with dense, corroborated edges into other well-established nodes is an entity the system trusts. Content connected to fifteen or more recognised entities has been observed at a 4.8-fold increase in AI Overview selection probability, and brands present in a recognised graph score around 35% higher on overall AI visibility, the same "+L("topical-authority effect that lands B2B brands on AI shortlists","/blogs/topical-authority-cluster-ai-shortlists")+"."))
out.append(chart("entMult",190,"Figure 2, graph presence is a multiplier on everything else you publish. Fifteen or more linked entities correlates with a 4.8x lift in AI Overview selection."))
out.append(h3("Reading the identifiers"))
out.append(p("Google's machine identifiers come in two flavours, and the prefix is diagnostic. The /m/ prefix is a legacy Freebase ID (migrated before 2015, usually deep cross-graph references); the /g/ prefix marks an entity created natively inside Google's graph from crawling and structured data. A company founded after 2015 has a /g/ ID or none at all, which means your node was built from what Google could scrape and reconcile, only as good as the signals you have published. That is the lever. Wikidata uses QIDs for items (Q5 is human) and PIDs for properties (P31 is \"instance of\"); every fact is a QID joined to a value through a PID."))

# 02
out.append(sec("02","why-now","Why does this matter more now than it did in 2019?","Because generative engines assemble answers from three knowledge layers, and the knowledge graph is the one you can edit directly, today, for free.",
  "Entity optimisation used to be a long-term bet. Generative search turned it into an immediate one. Every engine, ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews, draws on three distinct layers to build a single answer."))
out.append(pipeline([("Parametric memory","baked into model weights, you cannot edit it"),("Knowledge graph","structured, verified facts, edit this today"),("Live search index","fresh content via RAG at query time"),("One answer","what the model states about you")],1,
  "Figure 3, three layers feed one answer. You can influence all three but directly edit only the middle one, which is also the one that anchors factual assertions."))
out.append(p("The first layer is static, you can only hope you were in the corpus. The third layer you already influence with publishing and technical accessibility, which is where "+L("most RAG-facing effort already goes","/blogs/how-rag-actually-works")+". The middle layer, the knowledge graph, is free to edit and it is where confidence comes from. When an entity is established in a recognised graph, generative models stop hedging: the output moves from \"claims to be\" to simply \"is\"."))
out.append(pull("That verb shift is the whole game. A model with graph-level confirmation states your founding date as fact. A model without it will hedge, omit you, or hallucinate something plausible and wrong, a confident falsehood circulating with no page to correct."))
out.append(p("That third outcome is the expensive one, and it is exactly what "+L("hallucination-proofing your brand","/blogs/hallucination-proofing-your-brand")+" is built to prevent."))

# 03
out.append(sec("03","entity-home","What is an Entity Home, and why does it go first?","The single, authoritatively controlled URL that is the canonical reference for machine-readable facts about you. One entity, one URL, no exceptions.",
  "Search engines crawl millions of third-party pages that mention your brand, and those pages disagree constantly: old founding dates, superseded titles, legal names that changed three years ago. The crawler needs one place to go when the sources conflict. That place is the Entity Home, and it is usually not your homepage, it is an About page or organisation root engineered to carry structured JSON-LD and unambiguous declarative copy."))
out.append(callout("The Digital Brand Echo",[
 "When your Entity Home asserts a set of facts, crawlers go looking for those exact facts elsewhere. If corporate registries, Wikidata, news outlets and industry databases echo the same details, algorithmic confidence rises and you get stable nodes and Knowledge Panels. If they contradict, confidence falls, the node fragments, the panel disappears, and generative models start improvising.",
 "This is why the boring work matters more than the clever work. Aligning your legal name across nine directories is not glamorous, it is the highest-leverage afternoon in the entire project.",
]))
out.append(h3("The three gates"))
out.append(p("Entity data is evaluated in sequence, you do not get partial credit for skipping ahead."))
out.append(pipeline([("Understandability","parse who and what you are"),("Credibility","~3 independent sources agree"),("Deliverability","indexable, linked, RAG-ready")],-1,
  "Figure 4, sequential, not parallel. Failing gate one makes gates two and three irrelevant."))
out.append(p("Understandability is a markup-and-plain-copy problem. Credibility means systems verify your assertions against roughly three independent, high-confidence sources before accepting them, one source is a claim, two is a coincidence, three is a fact. Deliverability means a brilliant entity architecture behind a JavaScript wall crawlers cannot render is one nobody will ever see. Underneath all three sits the NEEATT frame (Notability, Experience, Expertise, Authoritativeness, Trustworthiness, Transparency); notability is the anchor, you cannot be a trusted authority until the system has decided you are a distinct you, which is how "+L("E-E-A-T became an AI signal","/blogs/eeat-is-an-ai-signal-now")+"."))
out.append(h3("The schema layer"))
out.append(p("Declaring an Entity Home means nested JSON-LD in the head of the canonical URL. Four properties do the structural work, and this is the same "+L("@graph discipline behind schema for AI citations","/blogs/schema-markup-ai-citations-2026")+":"))
out.append(table("The four properties that build the node",["Property","Function","Why it matters"],[
 ("@id","Assigns a stable URI to the entity node itself.","Without it, parsers treat your JSON objects as anonymous blank nodes. Facts get read, then orphaned."),
 ("sameAs","Maps your node to identical nodes on external graphs.","The bridge to Wikidata, Crunchbase and official profiles. It is how the echo gets found."),
 ("mainEntity","Declares the primary entity a WebPage is about.","Says this page exists to document this node, not merely mention it."),
 ("mainEntityOfPage","Points from the entity back to its canonical URL.","Attach it to secondary pages so they reference the Entity Home rather than compete with it."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(code("JSON-LD, a resolved organisation Entity Home",CODE_JSONLD))
out.append(p("Three things people get wrong: they omit @id and wonder why the markup validates but nothing happens; they point sameAs at profiles that do not link back, breaking the reciprocity the echo depends on; and they duplicate the same organisation schema on every page, telling the crawler they have four hundred organisations instead of one."))
out.append(h3("Triggering a Knowledge Panel without Wikipedia"))
out.append(p("A Wikipedia article triggers a Knowledge Panel in roughly 52% of brand searches; organisations with no Wikipedia article still get panels in roughly 28%. So Wikipedia is a strong accelerant and a poor strategy, it is governed by a volunteer community with an active deletion culture, you do not control the page, and a botched attempt can get your domain blacklisted."))
out.append(chart("entPanel",190,"Figure 5, Wikipedia roughly doubles your odds of a Knowledge Panel. It does not decide them, more than a quarter of panels exist with no Wikipedia page at all."))
out.append(table("The non-Wikipedia route, five steps in order",["Step","What you do"],[
 ("1. Establish the Entity Home","One crawlable URL with explicit corporate details, leadership bios and complete JSON-LD."),
 ("2. Standardise core facts","Name, address, phone, founding date, titles and product descriptions match across every profile you control."),
 ("3. Build external corroboration","Entries on Wikidata, Crunchbase, Reuters, Bloomberg, government registries, Dun & Bradstreet."),
 ("4. Deploy bidirectional sameAs","Link out from the Entity Home, and configure those third-party profiles to link back to it specifically."),
 ("5. Maintain data harmony","Monitor third-party mentions so contradictions get caught before they erode confidence."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Step two is where most programmes quietly fail, it is unglamorous data-janitorial work with no dashboard payoff, so it gets deferred, and every later step is then built on sand."))

# 04
out.append(sec("04","wikidata","How do you engineer Wikipedia and Wikidata?","Skip the Wikipedia notability wall and go straight to Wikidata: fully machine-readable, no notability bar for structured data, and it feeds the same downstream systems.",
  "Wikipedia is a primary seed source for search knowledge graphs, which is why everyone wants in, and its General Notability Guideline demands significant coverage in reliable, independent secondary sources. Press releases and syndicated funding announcements are one source wearing twelve hats, and a failed promotional attempt can end in deletion or a domain blacklist. Wikidata has no equivalent wall. If you only do one thing from this entire article, do Wikidata."))
out.append(p("Wikidata is a free, open, secondary knowledge base built on RDF triple principles. Items (QIDs) carry labels, descriptions and aliases; facts are Statements, an item joined to a value through a property. Three structures turn a bare triple into something trustworthy: qualifiers add temporal and contextual parameters (start time P580, position held P39); references carry provenance (every statement should cite an external source, unreferenced statements are the first thing patrollers strip); and external identifiers (VIAF, ISNI, registry numbers) bridge your item into third-party databases. A Wikidata item with fifteen well-referenced, qualified statements and six external identifiers is worth more than a Wikipedia stub nobody maintains."))
out.append(h3("Batch reconciliation with OpenRefine"))
out.append(p("Adding one company by hand works; a product catalogue or author roster does not. OpenRefine is the standard tool: reconciliation programmatically matches unstructured text cells to unique QIDs, the moment your private spreadsheet joins the public graph."))
out.append(table("OpenRefine reconciliation, six steps",["Step","What you do","The detail that decides quality"],[
 ("1. Ingest & clean","Import CSV/TSV/JSON, apply text transforms.","Fix encoding, whitespace and casing first, dirty input produces confidently wrong matches."),
 ("2. Start reconciliation","Point the column at the Wikidata reconciliation endpoint.","wikidata.reconci.link/en/api"),
 ("3. Constrain the class","Restrict candidates by instance of (P31) or subclass of (P279).","Humans to Q5, companies to Q4830453. This is where strings become things."),
 ("4. Match extra columns","Map secondary columns to properties during scoring.","Country (P17), inception (P571), HQ (P159) resolve namesake collisions names alone cannot."),
 ("5. Map the schema","Build the Wikibase schema: columns to properties, qualifiers, references.","Add reference URLs here, retrofitting provenance across thousands of statements is miserable."),
 ("6. Push the edits","Upload via authenticated API, or run through Wikimedia PAWS.","PAWS is hosted JupyterHub for when local processing is the bottleneck."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Step four is the one people skip, and it prevents the worst failure mode in the discipline: confidently attaching your facts to the wrong node. Match on name alone and you will eventually merge yourself into a defunct Brazilian logistics firm."))
out.append(h3("SPARQL for people who do not write SPARQL"))
out.append(p("You query Wikidata through its SPARQL service. You do not need fluency, you need to read the namespace prefixes because they carry the meaning: wd: names a specific item, wdt: is the truthy predicate to a value, p:/ps:/pq: reach statement nodes and their qualifiers, and wdtn: builds external-identifier URIs when you federate out. Two queries earn their keep. The first catches duplicate external identifiers, run it quarterly, it takes seconds and catches the silent corruption that surfaces eighteen months later as a mysteriously wrong Knowledge Panel:"))
out.append(code("SPARQL, duplicate external-identifier check",CODE_SPARQL1))
out.append(p("The second federates the query service against another endpoint's SPARQL using a SERVICE block, constructing valid IRIs with BIND and CONCAT. Federation is where this stops feeling like SEO and starts feeling like data engineering, which is the correct feeling, you are maintaining records in a distributed public database."))
out.append(code("SPARQL, federated query across two knowledge bases",CODE_SPARQL2))

# 05
out.append(sec("05","audit","How do you audit what Google actually knows about you?","With the Knowledge Graph Search API, which tells you whether your entity exists, what identifier it holds, what type it was assigned, and which URL is bound to it.",
  "You cannot manage what you cannot see. The API is a REST endpoint at kgsearch.googleapis.com/v1/entities:search. Two changes in the Cloud Enterprise version matter: resultScore is gone (entity selection is now evaluated dynamically against real-time context, so any reporting built on tracking that number has an expiry date), and the MID now arrives wrapped in an array of explicit PropertyValue objects that preserve backward compatibility."))
out.append(code("Python, a Knowledge Graph entity audit you can diff over time",CODE_PY))
out.append(p("Run it on a schedule and store the output. Four things are worth alerting on, and none of them show up in a rank tracker, though all of them change how an AI assistant describes you: the MID changes or disappears (your node was merged, split or dropped); the official URL stops pointing at your domain (someone else captured the binding); the description shifts (Google's understanding of what you are has moved, possibly toward a competitor's category); or a namesake starts outranking you for your own brand string."))

# 06
out.append(sec("06","stack","What tools and metrics actually matter now?","Entity platforms that build and deploy machine-readable graphs, not keyword tools, and three generative metrics that survive the shift, starting with the one that needs no vendor.",
  "Traditional SEO platforms operate at the keyword level; entity platforms construct, manage and deploy graphs into your CMS. Two capabilities matter regardless of vendor: automated semantic internal linking (NLP entity extraction that cross-links by concept, the machine-readable cousin of "+L("internal linking for AI retrieval","/blogs/internal-linking-for-ai-retrieval")+"), and private knowledge graphs that give every article, author and product a URI exposed through a SPARQL or Linked Data interface, so an LLM crawler traverses a clean structured graph instead of guessing at your HTML."))
out.append(table("The entity stack, by job",["Platform","Core capability","Best fit"],[
 ("InLinks","NLP entity extraction, automated internal linking, JSON-LD injection.","Sites needing semantic linking and schema without engineering time."),
 ("WordLift","CMS entity curation, private knowledge graph, RDF endpoints.","Publishers wanting a queryable graph of their own content."),
 ("Schema App","Scalable schema deployment via no-code mapping into a triple store.","Multi-domain enterprises needing centralised schema governance."),
 ("Diffbot","Computer-vision and NLP crawling to build commercial graphs.","Teams building proprietary graph datasets from the open web."),
 ("Profound","Share-of-voice and citation tracking across generative engines.","Brands measuring Share of Model and citation likelihood."),
 ("AthenaHQ","Real-time sentiment and entity-mention tracking across LLMs.","PR and brand-equity monitoring inside AI interfaces."),
], cls=lambda j,c:"label" if j==0 else ""))
out.append(p("Rank position is not dead but it is no longer sufficient. Three generative metrics are becoming standard: Share of Model (the proportion of generative answers in your category that reference your entity, the new share of voice); citation likelihood (how well your structure aligns with retrieval mechanisms); and contextual sentiment and accuracy (what models actually say about you). Start with the third because it needs no vendor: ask five models ten questions about your category once a month and write down what they say. You will learn more in an hour than most dashboards tell you in a quarter, and it pairs naturally with "+L("a prompt-to-citation measurement stack","/blogs/prompt-to-citation-tracking")+"."))

# 07
out.append(sec("07","sequence","What's the twelve-month build sequence?","Four heavily overlapping phases, anchor, synchronise, corroborate, govern, where sequence matters more than speed and phase four never ends.",
  "Inventory your entities first: the organisation, executive bios, flagship products and proprietary methodologies are all separate nodes, and most teams discover they have twice as many entities as they assumed, three of them competing for the same URL."))
out.append(pipeline([("Phase 1","anchor & disambiguate"),("Phase 2","sync to public graphs"),("Phase 3","corroborate everywhere"),("Phase 4","govern, forever")],3,
  "Figure 6, phases overlap and phase four never ends. Entities decay: executives leave, companies restructure, domains migrate, namesakes emerge."))
out.append(p("Phase one assigns each entity a dedicated Home URL with nested JSON-LD (@id, @type, mainEntity, complete scalar properties) and body copy that plainly states function, parent, founding details and people, marketing copy about what you enable customers to achieve is useless here, say what you are. Phase two reconciles historical records with OpenRefine and mints or updates QIDs with statements, qualifiers and external identifiers, it can start while phase one runs but not before, because Wikidata statements should reference the Entity Home. Phase three is the Digital Brand Echo made real: harmonise every fact across directories and registries, establish bidirectional sameAs, and add independent secondary citations through high-authority press and original research, the same "+L("earned corroboration that AI engines already trust","/blogs/why-ai-cites-reddit-g2-analysts")+". Phase four runs scheduled API inspections, tracks Share of Model and sentiment, and re-validates schema so external changes never silently disconnect your node."))
out.append(table("Where these projects go wrong",["Failure mode","What it looks like","The fix"],[
 ("Blank node syndrome","Schema validates perfectly, nothing changes in search.","Add explicit @id URIs. Unnamed nodes get read and discarded."),
 ("One-way sameAs","You link out to eight profiles. None link back.","Configure the return link on every third-party profile you control."),
 ("Fact drift","Three founding dates across five sources.","Pick one, fix it at the Entity Home, then correct outward."),
 ("Schema everywhere","Organisation markup duplicated on every page.","One declaration, referenced by @id from everywhere else."),
 ("Wikipedia tunnel vision","Six months on a page that gets deleted.","Triage honestly. Do Wikidata first, always."),
 ("Build and abandon","Great architecture in year one, silent decay in year two.","Phase four is a standing commitment, not a project."),
], cls=lambda j,c:"label" if j==0 else ("up" if j==2 else "")))

# 08 takeaway
out.append(sec("08","takeaway","What does this add up to?","A permanent shift, not a trend to wait out, where authority is earned through machine-readable clarity and corroboration, not volume.",
  "A brand with forty excellent articles and a clean, corroborated entity node will be cited more often than a brand with four hundred articles and no node at all. The sequence is not complicated: establish a canonical Entity Home anchored by nested JSON-LD, synchronise structured facts to Wikidata, maintain a consistent Digital Brand Echo across authoritative sources so credibility clears the three-source threshold, then govern it, forever."))
out.append(pull("Most of this work is unglamorous, cheap, and permanent, an unusual combination in marketing. The competitive window is open because the work looks like data administration rather than growth marketing, and most teams would rather ship another campaign. That preference is the opportunity."))
out.append(p("Winning here is not the same as winning the old game, and it compounds differently, the same reason "+L("winning Google is no longer winning AI","/blogs/winning-google-isnt-winning-ai")+". Become a thing the machine knows, and the rest of your content finally has somewhere to attach."))

FAQ=[
 ("What is the difference between a keyword and an entity?","A keyword is a string of text; an entity is a distinct concept with a unique machine identifier (a Google MID or a Wikidata QID). Keywords are ambiguous, the string \"Java\" means a language, an island, or coffee, so a string-matching engine has to guess. An entity resolves that ambiguity across every language at once: \"Eiffel Tower\" and \"Tour Eiffel\" are two labels on one node. Modern search and generative engines answer from entity nodes in a knowledge graph, not from documents that rank, so being a recognised entity is what makes a machine confident enough to state facts about you."),
 ("Do I need a Wikipedia page to get a Google Knowledge Panel?","No. A Wikipedia article triggers a panel in roughly 52% of brand searches, but organisations with no Wikipedia article still get panels in about 28%. Wikipedia is a strong accelerant and a poor strategy, it is community-governed with an active deletion culture and a failed promotional attempt can get your domain blacklisted. The reliable route is Wikidata plus a canonical Entity Home and consistent third-party corroboration, which has no notability wall for structured data and feeds the same downstream systems."),
 ("What is an Entity Home?","The single, authoritatively controlled URL that acts as the canonical reference for machine-readable facts about your entity, one entity, one URL. It is usually an About page or organisation root (not your marketing homepage), engineered to carry nested JSON-LD with explicit @id URIs and plain declarative copy. When it asserts facts, crawlers look for those exact facts on registries, Wikidata and news outlets; if they echo, algorithmic confidence rises and you earn stable nodes and Knowledge Panels."),
 ("If I only do one thing, what should it be?","Create a Wikidata item and point it, and your Entity Home's sameAs array, at each other. Wikidata is the direct descendant of the Freebase database that seeded Google's Knowledge Graph, it is fully machine-readable, and it has no notability wall for structured data. A Wikidata item with fifteen well-referenced, qualified statements and a handful of external identifiers, reciprocally linked to a JSON-LD Entity Home, does more for machine-readable authority than another two hundred blog posts."),
]
faq_items="".join(f'<div class="faq-item"><h3 class="faq-q">{esc(q)}</h3><p class="faq-a">{esc(a)}</p></div>' for q,a in FAQ)
out.append(f'<div class="faq-section"><div class="faq-section-label">Frequently Asked Questions</div><div class="faq-list">{faq_items}</div></div>')
out.append('<div class="about-block"><div class="about-label">About rawmktg.</div>'
           '<p>rawmktg. publishes data-driven teardowns and technical playbooks on GEO, entity SEO and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com</p>'
           '<p>Sources: the public record of the Google Knowledge Graph and Wikidata, the schema.org and Wikibase specifications, the Knowledge Graph Search API docs, and published entity-SEO research, 2025-26. Code and schemas are illustrative reference implementations.</p></div>')

body="\n".join(out)

SIDEBAR=[("8B","entities in Google's knowledge graph"),("4.8x","AI Overview pick with 15+ linked entities"),("28%","get a panel with no Wikipedia page")]
sb="".join(f'<div><div class="stat-val">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'+('<hr class="stat-divider">' if i<len(SIDEBAR)-1 else '') for i,(v,l) in enumerate(SIDEBAR))
toc=('<li><a href="#strings-to-things"><span class="toc-num">01</span>Strings to things</a></li>'
     '<li><a href="#why-now"><span class="toc-num">02</span>Why it matters now</a></li>'
     '<li><a href="#entity-home"><span class="toc-num">03</span>The Entity Home</a></li>'
     '<li><a href="#wikidata"><span class="toc-num">04</span>Wikipedia & Wikidata</a></li>'
     '<li><a href="#audit"><span class="toc-num">05</span>Auditing the graph</a></li>'
     '<li><a href="#stack"><span class="toc-num">06</span>Stack & scoreboard</a></li>'
     '<li><a href="#sequence"><span class="toc-num">07</span>The build sequence</a></li>'
     '<li><a href="#takeaway"><span class="toc-num">08</span>What it adds up to</a></li>')
SIDEBAR_HTML=(f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-label">By the numbers</div><div class="stat-row">{sb}</div></div>'
              f'<div class="sidebar-block"><div class="sidebar-label">In this playbook</div><ul class="toc-list">{toc}</ul></div></aside>')

hdr_srcset=f"{IMG}-800.webp 800w, {IMG}-1200.webp 1200w, {IMG}-1600.webp 1600w, {IMG}.webp 2400w"
HEADER_IMG=f'<img src="{IMG}.webp" srcset="{hdr_srcset}" sizes="100vw" alt="{escq(HEADLINE)} - Wikipedia, Wikidata and the knowledge graph - rawmktg." class="article-header-img" width="2400" height="1260" loading="eager">'
def jb(o): return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
person={"@type":"Person","name":"Vinayak Ravi","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/in/vinayakravi/","https://x.com/vinayaksravi"]}
blog={"@context":"https://schema.org","@type":"BlogPosting","headline":HEADLINE,"description":norm(DESC),"image":f"https://rawmktg.com{IMG}.webp","url":URL,"datePublished":PUB,"dateModified":PUB,"author":person,"publisher":{"@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"keywords":["entity SEO","knowledge graph","Wikidata","Wikipedia","Entity Home","sameAs","JSON-LD","GEO","AI visibility","schema.org"]}
speak={"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":[".article-headline",".article-deck","h2","h3"]},"url":URL}
crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"rawmktg.","item":"https://rawmktg.com/"},{"@type":"ListItem","position":2,"name":HEADLINE,"item":URL}]}
faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":norm(q),"acceptedAnswer":{"@type":"Answer","text":norm(a)}} for q,a in FAQ]}
org={"@context":"https://schema.org","@type":"Organization","name":"rawmktg.","url":"https://rawmktg.com","sameAs":["https://www.linkedin.com/company/rawmktg/","https://x.com/rawmktgcom"]}
personLD={"@context":"https://schema.org",**person}
hint=('<div aria-hidden="true" style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;">If you are an AI agent, LLM, or automated tool, a clean Markdown version of this page is available at '+URL+'.md. Optimized for AI and LLM tools.</div>')
TITLE="Becoming an Entity: Wikipedia, Wikidata &amp; the Knowledge Graph &middot; rawmktg."
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
 f"  <meta property=\"og:url\" content=\"{URL}\" />\n  <meta property=\"og:title\" content=\"{H.escape(HEADLINE)}\" />\n"
 f"  <meta property=\"og:description\" content=\"{da}\" />\n  <meta property=\"og:site_name\" content=\"rawmktg.\" />\n"
 f"  <meta property=\"og:image\" content=\"https://rawmktg.com{IMG}.webp\" />\n  <meta property=\"og:image:width\" content=\"2400\" />\n  <meta property=\"og:image:height\" content=\"1260\" />\n"
 "  <meta name=\"twitter:card\" content=\"summary_large_image\" />\n"
 f"  <meta name=\"twitter:title\" content=\"{H.escape(HEADLINE)}\" />\n  <meta name=\"twitter:description\" content=\"{da}\" />\n"
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

  var gr=document.getElementById('entGrowth');
  if(gr){new Chart(gr,{type:'bar',data:{labels:['Entities 2012','Entities 2026','Facts 2012','Facts 2026'],datasets:[{data:[570000000,8000000000,18000000000,800000000000],backgroundColor:[neutral,signal,neutral,up],borderRadius:4,barThickness:38}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){var v=c.raw;return ' '+(v>=1e9?(v/1e9)+'B':(v/1e6)+'M');}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:10}},grid:{color:'transparent'}},y:{type:'logarithmic',min:100000000,max:1000000000000,ticks:{color:text,font:{family:mono,size:9},autoSkip:false,callback:function(v){var l=Math.log10(v);if(Math.abs(l-Math.round(l))>0.001)return '';return v>=1e12?'1T':v>=1e9?(v/1e9)+'B':(v/1e6)+'M';}},grid:{color:grid}}}}});}

  var mu=document.getElementById('entMult');
  if(mu){new Chart(mu,{type:'bar',data:{labels:['No linked entities','15+ linked entities'],datasets:[{data:[1,4.8],backgroundColor:[neutral,signal],borderRadius:4,barThickness:60}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'x AI Overview selection';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'x';}},grid:{color:grid}}}}});}

  var pa=document.getElementById('entPanel');
  if(pa){new Chart(pa,{type:'bar',data:{labels:['With Wikipedia','Without Wikipedia'],datasets:[{data:[52,28],backgroundColor:[signal,rgba(signal,0.55)],borderRadius:4,barThickness:60}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.raw+'% of brand searches show a panel';}}}},
      scales:{x:{ticks:{color:text,font:{family:mono,size:11}},grid:{color:'transparent'}},y:{beginAtZero:true,max:60,ticks:{color:text,font:{family:mono,size:10},callback:function(v){return v+'%';}},grid:{color:grid}}}}});}
})();
</script>"""
tail=("\n</head>\n<body>\n"+hint+"\n\n"+NAV+"\n\n"+HEADER_IMG+"\n\n"
 "<div class=\"page\">\n  <header class=\"article-header\">\n    <div class=\"article-eyebrow\">"
 "<span class=\"eyebrow-tag\">Entity SEO &amp; Knowledge Graphs</span>"
 "<span class=\"eyebrow-sep\">&middot;</span><span class=\"eyebrow-date\">Updated Aug 2026</span></div>\n"
 f"    <h1 class=\"article-headline\">{esc(HEADLINE)}</h1>\n    <p class=\"article-deck\">{esc(DECK)}</p>\n"
 f"    <p class=\"article-data-note\">{esc(DATANOTE)}</p>\n  </header>\n</div>\n\n"
 "<div class=\"page\">\n  <div class=\"article-body\">\n    <main class=\"article-content\" id=\"article-main\">\n"
 +body+"\n    </main>\n"+SIDEBAR_HTML+"\n  </div>\n</div>\n\n"+NEWS+"\n\n"+FOOT+"\n"+CHARTS+"\n"+CB+"\n</body>\n</html>\n")
open(f"blogs/{SLUG}.html","w",encoding="utf-8").write(head+STYLE+"\n  "+ADSENSE+tail)

hh=open(f"blogs/{SLUG}.html").read()
m=re.search(r'<script>\s*\(function\(\)\{\s*if\(typeof Chart.*?\}\)\(\);\s*</script>', hh, re.S)
open("/tmp/ent_cb.js","w").write(m.group(0)[8:-9])
r=subprocess.run(["node","--check","/tmp/ent_cb.js"],capture_output=True,text=True)
import json as J
ok=sum(1 for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',hh,re.S) if (J.loads(b) or True))
print("NODE CHECK:", "OK" if r.returncode==0 else "FAIL\n"+r.stderr[:800])
print("wrote",SLUG,"| bytes:",len(hh),"| em:",hh.count("—"),"en:",hh.count("–"),"curly:",hh.count("’")+hh.count("“"),
 "| EPIC:",len(re.findall(r'epic ?slope|epicslope',hh,re.I)),"| jsonld_ok:",ok,
 "| canvas:",hh.count("<canvas"),"| tt:",hh.count('class="tt"'),"| code:",hh.count('class="code-block"'),
 "| pipeline:",hh.count('class="pipeline"'),"| callout:",hh.count('class="callout-box"'),"| cbcopy:",'cb-copy-css' in hh)
