#!/usr/bin/env python3
"""Draw the news-image-20261119 entry (v1): one newspaper front page that sums
up Thursday 19 November 2026 in a single 1024x1024 PNG. Pure Pillow, no
network, no randomness, no timestamps: the same bytes every run.

Built from the 17 Nov final-heat lessons + the 18 Nov v2 system: FOUR heroes
with rich, labelled flat scenes, a UTC timeline strip, an attribution chip on
every hero and card, data-viz cards for figure stories, 48 stories, and a
date check that names every story left out (with its date).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
CARD = (255, 253, 244)
INK = (20, 32, 46)
RED = (179, 49, 42)
GREY = (96, 104, 112)
LIGHT = (233, 226, 205)
FD = "/usr/share/fonts/truetype/dejavu/"

def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

REGION_COLOR = {
    "EUROPE": (36, 86, 166), "MIDDLE EAST": (179, 49, 42),
    "ASIA": (14, 122, 95), "AFRICA": (176, 110, 10),
    "GLOBAL": (106, 79, 163), "AMERICAS": (31, 122, 140),
    "US": (31, 122, 140), "RUSSIA": (90, 74, 140),
}

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

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

def badge(d, x, y, n, r=11):
    d.ellipse([x - r - 1.6, y - r - 1.6, x + r + 1.6, y + r + 1.6], fill=(255, 253, 244))
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    f = SANS_B(13 if n < 10 else 11)
    s = str(n)
    w = d.textlength(s, font=f)
    d.text((x - w / 2, y - 8), s, font=f, fill=(255, 255, 255))

def chip(d, x1, y, text):
    """Attribution chip: dark pill, top-right of a hero/card scene."""
    f = SANS_B(9)
    w = d.textlength(text, font=f)
    d.rounded_rectangle([x1 - w - 14, y, x1, y + 15], radius=4, fill=INK)
    d.text((x1 - w - 7, y + 3), text, font=f, fill=(255, 255, 255))

def tag(d, x, y, text, fill=(255, 255, 255), bg=INK, size=8):
    f = SANS_B(size)
    w = d.textlength(text, font=f)
    d.rectangle([x, y, x + w + 6, y + size + 5], fill=bg)
    d.text((x + 3, y + 2), text, font=f, fill=fill)

# (n, colour region, tally region, kicker, scene, headline, deck, chip)
HEROES = [
    (1, "ASIA", "Asia-Pacific", "SHENZHEN · SUMMIT", "summit",
     "Trump, Xi and Putin meet in Shenzhen",
     "Joint declaration: a nuclear war \u201ccannot be won\u201d; dialogue on nuclear risks.",
     "CONFIRMED · REUTERS"),
    (2, "EUROPE", "Europe", "THE HAGUE · LAW", "icj",
     "Myanmar guilty of genocide",
     "ICJ 9\u20136: the 2017 campaign killed about 10,000 Rohingya; reparations ordered.",
     "CONFIRMED · UN"),
    (3, "GLOBAL", "World", "NEW YORK · GAMES", "gta",
     "GTA VI arrives after a 13-year wait",
     "Unlocks at midnight worldwide; 19m copies, $1.84bn in a day; 6m watch the streams.",
     "CONFIRMED · SENSOR TOWER"),
    (4, "AMERICAS", "Americas", "NASDAQ · MARKETS", "ipo",
     "Anthropic\u2019s record $81.3bn debut",
     "Priced $83; opened $111.50, closed $97.17 as Wall Street slid.",
     "CONFIRMED · REUTERS"),
]

CARDS = [
    (5, "EUROPE", "Europe", "ANTALYA · CLIMATE", "climate",
     "COP31 draft drops fossil fuels",
     "Revised text cut 144 \u2192 80 paras; \u201cfossil\u201d gone; $120bn target cut.",
     "DRAFT · REUTERS"),
    (6, "ASIA", "Asia-Pacific", "ODISHA · STORM", "cyclone",
     "Cyclone Akvan: 300,000 flee the coast",
     "Landfall Fri noon, winds 90\u2013100 km/h gusting 110; shelters fill.",
     "FORECAST · IMD"),
    (7, "MIDDLE EAST", "Middle East", "GAZA · WAR", "tanks",
     "Israeli tanks cross the Yellow Line",
     "Operation near Nuseirat; Hamas calls it a truce breach; Gazans flee west.",
     "CONFIRMED · UN"),
    (8, "MIDDLE EAST", "Middle East", "RIYADH · GULF", "riyadh",
     "Saudi intercepts Houthi missiles",
     "Two cruise missiles and drones downed over Riyadh; a boom heard in the capital.",
     "CONFIRMED · REUTERS"),
    (9, "EUROPE", "Europe", "KERCH · WAR", "kerch",
     "Ukraine hits Crimean Bridge a third time",
     "Rail traffic halted; third strike in a week.",
     "REPORT · TIMES OF ISRAEL"),
    (10, "AMERICAS", "Americas", "FLORIDA · WEATHER", "florida",
     "Flooded Florida stays shut",
     "Schools closed a second day Thu; flood watch to 7 p.m.; 15 in of rain fell Tue\u2013Wed.",
     "CONFIRMED · NWS"),
    (11, "AMERICAS", "Americas", "NEW YORK · CULTURE", "vangogh",
     "Van Gogh sells for record $190.4m",
     "Tops the artist\u2019s auction record; night total $777.8m at Sotheby\u2019s.",
     "RECORD · SOTHEBY\u2019S"),
    (12, "AMERICAS", "Americas", "WASHINGTON · MARKETS", "chart",
     "Wall Street slides as Anthropic fades",
     "S&P \u22122.02%, a sixth fall; Dow \u22122.19%, below 50,000.",
     "CLOSE · NYSE"),
    (13, "ASIA", "Asia-Pacific", "SHENZHEN · TRADE", "apec",
     "APEC adopts the Shenzhen Outlook",
     "21 economies back digital trade and AI-risk rules; non-binding.",
     "ADOPTED · APEC"),
    (14, "GLOBAL", "World", "SPACE · SCIENCE", "voyagercard",
     "NASA confirms Voyager 1 one light-day out",
     "Crossed Wed 10:16 UTC; JPL confirms Thu; 16.1bn miles.",
     "CONFIRMED · NASA"),
    (15, "ASIA", "Asia-Pacific", "CANADA · TRADE", "carney",
     "Carney wraps APEC with China gains",
     "Arrangement extended to Dec 2028; about $400m in tariff relief.",
     "CONFIRMED · PMO"),
    (16, "ASIA", "Asia-Pacific", "HOBART · SPORT", "cricket",
     "England seal ODI series in Hobart",
     "Duckett 133; England win by 97 runs and take the series 2\u20131.",
     "RESULT · BBC"),
]

# (lead-in, rest, tally region) — stories 17–48
ALSO_PAIRS = [
    ('Fed:', ' Dec hike priced ~100% after hawkish minutes', "Americas"),
    ('Nvidia:', ' falls for a sixth straight session, \u22123.3%', "Americas"),
    ('Washington:', ' jobless claims 203,000; Philly Fed 6.3', "Americas"),
    ('Yemen:', ' Saudi-led coalition strikes a Houthi missile site', "Middle East"),
    ('Modi:', ' meets the Prince and Princess of Wales', "Asia-Pacific"),
    ('Canberra:', ' Australia sanctions West Bank settlers', "Asia-Pacific"),
    ('Dhaka:', ' shutdown; four killed, Yunus home torched', "Asia-Pacific"),
    ('Dakar:', ' boat with ~100 migrants sinks; dozens missing', "Africa"),
    ('Vienna:', ' IAEA: North Korea expands enrichment', "Asia-Pacific"),
    ('Caracas:', ' Hegseth signs a US\u2013Venezuela military pact', "Americas"),
    ('Trump:', ' weighs new Iran strikes as Netanyahu presses', "Americas"),
    ('Copenhagen:', ' Greenland deal approved, 109\u20130', "Europe"),
    ('Kyiv:', ' Russian strikes kill five; power cut in five regions', "Europe"),
    ('Gaza:', ' UN: fleeing Gazans \u201cmust be allowed to return\u201d', "Middle East"),
    ('West Bank:', ' E1 delayed; settler kills woman', "Middle East"),
    ('US:', ' asks court to block migrant protections', "Americas"),
    ('Alaska:', ' Begich keeps sole House seat', "Americas"),
    ('New York:', ' Bitcoin dips below $63,000, then recovers', "World"),
    ('New Delhi:', ' Murmu: 50 crore left extreme poverty', "Asia-Pacific"),
    ('Bengaluru:', ' Amazon pledges $7bn for India renewables', "Asia-Pacific"),
    ('Auckland:', ' NZ plays first as GTA VI unlocks at midnight', "Asia-Pacific"),
    ('Santa Clara:', ' Nvidia halts H-series shipments to China', "Asia-Pacific"),
    ('Senators:', ' AI cyber threats outpace defences', "Americas"),
    ('Frankfurt:', ' Deutsche Bank in $582m Epstein deals', "Europe"),
    ('Mogadishu:', ' Somalia accuses UAE of secret bases', "Africa"),
    ('Nairobi:', ' floods kill six as Ruto gives State of the Nation', "Africa"),
    ('La Paz:', ' El Ni\u00f1o emergency; 78,000 families hit', "Americas"),
    ('Thimphu:', ' lake burst floods hot springs; no injuries', "Asia-Pacific"),
    ('South Pacific:', ' M6.1 quake strikes remote ocean stretch', "Asia-Pacific"),
    ('Mexico City:', ' Banxico cut rates to 6.25% on a 3\u20132 vote', "Americas"),
    ('Jakarta:', ' Indonesia lifts its key rate as the rupiah falls', "Asia-Pacific"),
    ('Manila:', ' Trump meets Marcos Jr. before Shenzhen flight', "Asia-Pacific"),
]
ALSO = [a + b for a, b, _ in ALSO_PAIRS]

TALLY_ORDER = ["Asia-Pacific", "Americas", "Europe", "Middle East", "Africa", "World"]
_counts = {}
for _e in HEROES + CARDS:
    _counts[_e[2]] = _counts.get(_e[2], 0) + 1
for _a in ALSO_PAIRS:
    _counts[_a[2]] = _counts.get(_a[2], 0) + 1
assert sum(_counts.values()) == 48, _counts
TALLY = " · ".join(f"{r} {_counts[r]}" for r in TALLY_ORDER)

# ---------------- scenes (schematic, labelled; labels carry the meaning) ----
SKY = (207, 224, 235)
SEA = (84, 138, 178)
LAND = (216, 196, 148)
SMOKE = (120, 124, 130)

def scene_airport(d, b):
    x0, y0, x1, y1 = b
    # banded sky for depth
    for i in range(6):
        d.rectangle([x0, y0 + i * 10, x1, y0 + (i + 1) * 10], fill=(207 - i * 3, 224 - i * 3, 235 - i * 2))
    d.ellipse([x1 - 52, y0 + 8, x1 - 24, y0 + 36], fill=(246, 199, 80))
    for ccx, ccy in [(x0 + 60, y0 + 16), (x0 + 88, y0 + 11)]:
        d.ellipse([ccx - 17, ccy - 6, ccx + 17, ccy + 6], fill=(238, 242, 246))
    # skyline behind the tarmac, with the terminal sign
    for bx, bw, bh in [(x0 + 18, 26, 34), (x0 + 50, 20, 48), (x0 + 76, 30, 28),
                       (x1 - 84, 24, 42), (x1 - 54, 30, 30)]:
        d.rectangle([bx, y0 + 58 - bh, bx + bw, y0 + 58], fill=(168, 178, 190))
    d.rectangle([x0, y0 + 58, x1, y0 + 74], fill=(196, 200, 204))
    d.rectangle([x0 + 118, y0 + 60, x0 + 208, y0 + 72], fill=INK)
    d.text((x0 + 128, y0 + 62), "SHENZHEN", font=SANS_B(10), fill=(255, 255, 255))
    d.rectangle([x0, y0 + 74, x1, y1], fill=(150, 156, 162))
    # APEC banner strung over the tarmac
    d.line([x0 + 8, y0 + 78, x1 - 8, y0 + 78], fill=INK, width=1)
    d.rectangle([x0 + 132, y0 + 78, x0 + 196, y0 + 90], fill=(200, 50, 45))
    d.text((x0 + 141, y0 + 80), "APEC 2026", font=SANS_B(9), fill=(255, 255, 255))
    # airliner on the tarmac, nose right
    cy = y0 + 96
    d.ellipse([x0 + 26, cy - 13, x0 + 196, cy + 13], fill=(248, 248, 250), outline=INK)
    d.polygon([(x0 + 26, cy - 12), (x0 + 6, cy - 30), (x0 + 26, cy - 2)], fill=(200, 50, 45))
    d.polygon([(x0 + 96, cy + 2), (x0 + 128, cy + 20), (x0 + 150, cy + 20), (x0 + 128, cy + 2)], fill=(90, 100, 116))
    for wx in range(x0 + 52, x0 + 176, 16):
        d.ellipse([wx, cy - 6, wx + 7, cy + 1], fill=(70, 110, 160))
    # red carpet + two figures shaking hands + welcoming line
    d.polygon([(x0 + 196, y1 - 4), (x1 - 30, y1 - 4), (x1 - 58, y1 - 20), (x0 + 210, y1 - 20)], fill=(178, 40, 38))
    for fx, col in [(x1 - 108, (40, 50, 70)), (x1 - 82, (120, 40, 40))]:
        d.ellipse([fx - 6, y1 - 46, fx + 6, y1 - 34], fill=(238, 200, 170))
        d.rectangle([fx - 7, y1 - 34, fx + 7, y1 - 12], fill=col)
    d.line([x1 - 101, y1 - 28, x1 - 89, y1 - 24], fill=(40, 50, 70), width=3)
    for fx in (x0 + 222, x0 + 240, x0 + 258):
        d.ellipse([fx - 4, y1 - 34, fx + 4, y1 - 26], fill=(238, 200, 170))
        d.rectangle([fx - 5, y1 - 26, fx + 5, y1 - 10], fill=(52, 62, 78))
    # three small flags on poles: China, US, Russia
    for i, col in enumerate([(200, 50, 45), (40, 60, 140), (240, 240, 240)]):
        px = x0 + 226 + i * 30
        d.line([px, y0 + 66, px, y1 - 24], fill=INK, width=2)
        d.rectangle([px, y0 + 66, px + 24, y0 + 80], fill=col, outline=INK)

def scene_gulf(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(24, 34, 62))
    for sx, sy in [(x0 + 30, y0 + 14), (x0 + 90, y0 + 30), (x0 + 160, y0 + 10),
                   (x1 - 60, y0 + 22), (x1 - 130, y0 + 38), (x0 + 210, y0 + 16)]:
        d.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(230, 236, 245))
    # land masses: Arabia left, Iran right, strait between
    d.polygon([(x0, y1), (x0, y0 + 44), (x0 + 96, y0 + 62), (x0 + 120, y1)], fill=LAND)
    d.polygon([(x1, y1), (x1, y0 + 30), (x1 - 104, y0 + 52), (x1 - 88, y1)], fill=(206, 184, 138))
    d.text((x0 + 12, y1 - 22), "KUWAIT", font=SANS_B(11), fill=INK)
    d.text((x0 + 38, y0 + 8), "BAHRAIN", font=SANS_B(11), fill=(255, 255, 255))
    d.text((x1 - 56, y1 - 24), "IRAN", font=SANS_B(11), fill=INK)
    d.text(((x0 + x1) // 2 - 34, y1 - 16), "PERSIAN GULF", font=SANS_B(9), fill=(170, 200, 225))
    # base marker in Kuwait
    bx, by = x0 + 52, y0 + 84
    d.rectangle([bx - 9, by - 7, bx + 9, by + 7], fill=(60, 70, 84), outline=(255, 255, 255))
    d.line([bx, by - 7, bx, by - 16], fill=(255, 255, 255), width=2)
    tag(d, bx + 14, by + 10, "US BASE", size=8)
    # two ship silhouettes in the strait
    for sx, sy in [(x0 + 150, y0 + 88), (x0 + 196, y0 + 102)]:
        d.polygon([(sx, sy), (sx + 30, sy), (sx + 25, sy + 6), (sx + 4, sy + 6)], fill=(16, 24, 44), outline=(120, 140, 170))
        d.rectangle([sx + 10, sy - 5, sx + 19, sy], fill=(16, 24, 44), outline=(120, 140, 170))
    # drones flying in from the right, with dashed trails
    for dx, dy in [(x1 - 120, y0 + 34), (x1 - 84, y0 + 52), (x1 - 150, y0 + 62)]:
        for tx in range(dx + 22, min(dx + 52, x1 - 4), 8):
            d.line([tx, dy + 3, tx + 4, dy + 3], fill=(235, 150, 90), width=1)
        d.polygon([(dx, dy), (dx + 18, dy + 4), (dx, dy + 8)], fill=(235, 120, 60))
        d.line([dx + 18, dy + 4, dx + 30, dy + 2], fill=(235, 120, 60), width=2)
    # intercept arcs + bursts from Bahrain and Kuwait
    for ox, oy, r in [(x0 + 44, y0 + 96, 74), (bx, by, 96)]:
        d.arc([ox - r, oy - r, ox + r, oy + r], start=300, end=30, fill=(120, 220, 160), width=3)
    for ex, ey in [(x1 - 104, y0 + 44), (x1 - 66, y0 + 64)]:
        for a in range(0, 360, 45):
            import math
            d.line([ex, ey, ex + 9 * math.cos(math.radians(a)), ey + 9 * math.sin(math.radians(a))],
                   fill=(250, 210, 90), width=2)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(250, 230, 160))

def scene_voyager(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(10, 14, 34))
    for sx, sy in [(x0 + 24, y0 + 18), (x0 + 70, y0 + 44), (x0 + 130, y0 + 12),
                   (x0 + 190, y0 + 34), (x1 - 40, y0 + 14), (x1 - 90, y0 + 48),
                   (x0 + 46, y0 + 70), (x1 - 150, y0 + 8), (x0 + 110, y0 + 62),
                   (x0 + 240, y0 + 44), (x1 - 190, y0 + 26)]:
        d.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(235, 240, 250))
    # Earth, small, lower left
    ex, ey, er = x0 + 44, y1 - 34, 20
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(70, 130, 200))
    d.polygon([(ex - 12, ey - 10), (ex + 2, ey - 14), (ex + 6, ey - 2), (ex - 6, ey + 2)], fill=(90, 170, 100))
    d.polygon([(ex - 4, ey + 8), (ex + 10, ey + 6), (ex + 12, ey + 14), (ex, ey + 16)], fill=(90, 170, 100))
    d.text((ex - 20, ey + er + 4), "EARTH · 1977", font=SANS_B(10), fill=(255, 255, 255))
    # dashed signal path across the scene
    px, py = x1 - 84, y0 + 52
    for t in range(0, 26):
        lx = ex + 26 + t * ((px - 30 - ex) / 26)
        ly = ey - 16 - t * ((ey - 16 - py) / 26)
        if t % 2 == 0:
            d.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(250, 210, 90))
    d.text((x0 + 96, y0 + 8), "1 LIGHT-DAY · 25.9bn km", font=SANS_B(13), fill=(250, 210, 90))
    d.text((x0 + 104, y0 + 80), "SIGNAL TAKES 24H →", font=SANS_B(9), fill=(250, 210, 90))
    # the probe: dish, body, boom, golden record
    d.ellipse([px - 26, py - 26, px + 26, py + 26], fill=(238, 240, 244), outline=INK)
    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(150, 156, 166))
    d.rectangle([px + 18, py + 12, px + 34, py + 24], fill=(200, 170, 90), outline=INK)
    d.ellipse([px + 21, py + 15, px + 31, py + 21], fill=(240, 205, 90), outline=INK)
    d.line([px + 26, py + 20, px + 62, py + 44], fill=(200, 200, 208), width=3)
    d.ellipse([px + 58, py + 40, px + 68, py + 50], fill=(200, 170, 90))
    d.line([px - 14, py + 18, px - 40, py + 40], fill=(200, 200, 208), width=2)
    d.text((px - 34, py + 54), "VOYAGER 1", font=SANS_B(11), fill=(255, 255, 255))

def mini_bg(d, b, color):
    d.rectangle(b, fill=color)

def scene_card(d, kind, b):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "climate":
        mini_bg(d, b, (250, 232, 190))
        d.ellipse([x0 + 14, y0 + 5, x0 + 36, y0 + 27], fill=(245, 180, 40))
        d.rectangle([x0 + 44, y1 - 15, x0 + 66, y1 - 4], fill=(130, 130, 138))
        d.rectangle([x0 + 48, y1 - 23, x0 + 53, y1 - 15], fill=(130, 130, 138))
        d.ellipse([x0 + 44, y1 - 29, x0 + 56, y1 - 21], fill=(170, 170, 178))
        # the contested draft: paper with a red X
        d.rectangle([cx - 6, y0 + 5, cx + 16, y1 - 5], fill=(255, 255, 252), outline=INK)
        d.line([cx - 2, y0 + 9, cx + 12, y1 - 9], fill=RED, width=2)
        d.line([cx + 12, y0 + 9, cx - 2, y1 - 9], fill=RED, width=2)
        d.rectangle([cx + 26, y0 + 6, cx + 32, y1 - 8], outline=INK, width=2)
        d.ellipse([cx + 23, y1 - 14, cx + 35, y1 - 2], fill=RED)
        d.rectangle([cx + 28, y1 - 20, cx + 30, y1 - 10], fill=RED)
        tag(d, x1 - 52, y1 - 13, "ANTALYA", size=8)
    elif kind == "chart":
        mini_bg(d, b, (224, 236, 224))
        d.rectangle([x0 + 56, y0 + 14, x0 + 65, y1 - 8], fill=(180, 225, 180))
        d.rectangle([x0 + 70, y0 + 10, x0 + 79, y1 - 8], fill=(160, 215, 160))
        d.line([x0 + 8, y1 - 6, x1 - 8, y1 - 6], fill=(120, 130, 120), width=1)
        d.line([x0 + 10, y0 + 8, x0 + 44, y0 + 8], fill=(40, 150, 70), width=3)
        d.polygon([(x0 + 44, y0 + 3), (x0 + 52, y0 + 8), (x0 + 44, y0 + 13)], fill=(40, 150, 70))
        d.line([x0 + 10, y1 - 22, x1 - 40, y1 - 10], fill=RED, width=3)
        d.line([x1 - 40, y1 - 10, x1 - 14, y1 - 4], fill=RED, width=3)
        d.polygon([(x1 - 14, y1 - 12), (x1 - 6, y1 - 2), (x1 - 20, y1 - 1)], fill=RED)
        tag(d, x0 + 88, y1 - 12, "S&P −2.0%", bg=RED, size=8)
    elif kind == "parliament":
        mini_bg(d, b, (230, 226, 205))
        for i, px in enumerate(range(cx - 27, cx + 28, 11)):
            d.rectangle([px, y0 + 9, px + 6, y1 - 9], fill=(170, 160, 135), outline=INK)
        d.rectangle([cx - 32, y0 + 4, cx + 32, y0 + 9], fill=INK)
        d.rectangle([cx - 32, y1 - 9, cx + 32, y1 - 4], fill=INK)
        d.line([cx - 36, y1 - 3, cx + 36, y1 - 3], fill=INK, width=1)
        d.polygon([(cx - 34, y0 + 4), (cx - 26, y0 + 1), (cx - 26, y0 + 7)], fill=RED)
        d.polygon([(cx + 34, y0 + 4), (cx + 26, y0 + 1), (cx + 26, y0 + 7)], fill=RED)
    elif kind == "drones":
        mini_bg(d, b, (206, 216, 230))
        for dx, dy in [(x0 + 30, y0 + 10), (cx - 8, y0 + 6), (x1 - 44, y0 + 12)]:
            d.polygon([(dx, dy), (dx + 15, dy + 3), (dx, dy + 7)], fill=INK)
            d.line([dx - 5, dy + 3, dx, dy + 3], fill=INK, width=2)
        for ex, ey in [(cx + 26, cy + 6), (x1 - 30, cy - 2)]:
            for a in range(0, 360, 60):
                import math
                d.line([ex, ey, ex + 7 * math.cos(math.radians(a)), ey + 7 * math.sin(math.radians(a))],
                       fill=(232, 120, 40), width=2)
        d.line([x0 + 6, y1 - 5, x1 - 6, y1 - 5], fill=INK, width=1)
        for hx in (x0 + 20, x0 + 44, x1 - 52):
            d.rectangle([hx, y1 - 13, hx + 14, y1 - 5], fill=(150, 156, 166), outline=INK)
        tag(d, x0 + 66, y1 - 13, "KYIV", size=8)
    elif kind == "eu":
        mini_bg(d, b, (36, 66, 150))
        import math
        for a in range(0, 360, 30):
            sx = cx - 26 + 11 * math.cos(math.radians(a)); sy = cy + 11 * math.sin(math.radians(a))
            d.text((sx - 3, sy - 6), "*", font=SANS_B(10), fill=(250, 205, 60))
        d.text((cx + 2, cy - 11), "€45bn", font=SANS_B(17), fill=(255, 255, 255))
        # Ukraine flag the loan is for
        d.rectangle([x0 + 8, y0 + 6, x0 + 30, y1 - 6], outline=(255, 255, 255))
        d.rectangle([x0 + 8, y0 + 6, x0 + 30, cy], fill=(60, 120, 200))
        d.rectangle([x0 + 8, cy, x0 + 30, y1 - 6], fill=(250, 205, 60))
        tag(d, x1 - 38, y1 - 13, "2027", bg=(250, 205, 60), fill=INK, size=8)
    elif kind == "cyclone":
        mini_bg(d, b, (170, 200, 222))
        import math
        for r, a0 in [(15, 20), (10, 140), (5, 260)]:
            d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], start=a0, end=a0 + 250,
                  fill=(250, 250, 250), width=3)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(60, 90, 130))
        d.polygon([(x0, y1), (x0 + 52, y1), (x0 + 30, y0 + 16), (x0, y0 + 22)], fill=LAND)

        # curved arrow: the storm veers north toward the coast
        d.arc([cx + 6, y0 + 2, cx + 44, y0 + 30], start=90, end=200, fill=RED, width=2)
        d.polygon([(cx + 8, y0 + 14), (cx + 16, y0 + 10), (cx + 15, y0 + 20)], fill=RED)
        for wx in range(x0 + 60, x1 - 8, 26):
            d.arc([wx, y1 - 12, wx + 16, y1 - 2], start=200, end=340, fill=(70, 120, 160), width=2)
    elif kind == "sudan":
        mini_bg(d, b, (238, 224, 198))
        for hx, hh in [(x0 + 14, 12), (x0 + 36, 17), (x1 - 52, 14), (x1 - 28, 10)]:
            d.rectangle([hx, y1 - 5 - hh, hx + 16, y1 - 5], fill=(186, 164, 128), outline=INK)
        for dx, dy in [(cx - 20, y0 + 7), (cx + 16, y0 + 5)]:
            d.polygon([(dx, dy), (dx + 14, dy + 3), (dx, dy + 6)], fill=INK)
        d.ellipse([cx + 2, cy + 4, cx + 10, cy + 12], fill=(232, 120, 40))
        # smoke over the town
        for sx, sy, r in [(x1 - 44, y0 + 6, 6), (x1 - 34, y0 + 4, 8)]:
            d.ellipse([sx - r, sy - r * 0.6, sx + r, sy + r * 0.6], fill=SMOKE)
        d.line([x0 + 6, y1 - 4, x1 - 6, y1 - 4], fill=INK, width=1)
        tag(d, x0 + 62, y1 - 13, "EL OBEID", size=8)
    elif kind == "basket":
        mini_bg(d, b, (250, 236, 205))
        d.polygon([(cx - 24, cy - 2), (cx + 24, cy - 2), (cx + 17, y1 - 6), (cx - 17, y1 - 6)],
                  fill=(200, 130, 60), outline=INK)
        d.line([cx - 20, cy - 2, cx - 8, y0 + 5], fill=INK, width=2)
        d.line([cx + 20, cy - 2, cx + 8, y0 + 5], fill=INK, width=2)
        for lx in (cx - 14, cx, cx + 14):
            d.line([lx - 3, cy + 2, lx - 1, y1 - 8], fill=(150, 90, 40), width=1)
        # groceries in the basket: loaf + bottle
        d.ellipse([cx - 16, cy - 9, cx - 2, cy - 2], fill=(226, 178, 110), outline=INK)
        d.rectangle([cx + 4, cy - 12, cx + 10, cy - 2], fill=(240, 244, 248), outline=INK)
        d.rectangle([cx + 5, cy - 15, cx + 9, cy - 12], fill=RED)
        d.text((cx - 16, y0 + 3), "3.6%", font=SANS_B(14), fill=RED)
        d.polygon([(x1 - 22, y0 + 16), (x1 - 12, y0 + 5), (x1 - 2, y0 + 16)], fill=RED)
        tag(d, x1 - 40, y1 - 13, "OCT CPI", size=8)
    elif kind == "tanks":
        mini_bg(d, b, (216, 208, 188))
        for tx in (x0 + 18, cx + 6):
            d.rectangle([tx, cy + 2, tx + 34, cy + 12], fill=(96, 104, 84), outline=INK)
            d.rectangle([tx + 10, cy - 5, tx + 24, cy + 2], fill=(96, 104, 84), outline=INK)
            d.line([tx + 24, cy - 2, tx + 40, cy - 2], fill=INK, width=3)
            for wx in range(tx + 3, tx + 32, 8):
                d.ellipse([wx, cy + 11, wx + 6, cy + 17], fill=(60, 64, 56))
        d.rectangle([x1 - 34, y0 + 6, x1 - 14, y1 - 8], fill=(196, 188, 168), outline=INK)
        d.polygon([(x1 - 36, y0 + 6), (x1 - 12, y0 + 6), (x1 - 24, y0 - 2)], fill=(170, 160, 140))
        # the tunnel hatch the army says it is destroying
        d.rectangle([cx - 26, y1 - 8, cx - 8, y1 - 3], fill=(70, 66, 58), outline=INK)
        d.line([x0 + 6, y1 - 4, x1 - 6, y1 - 4], fill=INK, width=1)
        tag(d, x0 + 58, y0 + 3, "NUSEIRAT", size=8)
    elif kind == "ipo":
        mini_bg(d, b, (18, 26, 48))
        d.text((x0 + 26, y0 + 4), "$81.3bn", font=SANS_B(15), fill=(255, 255, 255))
        d.text((x0 + 26, y0 + 21), "at $83 a share", font=SANS_B(9), fill=(250, 205, 60))
        # ascending bars bottom-right: past debuts vs this one (kept low,
        # clear of the attribution chip in the top-right corner)
        for i, (bh, col) in enumerate([(4, (110, 120, 140)), (6, (140, 150, 165)), (9, (175, 140, 60)), (12, (250, 205, 60))]):
            bx = x0 + 118 + i * 13
            d.rectangle([bx, y1 - 3 - bh, bx + 9, y1 - 3], fill=col)
    elif kind == "riyadh":
        mini_bg(d, b, (30, 34, 62))
        for sx, sy in [(x0 + 20, y0 + 6), (x0 + 70, y0 + 10), (x1 - 30, y0 + 8)]:
            d.ellipse([sx - 1.4, sy - 1.4, sx + 1.4, sy + 1.4], fill=(230, 236, 245))
        d.rectangle([cx - 8, y0 + 4, cx + 8, y1 - 4], fill=(90, 110, 150), outline=(200, 210, 230))
        d.polygon([(cx - 8, y0 + 4), (cx, y0 - 2), (cx + 8, y0 + 4)], fill=(120, 140, 180))
        for wy in range(y0 + 8, y1 - 6, 6):
            d.rectangle([cx - 5, wy, cx + 5, wy + 3], fill=(255, 220, 130))
        for ox, oy, r in [(x0 + 30, y1 - 4, 30), (x1 - 30, y1 - 4, 30)]:
            d.arc([ox - r, oy - r, ox + r, oy + r], start=240, end=300, fill=(120, 220, 160), width=2)
        for ex, ey in [(x0 + 30, y0 + 12), (x1 - 34, y0 + 10)]:
            for a in range(0, 360, 60):
                import math
                d.line([ex, ey, ex + 5 * math.cos(math.radians(a)), ey + 5 * math.sin(math.radians(a))],
                       fill=(250, 210, 90), width=2)
        tag(d, x0 + 8, y1 - 12, "RIYADH", size=8)
    elif kind == "kerch":
        mini_bg(d, b, (200, 214, 230))
        d.rectangle([x0, y1 - 10, x1, y1], fill=(84, 138, 178))
        d.line([x0, y0 + 12, x1, y0 + 12], fill=INK, width=3)
        for px in (x0 + 20, x0 + 60, x0 + 100, x1 - 40):
            d.line([px, y0 + 12, px, y0 + 26], fill=INK, width=2)
        d.line([x0 + 100, y0 + 12, x0 + 116, y0 + 26], fill=RED, width=3)
        d.polygon([(x0 + 100, y0 + 12), (x0 + 116, y0 + 12), (x0 + 108, y0 + 26)], fill=RED)
        for sx, sy, r in [(x0 + 108, y0 + 6, 5), (x0 + 116, y0 + 4, 6)]:
            d.ellipse([sx - r, sy - r * 0.6, sx + r, sy + r * 0.6], fill=SMOKE)
        d.rectangle([x0 + 8, y0 + 4, x0 + 56, y0 + 11], fill=(60, 70, 84))
        tag(d, x1 - 46, y1 - 12, "KERCH", size=8)
    elif kind == "florida":
        mini_bg(d, b, (150, 190, 220))
        for hx, hw in [(x0 + 8, 26), (x0 + 40, 30), (x1 - 44, 28)]:
            d.rectangle([hx, y0 + 8, hx + hw, y0 + 22], fill=(240, 236, 222), outline=INK)
            d.polygon([(hx - 2, y0 + 8), (hx + hw // 2, y0 + 2), (hx + hw + 2, y0 + 8)], fill=(179, 49, 42))
        d.rectangle([x0, y0 + 22, x1, y1], fill=(60, 110, 160))
        for wx in range(x0 + 4, x1 - 8, 18):
            d.arc([wx, y0 + 24, wx + 12, y0 + 30], start=200, end=340, fill=(200, 230, 250), width=2)
        d.polygon([(cx - 14, y1 - 10), (cx + 14, y1 - 10), (cx + 10, y1 - 4), (cx - 10, y1 - 4)],
                  fill=(230, 120, 40), outline=INK)
        d.ellipse([cx - 3, y1 - 16, cx + 3, y1 - 10], fill=(238, 200, 170))
        tag(d, x0 + 8, y1 - 12, "15 IN", bg=RED, size=8)
    elif kind == "vangogh":
        mini_bg(d, b, (250, 232, 190))
        d.rectangle([cx - 3, y0 + 12, cx + 3, y1 - 4], fill=(120, 84, 48))
        for ox, oy, col in [(-14, 4, (250, 200, 80)), (10, 2, (240, 190, 90)),
                            (-6, 10, (180, 200, 90)), (16, 10, (250, 210, 100)),
                            (0, 0, (255, 220, 120))]:
            d.ellipse([cx + ox - 7, y0 + oy - 5, cx + ox + 7, y0 + oy + 5], fill=col, outline=(150, 120, 40))
        d.rectangle([x0 + 6, y1 - 8, x0 + 30, y1 - 4], fill=(90, 140, 90))
        tag(d, x1 - 58, y1 - 12, "$190.4m", bg=RED, size=8)
    elif kind == "apec":
        mini_bg(d, b, (36, 66, 150))
        import math
        for a in range(0, 360, 30):
            sx = cx - 30 + 10 * math.cos(math.radians(a)); sy = cy + 10 * math.sin(math.radians(a))
            d.text((sx - 3, sy - 6), "*", font=SANS_B(9), fill=(250, 205, 60))
        d.text((cx - 4, cy - 8), "21", font=SANS_B(16), fill=(255, 255, 255))
        d.text((x0 + 6, y0 + 3), "APEC", font=SANS_B(9), fill=(250, 205, 60))
        tag(d, x1 - 66, y1 - 12, "SHENZHEN", size=8)
    elif kind == "carney":
        mini_bg(d, b, (220, 232, 220))
        d.rectangle([x0 + 8, y0 + 6, x0 + 34, y0 + 18], fill=(200, 50, 45), outline=INK)
        d.rectangle([x0 + 8, y0 + 6, x0 + 34, y0 + 12], fill=(255, 255, 255))
        d.rectangle([x1 - 34, y0 + 6, x1 - 8, y0 + 18], fill=(200, 50, 45), outline=INK)
        for sx in range(x1 - 32, x1 - 10, 5):
            d.text((sx, y0 + 8), "*", font=SANS_B(7), fill=(250, 205, 60))
        d.ellipse([cx - 12, y1 - 18, cx - 4, y1 - 10], fill=(238, 200, 170))
        d.ellipse([cx + 4, y1 - 18, cx + 12, y1 - 10], fill=(238, 200, 170))
        d.line([cx - 8, y1 - 12, cx + 8, y1 - 12], fill=INK, width=3)
        tag(d, x0 + 40, y1 - 12, "DEC 2028", size=8)
    elif kind == "cricket":
        mini_bg(d, b, (140, 190, 120))
        d.rectangle([x0 + 20, y0 + 6, x1 - 20, y1 - 6], fill=(216, 196, 148))
        for sx in (cx - 30, cx + 28):
            for i in range(3):
                d.line([sx + i * 4, y0 + 10, sx + i * 4, y0 + 20], fill=(250, 205, 60), width=2)
        d.line([cx - 14, y1 - 14, cx + 6, y1 - 22], fill=(150, 110, 60), width=4)
        d.ellipse([cx + 18, y0 + 12, cx + 26, y0 + 20], fill=(179, 49, 42), outline=(255, 255, 255))
        tag(d, x0 + 8, y1 - 12, "133", bg=RED, size=8)
    elif kind == "voyagercard":
        mini_bg(d, b, (10, 14, 34))
        for sx, sy in [(x0 + 12, y0 + 6), (x0 + 40, y0 + 10), (x1 - 24, y0 + 8),
                       (x0 + 70, y0 + 4), (x1 - 50, y0 + 14)]:
            d.ellipse([sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2], fill=(235, 240, 250))
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(238, 240, 244), outline=(200, 200, 208))
        d.line([cx + 6, cy + 6, cx + 16, cy + 14], fill=(200, 200, 208), width=2)

    else:
        mini_bg(d, b, LIGHT)

def scene_summit(d, b):
    x0, y0, x1, y1 = b
    # grand hall: warm wood panel + window skyline of Shenzhen
    d.rectangle(b, fill=(94, 64, 48))
    for i in range(5):
        d.rectangle([x0, y0 + i * 12, x1, y0 + (i + 1) * 12], fill=(214 - i * 4, 226 - i * 3, 238 - i * 2))
    for bx, bw, bh in [(x0 + 14, 18, 30), (x0 + 38, 12, 44), (x0 + 56, 20, 24),
                       (x1 - 70, 16, 36), (x1 - 48, 12, 46), (x1 - 30, 20, 26)]:
        d.rectangle([bx, y0 + 58 - bh, bx + bw, y0 + 58], fill=(120, 134, 150))
    d.rectangle([x0, y0 + 58, x1, y0 + 62], fill=(70, 52, 44))
    d.text((x0 + 96, y0 + 6), "SHENZHEN", font=SANS_B(12), fill=(255, 255, 255))
    # three flags on the back wall: China, US, Russia
    for i, col in enumerate([(200, 50, 45), (40, 60, 140), (240, 240, 240)]):
        fx = x0 + 78 + i * 30
        d.rectangle([fx, y0 + 66, fx + 24, y0 + 82], fill=col, outline=(255, 255, 255))
    # long leaders' table, red cloth, three name plates
    d.rectangle([x0 + 8, y0 + 86, x1 - 8, y1 - 14], fill=(150, 36, 34))
    d.rectangle([x0 + 8, y0 + 86, x1 - 8, y0 + 92], fill=(200, 60, 52))
    for i, name in enumerate(["XI", "TRUMP", "PUTIN"]):
        px = x0 + 62 + i * 58
        # seated figure: head above the table edge, name on the cloth
        d.ellipse([px - 7, y0 + 72, px + 7, y0 + 86], fill=(238, 200, 170))
        d.rectangle([px - 10, y0 + 84, px + 10, y0 + 92], fill=(40, 50, 70) if i != 1 else (120, 40, 40))
        fw = d.textlength(name, font=SANS_B(8))
        d.text((px - fw / 2, y0 + 94), name, font=SANS_B(8), fill=(255, 230, 210))
    # microphones on the table, between the leaders
    for mx in (x0 + 91, x0 + 149, x0 + 207):
        d.line([mx, y0 + 92, mx, y0 + 100], fill=(220, 220, 220), width=2)
        d.ellipse([mx - 3, y0 + 97, mx + 3, y0 + 103], fill=(220, 220, 220))
    d.text((x0 + 8, y1 - 12), "APEC · 19 NOV", font=SANS_B(8), fill=(255, 220, 200))

def scene_icj(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(206, 220, 232))
    # courthouse facade: pediment + columns
    d.polygon([(x0 + 30, y0 + 8), (x1 - 30, y0 + 8), (x0 + 120, y0 + 34)], fill=(240, 236, 222), outline=INK)
    d.ellipse([(x0 + x1) // 2 - 10, y0 + 12, (x0 + x1) // 2 + 10, y0 + 32], fill=(179, 49, 42))
    for cx in (x0 + 44, x0 + 84, x0 + 124, x0 + 164, x0 + 204):
        d.rectangle([cx - 6, y0 + 36, cx + 6, y0 + 86], fill=(250, 248, 240), outline=INK)
    d.rectangle([x0 + 20, y0 + 86, x1 - 20, y0 + 92], fill=(240, 236, 222), outline=INK)
    d.text((x0 + 62, y0 + 40), "THE HAGUE", font=SANS_B(11), fill=INK)
    # scales of justice, centre foreground
    sx, sy = (x0 + x1) // 2, y0 + 96
    d.line([sx, sy - 14, sx, sy + 12], fill=INK, width=3)
    d.line([sx - 18, sy - 12, sx + 18, sy - 12], fill=INK, width=2)
    d.polygon([(sx - 22, sy + 2), (sx - 10, sy + 2), (sx - 16, sy - 10)], fill=(200, 170, 90), outline=INK)
    d.polygon([(sx + 10, sy + 2), (sx + 22, sy + 2), (sx + 16, sy - 10)], fill=(200, 170, 90), outline=INK)
    d.ellipse([sx - 3, sy - 17, sx + 3, sy - 11], fill=(200, 170, 90))
    # gavel + vote tally on the right
    d.rectangle([x1 - 52, y1 - 22, x1 - 20, y1 - 16], fill=(94, 64, 48))
    d.line([x1 - 44, y1 - 16, x1 - 30, y1 - 8], fill=(94, 64, 48), width=3)
    d.text((x0 + 8, y1 - 12), "VOTE 9\u20136", font=SANS_B(11), fill=RED)

def scene_gta(d, b):
    x0, y0, x1, y1 = b
    # Vice City sunset: gradient sky, sun, skyline, palms, neon
    for i in range(8):
        d.rectangle([x0, y0 + i * 8, x1, y0 + (i + 1) * 8],
                    fill=(250 - i * 6, 140 + i * 6, 120 + i * 8))
    d.ellipse([x1 - 66, y0 + 10, x1 - 22, y0 + 54], fill=(255, 220, 130))
    for bx, bw, bh in [(x0 + 8, 16, 34), (x0 + 30, 12, 48), (x0 + 48, 20, 28),
                       (x0 + 74, 14, 40), (x1 - 96, 18, 44), (x1 - 72, 12, 52), (x1 - 54, 22, 30)]:
        d.rectangle([bx, y0 + 78 - bh, bx + bw, y0 + 78], fill=(60, 30, 70))
        for wy in range(y0 + 78 - bh + 4, y0 + 74, 8):
            d.rectangle([bx + 3, wy, bx + 7, wy + 4], fill=(255, 210, 110))
    d.rectangle([x0, y0 + 78, x1, y1], fill=(40, 22, 50))
    d.rectangle([x0 + 40, y0 + 84, x0 + 200, y0 + 96], fill=(20, 40, 60), outline=(255, 120, 180))
    d.text((x0 + 52, y0 + 86), "VICE CITY", font=SANS_B(10), fill=(255, 120, 180))
    # palm silhouettes + a low sports car
    for px in (x0 + 22, x1 - 30):
        d.line([px, y0 + 78, px, y0 + 96], fill=(30, 60, 30), width=3)
        for a in range(0, 360, 60):
            import math
            d.line([px, y0 + 78, px + 12 * math.cos(math.radians(a)), y0 + 78 + 8 * math.sin(math.radians(a))],
                   fill=(30, 90, 50), width=2)
    d.polygon([(x0 + 96, y1 - 10), (x0 + 112, y1 - 20), (x0 + 150, y1 - 20), (x0 + 168, y1 - 10)],
              fill=(220, 40, 90), outline=(255, 255, 255))
    d.ellipse([x0 + 108, y1 - 8, x0 + 116, y1 - 2], fill=INK)
    d.ellipse([x0 + 148, y1 - 8, x0 + 156, y1 - 2], fill=INK)

def scene_ipo(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(16, 24, 46))
    # Nasdaq tower + ticker tape
    d.rectangle([x0 + 8, y0 + 10, x0 + 56, y0 + 62], fill=(30, 44, 80), outline=(90, 120, 180))
    for wy in range(y0 + 16, y0 + 58, 10):
        d.rectangle([x0 + 14, wy, x0 + 50, wy + 5], fill=(120, 200, 255))
    d.text((x0 + 8, y0 + 66), "ANT", font=SANS_B(20), fill=(255, 255, 255))
    d.text((x0 + 66, y0 + 40), "$83 \u2192 $111.50", font=SANS_B(13), fill=(250, 205, 60))
    d.text((x0 + 66, y0 + 58), "CLOSE $97.17", font=SANS_B(11), fill=(120, 220, 160))
    # ascending bars: past debuts vs ANT
    for i, (bh, col) in enumerate([(10, (110, 120, 140)), (16, (140, 150, 165)),
                                   (24, (175, 140, 60)), (40, (250, 205, 60))]):
        bx = x0 + 150 + i * 20
        d.rectangle([bx, y1 - 16 - bh, bx + 14, y1 - 16], fill=col)
    d.line([x0 + 140, y1 - 16, x1 - 8, y1 - 16], fill=(120, 140, 170), width=1)
    d.text((x0 + 150, y1 - 12), "BIGGEST IPO EVER", font=SANS_B(8), fill=(255, 255, 255))

SCENES = {"summit": scene_summit, "icj": scene_icj, "gta": scene_gta, "ipo": scene_ipo}

# ---------------- world map (dotted grid from continent ellipses) -----------
LAND_ELLIPSES = [
    (-100, 47, 42, 16), (-88, 36, 22, 10), (-152, 64, 14, 5), (-42, 73, 12, 6),
    (-62, -12, 14, 17), (-70, -32, 8, 12),
    (16, 52, 20, 9), (14, 63, 10, 6), (-3, 43, 9, 5), (22, 40, 10, 5), (-2, 54, 4, 4),
    (18, 8, 21, 15), (24, -16, 15, 13), (47, -19, 5, 7),
    (62, 52, 52, 13), (88, 34, 26, 13), (78, 21, 9, 9), (104, 16, 8, 9),
    (48, 24, 13, 7), (35, 39, 10, 5), (138, 37, 5, 5),
    (113, -1, 16, 4), (131, -3, 8, 3),
    (134, -25, 15, 8), (172, -42, 5, 5),
]

def is_land(lon, lat):
    for clon, clat, rx, ry in LAND_ELLIPSES:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
            return True
    return False

PINS = [  # (number, lon, lat, dx, dy)
    (1, 114, 22, 6, 10), (2, 4, 52, -10, -8), (3, -74, 41, 10, -6), (4, -74, 41, -12, 10),
    (5, 30, 37, -14, -8), (6, 85, 20, 6, 8), (7, 34, 31, 8, 12), (8, 47, 24, 12, 6),
    (9, 36, 45, 8, -8), (10, -80, 26, -10, 8), (11, -74, 41, 12, 12), (12, -74, 41, -14, -14),
    (13, 114, 22, -14, 12), (14, -170, 62, 0, 0), (15, -76, 45, -12, -6), (16, 147, -43, 6, -8),
]
BRIEF_DOTS = [
    (90, 24), (172, -41), (121, 14), (-106, 56), (138, 37), (127, 37),
    (114, 22), (45, 24), (13, 52), (33, 45), (40, 9), (-66, 10), (-72, 19),
    (32, 39), (30, -2), (107, -6), (0, 51), (2, 47), (23, -1), (-13, 10),
    (57, -20), (21, 42), (86, 55), (35, -19), (-75, -9), (-74, 4), (-58, -23),
    (-66, 10), (20, 0), (7, 45), (151, -33), (178, -17),
]

def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(240, 236, 218), outline=INK, width=1)
    cols, rows = 47, 28
    for r in range(rows):
        lat = 75 - (r + 0.5) * (135 / rows)
        for c in range(cols):
            lon = -180 + (c + 0.5) * (360 / cols)
            if is_land(lon, lat):
                px = x0 + (c + 0.5) * w / cols
                py = y0 + (r + 0.5) * h / rows
                d.ellipse([px - 1.7, py - 1.7, px + 1.7, py + 1.7], fill=(110, 116, 92))
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * w, y0 + (75 - lat) / 135 * h)
    for lon, lat in BRIEF_DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 2.4, py - 2.4, px + 2.4, py + 2.4], fill=RED)
    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        badge(d, px + dx, py + dy, n, r=7)

# ---------------- the day in UTC (timeline strip) ---------------------------
TIMELINE = [  # (hour, label, above?)
    (1.6, "Voyager confirmed \u00b7 01:37", True),
    (10.0, "ICJ judgment \u00b7 10:00", False),
    (11.2, "COP31 draft \u00b7 11:10", True),
    (14.5, "ANT opens \u00b7 14:30", False),
    (21.0, "Wall St closes \u00b7 21:00", True),
]

def draw_timeline(d):
    ty0, ty1 = 116, 150
    d.text((10, 120), "THE DAY IN UTC", font=SANS_B(10), fill=INK)
    d.text((10, 134), "all times UTC", font=SANS(8), fill=GREY)
    ax0, ax1, ay = 150, 1006, 134
    segs = ["OVERNIGHT", "MORNING", "MIDDAY", "EVENING"]
    for i, s in enumerate(segs):
        sx0 = ax0 + i * (ax1 - ax0) / 4
        sx1 = ax0 + (i + 1) * (ax1 - ax0) / 4
        d.rectangle([sx0, 126, sx1, 142], fill=(238, 232, 214) if i % 2 == 0 else (232, 225, 203))
        tw = d.textlength(s, font=SANS_B(7))
        d.text(((sx0 + sx1) / 2 - tw / 2, 136), s, font=SANS_B(7), fill=GREY)
    d.line([ax0, ay, ax1, ay], fill=INK, width=2)
    for h, label, above in TIMELINE:
        x = ax0 + h / 24 * (ax1 - ax0)
        d.ellipse([x - 3, ay - 3, x + 3, ay + 3], fill=RED)
        tw = d.textlength(label, font=SANS_B(8))
        lx = min(max(x - tw / 2, ax0), ax1 - tw)
        d.text((lx, 117 if above else 144), label, font=SANS_B(8), fill=INK)

# ---------------- page assembly ----------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # faint newsprint grain, deterministic (drawn first, under everything)
    for gx in range(3, W, 6):
        for gy in range(3, H, 6):
            d.point((gx, gy), fill=(238, 231, 214))
    # masthead
    center(d, 8, "THE WORLD'S NEWS IN ONE PICTURE", SANS_B(13), INK)
    d.line([10, 30, W - 10, 30], fill=INK, width=2)
    center(d, 36, "Thursday 19 November 2026", SERIF_B(44), INK)
    d.rectangle([10, 88, W - 10, 112], fill=RED)
    center(d, 94, "48 STORIES · 6 REGIONS · ALL FROM THURSDAY 19 NOVEMBER 2026", SANS_B(14), (255, 255, 255))
    # timeline strip
    draw_timeline(d)
    # heroes (scenes 118px, headlines 19px, decks 12px, attribution chips)
    hy, hh, hw, hgap = 154, 240, 245, 8
    for i, (n, region, _tally, kicker, scene, head, deck, ch) in enumerate(HEROES):
        x = 10 + i * (hw + hgap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD, outline=INK, width=2)
        SCENES[scene](d, (x + 2, hy + 2, x + hw - 2, hy + 120))
        badge(d, x + 16, hy + 16, n, r=12)
        chip(d, x + hw - 8, hy + 8, ch)
        d.text((x + 10, hy + 125), kicker, font=SANS_B(10), fill=REGION_COLOR[region])
        y = text_block(d, x + 10, hy + 140, head, SANS_B(19), INK, hw - 20, 21, 3)
        text_block(d, x + 10, y + 2, deck, SANS(12), (40, 48, 58), hw - 20, 15, 3)
    # cards (headlines 14px, 32px scenes with labels, attribution chips)
    cy0, chh, cw, cgap = 402, 132, 160, 8
    for i, (n, region, _tally, kicker, scene, head, deck, ch) in enumerate(CARDS):
        x = 10 + (i % 6) * (cw + cgap)
        y = cy0 + (i // 6) * (chh + cgap)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD, outline=INK, width=1)
        scene_card(d, scene, (x + 2, y + 2, x + cw - 2, y + 34))
        badge(d, x + 12, y + 18, n, r=10)
        chip(d, x + cw - 6, y + 5, ch)
        d.text((x + 8, y + 38), kicker, font=SANS_B(9), fill=REGION_COLOR[region])
        yy = text_block(d, x + 8, y + 52, head, SANS_B(14), INK, cw - 16, 16, 3)
        fit = max(0, (y + chh - 4 - (yy + 2)) // 11)
        text_block(d, x + 8, yy + 2, deck, SANS(10), (40, 48, 58), cw - 16, 11, min(3, fit))
    # bottom headers
    d.text((10, 682), "WHERE IT HAPPENED", font=SANS_B(14), fill=INK)
    d.text((262, 682), "ALSO ON THURSDAY 19 NOVEMBER", font=SANS_B(15), fill=INK)
    strap = "32 MORE STORIES · Nos 17–48"
    d.text((W - 10 - d.textlength(strap, font=SANS_B(11)), 685), strap, font=SANS_B(11), fill=GREY)
    d.line([10, 702, W - 10, 702], fill=INK, width=2)
    # map + tallies (left)
    draw_map(d, 10, 710, 236, 120)
    d.text((10, 834), "Pins 1–16 heroes & cards · 14 = space · Dots 17–48", font=SANS(9), fill=GREY)
    ty = 850
    ty = text_block(d, 10, ty, "BY REGION — " + TALLY, SANS(11), INK, 236, 13, 3)
    text_block(d, 10, ty + 4, "DATE CHECK — Left out on purpose: Pew Islam-largest report (18 Nov) · Jeffries nominated 251\u201311 (18 Nov) · EU \u20ac45bn Ukraine loan (18 Nov) · Nvidia quarter (17 Nov) · Fed minutes + Dow \u2212561 (18 Nov) · Iran strikes on Kuwait/Bahrain (18 Nov) · Nature Great Unconformity study (4 Nov).", SANS_B(10), RED, 236, 12, 8)
    # also list (right, two columns of 16, 12px, bold lead-ins)
    lx, lw, row_h = 262, 368, 14
    for i, (lead, rest, _r) in enumerate(ALSO_PAIRS):
        col, row = i // 16, i % 16
        x = lx + col * (lw + 16)
        y = 710 + row * row_h
        num = f"{17 + i}."
        d.text((x, y), num, font=SANS_B(12), fill=RED)
        nw = d.textlength(num + " ", font=SANS_B(12))
        lw_lead = d.textlength(lead, font=SANS_B(12))
        assert nw + lw_lead + d.textlength(rest, font=SANS(12)) <= lw, f"also item {17 + i} too wide"
        d.text((x + nw, y), lead, font=SANS_B(12), fill=INK)
        d.text((x + nw + lw_lead, y), rest, font=SANS(12), fill=INK)
    # footer
    d.line([10, 974, W - 10, 974], fill=INK, width=2)
    center(d, 982, "Every story happened or was first reported on Thursday 19 November 2026. Contested claims are marked as claims.", SANS_B(11), INK)
    center(d, 999, "Sources: Reuters · AP · AFP · BBC · Al Jazeera · UN News · NASA · IMD · NWS · Sensor Tower · Sotheby\u2019s · PMO · Times of Israel  |  One picture, one day: Thursday 19 November 2026.", SANS(10), GREY)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")

if __name__ == "__main__":
    main()
