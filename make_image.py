#!/usr/bin/env python3
"""Generate entry.png: the world news of Thursday 19 November 2026 in one image.
Stories per the day's wire reporting (Reuters, AP, AFP, BBC, Al Jazeera, WSJ).
Deterministic, no network, no assets — everything is drawn with PIL.
Canvas 1024x1024, editorial front-page collage style.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 20)
RED = (178, 34, 40)
BLUE = (24, 62, 120)
TEAL = (10, 110, 110)
GOLD = (196, 144, 32)
GREY = (90, 90, 95)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def panel(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=WHITE, outline=(205, 198, 182), width=2)
    d.rounded_rectangle([x, y, x + w, y + 30], radius=10, fill=accent)
    d.rectangle([x, y + 20, x + w, y + 30], fill=accent)

def headline(x, y, s, size, maxw, fill=INK):
    f = F(SANS_B, size)
    lh = int(size * 1.18)
    lines = wrap(s, f, maxw)
    for i, ln in enumerate(lines):
        text(x, y + i * lh, ln, f, fill)
    return y + len(lines) * lh

def caption(x, y, s, maxw, size=17):
    f = F(SANS, size)
    lines = wrap(s, f, maxw)
    for i, ln in enumerate(lines):
        text(x, y + i * int(size * 1.3), ln, f, (52, 52, 58))
    return y + len(lines) * int(size * 1.3)

def tag(x, y, s):
    text(x + 12, y + 5, s, F(SANS_B, 16), WHITE)

def flag(x0, y0, fw, fh, kind):
    if kind == "CN":
        d.rectangle([x0, y0, x0 + fw, y0 + fh], fill=(222, 41, 47))
        d.ellipse([x0 + 7, y0 + 6, x0 + 17, y0 + 16], fill=(255, 222, 0))
        for sx, sy in [(24, 5), (28, 12), (28, 20), (23, 26)]:
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 4, y0 + sy + 4], fill=(255, 222, 0))
    elif kind == "RU":
        d.rectangle([x0, y0, x0 + fw, y0 + fh // 3], fill=WHITE, outline=(180, 180, 180))
        d.rectangle([x0, y0 + fh // 3, x0 + fw, y0 + 2 * fh // 3], fill=(0, 57, 166))
        d.rectangle([x0, y0 + 2 * fh // 3, x0 + fw, y0 + fh], fill=(213, 43, 30))
    elif kind == "US":
        for i in range(7):
            d.rectangle([x0, y0 + i * fh // 7, x0 + fw, y0 + (i + 1) * fh // 7], fill=(178, 34, 52) if i % 2 == 0 else WHITE)
        d.rectangle([x0, y0, x0 + fw * 2 // 5, y0 + fh * 4 // 7], fill=(60, 59, 110))
        for r_ in range(3):
            for c_ in range(4):
                d.ellipse([x0 + 4 + c_ * 9, y0 + 3 + r_ * 7, x0 + 7 + c_ * 9, y0 + 6 + r_ * 7], fill=WHITE)

# ---------------- masthead ----------------
text(W // 2, 16, "T H E   W O R L D   I N   O N E   D A Y", F(SERIF_B, 25), INK, "ma")
d.line([36, 58, W - 36, 58], fill=INK, width=3)
text(W // 2, 66, "THURSDAY 19 NOVEMBER 2026", F(SERIF_B, 47), RED, "ma")
d.line([36, 128, W - 36, 128], fill=INK, width=3)
text(W // 2, 134, "Three presidents in Shenzhen, tankers ablaze in Hormuz — and a probe one light-day from home", F(SANS, 18), GREY, "ma")

# ---------------- lead panel: Shenzhen trilateral summit ----------------
LX, LY, LW, LH = 36, 168, W - 72, 218
panel(LX, LY, LW, LH, BLUE)
tag(LX, LY, "LEAD STORY  •  SHENZHEN SUMMIT")
flag(LX + 28, LY + 96, 92, 62, "US")
flag(LX + 140, LY + 96, 92, 62, "CN")
flag(LX + 252, LY + 96, 92, 62, "RU")
text(LX + 28, LY + 168, "WASHINGTON        BEIJING        MOSCOW", F(SANS_B, 12), GREY)
headline(LX + 380, LY + 46, "TRUMP, XI & PUTIN ISSUE A 'DECLARATION TOWARD PEACE'", 27, 560)
caption(LX + 380, LY + 122, "First-ever trilateral meeting, at APEC: UN reform, more fuel supply, ICC curbs, nuclear dialogue — with Ukraine and Iran unmentioned", 560, 16)

# ---------------- row 2: Hormuz + ICJ ----------------
RY, RH = 402, 196
PW = (W - 72 - 16) // 2
# Hormuz
panel(36, RY, PW, RH, RED); tag(36, RY, "THE GULF  •  STRAIT OF HORMUZ")
# burning tanker sketch
tx, ty = 52, RY + 138
d.polygon([(tx, ty), (tx + 130, ty), (tx + 114, ty + 16), (tx + 16, ty + 16)], fill=(70, 70, 78))
d.rectangle([tx + 44, ty - 14, tx + 84, ty], fill=(120, 120, 128))
for fx, fh_ in [(58, 26), (76, 36), (94, 24)]:
    d.polygon([(tx + fx, ty - 12), (tx + fx + 7, ty - 12 - fh_), (tx + fx + 14, ty - 12)], fill=(255, 120, 40))
    d.polygon([(tx + fx + 4, ty - 12), (tx + fx + 7, ty - 12 - fh_ // 2), (tx + fx + 10, ty - 12)], fill=(255, 190, 60))
for i in range(3):
    d.arc([52 + i * 10, RY + 168, 200 + i * 10, RY + 196], start=180, end=360, fill=(90, 140, 190), width=4)
headline(52, RY + 40, "TANKERS BURN IN THE STRAIT AS US–IRAN STRIKES ESCALATE", 20, PW - 32)
caption(220, RY + 140, "Tehran blames mines; CENTCOM disputes it", PW - 236, 15)
# ICJ Myanmar
MX = 36 + PW + 16
panel(MX, RY, PW, RH, (84, 60, 140)); tag(MX, RY, "THE HAGUE  •  WORLD COURT")
# scales of justice
cx2 = MX + 66
d.line([cx2, RY + 108, cx2, RY + 158], fill=INK, width=4)
d.line([cx2 - 34, RY + 116, cx2 + 34, RY + 116], fill=INK, width=4)
for sx in (cx2 - 34, cx2 + 34):
    d.line([sx, RY + 116, sx - 10, RY + 138], fill=INK, width=2)
    d.line([sx, RY + 116, sx + 10, RY + 138], fill=INK, width=2)
    d.arc([sx - 13, RY + 132, sx + 13, RY + 146], start=0, end=180, fill=INK, width=3)
d.rectangle([cx2 - 18, RY + 158, cx2 + 18, RY + 164], fill=INK)
headline(MX + 120, RY + 40, "WORLD COURT: MYANMAR COMMITTED GENOCIDE", 20, PW - 136)
caption(MX + 120, RY + 112, "ICJ rules 9–6 on the 2017 Rohingya crackdown; reparations and safe return ordered", PW - 136, 15)

# ---------------- row 3: Markets + Ukraine ----------------
R3Y, R3H = 614, 176
panel(36, R3Y, PW, R3H, TEAL); tag(36, R3Y, "MARKETS  •  A RECORD AND A ROUT")
text(52, R3Y + 44, "$81bn", F(SERIF_B, 44), BLUE)
text(52, R3Y + 100, "Dow −1,100", F(SERIF_B, 30), RED)
headline(232, R3Y + 44, "ANTHROPIC'S IPO IS HISTORY'S LARGEST", 18, PW - 248)
caption(262, R3Y + 96, "+17% close, $1.3tn value; sixth straight Dow loss", PW - 278, 15)
# Ukraine bridge
UX = 36 + PW + 16
panel(UX, R3Y, PW, R3H, (168, 84, 20)); tag(UX, R3Y, "UKRAINE  •  CRIMEA")
# bridge sketch with broken span
by2 = R3Y + 128
d.line([UX + 16, by2, UX + 170, by2], fill=INK, width=5)
d.line([UX + 240, by2 - 8, UX + PW - 16, by2 - 8], fill=INK, width=5)
d.line([UX + 170, by2, UX + 240, by2 - 8], fill=RED, width=4)
for px in (40, 100, 290, 380):
    d.line([UX + px, by2, UX + px, by2 + 22], fill=INK, width=4)
d.arc([UX + 16, by2 + 8, UX + 200, by2 + 44], start=0, end=180, fill=(90, 140, 190), width=4)
d.arc([UX + 240, by2, UX + PW - 16, by2 + 36], start=0, end=180, fill=(90, 140, 190), width=4)
headline(UX + 16, R3Y + 40, "KYIV HITS THE CRIMEAN BRIDGE — THIRD TIME IN A WEEK", 19, PW - 32)
caption(UX + 16, R3Y + 90, "Putin vows a 'far more painful' reply", 210, 15)

# ---------------- row 4: GTA VI + Voyager ----------------
R4Y, R4H = 806, 128
panel(36, R4Y, PW, R4H, (150, 40, 110)); tag(36, R4Y, "CULTURE  •  LAUNCH DAY")
sx2, sy2 = 36 + 48, R4Y + 88
d.ellipse([sx2 - 16, sy2 - 44, sx2 + 16, sy2 - 12], fill=(255, 170, 60))
for dx, dy in [(-26, -14), (-14, -24), (0, -28), (14, -24), (26, -14)]:
    d.line([sx2, sy2 - 6, sx2 + dx, sy2 - 6 + dy], fill=(40, 130, 80), width=5)
    d.line([sx2 + dx, sy2 - 6 + dy, sx2 + dx + (6 if dx >= 0 else -6), sy2 - 6 + dy + 10], fill=(40, 130, 80), width=4)
d.line([sx2, sy2 + 6, sx2 - 4, sy2 + 34], fill=(110, 80, 50), width=5)
headline(36 + 100, R4Y + 38, "GTA VI IS HERE — 99 ON METACRITIC", 17, PW - 116)
caption(36 + 100, R4Y + 66, "15.8m pre-orders after a 13-year wait; a Van Gogh fetches a record $190.4m", PW - 116, 15)
# Voyager
TX = 36 + PW + 16
panel(TX, R4Y, PW, R4H, (60, 60, 66)); tag(TX, R4Y, "SPACE  •  DEEP SPACE")
# probe: dish + boom
px2, py2 = TX + 56, R4Y + 74
d.ellipse([px2 - 20, py2 - 20, px2 + 20, py2 + 20], outline=(90, 90, 100), width=3)
d.ellipse([px2 - 6, py2 - 6, px2 + 6, py2 + 6], fill=(150, 150, 160))
d.line([px2 + 14, py2 + 14, px2 + 44, py2 + 34], fill=(90, 90, 100), width=3)
d.line([px2 - 14, py2 + 14, px2 - 34, py2 + 30], fill=(90, 90, 100), width=3)
for stx, sty in [(TX + 96, R4Y + 46), (TX + 30, R4Y + 44), (TX + 108, R4Y + 96)]:
    d.ellipse([stx, sty, stx + 4, sty + 4], fill=GOLD)
headline(TX + 124, R4Y + 38, "VOYAGER 1: ONE LIGHT-DAY OUT", 17, PW - 140)
caption(TX + 124, R4Y + 64, "16.1 billion miles from Earth — the first object a full day's light-travel from home", PW - 140, 15)

# ---------------- ticker ----------------
TY = 950
d.rectangle([0, TY, W, H], fill=INK)
ticker = "COP31 DRAFT DROPS FOSSIL FUELS  •  EBOLA PASSES 11,000 IN CONGO  •  SENEGAL BOAT DISASTER  •  JEFFRIES FIRST BLACK SPEAKER"
f = F(SANS_B, 17)
while d.textlength(ticker, font=f) > W - 40 and f.size > 11:
    f = F(SANS_B, f.size - 1)
text(W // 2, TY + 16, ticker, f, WHITE, "ma")
text(W // 2, TY + 44, "One day, one picture — Thursday 19 November 2026", F(SANS, 14), (200, 200, 205), "ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
print(out, os.path.getsize(out), "bytes")
