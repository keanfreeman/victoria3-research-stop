#!/usr/bin/env python3
"""Draws mod/thumbnail.png (512x512) in the same style as Date Stop's:
dark backdrop, green medallion with a gold ring, gold lightbulb with pause bars,
EB Garamond title. Uses the game's own EB Garamond (OFL) from the Steam install."""
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

GAME = os.path.expanduser(
    os.environ.get("VIC3_DIR", "~/.local/share/Steam/steamapps/common/Victoria 3"))
FONTS = os.path.join(GAME, "game/fonts/EBGaramond")
OUT = os.path.join(os.path.dirname(__file__), "..", "mod", "thumbnail.png")

S = 4  # supersampling factor
W = 512 * S
GOLD = (214, 178, 112)
GOLD_LIGHT = (240, 214, 160)


def backdrop():
    img = Image.new("RGB", (W, W))
    d = ImageDraw.Draw(img)
    # Radial-ish vignette: lighter in the middle
    for r in range(W, 0, -8 * S):
        t = r / W
        c = int(14 + 26 * (1 - t))
        d.ellipse([W / 2 - r, W * 0.42 - r, W / 2 + r, W * 0.42 + r], fill=(c, c + 1, c + 2))
    return img.filter(ImageFilter.GaussianBlur(20 * S))


def medallion(img):
    cx, cy, r = W / 2, 206 * S, 128 * S
    # Shadow
    shadow = Image.new("L", (W, W), 0)
    ImageDraw.Draw(shadow).ellipse([cx - r, cy - r + 8 * S, cx + r, cy + r + 8 * S], fill=170)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14 * S))
    img.paste((0, 0, 0), mask=shadow)

    # Green face with horizontal brushed streaks
    face = Image.new("RGB", (W, W), (30, 58, 50))
    fd = ImageDraw.Draw(face)
    rng = random.Random(7)
    for _ in range(900):
        y = rng.uniform(cy - r, cy + r)
        x = rng.uniform(cx - r, cx + r)
        length = rng.uniform(20, 120) * S
        shade = rng.randint(-14, 14)
        fd.line([x, y, x + length, y + rng.uniform(-2, 2) * S],
                fill=(30 + shade, 58 + shade, 50 + shade), width=rng.randint(1, 3) * S)
    face = face.filter(ImageFilter.GaussianBlur(1.5 * S))
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(face, mask=mask)

    d = ImageDraw.Draw(img)
    # Inner shading ring and gold rim
    d.ellipse([cx - r + 8 * S, cy - r + 8 * S, cx + r - 8 * S, cy + r - 8 * S],
              outline=(20, 38, 33), width=6 * S)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=7 * S)
    d.ellipse([cx - r - 3 * S, cy - r - 3 * S, cx + r + 3 * S, cy + r + 3 * S],
              outline=(120, 92, 48), width=2 * S)
    return cx, cy


def bulb(img, cx, cy):
    d = ImageDraw.Draw(img)
    lw = 8 * S
    # Glass: an arc open at the bottom, then two lines tapering to the base
    gr = 48 * S
    gy = cy - 34 * S
    d.arc([cx - gr, gy - gr, cx + gr, gy + gr], start=128, end=52, fill=GOLD, width=lw)
    neck_bot = gy + gr + 26 * S
    neck_w = 21 * S
    for sx in (-1, 1):
        # Arc endpoint at 128 / 52 degrees, measured along the centre of the stroke
        ex = cx + sx * 0.616 * (gr - lw / 2)
        ey = gy + 0.788 * (gr - lw / 2)
        bx = cx + sx * neck_w
        d.line([ex, ey, bx, neck_bot], fill=GOLD, width=lw)
        for x, y in ((ex, ey), (bx, neck_bot)):
            d.ellipse([x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2], fill=GOLD)
    # Screw base
    for i in range(3):
        y = neck_bot + 8 * S + i * 13 * S
        w = 25 * S - i * 3 * S
        d.rounded_rectangle([cx - w, y, cx + w, y + 8 * S], radius=4 * S, fill=GOLD)
    tip_y = neck_bot + 8 * S + 3 * 13 * S
    d.chord([cx - 11 * S, tip_y - 10 * S, cx + 11 * S, tip_y + 10 * S], 0, 180, fill=GOLD)
    # Pause bars inside the glass
    bw, bh, gap = 11 * S, 38 * S, 8 * S
    for x0 in (cx - gap - bw, cx + gap):
        d.rounded_rectangle([x0, gy - bh / 2, x0 + bw, gy + bh / 2], radius=3 * S, fill=GOLD_LIGHT)


def text(img):
    d = ImageDraw.Draw(img)
    title = ImageFont.truetype(os.path.join(FONTS, "EBGaramond-Medium.ttf"), 76 * S)
    tag = ImageFont.truetype(os.path.join(FONTS, "EBGaramond-Italic.ttf"), 27 * S)
    d.text((W / 2, 410 * S), "Research Stop", font=title, fill=(232, 210, 160), anchor="ms")
    d.text((W / 2, 470 * S), "Pause before research goes to waste", font=tag,
           fill=(222, 200, 152), anchor="ms")


def main():
    if not os.path.isdir(FONTS):
        sys.exit(f"EB Garamond not found in {FONTS}; set VIC3_DIR to the game install")
    img = backdrop()
    cx, cy = medallion(img)
    bulb(img, cx, cy)
    text(img)
    img.resize((512, 512), Image.LANCZOS).save(OUT)
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
