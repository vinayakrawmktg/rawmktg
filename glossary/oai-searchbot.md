# What is OAI-SearchBot?

OAI-SearchBot is OpenAI's crawler for its search product: it fetches and indexes web pages so they can be retrieved and cited when ChatGPT search answers a user's query.

## How it works
It is distinct from the crawler OpenAI uses to gather training data. OAI-SearchBot exists to build the live search index that feeds citations, which means allowing it is how you stay eligible to be cited in ChatGPT search results.
Like other AI search crawlers, it does not execute JavaScript. In rawmktg's testing, none of the three major AI crawlers run JS, so any content that only appears after client-side rendering is effectively invisible to them.

## OAI-SearchBot vs GPTBot
GPTBot is OpenAI's crawler for collecting training data. OAI-SearchBot is its crawler for the live search index that powers citations. Blocking GPTBot protects content from training use; blocking OAI-SearchBot removes you from ChatGPT search results, which is usually the opposite of the goal.

## Why it matters for B2B
If you want to appear in ChatGPT's answers, OAI-SearchBot is the bot that has to be able to reach and read your pages. Confirming it is allowed, and that your content is in static HTML, is step zero.

*Source: https://rawmktg.com/glossary/oai-searchbot · rawmktg. by Vinayak Ravi*
