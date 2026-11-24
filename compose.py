#!/usr/bin/env python3
"""Compose the news poster for 24 November 2026 (make.fun news-image-20261124).

Draws a single 1024x1024 PNG with PIL only (no network, no external images):
a header dated 24 November 2026 and three story panels, each with a drawn
illustration and a short, sourced headline:

  1. North Korea threatens to close the Swiss diplomatic office in Pyongyang
     (KCNA statement via Kim Yo Jong; Yonhap 08:57, Korea Herald, Xinhua).
  2. SpaceX and Tesla appoint five directors to guide merger talks
     (Financial Times, reported by Reuters; Hindu BusinessLine).
  3. Solomon Islands scrap the 2022 China security pact, pivot to Australia
     (Sydney Morning Herald; ABC News Australia; Reuters).

Deterministic: same inputs always produce the same PNG bytes.
Usage: python3 compose.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

BG = (13, 25, 44)          # deep navy
PANEL = (23, 41, 63)       # panel navy
PANEL_EDGE = (58, 86, 120)
WHITE = (245, 247, 250)
MUTED = (168, 184, 204)
GOLD = (232, 184, 75)
RED = (214, 69, 69)
BLUE = (91, 155, 213)
TEAL = (63, 169, 138)
SCENE1 = (30, 46, 74)      # night blue
SCENE2 = (16, 34, 58)      # space blue
SCENE3 = (18, 58, 66)      # lagoon teal

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(d, y, accent, tag, headline, sub, scene_fn):
    """One story panel: illustration left (276px), text right."""
    x0, w, h = 24, 976, 262
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=18, fill=PANEL,
                        outline=PANEL_EDGE, width=2)
    # illustration area
    ix0, iy0, iw, ih = x0 + 14, y + 14, 252, h - 28
    d.rounded_rectangle([ix0, iy0, ix0 + iw, iy0 + ih], radius=12, fill=SCENE1)
    scene_fn(d, ix0, iy0, iw, ih)
    # accent bar + tag
    tx = x0 + 292
    d.rectangle([tx, y + 26, tx + 6, y + 26 + 34], fill=accent)
    d.text((tx + 20, y + 24), tag, font=font(FONT_BOLD, 24), fill=accent)
    # headline (max 2 lines, 36px bold)
    hf = font(FONT_BOLD, 36)
    lines = wrap(d, headline, hf, w - 292 - 40)
    ly = y + 66
    for ln in lines[:2]:
        d.text((tx, ly), ln, font=hf, fill=WHITE)
        ly += 44
    # sub (max 3 lines, 23px)
    sf = font(FONT_REG, 23)
    slines = wrap(d, sub, sf, w - 292 - 40)
    sy = ly + 8
    for ln in slines[:3]:
        d.text((tx, sy), ln, font=sf, fill=MUTED)
        sy += 31


# ---- scene 1: embassy building at night, Swiss flag, warning triangle ----
def scene_korea(d, x0, y0, w, h):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12, fill=SCENE1)
    # stars
    for sx, sy in [(30, 26), (90, 48), (150, 22), (210, 44), (60, 80), (190, 76)]:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2], fill=(200, 210, 225))
    # moon
    d.ellipse([x0 + w - 52, y0 + 18, x0 + w - 20, y0 + 50], fill=(235, 230, 200))
    # building
    bx0, by0, bx1, by1 = x0 + 28, y0 + 118, x0 + w - 28, y0 + h - 18
    d.rectangle([bx0, by0, bx1, by1], fill=(52, 72, 102))
    d.polygon([(bx0 - 8, by0), (x0 + w // 2, by0 - 34), (bx1 + 8, by0)], fill=(64, 88, 122))
    for i in range(5):
        cx = bx0 + 18 + i * 38
        d.rectangle([cx, by0 + 14, cx + 12, by1 - 8], fill=(120, 140, 170))
    d.rectangle([bx0, by1 - 8, bx1, by1], fill=(38, 54, 80))
    # flagpole + Swiss flag
    fx, fy = x0 + w - 62, y0 + 30
    d.line([fx, fy, fx, by0 - 6], fill=(200, 210, 225), width=4)
    d.rectangle([fx + 4, fy, fx + 44, fy + 34], fill=(200, 40, 40))
    d.rectangle([fx + 20, fy + 4, fx + 28, fy + 30], fill=WHITE)
    d.rectangle([fx + 8, fy + 13, fx + 40, fy + 21], fill=WHITE)
    # warning triangle
    tx, ty = x0 + 30, y0 + 30
    d.polygon([(tx, ty + 44), (tx + 26, ty), (tx + 52, ty + 44)], fill=(232, 184, 75))
    d.text((tx + 21, ty + 12), "!", font=font(FONT_BOLD, 26), fill=(20, 20, 20))


# ---- scene 2: rocket and car, dashed merger link ----
def scene_merger(d, x0, y0, w, h):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12, fill=SCENE2)
    for sx, sy in [(24, 30), (70, 60), (200, 26), (228, 70), (120, 40), (180, 96)]:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2], fill=(200, 210, 225))
    cx, cy = x0 + 78, y0 + 118   # rocket centre
    # flame
    d.polygon([(cx - 12, cy + 52), (cx, cy + 92), (cx + 12, cy + 52)], fill=(240, 140, 40))
    d.polygon([(cx - 6, cy + 52), (cx, cy + 74), (cx + 6, cy + 52)], fill=(250, 210, 90))
    # fins + body + nose
    d.polygon([(cx - 16, cy + 52), (cx - 34, cy + 66), (cx - 16, cy + 40)], fill=(180, 40, 40))
    d.polygon([(cx + 16, cy + 52), (cx + 34, cy + 66), (cx + 16, cy + 40)], fill=(180, 40, 40))
    d.rectangle([cx - 16, cy - 30, cx + 16, cy + 52], fill=(235, 238, 242))
    d.polygon([(cx - 16, cy - 30), (cx, cy - 62), (cx + 16, cy - 30)], fill=(200, 40, 40))
    d.ellipse([cx - 9, cy - 12, cx + 9, cy + 6], fill=(91, 155, 213), outline=(40, 60, 90), width=2)
    # dashed link to the car
    for i in range(6):
        d.line([x0 + 128 + i * 10, y0 + 150, x0 + 136 + i * 10, y0 + 150],
               fill=GOLD, width=3)
    # car (simple sleek silhouette)
    carx, cary = x0 + 148, y0 + 168
    d.polygon([(carx, cary + 22), (carx + 8, cary + 4), (carx + 34, cary),
               (carx + 62, cary + 2), (carx + 82, cary + 16), (carx + 88, cary + 22)],
              fill=(200, 210, 225))
    d.ellipse([carx + 14, cary + 18, carx + 30, cary + 34], fill=(20, 24, 32))
    d.ellipse([carx + 62, cary + 18, carx + 78, cary + 34], fill=(20, 24, 32))
    d.ellipse([carx + 18, cary + 22, carx + 26, cary + 30], fill=(120, 130, 145))
    d.ellipse([carx + 66, cary + 22, carx + 74, cary + 30], fill=(120, 130, 145))


# ---- scene 3: Pacific island, palm, sun and waves ----
def scene_island(d, x0, y0, w, h):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12, fill=SCENE3)
    # sun
    d.ellipse([x0 + w - 66, y0 + 20, x0 + w - 22, y0 + 64], fill=(250, 200, 90))
    # sea
    d.rectangle([x0, y0 + 150, x0 + w, y0 + h], fill=(28, 110, 140))
    for wy in (168, 190, 212):
        for wx in range(12, w - 12, 44):
            d.arc([x0 + wx, y0 + wy, x0 + wx + 34, y0 + wy + 18], 180, 360,
                  fill=(190, 225, 240), width=3)
    # island
    d.polygon([(x0 + 30, y0 + 168), (x0 + 90, y0 + 138), (x0 + 190, y0 + 138),
               (x0 + 226, y0 + 168)], fill=(214, 186, 130))
    # palm trunk + fronds (fan of arcs from the trunk top)
    d.line([x0 + 118, y0 + 142, x0 + 108, y0 + 78], fill=(120, 84, 50), width=7)
    tx, ty = x0 + 108, y0 + 78
    for (bx0, by0, bx1, by1, a0, a1) in [
        (tx - 52, ty - 34, tx + 8, ty + 6, 200, 330),
        (tx - 8, ty - 34, tx + 52, ty + 6, 210, 340),
        (tx - 40, ty - 52, tx + 40, ty - 4, 180, 360),
        (tx - 46, ty - 22, tx + 2, ty + 22, 150, 280),
        (tx - 2, ty - 22, tx + 46, ty + 22, 260, 30),
    ]:
        d.arc([bx0, by0, bx1, by1], a0, a1, fill=(70, 170, 110), width=5)
    d.ellipse([x0 + 96, y0 + 74, x0 + 106, y0 + 84], fill=(90, 60, 30))
    d.ellipse([x0 + 110, y0 + 78, x0 + 120, y0 + 88], fill=(90, 60, 30))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header
    d.text((W // 2, 26), "THE WORLD IN ONE IMAGE",
           font=font(FONT_BOLD, 26), fill=GOLD, anchor="ma")
    d.text((W // 2, 58), "24 NOVEMBER 2026",
           font=font(FONT_BOLD, 62), fill=WHITE, anchor="ma")
    d.line([W // 2 - 180, 138, W // 2 + 180, 138], fill=GOLD, width=3)
    d.text((W // 2, 146), "TUESDAY  •  THREE STORIES THAT DEFINED THE DAY",
           font=font(FONT_REG, 20), fill=MUTED, anchor="ma")

    draw_panel(d, 186, RED, "PYONGYANG",
               "North Korea threatens to shut Swiss office",
               "Kim Yo Jong warns Pyongyang may close the Swiss "
               "diplomatic office over sanctions on a children's camp.",
               scene_korea)
    draw_panel(d, 462, BLUE, "BUSINESS",
               "SpaceX and Tesla name merger negotiators",
               "Five directors appointed to guide talks on combining "
               "Musk's rocket and car companies.",
               scene_merger)
    draw_panel(d, 738, TEAL, "PACIFIC",
               "Solomon Islands scrap China security pact",
               "Honiara will end the 2022 deal and sign a new treaty "
               "with Australia instead.",
               scene_island)

    # footer sources
    d.text((W // 2, 1006), "Sources: Yonhap · Reuters / Financial Times · ABC News Australia — 24 Nov 2026",
           font=font(FONT_REG, 17), fill=MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
