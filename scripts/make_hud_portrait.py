#!/usr/bin/env python3
"""HUD-style ASCII portrait: sparse '+' / '#' glyphs on a navy grid with ring arcs."""
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

BG = (10, 15, 27)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def build(src, out, n=96, cell=9, size=900):
    img = Image.open(src).convert("RGB")
    img = ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(1.3)).enhance(1.2)
    img = img.resize((n, n), Image.LANCZOS)
    S = size * 2  # supersample for smooth lines
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    for g in range(0, S, 80):  # faint grid
        d.line((g, 0, g, S), fill=(18, 26, 44), width=2)
        d.line((0, g, S, g), fill=(18, 26, 44), width=2)
    c = S // 2
    for r, w, col in ((int(S * 0.47), 3, (40, 52, 86)), (int(S * 0.455), 6, (95, 110, 175))):
        for a0 in (-80, 10, 100, 190):  # ring arcs with gaps
            d.arc((c - r, c - r, c + r, c + r), a0 + 12, a0 + 78, fill=col, width=w)
    font = ImageFont.truetype(MONO, int(cell * 2 * 1.05))
    ox = (S - n * cell * 2) // 2
    rad = n / 2 * 0.87
    for y in range(n):
        for x in range(n):
            if math.hypot(x - n / 2 + .5, y - n / 2 + .5) > rad:
                continue
            r, g, b = img.getpixel((x, y))
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            if lum > 0.58:
                ch, k = "+", 1.0
            elif lum > 0.27:
                ch, k = "#", 0.5
            else:
                continue
            k *= 1.0 if lum > 0.85 else 1.1
            col = tuple(min(255, int(v * k + (40 if ch == "+" else 0))) for v in (r, g, b))
            d.text((ox + x * cell * 2, ox + y * cell * 2), ch, font=font, fill=col)
    im.resize((size, size), Image.LANCZOS).save(out)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "assets/portrait.png")
