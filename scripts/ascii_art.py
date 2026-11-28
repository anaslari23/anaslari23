#!/usr/bin/env python3
"""Generate the 3D wordmark and ASCII portrait used in README.md.

    python3 scripts/ascii_art.py wordmark "ANAS LARI"
    python3 scripts/ascii_art.py portrait [photo.jpg] [--cols 60]

Without a photo, `portrait` draws a stylised developer silhouette.
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


FONT = {
    "A": [" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
    "N": ["███╗   ██╗", "████╗  ██║", "██╔██╗ ██║", "██║╚██╗██║", "██║ ╚████║", "╚═╝  ╚═══╝"],
    "S": ["███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"],
    "L": ["██╗     ", "██║     ", "██║     ", "██║     ", "███████╗", "╚══════╝"],
    "R": ["██████╗ ", "██╔══██╗", "██████╔╝", "██╔══██╗", "██║  ██║", "╚═╝  ╚═╝"],
    "I": ["██╗", "██║", "██║", "██║", "██║", "╚═╝"],
    " ": ["   "] * 6,
}


def wordmark(text="ANAS LARI"):
    """3D block lettering (ANSI-Shadow style): solid faces + box-drawing extrusion."""
    rows = ["".join(FONT[c][i] for c in text.upper()) for i in range(6)]
    return "\n".join(r.rstrip() for r in rows)


def silhouette(n=600):
    """Lit, shaded developer bust drawn procedurally (no photo needed)."""
    c = n // 2
    img = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(img)
    d.ellipse((c - 230, n - 190, c + 230, n + 330), fill=95)
    d.polygon([(c - 60, n - 190), (c, n - 90), (c + 60, n - 190)], fill=200)
    d.rectangle((c - 55, 360, c + 55, 470), fill=130)
    d.ellipse((c - 125, 120, c + 125, 420), fill=215)
    d.pieslice((c - 140, 85, c + 140, 330), 180, 360, fill=40)
    d.polygon([(c - 140, 215), (c - 125, 215), (c - 125, 285), (c - 140, 260)], fill=40)
    d.polygon([(c + 140, 215), (c + 125, 215), (c + 125, 285), (c + 140, 260)], fill=40)
    for sx in (-1, 1):
        x0 = c + sx * 62
        d.rounded_rectangle((x0 - 42, 245, x0 + 42, 305), 14, outline=20, width=8)
        d.ellipse((x0 - 12, 265, x0 + 12, 289), fill=25)
    d.line((c - 20, 270, c + 20, 270), fill=20, width=8)
    d.line((c, 285, c - 10, 345, c + 12, 345), fill=150, width=6)
    d.arc((c - 55, 340, c + 55, 400), 25, 155, fill=60, width=7)
    img = img.filter(ImageFilter.GaussianBlur(5))
    light = Image.radial_gradient("L").resize((n, n)).point(lambda v: 255 - v)
    light = ImageChops.offset(light, -60, -50).point(lambda v: 110 + v * 145 // 255)
    lit = ImageChops.multiply(img, light).point(lambda v: min(255, v * 255 // 150))
    # ink map: features (hair, glasses, shadow) dense, lit skin sparse, backdrop empty
    return lit.point(lambda v: 0 if v < 12 else min(255, 40 + (255 - v) * 215 // 255))


def portrait(path=None, cols=56):
    img = Image.open(path).convert("L") if path else silhouette()
    img = ImageOps.fit(img, (cols, round(cols * 0.5)))
    if path:
        img = ImageOps.autocontrast(img, cutoff=2)
    ramp = " .,:;i1tfLCG08@"
    out = []
    for y in range(img.height):
        out.append("".join(ramp[img.getpixel((x, y)) * (len(ramp) - 1) // 255] for x in range(img.width)).rstrip())
    return "\n".join(out)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "wordmark":
        print(wordmark(a[1] if len(a) > 1 else "ANAS LARI"))
    elif a and a[0] == "portrait":
        cols = int(a[a.index("--cols") + 1]) if "--cols" in a else 56
        files = [x for x in a[1:] if not x.startswith("--") and not x.isdigit()]
        print(portrait(files[0] if files else None, cols))
    else:
        print(__doc__)
