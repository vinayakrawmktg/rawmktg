# What is Core Web Vitals?

Core Web Vitals are a set of Google metrics that measure real-world page experience across three axes: loading (LCP), interactivity (INP), and visual stability (CLS). They feed into Google's page-experience signals.

## How it works

The three metrics are measured from real user data where available and lab data otherwise. Google publishes thresholds for good, needs-improvement, and poor on each, and assesses pages against the 75th percentile of real users.

They are a ranking input, but a modest one: strong vitals will not rescue weak content, and weak vitals will not sink genuinely better pages on their own. They matter most as a tiebreaker and as a user-retention factor.

## Core Web Vitals vs page speed

Page speed is the older, narrower idea of how fast a page loads. Core Web Vitals broaden that to include interactivity and visual stability, and ground it in real-user measurement rather than a single lab score. Vitals are page speed plus how stable and responsive the page feels, measured in the field.

## Why it matters for B2B

Vitals are largely a human-experience and ranking concern rather than a direct AI-citation factor; [current AI crawlers care more about whether](/blogs/how-ai-crawlers-index-your-site) content is present in the HTML than how fast it paints. The honest framing for B2B clients is that vitals protect conversion and traditional rankings, while crawlability and content structure do the heavy lifting for AI visibility.

**Example**

```
LCP  < 2.5s    loading
INP  < 200ms   responsiveness
CLS  < 0.1     visual stability
```

These are the "good" thresholds, scored on real-world field data, not just a lab test.

*Source: https://rawmktg.com/glossary/core-web-vitals · rawmktg. by Vinayak Ravi*
