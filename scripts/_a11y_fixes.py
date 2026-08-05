#!/usr/bin/env python3
"""SCRATCH one-off: accessibility fixes site-wide.
 1. Darken tokens for AA contrast: --mute #8A8278 -> #6B6459 (5.09:1),
    --signal #D04A2A -> #BC3F1D (4.73:1).
 2. Reassign readable --faint label classes to --mute (arrows/carets stay faint;
    they are aria-hidden so Lighthouse skips them).
 3. Enlarge footer touch targets (foot-cats / foot-links links).
 4. Add a <main> landmark to pages missing one (index + topics).
Idempotent. Do NOT commit."""
import glob, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

FILES = (["index.html", "privacy.html", "404.html", "glossary.html"]
         + sorted(glob.glob("topics/*.html"))
         + sorted(glob.glob("blogs/*.html"))
         + sorted(glob.glob("glossary/*.html")))

FAINT_TO_MUTE = ["cluster-num", "foot-col-label", "newsletter-note", "row-label", "topic-count"]

TOUCH_CSS = ("    .foot-cats{gap:2px;}.foot-cats a{display:inline-block;padding:6px 0;line-height:1.1;}"
             ".foot-links a{display:inline-block;padding:6px 0;}\n")

tok=faint=touch=mains=0
for p in FILES:
    if not os.path.exists(p):
        continue
    h = open(p, encoding="utf-8").read()
    orig = h

    # 1. tokens
    h = h.replace("--mute:#8A8278", "--mute:#6B6459")
    h = h.replace("--signal:#D04A2A", "--signal:#BC3F1D")
    if h != orig:
        tok += 1

    # 2. faint -> mute for readable labels (handles both ".x { ... }" and ".x{...}")
    for cls in FAINT_TO_MUTE:
        pat = re.compile(r'(\.' + re.escape(cls) + r'\b[^{}]*\{[^{}]*?)color:var\(--faint\)')
        h2 = pat.sub(lambda m: m.group(1) + "color:var(--mute)", h)
        if h2 != h:
            faint += 1
            h = h2

    # 3. touch targets (inject once)
    if ".foot-cats a{display:inline-block" not in h and "</style>" in h:
        h = h.replace("</style>", TOUCH_CSS + "  </style>", 1)
        touch += 1

    # 4. main landmark only where missing
    if "<main" not in h and "</nav>" in h and '<footer class="site-foot"' in h:
        h = h.replace("</nav>", '</nav>\n<main id="main">', 1)
        h = h.replace('<footer class="site-foot"', '</main>\n<footer class="site-foot"', 1)
        mains += 1

    if h != orig:
        open(p, "w", encoding="utf-8").write(h)

print(f"files token-darkened: {tok}")
print(f"faint->mute class swaps: {faint}")
print(f"touch-target CSS added: {touch}")
print(f"<main> added: {mains}")
# safety checks
old = sum(open(p).read().count("#D04A2A") + open(p).read().count("#8A8278") for p in FILES if os.path.exists(p))
print("remaining old hex (#D04A2A/#8A8278), expect 0:", old)
em = sum(open(p).read().count("—") for p in FILES if os.path.exists(p))
print("em dashes across files:", em)
multi = [p for p in FILES if os.path.exists(p) and open(p).read().count("<main") > 1]
print("files with >1 <main> (expect none):", multi or "none")
