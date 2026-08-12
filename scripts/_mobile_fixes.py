#!/usr/bin/env python3
"""Apply site-wide mobile-audit fixes: inject mobile-fixes CSS, 100vh->100dvh, aria-labels on tool inputs."""
import os, re, glob, html as H
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")

MOBILE_FIX = """<style id="mobile-fixes">
:root{--faint:#8B8578;}
.article-content,.article-content p,.article-content li,.article-content td,.faq-a,.faq-a p,.about-block p,.method p,.method li,.section-answer,.callout-box p,.card-desc,.tt td,.gloss-body,.gloss-body p,.entry-body,.entry-body p,.legal-inner,.legal-inner li,.legal-inner p{overflow-wrap:anywhere;word-break:break-word;}
.about-block a,.article-content a,.method a,.references a{overflow-wrap:anywhere;}
@media(max-width:768px){
  .foot-row{flex-direction:column;align-items:flex-start;gap:16px;}
  .foot-links{gap:18px!important;flex-wrap:wrap;}
  .foot-cats{gap:10px!important;flex-wrap:wrap;}
  .foot-links a,.foot-cats a,.nav-menu a{min-height:44px;display:inline-flex;align-items:center;}
  .method .srcs{gap:12px 20px!important;}
  .method .srcs a,.srcs a{padding:6px 0;display:inline-block;}
  .eyebrow-tag,.eyebrow-date,.chart-caption,.tt-label,.code-label,.toc-list a,.stat-label,.sidebar-label,.about-label,.card-topic,.newsletter-note,.pl-desc,.figcap,.o-eyebrow,.gaps-h,.lab,.sg-label,.article-data-note,.nav-links{font-size:12px!important;}
}
</style>
"""

def served_pages():
    files=[]
    files+=glob.glob("blogs/*.html")+glob.glob("tools/*.html")+glob.glob("topics/*.html")+glob.glob("glossary/*.html")
    for f in ["index.html","tools.html","topics.html","glossary.html","about.html","contact.html","terms.html","privacy.html","404.html","subscribed.html"]:
        if os.path.exists(f): files.append(f)
    return [f for f in files if '.preview.' not in f and not os.path.basename(f).startswith('google')]

def prettify(idv):
    s=re.sub(r'[_-]+',' ',idv); s=re.sub(r'([a-z])([A-Z])',r'\1 \2',s)
    return s.strip().capitalize()

def add_aria(h):
    # add aria-label to input/textarea missing it (skip hidden + already-labelled + newsletter email)
    def fix(m):
        tag=m.group(0)
        if 'aria-label' in tag or 'type="hidden"' in tag or 'name="email"' in tag or 'name="bot-field"' in tag:
            return tag
        # find label from placeholder or id
        ph=re.search(r'placeholder="([^"]+)"',tag)
        idv=re.search(r'id="([^"]+)"',tag)
        nm=re.search(r'name="([^"]+)"',tag)
        label = (ph.group(1) if ph else (prettify(idv.group(1)) if idv else (prettify(nm.group(1)) if nm else "Input")))
        label=H.escape(label,quote=True)
        return tag[:-1]+f' aria-label="{label}">' if tag.endswith('>') else tag
    h=re.sub(r'<input\b[^>]*>', fix, h)
    h=re.sub(r'<textarea\b[^>]*>', fix, h)
    return h

def process(f):
    h=open(f,encoding="utf-8").read(); orig=h
    # 1) inject mobile-fixes before </head>
    if 'id="mobile-fixes"' not in h and '</head>' in h:
        h=h.replace('</head>', '  '+MOBILE_FIX+'</head>', 1)
    # 2) 100vh -> dvh fallback
    if 'min-height:100vh' in h and 'min-height:100dvh' not in h:
        h=h.replace('min-height:100vh','min-height:100vh;min-height:100dvh')
    # 3) aria-labels (tools + any page with tool inputs / forms)
    if '<input' in h or '<textarea' in h:
        h=add_aria(h)
    if h!=orig:
        open(f,"w",encoding="utf-8").write(h); return True
    return False

if __name__=="__main__":
    n=0; pages=served_pages()
    for f in pages:
        if process(f): n+=1
    print(f"processed {n}/{len(pages)} served pages")
