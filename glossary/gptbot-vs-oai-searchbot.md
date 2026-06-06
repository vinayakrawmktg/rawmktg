# What is GPTBot vs OAI-SearchBot?

GPTBot and OAI-SearchBot are two different OpenAI crawlers: GPTBot collects data used to train models, while OAI-SearchBot builds the live search index that lets ChatGPT retrieve and cite current web pages.

## How it works

The distinction matters because the two serve opposite goals. Allowing OAI-SearchBot keeps you eligible for citations in ChatGPT search. Allowing GPTBot lets your content be used in future model training, which some publishers permit and others block.

This is why a blanket block of all OpenAI bots can backfire: it is possible, and often preferable, to allow the citation crawler while restricting the training crawler, so you stay visible in answers without contributing to training corpora.

## Training crawler vs citation crawler

A training crawler gathers text to improve a model and affects what the model knows in general. A citation crawler builds a live index and affects whether your specific pages get named in answers today. They are [configured separately in robots.txt](/blogs/how-ai-crawlers-index-your-site).

## Why it matters for B2B

Getting this split right is the single most consequential robots.txt decision for AI visibility. Block the wrong bot and you either leak content to training or disappear from citations, when you can usually choose precisely.

**Example**

```
User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Disallow: /
```

This robots.txt keeps you eligible for citations in ChatGPT search while keeping your content out of model-training collection. A blanket block of all OpenAI bots gives up the first to get the second.

*Source: https://rawmktg.com/glossary/gptbot-vs-oai-searchbot · rawmktg. by Vinayak Ravi*
