# What is @graph?

@graph is a Schema.org JSON-LD construct that lets a page declare multiple connected entities, such as an organisation, a person and an article, in a single structured-data block, with explicit relationships between them.

## How it works

Instead of scattering separate, disconnected schema snippets across a page, an @graph groups them and [links them by identifier](/blogs/schema-markup-ai-citations-2026). This lets a machine see that the article was written by this person, published by this organisation, as one connected model.

That connectedness is what makes it powerful for AI: it resolves a coherent picture of who is behind the content and how the entities relate, which strengthens trust and accurate attribution.

## @graph vs separate schema blocks

Separate schema blocks describe entities in isolation and leave the relationships implicit. An @graph states the relationships explicitly in one place, so a machine does not have to guess how the organisation, author and content connect.

## Why it matters for B2B

For B2B brands, a well-built @graph ties the company, its author entities and its content into one machine-readable identity, which is the foundation of being recognised and cited as a consistent source.

**Example**

```
"@graph": [
  { "@type": "Organization", "@id": "#org",  "name": "rawmktg." },
  { "@type": "Person",       "@id": "#author", "name": "Vinayak Ravi" },
  { "@type": "Article", "author": {"@id": "#author"},
    "publisher": {"@id": "#org"} }
]
```

The `@id` references let a machine read one connected identity, this article, by this author, from this organisation, instead of three unrelated snippets.

*Source: https://rawmktg.com/glossary/graph-schema · rawmktg. by Vinayak Ravi*
