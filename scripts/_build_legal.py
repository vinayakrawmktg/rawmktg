#!/usr/bin/env python3
"""SCRATCH: build refunds/pricing + refresh privacy/terms in the rawmktg legal shell. Do NOT commit as content."""
import os, re, glob
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
UP="/sessions/optimistic-youthful-planck/mnt/uploads/"

shell=open("privacy.html",encoding="utf-8").read()
PREFIX=shell[:shell.index('<span class="legal-eyebrow">')]
SUFFIX=shell[shell.rindex('</div>',0,shell.index('</main>')):]

PRICING_CSS=('  <style>\n'
 '    .legal .plans{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin:28px 0 14px;}\n'
 '    .legal .plan{border:1px solid var(--rule);border-radius:10px;padding:20px;background:var(--paper-2);}\n'
 '    .legal .plan h3{margin:0 0 6px;font-family:var(--f-display);font-weight:700;font-size:18px;color:var(--ink);}\n'
 '    .legal .plan .price{font-family:var(--f-display);font-weight:700;font-size:26px;color:var(--signal);margin:0 0 12px;line-height:1;}\n'
 '    .legal .plan .price span{font-size:13px;color:var(--mute);font-weight:500;}\n'
 '    .legal .plan ul{margin:0;padding-left:18px;}\n'
 '    .legal .plan li{font-size:13.5px;line-height:1.6;color:var(--ink-2);margin-bottom:4px;}\n'
 '  </style>\n</head>')

def clean(content):
    # strip uploaded h1 + updated line + trailing footer wrapper (shell supplies its own)
    content=re.sub(r'^\s*<h1>.*?</h1>\s*','',content,flags=re.S)
    content=re.sub(r'<p class="updated">.*?</p>\s*','',content,count=1,flags=re.S)
    m=re.search(r'<footer>(.*?)</footer>\s*$',content,flags=re.S)
    tail=''
    if m:
        inner=m.group(1).strip()
        content=content[:m.start()]
        tail='\n    <p class="legal-note">'+re.sub(r'\s+',' ',inner).replace('<p>','').replace('</p>','').strip()+'</p>'
    out=content.strip()+tail
    # real legal details
    out=out.replace('[DATE]','15 August 2026')
    out=out.replace('[LEGAL ENTITY NAME]','Sageo Consulting LLP')
    out=out.replace('[REGISTERED ADDRESS]','TB3, Sowparnika Ananda, Sompura Gate, Sarjapur Road, Bangalore 562125, Karnataka')
    out=out.replace('[COUNTRY]','India')
    out=out.replace('[JURISDICTION]','India')
    return out

def head(prefix,slug,title,desc,extra_css=False):
    p=prefix
    p=p.replace('<title>Privacy Policy · rawmktg.</title>',f'<title>{title} · rawmktg.</title>')
    p=re.sub(r'<meta name="description" content="[^"]*" />',f'<meta name="description" content="{desc}" />',p,count=1)
    p=p.replace('https://rawmktg.com/privacy',f'https://rawmktg.com/{slug}')
    p=p.replace('<meta property="og:title" content="Privacy Policy" />',f'<meta property="og:title" content="{title}" />')
    p=re.sub(r'<meta name="twitter:title" content="[^"]*" />',f'<meta name="twitter:title" content="{title}" />',p)
    if extra_css: p=p.replace('</head>',PRICING_CSS,1)
    return p

def build(slug,title,eyebrow,h1,meta,desc,src,extra_css=False):
    raw=re.search(r'<main>(.*?)</main>',open(UP+src,encoding="utf-8").read(),re.S).group(1)
    content=clean(raw)
    pre=head(PREFIX,slug,title,desc,extra_css)
    page=(pre+f'<span class="legal-eyebrow">{eyebrow}</span>\n    <h1>{h1}</h1>\n'
          f'    <p class="legal-meta">{meta}</p>\n    '+content+'\n  '+SUFFIX)
    open(f"{slug}.html","w",encoding="utf-8").write(page)
    left=page.count('[')
    return f"{slug}.html  {len(page)}b  placeholders_left:{left}  h1:{page.count('<h1')}  legal-inner:{page.count('legal-inner')}"

print(build("privacy","Privacy Policy","Legal","Privacy Policy",
  "rawmktg.com&nbsp;&nbsp;·&nbsp;&nbsp;Last updated 15 August 2026",
  "What data RawMktg collects, why, how long we keep it, and who processes it. Your rights and how to contact us about privacy.","privacy.html"))
print(build("terms","Terms of Service","Legal","Terms of Service",
  "rawmktg.com&nbsp;&nbsp;·&nbsp;&nbsp;Last updated 15 August 2026",
  "The terms governing your use of RawMktg: the service, your account, payment, acceptable use, liability and termination.","terms.html"))
print(build("refunds","Refund &amp; Cancellation Policy","Legal","Refund and Cancellation Policy",
  "rawmktg.com&nbsp;&nbsp;·&nbsp;&nbsp;Last updated 15 August 2026",
  "RawMktg cancellation and refund policy: cancel any time, a 14-day refund on a first subscription, processed by Paddle.","refunds.html"))
print(build("pricing","Pricing","Pricing","Pricing",
  "All prices in US dollars, billed monthly. Cancel at any time.",
  "RawMktg pricing: diagnose why AI assistants do not recommend your brand, and track your share of their answers. Plans from $99/month.","pricing.html",extra_css=True))
