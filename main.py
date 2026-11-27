#!/usr/bin/env python3
"""THE WORLD TODAY - Friday 27 November 2026.

A one-page newspaper front page summing up the world's news of
Friday 27 November 2026: 32 stories, 6 regions. Written from
scratch in this session with the Python standard library only.
A Surface owns a flat RGB pixel buffer; text is set in a hand
drawn 5x7 bitmap font (each glyph stored as seven pipe separated
rows); a small PNG encoder writes the file. No network, no clock,
no randomness, so every run writes the same bytes. The program
writes a 1024x1024 PNG.
"""

import binascii
import os
import struct
import sys
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GREY = (96, 92, 82)
PALE = (233, 228, 214)
SEA = (214, 226, 232)
LAND = (198, 206, 178)
COAST = (110, 118, 92)


# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, drawn by hand in this session. Each glyph is
# one string of seven rows separated by '|'. '#' is ink, '.' empty.
# All page text is set in capitals, newspaper style.

FONT = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#",
    "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".####|#....|#....|#....|#....|#....|.####",
    "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####",
    "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".####|#....|#....|#..##|#...#|#...#|.###.",
    "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": ".###.|..#..|..#..|..#..|..#..|..#..|.###.",
    "J": "..###|...#.|...#.|...#.|...#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
    "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
    "N": "#...#|##..#|#.#.#|#..##|#...#|#...#|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
    "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.",
    "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
    "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#",
    "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
    "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.",
    "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    "2": ".###.|#...#|....#|...#.|..#..|.#...|#####",
    "3": "####.|....#|....#|.###.|....#|....#|####.",
    "4": "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.",
    "5": "#####|#....|####.|....#|....#|#...#|.###.",
    "6": ".###.|#....|#....|####.|#...#|#...#|.###.",
    "7": "#####|....#|...#.|..#..|..#..|..#..|..#..",
    "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.",
    "9": ".###.|#...#|#...#|.####|....#|....#|.###.",
    " ": ".....|.....|.....|.....|.....|.....|.....",
    ".": ".....|.....|.....|.....|.....|..##.|..##.",
    ",": ".....|.....|.....|.....|..##.|..#..|.#...",
    "-": ".....|.....|.....|#####|.....|.....|.....",
    "'": "..#..|..#..|.....|.....|.....|.....|.....",
    "!": "..#..|..#..|..#..|..#..|..#..|.....|..#..",
    "?": ".###.|#...#|....#|...#.|..#..|.....|..#..",
    "/": "....#|....#|...#.|..#..|.#...|#....|#....",
    "(": "...#.|..#..|.#...|.#...|.#...|..#..|...#.",
    ")": ".#...|..#..|...#.|...#.|...#.|..#..|.#...",
    "%": "#...#|#..#.|...#.|..#..|.#...|#..#.|#...#",
    "+": ".....|..#..|..#..|#####|..#..|..#..|.....",
    "&": ".##..|#..#.|#..#.|.#...|#.#.#|#..#.|.##.#",
    "=": ".....|.....|#####|.....|#####|.....|.....",
    ";": ".....|..##.|..##.|.....|..##.|..#..|.#...",
    ":": ".....|..##.|..##.|.....|..##.|..##.|.....",
    "*": ".....|.#.#.|..#..|#####|..#..|.#.#.|.....",
    '"': ".#.#.|.#.#.|.....|.....|.....|.....|.....",
    "_": ".....|.....|.....|.....|.....|.....|#####",
    "<": "....#|...#.|..#..|.#...|..#..|...#.|....#",
    ">": "#....|.#...|..#..|...#.|..#..|.#...|#....",
    "$": "..#..|.####|#.#.#|.###.|..#.#|####.|..#..",
    "@": ".###.|#...#|#.###|#.#.#|#.###|#....|.###.",
    "[": ".###.|.#...|.#...|.#...|.#...|.#...|.###.",
    "]": ".###.|...#.|...#.|...#.|...#.|...#.|.###.",
}

BLANK = ".....|.....|.....|.....|.....|.....|....."


def glyph_rows(ch):
    """Return the seven rows of a glyph, blank for unknown chars."""
    return FONT.get(ch, BLANK).split("|")


# ------------------------------------------------------------ surface

class Surface:
    """A flat RGB pixel buffer with newspaper drawing helpers."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        self.rect(0, 0, w, h, bg)

    def set(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = col[0]
            self.buf[i + 1] = col[1]
            self.buf[i + 2] = col[2]

    def rect(self, x, y, w, h, col):
        x0 = max(x, 0)
        x1 = min(x + w, self.w)
        for yy in range(max(y, 0), min(y + h, self.h)):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                self.buf[base] = col[0]
                self.buf[base + 1] = col[1]
                self.buf[base + 2] = col[2]
                base += 3

    def hline(self, x, y, w, col, t=1):
        self.rect(x, y, w, t, col)

    def vline(self, x, y, h, col, t=1):
        self.rect(x, y, t, h, col)

    def border(self, x, y, w, h, col, t=1):
        self.hline(x, y, w, col, t)
        self.hline(x, y + h - t, w, col, t)
        self.vline(x, y, h, col, t)
        self.vline(x + w - t, y, h, col, t)

    def line(self, x0, y0, x1, y1, col):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.set(x, y, col)
            if x == x1 and y == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, col):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, col)

    def polyfill(self, pts, col):
        if len(pts) < 3:
            return
        top = min(p[1] for p in pts)
        bot = max(p[1] for p in pts)
        n = len(pts)
        for y in range(top, bot + 1):
            xs = []
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                for xx in range(int(xs[k]), int(xs[k + 1]) + 1):
                    self.set(xx, y, col)

    def polyline(self, pts, col):
        n = len(pts)
        for i in range(n):
            self.line(pts[i][0], pts[i][1],
                      pts[(i + 1) % n][0], pts[(i + 1) % n][1], col)


# ------------------------------------------------------------ text out

def draw_char(sf, x, y, ch, scale, col):
    rows = glyph_rows(ch)
    for r in range(7):
        row = rows[r]
        for c in range(5):
            if row[c] == "#":
                sf.rect(x + c * scale, y + r * scale, scale, scale, col)


def text_width(s, scale):
    return len(s) * 6 * scale


def draw_text(sf, x, y, s, scale, col, bold=False):
    s = s.upper()
    cx = x
    for ch in s:
        draw_char(sf, cx, y, ch, scale, col)
        if bold:
            draw_char(sf, cx + max(1, scale // 2), y, ch, scale, col)
        cx += 6 * scale
    return cx


def draw_text_centre(sf, cx, y, s, scale, col, bold=False):
    draw_text(sf, cx - text_width(s, scale) // 2, y, s, scale, col, bold)


def draw_text_right(sf, rx, y, s, scale, col, bold=False):
    draw_text(sf, rx - text_width(s, scale), y, s, scale, col, bold)


def wrap_text(s, scale, maxw):
    words = s.upper().split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if text_width(trial, scale) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_para(sf, x, y, s, scale, maxw, col, max_lines=None, leading=None):
    if leading is None:
        leading = 7 * scale + 3
    lines = wrap_text(s, scale, maxw)
    if max_lines is not None:
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        draw_text(sf, x, y + i * leading, ln, scale, col)
    return y + len(lines) * leading


def draw_para_centre(sf, cx, y, s, scale, maxw, col, max_lines=None):
    lines = wrap_text(s, scale, maxw)
    if max_lines is not None:
        lines = lines[:max_lines]
    leading = 7 * scale + 3
    for i, ln in enumerate(lines):
        draw_text_centre(sf, cx, y + i * leading, ln, scale, col)
    return y + len(lines) * leading


# ------------------------------------------------------------ png out

def png_chunk(kind, data):
    crc = binascii.crc32(kind + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)


def png_bytes(sf):
    raw = bytearray()
    for y in range(sf.h):
        raw.append(0)
        raw.extend(sf.buf[y * sf.w * 3:(y + 1) * sf.w * 3])
    comp = zlib.compress(bytes(raw), 9)
    head = struct.pack(">IIBBBBB", sf.w, sf.h, 8, 2, 0, 0, 0)
    out = b"\x89PNG\r\n\x1a\n"
    out += png_chunk(b"IHDR", head)
    out += png_chunk(b"IDAT", comp)
    out += png_chunk(b"IEND", b"")
    return out


def save_png(sf, path):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_bytes(sf))


# ------------------------------------------------------------ the news
# All 32 stories happened, or were first reported, on Friday
# 27 November 2026 (see SOURCES.md). Three leads, sixteen briefs,
# thirteen also. Six regions: Europe 7, Asia-Pacific 17,
# South Asia 4, Middle East 2, Africa 1, Americas/global 1.

LEADS = [
    (
        "JAPAN - INFLATION",
        "TOKYO INFLATION JUMPS TO 2.9%",
        "TOKYO CORE INFLATION HITS 2.9%, THE FASTEST IN 16 MONTHS "
        "AND ABOVE THE BANK OF JAPAN'S 2% TARGET FOR A THIRD "
        "MONTH. A RATE HIKE IS EXPECTED IN DECEMBER.",
    ),
    (
        "EUROPE - DEFENCE",
        "FIVE NATIONS SIGN 7.5BN EURO CV90 DEAL",
        "FINLAND, SWEDEN, NORWAY, LITHUANIA AND THE NETHERLANDS "
        "JOINTLY BUY MORE THAN 430 CV90 FIGHTING VEHICLES FROM "
        "BAE SYSTEMS. FINLAND TAKES 160 FOR 2.8 BILLION EUROS.",
    ),
    (
        "NEW ZEALAND - ELECTION",
        "NZ ELECTION ENDS IN DEADLOCK",
        "THE FINAL COUNT ERASES THE COALITION'S MAJORITY: 65 "
        "SEATS EACH IN A 130-SEAT PARLIAMENT. OPPORTUNITY'S "
        "SEVEN MPS HOLD THE BALANCE OF POWER. LABOUR FLIPS "
        "WAIRARAPA AND HAMILTON EAST.",
    ),
]

NUMBERS = [
    ("+2.9%", "TOKYO CORE CPI, FASTEST IN 16 MONTHS"),
    ("430+", "CV90 VEHICLES IN FIVE-NATION DEAL"),
    ("561BN", "EUROS: GERMAN 2027 BUDGET, FINAL VOTE"),
    ("64,141", "UK VEHICLES BUILT IN OCTOBER"),
    ("40,000", "SCHOOL WORKERS EXPECTED IN SEOUL"),
    ("65-65", "NZ PARLIAMENT DEADLOCKED AFTER FINAL COUNT"),
]

BRIEFS = [
    ("BUNDESTAG VOTES ON BUDGET",
     "GERMANY'S PARLIAMENT VOTES ON A RECORD 2027 BUDGET OF "
     "560.9 BILLION EUROS, WITH 123 BILLION OF NEW BORROWING."),
    ("MODI CHAIRS CABINET",
     "PM MODI CHAIRS A 1PM CABINET MEETING TO CLEAR THE WOMEN'S "
     "RESERVATION BILL BEFORE PARLIAMENT SITS."),
    ("MURMU BEGINS TOUR",
     "PRESIDENT DROUPADI MURMU BEGINS A SIX-DAY VISIT TO KERALAM, "
     "MIZORAM AND NAGALAND, RUNNING TO 2 DECEMBER."),
    ("POLAND SIGNS PALANTIR DEAL",
     "POLAND SIGNS A DEAL WITH PALANTIR FOR AI SOFTWARE TO "
     "SUPPORT MILITARY DECISIONS. NO VALUE DISCLOSED."),
    ("FINLAND SIGNS BORDER LAW",
     "PRESIDENT STUBB SIGNS A TWO-YEAR EXTENSION OF THE BORDER "
     "SECURITY LAW, IN FORCE UNTIL THE END OF 2028."),
    ("RHEINMETALL TARGETS DUE",
     "RHEINMETALL PRESENTS REVISED TARGETS AT 10:00 CET; "
     "ANALYSTS EXPECT A CUT FROM 50BN EUROS OF 2030 REVENUE."),
    ("N. KOREA BORDER CROSSINGS",
     "NORTH KOREAN TROOPS CROSSED THE BORDER ABOUT 40 TIMES IN "
     "OCTOBER AND NOVEMBER DESPITE WARNING SHOTS."),
    ("S. KOREA BANS AI DOCTORS",
     "SOUTH KOREA BANS AI-GENERATED DOCTORS IN ADS FOR "
     "SUPPLEMENTS, MEDICINES AND COSMETICS FROM TODAY."),
    ("ASIAN STOCKS SLIP",
     "ASIAN STOCKS SLIP AFTER A HIGHER OPEN: THE NIKKEI GIVES "
     "UP A 0.30% GAIN AND THE KOSPI A 0.37% GAIN."),
    ("UK AUTO OUTPUT +4.8%",
     "UK CAR PRODUCTION RISES 4.8% IN OCTOBER TO 64,141 "
     "VEHICLES; CAR EXPORTS JUMP 14.2%."),
    ("FLIGHT CENTRE BREACH",
     "FLIGHT CENTRE INVESTIGATES A BREACH OF A THIRD-PARTY "
     "BOOKING SYSTEM; CUSTOMER RECORDS MAY HAVE BEEN ACCESSED."),
    ("SEOUL SCHOOL WORKERS RALLY",
     "ABOUT 40,000 SCHOOL WORKERS ARE EXPECTED TO RALLY IN "
     "YEOUIDO, SEOUL, IN A ONE-DAY STRIKE."),
    ("MELENCHON SPEAKS IN BERLIN",
     "JEAN-LUC MELENCHON SPEAKS IN BERLIN THIS EVENING; MORE "
     "THAN 2,000 PEOPLE HAVE REGISTERED TO ATTEND."),
    ("SEOUL GUESTHOUSE FIRE",
     "A FIRE AT A GUESTHOUSE IN JUNG-GU, SEOUL, AT 04:46 KILLS "
     "A MAN IN HIS 70S AND INJURES ANOTHER."),
    ("BOK WARNS ON AI SLOWDOWN",
     "SOUTH KOREA'S CENTRAL BANK WARNS GROWTH FALLS BACK TO 2% "
     "IF THE AI BUILDOUT SLOWS."),
    ("HALF OF S. KOREA BUSES ACCESSIBLE",
     "OVER HALF OF SOUTH KOREA'S PUBLIC BUSES ARE NOW "
     "WHEELCHAIR-ACCESSIBLE, AT 51.8%, UP 7.4 POINTS IN A YEAR."),
]

ALSO = [
    "20. BLACK FRIDAY: SALES BEGIN; 1 IN 3 SHOPPERS PLAN TO USE AI",
    "21. NZ-INDIA 2ND TEST, DAY 1: NZ 77-1 AT LUNCH; BRAR DEBUTS",
    "22. QATAR GP: PRACTICE 1 AND 2 AT LUSAIL; RACE ON SUNDAY",
    "23. ILT20: SHARJAH WARRIORZ V DUBAI CAPITALS, 6:30PM GST",
    "24. WOMEN'S HOCKEY SEMIS: INDIA V MALAYSIA, 19:00 IST",
    "25. JOHANNESBURG ELECTS A MAYOR; ZILLE V MASHABA",
    "26. AIR NZ TO WEIGH CARRY-ON BAGS AT THE GATE",
    "27. NZ TEST: 1 IN 5 AI-QUOTED BLACK FRIDAY PRICES WRONG",
    "28. ENDANGERED FROGS FOUND IN INCHEON WETLAND",
    "29. 'WHITE BLAST' TOPS KOREAN BOX OFFICE, 9TH DAY",
    "30. KIM YONG-BEOM TO LEAD REFORM COMMITTEE",
    "31. BAL VIVAH MUKT BHARAT: CHILD-MARRIAGE-FREE INDIA EVENT",
    "32. CHINA CUTS FUEL PRICES FROM MIDNIGHT; PETROL -440 YUAN/T",
]

# Schematic continents inside the map box, rough polygons.
CONTINENTS = [
    [(70, 365), (150, 355), (230, 360), (250, 380), (210, 405),
     (170, 420), (120, 415), (75, 395)],
    [(235, 428), (275, 422), (295, 445), (275, 478), (250, 472),
     (232, 450)],
    [(475, 358), (520, 352), (545, 360), (540, 378), (510, 385),
     (480, 375)],
    [(485, 392), (530, 388), (555, 405), (545, 445), (520, 468),
     (495, 450), (482, 420)],
    [(560, 355), (650, 348), (750, 355), (785, 372), (760, 398),
     (700, 412), (640, 408), (585, 395), (558, 375)],
    [(705, 448), (745, 442), (765, 452), (750, 470), (715, 472)],
    [(800, 452), (815, 450), (818, 462), (805, 466)],
]

# (x, y, label, label dx, label dy) - places in the day's news.
PLACES = [
    (480, 368, "LONDON", -60, -3),
    (505, 364, "BERLIN", -8, 12),
    (528, 358, "WARSAW", 8, -3),
    (500, 352, "STOCKHOLM", -66, -3),
    (520, 448, "JOHANNESBURG", 8, -3),
    (640, 388, "NEW DELHI", 8, -3),
    (592, 396, "LUSAIL", -54, 10),
    (700, 368, "BEIJING", 8, -3),
    (728, 376, "SEOUL", 8, 10),
    (752, 378, "TOKYO", 8, -3),
    (812, 460, "WELLINGTON", 8, -3),
]

# ------------------------------------------------------------ layout
MARGIN = 28
RIGHT = 996


def section_head(sf, y, text, note=None):
    draw_text(sf, MARGIN, y, text, 2, RED, bold=True)
    if note:
        draw_text_right(sf, RIGHT, y + 3, note, 1, GREY)
    sf.hline(MARGIN, y + 20, RIGHT - MARGIN, INK, 2)


def masthead(sf):
    sf.rect(0, 0, W, 6, INK)
    draw_text_centre(sf, W // 2, 16, "THE WORLD TODAY", 7, INK)
    draw_text(sf, MARGIN, 38, "VOL. II", 1, GREY)
    draw_text_right(sf, RIGHT, 38, "FRIDAY EDITION", 1, GREY)
    sf.hline(MARGIN, 74, RIGHT - MARGIN, INK, 3)
    sf.hline(MARGIN, 79, RIGHT - MARGIN, RED, 1)
    draw_text(sf, MARGIN, 88, "FRIDAY 27 NOVEMBER 2026", 2, INK, bold=True)
    draw_text_right(sf, RIGHT, 88, "32 STORIES - 6 REGIONS", 2, INK, bold=True)
    sf.hline(MARGIN, 108, RIGHT - MARGIN, INK, 1)


def numbers_strip(sf):
    y = 116
    box_w = 156
    gap = 6
    for i, (big, label) in enumerate(NUMBERS):
        x = MARGIN + i * (box_w + gap)
        sf.border(x, y, box_w, 54, GREY, 1)
        draw_text_centre(sf, x + box_w // 2, y + 6, big, 2, RED, bold=True)
        draw_para_centre(sf, x + box_w // 2, y + 27, label, 1,
                         box_w - 10, GREY, max_lines=2)


def leads_section(sf):
    section_head(sf, 178, "THE LEADS")
    xs = [28, 357, 686]
    for col, (kicker, head, body) in enumerate(LEADS):
        x = xs[col]
        draw_text(sf, x, 206, kicker, 1, RED, bold=True)
        draw_para(sf, x, 218, head, 2, 310, INK, max_lines=2, leading=17)
        draw_para(sf, x, 256, body, 1, 310, INK, max_lines=5, leading=10)
    sf.vline(347, 206, 100, PALE, 1)
    sf.vline(676, 206, 100, PALE, 1)


def map_section(sf):
    section_head(sf, 322, "WHERE IT HAPPENED", "SCHEMATIC MAP - NOT TO SCALE")
    sf.border(MARGIN, 342, RIGHT - MARGIN, 146, INK, 1)
    sf.rect(MARGIN + 1, 343, RIGHT - MARGIN - 2, 144, SEA)
    for poly in CONTINENTS:
        sf.polyfill(poly, LAND)
        sf.polyline(poly, COAST)
    draw_text(sf, 95, 392, "N. AMERICA", 1, GREY)
    draw_text(sf, 232, 455, "S. AMERICA", 1, GREY)
    draw_text(sf, 495, 420, "AFRICA", 1, GREY)
    draw_text(sf, 660, 360, "ASIA", 1, GREY)
    draw_text(sf, 705, 462, "AUSTRALIA", 1, GREY)
    for (dx, dy, label, lx, ly) in PLACES:
        sf.circle(dx, dy, 5, INK)
        sf.circle(dx, dy, 3, RED)
        draw_text(sf, dx + lx, dy + ly, label, 1, INK, bold=True)


def briefs_section(sf):
    section_head(sf, 496, "THE DAY IN BRIEF - 16 STORIES")
    xs = [28, 273, 518, 763]
    ys = [522, 592, 662, 732]
    for i, (head, body) in enumerate(BRIEFS):
        col = i % 4
        row = i // 4
        x = xs[col]
        y = ys[row]
        draw_text(sf, x, y, "%02d" % (i + 4), 1, RED, bold=True)
        draw_para(sf, x + 20, y, head, 1, 213, INK, max_lines=2, leading=10)
        draw_para(sf, x, y + 22, body, 1, 233, INK, max_lines=3, leading=10)
    for vx in (261, 506, 751):
        sf.vline(vx, 522, 276, PALE, 1)
    for hy in (588, 658, 728):
        sf.hline(MARGIN, hy, RIGHT - MARGIN, PALE, 1)


def also_section(sf):
    section_head(sf, 806, "ALSO ON FRIDAY 27 NOVEMBER")
    for i, item in enumerate(ALSO):
        col = i // 7
        row = i % 7
        x = MARGIN if col == 0 else 524
        draw_text(sf, x, 832 + row * 19, item, 1, INK)


def footer_section(sf):
    sf.hline(MARGIN, 970, RIGHT - MARGIN, INK, 2)
    draw_para(sf, MARGIN, 978,
              "DATE CHECK: TOKYO CPI RELEASED 23:42 UTC 26 NOV (FRI "
              "MORNING TOKYO). NZ RESULTS OUT 2PM NZDT. CHINA FUEL "
              "CUT ANNOUNCED 26 NOV, IN FORCE FROM 00:00 ON 27 NOV. "
              "WHITE BLAST FIGURES ARE THU 26 NOV, REPORTED FRI. "
              "CV90, PALANTIR AND BUNDESTAG ARE SCHEDULED EVENTS ON "
              "27 NOV, ANNOUNCED 26 NOV.",
              1, RIGHT - MARGIN, INK, max_lines=2, leading=10)
    draw_text(sf, MARGIN, 1002,
              "SOURCES: REUTERS, FARMERS WEEKLY, RNZ, FINNISH "
              "GOVERNMENT, SMMT, AJP, HOCKEY INDIA, FORMULA1.COM - "
              "SEE SOURCES.MD",
              1, GREY)


def build_page():
    sf = Surface(W, H, PAPER)
    masthead(sf)
    numbers_strip(sf)
    leads_section(sf)
    map_section(sf)
    briefs_section(sf)
    also_section(sf)
    footer_section(sf)
    return sf


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    save_png(build_page(), out)


if __name__ == "__main__":
    main()
