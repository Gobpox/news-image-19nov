#!/usr/bin/env python3
"""news-image-20261119 entry, v3: v2's page system untouched (same text, data,
layout, bars, strips, timeline, map, date check) with EVERY scene redrawn from
scratch: real national flags, a frontal summit table with three seated
leaders, the Peace Palace, a tilted COP31 draft, a candlestick IPO chart, and
card strips that each tell their story in four or more objects.
"""
import math
from PIL import Image, ImageDraw
import draw2
from draw2 import FR, PF, INK, RED, REGION_COLOR

W2 = draw2

def star(d, cx, cy, r, fill, rot=-90):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = math.radians(rot + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)

def flag(d, x, y, w, h, code):
    """A recognisable national flag in the rect (x, y, w, h)."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK)
    if code == "us":
        sh = h / 13
        for i in range(13):
            if i % 2 == 0:
                d.rectangle([x, y + i * sh, x + w, y + (i + 1) * sh], fill=(178, 34, 52))
        cw, ch = w * 0.44, sh * 7
        d.rectangle([x, y, x + cw, y + ch], fill=(30, 40, 110))
        for r in range(4):
            for c in range(5):
                sx = x + 4 + c * (cw - 7) / 4
                sy = y + 3.5 + r * (ch - 6) / 3
                d.ellipse([sx - 1.1, sy - 1.1, sx + 1.1, sy + 1.1], fill=(255, 255, 255))
    elif code == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        star(d, x + w * 0.17, y + h * 0.26, h * 0.17, (255, 222, 0))
        for i, a in enumerate([-50, -10, 30, 70]):
            sx = x + w * 0.33 + h * 0.10 * math.cos(math.radians(a + 180))
            sy = y + h * 0.26 + h * 0.16 * math.sin(math.radians(a))
            star(d, x + w * 0.335, y + h * (0.13 + i * 0.17), h * 0.055, (255, 222, 0))
    elif code == "ru":
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))
    elif code == "eu":
        d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        cx, cy = x + w / 2, y + h / 2
        for i in range(12):
            a = math.radians(i * 30 - 90)
            star(d, cx + h * 0.33 * math.cos(a), cy + h * 0.33 * math.sin(a), h * 0.075, (255, 204, 0))
    elif code == "uk":
        d.rectangle([x, y, x + w, y + h], fill=(1, 33, 105))
        d.line([x, y, x + w, y + h], fill=(255, 255, 255), width=max(2, int(h * 0.2)))
        d.line([x + w, y, x, y + h], fill=(255, 255, 255), width=max(2, int(h * 0.2)))
        d.line([x, y, x + w, y + h], fill=(200, 16, 46), width=max(1, int(h * 0.07)))
        d.line([x + w, y, x, y + h], fill=(200, 16, 46), width=max(1, int(h * 0.07)))
        d.rectangle([x + w * 0.38, y, x + w * 0.62, y + h], fill=(255, 255, 255))
        d.rectangle([x, y + h * 0.36, x + w, y + h * 0.64], fill=(255, 255, 255))
        d.rectangle([x + w * 0.44, y, x + w * 0.56, y + h], fill=(200, 16, 46))
        d.rectangle([x, y + h * 0.43, x + w, y + h * 0.57], fill=(200, 16, 46))
    elif code == "jp":
        d.ellipse([x + w / 2 - h * 0.3, y + h * 0.2, x + w / 2 + h * 0.3, y + h * 0.8], fill=(188, 0, 45))
    elif code == "ua":
        d.rectangle([x, y, x + w, y + h / 2], fill=(0, 91, 187))
        d.rectangle([x, y + h / 2, x + w, y + h], fill=(255, 213, 0))
    elif code == "ca":
        d.rectangle([x, y, x + w * 0.22, y + h], fill=(213, 0, 50))
        d.rectangle([x + w * 0.78, y, x + w, y + h], fill=(213, 0, 50))
        cx, cy = x + w / 2, y + h / 2
        d.polygon([(cx, cy - h * 0.26), (cx + h * 0.09, cy - h * 0.05), (cx + h * 0.24, cy - h * 0.1),
                   (cx + h * 0.13, cy + h * 0.06), (cx + h * 0.22, cy + h * 0.16), (cx + h * 0.05, cy + h * 0.13),
                   (cx + h * 0.04, cy + h * 0.27), (cx - h * 0.04, cy + h * 0.27), (cx - h * 0.05, cy + h * 0.13),
                   (cx - h * 0.22, cy + h * 0.16), (cx - h * 0.13, cy + h * 0.06), (cx - h * 0.24, cy - h * 0.1),
                   (cx - h * 0.09, cy - h * 0.05)], fill=(213, 0, 50))
    elif code == "in":
        d.rectangle([x, y, x + w, y + h / 3], fill=(255, 153, 51))
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(255, 255, 255))
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(19, 136, 8))
        cx, cy = x + w / 2, y + h / 2
        d.ellipse([cx - h * 0.11, cy - h * 0.11, cx + h * 0.11, cy + h * 0.11], outline=(0, 0, 128), width=1)
        d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=(0, 0, 128))
    elif code == "mm":  # Myanmar: yellow-green-red, big white star
        d.rectangle([x, y, x + w, y + h / 3], fill=(254, 203, 0))
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(52, 178, 65))
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(234, 40, 57))
        star(d, x + w / 2, y + h / 2, h * 0.3, (255, 255, 255))
    elif code == "gm":  # Gambia: red, white, blue, white, green
        d.rectangle([x, y, x + w, y + h], fill=(206, 17, 38))
        d.rectangle([x, y + h * 6 / 18, x + w, y + h * 7 / 18], fill=(255, 255, 255))
        d.rectangle([x, y + h * 7 / 18, x + w, y + h * 11 / 18], fill=(12, 28, 140))
        d.rectangle([x, y + h * 11 / 18, x + w, y + h * 12 / 18], fill=(255, 255, 255))
        d.rectangle([x, y + h * 12 / 18, x + w, y + h], fill=(28, 128, 60))
    elif code == "sa":
        d.rectangle([x, y, x + w, y + h], fill=(0, 84, 48))
        d.rectangle([x + w * 0.18, y + h * 0.34, x + w * 0.82, y + h * 0.46], fill=(255, 255, 255))
        d.line([x + w * 0.2, y + h * 0.66, x + w * 0.8, y + h * 0.66], fill=(255, 255, 255), width=2)
    elif code == "tr":
        d.rectangle([x, y, x + w, y + h], fill=(227, 10, 23))
        cx, cy = x + w * 0.42, y + h / 2
        d.ellipse([cx - h * 0.25, cy - h * 0.25, cx + h * 0.25, cy + h * 0.25], fill=(255, 255, 255))
        d.ellipse([cx - h * 0.19 + 2, cy - h * 0.2, cx + h * 0.31, cy + h * 0.2], fill=(227, 10, 23))
        star(d, x + w * 0.68, cy, h * 0.15, (255, 255, 255), rot=-90)

def figure(d, cx, top_y, skin, hair, style, suit, tie):
    """A seated leader: head with hair, suit, shirt, tie. top_y = head top."""
    r = 10
    cy = top_y + r
    # suit: shoulders trapezoid down to the table line
    d.polygon([(cx - 15, top_y + 46), (cx - 10, top_y + 24), (cx + 10, top_y + 24),
               (cx + 15, top_y + 46)], fill=suit)
    d.polygon([(cx - 4, top_y + 25), (cx + 4, top_y + 25), (cx, top_y + 34)], fill=(255, 255, 255))
    d.polygon([(cx - 1.6, top_y + 27), (cx + 1.6, top_y + 27), (cx + 1, top_y + 42),
               (cx - 1, top_y + 42)], fill=tie)
    d.ellipse([cx - 1.8, top_y + 25, cx + 1.8, top_y + 28.5], fill=tie)
    # head + hair
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin, outline=(120, 90, 70))
    if style == "blond":      # swept blond fringe
        d.chord([cx - r, cy - r, cx + r, cy + r - 3], start=180, end=345, fill=hair)
        d.polygon([(cx - r, cy - 2), (cx - r + 4, cy - 8), (cx - r + 5, cy + 1)], fill=hair)
    elif style == "black":    # neat black cap
        d.chord([cx - r, cy - r, cx + r, cy + r - 6], start=180, end=360, fill=hair)
    elif style == "grey":     # thinning grey, high forehead
        d.chord([cx - r + 1, cy - r, cx + r - 1, cy + r - 11], start=185, end=355, fill=hair)

def scene_summit3(d, b):
    x0, y0, x1, y1 = b
    # hall wall + banner + pillars
    for i in range(6):
        d.rectangle([x0, y0 + i * 20, x1, y0 + (i + 1) * 20], fill=(206 - i * 4, 182 - i * 4, 148 - i * 3))
    d.rectangle([x0, y0 + 3, x1, y0 + 19], fill=(120, 30, 30))
    d.text((x0 + 47, y0 + 6), "APEC 2026", font=FR(10, 800), fill=(250, 210, 120))
    for px in (x0 + 4, x1 - 14):
        d.rectangle([px, y0 + 22, px + 10, y0 + 88], fill=(226, 214, 190), outline=(150, 135, 105))
        d.rectangle([px - 2, y0 + 22, px + 12, y0 + 27], fill=(196, 178, 145), outline=(150, 135, 105))
    # three big true flags on poles behind the table: US, China, Russia
    centers = [x0 + 46, (x0 + x1) // 2, x1 - 46]
    for cx, code in zip(centers, ["us", "cn", "ru"]):
        d.line([cx, y0 + 24, cx, y0 + 88], fill=(90, 80, 70), width=2)
        d.ellipse([cx - 2, y0 + 22, cx + 2, y0 + 26], fill=(200, 170, 90))
        flag(d, cx - 24, y0 + 27, 48, 31, code)
        d.rectangle([cx + 21, y0 + 27, cx + 24, y0 + 58], fill=(168, 168, 168))  # fly-end shade
    # seated leaders
    figure(d, centers[0], y0 + 52, (240, 200, 165), (232, 190, 90), "blond", (35, 45, 75), (200, 40, 40))
    figure(d, centers[1], y0 + 52, (238, 205, 175), (25, 25, 30), "black", (25, 28, 38), (140, 30, 40))
    figure(d, centers[2], y0 + 52, (242, 205, 180), (178, 178, 184), "grey", (45, 50, 65), (40, 70, 150))
    # the long table, red cloth
    d.rectangle([x0 + 8, y0 + 86, x1 - 8, y0 + 106], fill=(150, 36, 34))
    d.rectangle([x0 + 8, y0 + 86, x1 - 8, y0 + 90], fill=(196, 70, 60))
    d.line([x0 + 8, y0 + 106, x1 - 8, y0 + 106], fill=(90, 20, 20), width=2)
    # name plates + microphones + papers
    for cx, name in zip(centers, ["TRUMP", "XI", "PUTIN"]):
        d.rectangle([cx - 20, y0 + 93, cx + 20, y0 + 104], fill=(252, 250, 244), outline=INK)
        tw = d.textlength(name, font=FR(8, 800))
        d.text((cx - tw / 2, y0 + 94.5), name, font=FR(8, 800), fill=INK)
        d.line([cx - 13, y0 + 86, cx - 17, y0 + 78], fill=(60, 60, 66), width=2)
        d.ellipse([cx - 19, y0 + 75, cx - 15, y0 + 79], fill=(60, 60, 66))
    d.rectangle([centers[0] + 24, y0 + 82, centers[0] + 38, y0 + 87], fill=(255, 255, 252), outline=(150, 150, 150))
    d.rectangle([centers[2] - 38, y0 + 82, centers[2] - 24, y0 + 87], fill=(255, 255, 252), outline=(150, 150, 150))
    # red carpet
    d.rectangle([x0, y0 + 108, x1, y1], fill=(140, 30, 30))
    d.line([x0 + 30, y1, x0 + 70, y0 + 108], fill=(170, 60, 55), width=1)
    d.line([x1 - 30, y1, x1 - 70, y0 + 108], fill=(170, 60, 55), width=1)

def scene_icj3(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    for i in range(6):
        d.rectangle([x0, y0 + i * 20, x1, y0 + (i + 1) * 20], fill=(203 - i * 2, 219 - i * 2, 233 - i * 1))
    for ex, ey in [(x0 + 34, y0 + 12), (x1 - 58, y0 + 8)]:
        d.ellipse([ex - 13, ey - 5, ex + 13, ey + 5], fill=(244, 247, 250))
        d.ellipse([ex + 6, ey - 7, ex + 20, ey + 3], fill=(244, 247, 250))
    # lawn + path
    d.rectangle([x0, y1 - 15, x1, y1], fill=(118, 158, 92))
    d.polygon([(cx - 12, y1), (cx + 12, y1), (cx + 6, y1 - 15), (cx - 6, y1 - 15)], fill=(216, 204, 175))
    # Peace Palace: brick wings, steep roofs, central clock tower
    brick, roof = (168, 96, 74), (70, 80, 95)
    d.rectangle([cx - 72, y0 + 52, cx - 18, y0 + 98], fill=brick, outline=INK)
    d.rectangle([cx + 18, y0 + 52, cx + 72, y0 + 98], fill=brick, outline=INK)
    d.polygon([(cx - 76, y0 + 52), (cx - 45, y0 + 34), (cx - 14, y0 + 52)], fill=roof, outline=INK)
    d.polygon([(cx + 14, y0 + 52), (cx + 45, y0 + 34), (cx + 76, y0 + 52)], fill=roof, outline=INK)
    for wx in (cx - 64, cx - 50, cx - 36, cx + 28, cx + 42, cx + 56):
        for wy in (y0 + 60, y0 + 76):
            d.rectangle([wx, wy, wx + 8, wy + 11], fill=(250, 240, 205), outline=(110, 70, 55))
    d.rectangle([cx - 15, y0 + 22, cx + 15, y0 + 98], fill=(176, 104, 80), outline=INK)
    d.polygon([(cx - 18, y0 + 22), (cx, y0 + 2), (cx + 18, y0 + 22)], fill=roof, outline=INK)
    d.ellipse([cx - 2, y0 - 1, cx + 2, y0 + 3], fill=(200, 170, 90))
    d.ellipse([cx - 8, y0 + 28, cx + 8, y0 + 44], fill=(255, 255, 250), outline=INK)
    d.line([cx, y0 + 36, cx, y0 + 30], fill=INK, width=2)
    d.line([cx, y0 + 36, cx + 5, y0 + 39], fill=INK, width=2)
    for wy in (y0 + 52, y0 + 66):
        d.rectangle([cx - 4, wy, cx + 4, wy + 9], fill=(250, 240, 205), outline=(110, 70, 55))
    d.pieslice([cx - 8, y0 + 82, cx + 8, y0 + 98], start=180, end=360, fill=(60, 44, 40), outline=INK)
    for i, sw in enumerate([46, 56, 66]):
        d.rectangle([cx - sw // 2, y0 + 98 + i * 3, cx + sw // 2, y0 + 101 + i * 3], fill=(226, 218, 200), outline=(150, 140, 120))
    # flagpoles: Gambia (applicant) and Myanmar (respondent)
    for px, code in [(x0 + 20, "gm"), (x1 - 50, "mm")]:
        d.line([px, y0 + 26, px, y0 + 100], fill=(90, 80, 70), width=2)
        flag(d, px + 2, y0 + 28, 30, 20, code)
    d.text((x0 + 8, y0 + 104), "PEACE PALACE", font=FR(7, 800), fill=(70, 90, 60))
    # the 9-6 scoreboard, bottom right on the lawn
    d.rectangle([x1 - 64, y0 + 86, x1 - 6, y0 + 112], fill=(18, 30, 58), outline=(250, 205, 60), width=2)
    d.text((x1 - 58, y0 + 89), "VOTE", font=FR(7, 800), fill=(250, 205, 60))
    tw = d.textlength("9\u20136", font=FR(17, 800))
    d.text((x1 - 35 - tw / 2, y0 + 96), "9\u20136", font=FR(17, 800), fill=(255, 255, 255))
    # scales of justice, small, bottom left
    sx, sy = x0 + 26, y0 + 96
    d.line([sx, sy - 10, sx, sy + 6], fill=(150, 120, 40), width=2)
    d.line([sx - 9, sy - 8, sx + 9, sy - 8], fill=(150, 120, 40), width=2)
    d.polygon([(sx - 12, sy), (sx - 5, sy), (sx - 8.5, sy - 7)], fill=(200, 170, 90), outline=(120, 95, 30))
    d.polygon([(sx + 5, sy), (sx + 12, sy), (sx + 8.5, sy - 7)], fill=(200, 170, 90), outline=(120, 95, 30))
    d.rectangle([sx - 6, sy + 6, sx + 6, sy + 8], fill=(150, 120, 40))

def scene_doc3(d, b):
    """COP31: the draft deal on a tilted page, fossil lines struck, CUT stamp,
    a thermometer rising at the side."""
    x0, y0, x1, y1 = b
    for i in range(6):
        d.rectangle([x0, y0 + i * 20, x1, y0 + (i + 1) * 20], fill=(186 - i * 5, 216 - i * 4, 206 - i * 3))
    # the tilted page, drawn on its own layer
    layer = Image.new("RGBA", (250, 140), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([26, 14, 196, 130], fill=(0, 0, 0, 60))
    ld.rectangle([20, 8, 190, 124], fill=(255, 255, 250, 255), outline=(22, 28, 38, 255))
    ld.rectangle([24, 12, 186, 27], fill=(22, 28, 38, 255))
    ld.text((30, 15), "DRAFT \u2014 19 NOV", font=FR(10, 800), fill=(255, 255, 255, 255))
    ld.text((30, 31), "COP31 \u00b7 ANTALYA \u00b7 REVISED TEXT", font=FR(7, 700), fill=(120, 124, 130, 255))
    for i, lw in enumerate([140, 152, 128]):
        ld.line([30, 44 + i * 8, 30 + lw, 44 + i * 8], fill=(175, 177, 168, 255), width=2)
    ld.text((30, 66), "FOSSIL FUELS", font=FR(17, 800), fill=(22, 28, 38, 255))
    ld.line([28, 75, 138, 75], fill=(200, 40, 35, 255), width=4)
    ld.text((30, 84), "$120BN ADAPTATION AID", font=FR(11, 800), fill=(22, 28, 38, 255))
    ld.line([28, 92, 158, 92], fill=(200, 40, 35, 255), width=4)
    for i, lw in enumerate([148, 118]):
        ld.line([30, 102 + i * 8, 30 + lw, 102 + i * 8], fill=(175, 177, 168, 255), width=2)
    ld.text((30, 114), "TEXT CUT: 144 TO 80 PAGES", font=FR(7, 800), fill=(200, 40, 35, 255))
    layer = layer.rotate(4, expand=True, resample=Image.BILINEAR)
    d._pil.paste(layer, (x0 - 8, y0 - 6), layer)
    # CUT stamp over the page's right edge
    W2.stamp(d, x1 - 52, y0 + 46, "CUT", angle=16, size=18)
    # thermometer at the side: tube, red column, bulb, ticks
    tx = x1 - 22
    d.rectangle([tx - 3, y0 + 34, tx + 3, y0 + 94], fill=(255, 255, 252), outline=INK)
    d.rectangle([tx - 1.5, y0 + 52, tx + 1.5, y0 + 94], fill=RED)
    d.ellipse([tx - 6, y0 + 90, tx + 6, y0 + 102], fill=RED, outline=INK)
    for ty in (y0 + 42, y0 + 56, y0 + 70, y0 + 84):
        d.line([tx + 4, ty, tx + 8, ty], fill=INK, width=1)
    d.text((tx - 12, y0 + 106), "HOTTER", font=FR(7, 800), fill=RED)

def scene_ipo3(d, b):
    """Anthropic's first day: exchange building + candlesticks $83 to $97.17."""
    x0, y0, x1, y1 = b
    for i in range(6):
        d.rectangle([x0, y0 + i * 20, x1, y0 + (i + 1) * 20], fill=(15 + i, 23 + i * 2, 45 + i * 3))
    # exchange building, left
    d.polygon([(x0 + 6, y0 + 26), (x0 + 30, y0 + 12), (x0 + 54, y0 + 26)], fill=(52, 70, 110), outline=(110, 135, 185))
    for i in range(3):
        d.rectangle([x0 + 12 + i * 15, y0 + 28, x0 + 18 + i * 15, y0 + 62], fill=(52, 70, 110), outline=(110, 135, 185))
    d.rectangle([x0 + 6, y0 + 62, x0 + 54, y0 + 68], fill=(52, 70, 110), outline=(110, 135, 185))
    d.rectangle([x0 + 6, y0 + 68, x0 + 54, y0 + 78], fill=(30, 44, 80), outline=(110, 135, 185))
    tw = d.textlength("NASDAQ", font=FR(8, 800))
    d.text((x0 + 30 - tw / 2, y0 + 70), "NASDAQ", font=FR(8, 800), fill=(250, 205, 60))
    d.text((x0 + 8, y0 + 84), "ANT", font=FR(15, 800), fill=(255, 255, 255))
    # price gridlines: $83 low, $97.17 high
    for gy in (y0 + 88, y0 + 30):
        for gx in range(x0 + 66, x1 - 8, 9):
            d.line([gx, gy, gx + 4, gy], fill=(90, 105, 140), width=1)
    d.text((x1 - 34, y0 + 74), "$83", font=FR(8, 800), fill=(170, 180, 200))
    d.text((x0 + 110, y0 + 34), "$97.17", font=FR(8, 800), fill=(250, 205, 60))
    # candlesticks rising, one red fade in the middle
    candles = [  # (body_top, body_bottom, up?)
        (76, 88, True), (66, 78, True), (58, 70, True), (56, 64, False),
        (46, 58, True), (32, 46, True),
    ]
    for i, (t, bt, up) in enumerate(candles):
        cx = x0 + 76 + i * 24
        col = (52, 199, 123) if up else (224, 80, 80)
        d.line([cx, y0 + t - 6, cx, y0 + bt + 6], fill=col, width=2)
        d.rectangle([cx - 6, y0 + t, cx + 6, y0 + bt], fill=col, outline=(10, 16, 30))
    # the +17% arrow over the candles
    for t in range(21):
        ax = x0 + 74 + t * (118 / 20)
        ay = y0 + 74 - t * (44 / 20) - 6 * math.sin(t / 20 * math.pi)
        d.ellipse([ax - 1.6, ay - 1.6, ax + 1.6, ay + 1.6], fill=(250, 205, 60))
    d.polygon([(x0 + 192, y0 + 22), (x0 + 200, y0 + 30), (x0 + 188, y0 + 32)], fill=(250, 205, 60))
    d.rectangle([x0 + 62, y0 + 6, x0 + 108, y0 + 22], fill=(52, 199, 123), outline=(10, 16, 30))
    d.text((x0 + 69, y0 + 9), "+17%", font=FR(11, 800), fill=(8, 24, 18))
    # ticker tape along the bottom
    d.rectangle([x0 + 62, y0 + 100, x1 - 6, y0 + 112], fill=(10, 16, 34), outline=(90, 105, 140))
    d.text((x0 + 68, y0 + 102), "FIRST DAY \u00b7 BIGGEST IPO EVER \u00b7 RAISED $81.3BN", font=FR(7, 800), fill=(250, 205, 60))

# ---------------- card strips (each tells its story, 4+ objects) -------------
def tag3(d, x, y, text, fill=(255, 255, 255), bg=INK, size=7):
    f = FR(size, 800)
    w = d.textlength(text, font=f)
    d.rectangle([x, y, x + w + 6, y + size + 5], fill=bg)
    d.text((x + 3, y + 2), text, font=f, fill=fill)

def cs_gtawide(d, b):
    x0, y0, x1, y1 = b
    h = y1 - y0
    for i in range(6):
        d.rectangle([x0, y0 + i * (h // 6 + 1), x1, y0 + (i + 1) * (h // 6 + 1)],
                    fill=(110 + i * 20, 40 + i * 17, 130 + i * 11))
    d.ellipse([x0 + 26, y0 + 5, x0 + 52, y0 + 27], fill=(255, 214, 120))
    for bx, bw, bh in [(x0 + 84, 15, 20), (x0 + 105, 11, 26), (x0 + 122, 18, 16),
                       (x1 - 118, 15, 22), (x1 - 97, 11, 27), (x1 - 80, 18, 17)]:
        d.rectangle([bx, y1 - 8 - bh, bx + bw, y1 - 8], fill=(36, 19, 52))
        for wy in range(y1 - 8 - bh + 3, y1 - 11, 6):
            d.rectangle([bx + 3, wy, bx + 6, wy + 3], fill=(255, 205, 105))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(28, 15, 38))
    for gx in range(x0 + 12, x1 - 10, 26):
        d.line([gx, y1 - 4, gx + 12, y1 - 4], fill=(250, 205, 60), width=1)
    for px in (x0 + 66, x1 - 58):  # palms
        d.line([px, y1 - 8, px + 2, y0 + 8], fill=(24, 50, 26), width=2)
        for a in (200, 245, 290, 335, 160):
            d.line([px + 2, y0 + 8, px + 2 + 11 * math.cos(math.radians(a)),
                    y0 + 8 + 7 * math.sin(math.radians(a))], fill=(30, 95, 52), width=2)
    d.polygon([(x0 + 158, y1 - 8), (x0 + 172, y1 - 17), (x0 + 208, y1 - 17), (x0 + 224, y1 - 8)],
              fill=(216, 42, 92), outline=(255, 255, 255))
    d.rectangle([x0 + 206, y1 - 20, x0 + 222, y1 - 17], fill=(216, 42, 92), outline=(255, 255, 255))
    d.ellipse([x0 + 168, y1 - 7, x0 + 175, y1 - 1], fill=INK)
    d.ellipse([x0 + 202, y1 - 7, x0 + 209, y1 - 1], fill=INK)
    d.rectangle([x1 - 56, y0 + 4, x1 - 12, y0 + 23], fill=(24, 10, 34), outline=(255, 120, 190))
    d.text((x1 - 45, y0 + 7), "VI", font=FR(13, 800), fill=(255, 120, 190))

def cs_cyclone(d, b):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle(b, fill=(170, 200, 222))
    d.polygon([(x0, y0), (x0 + 52, y0), (x0 + 40, cy), (x0 + 56, y1), (x0, y1)], fill=(216, 196, 148), outline=(150, 130, 90))
    for hx in (x0 + 10, x0 + 26):
        d.rectangle([hx, y1 - 14, hx + 11, y1 - 6], fill=(240, 236, 222), outline=INK)
        d.polygon([(hx - 2, y1 - 14), (hx + 5, y1 - 19), (hx + 13, y1 - 14)], fill=RED)
    for r, a0 in [(14, 20), (9, 150), (4.5, 280)]:
        d.arc([cx + 22 - r, cy - r * 0.8, cx + 22 + r, cy + r * 0.8], start=a0, end=a0 + 250,
              fill=(250, 250, 250), width=3)
    d.ellipse([cx + 19, cy - 3, cx + 25, cy + 3], fill=(60, 90, 130))
    d.arc([x0 + 44, y0 + 4, x0 + 96, y0 + 30], start=200, end=320, fill=RED, width=2)
    d.polygon([(x0 + 90, y0 + 7), (x0 + 99, y0 + 9), (x0 + 92, y0 + 14)], fill=RED)
    tag3(d, x0 + 4, y0 + 3, "ODISHA")

def cs_tanks(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(216, 208, 188))
    d.line([x0 + 4, y1 - 5, x1 - 4, y1 - 5], fill=INK, width=1)
    for tx in (x0 + 14, x0 + 62):
        d.rectangle([tx, y1 - 15, tx + 32, y1 - 6], fill=(96, 104, 84), outline=INK)
        d.rectangle([tx + 9, y1 - 21, tx + 23, y1 - 15], fill=(96, 104, 84), outline=INK)
        d.line([tx + 23, y1 - 18, tx + 38, y1 - 18], fill=INK, width=3)
        for wx in range(tx + 3, tx + 30, 7):
            d.ellipse([wx, y1 - 6, wx + 5, y1 - 2], fill=(60, 64, 56))
    d.polygon([(x1 - 36, y1 - 5), (x1 - 36, y0 + 8), (x1 - 24, y0 + 13), (x1 - 16, y0 + 6),
               (x1 - 8, y0 + 12), (x1 - 8, y1 - 5)], fill=(196, 188, 168), outline=INK)
    d.line([x1 - 24, y0 + 14, x1 - 18, y1 - 12], fill=(120, 112, 96), width=1)
    for sx, sy, r in [(x1 - 30, y0 + 3, 5), (x1 - 20, y0 + 2, 7)]:
        d.ellipse([sx - r, sy - r * 0.6, sx + r, sy + r * 0.6], fill=(120, 124, 130))
    tag3(d, x0 + 96, y0 + 3, "NUSEIRAT")

def cs_riyadh(d, b):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle(b, fill=(26, 32, 58))
    for sx, sy in [(x0 + 16, y0 + 5), (x0 + 60, y0 + 8), (x1 - 24, y0 + 5), (x1 - 70, y0 + 3)]:
        d.ellipse([sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2], fill=(230, 236, 245))
    for bx, bw, bh in [(x0 + 6, 16, 12), (x0 + 28, 12, 17), (x1 - 40, 14, 14), (x1 - 20, 12, 10)]:
        d.rectangle([bx, y1 - 4 - bh, bx + bw, y1 - 4], fill=(52, 64, 96), outline=(96, 116, 160))
        d.rectangle([bx + 3, y1 - 4 - bh + 3, bx + 6, y1 - 8], fill=(255, 220, 130))
    d.rectangle([cx - 5, y0 + 6, cx + 5, y1 - 4], fill=(90, 110, 150), outline=(200, 210, 230))
    d.polygon([(cx - 5, y0 + 6), (cx, y0 + 1), (cx + 5, y0 + 6)], fill=(120, 140, 180))
    for gx in range(x1 - 66, x1 - 30, 8):
        d.line([gx, y0 + 7, gx + 4, y0 + 7], fill=(235, 150, 90), width=1)
    d.polygon([(x1 - 30, y0 + 4), (x1 - 16, y0 + 8), (x1 - 29, y0 + 12)], fill=(240, 240, 245), outline=INK)
    d.polygon([(x1 - 32, y0 + 8), (x1 - 40, y0 + 11), (x1 - 31, y0 + 13)], fill=(250, 140, 60))
    ex, ey = x0 + 44, y0 + 10
    for a in range(0, 360, 45):
        d.line([ex, ey, ex + 8 * math.cos(math.radians(a)), ey + 8 * math.sin(math.radians(a))],
               fill=(250, 210, 90), width=2)
    d.arc([x0 + 8, y0 + 12, x0 + 52, y1 + 8], start=290, end=350, fill=(120, 220, 160), width=2)
    tag3(d, x0 + 100, y1 - 12, "RIYADH")

def cs_kerch(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.rectangle(b, fill=(200, 214, 230))
    d.rectangle([x0, y1 - 9, x1, y1], fill=(84, 138, 178))
    for wx in range(x0 + 8, x1 - 12, 24):
        d.arc([wx, y1 - 7, wx + 13, y1 - 2], start=200, end=340, fill=(200, 230, 250), width=1)
    d.line([x0 + 2, y0 + 12, cx - 8, y0 + 12], fill=INK, width=3)
    d.line([cx + 14, y0 + 12, x1 - 2, y0 + 12], fill=INK, width=3)
    for px in (x0 + 22, x0 + 58, x1 - 58, x1 - 22):
        d.line([px, y0 + 12, px, y0 + 24], fill=INK, width=2)
    d.polygon([(cx - 8, y0 + 12), (cx + 14, y0 + 12), (cx + 20, y1 - 7), (cx + 4, y1 - 7)],
              fill=(150, 60, 50), outline=INK)
    for sx, sy, r in [(cx + 2, y0 + 5, 5), (cx + 12, y0 + 3, 7)]:
        d.ellipse([sx - r, sy - r * 0.6, sx + r, sy + r * 0.6], fill=(120, 124, 130))
    for wx in (cx + 12, cx + 22):
        d.arc([wx, y1 - 10, wx + 10, y1 - 4], start=180, end=330, fill=(255, 255, 255), width=2)
    tag3(d, x1 - 40, y0 + 2, "KERCH")

def cs_florida(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.rectangle(b, fill=(150, 190, 220))
    for rx in range(x0 + 8, x1 - 6, 17):
        d.line([rx, y0 + 2, rx - 3, y0 + 9], fill=(90, 130, 170), width=1)
    for hx, hw in [(x0 + 8, 24), (x0 + 42, 28), (x1 - 40, 26)]:
        d.rectangle([hx, y0 + 9, hx + hw, y0 + 23], fill=(240, 236, 222), outline=INK)
        d.polygon([(hx - 2, y0 + 9), (hx + hw // 2, y0 + 3), (hx + hw + 2, y0 + 9)], fill=RED)
    d.rectangle([x0, y0 + 21, x1, y1], fill=(60, 110, 160))
    for wx in range(x0 + 4, x1 - 10, 18):
        d.arc([wx, y0 + 23, wx + 12, y0 + 29], start=200, end=340, fill=(200, 230, 250), width=2)
    d.polygon([(cx - 6, y1 - 4), (cx, y0 + 19), (cx + 6, y1 - 4)], fill=(230, 120, 40), outline=INK)
    tag3(d, x0 + 6, y1 - 12, "15 IN", bg=RED)

def cs_vangogh(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.rectangle(b, fill=(250, 232, 190))
    d.rectangle([x0 + 22, y0 + 3, x0 + 84, y1 - 3], fill=(176, 132, 52), outline=(120, 88, 30))
    d.rectangle([x0 + 26, y0 + 6, x0 + 80, y1 - 6], fill=(30, 40, 90))
    for sx, sy in [(x0 + 36, y0 + 11), (x0 + 56, y0 + 9), (x0 + 68, y0 + 15)]:
        d.ellipse([sx - 3.4, sy - 3.4, sx + 3.4, sy + 3.4], fill=(250, 205, 60))
        d.ellipse([sx - 1.4, sy - 1.4, sx + 1.4, sy + 1.4], fill=(255, 240, 190))
    d.polygon([(x0 + 26, y1 - 6), (x0 + 44, y0 + 17), (x0 + 62, y1 - 6)], fill=(70, 130, 70))
    d.polygon([(x0 + 48, y1 - 6), (x0 + 64, y0 + 19), (x0 + 80, y1 - 6)], fill=(90, 150, 80))
    d.line([x0 + 84, y0 + 8, x0 + 96, y0 + 5], fill=(120, 100, 70), width=1)
    d.rectangle([x0 + 96, y0 + 3, x1 - 6, y0 + 16], fill=(255, 255, 252), outline=INK)
    d.text((x0 + 100, y0 + 6), "$190.4m", font=FR(8, 800), fill=RED)
    d.rectangle([x0 + 104, y1 - 10, x0 + 118, y1 - 7], fill=(94, 64, 48))
    d.line([x0 + 110, y1 - 7, x0 + 118, y1 - 2], fill=(94, 64, 48), width=3)

def cs_chart(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(224, 236, 224))
    d.polygon([(x0 + 6, y0 + 10), (x0 + 18, y0 + 3), (x0 + 30, y0 + 10)], fill=(90, 104, 120), outline=INK)
    for i in range(2):
        d.rectangle([x0 + 10 + i * 10, y0 + 11, x0 + 14 + i * 10, y1 - 8], fill=(90, 104, 120), outline=INK)
    d.rectangle([x0 + 6, y1 - 8, x0 + 30, y1 - 4], fill=(90, 104, 120), outline=INK)
    candles = [(8, 15), (13, 20), (18, 25), (23, 29)]
    for i, (t, bt) in enumerate(candles):
        cx = x0 + 52 + i * 17
        d.line([cx, y0 + t - 3, cx, y0 + bt + 2], fill=RED, width=2)
        d.rectangle([cx - 4, y0 + t, cx + 4, y0 + bt], fill=(214, 90, 80), outline=(120, 40, 35))
    d.line([x0 + 46, y0 + 6, x1 - 16, y1 - 8], fill=RED, width=2)
    d.polygon([(x1 - 16, y1 - 14), (x1 - 8, y1 - 6), (x1 - 18, y1 - 5)], fill=RED)
    tag3(d, x0 + 108, y0 + 3, "S&P -2.0%", bg=RED)

def cs_apec(d, b):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle(b, fill=(36, 66, 150))
    tw = d.textlength("21", font=FR(17, 800))
    d.text((cx - tw / 2, cy - 10), "21", font=FR(17, 800), fill=(255, 255, 255))
    import math as _m
    for i, code in enumerate(["cn", "us", "jp", "eu", "ua"]):
        a = _m.radians(-90 + i * 72)
        fx = cx + 44 * _m.cos(a) - 8
        fy = cy + 12 * _m.sin(a) - 5
        flag(d, fx, fy, 16, 10, code)
    tag3(d, x0 + 5, y0 + 3, "APEC", bg=(250, 205, 60), fill=INK)
    tag3(d, x1 - 52, y1 - 12, "SHENZHEN")

def cs_voyagercard(d, b):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle(b, fill=(10, 14, 34))
    for sx, sy in [(x0 + 14, y0 + 6), (x0 + 44, y0 + 11), (x1 - 26, y0 + 7), (x0 + 76, y0 + 4), (x1 - 56, y0 + 13)]:
        d.ellipse([sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2], fill=(235, 240, 250))
    ex, ey = x0 + 22, y1 - 10
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(70, 130, 200), outline=(140, 180, 230))
    d.polygon([(ex - 4, ey - 3), (ex + 2, ey - 4), (ex + 3, ey), (ex - 2, ey + 2)], fill=(90, 170, 100))
    px, py = x1 - 34, y0 + 12
    for t in range(13):
        lx = ex + 10 + t * ((px - 16 - ex) / 13)
        ly = ey - 4 - t * ((ey - 4 - py) / 13)
        if t % 2 == 0:
            d.ellipse([lx - 1.4, ly - 1.4, lx + 1.4, ly + 1.4], fill=(250, 210, 90))
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(238, 240, 244), outline=(200, 200, 208))
    d.line([px + 6, py + 6, px + 15, py + 13], fill=(200, 200, 208), width=2)
    d.ellipse([px + 13, py + 11, px + 18, py + 16], fill=(220, 180, 90))
    d.text((x0 + 40, y0 + 3), "1 LIGHT-DAY", font=FR(7, 800), fill=(250, 210, 90))
    tag3(d, x1 - 44, y1 - 12, "VOYAGER 1")

def cs_carney(d, b):
    x0, y0, x1, y1 = b
    cx = (x0 + x1) // 2
    d.rectangle(b, fill=(220, 232, 220))
    d.line([x0 + 14, y0 + 4, x0 + 14, y1 - 3], fill=(90, 80, 70), width=2)
    flag(d, x0 + 16, y0 + 5, 30, 20, "ca")
    d.line([x1 - 14, y0 + 4, x1 - 14, y1 - 3], fill=(90, 80, 70), width=2)
    flag(d, x1 - 46, y0 + 5, 30, 20, "cn")
    for hx, col in [(cx - 12, (35, 45, 75)), (cx + 12, (25, 28, 38))]:
        d.ellipse([hx - 5, y1 - 19, hx + 5, y1 - 9], fill=(238, 200, 170), outline=(120, 90, 70))
        d.rectangle([hx - 6, y1 - 9, hx + 6, y1 - 3], fill=col)
    d.line([cx - 7, y1 - 7, cx + 7, y1 - 10], fill=(60, 50, 45), width=3)
    d.line([cx - 7, y1 - 10, cx + 7, y1 - 7], fill=(60, 50, 45), width=3)
    tag3(d, cx - 24, y0 + 3, "DEC 2028")

CARD_SCENES3 = {
    "gtawide": cs_gtawide, "cyclone": cs_cyclone, "tanks": cs_tanks,
    "riyadh": cs_riyadh, "kerch": cs_kerch, "florida": cs_florida,
    "vangogh": cs_vangogh, "chart": cs_chart, "apec": cs_apec,
    "voyagercard": cs_voyagercard, "carney": cs_carney,
}

def scene_card3(d, kind, b):
    CARD_SCENES3[kind](d, b)

W2.HERO_SCENES = {"summit": scene_summit3, "icj": scene_icj3,
                  "doc": scene_doc3, "ipo": scene_ipo3}
W2.scene_for_card = scene_card3

if __name__ == "__main__":
    W2.main()
