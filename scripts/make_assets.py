#!/usr/bin/env python3
"""Render README header images: colour ASCII portrait + 3D wordmark (PNGs)."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

BG = (10, 15, 27)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"


def portrait(src, out, cols=150, cw=7, ch=13):
    img = Image.open(src).convert("RGB")
    rows = round(cols * cw / ch)
    img = img.resize((cols, rows), Image.LANCZOS)
    img = ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(1.35)).enhance(1.25)
    ramp = " .'`:;-~=+*xo#%&@"
    font = ImageFont.truetype(MONO, ch - 2)
    W, H = cols * cw, rows * ch
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for y in range(rows):
        for x in range(cols):
            r, g, b = img.getpixel((x, y))
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            c = ramp[int(min(1, lum ** 1.15) * (len(ramp) - 1))]
            if c != " ":
                # brighten: lift dark inks so shadows (headphones, laptop) stay visible
                m = max(r, g, b, 1)
                k = max(1.25, 170 / m)
                d.text((x * cw, y * ch), c, font=font, fill=(min(255, int(r * k) + 25), min(255, int(g * k) + 25), min(255, int(b * k) + 25)))
    im.save(out)


def wordmark(text, out, size=300, depth=34):
    font = ImageFont.truetype(SANS, size)
    l, t, r, b = font.getbbox(text)
    pad = 60
    W, H = r - l + pad * 2 + depth, b - t + pad * 2 + depth
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    pos = (pad - l, pad - t)
    # extrusion: stack shifted copies, dark -> lighter toward the face
    for i in range(depth, 0, -1):
        k = 1 - i / depth
        col = (int(30 + 60 * k), int(40 + 90 * k), int(110 + 120 * k))
        d.text((pos[0] + i, pos[1] + i), text, font=font, fill=col)
    # face with vertical gradient
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).text(pos, text, font=font, fill=255)
    grad = Image.new("RGB", (W, H))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        k = y / H
        gd.line((0, y, W, y), fill=(int(255 - 60 * k), int(230 - 40 * k), int(120 + 40 * k)))
    im.paste(grad, (0, 0), mask)
    # soft glow behind
    glow = Image.new("RGB", (W, H), BG)
    glow.paste((60, 100, 200), (0, 0), mask.filter(ImageFilter.GaussianBlur(30)).point(lambda v: v // 3))
    from PIL import ImageChops
    ImageChops.add(Image.new("RGB", (W, H), BG), glow)
    im.save(out)


if __name__ == "__main__":
    portrait(sys.argv[1], "assets/portrait.png")
    wordmark("ANAS LARI", "assets/wordmark.png")
