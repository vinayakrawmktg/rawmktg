# What is Interaction to Next Paint (INP)?

Interaction to Next Paint (INP) is a Core Web Vital that measures how quickly a page visually responds to user interactions across the whole visit. It replaced First Input Delay as a Core Web Vital in March 2024.

## How it works

INP observes the latency of taps, clicks, and key presses throughout the session and reports a value representing the page's worst-ish responsiveness. Google's good threshold is 200 milliseconds or below.

Poor INP usually traces to heavy JavaScript blocking the main thread, so fixes involve breaking up long tasks, reducing script work, and deferring non-critical code.

## INP vs First Input Delay (FID)

FID, which INP replaced, only measured the delay before the page responded to the first interaction. INP measures responsiveness across all interactions and includes the time to actually paint the result, making it a fuller, stricter measure of how responsive a page feels throughout use.

## Why it matters for B2B

Like the other vitals, INP is a human and ranking metric rather than an AI-citation factor. Its relevance to AI work is indirect: the heavy client-side JavaScript that wrecks INP is often the same code that renders content client-side and [hides it from AI crawlers](/blogs/how-ai-crawlers-index-your-site), so reducing that JavaScript tends to help both responsiveness and crawlability.

**Common mistake**

Blocking the main thread with heavy JavaScript, including third-party tags, so taps and clicks feel laggy. INP measures that delay across the whole visit, so trimming and deferring scripts is the main lever.

*Source: https://rawmktg.com/glossary/interaction-to-next-paint · rawmktg. by Vinayak Ravi*
