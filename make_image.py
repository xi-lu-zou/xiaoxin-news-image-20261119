#!/usr/bin/env python3
"""Generate entry.png: the world news of Thursday 19 November 2026 in one image.
Deterministic, no network, no assets — everything is drawn with PIL.
Canvas 1024x1024, editorial front-page collage style.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

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

# ---------------- masthead ----------------
text(W // 2, 16, "T H E   W O R L D   I N   O N E   D A Y", F(SERIF_B, 25), INK, "ma")
d.line([36, 58, W - 36, 58], fill=INK, width=3)
text(W // 2, 66, "THURSDAY 19 NOVEMBER 2026", F(SERIF_B, 47), RED, "ma")
d.line([36, 128, W - 36, 128], fill=INK, width=3)
text(W // 2, 134, "Bombers over Iran, a beach in mourning — and the game the world waited a decade for", F(SANS, 18), GREY, "ma")

# ---------------- lead panel: US strikes Iran, Hormuz closed ----------------
LX, LY, LW, LH = 36, 168, W - 72, 218
panel(LX, LY, LW, LH, RED)
tag(LX, LY, "LEAD STORY  •  THE GULF")
# strait sketch: land masses, water gap, tanker, closure hatch
base = LY + LH - 14
d.polygon([(LX + 24, LY + 148), (LX + 260, LY + 148), (LX + 220, base), (LX + 24, base)], fill=(233, 220, 190))
d.polygon([(LX + 640, LY + 138), (LX + LW - 24, LY + 138), (LX + LW - 24, base), (LX + 690, base), (LX + 620, LY + 168)], fill=(233, 220, 190))
text(LX + 52, LY + 156, "IRAN", F(SANS_B, 15), (120, 100, 60))
text(LX + LW - 196, LY + 146, "ARABIAN PENINSULA", F(SANS_B, 13), (120, 100, 60))
# tanker in the strait
tx, ty = LX + 400, LY + 172
d.polygon([(tx, ty), (tx + 96, ty), (tx + 84, ty + 14), (tx + 12, ty + 14)], fill=(70, 70, 78))
d.rectangle([tx + 30, ty - 12, tx + 62, ty], fill=(120, 120, 128))
# red closure X over the strait
cx, cy = LX + 500, LY + 158
d.line([cx - 26, cy - 20, cx + 26, cy + 20], fill=RED, width=7)
d.line([cx - 26, cy + 20, cx + 26, cy - 20], fill=RED, width=7)
text(LX + 500, LY + 190, "STRAIT CLOSED", F(SANS_B, 14), RED, "ma")
# bomber silhouette top-left
bx, by = LX + 130, LY + 66
d.polygon([(bx, by), (bx + 34, by + 10), (bx + 120, by + 12), (bx + 34, by + 20), (bx + 8, by + 30), (bx + 2, by + 18), (bx - 12, by + 14)], fill=(60, 60, 66))
headline(LX + 250, LY + 46, "US BOMBS FORDOW & NATANZ — IRAN SHUTS THE STRAIT OF HORMUZ", 26, 690)
caption(LX + 250, LY + 122, "B-2s hit the nuclear sites after the tanker attack — UNSC emergency session", 700, 16)

# ---------------- row 2: Shenzhen + Sydney ----------------
RY, RH = 402, 196
PW = (W - 72 - 16) // 2
# Shenzhen
panel(36, RY, PW, RH, BLUE); tag(36, RY, "DIPLOMACY  •  SHENZHEN SUMMIT")
def flag(x0, y0, fw, fh, kind):
    if kind == "CN":
        d.rectangle([x0, y0, x0 + fw, y0 + fh], fill=(222, 41, 47))
        d.ellipse([x0 + 7, y0 + 6, x0 + 17, y0 + 16], fill=(255, 222, 0))
        for sx, sy in [(24, 5), (28, 12), (28, 20), (23, 26)]:
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 4, y0 + sy + 4], fill=(255, 222, 0))
    else:
        d.rectangle([x0, y0, x0 + fw, y0 + fh // 3], fill=WHITE, outline=(180, 180, 180))
        d.rectangle([x0, y0 + fh // 3, x0 + fw, y0 + 2 * fh // 3], fill=(0, 57, 166))
        d.rectangle([x0, y0 + 2 * fh // 3, x0 + fw, y0 + fh], fill=(213, 43, 30))
flag(52, RY + 128, 64, 42, "CN"); flag(128, RY + 128, 64, 42, "RU")
headline(52, RY + 40, "XI & PUTIN CONDEMN THE STRIKES, DEMAND A GULF CEASEFIRE", 20, PW - 32)
caption(204, RY + 132, "Joint statement from the Shenzhen summit", PW - 220, 15)
# Sydney
SX = 36 + PW + 16
panel(SX, RY, PW, RH, (84, 60, 140)); tag(SX, RY, "AUSTRALIA  •  SYDNEY")
# beach: sand, wave, candle
wy = RY + 156
d.rectangle([SX + 16, wy + 10, SX + PW - 16, RY + RH - 10], fill=(233, 220, 190))
for i in range(3):
    d.arc([SX + 34 + i * 8, wy - 2 + i * 6, SX + 170 + i * 8, wy + 22 + i * 6], start=180, end=360, fill=(90, 140, 190), width=4)
# candle with flame
kx, ky = SX + PW - 92, RY + 128
d.rectangle([kx, ky, kx + 14, ky + 44], fill=(240, 238, 230), outline=(170, 165, 155))
d.ellipse([kx + 2, ky - 16, kx + 12, ky - 2], fill=GOLD)
d.ellipse([kx + 5, ky - 11, kx + 9, ky - 4], fill=(255, 120, 40))
headline(SX + 16, RY + 40, "BONDI BEACH MASSACRE: 16 DEAD IN SYDNEY'S WORST SHOOTING", 20, PW - 32)
caption(SX + 16, RY + 112, "Gunman killed by police; a national day of mourning declared", PW - 140, 15)

# ---------------- row 3: Economy + Ukraine ----------------
R3Y, R3H = 614, 176
panel(36, R3Y, PW, R3H, TEAL); tag(36, R3Y, "ECONOMY  •  THE OIL SHOCK")
# falling chart
gx, gy = 52, R3Y + 62
pts = [(0, 6), (34, 2), (68, 14), (102, 10), (136, 30), (170, 44), (204, 62)]
for i in range(len(pts) - 1):
    d.line([gx + pts[i][0], gy + pts[i][1], gx + pts[i + 1][0], gy + pts[i + 1][1]], fill=RED, width=4)
d.polygon([(gx + 204, gy + 62), (gx + 192, gy + 58), (gx + 200, gy + 48)], fill=RED)
text(36 + 240, R3Y + 52, "2.4%", F(SERIF_B, 50), BLUE)
headline(36 + 236, R3Y + 112, "IMF CUTS WORLD GROWTH — FED HOLDS RATES", 17, PW - 252)
caption(52, R3Y + 128, "Held at 4.25–4.50%", PW - 260, 15)
# Ukraine / EU
UX = 36 + PW + 16
panel(UX, R3Y, PW, R3H, (168, 84, 20)); tag(UX, R3Y, "EUROPE  •  UKRAINE")
text(UX + 16, R3Y + 46, "€140bn", F(SERIF_B, 46), GOLD)
headline(UX + 16, R3Y + 104, "EU AGREES REPARATIONS LOAN FROM FROZEN RUSSIAN ASSETS", 17, PW - 32)
caption(UX + 216, R3Y + 58, "Kyiv funded into 2028", PW - 232, 15)

# ---------------- row 4: GTA VI + Starship ----------------
R4Y, R4H = 806, 128
panel(36, R4Y, PW, R4H, (150, 40, 110)); tag(36, R4Y, "CULTURE  •  LAUNCH DAY")
# palm + sun (Vice City mood)
sx2, sy2 = 36 + 48, R4Y + 88
d.ellipse([sx2 - 16, sy2 - 44, sx2 + 16, sy2 - 12], fill=(255, 170, 60))
for dx, dy in [(-26, -14), (-14, -24), (0, -28), (14, -24), (26, -14)]:
    d.line([sx2, sy2 - 6, sx2 + dx, sy2 - 6 + dy], fill=(40, 130, 80), width=5)
    d.line([sx2 + dx, sy2 - 6 + dy, sx2 + dx + (6 if dx >= 0 else -6), sy2 - 6 + dy + 10], fill=(40, 130, 80), width=4)
d.line([sx2, sy2 + 6, sx2 - 4, sy2 + 34], fill=(110, 80, 50), width=5)
headline(36 + 100, R4Y + 38, "GTA VI IS HERE — LEONIDA OPENS AT LAST", 17, PW - 116)
caption(36 + 100, R4Y + 76, "A decade's wait ends; record first-day sales projected", PW - 116, 15)
# Starship
TX = 36 + PW + 16
panel(TX, R4Y, PW, R4H, (60, 60, 66)); tag(TX, R4Y, "SPACE  •  TEXAS")
# rocket
rx, ry2 = TX + 52, R4Y + 52
d.polygon([(rx, ry2), (rx + 12, ry2 - 22), (rx + 24, ry2)], fill=(200, 200, 208))
d.rectangle([rx, ry2, rx + 24, ry2 + 34], fill=(200, 200, 208))
d.polygon([(rx, ry2 + 34), (rx - 8, ry2 + 48), (rx, ry2 + 48)], fill=(150, 150, 160))
d.polygon([(rx + 24, ry2 + 34), (rx + 32, ry2 + 48), (rx + 24, ry2 + 48)], fill=(150, 150, 160))
d.polygon([(rx + 7, ry2 + 48), (rx + 12, ry2 + 66), (rx + 17, ry2 + 48)], fill=(255, 140, 40))
headline(TX + 108, R4Y + 38, "STARSHIP V3 FLIES — FULL ORBIT FIRST TRY", 17, PW - 124)
caption(TX + 108, R4Y + 76, "SpaceX's biggest rocket completes its maiden orbital flight", PW - 124, 15)

# ---------------- ticker ----------------
TY = 950
d.rectangle([0, TY, W, H], fill=INK)
ticker = "CYCLONE XAVIER BATTERS QUEENSLAND  •  EBOLA PASSES 14,000 CASES IN DR CONGO  •  PELTOLA HOLDS ALASKA FOR THE DEMOCRATS"
f = F(SANS_B, 17)
while d.textlength(ticker, font=f) > W - 40 and f.size > 11:
    f = F(SANS_B, f.size - 1)
text(W // 2, TY + 16, ticker, f, WHITE, "ma")
text(W // 2, TY + 44, "One day, one picture — Thursday 19 November 2026", F(SANS, 14), (200, 200, 205), "ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
print(out, os.path.getsize(out), "bytes")
