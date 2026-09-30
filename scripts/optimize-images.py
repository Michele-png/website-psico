#!/usr/bin/env python3
"""Rigenera le versioni ottimizzate delle foto (WebP + JPEG ridimensionati + social card).

Uso (dalla root del repo):  python3 scripts/optimize-images.py
Richiede Pillow:            pip install pillow

Emma sostituisce le foto originali in assets/img/ mantenendo i nomi
(camelia.jpg, emma-portrait.jpg, camelia-small.jpg); poi si rilancia questo
script, che produce i file usati dalle pagine HTML:
  camelia-900.{webp,jpg}, camelia-450.{webp,jpg}
  emma-portrait-600.{webp,jpg}, emma-portrait-300.{webp,jpg}
  camelia-small-300.{webp,jpg}
  og-card.jpg (1200x630, anteprima per WhatsApp/Facebook/LinkedIn)
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")

JOBS = {
    "camelia.jpg": [(900, "camelia-900"), (450, "camelia-450")],
    "emma-portrait.jpg": [(600, "emma-portrait-600"), (300, "emma-portrait-300")],
    "camelia-small.jpg": [(300, "camelia-small-300")],
}

for src, outs in JOBS.items():
    im = Image.open(os.path.join(IMG, src)).convert("RGB")
    for w, name in outs:
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(os.path.join(IMG, name + ".webp"), "WEBP", quality=78, method=6)
        r.save(os.path.join(IMG, name + ".jpg"), "JPEG", quality=80, optimize=True, progressive=True)
        print(f"{name}: {w}x{h}")

# Social card 1200x630 dalla camelia (ritaglio centrale, terzo superiore)
im = Image.open(os.path.join(IMG, "camelia.jpg")).convert("RGB")
tw, th = 1200, 630
scale = max(tw / im.width, th / im.height)
r = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
left = (r.width - tw) // 2
top = (r.height - th) // 3
r.crop((left, top, left + tw, top + th)).save(os.path.join(IMG, "og-card.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
print("og-card.jpg: 1200x630")
