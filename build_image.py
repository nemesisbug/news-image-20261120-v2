#!/usr/bin/env python3
"""Draw the v2 renewal front page for news-image-20261120.

"Friday 20 November 2026" in one image, following the live top-1 grammar:
giant serif date masthead, 4-story red deck, 6-stat strip, region bar,
3 illustrated leads, 10 illustrated cards, world map with numbered pins,
22 numbered briefs, and a two-line date check.

35 stories, all events that happened or were first reported on Friday
20 November 2026 (sources in the README). Deterministic: same bytes on
every run, no network, no timestamps, no randomness.
Run: python3 build_image.py  ->  writes entry.png next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 232)
INK = (18, 18, 18)
MUTED = (96, 92, 84)
RED = (178, 30, 30)
RED_DK = (140, 22, 22)
NAVY = (24, 44, 74)
NAVY_DK = (16, 30, 54)
TEAL = (14, 94, 98)
MAROON = (92, 26, 26)
OCHRE = (164, 116, 28)
SLATE = (74, 88, 104)
GREEN = (46, 96, 58)
PURPLE = (92, 64, 120)
LINE = (198, 192, 180)
CARD_BG = (255, 255, 255)
SEA = (30, 54, 88)
LAND = (224, 212, 186)
LAND_LINE = (190, 176, 146)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


def F_SERIF(s):
    return _font("DejaVuSerif-Bold.ttf", s)


def F_SERIF_IT(s):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf"), s)
    except OSError:
        return _font("DejaVuSerif.ttf", s)


def F_SERIF_R(s):
    return _font("DejaVuSerif.ttf", s)


def F_SANS(s):
    return _font("DejaVuSans.ttf", s)


def F_BOLD(s):
    return _font("DejaVuSans-Bold.ttf", s)


def wrap(d, text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped paragraph; returns y after the last line."""
    lh = leading or int(fnt.size * 1.28)
    lines = wrap(d, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def fit_para(d, x, y, text, fnt_fn, size, width, max_lines, fill=INK, leading=None):
    """Draw paragraph, shrinking the font until it fits max_lines."""
    while size >= 8:
        fnt = fnt_fn(size)
        lines = wrap(d, text, fnt, width)
        if len(lines) <= max_lines:
            lh = leading or int(size * 1.24)
            for line in lines:
                d.text((x, y), line, font=fnt, fill=fill)
                y += lh
            return y
        size -= 1
    fnt = fnt_fn(8)
    lh = leading or 10
    for line in wrap(d, text, fnt, width)[:max_lines]:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hline(d, x0, x1, y, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ------------------------------------------------------------------ content

DECK = ("Kyiv's bridges hit  ·  Akvan comes ashore  ·  Asia's markets plunge  ·  "
        "UK and EU sign three deals")

STATS = [
    ("3", "Dnipro bridges hit in Kyiv"),
    ("300,000+", "evacuated before Akvan"),
    ("\u22126.2%", "Taiex \u2014 worst week since 1991"),
    ("100,000", "UK\u2013EU youth visas a year"),
    ("2.2%", "Japan core inflation"),
    ("$3.79bn", "GTA VI first-day sales"),
]

REGIONS = [("Europe", 9, (178, 30, 30)), ("Asia", 10, (24, 44, 74)),
           ("Middle East", 3, (14, 94, 98)), ("Africa", 5, (164, 116, 28)),
           ("Americas", 6, (46, 96, 58)), ("Oceania", 1, (92, 64, 120)),
           ("Global", 1, (74, 88, 104))]

LEADS = [
    dict(num=1, kicker="KYIV, UKRAINE \u2014 MISSILE STRIKES",
         head="Russian missiles hit three Kyiv bridges",
         deck=("400+ drones and 110+ missiles in an overnight barrage kill 8 "
               "across Ukraine and cut power, heating and water. (Reuters, AP)"),
         chip="OFFICIALS' COUNT"),
    dict(num=2, kicker="GOPALPUR, INDIA \u2014 CYCLONE AKVAN",
         head="Akvan comes ashore in eastern India",
         deck=("Landfall 07:30\u201308:30 IST; 300,000+ moved to shelters as winds gust "
               "to 90 km/h. (IMD)"),
         chip="LANDFALL 07:30\u201308:30 IST"),
    dict(num=3, kicker="ASIA \u2014 AI SELL-OFF",
         head="AI fears sink Asia's stock markets",
         deck=("Taiwan leads the rout as AI valuations slide; SoftBank closes "
               "14.5% down. (Morningstar)"),
         chip="CLOSING PRICES"),
]

CARDS = [
    dict(num=4, kicker="BRUSSELS \u2014 UK\u2013EU DEAL", bg=NAVY, art="flags",
         head="UK and EU sign food, youth and carbon deals",
         deck="Post-Brexit summit eases farm trade, links carbon markets. (Reuters)"),
    dict(num=5, kicker="ANTALYA \u2014 COP31", bg=TEAL, art="globe",
         head="Climate talks reach final day deadlocked",
         deck="Draft drops the fossil-fuel phase-out and $120bn goal. (Reuters)"),
    dict(num=6, kicker="POLAND \u2014 AIRSPACE", bg=SLATE, art="jet",
         head="Russian missiles cross into Poland",
         deck="NATO calls it a grave violation; jets scrambled. (Reuters, AP)"),
    dict(num=7, kicker="TOKYO \u2014 INFLATION", bg=RED_DK, art="cpi",
         head="Japan core inflation hits 2.2%",
         deck="Highest this year keeps a BOJ rate rise on track. (Japan Times)"),
    dict(num=8, kicker="KUALA LUMPUR \u2014 FOOTBALL", bg=PURPLE, art="ball",
         head="India U17 reach the Asian Cup",
         deck="A 0\u20130 draw with Malaysia tops Group E and seals qualification. (IANS)"),
    dict(num=9, kicker="BUENOS AIRES \u2014 TESLA", bg=GREEN, art="car",
         head="Tesla opens its first store in Argentina",
         deck="Unicenter showroom opens in Mart\u00ednez; Model 3, Model Y orders open. (Reuters)"),
    dict(num=10, kicker="ROME \u2014 GENERAL STRIKE", bg=OCHRE, art="crowd",
         head="Italy stops as CGIL calls strike",
         deck="Tens of thousands march in 100+ cities over wages. (Reuters)"),
    dict(num=11, kicker="PRETORIA \u2014 OBITUARY", bg=NAVY, art="globe",
         head="S. Africa mourns its first woman deputy president",
         deck="Mlambo-Ngcuka, ex-UN Women chief, dies at 71. (Mail & Guardian)"),
    dict(num=12, kicker="PARIS \u2014 YOUTH STRIKE", bg=MAROON, art="mega",
         head="Youth strike sweeps 25+ countries",
         deck="Students march across Europe over living costs. (Straits Times)"),
    dict(num=13, kicker="WELLINGTON \u2014 CRICKET", bg=TEAL, art="cricket",
         head="Phillips 118 makes history vs India",
         deck="First to hit Test, ODI and T20I hundreds vs India in one year. (IANS)"),
]

BRIEFS = [
    (14, "HODEIDAH", "Saudi coalition strikes Hodeidah port; Houthis warn airlines off Saudi airspace. (Reuters)"),
    (15, "JURF AL-SAKHAR", "Iraq moves against an Iran-backed militia stronghold. (Just Security)"),
    (16, "BAYELSA", "Funeral boat capsizes in Bayelsa; 4 dead, 24 rescued, hundreds feared aboard. (Reuters)"),
    (17, "LUSAKA", "High Court clears the way for jailed opposition leaders to seek bail. (Zambian Observer)"),
    (18, "PRETORIA", "Police report 581 women killed in three months; 16 Days campaign launched. (BBC)"),
    (19, "LOS ANGELES", "Jury convicts man of starting the deadly Palisades Fire at retrial. (AP)"),
    (20, "NEW YORK", "Indian man gets 19\u00bd years for plot to kill Sikh separatist Pannun. (Reuters)"),
    (21, "ST. LOUIS", "Judge approves Bayer's $7.25bn Roundup settlement. (Reuters)"),
    (22, "WASHINGTON", "Trump confirms he fired his cyber chief: 'didn't think that person was good enough.' (Reuters)"),
    (23, "MANCHESTER", "Drone pilot apologises for filming Pochettino's first Man Utd training. (Guardian)"),
    (24, "TALLINN", "Estonia to shut its road borders with Russia for six months. (Just Security)"),
    (25, "GENEVA", "UNICEF: 1,144 children killed or injured in Ukraine in 2026. (Reuters)"),
    (26, "TOKYO", "Japan to buy 8m barrels of Saudi crude; Riyadh gains 16m barrels of storage. (Bloomberg)"),
    (27, "SHENZHEN", "Xi and Prabowo launch China\u2013Indonesia economic partnership talks. (Xinhua)"),
    (28, "SEOUL", "Seoul asks Uruguay to help restart Korea\u2013Mercosur trade talks. (Yonhap)"),
    (29, "DHAKA", "Police say 124 Awami League members arrested in raids over 24 hours. (Views Bangladesh)"),
    (30, "KATHMANDU", "Nepal PM Balendra Shah to visit India Nov 22\u201323, his first trip abroad. (IANS)"),
    (31, "HORMUZ", "Tanker hit by projectile near Khasab catches fire; no casualties. (Reuters)"),
    (32, "NAIROBI", "High Court lifts ban on publishing judges' individual performance scores. (The Standard)"),
    (33, "BOGOT\u00c1", "Finance minister: 2026 deficit will top 7.6% of GDP, above budget. (Reuters)"),
    (34, "GLOBAL", "UN's ninth straw poll fails; Grynspan leads with 10 votes, blocked by vetoes. (Guardian)"),
    (35, "DOHA", "India A thrash Nepal by 306 runs in the Rising Stars Cup. (IANS)"),
]

DATE_CHECK_1 = ("LEFT OUT \u2014 Thu 19 Nov: ICJ Myanmar ruling \u00b7 Shenzhen declaration \u00b7 "
                "Anthropic $81.3bn IPO \u00b7 GTA VI launch \u00b7 Senate Iran vote 51\u201348 \u00b7 "
                "Homo erectus papers (18 Nov).")
DATE_CHECK_2 = ("NOT YET SHOWN \u2014 any COP31 final text \u00b7 BepiColombo's Mercury orbit entry, "
                "due Saturday 21 Nov [FORECAST].")

FOOTER = ("Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 IMD \u00b7 Morningstar/Dow Jones \u00b7 IANS \u00b7 "
          "Japan Times \u00b7 The Guardian \u00b7 Straits Times \u00b7 Just Security \u00b7 Mail & Guardian \u00b7 "
          "Zambian Observer \u00b7 Bloomberg \u00b7 Xinhua \u00b7 Yonhap \u00b7 Views Bangladesh \u00b7 The Standard. "
          "All 35 stories happened or were first reported Friday 20 November 2026.")

# ------------------------------------------------------------------ map data
# Rough continent outlines as (lon, lat) polygons; equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-72, 12), (-62, 10), (-52, 5), (-40, -5), (-35, -8),
     (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -50),
     (-73, -37), (-70, -20), (-77, -12), (-80, -3)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (40, 15), (43, 11), (48, 11), (51, 10), (44, 0), (40, -10), (35, -20),
     (32, -28), (26, -34), (20, -35), (15, -27), (12, -18), (13, -10),
     (9, 4), (-8, 5), (-15, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (40, 68), (45, 68),
     (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42), (12, 44),
     (8, 44), (3, 43), (-2, 37), (-6, 36)],
    [(40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72), (160, 70),
     (178, 66), (170, 60), (162, 56), (158, 52), (142, 50), (140, 40),
     (130, 35), (127, 38), (122, 30), (120, 22), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (77, 8), (72, 20),
     (65, 25), (60, 25), (55, 26), (50, 29), (48, 30), (44, 29), (40, 32),
     (36, 36), (30, 36), (28, 41), (30, 45), (35, 50), (40, 55)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43),
     (145, 44), (141, 39), (137, 36), (132, 33)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (178, -37),
     (175, -40), (172, -42), (168, -46)],
]

# Story number -> (lon, lat) of the place it happened.
PINS = {1: (30.5, 50.4), 2: (84.9, 19.3), 3: (121.5, 25.0), 4: (4.4, 50.85),
        5: (30.7, 36.9), 6: (23.0, 50.3), 7: (139.7, 35.7), 8: (101.7, 3.1),
        9: (-58.4, -34.6), 10: (12.5, 41.9), 11: (28.19, -25.75),
        12: (2.35, 48.85), 13: (174.8, -41.3)}
# Badge nudges (dx, dy) in px where true pin positions would collide.
# Europe cluster: pins 1/4/6 sit within ~10 px of each other at this scale,
# so their badges are spread apart (true spot kept as a red dot + leader).
NUDGE = {1: (16, -16), 4: (20, -18), 6: (-18, -16), 12: (-17, 11),
         7: (13, 12)}


def project(lon, lat, mx, my, s):
    """Equirectangular: lon -168..192 -> x, lat 84..-58 -> y (square scale)."""
    x = mx + (lon + 168.0) * s
    y = my + 56 + (84.0 - lat) * s
    return x, y


# ------------------------------------------------------------------ art panels

def draw_lead_art(d, idx, x0, y0, x1, y1):
    """Flat-vector illustration for lead idx inside (x0,y0,x1,y1)."""
    w, h = x1 - x0, y1 - y0
    if idx == 1:
        # Night skyline, three bridges over a river, missile trails, fires.
        d.rectangle([x0, y0, x1, y1], fill=NAVY_DK)
        d.rectangle([x0, y0 + h - 26, x1, y1], fill=(38, 68, 110))
        for bx, bw, bh in [(8, 34, 52), (48, 26, 66), (80, 40, 44), (126, 30, 60),
                           (162, 36, 48), (204, 28, 62), (238, 34, 46), (278, 30, 56)]:
            d.rectangle([x0 + bx, y0 + h - 26 - bh, x0 + bx + bw, y0 + h - 26],
                        fill=(10, 18, 36))
            for wy in range(0, bh - 8, 12):
                for wx in range(4, bw - 4, 9):
                    d.rectangle([x0 + bx + wx, y0 + h - 26 - bh + wy,
                                 x0 + bx + wx + 3, y0 + h - 26 - bh + wy + 4],
                                fill=(232, 196, 90))
        for ax, ay in [(60, 26), (150, 18), (240, 30)]:
            d.line([(x0 + ax, y0 + ay), (x0 + ax + 26, y0 + ay + 34)],
                   fill=(255, 220, 160), width=2)
        for fx, fy in [(58, y0 + h - 30), (150, y0 + h - 34), (238, y0 + h - 30)]:
            for k in range(8):
                ang = k * 3.14159 / 4
                d.line([(fx, fy), (fx + 9 * __import__("math").cos(ang),
                                   fy + 9 * __import__("math").sin(ang))],
                       fill=(255, 120, 40), width=2)
        for bx in [30, 130, 230]:
            d.arc([x0 + bx, y0 + h - 40, x0 + bx + 60, y0 + h - 6], 180, 360,
                  fill=(220, 220, 220), width=3)
            d.line([(x0 + bx, y0 + h - 23), (x0 + bx + 60, y0 + h - 23)],
                   fill=(220, 220, 220), width=2)
    elif idx == 2:
        # Cyclone spiral over the Bay of Bengal.
        d.rectangle([x0, y0, x1, y1], fill=(16, 74, 92))
        cx, cy = x0 + w // 2 - 18, y0 + h // 2
        for r, a0, a1 in [(58, 20, 300), (46, 80, 340), (34, 140, 380),
                          (23, 200, 420), (13, 260, 460)]:
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1,
                  fill=(240, 244, 248), width=4)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(240, 244, 248))
        lx, ly = x0 + w - 52, y0 + h - 26
        d.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], fill=RED)
        d.ellipse([lx - 11, ly - 11, lx + 11, ly + 11], outline=(255, 255, 255), width=2)
        d.text((x0 + 8, y0 + 6), "BAY OF BENGAL", font=F_BOLD(9), fill=(220, 235, 240))
    else:
        # Falling market chart + 4-index closing table.
        d.rectangle([x0, y0, x1, y1], fill=MAROON)
        pts = [(x0 + 12, y0 + 16), (x0 + 48, y0 + 24), (x0 + 84, y0 + 20),
               (x0 + 120, y0 + 38), (x0 + 156, y0 + 34), (x0 + 192, y0 + 52),
               (x0 + 228, y0 + 48), (x0 + 264, y0 + 66), (x0 + 300, y0 + 62)]
        d.line(pts, fill=(255, 90, 70), width=3, joint="curve")
        d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
                   (pts[-1][0] - 2, pts[-1][1] + 12)], fill=(255, 90, 70))
        rows = [("TAIPEI", "\u22126.2%"), ("SEOUL", "\u22125.2%"),
                ("TOKYO", "\u22125.1%"), ("HONG KONG", "\u22121.9%")]
        ty = y0 + h - 52
        d.rectangle([x0 + 10, ty - 4, x1 - 10, y0 + h - 6], fill=(70, 16, 16))
        for j, (city, val) in enumerate(rows):
            yy = ty + j * 12
            d.text((x0 + 16, yy), city, font=F_BOLD(9), fill=(235, 235, 235))
            d.text((x1 - 62, yy), val, font=F_BOLD(9), fill=(255, 120, 100))
        d.text((x0 + 8, y0 + 6), "ASIA \u2014 FRIDAY'S CLOSES", font=F_BOLD(9),
               fill=(255, 200, 190))


def draw_card_art(d, kind, x0, y0, x1, y1):
    """Small flat-vector icon for a card inside (x0,y0,x1,y1)."""
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w // 2, y0 + h // 2
    white = (245, 245, 245)
    if kind == "flags":
        d.rectangle([x0 + 52, y0 + 8, x0 + 118, y0 + h - 8], fill=(20, 40, 90))
        d.line([(x0 + 52, cy), (x0 + 118, cy)], fill=(255, 255, 255), width=6)
        d.line([(x0 + 85, y0 + 8), (x0 + 85, y0 + h - 8)], fill=(255, 255, 255), width=6)
        d.line([(x0 + 52, cy), (x0 + 118, cy)], fill=(200, 30, 30), width=3)
        d.line([(x0 + 85, y0 + 8), (x0 + 85, y0 + h - 8)], fill=(200, 30, 30), width=3)
        d.rectangle([x0 + 126, y0 + 8, x0 + 192, y0 + h - 8], fill=(0, 50, 150))
        for k in range(12):
            import math
            a = k * math.pi / 6
            d.ellipse([x0 + 159 + 12 * math.cos(a) - 2, cy + 9 * math.sin(a) - 2,
                       x0 + 159 + 12 * math.cos(a) + 2, cy + 9 * math.sin(a) + 2],
                      fill=(255, 210, 0))
    elif kind == "globe":
        d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline=white, width=3)
        d.ellipse([cx - 8, cy - 18, cx + 8, cy + 18], outline=white, width=2)
        d.line([(cx - 18, cy), (cx + 18, cy)], fill=white, width=2)
        d.rectangle([x0 + w - 34, y0 + 8, x0 + w - 26, y0 + h - 8], fill=white)
        d.ellipse([x0 + w - 38, y0 + 4, x0 + w - 22, y0 + 20], fill=(255, 80, 60))
    elif kind == "jet":
        d.polygon([(x0 + 40, cy - 4), (x0 + 150, cy - 10), (x0 + 168, cy),
                   (x0 + 150, cy + 10), (x0 + 40, cy + 4)], fill=white)
        d.polygon([(x0 + 90, cy - 4), (x0 + 110, cy - 20), (x0 + 122, cy - 4)],
                  fill=white)
        d.polygon([(x0 + 90, cy + 4), (x0 + 110, cy + 20), (x0 + 122, cy + 4)],
                  fill=white)
        d.line([(x0 + 20, cy + 14), (x0 + 44, cy + 2)], fill=(255, 120, 80), width=3)
    elif kind == "cpi":
        d.ellipse([cx - 52, cy - 18, cx - 16, cy + 18], outline=white, width=3)
        d.line([(cx - 46, cy + 8), (cx - 38, cy - 2), (cx - 30, cy - 8),
                (cx - 22, cy - 14)], fill=(255, 120, 90), width=3)
        d.polygon([(cx - 22, cy - 14), (cx - 30, cy - 14), (cx - 22, cy - 6)],
                  fill=(255, 120, 90))
        d.text((cx - 8, cy - 11), "2.2%", font=F_BOLD(17), fill=white)
    elif kind == "court":
        d.rectangle([x0 + 52, y0 + 10, x0 + 192, y0 + 16], fill=white)
        for px in [62, 92, 122, 152, 178]:
            d.rectangle([px, y0 + 16, px + 8, y0 + h - 10], fill=white)
        d.rectangle([x0 + 48, y0 + h - 10, x0 + 196, y0 + h - 6], fill=white)
    elif kind == "forest":
        # Three rainforest trees (unused after the Raoni card was replaced).
        for tx, top, base in [(76, 8, 34), (116, 2, 42), (156, 10, 30)]:
            d.polygon([(tx, y0 + top), (tx + 14, y0 + base), (tx - 14, y0 + base)],
                      fill=white)
            d.rectangle([tx - 3, y0 + base, tx + 3, y0 + h - 6], fill=white)
    elif kind == "ballot":
        d.rectangle([x0 + 66, y0 + 16, x0 + 178, y0 + h - 8], fill=white)
        d.rectangle([x0 + 88, y0 + 8, x0 + 156, y0 + 16], fill=(200, 30, 30))
        d.line([(x0 + 100, cy + 2), (x0 + 116, cy + 14), (x0 + 146, cy - 12)],
               fill=(46, 96, 58), width=4)
    elif kind == "crowd":
        for hx in [62, 92, 122, 152, 182]:
            d.ellipse([hx - 8, y0 + 12, hx + 8, y0 + 28], fill=white)
            d.pieslice([hx - 12, y0 + 28, hx + 12, y0 + h - 6], 180, 360, fill=white)
        d.rectangle([x0 + 30, y0 + 6, x0 + 52, y0 + 22], fill=(255, 210, 0))
    elif kind == "boat":
        d.polygon([(x0 + 48, cy + 2), (x0 + 196, cy + 2), (x0 + 176, cy + 16),
                   (x0 + 68, cy + 16)], fill=white)
        d.line([(x0 + 122, cy + 2), (x0 + 122, cy - 16)], fill=white, width=3)
        d.polygon([(x0 + 122, cy - 16), (x0 + 150, cy - 2), (x0 + 122, cy - 2)],
                  fill=(255, 210, 0))
        d.line([(x0 + 40, y0 + h - 8), (x0 + 204, y0 + h - 8)], fill=white, width=2)
    elif kind == "mega":
        d.polygon([(x0 + 60, cy - 6), (x0 + 150, cy - 18), (x0 + 150, cy + 18),
                   (x0 + 60, cy + 6)], fill=white)
        d.rectangle([x0 + 48, cy - 12, x0 + 60, cy + 12], fill=white)
        d.line([(x0 + 150, cy - 18), (x0 + 168, cy - 26)], fill=white, width=3)
        d.line([(x0 + 150, cy), (x0 + 172, cy)], fill=white, width=3)
        d.line([(x0 + 150, cy + 18), (x0 + 168, cy + 26)], fill=white, width=3)
    elif kind == "ball":
        # Soccer ball: white ring, pentagon, seams.
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=white, width=3)
        d.polygon([(cx, cy - 7), (cx + 7, cy - 2), (cx + 4, cy + 7),
                   (cx - 4, cy + 7), (cx - 7, cy - 2)], fill=white)
        d.line([(cx, cy - 16), (cx, cy - 7)], fill=white, width=2)
        d.line([(cx + 15, cy - 5), (cx + 7, cy - 2)], fill=white, width=2)
        d.line([(cx - 15, cy - 5), (cx - 7, cy - 2)], fill=white, width=2)
        d.line([(cx + 10, cy + 13), (cx + 4, cy + 7)], fill=white, width=2)
        d.line([(cx - 10, cy + 13), (cx - 4, cy + 7)], fill=white, width=2)
    elif kind == "car":
        # Side-on car: cabin + body + two dark wheels.
        d.polygon([(x0 + 56, cy + 4), (x0 + 78, cy - 12), (x0 + 128, cy - 12),
                   (x0 + 148, cy + 4)], fill=white)
        d.rectangle([x0 + 44, cy + 2, x0 + 160, cy + 12], fill=white)
        d.ellipse([x0 + 62, cy + 8, x0 + 80, cy + 24], fill=(30, 30, 30))
        d.ellipse([x0 + 124, cy + 8, x0 + 142, cy + 24], fill=(30, 30, 30))
    else:  # cricket
        d.line([(x0 + 60, y0 + 10), (x0 + 96, y0 + h - 12)], fill=(210, 170, 110), width=10)
        d.ellipse([x0 + 150, cy - 10, x0 + 170, cy + 10], fill=(200, 30, 30))
        d.text((x0 + 108, y0 + 8), "118", font=F_BOLD(20), fill=white)


# ------------------------------------------------------------------ draw page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 12  # side margin
    X1 = W - M

    # ---- masthead ----
    d.text((M, 8), "THE WORLD IN ONE DAY", font=F_BOLD(13), fill=RED)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 ALL DATED FRIDAY 20 NOVEMBER 2026"
    d.text((X1 - d.textlength(right, font=F_BOLD(9)), 11), right,
           font=F_BOLD(9), fill=MUTED)
    title = "Friday 20 November 2026"
    tf = F_SERIF(56)
    while d.textlength(title, font=tf) > X1 - M and tf.size > 30:
        tf = F_SERIF(tf.size - 2)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title, font=tf, fill=INK)
    hline(d, M, X1, 96, fill=RED, width=2)
    deck = DECK
    df = F_SERIF_IT(14)
    d.text(((W - d.textlength(deck, font=df)) / 2, 102), deck, font=df, fill=RED)
    hline(d, M, X1, 124, fill=INK, width=1)

    # ---- stat strip: 6 cells ----
    sw = (X1 - M) / 6
    y = 130
    for i, (num, label) in enumerate(STATS):
        x = M + i * sw
        if i:
            d.line([(x, y), (x, y + 40)], fill=LINE, width=1)
        nf = F_BOLD(17)
        while d.textlength(num, font=nf) > sw - 12 and nf.size > 11:
            nf = F_BOLD(nf.size - 1)
        d.text((x + 6, y), num, font=nf, fill=RED)
        para(d, x + 6, y + 22, label, F_SANS(9), sw - 12, fill=MUTED,
             leading=11, max_lines=2)
    hline(d, M, X1, 176, fill=LINE, width=1)

    # ---- region bar ----
    total = sum(c for _, c, _ in REGIONS)
    y = 182
    d.text((M, y + 2), "STORIES BY REGION", font=F_BOLD(9), fill=MUTED)
    bx = M + 128
    bw = X1 - bx
    x = bx
    for name, count, color in REGIONS:
        seg = bw * count / total
        d.rectangle([x, y, x + seg - 1, y + 16], fill=color)
        lab = f"{name} {count}"
        lf = F_BOLD(9)
        if d.textlength(lab, font=lf) <= seg - 6:
            d.text((x + (seg - d.textlength(lab, font=lf)) / 2, y + 3),
                   lab, font=lf, fill=(255, 255, 255))
        x += seg
    # legend line: colour square + name for every segment (small ones included)
    lx = M + 128
    for name, count, color in REGIONS:
        d.rectangle([lx, y + 21, lx + 8, y + 29], fill=color)
        lab = f"{name} {count}"
        d.text((lx + 11, y + 20), lab, font=F_BOLD(8), fill=MUTED)
        lx += 11 + d.textlength(lab, font=F_BOLD(8)) + 12
    hline(d, M, X1, 212, fill=INK, width=1)

    # ---- leads: 3 columns ----
    lw = (X1 - M - 24) / 3
    ly = 218
    art_h = 96
    for i, lead in enumerate(LEADS):
        x = M + i * (lw + 12)
        d.rectangle([x, ly, x + lw, ly + art_h], outline=LINE, width=1)
        draw_lead_art(d, lead["num"], x + 1, ly + 1, x + lw - 1, ly + art_h - 1)
        chip = lead["chip"]
        cf = F_BOLD(8)
        tw = d.textlength(chip, font=cf)
        # lead 3's table fills the art bottom, so its chip goes top-right
        cy0 = ly + 4 if lead["num"] == 3 else ly + art_h - 16
        d.rectangle([x + lw - tw - 12, cy0, x + lw - 2, cy0 + 14],
                    fill=(255, 255, 255))
        d.text((x + lw - tw - 8, cy0 + 2), chip, font=cf, fill=INK)
        ty = ly + art_h + 6
        d.text((x, ty), f"{lead['num']}  ", font=F_BOLD(11), fill=RED)
        kx = x + d.textlength(f"{lead['num']}  ", font=F_BOLD(11))
        d.text((kx, ty), lead["kicker"], font=F_BOLD(10), fill=RED)
        ty += 16
        ty = fit_para(d, x, ty, lead["head"], F_SERIF, 17, lw, 3, fill=INK,
                      leading=19)
        ty += 2
        para(d, x, ty, lead["deck"], F_SANS(10), lw, fill=INK, leading=12,
             max_lines=2)
    hline(d, M, X1, 402, fill=LINE, width=1)

    # ---- cards: 2 rows x 5 ----
    cw = (X1 - M - 44) / 5
    ch = 118
    for r in range(2):
        for c in range(5):
            card = CARDS[r * 5 + c]
            x = M + c * (cw + 11)
            y0 = 408 + r * (ch + 8)
            d.rectangle([x, y0, x + cw, y0 + ch], fill=CARD_BG, outline=LINE, width=1)
            ax0, ay0, ax1, ay1 = x + 1, y0 + 1, x + cw - 1, y0 + 52
            d.rectangle([ax0, ay0, ax1, ay1], fill=card["bg"])
            draw_card_art(d, card["art"], ax0, ay0, ax1, ay1)
            ty = y0 + 56
            d.text((x + 5, ty), f"{card['num']}  {card['kicker']}", font=F_BOLD(8),
                   fill=RED)
            ty += 12
            ty = fit_para(d, x + 5, ty, card["head"], F_SERIF, 12, cw - 10, 2,
                          fill=INK)
            para(d, x + 5, ty + 1, card["deck"], F_SANS(9), cw - 10,
                 fill=MUTED, leading=11, max_lines=2)

    # ---- bottom: map (left) + briefs (right) ----
    hline(d, M, X1, 656, fill=INK, width=1)
    d.text((M, 662), "WHERE IT HAPPENED", font=F_BOLD(12), fill=INK)
    d.text((432, 662), "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES",
           font=F_BOLD(12), fill=INK)
    # map panel
    mx, my, mw, mh = M, 682, 404, 272
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA)
    s = mw / 360.0
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, s) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for num, (lon, lat) in sorted(PINS.items()):
        px, py = project(lon, lat, mx, my, s)
        dx, dy = NUDGE.get(num, (0, 0))
        bx, by = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
            d.line([(px, py), (bx, by)], fill=(255, 255, 255), width=1)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        nf = F_BOLD(9)
        t = str(num)
        d.text((bx - d.textlength(t, font=nf) / 2, by - 6), t, font=nf,
               fill=(255, 255, 255))
    d.text((mx + 2, my + mh - 26),
           "Each number is the story with that number on this page.",
           font=F_SANS(8), fill=(220, 228, 240))
    # briefs: two columns of 11
    bw2 = (X1 - 432 - 12) / 2
    for j, (num, city, text) in enumerate(BRIEFS):
        col = j // 11
        row = j % 11
        x = 432 + col * (bw2 + 12)
        y = 682 + row * 24
        nf = F_BOLD(10)
        d.text((x, y), str(num), font=nf, fill=RED)
        rest = f"{city} \u2014 {text}"
        rx = x + d.textlength(f"{num} ", font=nf)
        para(d, rx, y, rest, F_SANS(9), x + bw2 - rx, fill=INK, leading=11,
             max_lines=2)
    hline(d, M, X1, 682 + 11 * 24 + 2, fill=LINE, width=1)

    # ---- date check ----
    by = 682 + 11 * 24 + 8
    d.rectangle([M, by, X1, by + 40], outline=RED, width=2)
    d.text((M + 8, by + 4), "DATE CHECK", font=F_BOLD(10), fill=RED)
    para(d, M + 88, by + 4, DATE_CHECK_1, F_SANS(9), X1 - M - 96, fill=INK,
         leading=11, max_lines=1)
    para(d, M + 88, by + 22, DATE_CHECK_2, F_SANS(9), X1 - M - 96, fill=INK,
         leading=11, max_lines=1)

    # ---- footer ----
    fy = by + 46
    para(d, M, fy, FOOTER, F_SANS(8), X1 - M, fill=MUTED, leading=10,
         max_lines=2)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    build()
