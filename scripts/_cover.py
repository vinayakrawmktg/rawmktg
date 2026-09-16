#!/usr/bin/env python3
"""Reusable on-brand rawmktg article cover generator (dark, Space Grotesk + JetBrains Mono)."""
import os, html, cairosvg
from PIL import Image
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
DISP="Space Grotesk Light"; MONO="JetBrains Mono"
BG="#0B0E13"; PANEL="#11151C"; INK="#F2EFE8"; MUTE="#8A9099"; SIG="#E85D2C"; FAINT="#3A4048"

def esc(t): return html.escape(t, quote=True)

def make_cover(slug, eyebrow, lines, stat, dot=True):
    W,H=2400,1260
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    # subtle grid
    for x in range(0,W,120): p.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#FFFFFF" stroke-opacity="0.02"/>')
    for y in range(0,H,120): p.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.02"/>')
    p.append(f'<rect x="0" y="{H-14}" width="{W}" height="14" fill="{SIG}"/>')
    # top bar: wordmark left, eyebrow right
    p.append(f'<circle cx="150" cy="132" r="13" fill="{SIG}"/>')
    p.append(f'<text x="182" y="146" font-family="{DISP}" font-weight="700" font-size="42" fill="{INK}">RawMktg<tspan fill="{SIG}">.</tspan></text>')
    p.append(f'<text x="{W-150}" y="142" text-anchor="end" font-family="{MONO}" font-weight="500" font-size="26" letter-spacing="6" fill="{MUTE}">{esc(eyebrow)}</text>')
    # eyebrow tag above title
    p.append(f'<text x="150" y="470" font-family="{MONO}" font-weight="700" font-size="30" letter-spacing="8" fill="{SIG}">{esc("▸  "+ (lines[0][1] if isinstance(lines[0],tuple) else ""))}</text>')
    return "\n".join(p)  # placeholder, replaced below

# We build the real SVG here (clearer than the stub above)
def cover_svg(eyebrow, kicker, title_lines, stat):
    W,H=2400,1260
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    for x in range(0,W+1,120): s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#FFFFFF" stroke-opacity="0.022"/>')
    for y in range(0,H+1,120): s.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.022"/>')
    # soft radial glow
    s.append(f'<defs><radialGradient id="g" cx="22%" cy="38%" r="70%"><stop offset="0%" stop-color="{SIG}" stop-opacity="0.10"/><stop offset="100%" stop-color="{SIG}" stop-opacity="0"/></radialGradient></defs>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#g)"/>')
    s.append(f'<rect x="0" y="{H-14}" width="{W}" height="14" fill="{SIG}"/>')
    # top bar
    s.append(f'<circle cx="152" cy="130" r="13" fill="{SIG}"/>')
    s.append(f'<text x="184" y="145" font-family="{DISP}" font-weight="700" font-size="44" letter-spacing="-1" fill="{INK}">RawMktg<tspan fill="{SIG}">.</tspan></text>')
    s.append(f'<text x="{W-152}" y="140" text-anchor="end" font-family="{MONO}" font-weight="500" font-size="26" letter-spacing="6" fill="{MUTE}">{esc(eyebrow)}</text>')
    # kicker (vector triangle marker + text; font glyphs like U+25B8 are unavailable)
    s.append(f'<polygon points="150,420 150,442 169,431" fill="{SIG}"/>')
    s.append(f'<text x="196" y="440" font-family="{MONO}" font-weight="700" font-size="30" letter-spacing="9" fill="{SIG}">{esc(kicker)}</text>')
    # title lines
    y=560
    for ln,accent in title_lines:
        t=f'<text x="146" y="{y}" font-family="{DISP}" font-weight="700" font-size="132" letter-spacing="-4" fill="{INK}">{esc(ln)}'
        if accent: t+=f'<tspan fill="{SIG}">{esc(accent)}</tspan>'
        t+='</text>'; s.append(t); y+=150
    # stat chips row near bottom
    s.append(f'<text x="150" y="{H-90}" font-family="{MONO}" font-weight="500" font-size="30" letter-spacing="2" fill="{MUTE}">{esc(stat)}</text>')
    s.append('</svg>')
    return "\n".join(s)

def render(slug, eyebrow, kicker, title_lines, stat):
    svg=cover_svg(eyebrow,kicker,title_lines,stat)
    base=f"assets/images/{slug}"
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f"/tmp/{slug}.png", output_width=2400, output_height=1260)
    im=Image.open(f"/tmp/{slug}.png").convert("RGB")
    im.save(f"{base}.webp","WEBP",quality=88,method=6)
    for w in [1600,1200,800]:
        im.resize((w,round(1260*w/2400)),Image.LANCZOS).save(f"{base}-{w}.webp","WEBP",quality=86,method=6)
    for w in [1000,700,400]:
        im.resize((w,round(525*w/1000)),Image.LANCZOS).save((f"{base}-card.webp" if w==1000 else f"{base}-card-{w}.webp"),"WEBP",quality=86,method=6)
    return f"{base}.webp"

if __name__=="__main__":
    out=render("ai-visibility-tools-compared",
        "The Buyer's Guide  ·  2026",
        "▸  AI VISIBILITY TOOLING",
        [("AI Visibility Tools,",None),("Compared",".")],
        "10 platforms  ·  $29–$499+/mo  ·  6+ answer engines tracked")
    print("wrote", out)
