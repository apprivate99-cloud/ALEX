"""More props for the money-history videos: animals, ancient money, charts, and 1920s scenery."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from kit import *  # noqa: F401,F403  (shared palette, characters, maps, backgrounds)
from tulip_v2 import stamp_img, slam  # noqa: F401

CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
CLAY, CLAY_D = (176, 120, 78), (120, 76, 44)
ELECTRUM, ELECTRUM_D = (226, 204, 140), (150, 126, 70)
IRON, IRON_D = (110, 110, 116), (60, 60, 66)
GREEN_UP, DECO = (70, 210, 120), (212, 175, 90)


def card(d, box, items, fill=(250, 244, 226), outline=INK, pad=50):
    """Draw a box and centre `items` [(text, font_name, size, colour)] inside it, shrinking text to fit."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 20, fill=fill, outline=outline, width=5)
    fonts = [fit(d, t, n, sz, (x1 - x0) - 2 * pad) for t, n, sz, _ in items]
    hs = [f.size * 1.25 for f in fonts]; y = y0 + ((y1 - y0) - sum(hs)) / 2
    for (t, n, sz, c), f, h in zip(items, fonts, hs):
        w = d.textlength(t, font=f); d.text(((x0 + x1 - w) / 2, y + (h - f.size * 1.15) / 2), t, font=f, fill=c); y += h


def cow(d, x, y, s, t):
    """A side-on cartoon cow standing with its feet on y."""
    b = math.sin(t * 3) * 3 * s
    for lx in (-70, -40, 40, 70):
        d.rectangle((x + lx * s - 10 * s, y - 90 * s, x + lx * s + 10 * s, y), fill=(240, 240, 236))
        d.rectangle((x + lx * s - 10 * s, y - 14 * s, x + lx * s + 10 * s, y), fill=(60, 50, 44))
    d.ellipse((x - 120 * s, y - 210 * s + b, x + 110 * s, y - 70 * s + b), fill=(244, 244, 240), outline=(60, 50, 44), width=max(int(4 * s), 1))
    for sx, sy, r in [(-50, -170, 34), (30, -120, 28), (60, -180, 20)]:
        d.ellipse((x + (sx - r) * s, y + (sy - r) * s + b, x + (sx + r) * s, y + (sy + r) * s + b), fill=(50, 44, 40))
    hx, hy = x + 120 * s, y - 190 * s + b
    d.ellipse((hx - 50 * s, hy - 40 * s, hx + 50 * s, hy + 50 * s), fill=(244, 244, 240), outline=(60, 50, 44), width=max(int(4 * s), 1))
    d.ellipse((hx - 10 * s, hy + 14 * s, hx + 56 * s, hy + 54 * s), fill=(236, 170, 170))
    d.ellipse((hx - 18 * s, hy - 14 * s, hx - 6 * s, hy - 2 * s), fill=INK)
    d.polygon([(hx - 40 * s, hy - 30 * s), (hx - 60 * s, hy - 60 * s), (hx - 26 * s, hy - 40 * s)], fill=(220, 210, 180))
    d.line([(x - 118 * s, y - 160 * s + b), (x - 150 * s, y - 100 * s)], fill=(60, 50, 44), width=max(int(6 * s), 1))


def sack(d, x, y, s, label="GRAIN"):
    d.polygon([(x - 80 * s, y), (x - 90 * s, y - 120 * s), (x - 40 * s, y - 190 * s), (x + 40 * s, y - 190 * s), (x + 90 * s, y - 120 * s), (x + 80 * s, y)], fill=(200, 170, 110), outline=(120, 90, 50))
    d.rectangle((x - 46 * s, y - 206 * s, x + 46 * s, y - 186 * s), fill=(150, 110, 60))
    f = fit(d, label, "sans_black", int(40 * s), 140 * s)
    w = d.textlength(label, font=f); d.text((x - w / 2, y - 110 * s), label, font=f, fill=(110, 80, 40))


def tablet(img, cx, cy, s, lines, t=0):
    """Clay tablet with cuneiform-like wedges and an English gloss."""
    tw, th = int(520 * s), int(640 * s)
    tb = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); td = ImageDraw.Draw(tb)
    td.rounded_rectangle((0, 0, tw - 1, th - 1), int(60 * s), fill=CLAY, outline=CLAY_D, width=max(int(8 * s), 1))
    rng = np.random.default_rng(11)
    for row in range(6):
        y = 60 * s + row * 52 * s; x = 50 * s
        while x < tw - 80 * s:
            k = rng.integers(0, 3)
            if k == 0: td.polygon([(x, y), (x + 26 * s, y + 8 * s), (x, y + 16 * s)], fill=CLAY_D)
            elif k == 1: td.polygon([(x, y), (x + 16 * s, y), (x + 8 * s, y + 30 * s)], fill=CLAY_D)
            else: td.line([(x, y + 6 * s), (x + 30 * s, y + 6 * s)], fill=CLAY_D, width=max(int(5 * s), 1))
            x += (30 + rng.integers(4, 18)) * s
    for i, ln in enumerate(lines):
        f = fit(td, ln, "serif_bold", int(44 * s), tw - 80 * s)
        w = td.textlength(ln, font=f); td.text(((tw - w) / 2, 400 * s + i * 62 * s), ln, font=f, fill=(250, 236, 210))
    tb = tb.rotate(math.sin(t) * 2, expand=True, resample=Image.BICUBIC)
    img.paste(tb, (int(cx - tb.width / 2), int(cy - tb.height / 2)), tb)


def lion_coin(d, cx, cy, r):
    """Lydian electrum coin: irregular lump with a lion's head."""
    pts = [(cx + r * (1 + 0.06 * math.sin(a * 5)) * math.cos(a), cy + r * (1 + 0.06 * math.cos(a * 3)) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)]
    d.polygon(pts, fill=ELECTRUM, outline=ELECTRUM_D)
    for i in range(14):  # mane
        a = i * 2 * math.pi / 14
        d.polygon([(cx + r * 0.25 * math.cos(a - 0.2), cy + r * 0.25 * math.sin(a - 0.2)), (cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a)),
                   (cx + r * 0.25 * math.cos(a + 0.2), cy + r * 0.25 * math.sin(a + 0.2))], fill=ELECTRUM_D)
    d.ellipse((cx - r * 0.34, cy - r * 0.34, cx + r * 0.34, cy + r * 0.34), fill=ELECTRUM, outline=ELECTRUM_D, width=max(int(r * 0.03), 1))
    d.ellipse((cx - r * 0.16, cy - r * 0.1, cx - r * 0.06, cy), fill=ELECTRUM_D); d.ellipse((cx + r * 0.06, cy - r * 0.1, cx + r * 0.16, cy), fill=ELECTRUM_D)
    d.arc((cx - r * 0.14, cy, cx + r * 0.14, cy + r * 0.2), 20, 160, fill=ELECTRUM_D, width=max(int(r * 0.03), 1))


def iron_string(d, x0, y, n, r, sag=40):
    """A string of heavy square-holed iron coins."""
    pts = [(x0 + i * r * 1.7, y + sag * math.sin(math.pi * i / max(n - 1, 1))) for i in range(n)]
    d.line(pts, fill=(140, 100, 60), width=6)
    for x, yy in pts:
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=IRON, outline=IRON_D, width=4)
        d.rectangle((x - r * 0.28, yy - r * 0.28, x + r * 0.28, yy + r * 0.28), fill=(240, 232, 210))


def jiaozi(img, cx, cy, s, t=0):
    """Song-dynasty style paper note (vertical, red seal)."""
    w, h = int(300 * s), int(520 * s)
    nt = Image.new("RGBA", (w, h), (0, 0, 0, 0)); nd = ImageDraw.Draw(nt)
    nd.rectangle((0, 0, w - 1, h - 1), fill=(236, 222, 186), outline=(60, 40, 30), width=max(int(8 * s), 1))
    nd.rectangle((18 * s, 18 * s, w - 18 * s, h - 18 * s), outline=(60, 40, 30), width=max(int(3 * s), 1))
    f = ImageFont.truetype(CJK, int(96 * s)); tw = nd.textlength("交子", font=f)
    nd.text(((w - tw) / 2, 50 * s), "交子", font=f, fill=(40, 30, 24))
    for k in range(5): nd.line([(50 * s, 200 * s + k * 34 * s), (w - 50 * s, 200 * s + k * 34 * s)], fill=(120, 100, 80), width=max(int(3 * s), 1))
    nd.rectangle((w / 2 - 50 * s, 390 * s, w / 2 + 50 * s, 480 * s), fill=(190, 40, 40))
    nt = nt.rotate(math.sin(t) * 3, expand=True, resample=Image.BICUBIC)
    img.paste(nt, (int(cx - nt.width / 2), int(cy - nt.height / 2)), nt)


def swords(d, x1, x2, y, t, clash):
    """Two rapiers that meet between the duellists."""
    mid = (x1 + x2) / 2; off = 0 if clash else 40
    for sx, ex in ((x1, mid + off), (x2, mid - off)):
        d.line([(sx, y), (ex, y - 60 + 10 * math.sin(t * 12))], fill=(210, 214, 222), width=8)
        d.ellipse((sx - 16, y - 16, sx + 16, y + 16), fill=GOLD)


def bars(d, x0, y0, x1, y1, bent=0.0):
    """Prison bars; `bent` 0..1 bends the middle pair apart."""
    d.rectangle((x0, y0, x1, y0 + 24), fill=(70, 70, 76)); d.rectangle((x0, y1 - 24, x1, y1), fill=(70, 70, 76))
    n = 7
    for i in range(n):
        x = x0 + 30 + i * (x1 - x0 - 60) / (n - 1)
        if i in (3, 4):
            dx = (-1 if i == 3 else 1) * 70 * bent
            d.line([(x, y0 + 24), (x + dx, (y0 + y1) / 2), (x, y1 - 24)], fill=(90, 90, 98), width=18, joint="curve")
        else:
            d.line([(x, y0 + 24), (x, y1 - 24)], fill=(90, 90, 98), width=18)


def line_chart(d, pts, X0, X1, Y0, Y1, vmax, p, col, log=False, xlabels=(), ylabels=(), label_col=(150, 156, 170)):
    """Draw a (possibly log-scale) line chart revealed up to fraction p of its x-range. pts = [(x 0..1, value)]."""
    def Y(v): return Y0 - (Y0 - Y1) * ((math.log10(max(v, 1e-9)) / math.log10(vmax)) if log else v / vmax)
    for v, lab in ylabels:
        y = Y(v); d.line([(X0, y), (X1, y)], fill=(255, 255, 255, 25), width=2); d.text((X0 - 110, y - 18), lab, font=F("sans_bold", 30), fill=label_col)
    for u, lab in xlabels:
        x = X0 + (X1 - X0) * u; w = d.textlength(lab, font=F("sans_bold", 30)); d.text((x - w / 2, Y0 + 16), lab, font=F("sans_bold", 30), fill=label_col)
    xs = np.linspace(0, p, 200); ys = np.interp(xs, [a for a, _ in pts], [b for _, b in pts])
    poly = [(X0 + (X1 - X0) * x, Y(y)) for x, y in zip(xs, ys)]
    d.polygon(poly + [(poly[-1][0], Y0), (X0, Y0)], fill=col + (40,)); d.line(poly, fill=col, width=10, joint="curve")
    d.ellipse((poly[-1][0] - 14, poly[-1][1] - 14, poly[-1][0] + 14, poly[-1][1] + 14), fill=col)
    return float(ys[-1]), poly[-1]


def phone(d, cx, cy, s, balance):
    w, h = 300 * s, 580 * s
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(46 * s), fill=(24, 26, 32), outline=(80, 84, 96), width=max(int(6 * s), 1))
    d.rounded_rectangle((cx - w / 2 + 16 * s, cy - h / 2 + 40 * s, cx + w / 2 - 16 * s, cy + h / 2 - 40 * s), int(24 * s), fill=(240, 244, 248))
    tc(d, cy - 190 * s, "BALANCE", F("sans_bold", int(30 * s)), (90, 100, 120), x=cx)
    tc(d, cy - 140 * s, balance, fit(d, balance, "sans_black", int(56 * s), w - 60 * s), (20, 110, 60), x=cx)
    for k in range(4):
        y = cy - 30 * s + k * 60 * s
        d.rounded_rectangle((cx - w / 2 + 36 * s, y, cx + w / 2 - 36 * s, y + 40 * s), int(10 * s), fill=(222, 228, 236))


def ticker(d, cx, cy, s, t, tape_len):
    """1920s ticker-tape machine under a glass dome, spewing tape."""
    d.rectangle((cx - 120 * s, cy + 60 * s, cx + 120 * s, cy + 140 * s), fill=(70, 46, 30))
    d.ellipse((cx - 110 * s, cy - 160 * s, cx + 110 * s, cy + 80 * s), fill=(200, 220, 230, 90), outline=(230, 240, 250), width=max(int(5 * s), 1))
    d.rectangle((cx - 60 * s, cy - 20 * s, cx + 60 * s, cy + 60 * s), fill=(40, 40, 46))
    d.ellipse((cx - 30 * s, cy - 70 * s, cx + 30 * s, cy - 10 * s), fill=(60, 60, 66))
    pts = [(cx + 60 * s + k * 18, cy + 20 * s + 36 * math.sin(k * 0.35 + t * 4) + k * 1.0) for k in range(int(tape_len)) if cx + 60 * s + k * 18 < W - 30]
    if len(pts) > 1:
        d.line(pts, fill=(250, 246, 230), width=int(22 * s))
        for k in range(0, len(pts), 6): d.text((pts[k][0] - 8, pts[k][1] - 12), "▼", font=F("sans_bold", 18), fill=(200, 30, 40))


def calendar(d, cx, cy, s, month, day, year=None, col=RED):
    w, h = 300 * s, 320 * s
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(24 * s), fill=(255, 255, 255), outline=INK, width=max(int(5 * s), 1))
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 90 * s), int(24 * s), fill=col)
    d.rectangle((cx - w / 2, cy - h / 2 + 60 * s, cx + w / 2, cy - h / 2 + 90 * s), fill=col)
    tc(d, cy - h / 2 + 14 * s, month, F("sans_black", int(54 * s)), (255, 255, 255), x=cx)
    tc(d, cy - h / 2 + 100 * s, str(day), F("sans_black", int(140 * s)), INK, x=cx)
    if year: tc(d, cy + h / 2 - 66 * s, str(year), F("sans_bold", int(40 * s)), (90, 90, 90), x=cx)


def deco_bg():
    """Black and gold art-deco backdrop for the 1920s."""
    img = Image.new("RGB", (W, H), (14, 14, 18)); d = ImageDraw.Draw(img)
    for i in range(14):
        a0 = -math.pi / 2 + (i - 6.5) * 0.13
        d.line([(540, 1700), (540 + 2400 * math.cos(a0), 1700 + 2400 * math.sin(a0))], fill=(60, 50, 26), width=6)
    for k in range(3): d.arc((540 - 300 - k * 120, 1400 - 300 - k * 120, 540 + 300 + k * 120, 1400 + 300 + k * 120), 180, 360, fill=(90, 74, 36), width=6)
    return img
