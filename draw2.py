#!/usr/bin/env python3
"""news-image-20261119 entry, v2: the same verified 48 stories of Thursday
19 November 2026, rebuilt to the winners' system (dev top-10 of this edition
+ final top-10 of the 18 Nov edition): Playfair Display masthead and serif
headlines, Libre Franklin labels, a red italic strap, region and field bars,
a day-in-numbers strip, a precise UTC timeline, four layered hero scenes,
scene cards with region-coloured numbers, a dotted map with a HOW SURE
legend, and a date check that names what was left out and what is not yet.
Pure Pillow, bundled OFL fonts, no network, deterministic bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import draw as v1  # v1 data + hero scenes + map geometry (same session's work)

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts") + "/"
W = H = 1024
M = 20
CW = W - 2 * M
PAPER = (250, 246, 235)
CARD = (255, 253, 245)
INK = (22, 28, 38)
RED = (178, 44, 38)
GREY = (96, 100, 108)
RULE = (210, 202, 180)

def PF(size, weight=700):
    return ImageFont.truetype(FD + f"playfair-display-v40-latin-{weight}.ttf", size)

def PFI(size):
    return ImageFont.truetype(FD + "playfair-display-v40-latin-700italic.ttf", size)

def FR(size, weight=700):
    return ImageFont.truetype(FD + f"libre-franklin-v20-latin-{weight}.ttf", size)

REGION_COLOR = {
    "Asia-Pacific": (14, 122, 95), "Americas": (31, 122, 140),
    "Europe": (36, 86, 166), "Middle East": (179, 49, 42),
    "Africa": (176, 110, 10), "World": (106, 79, 163),
}
FIELD_COLOR = {
    "POLITICS": (58, 62, 110), "WAR": (120, 44, 40), "MARKETS": (24, 96, 74),
    "CLIMATE": (30, 110, 150), "CULTURE": (150, 96, 20), "SCIENCE": (96, 74, 140),
}

wrap = v1.wrap

def text_block(d, x, y, text, font, fill, maxw, leading, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def center(d, y, text, font, fill, cx=W // 2):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)

def fit_size(d, text, maker, maxw, start, minimum):
    s = start
    while s > minimum and d.textlength(text, font=maker(s)) > maxw:
        s -= 1
    return maker(s)

def headline_fit(d, text, maxw, start=21, minimum=15, max_lines=2):
    """Largest Playfair 700 size whose wrap fits max_lines lines."""
    for s in range(start, minimum - 1, -1):
        f = PF(s)
        if len(wrap(d, text, f, maxw)) <= max_lines:
            return f, s
    return PF(minimum), minimum

def badge2(d, x, y, n, color, r=11):
    d.ellipse([x - r - 1.6, y - r - 1.6, x + r + 1.6, y + r + 1.6], fill=(255, 253, 244))
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    f = FR(13 if n < 10 else 11, 800)
    s = str(n)
    w = d.textlength(s, font=f)
    d.text((x - w / 2, y - 8), s, font=f, fill=(255, 255, 255))

def chip2(d, x1, y, text):
    f = FR(9, 800)
    w = d.textlength(text, font=f)
    d.rounded_rectangle([x1 - w - 14, y, x1, y + 15], radius=4, fill=INK)
    d.text((x1 - w - 7, y + 3), text, font=f, fill=(255, 255, 255))

# (n, region, kicker, scene, headline, deck, chip, field)
HEROES = [
    (1, "Asia-Pacific", "SHENZHEN · SUMMIT", "summit",
     "Trump, Xi and Putin hold first three-way summit",
     "Joint declaration: a nuclear war \u201ccannot be won\u201d; talks on nuclear risk and energy. No deal on Ukraine. \u2014 Reuters",
     "CONFIRMED · REUTERS", "POLITICS"),
    (2, "Europe", "THE HAGUE · LAW", "icj",
     "World Court: Myanmar committed genocide",
     "Judges ruled 9\u20136: the 2017 campaign killed about 10,000 Rohingya. Reparations ordered; a first for any state. \u2014 UN News",
     "CONFIRMED · UN", "POLITICS"),
    (3, "Europe", "ANTALYA · CLIMATE", "doc",
     "COP31 draft drops fossil fuels, $120bn aid",
     "Revised text cut 144 to 80 paragraphs; \u201cfossil\u201d deleted, $120bn adaptation goal cut. Talks close Friday. \u2014 Reuters",
     "DRAFT · REUTERS", "CLIMATE"),
    (4, "Americas", "NASDAQ · MARKETS", "ipo",
     "Anthropic\u2019s record IPO: $83 to $97.17",
     "Raised $81.3bn, the biggest IPO on record. Opened $111.50, closed +17% as the Dow fell 1,101 points. \u2014 Reuters",
     "CONFIRMED · REUTERS", "MARKETS"),
]

# (n, region, kicker, scene-kind, headline, deck, field, wide?)
CARDS = [
    (5, "World", "WORLDWIDE · GAMES", "gtawide",
     "GTA VI goes on sale after 13 years",
     "Unlocks at midnight, Auckland first. 19.05m copies, $1.84bn on day one (Sensor Tower est.); 6m watch the streams; PSN buckles.",
     "CULTURE", True),
    (6, "Asia-Pacific", "ODISHA · STORM", "cyclone",
     "Cyclone Akvan: 300,000 flee the coast",
     "Winds 90\u2013100 km/h, gusting 110; landfall Fri noon. \u2014 IMD",
     "CLIMATE", False),
    (7, "Middle East", "GAZA · WAR", "tanks",
     "Israeli tanks cross the Yellow Line",
     "Near Nuseirat; Hamas calls it a truce breach. \u2014 UN OCHA",
     "WAR", False),
    (8, "Middle East", "RIYADH · GULF", "riyadh",
     "Saudi intercepts Houthi missiles",
     "Missiles and drones downed over the capital. \u2014 Reuters",
     "WAR", False),
    (9, "Europe", "KERCH · WAR", "kerch",
     "Ukraine hits Crimean Bridge a third time",
     "Rail traffic halted; third strike in a week. \u2014 Times of Israel",
     "WAR", False),
    (10, "Americas", "FLORIDA · WEATHER", "florida",
     "Flooded Florida stays shut",
     "Schools shut a second day; flood watch to 7 p.m. \u2014 AP/NWS",
     "CLIMATE", False),
    (11, "Americas", "NEW YORK · CULTURE", "vangogh",
     "Van Gogh sells for record $190.4m",
     "Tops the artist\u2019s auction record; night total $777.8m. \u2014 CNBC",
     "CULTURE", False),
    (12, "Americas", "WASHINGTON · MARKETS", "chart",
     "Wall Street slides as Anthropic fades",
     "S&P -2.02%, a sixth straight fall; Dow below 50,000. \u2014 Reuters",
     "MARKETS", False),
    (13, "Asia-Pacific", "SHENZHEN · TRADE", "apec",
     "APEC adopts the Shenzhen Outlook",
     "21 economies back digital trade, AI-risk rules. \u2014 APEC",
     "POLITICS", False),
    (14, "World", "SPACE · SCIENCE", "voyagercard",
     "Voyager 1 is one light-day out",
     "Crossed Wed 10:16 UTC; NASA confirms Thu. \u2014 NASA",
     "SCIENCE", False),
    (15, "Asia-Pacific", "CANADA · TRADE", "carney",
     "Carney wraps APEC with China gains",
     "Deal extended to Dec 2028; $400m tariff relief. \u2014 PMO",
     "POLITICS", False),
]

# briefs 16-48: (lead-in, rest, region, field) — Hobart joins from the cards
BRIEFS = [
    ('Hobart:', ' Duckett 133 as England win by 97 runs and take the ODI series 2\u20131', "Asia-Pacific", "CULTURE"),
] + [(a, b, r, f) for (a, b, r), f in zip(v1.ALSO_PAIRS, [
    "MARKETS", "MARKETS", "MARKETS", "WAR", "POLITICS", "POLITICS", "POLITICS",
    "POLITICS", "POLITICS", "WAR", "WAR", "POLITICS", "WAR", "WAR", "WAR",
    "POLITICS", "POLITICS", "MARKETS", "POLITICS", "MARKETS", "CULTURE",
    "MARKETS", "SCIENCE", "MARKETS", "WAR", "POLITICS", "CLIMATE", "CLIMATE",
    "SCIENCE", "MARKETS", "MARKETS", "POLITICS",
])]

_counts = {}
for _e in HEROES:
    _counts[_e[1]] = _counts.get(_e[1], 0) + 1
for _e in CARDS:
    _counts[_e[1]] = _counts.get(_e[1], 0) + 1
for _b in BRIEFS:
    _counts[_b[2]] = _counts.get(_b[2], 0) + 1
assert sum(_counts.values()) == 48, _counts
REGION_ORDER = ["Asia-Pacific", "Americas", "Europe", "Middle East", "Africa", "World"]
REGION_TALLY = [(r, _counts[r]) for r in REGION_ORDER]

_fcounts = {}
for _e in HEROES:
    _fcounts[_e[7]] = _fcounts.get(_e[7], 0) + 1
for _e in CARDS:
    _fcounts[_e[6]] = _fcounts.get(_e[6], 0) + 1
for _b in BRIEFS:
    _fcounts[_b[3]] = _fcounts.get(_b[3], 0) + 1
assert sum(_fcounts.values()) == 48, _fcounts
FIELD_ORDER = ["POLITICS", "MARKETS", "WAR", "CLIMATE", "CULTURE", "SCIENCE"]
FIELD_TALLY = [(f, _fcounts[f]) for f in FIELD_ORDER]

NUMBERS = [
    ("9\u20136", "ICJ GENOCIDE VOTE"),
    ("$81.3bn", "BIGGEST IPO EVER"),
    ("300,000+", "FLEE CYCLONE AKVAN"),
    ("19.05m", "GTA VI COPIES, DAY ONE"),
    ("$190.4m", "VAN GOGH AUCTION RECORD"),
    ("109\u20130", "DENMARK\u2019S ARCTIC VOTE"),
]

TIMELINE = [  # (hour, label, above?)
    (0.0, "00:00 AUCKLAND \u00b7 GTA VI", True),
    (1.62, "01:37 VOYAGER CONFIRMED", False),
    (10.0, "10:00 THE HAGUE \u00b7 ICJ", False),
    (11.17, "11:10 ANTALYA \u00b7 COP31", True),
    (14.5, "14:30 NEW YORK \u00b7 ANT", False),
    (21.0, "21:00 WALL ST CLOSE", True),
]

# ---------------- v2 scenes -------------------------------------------------
def stamp(d, cx, cy, text, angle=16, color=RED, size=17):
    """A tilted rubber stamp, drawn on its own layer and rotated."""
    f = FR(size, 800)
    w = int(d.textlength(text, font=f)) + 16
    layer = Image.new("RGBA", (w + 8, size + 16), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([2, 2, w + 4, size + 12], radius=4, outline=color + (255,), width=3)
    ld.text((10, 5), text, font=f, fill=color + (255,))
    layer = layer.rotate(angle, expand=True, resample=Image.BILINEAR)
    d._pil.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)

def scene_doc(d, b):
    """COP31 hero: the draft deal, its fossil-fuel line struck out, CUT stamp."""
    x0, y0, x1, y1 = b
    for i in range(6):
        d.rectangle([x0, y0 + i * 16, x1, y0 + (i + 1) * 16], fill=(196 - i * 5, 224 - i * 4, 216 - i * 3))
    d.rectangle([x0 + 18, y0 + 8, x1 - 58, y1 - 8], fill=(255, 255, 250), outline=INK)
    d.rectangle([x0 + 22, y0 + 12, x1 - 62, y0 + 24], fill=INK)
    d.text((x0 + 28, y0 + 15), "DRAFT DEAL \u00b7 19 NOV", font=FR(8, 800), fill=(255, 255, 255))
    for i, lw in enumerate([110, 124, 96]):
        d.line([x0 + 30, y0 + 34 + i * 9, x0 + 30 + lw, y0 + 34 + i * 9], fill=(170, 172, 160), width=2)
    d.text((x0 + 30, y0 + 58), "FOSSIL FUELS", font=FR(16, 800), fill=INK)
    d.line([x0 + 28, y0 + 67, x0 + 124, y0 + 67], fill=RED, width=3)
    d.text((x0 + 30, y0 + 76), "$120BN ADAPTATION AID", font=FR(10, 800), fill=INK)
    d.line([x0 + 28, y0 + 84, x0 + 146, y0 + 84], fill=RED, width=3)
    d.text((x0 + 30, y0 + 94), "144 PARAGRAPHS CUT TO 80", font=FR(8, 800), fill=RED)
    stamp(d, x1 - 42, y0 + 56, "CUT", angle=16, size=19)

def scene_gtawide(d, b):
    """Wide GTA card strip: Vice City sunset, skyline, car, VI badge."""
    x0, y0, x1, y1 = b
    h = y1 - y0
    for i in range(6):
        d.rectangle([x0, y0 + i * (h // 6 + 1), x1, y0 + (i + 1) * (h // 6 + 1)],
                    fill=(122 + i * 18, 44 + i * 16, 128 + i * 10))
    d.ellipse([x0 + 30, y0 + 6, x0 + 58, y0 + 30], fill=(255, 214, 120))
    for bx, bw, bh in [(x0 + 90, 16, 18), (x0 + 112, 12, 23), (x0 + 130, 20, 15),
                       (x1 - 120, 16, 20), (x1 - 98, 12, 24), (x1 - 80, 20, 16)]:
        d.rectangle([bx, y1 - 8 - bh, bx + bw, y1 - 8], fill=(38, 20, 54))
        for wy in range(y1 - 8 - bh + 3, y1 - 10, 7):
            d.rectangle([bx + 3, wy, bx + 6, wy + 3], fill=(255, 205, 105))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(30, 16, 40))
    d.polygon([(x0 + 168, y1 - 8), (x0 + 182, y1 - 17), (x0 + 216, y1 - 17), (x0 + 232, y1 - 8)],
              fill=(216, 42, 92), outline=(255, 255, 255))
    d.ellipse([x0 + 178, y1 - 7, x0 + 185, y1 - 1], fill=INK)
    d.ellipse([x0 + 214, y1 - 7, x0 + 221, y1 - 1], fill=INK)
    d.rectangle([x1 - 58, y0 + 5, x1 - 12, y0 + 25], fill=(24, 10, 34), outline=(255, 120, 190))
    d.text((x1 - 46, y0 + 8), "VI", font=FR(15, 800), fill=(255, 120, 190))
    d.text((x0 + 8, y1 - 20), "VICE CITY", font=FR(8, 800), fill=(255, 190, 220))

HERO_SCENES = {"summit": v1.scene_summit, "icj": v1.scene_icj, "ipo": v1.scene_ipo,
               "doc": scene_doc}

def scene_for_card(d, kind, b):
    if kind == "gtawide":
        scene_gtawide(d, b)
    else:
        v1.scene_card(d, kind, b)

# ---------------- map (v2 pins, region colours) ------------------------------
PINS2 = [  # (n, lon, lat, dx, dy, region)
    (1, 114, 22, 8, 10, "Asia-Pacific"), (2, 4, 52, -12, -10, "Europe"),
    (3, 30, 37, -16, -6, "Europe"), (4, -74, 41, 12, -12, "Americas"),
    (5, -74, 41, -14, 12, "World"), (6, 85, 20, 8, 8, "Asia-Pacific"),
    (7, 34, 31, 10, 12, "Middle East"), (8, 47, 24, 12, 4, "Middle East"),
    (9, 36, 45, 10, -10, "Europe"), (10, -80, 26, -12, 8, "Americas"),
    (11, -74, 41, 16, 4, "Americas"), (12, -74, 41, -16, -14, "Americas"),
    (13, 114, 22, -16, 12, "Asia-Pacific"), (14, -168, 66, 0, 0, "World"),
    (15, -76, 45, -14, -8, "Asia-Pacific"),
]
BRIEF_DOTS2 = v1.BRIEF_DOTS + [(147, -43)]

def draw_map2(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(240, 236, 218), outline=INK, width=1)
    cols, rows = 52, 26
    for r in range(rows):
        lat = 75 - (r + 0.5) * (135 / rows)
        for c in range(cols):
            lon = -180 + (c + 0.5) * (360 / cols)
            if v1.is_land(lon, lat):
                px = x0 + (c + 0.5) * w / cols
                py = y0 + (r + 0.5) * h / rows
                d.ellipse([px - 1.7, py - 1.7, px + 1.7, py + 1.7], fill=(110, 116, 92))
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * w, y0 + (75 - lat) / 135 * h)
    for lon, lat in BRIEF_DOTS2:
        px, py = proj(lon, lat)
        d.ellipse([px - 2.2, py - 2.2, px + 2.2, py + 2.2], fill=RED)
    for n, lon, lat, dx, dy, region in PINS2:
        px, py = proj(lon, lat)
        badge2(d, px + dx, py + dy, n, REGION_COLOR[region], r=7)

# ---------------- bars and strips ---------------------------------------------
def tally_bar(d, y, h, tally, colors, total=48, label_size=11, short=None):
    x = M
    for name, count in tally:
        wseg = CW * count / total
        d.rectangle([x, y, x + wseg, y + h], fill=colors[name])
        label = f"{(short or {}).get(name, name)} {count}"
        f = fit_size(d, label, lambda s: FR(s, 800), wseg - 8, label_size, 8)
        tw = d.textlength(label, font=f)
        d.text((x + (wseg - tw) / 2, y + (h - label_size) / 2 - 1), label, font=f, fill=(255, 255, 255))
        x += wseg

def draw_timeline(d, y):
    d.text((M, y + 2), "THE DAY", font=FR(10, 800), fill=INK)
    d.text((M, y + 15), "IN UTC", font=FR(10, 800), fill=INK)
    ax0, ax1, ay = 118, W - M, y + 16
    for i, s in enumerate(["OVERNIGHT", "MORNING", "MIDDAY", "EVENING"]):
        sx0 = ax0 + i * (ax1 - ax0) / 4
        sx1 = ax0 + (i + 1) * (ax1 - ax0) / 4
        d.rectangle([sx0, y + 6, sx1, y + 26], fill=(240, 234, 216) if i % 2 == 0 else (233, 226, 204))
        tw = d.textlength(s, font=FR(7, 700))
        d.text(((sx0 + sx1) / 2 - tw / 2, y + 18), s, font=FR(7, 700), fill=GREY)
    d.line([ax0, ay, ax1, ay], fill=INK, width=2)
    for hh, label, above in TIMELINE:
        x = ax0 + hh / 24 * (ax1 - ax0)
        d.ellipse([x - 3, ay - 3, x + 3, ay + 3], fill=RED)
        tw = d.textlength(label, font=FR(8, 700))
        lx = min(max(x - tw / 2, ax0), ax1 - tw)
        d.text((lx, y - 6 if above else y + 30), label, font=FR(8, 700), fill=INK)

# ---------------- page assembly ----------------------------------------------
WARNS = []

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d._pil = img
    for gx in range(3, W, 6):
        for gy in range(3, H, 6):
            d.point((gx, gy), fill=(240, 234, 218))
    # eyebrow + rules
    d.text((M, 10), "THE WORLD IN ONE DAY", font=FR(12, 800), fill=INK)
    rtxt = "48 STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY"
    d.text((W - M - d.textlength(rtxt, font=FR(11, 700)), 11), rtxt, font=FR(11, 700), fill=INK)
    d.line([M, 28, W - M, 28], fill=INK, width=2)
    d.line([M, 32, W - M, 32], fill=INK, width=1)
    # masthead (Playfair Black, auto-fit)
    mf = fit_size(d, "Thursday 19 November 2026", lambda s: PF(s, 900), CW, 88, 40)
    center(d, 38, "Thursday 19 November 2026", mf, INK)
    # red italic strap
    strap = "Trump, Xi and Putin share one table \u00b7 The World Court finds genocide in Myanmar \u00b7 COP31\u2019s draft drops fossil fuels"
    sf = fit_size(d, strap, PFI, CW, 19, 12)
    center(d, 118, strap, sf, RED)
    # region + field bars
    tally_bar(d, 142, 24, REGION_TALLY, REGION_COLOR)
    tally_bar(d, 170, 20, FIELD_TALLY, FIELD_COLOR, label_size=10)
    # the day in numbers
    nw = CW / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + nw * i + nw / 2
        nf = fit_size(d, num, lambda s: FR(s, 800), nw - 10, 23, 12)
        tw = d.textlength(num, font=nf)
        d.text((cx - tw / 2, 196), num, font=nf, fill=INK)
        lf = fit_size(d, lab, lambda s: FR(s, 600), nw - 6, 8, 6)
        tw = d.textlength(lab, font=lf)
        d.text((cx - tw / 2, 218), lab, font=lf, fill=GREY)
        if i:
            d.line([M + nw * i, 194, M + nw * i, 228], fill=RULE, width=1)
    d.line([M, 234, W - M, 234], fill=RULE, width=1)
    # timeline
    draw_timeline(d, 242)
    d.line([M, 278, W - M, 278], fill=INK, width=2)
    # heroes
    hy, hh, hw, hgap = 284, 222, 237, 12
    for i, (n, region, kicker, scene, head, deck, ch, _field) in enumerate(HEROES):
        x = M + i * (hw + hgap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD, outline=INK, width=2)
        HERO_SCENES[scene](d, (x + 2, hy + 2, x + hw - 2, hy + 120))
        badge2(d, x + 15, hy + 15, n, REGION_COLOR[region], r=11)
        chip2(d, x + hw - 8, hy + 8, ch)
        d.text((x + 10, hy + 126), kicker, font=FR(9, 800), fill=REGION_COLOR[region])
        hf, hs = headline_fit(d, head, hw - 20, start=21)
        y = text_block(d, x + 10, hy + 139, head, hf, INK, hw - 20, hs + 1, 2)
        if len(wrap(d, head, hf, hw - 20)) > 2:
            WARNS.append(f"hero {n} headline wraps >2")
        y2 = text_block(d, x + 10, y + 2, deck, FR(10, 600), (40, 48, 58), hw - 20, 11.5, 3)
        if len(wrap(d, deck, FR(10, 600), hw - 20)) > 3:
            WARNS.append(f"hero {n} deck wraps >3")
        if y2 > hy + hh - 1:
            WARNS.append(f"hero {n} deck overflows box ({y2} > {hy + hh - 1})")
    # cards: row 1 = GTA wide + 4 singles, row 2 = 6 singles
    cw_, chh, cgap = 155, 102, 10
    rows = [CARDS[:5], CARDS[5:]]
    for ri, row in enumerate(rows):
        y = 512 + ri * (chh + 8)
        x = M + 2
        for (n, region, kicker, scene, head, deck, _field, wide) in row:
            wcard = cw_ * 2 + cgap if wide else cw_
            d.rectangle([x, y, x + wcard, y + chh], fill=CARD, outline=INK, width=1)
            scene_for_card(d, scene, (x + 1, y + 1, x + wcard - 1, y + 33))
            badge2(d, x + 11, y + 11, n, REGION_COLOR[region], r=8)
            d.text((x + 7, y + 37), kicker, font=FR(8, 800), fill=REGION_COLOR[region])
            hf, hs = headline_fit(d, head, wcard - 14, start=14, minimum=11)
            yy = text_block(d, x + 7, y + 48, head, hf, INK, wcard - 14, hs + 1, 2)
            if len(wrap(d, head, hf, wcard - 14)) > 2:
                WARNS.append(f"card {n} headline wraps >2")
            y2 = text_block(d, x + 7, yy + 1, deck, FR(9, 600), (40, 48, 58), wcard - 14, 10.5, 2)
            if len(wrap(d, deck, FR(9, 600), wcard - 14)) > 2:
                WARNS.append(f"card {n} deck wraps >2")
            if y2 > y + chh - 1:
                WARNS.append(f"card {n} overflows box ({y2} > {y + chh - 1})")
            x += wcard + cgap
    # bottom headers
    d.text((M, 730), "WHERE IT HAPPENED", font=FR(13, 800), fill=INK)
    d.text((352, 730), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=FR(13, 800), fill=INK)
    strap2 = "33 MORE STORIES \u00b7 Nos 16\u201348"
    d.text((W - M - d.textlength(strap2, font=FR(10, 700)), 733), strap2, font=FR(10, 700), fill=GREY)
    d.line([M, 748, W - M, 748], fill=INK, width=2)
    # map + how-sure legend (left)
    draw_map2(d, M, 756, 316, 130)
    d.text((M, 894), "HOW SURE ARE WE?", font=FR(9, 800), fill=INK)
    for j, line in enumerate([
            "CONFIRMED \u2014 named sources agree",
            "REPORT \u00b7 CLAIM \u2014 one side says so",
            "FORECAST \u00b7 DRAFT \u2014 set, not yet final"]):
        d.text((M, 907 + j * 13), line, font=FR(9, 600), fill=(40, 48, 58))
    # briefs (right, two columns)
    bx, bw, brow = 352, 318, 11.2
    for i, (lead, rest, _r, _f) in enumerate(BRIEFS):
        col, rowi = i // 17, i % 17
        x = bx + col * (bw + 16)
        y = 756 + rowi * brow
        num = f"{16 + i}."
        d.text((x, y), num, font=FR(10, 800), fill=RED)
        nw2 = d.textlength(num + " ", font=FR(10, 800))
        size = 10
        while size > 8 and nw2 + d.textlength(lead + rest, font=FR(size, 600)) > bw:
            size -= 0.5
        if nw2 + d.textlength(lead + rest, font=FR(size, 600)) > bw:
            WARNS.append(f"brief {16 + i} too wide at 8.5px")
        d.text((x + nw2, y), lead, font=FR(size, 700), fill=INK)
        lw3 = d.textlength(lead, font=FR(size, 700))
        d.text((x + nw2 + lw3, y), rest, font=FR(size, 600), fill=INK)
    # date check box
    d.rectangle([M, 948, W - M, 1002], fill=(250, 233, 224), outline=RED, width=1)
    dx = M + 12
    d.text((dx, 953), "DATE CHECK", font=FR(10, 800), fill=RED)
    w1 = d.textlength("DATE CHECK", font=FR(10, 800))
    d.text((dx + w1, 953), " \u2014 every story on this page happened, or was first reported, on Thursday 19 November 2026.",
           font=FR(10, 600), fill=INK)
    d.text((dx, 965), "LEFT OUT AS OTHER DAYS\u2019 NEWS \u2014 Wed 18 Nov: Pew\u2019s Islam-by-2035 study \u00b7 Jeffries nominated 251\u201311 \u00b7 EU \u20ac45bn Ukraine loan \u00b7 Fed minutes, Dow -561",
           font=FR(10, 600), fill=INK)
    d.text((dx, 977), "\u00b7 Iran\u2019s strikes on Kuwait and Bahrain \u00b7 Libya\u2019s Derna drug seizure \u00b7 Tue 17 Nov: Nvidia\u2019s $115.8bn quarter \u00b7 4 Nov: Nature\u2019s Great Unconformity study",
           font=FR(10, 600), fill=INK)
    d.text((dx, 989), "NOT YET", font=FR(10, 800), fill=RED)
    w4 = d.textlength("NOT YET", font=FR(10, 800))
    d.text((dx + w4, 989), " \u2014 Fri 20 Nov: Cyclone Akvan makes landfall \u00b7 COP31\u2019s scheduled close",
           font=FR(10, 600), fill=INK)
    # footer
    center(d, 1008, "Claims are attributed, not stated as fact \u00b7 Pictures and map: original, drawn in code \u00b7 Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 UN News \u00b7 NASA \u00b7 IMD \u00b7 NWS \u00b7 Sensor Tower \u00b7 Sotheby\u2019s \u00b7 PMO \u00b7 Times of Israel",
           FR(9, 600), GREY)
    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png")
    for w_ in WARNS:
        print("WARN:", w_)

if __name__ == "__main__":
    main()
