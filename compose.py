#!/usr/bin/env python3
"""Compose entry.png for make.fun news-image-20261122.

A newspaper front page summing up Sunday 22 November 2026 in one image.
All text is rendered with PIL from system fonts (real vector text, never
AI-generated lettering). The lead illustration is a flat editorial scene
(assets/lead-illustration.png); the smaller panels are simple flat shapes
drawn in code. Rendered at 2x and downscaled for crisp antialiasing.

Usage: python3 compose.py  (writes entry.png next to this script)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2  # supersample factor
W, H = 1024, 1024

PAPER = (250, 246, 236)
INK = (18, 16, 14)
RED = (158, 27, 24)
GREY = (90, 86, 78)
RULE = (40, 36, 30)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w (1024 coords)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w * S or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    """Draw lines of text; y is the top. Returns y below the last line."""
    for ln in lines:
        draw.text((x * S, y * S), ln, font=fnt, fill=fill, anchor="la")
        y += leading
    return y


def rule(draw, x0, x1, y, width=1):
    draw.rectangle([x0 * S, y * S, x1 * S, (y + width) * S], fill=RULE)


def double_rule(draw, x0, x1, y):
    rule(draw, x0, x1, y, 3)
    rule(draw, x0, x1, y + 6, 1)


def main():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)
    MX = 30  # side margin
    CW = W - 2 * MX  # content width 964

    # ---------- Masthead ----------
    double_rule(d, MX, W - MX, 14)
    d.text((W * S / 2, 26 * S), "THE WORLD", font=font(SERIF_B, 84),
           fill=INK, anchor="ma")
    d.text((W * S / 2, 118 * S),
           "SUNDAY 22 NOVEMBER 2026  \u2022  ONE DAY IN ONE IMAGE",
           font=font(SANS_B, 25), fill=RED, anchor="ma")
    double_rule(d, MX, W - MX, 150)

    # ---------- Lead illustration ----------
    lead = Image.open(os.path.join(HERE, "assets", "lead-illustration.png"))
    # Crop the band with the burning tankers and warships (full width).
    lw, lh = lead.size
    crop = lead.crop((0, int(lh * 0.412), lw, int(lh * 0.723)))
    crop = crop.resize((964 * S, 200 * S), Image.LANCZOS)
    img.paste(crop, (MX * S, 162 * S))
    d.rectangle([MX * S, 162 * S, (W - MX) * S, 362 * S], outline=INK, width=2 * S)

    # ---------- Lead story ----------
    d.text((MX * S, 374 * S), "GULF CRISIS", font=font(SANS_B, 20), fill=RED, anchor="la")
    d.text((MX * S, 398 * S), "GULF IN FLAMES", font=font(SERIF_B, 56), fill=INK, anchor="la")
    d.text((MX * S, 462 * S),
           "Iran strikes US forces in Bahrain; tankers hit off Oman.",
           font=font(SERIF, 27), fill=INK, anchor="la")
    d.text((MX * S, 496 * S),
           "ADNOC vessel attacked in the Strait of Hormuz; one crew member missing.",
           font=font(SERIF_I, 22), fill=GREY, anchor="la")
    rule(d, MX, W - MX, 530, 2)

    # ---------- Row 2: two panels ----------
    col_w = (CW - 20) // 2  # 472 each
    row2_y = 544
    # --- Peru panel (left) ---
    px = MX
    d.rectangle([px * S, row2_y * S, (px + col_w) * S, (row2_y + 56) * S],
                fill=(214, 200, 178))
    d.polygon([(px * S, (row2_y + 56) * S),
               ((px + 110) * S, (row2_y + 8) * S),
               ((px + 220) * S, (row2_y + 56) * S)], fill=(122, 96, 66))
    d.polygon([((px + 150) * S, (row2_y + 56) * S),
               ((px + 300) * S, (row2_y + 2) * S),
               ((px + 430) * S, (row2_y + 56) * S)], fill=(96, 74, 52))
    d.polygon([((px + 96) * S, (row2_y + 19) * S),
               ((px + 110) * S, (row2_y + 8) * S),
               ((px + 124) * S, (row2_y + 19) * S),
               ((px + 110) * S, (row2_y + 14) * S)], fill=(250, 246, 236))
    d.polygon([((px + 282) * S, (row2_y + 15) * S),
               ((px + 300) * S, (row2_y + 2) * S),
               ((px + 318) * S, (row2_y + 15) * S),
               ((px + 300) * S, (row2_y + 9) * S)], fill=(250, 246, 236))
    for (x0, y0, x1, y1) in [(60, 34, 90, 46), (350, 26, 385, 40), (410, 16, 430, 28)]:
        d.line([((px + x0) * S, (row2_y + y0) * S),
                ((px + x1) * S, (row2_y + y1) * S)], fill=RED, width=3 * S)
    y = row2_y + 64
    y = draw_lines(d, ["STRONG QUAKE SHAKES", "PERU\u2019S ANDES"], px, y,
                   font(SERIF_B, 29), INK, 34)
    y += 2
    d.text((px * S, y * S), "Homes damaged, no deaths reported.",
           font=font(SERIF, 20), fill=INK, anchor="la")

    # --- Poland panel (right) ---
    qx = MX + col_w + 20
    d.rectangle([qx * S, row2_y * S, (qx + col_w) * S, (row2_y + 56) * S],
                fill=(38, 44, 62))
    for (x0, y0, x1, y1) in [(40, 6, 150, 50), (200, 4, 320, 52), (330, 10, 430, 46)]:
        d.line([((qx + x0) * S, (row2_y + y0) * S),
                ((qx + x1) * S, (row2_y + y1) * S)], fill=(255, 190, 90), width=3 * S)
        d.ellipse([((qx + x1 - 4) * S, (row2_y + y1 - 4) * S),
                   ((qx + x1 + 4) * S, (row2_y + y1 + 4) * S)], fill=(255, 220, 150))
    d.polygon([((qx + 20) * S, (row2_y + 56) * S),
               ((qx + 60) * S, (row2_y + 38) * S),
               ((qx + 100) * S, (row2_y + 56) * S)], fill=(20, 22, 30))
    y = row2_y + 64
    d.text((qx * S, y * S), "MISSILES FALL IN POLAND",
           font=font(SERIF_B, 29), fill=INK, anchor="la")
    y += 34
    d.text((qx * S, y * S), "Tusk calls it provocation",
           font=font(SERIF_B, 25), fill=RED, anchor="la")
    y += 32
    d.text((qx * S, y * S), "War spills across Ukraine\u2019s border.",
           font=font(SERIF, 20), fill=INK, anchor="la")

    rule(d, MX, W - MX, 712, 2)

    # ---------- Row 3: four panels ----------
    pw = (CW - 3 * 20) // 4  # 226 each
    row3_y = 726
    panels = [
        ("UK\u2013EU DEAL", "UK AND EU STRIKE DEAL",
         "Trade and youth mobility, ten years after Brexit.", "flags"),
        ("FBI HACK", "FBI PROBES HACK OF CRIME DATABASE",
         "National criminal database breached.", "db"),
        ("COP31", "CLIMATE TALKS DEADLOCKED",
         "Talks in overtime; fossil-fuel fight unresolved.", "globe"),
        ("MEXICO", "KINGPIN CAPTURED",
         "\u201cEl Chapo Isidro\u201d seized; 11 killed in Sinaloa violence.", "bars"),
    ]
    for i, (kick, head, sub, kind) in enumerate(panels):
        x = MX + i * (pw + 20)
        d.rectangle([x * S, row3_y * S, (x + pw) * S, (row3_y + 46) * S],
                    fill=(232, 224, 205))
        if kind == "flags":
            d.rectangle([(x + 14) * S, (row3_y + 10) * S, (x + 84) * S, (row3_y + 36) * S],
                        fill=(30, 60, 130))
            d.line([((x + 14) * S, (row3_y + 23) * S), ((x + 84) * S, (row3_y + 23) * S)],
                   fill=(255, 255, 255), width=6 * S)
            d.line([((x + 49) * S, (row3_y + 10) * S), ((x + 49) * S, (row3_y + 36) * S)],
                   fill=(255, 255, 255), width=6 * S)
            d.line([((x + 14) * S, (row3_y + 23) * S), ((x + 84) * S, (row3_y + 23) * S)],
                   fill=(180, 30, 30), width=3 * S)
            d.line([((x + 49) * S, (row3_y + 10) * S), ((x + 49) * S, (row3_y + 36) * S)],
                   fill=(180, 30, 30), width=3 * S)
            d.rectangle([(x + 140) * S, (row3_y + 10) * S, (x + 210) * S, (row3_y + 36) * S],
                        fill=(20, 50, 130))
            for k in range(8):
                a = math.pi * 2 * k / 8
                cx = (x + 175) + int(9 * math.cos(a))
                cy = (row3_y + 23) + int(9 * math.sin(a))
                d.ellipse([(cx - 1.5) * S, (cy - 1.5) * S, (cx + 1.5) * S, (cy + 1.5) * S],
                          fill=(255, 220, 60))
        elif kind == "db":
            d.ellipse([(x + 84) * S, (row3_y + 8) * S, (x + 142) * S, (row3_y + 20) * S],
                      fill=(70, 90, 120))
            d.rectangle([(x + 84) * S, (row3_y + 14) * S, (x + 142) * S, (row3_y + 38) * S],
                        fill=(50, 66, 92))
            d.ellipse([(x + 84) * S, (row3_y + 32) * S, (x + 142) * S, (row3_y + 44) * S],
                      fill=(70, 90, 120))
            d.line([((x + 84) * S, (row3_y + 26) * S), ((x + 142) * S, (row3_y + 26) * S)],
                   fill=(200, 210, 220), width=2 * S)
            d.polygon([((x + 168) * S, (row3_y + 36) * S),
                       ((x + 182) * S, (row3_y + 12) * S),
                       ((x + 196) * S, (row3_y + 36) * S)], fill=RED)
            d.text(((x + 182) * S, (row3_y + 22) * S), "!",
                   font=font(SANS_B, 16), fill=(255, 255, 255), anchor="ma")
        elif kind == "globe":
            d.ellipse([(x + 95) * S, (row3_y + 6) * S, (x + 129) * S, (row3_y + 40) * S],
                      fill=(90, 140, 90), outline=(40, 80, 40), width=2 * S)
            d.arc([(x + 95) * S, (row3_y + 6) * S, (x + 129) * S, (row3_y + 40) * S],
                  200, 340, fill=(60, 110, 60), width=2 * S)
            d.line([((x + 95) * S, (row3_y + 23) * S), ((x + 129) * S, (row3_y + 23) * S)],
                   fill=(60, 110, 60), width=2 * S)
            d.text(((x + 168) * S, (row3_y + 12) * S), "31",
                   font=font(SANS_B, 22), fill=RED, anchor="la")
        else:  # bars
            for k in range(5):
                bx = x + 76 + k * 16
                d.rectangle([bx * S, (row3_y + 8) * S, (bx + 6) * S, (row3_y + 38) * S],
                            fill=(60, 60, 66))
            d.rectangle([(x + 70) * S, (row3_y + 8) * S, (x + 156) * S, (row3_y + 12) * S],
                        fill=(60, 60, 66))
            d.rectangle([(x + 70) * S, (row3_y + 34) * S, (x + 156) * S, (row3_y + 38) * S],
                        fill=(60, 60, 66))
        y = row3_y + 54
        d.text((x * S, y * S), kick, font=font(SANS_B, 17), fill=RED, anchor="la")
        y += 24
        hf = font(SERIF_B, 21)
        y = draw_lines(d, wrap(d, head, hf, pw), x, y, hf, INK, 25)
        y += 3
        sf = font(SERIF, 17)
        draw_lines(d, wrap(d, sub, sf, pw), x, y, sf, INK, 20)

    # ---------- Footer ----------
    rule(d, MX, W - MX, 916, 2)
    fy = 926
    foot = [
        ("SPORT", "England 37\u201312 All Blacks \u2014 a record win"),
        ("INDIA", "Modi opens Nitish Setu bridge in Bihar \u00b7 Cyclone Akvan cancels 14 flights at Ranchi"),
        ("BUSINESS", "Anthropic shares fall after record $81.3bn IPO debut"),
    ]
    for label, text in foot:
        lf = font(SANS_B, 18)
        d.text((MX * S, fy * S), label, font=lf, fill=RED, anchor="la")
        lw = d.textlength(label, font=lf) / S
        d.text(((MX + lw + 12) * S, fy * S), text, font=font(SERIF, 19), fill=INK, anchor="la")
        fy += 26

    out = img.resize((W, H), Image.LANCZOS)
    out.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png", out.size)


if __name__ == "__main__":
    main()
