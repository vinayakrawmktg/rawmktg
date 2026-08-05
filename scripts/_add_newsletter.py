#!/usr/bin/env python3
"""SCRATCH one-off: add the homepage newsletter section (+ its CSS) to every blog,
the glossary hub, and every glossary entry, just before <footer>. Idempotent.
Do NOT commit."""
import glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CSS = """    .newsletter-section{padding:56px 0 72px;border-top:1px solid var(--rule);}
    .newsletter-inner{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;}
    .newsletter-label{font-family:var(--f-mono);font-size:11px;font-weight:600;letter-spacing:0.20em;text-transform:uppercase;color:var(--signal);margin-bottom:14px;}
    .newsletter-title{font-family:var(--f-display);font-weight:700;font-size:28px;line-height:1.18;letter-spacing:-0.020em;color:var(--ink);margin-bottom:12px;}
    .newsletter-desc{font-family:var(--f-prose);font-size:14px;line-height:1.65;color:var(--mute);}
    .newsletter-form{display:flex;flex-direction:column;gap:12px;}
    .newsletter-form input[type="email"]{width:100%;padding:14px 16px;background:var(--paper-2);border:1px solid var(--rule-2);border-radius:6px;font-family:var(--f-prose);font-size:14px;color:var(--ink);outline:none;transition:border-color 0.15s;}
    .newsletter-form input[type="email"]::placeholder{color:var(--faint);}
    .newsletter-form input[type="email"]:focus{border-color:var(--signal);}
    .newsletter-form button{width:100%;padding:14px 24px;background:var(--ink);color:var(--paper);border:none;border-radius:6px;font-family:var(--f-mono);font-size:12px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;cursor:pointer;transition:background 0.15s;}
    .newsletter-form button:hover{background:var(--signal);}
    .newsletter-note{font-family:var(--f-mono);font-size:10px;letter-spacing:0.10em;text-transform:uppercase;color:var(--faint);}
    @media(max-width:768px){.newsletter-inner{grid-template-columns:1fr;gap:32px;}}
"""

HTML = """<section class="newsletter-section" id="newsletter" aria-label="Newsletter signup">
  <div class="page">
    <div class="newsletter-inner">
      <div>
        <div class="newsletter-label">Newsletter</div>
        <h2 class="newsletter-title">Get the next article in your inbox</h2>
        <p class="newsletter-desc">New articles on B2B SEO, GEO, and AI search visibility. No fluff, no cadence for the sake of it. When there's something worth saying.</p>
      </div>
      <form class="newsletter-form" name="newsletter" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="newsletter" />
        <p style="display:none"><input name="bot-field" /></p>
        <input type="email" name="email" placeholder="your@email.com" required aria-label="Email address" />
        <button type="submit">Subscribe &rarr;</button>
        <p class="newsletter-note">No spam. Unsubscribe any time.</p>
      </form>
    </div>
  </div>
</section>

"""

targets = sorted(glob.glob("blogs/*.html")) + ["glossary.html"] + sorted(glob.glob("glossary/*.html"))
done = 0; skipped = 0; problems = []
for path in targets:
    h = open(path, encoding="utf-8").read()
    if "newsletter-section" in h:
        skipped += 1; continue
    if ".newsletter-section{" not in h and "</style>" in h:
        h = h.replace("</style>", CSS + "  </style>", 1)
    # insert before the footer
    marker = '<footer class="site-foot"'
    if marker not in h:
        problems.append(path + ": no footer"); continue
    h = h.replace(marker, HTML + marker, 1)
    open(path, "w", encoding="utf-8").write(h)
    done += 1

print(f"added: {done} | already had it (skipped): {skipped} | problems: {problems or 'none'}")
em = sum(open(p, encoding="utf-8").read().count("—") for p in targets)
print("em dashes across targets:", em)
