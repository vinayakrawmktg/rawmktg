# How Your Page Gets Retrieved

> Chunking, embeddings and the rerank funnel. Every AI engine breaks your page apart before it considers citing you, here is what happens inside, why good content loses at the boundary, and how to write pages that survive the cut.

*Source: https://rawmktg.com/blogs/how-your-page-gets-retrieved · rawmktg. by Vinayak Ravi*


Here is the uncomfortable part. When an AI assistant answers a question and cites a source, no model read your page, not the way a person does, not top to bottom. Your page was pulled apart into passages, each converted into a list of numbers and stored in an index. The question became numbers too, and the system went looking for the closest match.

The unit that competed was never your page. It was a fragment of it, maybe three hundred words long, sitting alone in a database with no title, no navigation, and no memory of the paragraph above it. Teams still write for the page, measure at the page level, and audit at the page level, meanwhile the thing being judged is a passage they never saw in isolation.

Your page is the container. The chunk is the competitor.

This piece walks the whole pipeline, because the shape of the machine determines the shape of the content that wins inside it. Once you can see where passages get cut, where meaning leaks out, and where the ranking actually happens, a lot of vague advice about "writing for AI" collapses into something specific, the mechanical layer beneath [how RAG actually works](/blogs/how-rag-actually-works).

200-800

tokens per indexed passage

1536

embedding dimensions, any input length

80/20

dense-to-sparse fusion, k=60

5-20

chunks survive from ~150 candidates

## 01. Why does your page get cut up at all?

**Because a fixed-size vector cannot hold a whole page without dissolving its details, so systems split first, then encode each passage on its own budget.** An embedding model takes text of any length and returns a fixed-length list of numbers, usually 384 to 1536 of them. A tweet gets 1536 numbers; a 4,000-word guide gets 1536 numbers. The model has a fixed budget of expressive capacity and must spend it across everything in the text.

Feed it one tight paragraph about pricing tiers and the vector strongly encodes pricing tiers. Feed it your entire product page and the vector encodes something like "general B2B software marketing page", with the pricing detail smeared into near-invisibility. That is not a bug, it is the arithmetic of compression: specific numbers, named entities and precise claims lose signal strength relative to the dominant topic of the document. Chunking is the fix, split the document into smaller passages before encoding and each passage gets its own full budget.

But cutting costs you something too

Go too far the other way and you break the thing that made the text useful. Chop a document into hyper-granular fragments and you destroy the macro narrative, leaving isolated statements stripped of the detail that gave them meaning. Every retrieval system sits somewhere on this trade-off, and where it sits determines what it can find. Most production systems land between 200 and 800 tokens per chunk, roughly 150 to 600 words.

## 02. What are the four ways your page gets cut?

**Fixed-size windows, sentence/paragraph boundaries, semantic-distance boundaries, and structural header parsing, and only the last one follows your intent.** The algorithm that decides where the cuts fall determines the entire shape of the index built from your content, and the four approaches are not equally kind to well-structured writing.

Boundary strategies compared, and what each does to your writing

| Strategy | How it cuts | What it buys | What it breaks |
| --- | --- | --- | --- |
| Fixed-size sliding window | Static token count with a fixed stride overlap. | Almost no compute cost; predictable memory. | Bisects named entities, formulas and logical propositions. |
| Sentence / paragraph | Punctuation and newline delimiters. | Preserves local syntax and clause structure. | Variable lengths create unstable embedding density. |
| Semantic distance | Cuts where cosine similarity drops between adjacent sentences. | Boundaries land on genuine topic shifts. | High ingestion latency, a forward pass per sentence. |
| Structural headers | Markdown headers and HTML DOM nodes. | Preserves the organisation you actually intended. | Collapses on inconsistent or malformed markup. |

What this changes about how you write

You cannot control which algorithm indexes you, and different assistants use different ones. What you can control is making your content survive all four: real heading tags, semantically complete sections, and topic shifts that align with structural breaks give every parser the same answer, which is also why [clean internal structure decides retrieval](/blogs/internal-linking-for-ai-retrieval).

## 03. What is context rupture, and why does good content fail?

**Because standard pipelines encode each chunk alone, a passage that never names its own subject drifts out of range of the query it should answer, even when the fact is correctly indexed.** This is the single most important mechanic in the article, and it explains why genuinely excellent content sometimes gets no AI visibility at all. Passages lean heavily on the document around them; isolate a segment and anaphoric references lose their target nouns.

A concrete example, two adjacent chunks

Chunk A: "ACME Corporation expanded its robotics division in Q3."

Chunk B: "The division achieved a 14% revenue increase over the prior fiscal year."

Chunk B has the answer, the number, the growth rate. And it will not be retrieved. Nothing in it says ACME, robotics, or Q3. Embedded on its own, its vector is positioned entirely on its isolated text, so the query "ACME Corporation Q3 financial performance" lands somewhere else and Chunk B falls outside the nearest-neighbour radius. The fact exists, it is correctly indexed, and it cannot be found.

Most content does not fail because it is thin. It fails because its best paragraphs cannot say what they are about.

Now audit your own writing: pronouns carrying the subject across paragraphs, section three referring to "this approach" from section two, a case study where the client name appears once in the intro and never again, comparison tables where product names live in the header row and the rows say "it" and "the platform". All of that is fine for a human reader. All of it produces orphaned chunks, the same failure that makes [AI misdescribe a brand it can't cleanly resolve](/blogs/hallucination-proofing-your-brand).

## 04. How do retrieval systems patch the problem?

**Two ways: generative contextualisation prepends a written summary to each chunk before indexing; late chunking runs the whole document through the encoder first and slices after. Together they cut retrieval failures by up to 67%.** Engineers noticed the failure and built two very different fixes, and understanding both tells you what the systems reward.

### Fix one: generative contextual augmentation

Before embedding a chunk, send it to a language model with the full parent document and ask for a short prefix explaining what the chunk is about, then glue that prefix on and index the combined text. A chunk reading "Operating margins expanded by 240 basis points" becomes "This chunk is from the Q2 2023 financial statement for ACME Corporation... Operating margins expanded by 240 basis points". The rewritten passage resolves the pronouns, names the entity, anchors the timeframe, and the explicit terms become searchable in the keyword index too. This is [Anthropic's contextual retrieval](https://www.anthropic.com/engineering/contextual-retrieval).

The prompt that writes the context prefix

```
<document>
{{WHOLE_DOCUMENT_TEXT}}
</document>

<chunk>
{{TARGET_CHUNK_TEXT}}
</chunk>

Please give a succinct context (50-100 tokens) to situate this
chunk within the overall document, to improve search retrieval.
Answer only with the contextual prefix and nothing else.
```

The measured gains are not marginal. On standard evaluation sets, contextual prefixes on dense embeddings cut top-20 retrieval failure by 35% against a naive pipeline; pair them with contextual keyword search and failures drop 49%; add a reranking stage and the reduction reaches 67%. The whole funnel runs once per sub-query produced by [query fan-out](/blogs/query-fan-out-how-one-prompt-becomes-ten-searches).

Figure 1, retrieval failure reduction across the stack. Each layer targets a different cause, which is why the gains compound instead of overlapping. Source: Anthropic contextual retrieval.

Read those numbers as a diagnosis, not a benchmark: two thirds of retrieval failures in a naive system are caused by problems that have nothing to do with content quality, context loss, vocabulary mismatch, and bad ranking. All three have content-side counterparts. And it is cheap: key-value prompt caching gives cache reads a ~90% token discount, so ingestion lands near $1 per million document tokens, which means you should assume the systems reading your content already do this and are already compensating for some of your ambiguity. Some, not all.

### Fix two: late chunking

The more elegant approach reverses the order of operations. Traditional pipelines split first and encode second, so attention only ever sees one isolated chunk. [Late chunking](https://jina.ai/news/late-chunking-in-long-context-embedding-models/) feeds the entire document through a long-context encoder in one pass, so every token vector already encodes global context, and only then applies chunk boundaries, pooling across the token slice. It preserves cross-chunk dependencies and document-level context without changing the vector's dimensions, and adds no query-time cost.

The two fixes compared, same problem, different mechanisms

| Axis | Generative contextualisation | Late chunking |
| --- | --- | --- |
| Depends on | An external LLM API or local generative model. | A long-context transformer embedder (8k+ tokens). |
| Ingestion speed | Slower, bound by token generation. | Fast, one encoder pass per document. |
| Effect on keyword search | Large, adds real searchable words to the sparse index. | None, the underlying text is untouched. |
| How context is stored | Explicitly, as text prepended to the passage. | Implicitly, inside the attention layers. |
| Operational complexity | Higher, needs caching, orchestration, retries. | Lower, needs slice-based pooling support. |

The content implication

Late chunking recovers context that exists in your document. It cannot invent context that was never written down. If your page never states the entity, the timeframe, or the qualifier anywhere in the surrounding text, no amount of attention across the document will surface it. Explicit beats implicit, every time.

## 05. What happens inside the vector space?

**Text becomes points in a continuous space; closeness is measured by cosine angle; and the first filter judges only coarse topical signal, so a passage that takes four sentences to reveal its subject may never reach the stage where its detail counts.** Cosine similarity measures the angle between two vectors and ignores magnitude, which stops passage length from distorting relevance, that is the standard for text. Dot product and Euclidean distance are the alternatives, and at the dense stage your chunk either scores in the top handful or it does not exist.

What dense retrieval computes, in essence

```
# What dense retrieval actually computes, stripped to essentials
import numpy as np

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query  = embed("how long does onboarding take")
chunks = [embed(c) for c in page_chunks]

scores  = [cosine(query, c) for c in chunks]
ranking = np.argsort(scores)[::-1]

# Only the top handful ever reach the model.
top_k = [page_chunks[i] for i in ranking[:5]]
```

Two refinements matter for content. Matryoshka embeddings nest meaning hierarchically, coarse topic in the leading dimensions, fine detail later, which enables a cheap first pass on a 64-dimensional prefix before rescoring the shortlist on full vectors. The blunt consequence: the first filter your chunk faces is deliberately coarse, judging on broad topical signal alone, so passages whose topic is unmistakable in the opening lines pass it. And multi-vector models like [ColBERT keep token-level vectors and score with MaxSim](/blogs/internal-linking-for-ai-retrieval), which rewards passages containing the literal terminology of the question, not just its general vibe. The exact words still matter.

## 06. What funnel does your chunk have to survive?

**Four filters: dense and sparse search running together, reciprocal rank fusion merging them, then a cross-encoder reranker that narrows ~150 candidates to the 5-20 that reach the model. Most content dies at the reranker.** Dense vector search is one stage of several, and content usually dies at a different stage than people assume.

Dense + sparse

vectors for concepts, BM25 for exact terms

→

Rank fusion

merge by rank, dense 80 / keyword 20

→

Cross-encoder rerank

~150 candidates scored jointly

→

Context window

the 5-20 that reach the model

Figure 2, the production funnel. Four filters between an indexed chunk and a chunk that gets quoted.

Dense vectors are excellent at intent and synonyms and weak at exact lookups (part numbers, SKUs, proper nouns), so BM25 keyword search runs alongside. BM25's term-frequency component saturates, so the tenth mention of a keyword adds almost nothing and dilutes your passage on the vector side, there is no version of this system where stuffing works. The two score scales are incompatible, so [Reciprocal Rank Fusion](/blogs/internal-linking-for-ai-retrieval) throws away raw scores and operates on rank positions, commonly weighting dense 80% and keyword 20%. The passage that wins is rarely the best on either axis, it is the one that is good on both.

Reciprocal Rank Fusion, the whole idea

```
# Reciprocal Rank Fusion, the whole idea in a few lines
K = 60

def rrf(rankings, weights=None):
    scores = {}
    for i, ranked_ids in enumerate(rankings):
        w = (weights or [1] * len(rankings))[i]
        for rank, doc_id in enumerate(ranked_ids, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + w / (K + rank)
    return sorted(scores, key=scores.get, reverse=True)

# Dense search carries more weight than keyword search
final = rrf([dense_results, bm25_results], weights=[0.8, 0.2])
```

Being retrieved is not the same as being read. A chunk at rank 40 in the candidate pool is invisible in exactly the same way as a chunk that was never indexed.

The reranker is where most outcomes are decided. Dense retrieval uses a bi-encoder that embeds query and passage separately (what makes pre-indexing possible); a cross-encoder runs both through one transformer together, letting every query word attend to every passage word. Far more accurate, far too expensive to run over the whole index, so it runs as a second pass over 100 to 150 candidates and narrows them to the 5 to 20 that build the final context.

## 07. What are the three failure modes, and their fixes?

**Semantic fragmentation, lexical mismatch, and ranking degradation, each with an engineering fix and a content-side counterpart you actually control.** Retrieval failures group cleanly into three architectural categories, and diagnosing which one you have matters more than any generic optimisation.

Three failure modes, and the content response to each

| Failure mode | What happens | Your content-side fix |
| --- | --- | --- |
| Semantic fragmentation | Chunking split related facts across passages; no single vector matches. | Write sections that are semantically complete, every section names its own subject. |
| Lexical mismatch | Dense search misses exact constraints, part numbers, identifiers, versions. | Vocabulary discipline, use the literal category, competitor and version terms buyers type. |
| Ranking degradation | The right chunk is retrieved but sits too low to make the window. | Directness, answer the query head-on, early, in language that mirrors the question. |

Clever renaming of a known category is a lexical mismatch you are inflicting on yourself. And cross-encoders reward passages that answer the query head-on: a passage that opens with three sentences of throat-clearing loses to one that opens with the answer, the same shape as [any high-citation page](/blogs/anatomy-of-a-high-citation-page).

## 08. How do you write content that survives the cut?

**By being clearer than you needed to be: self-contained sections, named subjects, front-loaded answers, real structure, self-describing tables, and specific facts. None of it means writing worse for humans.** Everything above collapses into a manageable set of habits, and they mostly amount to writing every section as if it will be read alone, because it will be.

A pre-publish checklist derived from the mechanics

| Check | What good looks like | Failure it prevents |
| --- | --- | --- |
| Section independence | Every H2 makes full sense read alone, with no prior paragraph. | Semantic fragmentation |
| Entity naming | The subject is named by name at least once inside every section. | Vector drift |
| Temporal anchors | Dates and periods stated explicitly, never "last year". | Vector drift |
| Answer position | The core claim appears in the first two sentences of the section. | Ranking degradation |
| Vocabulary match | Uses the literal category and product terms buyers type. | Lexical mismatch |
| Markup integrity | Real H2 and H3 tags in a clean, consistent hierarchy. | Bad boundary placement |
| Table framing | A summary line above each table; subjects repeated in row labels. | Structural fragmentation |
| Specificity | Concrete numbers and named entities, not general characterisation. | Compression loss |

Free Tool · Analyzer

Read your page the way a retriever does

Paste your content; it splits into passages and scores each one alone, flagging the orphaned chunks that never name their subject.

Primary topic / entity optional

Paste your page content

Simulates fixed-size chunking (~150 words). Each passage is scored in isolation, with no title and no surrounding text, exactly the object that competes in the vector index.

Retrievability

Heuristic scan for the failure modes in the article: unnamed subject, dangling pronouns, vague time anchors, buried answers, and low specificity. An orphaned chunk is one that never says what it is about.

[Open the full tool →](/tools/chunk-retrievability-analyzer)

Front-loading the answer helps at three separate stages at once, coarse first-pass filtering, cross-encoder scoring, and the moment a model decides which passage to quote, which is exactly what the [answer-block optimizer](/tools/answer-block-optimizer) checks. Naming the subject in every section directly reduces fragmentation, the highest-leverage change a content team can make, and it is the same explicitness that [makes you resolvable as an entity](/blogs/becoming-an-entity).

The authority connection

None of this replaces authority. Retrieval mechanics determine whether your passage can be found; corroboration across independent sources, consistent entity naming, and genuine subject depth determine whether it gets trusted once it is. Mechanics get you into the candidate pool. [Authority](/blogs/authority-seeding-ai-llm-trust) is what survives the reranker.

## 09. How do you tell whether any of this is working?

**With two metrics, context precision (is the good material near the top) and context recall (was everything needed retrieved at all), plus a manual buyer-question loop you can run without touching anyone's index.** Retrieval quality is measurable, and the two metrics that matter are worth borrowing even if you never run a formal evaluation. They pull against each other, governed by the retrieval window size.

Figure 3, precision and recall as a function of retrieval window size. Retrieve fifty chunks and recall climbs while precision falls; retrieve two and precision peaks while facts spread across passages go missing. Every system picks a point on this curve.

The retrieval metrics worth knowing

| Metric | What it measures | What a low score is telling you |
| --- | --- | --- |
| Context precision | Signal-to-noise and ranking quality. | Ranking is weak, relevant passages exist but sit too low. |
| Context recall | Completeness of retrieved information. | The candidate window is too narrow, or facts are fragmented. |
| Context entity recall | Coverage of named entities. | Vocabulary and entity-naming gaps between query and corpus. |
| Faithfulness | Whether generated claims are grounded in context. | The generator is hallucinating past what was retrieved. |
| Answer relevancy | Whether the output addresses the actual question. | Instruction-following failure downstream of retrieval. |

You will not run RAGAS on someone else's index, but a manual equivalent is genuinely useful: build 30 to 50 questions your buyers actually ask in their words; run each through the assistants that matter and record whether you appear and which passage got quoted; for the misses, read the passage on your site that should have answered it in isolation, with no title and no surrounding text. In most cases the reason is visible in ten seconds, the passage does not name its subject, does not state its qualifier, or buries the answer four sentences deep. Fix the passage, not the page, then [re-run the same question set in four to six weeks](/blogs/prompt-to-citation-tracking). Different assistants weight these stages differently, which is part of [why engines recommend different vendors](/blogs/why-engines-recommend-different-vendors).

Free tools from this piece

Three browser-based tools built from this teardown: the [Chunk Retrievability Analyzer](/tools/chunk-retrievability-analyzer) to find your orphaned passages, the [Retrieval-Readiness Checklist](/tools/retrieval-readiness-checklist) to score a page against the eight-point test, and the [RRF Rank-Fusion Calculator](/tools/rrf-rank-fusion-calculator) to see how dense and keyword rankings merge. All free, all run in your browser.

## 10. What's the takeaway?

**At every step, the same content property is rewarded: explicitness. Passages that name their subject, state their qualifiers, use the vocabulary of the question, and answer it directly.** Retrieval is not a black box. It is a sequence of mechanical steps, each of which discards content for a specific and knowable reason: your document gets split because a fixed vector cannot hold a page; the split severs relationships; engineering compensates with contextualisation and late chunking; then dense and keyword search merge by rank fusion and get filtered by a cross-encoder before anything reaches a model.

Write every section as if it will be read alone. Because it will be.

That is not a hack, and it will not stop working when the architectures change. It is simply what it looks like to write for a reader who arrives in the middle, with no context, and only a few seconds of attention to spend, which, as it turns out, describes most human readers too.

Frequently Asked Questions

### Do AI search engines read my whole page?

No. Before an AI engine can cite you, your page is split into passages (typically 150-600 words, 200-800 tokens), each converted into a fixed-length vector and stored in an index. When someone asks a question, that question is vectorised too and the system retrieves the closest-matching passages, not pages. The unit that competes for a citation is a single chunk, scored alone with no title, no navigation and no memory of the paragraph above it, so writing and auditing at the page level misses where the contest actually happens.

### Why does my best content sometimes get zero AI visibility?

Usually context rupture. Standard pipelines embed each chunk in isolation, so a passage that carries its meaning through pronouns or references to earlier paragraphs, "the division", "this approach", "last year", loses its subject when cut. Its vector lands away from the query's vector and it falls outside the nearest-neighbour search radius, so the fact is correctly indexed but cannot be found. The fix is to name the subject, state the timeframe, and repeat the qualifier inside every section.

### What is contextual retrieval and late chunking?

Two engineering fixes for context rupture. Contextual retrieval (Anthropic) uses an LLM to write a short prefix naming a chunk's subject and timeframe before indexing it, cutting top-20 retrieval failures by 35%, rising to 67% when combined with keyword search and reranking. Late chunking (Jina AI) runs the whole document through a long-context encoder first so every token vector carries global context, then slices, preserving cross-chunk meaning at no query-time cost. Both recover context that was written down, neither can invent context you never stated.

### How do I write content that gets retrieved and cited?

Write every H2 section so it makes sense read alone: name the subject by name at least once, state dates explicitly, put the core claim in the first two sentences, use the literal terms buyers type (category, competitor and version names), keep real H2/H3 markup, add a summary line above every table, and prefer concrete numbers over general characterisation. These reduce the three failure modes, semantic fragmentation, lexical mismatch and ranking degradation, without writing worse for humans.

References

The research and engineering sources this teardown draws on.

1. [Contextual Retrieval in AI Systems. Anthropic.](https://www.anthropic.com/engineering/contextual-retrieval)
2. [jina-ai/late-chunking: code for explaining and evaluating late chunking. GitHub.](https://github.com/jina-ai/late-chunking)
3. [Late Chunking in Long-Context Embedding Models. Jina AI.](https://jina.ai/news/late-chunking-in-long-context-embedding-models/)
4. [A Step-by-Step RAG Evaluation Process & Key Metrics Explained. Openxcell.](https://www.openxcell.com/blog/rag-evaluation/)
5. [RAG Evaluation Metrics: Best Practices. Patronus AI.](https://www.patronus.ai/llm-testing/rag-evaluation-metrics)
6. [Matryoshka Representation Learning (arXiv:2205.13147). arXiv.](https://arxiv.org/abs/2205.13147)
7. [Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models (PDF). arXiv.](https://arxiv.org/pdf/2409.04701)
8. [Enhancing RAG with contextual retrieval. Claude Cookbook.](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide)
9. [Late Chunking: Contextual Chunk Embeddings (v3). arXiv.](https://arxiv.org/html/2409.04701v3)
10. [Late Chunking: Contextual Chunk Embeddings (v2). arXiv.](https://arxiv.org/html/2409.04701v2)
11. [Chunking Strategies for LLM Applications. Pinecone.](https://www.pinecone.io/learn/chunking-strategies/)
12. [Contextual Retrieval in Retrieval-Augmented Generation (RAG). Box Blog.](https://blog.box.com/contextual-retrieval-in-retrieval-augmented-generation-rag)
13. [Implementing Anthropic's Contextual Retrieval with Async Processing. Instructor.](https://python.useinstructor.com/blog/2024/09/26/implementing-anthropics-contextual-retrieval-with-async-processing/)
14. [Late Chunking vs Contextual Retrieval: The Math Behind RAG's Context Problem. KX Systems on Medium.](https://medium.com/kx-systems/late-chunking-vs-contextual-retrieval-the-math-behind-rags-context-problem-d5a26b9bbd38)
15. [Introducing Contextual Retrieval by Anthropic. r/Rag, Reddit.](https://www.reddit.com/r/Rag/comments/1fl2wma/introducing_contextual_retrieval_by_anthropic/)
16. [Late Chunking in RAG: Improving Text Retrieval Performance. Bluetick Consultants.](https://www.bluetickconsultants.com/unlocking-better-text-retrieval-with-late-chunking-a-revolutionary-approach-for-rag-applications/)
17. [MIPIC: Matryoshka Representation Learning via Self-Distilled Intra-Relational and Progressive Information Chaining. arXiv.](https://arxiv.org/html/2604.24374v2)
18. [MaxSim Operator in Dense Retrieval. Emergent Mind.](https://www.emergentmind.com/topics/maxsim-operator)
19. [Late Chunking: Embedding First, Chunk Later. Stackademic.](https://blog.stackademic.com/late-chunking-embedding-first-chunk-later-long-context-retrieval-in-rag-applications-3a292f6443bb)
20. [Ragas Evaluation: In-Depth Insights. PIXION Blog.](https://pixion.co/blog/ragas-evaluation-in-depth-insights)
21. [RAG Evaluation Simplified, Part 2: Deep Dive into Recall & Precision. Medium.](https://medium.com/@fassha08/rag-evaluation-simplified-part-2-deep-dive-into-recall-precision-4853709630bb)
22. [Context Recall. Ragas Documentation.](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/)
23. [Metrics. Ragas Documentation.](https://docs.ragas.io/en/v0.1.21/concepts/metrics/)
24. [Evaluating RAG Applications with RAGAs. Leonie Monigatti.](https://www.leoniemonigatti.com/blog/rag-evaluation-with-ragas.html)
25. [Context Precision. Ragas Documentation.](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/)
26. [Contextual retrieval in Anthropic using Amazon Bedrock Knowledge Bases. AWS.](https://aws.amazon.com/blogs/machine-learning/contextual-retrieval-in-anthropic-using-amazon-bedrock-knowledge-bases/)

About rawmktg.

rawmktg. publishes data-driven teardowns and technical playbooks on GEO, retrieval mechanics and B2B AI-search visibility. Method: same data, same lens, every time. Contact: vinayak@rawmktg.com

Sources: Anthropic contextual retrieval, Jina AI late chunking, the Matryoshka Representation Learning and ColBERT papers, Pinecone chunking guidance, and the RAGAS evaluation framework, 2024-26. Code is illustrative; figures are drawn from the cited sources.
