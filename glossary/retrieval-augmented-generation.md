# What is Retrieval-Augmented Generation (RAG)?

Retrieval-Augmented Generation (RAG) is the architecture most AI search systems use to answer a query: they retrieve relevant passages from an external source such as the web, then generate an answer grounded in and citing those passages.

## How it works

Instead of answering only from what the model memorised in training, a RAG system runs a retrieval step first. It decomposes the query, fetches candidate passages, reranks them by relevance and authority, and feeds the best ones to the model as context for the answer.

Because it competes at the passage level, your content is judged in fragments, not as a whole page. A clean, self-contained passage near the top of a page is far more likely to be retrieved and cited than the same point buried mid-article.

## RAG vs a base language model

A base language model answers from its training data, with a fixed knowledge cutoff and no sources. A RAG system retrieves live external content at query time and grounds its answer in it, which is what lets AI search cite current pages and name the brands in them.

## Why it matters for B2B

RAG is the mechanism that decides whether your content is even eligible to be cited. Understanding it tells you why structure and extractability, not just authority, determine whether a model can pull your page into an answer.

*Source: https://rawmktg.com/glossary/retrieval-augmented-generation · rawmktg. by Vinayak Ravi*
