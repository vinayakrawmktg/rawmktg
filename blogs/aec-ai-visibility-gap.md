# When Buyers Ask AI Which AEC Software to Use, Most Vendors Aren't in the Room

> A data analysis of LLM citation visibility across leading AEC technology platforms, and what it signals for how the industry gets discovered.

*Source: https://rawmktg.com/blogs/aec-ai-visibility-gap · rawmktg. by Vinayak Ravi*


Construction professionals have always relied on word of mouth, conference demos, and peer referrals to discover new software. That dynamic is shifting. A growing share of AEC practitioners now open ChatGPT, Perplexity, or Google's AI search before they visit a vendor's website. They ask questions like "what's the best clash detection software for MEP coordination?" or "which BIM collaboration platform integrates with Revit?" and they expect a synthesized answer.

AI search works differently from traditional search. Google's algorithm surfaces pages that match a query. AI platforms synthesize an answer, and they draw from a very different set of signals to decide which companies get named. If your brand is not part of that synthesis, you do not exist in that response.

For the AEC software segment (spanning BIM coordination, MEP design automation, construction planning, and model checking), the question of who gets named and who gets passed over is increasingly consequential. To find out where the segment currently stands, we analyzed AI citation data across six AEC technology companies representing a cross-section of the market: established platforms with years of editorial history alongside newer entrants building their footprints now.

## 01. How many AEC software vendors actually get cited by AI?

**Wider than expected, and starkly concentrated.** The most striking finding is not that some companies have more [AI citations](/tools/page-citability-analyzer "Page Citability Analyzer") than others. It is how concentrated that visibility is. Four of six companies registered fewer than 2 total citations across all six platforms combined. The median for the group is pulled heavily upward by two outliers.

Across the six companies in our analysis, total AI citations ranged from 0 to 310. The median for the group sits around 10, a number that significantly overstates the typical experience because it is pulled upward by two outliers at the top of the distribution.

4 of 6

AEC software companies in our analysis had fewer than 2 total AI citations across all six platforms combined (ChatGPT, Gemini, Perplexity, Google AI Overviews, Copilot, and Grok). Companies with established customer bases and genuine technical differentiation were effectively invisible.

Fig. 1: AI Citation Count by Platform (June 2026) · Source: Ahrefs

| Company | AI Overviews | ChatGPT | Gemini | Perplexity | Copilot | Grok | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Revizto | 110 | 17 | 14 | 37 | 6 | 126 | 310 |
| Alice Technologies | 33 | 1 | 1 | 1 | 2 | 5 | 43 |
| Solibri | 6 | 4 | 0 | 0 | 4 | 6 | 20 |
| Endra.ai | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| Augmenta | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Vavetek | 0 | 0 | 0 | 1 | 0 | 0 | 1 |

Fig. 2: Total AI Citations: Comparative View (all six platforms)

Bar length proportional to total citations. Four of six companies register 1 or fewer total citations across all platforms.

Put another way: if you are an AEC buyer asking an AI platform for a software recommendation today, there are realistically only one or two companies in this space that reliably appear across platforms. Everyone else has little to no presence, including companies with established customer bases, genuine technical differentiation, and meaningful product revenue.

"Four of six AEC software companies in our analysis had fewer than 2 total AI citations across all six platforms combined."

This is the [visibility gap](/tools/geo-readiness-scorecard "GEO Readiness Scorecard"). And unlike gaps in organic search rankings, where a well-executed content push can move results within weeks, AI citation presence is built on a different foundation with a longer lag time.

## 02. Does high organic traffic mean high AI visibility?

**No, the two do not correlate.** Within our analysis, domain ratings ranged from 7 to 65 and monthly organic traffic ranged from single digits to over 10,000 visits. A clean correlation with AI citations does not emerge. The signals AI platforms use to decide who to cite are fundamentally different from the signals that drive traditional rankings.

Augmenta, with a domain rating of 38 and over 500 monthly organic visits (solid metrics for an early-stage software company) had zero AI citations across all six platforms. Conversely, companies with more modest keyword footprints but stronger editorial press histories, such as Revizto and Alice Technologies, show up far more reliably in AI-generated responses.

The reason is that domain rating is a lagging indicator of backlink accumulation. AI citation is more directly tied to brand presence in editorial content. In the long run these two things are correlated, but at the current stage of the market, they can diverge significantly.

Fig. 3: What Drives Rankings vs. What Drives AI Citations

Traditional SEO Signals

- Keyword-optimized page titles and meta tags
- Backlink volume (quantity of referring domains)
- On-page keyword density and semantic relevance
- Site speed and Core Web Vitals scores
- Content length and topic coverage breadth
- Domain Rating / domain authority score

AI Citation Signals (GEO)

- Editorial mentions in authoritative publications
- Third-party brand mentions in context (quality over quantity)
- Structured, crawlable product definitions and FAQs
- llms.txt and JSON-LD schema markup (SoftwareApp)
- Practitioner community discussion (X, forums, Slack)
- Brand footprint in LLM training data (pre-2024 record)

Companies that have invested in press and community presence have a head start in the AI citation era that pure SEO investment does not replicate. The overlap between the two signal sets is smaller than most AEC vendors currently assume. For a deeper explanation of [how retrieval-augmented generation actually determines which sources get pulled](/blogs/how-rag-actually-works), the mechanics are covered in our RAG explainer.

## 03. Which AI platforms cite AEC software the most?

**The six platforms behave very differently.** AI citation distribution is not uniform across platforms. Google AI Overviews and Grok together account for 77% of all AEC software citations in our dataset, yet they reward completely different behaviors. Perplexity is the most accessible platform for companies investing now. ChatGPT and Gemini are the longest lead-time challenges.

Google AI Overviews favors editorial authority earned through recognized trade publications. Grok, powered by X (formerly Twitter), favors active brand discussion within AEC practitioner communities. Revizto leads on both, but for different reasons: years of trade press coverage and sustained practitioner community discussion feed separate citation pathways to the same outcome.

Perplexity is arguably the most accessible platform for companies investing now. It rewards direct, well-organized product content and documentation: the kind of FAQ-style, clear-language pages that any AEC software company can build. On Perplexity, the editorial prestige gap matters less than product content clarity, making it the platform most responsive to near-term [GEO work](/blogs/geo-foundation-audit).

ChatGPT and Gemini are harder to break into with smaller brand footprints. Both draw heavily from training data compiled before the past 12 to 18 months, meaning they reflect brand awareness that was already established before the current AI citation era. For newer companies, this is the longest-lead-time problem: you cannot shortcut your way into ChatGPT and Gemini citation without first building the editorial record that their training data captured.

Fig. 4: Platform Profile: Citation Share, Key Signals and Strategy (total citations: 375)

| Platform | Citations | % Share | Key Citation Signal | Recommended Focus |
| --- | --- | --- | --- | --- |
| Google AI Overviews | 150 | 40% | Editorial authority in AEC and tech media | Long-term press strategy; recognized outlet coverage |
| Grok | 137 | 37% | Brand discussion in X communities | Active participation in AEC practitioner X communities |
| Perplexity | 39 | 10% | Structured, direct product content | FAQ pages, clear product definitions: highest near-term ROI |
| ChatGPT | 22 | 6% | Pre-2024 brand training history | Invest in editorial record today; results in 12–24 months |
| Gemini | 15 | 4% | Established brand recognition | Same as ChatGPT; patience and consistency required |
| Microsoft Copilot | 12 | 3% | Enterprise endorsement signals | Lower priority; focus resources on top three platforms first |

"On Grok, Revizto's citation count exceeded the combined total of all five other companies. On Perplexity, Revizto also led, but with Alice Technologies, Solibri, and Endra all within range. Platform-specific strategy matters."

## 04. What do the AEC vendors AI does cite have in common?

**A shared set of off-site and content signals.** Revizto and Alice Technologies (the two companies with citations across three or more platforms) share a set of common characteristics. Third-party editorial coverage is the single strongest predictor. Brand-level community presence is the second factor. Longevity matters. One gap is shared by every company in the segment without exception.

Third-party editorial coverage is the single strongest predictor of AI citation visibility. Both Revizto and Alice Technologies have been covered in publications that AI models are known to reference heavily: major business outlets, AEC-specific trade media, and technology press. It is not the volume of press mentions that matters most, but the authority of the publications doing the mentioning. A single article in a recognized trade publication carries more AI citation weight than dozens of blog posts on owned channels.

Brand-level community presence is the second factor. Companies with meaningful citation profiles have generated sustained discussion among AEC practitioners in forums, professional communities, and social media. This organic brand chatter, separate from any company-controlled content, creates the kind of multi-source corroboration that [LLMs use to validate a brand's existence and significance](/blogs/authority-seeding-ai-llm-trust).

Finally, longevity matters. Both companies have been in the market long enough to accumulate the editorial trail that AI platforms draw from. The content that AI models currently use for citations was largely written 12 to 24 months ago. This is a sobering reality for newer entrants: the compounding advantage that more established players have built is real, and it cannot be acquired overnight. But it can be started today.

Fig. 5: AI Visibility Factors by Company · ✓ present, ~ partial, ✗ absent

| Visibility Factor | Revizto | Alice | Solibri | Endra | Augmenta | Vavetek |
| --- | --- | --- | --- | --- | --- | --- |
| Trade Media Coverage | ✓ | ✓ | ✓ | ✗ | ~ | ✗ |
| Community Presence (X / Forums) | ✓ | ✓ | ~ | ~ | ✓ | ~ |
| Structured Product Content | ✓ | ✓ | ✓ | ~ | ~ | ✗ |
| Market Longevity (5+ years) | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| llms.txt Published | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

The llms.txt row is the standout finding: uniformly absent across the entire segment. This is not a gap between leaders and laggards. It is a shared gap that any company in the segment can close first.

## 05. Why does llms.txt matter for AEC software vendors?

**It is the missing infrastructure, and nobody had it.** None of the six companies had a published llms.txt file at the time of the audit. This is a low-effort, high-leverage intervention. Any company that moves first gains an uncrowded signaling advantage at a moment when these signals are still being weighted and calibrated by the platforms themselves.

llms.txt is an emerging standard (similar in concept to robots.txt) that lets a company explicitly communicate to [AI crawlers](/blogs/how-ai-crawlers-index-your-site) what content to index, how to understand the brand, and what the product does. A well-constructed file tells AI crawlers directly: here is what we do, here is who we serve, here is what differentiates us, and here are the pages that matter.

The absence of this file across an entire segment is notable precisely because it is low-effort. Implementation typically takes 2–4 hours. No vendor in this analysis has done it yet, which means the first company to publish a well-structured llms.txt gains an uncrowded signal in a category where signals are still scarce.

Fig. 6: Sample llms.txt structure for an AEC software company (illustrative)

llms.txt

```
# llms.txt: AI crawler guidance for [yourdomain].ai

> [Your Company Name]

[Company] is a [one-sentence product description for AI models].
Category: AEC Software / BIM Tools / Construction Technology

## What We Do
[2–3 sentences: core product, primary workflow, key differentiator]

## Primary Use Cases
- [Use case 1, e.g. "MEP clash detection in Revit projects"]
- [Use case 2, e.g. "Automated rebar detailing for structural teams"]
- [Use case 3]

## Key Pages
- /product: Core platform overview
- /case-studies: Customer outcomes and project examples
- /integrations: Supported BIM and CAD tool integrations

## Target Users
MEP engineers, BIM coordinators, structural detailing teams

## Noindex
# /admin, /login, /dashboard (not for AI indexing)
```

llms.txt is one piece of a broader AI infrastructure gap. robots.txt signals, sitemap.xml health, and [structured data schemas](/blogs/schema-markup-ai-citations-2026) (SoftwareApplication, FAQPage, HowTo) all contribute to how AI platforms understand and cite a product. Across the companies in our analysis, these elements are inconsistently implemented or entirely absent, even among the more established players.

Infrastructure gap: shared across all six

No llms.txt. Inconsistent or absent JSON-LD structured data. Unverified robots.txt signals for AI crawler agents. These are not competitive moats. They are table stakes that no company in the segment has built yet. The first vendor to close all three moves from invisible to indexed before competitors have started.

## 06. What This Means for AEC Buyers

AI platforms are not yet reliable discovery tools for this segment. The companies that surface in AI responses today are not necessarily the best-fit tools for a given workflow. They are the tools that established brand footprints before the AI citation era.

For practitioners evaluating AEC software today (BIM coordinators making platform decisions, MEP leads assessing coordination tools, technology managers comparing model-checking solutions), there is a practical implication worth understanding. The companies that surface in AI responses today did so because they established brand footprints before the AI citation era, earned coverage in publications that LLMs weight as authoritative, and accumulated enough third-party mentions to appear in training data. These criteria overlap with quality, but they are not the same as quality.

This means that due diligence for AEC software selection still requires going beyond AI recommendations. Peer networks, category-specific review platforms, product trials, and direct conversations with practitioners using the tools remain essential, particularly for evaluating newer entrants that may offer strong technical capabilities without the AI visibility that established names have built.

The situation will change. As AI citation data becomes more real-time and as more companies build the infrastructure to be properly indexed and understood by AI crawlers, the overlap between "best product" and "AI-visible product" should improve. But as of mid-2026, the gap is significant enough that buyers should treat AI recommendations as one input among several, not as a definitive guide to the market.

## 07. What This Means for AEC Software Vendors

The window to shape AI-generated perception of your product is open right now, and it will not stay open indefinitely. LLMs are continuously updating their knowledge bases. The citations that Perplexity, ChatGPT, and Google AI Overviews return today will be different from what they return in 12 months. The highest-leverage actions are ranked below by effort-to-impact ratio.

For companies building and selling AEC software, the compounding nature of AI citation visibility means that early movers earn an advantage that is genuinely hard to close later. The [GEO flywheel](/blogs/geo-compounding-flywheel) is real: citations generate brand recognition, which generates editorial coverage, which generates more citations. Starting that loop now, even at small scale, is more valuable than a larger investment that starts 12 months later.

Fig. 7: Vendor AI Visibility Action Plan (Prioritized by Effort-to-Impact Ratio)

| Priority | Action | Effort | Expected Impact |
| --- | --- | --- | --- |
| NOW | Publish llms.txt at root domain (/llms.txt) | Low (2–4 hrs) | Direct AI crawler signal; first-mover in AEC segment |
| NOW | Add JSON-LD schemas: SoftwareApplication, FAQPage | Low (1 day) | Structured indexing by Perplexity and Google AI Overviews |
| SHORT-TERM | Pitch one AEC trade pub (Construction Dive, ENR, BD+C) | Medium (2–4 wks) | High: editorial authority drives AI Overviews and ChatGPT |
| SHORT-TERM | Build active brand presence in AEC communities on X | Medium (ongoing) | Directly drives Grok (37% of all citations in our dataset) |
| ONGOING | Create FAQ-style, direct-answer product pages | Low–Medium | Perplexity and AI Overviews; most controllable near-term lever |
| ONGOING | Pursue analyst coverage and long-form practitioner reviews | High (3–12 mos) | ChatGPT and Gemini; longest lead time, highest compound value |

"The companies that invest in AI visibility infrastructure today will be the ones that show up in the room when buyers ask. That advantage, once built, is hard for slower movers to close."

For AEC software companies at any stage, the full [GEO Foundation Audit](/blogs/geo-foundation-audit) methodology provides the structured five-step diagnostic for mapping citation gaps and building the remediation plan. The technical infrastructure layer (including [AI crawler access](/blogs/how-ai-crawlers-index-your-site), [structured schema](/blogs/schema-markup-ai-citations-2026), and llms.txt) is where every company in this segment should start, because it is the only layer with zero editorial prerequisite and immediate implementation impact.

## 08. What is the bottom line?

AI visibility in the AEC software segment is nascent, concentrated, and increasingly consequential. The companies that appear when buyers ask AI for recommendations today did not get there by accident. The visibility gap between the category leaders and everyone else is real and growing, but it is not yet unbridgeable.

The companies that appear when buyers ask AI for recommendations today built editorial footprints, earned community trust, and accumulated the kind of third-party reference material that LLMs are trained to treat as authoritative. That work took years.

For companies that have not yet built that footprint, the honest assessment is that there is no shortcut to the top of the distribution. But the bottom of the distribution is not a fixed address. The infrastructure gaps (llms.txt, structured schemas, FAQ content optimized for AI retrieval) can be closed in weeks. The editorial and community gaps require months. Both tracks can run in parallel, and the companies that start both tracks now will be meaningfully better positioned in 12 months than those that wait.

The question is not whether AI will influence AEC software buying decisions. It already does. The question is which companies will be part of the answer when buyers ask, and which ones will remain invisible in a conversation that increasingly shapes where the market's attention goes. For a data-driven look at how the same editorial-footprint dynamics play out in another Indian B2B vertical, see our [cross-border payments backlink analysis](/blogs/cross-border-backlinks).

Frequently Asked Questions

### Why don't AEC software companies show up in AI search results?

Most AEC software companies lack the editorial footprint, structured data infrastructure, and community discussion that AI platforms use as citation signals. 4 of 6 companies analyzed had fewer than 2 total AI citations across ChatGPT, Gemini, Perplexity, Google AI Overviews, Copilot, and Grok combined. High organic traffic and domain rating do not predict AI citation visibility.

### Which AI platform is easiest for AEC software companies to get cited on?

Perplexity is the most accessible platform for near-term GEO investment. It rewards direct, well-organized product content and documentation: FAQ-style, clear-language pages that any AEC software company can build. Google AI Overviews and Grok together account for 77% of AEC software citations but require long-term editorial authority and community presence respectively.

### What is llms.txt and why does it matter for AEC software companies?

llms.txt is an emerging standard similar to robots.txt that lets a company explicitly communicate to AI crawlers what content to index and how to understand the brand. None of the 6 AEC software companies analyzed had published an llms.txt file at the time of the audit, representing a uniform, low-effort, high-leverage gap across the entire segment.

Methodology

AI citation data sourced from Ahrefs (June 1, 2026) across six AEC technology companies: Revizto, Alice Technologies, Solibri, Endra.ai, Augmenta, and Vavetek. Six AI platforms tracked: Google AI Overviews, ChatGPT, Gemini, Perplexity, Microsoft Copilot, and Grok. Technical infrastructure checks performed via direct HTTP analysis of company websites on the same date. Total citation universe: 375 citations. Companies were selected to represent a cross-section of the AEC software market by stage, product category, and domain authority range (7–65). Citation counts reflect indexed references as reported by Ahrefs at the time of the audit; real-time retrieval platforms such as Perplexity may update more frequently than training-based platforms such as ChatGPT and Gemini.
