#!/usr/bin/env python3
"""SCRATCH: build /about, /contact, /terms from the privacy.html scaffold. Do NOT commit."""
import re, os
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

P=open("privacy.html",encoding="utf-8").read()
# scaffold = everything before <main ...>  (head + nav)
i=P.index('<main class="page legal">')
HEAD_NAV=P[:i]
# standard footer (rolled out site-wide separately too)
FOOTER='''<footer class="site-foot" aria-label="Site footer">
  <div class="page">
    <div class="foot-row">
      <a href="/" style="font-family:'Geist',system-ui;font-weight:800;font-size:15px;letter-spacing:-0.04em;">raw<span style="color:var(--ink-2)">mktg</span><span style="color:var(--signal)">.</span></a>
      <div class="foot-links"><a href="/about">About</a><a href="/contact">Contact</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/llms.txt">llms.txt</a></div>
      <span>&copy; 2026 rawmktg.</span>
    </div>
  </div>
</footer>'''

def head_for(title, desc, slug):
    h=HEAD_NAV
    h=re.sub(r'<title>[^<]*</title>', f'<title>{title} &middot; rawmktg.</title>', h, 1)
    h=re.sub(r'<meta name="description" content="[^"]*" />',
             f'<meta name="description" content="{desc}" />', h, 1)
    h=re.sub(r'<link rel="canonical" href="[^"]*" />',
             f'<link rel="canonical" href="https://rawmktg.com/{slug}" />', h, 1)
    # nav About -> /about
    h=h.replace('href="/#about"','href="/about"').replace('href="#about"','href="/about"')
    return h

def page(title, desc, slug, main):
    return head_for(title,desc,slug)+main+"\n\n"+FOOTER+"\n\n</body>\n</html>\n"

# ---------------- ABOUT ----------------
about_main='''<main class="page legal">
  <div class="legal-inner">
    <span class="legal-eyebrow">About</span>
    <h1>About rawmktg.</h1>
    <p class="legal-meta">Data-driven teardowns of B2B search and AI visibility</p>

    <p>rawmktg. is a research publication about how B2B brands get discovered in the AI era. It pairs the new mechanics of AI search and Generative Engine Optimization (GEO) with the SEO fundamentals underneath, and tests both against real data rather than opinion.</p>
    <p>Every piece here starts from a dataset, not a hunch. If a finding is published, it is because the numbers behind it showed something worth writing down.</p>

    <h2>Who writes this</h2>
    <p>rawmktg. is written by <strong>Vinayak Ravi</strong>. The analyses come out of original research: AI-citation data pulled across the major engines (ChatGPT, Perplexity, Gemini, Google AI Overviews, Copilot), lined up against the SEO fundamentals underneath, and checked against the published studies that hold up.</p>
    <p>Nothing here is theory for its own sake. The goal is to show B2B marketing teams, founders, and operators exactly where the visibility gaps are in their category, and what actually moves them.</p>

    <h2>The method</h2>
    <p>Same data, same lens, every time. The teardowns use live Ahrefs data (organic keywords, referring domains, AI citations) captured at the time of writing, classified into funnel stages and brand vs non-brand segments from full keyword exports. Where a figure appears, it is drawn from that analysis or from a named, published study.</p>
    <ul>
      <li><strong>Primary sources:</strong> Ahrefs for organic-search and AI-citation data; Google Search Console and GA4 for first-party signals where relevant.</li>
      <li><strong>Secondary sources:</strong> peer-reviewed and industry GEO research (for example the Princeton / Georgia Tech GEO study), cited inline.</li>
      <li><strong>What we avoid:</strong> invented statistics, scraped or spun content, and claims we cannot point to a source for.</li>
    </ul>

    <h2>What you will find</h2>
    <ul>
      <li><a href="/topics/industry-teardowns">Industry teardowns</a> &ndash; data analyses of who wins AI visibility in a specific B2B vertical, and why.</li>
      <li><a href="/topics/how-ai-search-works">How AI search actually works</a>, <a href="/topics/technical-layer">the technical layer</a>, <a href="/topics/content-authority">content and authority</a>, and <a href="/topics/ranking-signals">ranking signals and measurement</a>.</li>
      <li>The <a href="/glossary">AI-Search and Technical SEO glossary</a> &ndash; plain, sourced definitions of the vocabulary behind it all.</li>
    </ul>

    <h2>Get in touch</h2>
    <p>Questions, data requests, corrections, or collaboration ideas are all welcome. The fastest way to reach us is the <a href="/contact">contact page</a>, or email <a href="mailto:vinayak@rawmktg.com">vinayak@rawmktg.com</a> directly.</p>
  </div>
</main>'''

# ---------------- CONTACT ----------------
contact_main='''<main class="page legal">
  <div class="legal-inner">
    <span class="legal-eyebrow">Contact</span>
    <h1>Get in touch</h1>
    <p class="legal-meta">We read every message and reply personally</p>

    <p>rawmktg. is written and run by Vinayak Ravi. Whether you have a question about a teardown, a correction, a data request, or a collaboration idea, the best way to reach us is by email.</p>

    <div class="legal-note">
      <strong>Email</strong>
      <p><a href="mailto:vinayak@rawmktg.com">vinayak@rawmktg.com</a> &nbsp;&middot;&nbsp; we aim to reply within 2 to 3 business days.</p>
    </div>

    <h2>What to reach out about</h2>
    <ul>
      <li><strong>Feedback or corrections</strong> on any analysis. If a number looks off, tell us and we will check and update it.</li>
      <li><strong>Data or teardown requests</strong> for a specific B2B vertical you want analysed.</li>
      <li><strong>Press and citations.</strong> Happy to share methodology or underlying figures for any published piece.</li>
      <li><strong>Collaboration and partnerships</strong> with B2B marketing teams, founders, and operators.</li>
    </ul>

    <h2>Elsewhere</h2>
    <ul>
      <li>LinkedIn: <a href="https://www.linkedin.com/in/vinayakravi/" target="_blank" rel="noopener">linkedin.com/in/vinayakravi</a></li>
      <li>X: <a href="https://x.com/vinayaksravi" target="_blank" rel="noopener">@vinayaksravi</a></li>
    </ul>

    <h2>Newsletter</h2>
    <p>To get new teardowns and glossary additions in your inbox, subscribe from the <a href="/#newsletter">homepage newsletter</a>. No spam, unsubscribe any time.</p>
  </div>
</main>'''

# ---------------- TERMS ----------------
terms_main='''<main class="page legal">
  <div class="legal-inner">
    <span class="legal-eyebrow">Legal</span>
    <h1>Terms of Use</h1>
    <p class="legal-meta">rawmktg.com&nbsp;&nbsp;&middot;&nbsp;&nbsp;Effective 9 June 2026&nbsp;&nbsp;&middot;&nbsp;&nbsp;Last updated 9 June 2026</p>

    <p>These Terms of Use ("Terms") govern your access to and use of rawmktg.com (the "Site"), operated by Vinayak Ravi ("rawmktg.", "we", "us", or "our"). By accessing or using the Site, you agree to these Terms. If you do not agree, please do not use the Site.</p>

    <div class="legal-note">
      <strong>Not professional advice</strong>
      <p>The content on this Site is provided for general informational purposes only and does not constitute marketing, legal, financial, or other professional advice. Use it at your own discretion and verify before acting.</p>
    </div>

    <h2>1. Use of the Site</h2>
    <p>You may read, share, and reference our content for personal and professional purposes. You agree not to use the Site in any way that is unlawful, infringes the rights of others, or interferes with its operation or security.</p>

    <h2>2. About the content</h2>
    <p>rawmktg. publishes data-driven analysis of B2B search and AI visibility. Articles reflect our analysis and opinion at the time of writing. We strive for accuracy but make no guarantee that any finding, figure, or recommendation will apply to your specific situation or produce a particular result.</p>

    <h2>3. Data and third-party sources</h2>
    <p>Our analyses rely on third-party data sources, including Ahrefs, and on publicly available research, captured at a point in time. Such data can change, contain errors, or be interpreted differently. We present figures in good faith but do not warrant their accuracy, completeness, or currency. Brand names and trademarks referenced in our analyses belong to their respective owners and are used for identification and commentary only; their mention does not imply any affiliation or endorsement.</p>

    <h2>4. Intellectual property</h2>
    <p>Unless otherwise stated, the content, design, and original research on the Site are owned by rawmktg. and protected by applicable intellectual-property laws. You may quote or cite our work with clear attribution and a link back to the source page. You may not republish substantial portions, or present our research as your own, without permission.</p>

    <h2>5. Advertising</h2>
    <p>The Site displays third-party advertisements, including through Google AdSense. Ads are served by Google and other vendors, who may use cookies and similar technologies as described in our <a href="/privacy">Privacy Policy</a>. We do not endorse, and are not responsible for, the products or services featured in third-party ads.</p>

    <h2>6. External links</h2>
    <p>The Site contains links to third-party websites and tools for convenience and reference. We do not control and are not responsible for the content, accuracy, or practices of those sites. Following external links is at your own risk.</p>

    <h2>7. Disclaimers</h2>
    <p>The Site and its content are provided "as is" and "as available", without warranties of any kind, whether express or implied, including warranties of accuracy, fitness for a particular purpose, or non-infringement. We do not warrant that the Site will be uninterrupted, error-free, or secure.</p>

    <h2>8. Limitation of liability</h2>
    <p>To the maximum extent permitted by law, rawmktg. and Vinayak Ravi will not be liable for any indirect, incidental, consequential, or special damages arising from your use of, or inability to use, the Site or its content, including any decisions made in reliance on it.</p>

    <h2>9. Changes to these Terms</h2>
    <p>We may update these Terms from time to time. Material changes will be reflected in the "Last updated" date above. Your continued use of the Site after changes take effect constitutes acceptance of the revised Terms.</p>

    <h2>10. Contact</h2>
    <p>Questions about these Terms can be sent to <a href="mailto:vinayak@rawmktg.com">vinayak@rawmktg.com</a> or via our <a href="/contact">contact page</a>.</p>
  </div>
</main>'''

open("about.html","w",encoding="utf-8").write(page("About","About rawmktg. - data-driven teardowns of B2B search and AI visibility, the method behind them, and who writes them.","about",about_main))
open("contact.html","w",encoding="utf-8").write(page("Contact","Contact rawmktg. - email, social, and what to reach out about. We reply personally within 2 to 3 business days.","contact",contact_main))
open("terms.html","w",encoding="utf-8").write(page("Terms of Use","The terms governing use of rawmktg.com, including content, data sources, intellectual property, advertising, and disclaimers.","terms",terms_main))

# em dash / verify
for f in ("about.html","contact.html","terms.html"):
    h=open(f).read()
    print(f, "| em dashes:", h.count("—"), "| has nav:", "<nav" in h, "| has footer foot-links:", '/terms' in h, "| bytes:", len(h))
