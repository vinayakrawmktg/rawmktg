# What is Cumulative Layout Shift (CLS)?

Cumulative Layout Shift (CLS) is a Core Web Vital that quantifies how much visible content jumps around unexpectedly as a page loads. A lower score means a more visually stable page; Google's good threshold is 0.1 or below.

## How it works

Shifts happen when elements load without reserved space: images without dimensions, ads or embeds that push content down, or fonts that swap and reflow text. CLS sums the impact of these unexpected movements over the page's life.

Fixes are mostly about reserving space in advance: setting width and height on media, preloading fonts, and avoiding inserting content above existing content.

## CLS vs LCP

LCP measures how fast the main content appears; CLS measures how much everything moves once it does. A page can paint quickly (good LCP) yet be infuriating to use because elements keep jumping (poor CLS). They are independent axes of the same loading experience.

## Why it matters for B2B

CLS is purely a human-experience metric with no bearing on whether an AI engine can read or cite your content; crawlers do not experience layout shift. It earns its place in a technical glossary because clients ask about it, but the honest guidance for AI visibility is to treat it as a conversion and usability concern, not a citation lever.

**Common mistake**

Omitting width and height on images and embeds, or injecting banners and ads above content after load. Both shove the page around as it renders and spike CLS; reserve space for anything that arrives late.

*Source: https://rawmktg.com/glossary/cumulative-layout-shift · rawmktg. by Vinayak Ravi*
