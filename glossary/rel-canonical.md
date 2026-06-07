# What is rel=canonical?

rel=canonical is a link element placed in a page's head that names the preferred URL for that content. It is the primary technical signal used to consolidate duplicate or parameterized URLs onto a single indexable version.

## How it works

The tag looks like a link element pointing at the canonical URL and sits in the head of every variant, including the canonical page itself (a self-referencing canonical). Engines read it as a strong hint about which URL to index and which to fold in.

It can also be delivered as an HTTP header for non-HTML files like PDFs. Mistakes are common: canonicalizing every page to the homepage, pointing canonicals at noindexed or redirected URLs, or using relative paths that resolve wrongly.

## rel=canonical vs noindex

A canonical says these URLs are the same, please index this one. noindex says do not index this URL at all. Using noindex on a duplicate can also suppress the page it duplicates if signals get crossed; canonical is the safer tool for true duplicates because it consolidates rather than removes.

## Why it matters for B2B

Self-referencing canonicals give AI crawlers an unambiguous, machine-readable statement of the one true URL for each answer. That removes guesswork about which version to retrieve and attribute. On templated sets like glossaries, a correct self-canonical on every term page is cheap insurance against parameter and trailing-slash variants splitting your citations.

**Example**

```
<link rel="canonical" href="https://example.com/page" />
```

Put a self-referencing canonical on every page. The usual errors: canonicalising everything to the homepage, or pointing at a noindexed or redirected URL, both of which scramble the signal.

*Source: https://rawmktg.com/glossary/rel-canonical · rawmktg. by Vinayak Ravi*
