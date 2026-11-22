import sys, os, json, math, numpy as np; sys.path.insert(0, os.path.dirname(__file__))
from engine2 import *
from PIL import Image, ImageDraw, ImageFilter
from functools import lru_cache

GOLD=(232,178,72); CREAM=(246,236,212); INK=(36,26,18); RED=(214,40,58); DRED=(120,20,28); LEAF=(62,128,64)
SKIN=(236,194,160); COAT=(28,26,30); BRICK=(150,62,44); SEA=(26,58,84)
F = lambda n, s: font(n, s)

# ---------- backgrounds ----------
def radial(c_in, c_out, cx=0.5, cy=0.45, r=0.8):
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx / W - cx) / r) ** 2 + ((yy / H - cy) / (r * 1.0)) ** 2 * (H / W) ** 2 * 0.35)
    d = np.clip(d, 0, 1)[..., None]; a = np.array(c_in) * (1 - d) + np.array(c_out) * d
    n = np.random.default_rng(1).normal(0, 3.5, (H, W, 1))
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
@lru_cache(None)
def bg(name):
    if name == "dark": return radial((84, 58, 38), (14, 10, 8))
    if name == "burgundy": return radial((120, 30, 40), (30, 8, 12))
    if name == "chart": return radial((30, 34, 44), (8, 9, 12))
    if name == "paper":
        im = radial((238, 222, 188), (160, 128, 88), r=1.1); return im
    if name == "ledger":
        im = radial((244, 236, 214), (196, 180, 148), r=1.2); d = ImageDraw.Draw(im)
        for y in range(300, H, 64): d.line([(0, y), (W, y)], fill=(150, 175, 205), width=2)
        d.line([(120, 0), (120, H)], fill=(205, 90, 90), width=3); return im
    if name == "tavern":
        im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im); rng = np.random.default_rng(4)
        for i, x in enumerate(range(0, W, 120)):
            c = int(rng.integers(70, 95)); d.rectangle((x, 0, x + 118, H), fill=(c, int(c * 0.62), int(c * 0.38)))
            for _ in range(12):
                y = int(rng.integers(0, H)); d.line([(x + 10, y), (x + 108, y + int(rng.integers(-6, 6)))], fill=(c - 14, int((c - 14) * 0.62), int((c - 14) * 0.38)), width=2)
        d.rectangle((0, 1180, W, H), fill=(52, 34, 22)); d.rectangle((0, 1180, W, 1200), fill=(92, 62, 40))   # table
        glow = Image.new("L", (W, H)); ImageDraw.Draw(glow).ellipse((-100, 100, 700, 900), fill=120); glow = glow.filter(ImageFilter.GaussianBlur(140))
        im = Image.composite(Image.new("RGB", (W, H), (255, 190, 110)), im, glow.point(lambda v: v // 2)); return im
    if name == "curtain":
        x = np.arange(W); fold = (np.sin(x / 38) * 0.5 + 0.5) ** 1.6
        col = np.array([150, 22, 34]) * (0.45 + 0.55 * fold)[:, None]; arr = np.repeat(col[None], H, 0)
        im = Image.fromarray(arr.astype(np.uint8)); d = ImageDraw.Draw(im)
        d.rectangle((0, 1150, W, H), fill=(70, 46, 30))
        for x in range(0, W, 90): d.line([(x, 1150), (x - 200, H)], fill=(58, 38, 24), width=3)
        return im
    raise KeyError(name)

def rays(d, t, col, n=16, cx=540, cy=760):
    for i in range(n):
        a0 = i * 2 * math.pi / n + t * 0.15; a1 = a0 + math.pi / n
        d.polygon([(cx, cy), (cx + 2400 * math.cos(a0), cy + 2400 * math.sin(a0)), (cx + 2400 * math.cos(a1), cy + 2400 * math.sin(a1))], fill=col)

# ---------- props & characters ----------
def mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))
def tulip(d, cx, by, s, col=RED, stripes=0.0, sway=0.0, grey=0.0, wilt=0.0, stem=True):
    col = mix(col, (120, 110, 100), grey); dark = mix(col, (0, 0, 0), 0.35); g = mix(LEAF, (110, 100, 80), grey)
    hx = cx + sway * 40 * s + wilt * 110 * s; hy = by - 330 * s + wilt * 150 * s
    if stem:
        pts = [((1 - u) ** 2 * cx + 2 * u * (1 - u) * cx + u * u * hx, (1 - u) ** 2 * by + 2 * u * (1 - u) * (by - 190 * s) + u * u * (hy + 50 * s)) for u in np.linspace(0, 1, 20)]
        d.line(pts, fill=g, width=max(int(14 * s), 2), joint="curve")
        d.polygon([(cx, by - 10 * s), (cx - 120 * s, by - 190 * s + wilt * 60 * s), (cx - 30 * s, by - 120 * s), (cx + 4 * s, by - 70 * s)], fill=g)
        d.polygon([(cx, by - 20 * s), (cx + 100 * s, by - 230 * s + wilt * 70 * s), (cx + 26 * s, by - 140 * s), (cx - 4 * s, by - 80 * s)], fill=mix(g, (0, 0, 0), 0.15))
    rot = wilt * 0.9
    def P(x, y):
        return (hx + x * s * math.cos(rot) - y * s * math.sin(rot), hy + x * s * math.sin(rot) + y * s * math.cos(rot))
    d.polygon([P(-48, -30), P(-26, -104), P(0, -64), P(26, -104), P(48, -30)], fill=dark)
    cup = [(-78, -40), (-64, 30), (-34, 70), (0, 82), (34, 70), (64, 30), (78, -40), (72, -98), (40, -52), (0, -114), (-40, -52), (-72, -98)]
    d.polygon([P(*p) for p in cup], fill=col)
    if stripes > 0:
        for k in range(-2, 3):
            bx = k * 24; tipx = k * 30; a = int(235 * stripes)
            fl = [(bx - 7, 66), (bx + 10 * math.sin(k + 1) - 4, 10), (tipx - 3, -70 + abs(k) * 10), (bx + 10 * math.sin(k + 1) + 8, 10), (bx + 7, 66)]
            d.polygon([P(*p) for p in fl], fill=(255, 248, 230, a))
    d.line([P(0, 78), P(-40, -52)], fill=dark, width=max(int(3 * s), 1)); d.line([P(0, 78), P(40, -52)], fill=dark, width=max(int(3 * s), 1))
    return P(0, -10)

def bulb(d, cx, cy, s, glow=0):
    d.ellipse((cx - 70 * s, cy - 60 * s, cx + 70 * s, cy + 70 * s), fill=(176, 120, 76))
    d.polygon([(cx - 40 * s, cy - 40 * s), (cx, cy - 130 * s), (cx + 40 * s, cy - 40 * s)], fill=(176, 120, 76))
    d.arc((cx - 50 * s, cy - 50 * s, cx + 50 * s, cy + 66 * s), 200, 340, fill=(120, 76, 44), width=max(int(5 * s), 1))
    d.line([(cx, cy - 120 * s), (cx + 6 * s, cy - 170 * s)], fill=LEAF, width=max(int(10 * s), 1))
    for k in range(-2, 3): d.line([(cx + k * 14 * s, cy + 66 * s), (cx + k * 22 * s, cy + 96 * s)], fill=(210, 190, 150), width=max(int(4 * s), 1))

def house(d, x, base, s, col=BRICK):
    w, h = 220 * s, 300 * s; d.rectangle((x - w / 2, base - h, x + w / 2, base), fill=col)
    st = [(-w / 2, -h)]; steps = 4
    for i in range(steps):
        xl = -w / 2 + i * w / (2 * steps + 1); st += [(xl, -h - i * 34 * s), (xl, -h - (i + 1) * 34 * s), (xl + w / (2 * steps + 1), -h - (i + 1) * 34 * s)]
    st += [(-x0, y0) for x0, y0 in reversed(st)]
    d.polygon([(x + a, base + b) for a, b in st], fill=col)
    for r in range(3):
        for c in range(3):
            wx = x - w / 2 + 28 * s + c * 64 * s; wy = base - h + 20 * s + r * 74 * s
            if r == 2 and c == 1: continue
            d.rectangle((wx, wy, wx + 36 * s, wy + 52 * s), fill=(250, 236, 190)); d.line([(wx + 18 * s, wy), (wx + 18 * s, wy + 52 * s)], fill=col, width=max(int(3 * s), 1))
    d.rectangle((x - 22 * s, base - 70 * s, x + 22 * s, base), fill=(60, 34, 24))
    d.ellipse((x - 18 * s, base - h - 120 * s, x + 18 * s, base - h - 84 * s), fill=(250, 236, 190))

ERA = "1600s"   # default costume; each video sets kit.ERA for its period


def _hat(d, kind, hx, hy, s, col=(18, 16, 18)):
    if kind == "tall":      # 1600s Dutch
        d.ellipse((hx - 110 * s, hy - 66 * s, hx + 110 * s, hy - 34 * s), fill=col)
        d.polygon([(hx - 62 * s, hy - 52 * s), (hx + 62 * s, hy - 52 * s), (hx + 52 * s, hy - 170 * s), (hx - 52 * s, hy - 170 * s)], fill=col)
        d.rectangle((hx - 60 * s, hy - 84 * s, hx + 60 * s, hy - 66 * s), fill=GOLD)
    elif kind == "tricorn":  # 1700s
        d.polygon([(hx - 104 * s, hy - 60 * s), (hx, hy - 128 * s), (hx + 104 * s, hy - 60 * s), (hx + 60 * s, hy - 42 * s), (hx, hy - 54 * s), (hx - 60 * s, hy - 42 * s)], fill=col)
        d.line([(hx - 104 * s, hy - 60 * s), (hx, hy - 128 * s), (hx + 104 * s, hy - 60 * s)], fill=GOLD, width=max(int(5 * s), 1))
    elif kind == "fedora":   # 1920s
        d.ellipse((hx - 96 * s, hy - 62 * s, hx + 96 * s, hy - 38 * s), fill=col)
        d.rounded_rectangle((hx - 56 * s, hy - 128 * s, hx + 56 * s, hy - 48 * s), int(24 * s), fill=col)
        d.polygon([(hx - 20 * s, hy - 128 * s), (hx, hy - 112 * s), (hx + 20 * s, hy - 128 * s)], fill=(60, 56, 60))
        d.rectangle((hx - 56 * s, hy - 70 * s, hx + 56 * s, hy - 56 * s), fill=(120, 30, 34))
    elif kind == "flatcap":  # 1920s worker
        d.chord((hx - 66 * s, hy - 96 * s, hx + 66 * s, hy - 20 * s), 180, 360, fill=(90, 84, 76))
        d.polygon([(hx + 20 * s, hy - 60 * s), (hx + 92 * s, hy - 48 * s), (hx + 40 * s, hy - 40 * s)], fill=(70, 64, 58))
    elif kind == "cap":      # 1600s worker
        d.chord((hx - 66 * s, hy - 90 * s, hx + 66 * s, hy - 10 * s), 180, 360, fill=(90, 60, 40))
    elif kind == "futou":    # Song dynasty official hat with long wings
        d.rectangle((hx - 56 * s, hy - 110 * s, hx + 56 * s, hy - 46 * s), fill=col)
        d.rectangle((hx - 150 * s, hy - 92 * s, hx + 150 * s, hy - 82 * s), fill=col)
    elif kind == "band":     # ancient headband
        d.rectangle((hx - 62 * s, hy - 44 * s, hx + 62 * s, hy - 30 * s), fill=(170, 40, 40))


def merchant(d, x, y, s, t, mood="happy", coat=COAT, hat=True, hat_off=(0, 0), look=0, cap=False, arm=None, beard=True, era=None, tie=(150, 30, 40)):
    """A cartoon person. `era` picks the costume: 1600s, 1700s, 1920s, ancient, song."""
    era = era or ERA
    if era == "1700s": beard = False  # 18th-century men were usually clean-shaven
    b = math.sin(t * 5 + x) * 4 * s; y = y + b
    robe = era in ("ancient", "song")
    # legs and feet
    if era == "1920s":
        trouser = tuple(max(c - 20, 0) for c in coat)
        d.rectangle((x - 46 * s, y - 170 * s, x - 6 * s, y), fill=trouser); d.rectangle((x + 6 * s, y - 170 * s, x + 46 * s, y), fill=trouser)
    elif not robe:
        d.rectangle((x - 46 * s, y - 100 * s, x - 14 * s, y), fill=(232, 222, 200)); d.rectangle((x + 14 * s, y - 100 * s, x + 46 * s, y), fill=(232, 222, 200))
    shoe = (120, 80, 50) if era == "ancient" else (20, 16, 14)
    d.ellipse((x - 62 * s, y - 16 * s, x - 6 * s, y + 10 * s), fill=shoe); d.ellipse((x + 6 * s, y - 16 * s, x + 62 * s, y + 10 * s), fill=shoe)
    # body
    if robe:
        d.polygon([(x - 78 * s, y - 330 * s), (x + 78 * s, y - 330 * s), (x + 110 * s, y - 10 * s), (x - 110 * s, y - 10 * s)], fill=coat)
        if era == "ancient":
            d.rectangle((x - 92 * s, y - 210 * s, x + 92 * s, y - 186 * s), fill=(200, 160, 70))
        else:
            d.line([(x - 50 * s, y - 330 * s), (x + 30 * s, y - 200 * s)], fill=(250, 244, 230), width=max(int(10 * s), 1))
            d.rectangle((x - 96 * s, y - 220 * s, x + 96 * s, y - 196 * s), fill=(40, 40, 40))
    elif era == "1700s":
        d.polygon([(x - 78 * s, y - 330 * s), (x + 78 * s, y - 330 * s), (x + 116 * s, y - 70 * s), (x - 116 * s, y - 70 * s)], fill=coat)
        d.rectangle((x - 30 * s, y - 330 * s, x + 30 * s, y - 150 * s), fill=tuple(min(c + 60, 255) for c in coat))
        for k in range(4): d.ellipse((x - 6 * s, y - 300 * s + k * 40 * s, x + 6 * s, y - 288 * s + k * 40 * s), fill=GOLD)
    elif era == "1920s":
        d.polygon([(x - 80 * s, y - 330 * s), (x + 80 * s, y - 330 * s), (x + 92 * s, y - 150 * s), (x - 92 * s, y - 150 * s)], fill=coat)
        d.polygon([(x - 30 * s, y - 330 * s), (x + 30 * s, y - 330 * s), (x, y - 230 * s)], fill=(248, 248, 248))
        d.polygon([(x - 9 * s, y - 326 * s), (x + 9 * s, y - 326 * s), (x + 12 * s, y - 250 * s), (x, y - 232 * s), (x - 12 * s, y - 250 * s)], fill=tie)
        lap = tuple(max(c - 25, 0) for c in coat)
        d.polygon([(x - 30 * s, y - 330 * s), (x - 52 * s, y - 300 * s), (x - 4 * s, y - 226 * s)], fill=lap); d.polygon([(x + 30 * s, y - 330 * s), (x + 52 * s, y - 300 * s), (x + 4 * s, y - 226 * s)], fill=lap)
        d.ellipse((x - 5 * s, y - 200 * s, x + 5 * s, y - 190 * s), fill=(20, 20, 20))
    else:
        d.polygon([(x - 78 * s, y - 330 * s), (x + 78 * s, y - 330 * s), (x + 104 * s, y - 92 * s), (x - 104 * s, y - 92 * s)], fill=coat)
        for k in range(4): d.ellipse((x - 6 * s, y - 300 * s + k * 50 * s, x + 6 * s, y - 288 * s + k * 50 * s), fill=GOLD)
    if arm:  # arm = (hand_x, hand_y) absolute
        d.line([(x + 60 * s, y - 300 * s), arm], fill=coat, width=int(34 * s)); d.ellipse((arm[0] - 18 * s, arm[1] - 18 * s, arm[0] + 18 * s, arm[1] + 18 * s), fill=SKIN)
    # collar / neck
    if era == "1600s":
        for k in range(3): d.ellipse((x - 80 * s + k * 4 * s, y - 360 * s + k * 6 * s, x + 80 * s - k * 4 * s, y - 318 * s + k * 6 * s), fill=(250, 248, 240), outline=(200, 196, 186), width=2)
    else:
        d.rectangle((x - 22 * s, y - 360 * s, x + 22 * s, y - 326 * s), fill=SKIN)
        if era == "1700s":  # lace cravat
            d.polygon([(x - 26 * s, y - 340 * s), (x + 26 * s, y - 340 * s), (x + 14 * s, y - 270 * s), (x, y - 256 * s), (x - 14 * s, y - 270 * s)], fill=(250, 248, 240), outline=(210, 206, 196))
        elif era == "1920s":
            d.polygon([(x - 24 * s, y - 344 * s), (x, y - 324 * s), (x - 30 * s, y - 318 * s)], fill=(248, 248, 248)); d.polygon([(x + 24 * s, y - 344 * s), (x, y - 324 * s), (x + 30 * s, y - 318 * s)], fill=(248, 248, 248))
    hy = y - 410 * s; d.ellipse((x - 60 * s, hy - 64 * s, x + 60 * s, hy + 60 * s), fill=SKIN)
    blink = (t % 3.3) < 0.12; ex = look * 8 * s
    for sx in (-1, 1):
        cx = x + sx * 24 * s + ex
        if blink: d.line([(cx - 10 * s, hy - 8 * s), (cx + 10 * s, hy - 8 * s)], fill=INK, width=max(int(4 * s), 1))
        else: d.ellipse((cx - 9 * s, hy - 18 * s, cx + 9 * s, hy + 2 * s), fill=INK)
        eb = -40 if mood == "shock" else -30
        d.line([(cx - 14 * s, hy + eb * s), (cx + 14 * s, hy + (eb + (4 if mood == "smug" else 0) * sx) * s)], fill=(80, 50, 30), width=max(int(5 * s), 1))
    if beard:
        if era == "1920s":  # 1920s: a neat moustache instead of a beard
            d.line([(x - 22 * s, hy + 22 * s), (x, hy + 16 * s), (x + 22 * s, hy + 22 * s)], fill=(90, 60, 40), width=max(int(7 * s), 1))
        elif era == "ancient":
            d.chord((x - 50 * s, hy + 10 * s, x + 50 * s, hy + 100 * s), 0, 180, fill=(60, 40, 30))
        else:
            d.polygon([(x - 26 * s, hy + 40 * s), (x + 26 * s, hy + 40 * s), (x, hy + 82 * s)], fill=(110, 70, 40)); d.line([(x - 26 * s, hy + 22 * s), (x, hy + 14 * s), (x + 26 * s, hy + 22 * s)], fill=(110, 70, 40), width=max(int(8 * s), 1))
    if mood == "shock": d.ellipse((x - 12 * s, hy + 18 * s, x + 12 * s, hy + 48 * s), fill=(90, 20, 20))
    elif mood == "sad": d.arc((x - 20 * s, hy + 26 * s, x + 20 * s, hy + 50 * s), 200, 340, fill=INK, width=max(int(5 * s), 1))
    else: d.arc((x - 22 * s, hy + 6 * s, x + 22 * s, hy + 36 * s), 20, 160, fill=INK, width=max(int(5 * s), 1))
    hx, hyy = x + hat_off[0], hy + hat_off[1]
    if cap: _hat(d, {"1920s": "flatcap"}.get(era, "cap"), hx, hyy, s)
    elif hat: _hat(d, {"1600s": "tall", "1700s": "tricorn", "1920s": "fedora", "ancient": "band", "song": "futou"}[era], hx, hyy, s)


COIN_SYM = "ƒ"   # each video sets its currency: ƒ guilders, $ dollars, £ pounds, "" plain


def coin(d, x, y, s, a=255, sym=None):
    sym = COIN_SYM if sym is None else sym
    d.ellipse((x - 26 * s, y - 26 * s, x + 26 * s, y + 26 * s), fill=(200, 150, 50, a), outline=(140, 98, 30, a), width=max(int(3 * s), 1))
    if sym: d.text((x, y), sym, font=F("serif_bold", int(30 * s)), fill=(120, 80, 20, a), anchor="mm")

def fit(d, text, name, size, maxw):
    """Largest font (<= size) for which text fits in maxw pixels."""
    while size > 8 and d.textlength(text, font=F(name, size)) > maxw: size -= 2
    return F(name, size)

def pill(d, y, text, fg, bgc, size=40, x=None):
    f = F("sans_black", size); w = d.textlength(text, font=f); cx = W / 2 if x is None else x
    d.rounded_rectangle((cx - w / 2 - 26, y, cx + w / 2 + 26, y + size + 28), (size + 28) // 2, fill=bgc); d.text((cx - w / 2, y + 12), text, font=f, fill=fg)

# ---------- map ----------
GEO = os.path.join(os.path.dirname(__file__), "..", "data", "countries.geojson")
def merc(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
@lru_cache(None)
def polys(bbox=(-30, 60, 20, 72)):
    out = []
    for f in json.load(open(GEO))["features"]:
        g = f["geometry"]; cs = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in cs:
            ring = np.array(poly[0]); lo, la = ring[:, 0], ring[:, 1]
            if lo.max() < bbox[0] or lo.min() > bbox[1] or la.max() < bbox[2] or la.min() > bbox[3]: continue
            out.append((f["properties"]["ADM0_A3"], np.c_[lo, [merc(v) for v in la]]))
    return out
def draw_map(img, d, clon, clat, sc, t, hl=("NLD",), cy=720, bbox=(-30, 60, 20, 72)):
    my = merc(clat)
    for code, r in polys(bbox):
        pts = np.c_[W / 2 + (r[:, 0] - clon) * sc, cy - (r[:, 1] - my) * sc]
        if pts[:, 0].max() < -50 or pts[:, 0].min() > W + 50 or pts[:, 1].max() < -50 or pts[:, 1].min() > H + 50: continue
        on = code in hl; fill = mix(GOLD, (255, 230, 150), 0.5 + 0.5 * math.sin(t * 5)) if on else (204, 184, 142)
        d.polygon([tuple(p) for p in pts], fill=fill, outline=(150, 128, 92) if not on else (255, 240, 200))
    return lambda lon, lat: (W / 2 + (lon - clon) * sc, cy - (merc(lat) - my) * sc)

def ship(d, x, y, s, a=255):
    d.polygon([(x - 40 * s, y), (x + 40 * s, y), (x + 28 * s, y + 18 * s), (x - 28 * s, y + 18 * s)], fill=(70, 44, 28, a))
    d.line([(x, y), (x, y - 70 * s)], fill=(50, 30, 20, a), width=max(int(4 * s), 1))
    d.polygon([(x + 3 * s, y - 66 * s), (x + 36 * s, y - 20 * s), (x + 3 * s, y - 14 * s)], fill=(250, 244, 226, a))
    d.polygon([(x - 3 * s, y - 60 * s), (x - 30 * s, y - 16 * s), (x - 3 * s, y - 12 * s)], fill=(236, 228, 206, a))

# ================= SCENES =================
SCALE_PIV = (540, 610)
def scale_scene(lt, dur, T, phase):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA")
    rays(d, T, (255, 200, 120, 16 if phase == 0 else 8))
    e = back(lt / 0.5) if phase == 0 else 1
    f = F("serif_bold", 170); tc(d, 250 - 60 * (1 - e), "1637", f, GOLD + (int(255 * clamp(e)),), 0)
    if phase == 0:
        ang = 16 if lt < 0.75 else -13 + 29 * math.exp(-(lt - 0.75) * 3.2) * math.cos((lt - 0.75) * 10)
        price = 5000 * eio((lt - 0.8) / 2.0); grey = 0; wilt = 0
    else:
        k = eio(lt / 1.2); ang = -13 + 29 * k + 3 * math.exp(-lt * 2) * math.sin(lt * 12) * k
        price = 5000 * (1 - eio((lt - 0.2) / 0.9)); grey = k; wilt = k
    a = math.radians(ang); px, py = SCALE_PIV; L = 330
    d.polygon([(px - 120, 1300), (px + 120, 1300), (px + 30, 1240), (px - 30, 1240)], fill=(110, 80, 40)); d.rectangle((px - 14, py, px + 14, 1250), fill=(150, 110, 50))
    lx, ly = px - L * math.cos(a), py - L * math.sin(a); rx, ry = px + L * math.cos(a), py + L * math.sin(a)
    d.line([(lx, ly), (rx, ry)], fill=GOLD, width=22); d.ellipse((px - 26, py - 26, px + 26, py + 26), fill=GOLD)
    for ex, ey, item in [(lx, ly, "tulip"), (rx, ry, "house")]:
        pan_y = ey + 260
        d.line([(ex, ey), (ex - 110, pan_y)], fill=(230, 190, 110), width=4); d.line([(ex, ey), (ex + 110, pan_y)], fill=(230, 190, 110), width=4)
        if item == "tulip": tulip(d, ex, pan_y, 0.62, stripes=1, sway=math.sin(T * 2) * 0.3, grey=grey, wilt=wilt)
        else: house(d, ex, pan_y, 0.62)
        d.chord((ex - 130, pan_y - 40, ex + 130, pan_y + 50), 0, 180, fill=GOLD)
        lab = "1 TULIP BULB" if item == "tulip" else "1 HOUSE"
        tc(d, pan_y + 70, lab, F("sans_black", 46), CREAM, 6, (40, 10, 14), x=ex)
    # price tag
    col = (60, 170, 90) if phase == 0 else RED
    if phase == 1 and lt > 0.9:
        e = back((lt - 0.9) / 0.35); tc(d, 430, "NO BUYERS", F("sans_black", 84), RED + (int(255 * clamp(e)),), 8, CREAM)
    elif not (phase == 0 and lt < 0.8):
        tc(d, 430, f"ƒ{price:,.0f}", F("sans_black", 84), col, 8, (40, 10, 14))
    return img

def map_a(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    clon, clat, sc = 8 - 3 * k, 50 + 2.2 * k, 30 + 40 * k
    pr = draw_map(img, d, clon, clat, sc, T)
    ax, ay = pr(4.9, 52.37)
    for i, (dl, dla) in enumerate([(-30, 50), (-20, 64), (-12, 38), (30, 60)]):
        p = ((lt * 0.35 + i * 0.27) % 1); ex, ey = pr(4.9 + (dl) * 0.4, 52.37 + (dla - 52.37) * 0.4)
        d.line([(ax, ay), (ex, ey)], fill=(255, 255, 255, 60), width=4)
        ship(d, ax + (ex - ax) * p, ay + (ey - ay) * p, 0.9, int(255 * min(1, 4 * (1 - p))))
    from kit2 import map_face, coin_flow
    for i, (dl, dla) in enumerate([(-30, 50), (30, 60)]):
        ex, ey = pr(4.9 + dl * 0.4, 52.37 + (dla - 52.37) * 0.4); coin_flow(d, (ex, ey), (ax, ay), T + i, n=4, arc=-60)
    nx_, ny_ = pr(5.6, 52.3); map_face(d, nx_, ny_, 0.35 + 0.5 * k, "happy", T)
    pill(d, ay - 160, "DUTCH REPUBLIC", INK, GOLD, 44, x=min(max(ax, 260), W - 260))
    pill(d, 230, "THE 1630s", CREAM, (0, 0, 0, 150), 40)
    return img

def map_b(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / 1.3)
    clon, clat, sc = 5 + 12 * k, 52.2 - 6 * k, 70 - 46 * k
    pr = draw_map(img, d, clon, clat, sc, T, hl=("NLD",))
    (ix, iy), (ax, ay) = pr(28.97, 41.01), pr(4.9, 52.37)
    cx, cy = (ix + ax) / 2 + 60, min(iy, ay) - 260
    p = eio((lt - 0.9) / (dur - 1.6)); pts = [((1 - u) ** 2 * ix + 2 * u * (1 - u) * cx + u * u * ax, (1 - u) ** 2 * iy + 2 * u * (1 - u) * cy + u * u * ay) for u in np.linspace(0, p, 40)]
    if p > 0:
        for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=CREAM, width=8)
        tulip(d, pts[-1][0], pts[-1][1] + 30, 0.28, stripes=1, sway=0)
    for (x, y), lab in [((ix, iy), "OTTOMAN EMPIRE"), ((ax, ay), "DUTCH REPUBLIC")]:
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=RED, outline=CREAM, width=4)
        tc(d, y + 26, lab, F("sans_black", 40), CREAM, 6, (10, 20, 30), x=min(max(x, 220), W - 220))
    if lt > dur - 1.6:
        e = back((lt - (dur - 1.6)) / 0.4); pill(d, 260 + 30 * (1 - e), "★ STATUS SYMBOL ★", INK, GOLD, 52)
        for i in range(8):
            a = i * math.pi / 4 + T * 2; r = 100 + 20 * math.sin(T * 6 + i)
            tc(d, ay - 90 + r * math.sin(a) * 0.6 - 30, "✦", F("sans_black", 40), (255, 230, 140), x=ax + r * math.cos(a))
    return img

def still(lt, dur, T, phase):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 1180, W, H), fill=(40, 26, 18)); d.rectangle((0, 1180, W, 1196), fill=(90, 62, 40))
    d.polygon([(420, 1185), (660, 1185), (630, 1000), (450, 1000)], fill=(60, 80, 110)); d.ellipse((440, 980, 640, 1020), fill=(80, 100, 130))
    s = 1.3 + 0.1 * (lt / dur if phase == 0 else 1)
    stripes = eio((lt - 0.6) / 1.6) if phase == 0 else 1
    head = tulip(d, 540, 1010, s, stripes=stripes, sway=math.sin(T * 1.5) * 0.15)
    if phase == 0:
        tc(d, 210, "SEMPER AUGUSTUS", F("serif_bold", 84), GOLD); tc(d, 305, "the most prized tulip", F("serif", 52), CREAM)
        if lt > dur * 0.55:
            for i in range(3):
                e = back((lt - dur * 0.55 - i * 0.15) / 0.35); tc(d, 560 - 40 * e + i * 20, "?", F("serif_bold", 150), CREAM + (int(255 * clamp(e)),), x=230 + i * 300 + (i == 1) * 0)
    else:
        e = eio(lt / 0.7); lx, ly, R = 1300 - (1300 - head[0]) * e, head[1] - 20, 210
        micro = Image.new("RGB", (W, H), (190, 226, 170)); md = ImageDraw.Draw(micro)
        rng = np.random.default_rng(2)
        for i in range(14):
            vx = lx - R + (rng.uniform(0, 2 * R) + T * 30 * rng.uniform(-1, 1)) % (2 * R); vy = ly - R + (rng.uniform(0, 2 * R) + T * 25 * rng.uniform(-1, 1)) % (2 * R); r = rng.uniform(16, 28)
            for k2 in range(8):
                aa = k2 * math.pi / 4 + T; md.line([(vx, vy), (vx + (r + 14) * math.cos(aa), vy + (r + 14) * math.sin(aa))], fill=(40, 110, 50), width=4)
            md.ellipse((vx - r, vy - r, vx + r, vy + r), fill=(60, 150, 70), outline=(30, 90, 40), width=4)
        mask = Image.new("L", (W, H)); ImageDraw.Draw(mask).ellipse((lx - R, ly - R, lx + R, ly + R), fill=255)
        img.paste(micro, (0, 0), mask); d = ImageDraw.Draw(img, "RGBA")
        d.line([(lx + R * 0.7, ly + R * 0.7), (lx + R * 1.4, ly + R * 1.4)], fill=(60, 40, 26), width=46)
        d.ellipse((lx - R, ly - R, lx + R, ly + R), outline=GOLD, width=22)
        if lt > 0.9:
            e2 = back((lt - 0.9) / 0.4); pill(d, 1220 + 40 * (1 - e2), "TULIP BREAKING VIRUS", CREAM, (150, 30, 40), 50)
            tc(d, 1320, "the stripes were a disease", F("serif", 52), CREAM)
    return img

PRICES = [100, 250, 600, 1200, 2500]
def tavern(lt, dur, T, phase):
    img = bg("tavern").copy(); d = ImageDraw.Draw(img, "RGBA")
    if phase == 0:
        per = 1.15; n = int(lt / per); u = (lt % per) / per; price = PRICES[min(n, len(PRICES) - 1)]
        L, R = (390, 1000), (690, 1000)
        a, b = (L, R) if n % 2 == 0 else (R, L)
        x = a[0] + (b[0] - a[0]) * eio(u); y = a[1] - 130 * math.sin(math.pi * u)
        merchant(d, 180, 1180, 0.95, T, "happy", look=1, arm=(330, 1000))
        merchant(d, 900, 1180, 0.95, T + 1, "smug", coat=(60, 30, 40), look=-1, arm=(750, 1000))
        doc = Image.new("RGBA", (240, 170), (0, 0, 0, 0)); dd = ImageDraw.Draw(doc); _shrink = 0.8
        dd.rectangle((0, 0, 239, 169), fill=(248, 240, 214), outline=(120, 90, 50), width=4)
        dd.text((16, 12), "BULB CONTRACT", font=fit(dd, "BULB CONTRACT", "serif_bold", 30, 208), fill=INK); dd.line([(16, 54), (224, 54)], fill=INK, width=2)
        dd.text((16, 66), f"ƒ{price:,}", font=fit(dd, f"ƒ{price:,}", "sans_black", 62, 208), fill=(30, 110, 50)); dd.text((16, 136), "pay on delivery", font=F("serif", 22), fill=INK)
        doc = doc.resize((192, 136), Image.LANCZOS).rotate(math.sin(u * math.pi * 2) * 15, expand=True, resample=Image.BICUBIC)
        img.paste(doc, (int(x - doc.width / 2), int(y - doc.height / 2)), doc); d = ImageDraw.Draw(img, "RGBA")
        pill(d, 230, "WINTER 1636 · TAVERN TRADING", CREAM, (0, 0, 0, 160), 38)
        tc(d, 380, f"ƒ{price:,}", F("sans_black", 140), GOLD, 8, INK)
        # bulb underground inset
        d.rounded_rectangle((60, 1230, 360, 1380), 20, fill=(70, 46, 28)); bulb(d, 210, 1310, 0.38); tc(d, 1236, "still in the ground", F("sans_bold", 26), CREAM, x=210)
    else:
        k = eio(lt / 1.0)
        merchant(d, 180, 1180, 0.95, T, "shock", hat_off=(1100 * k, -60 * k), look=1)
        merchant(d, 900, 1180, 0.95, T + 1, "shock", coat=(60, 30, 40), hat_off=(700 * k, -40 * k), look=1)
        rng = np.random.default_rng(int(T * 8))
        for i in range(14):
            y = 560 + i * 34; x0 = (T * 1900 + i * 211) % (W + 600) - 300; d.line([(x0, y), (x0 + 260, y)], fill=(255, 255, 255, 70), width=5)
        e = back((lt - 0.2) / 0.45); f = F("serif_bold", 130)
        tc(d, 300 + 60 * (1 - e), "WINDHANDEL", f, GOLD + (int(255 * clamp(e)),), 8, INK); tc(d, 450, "“the wind trade”", F("serif", 64), CREAM, 5, INK)
    return img

def wages(lt, dur, T, phase, years=16, price=5000):
    if phase == 0:
        img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
        d.polygon([(540, 0), (180, 1150), (900, 1150)], fill=(255, 230, 170, 26)); d.ellipse((260, 1100, 820, 1200), fill=(255, 230, 170, 30))
        d.rectangle((400, 1000, 680, 1180), fill=(110, 20, 30)); d.rectangle((380, 980, 700, 1010), fill=(150, 30, 40))
        bulb(d, 540, 900 + 8 * math.sin(T * 2), 1.0)
        v = price * eio((lt - 0.3) / (dur - 0.8)); tc(d, 300, f"ƒ{v:,.0f}", F("sans_black", 150), GOLD, 8, INK)
        tc(d, 470, "for ONE top bulb", F("serif", 56), CREAM)
        rng = np.random.default_rng(5)
        for i in range(40):
            st = i * dur / 44; u = (lt - st) / 0.7
            if u > 0: coin(d, rng.uniform(80, 1000), min(-40 + 1300 * u * u, 1150 - (i % 5) * 18), 1.0)
        return img
    img = bg("ledger").copy(); d = ImageDraw.Draw(img, "RGBA")
    merchant(d, 250, 1180, 0.68, T, "happy", coat=(110, 80, 50), cap=True, beard=False)
    d.rectangle((150, 1180, 350, 1200), fill=(90, 60, 40)); tc(d, 1210, "Craftsman", F("serif_bold", 44), INK, x=250); tc(d, 1262, "ƒ300 / year", F("sans_black", 44), (40, 110, 60), x=250)
    bulb(d, 800, 1060, 0.7); tc(d, 1210, "One bulb", F("serif_bold", 44), INK, x=800); tc(d, 1262, f"ƒ{price:,}", F("sans_black", 44), RED, x=800)
    n = max(1, min(years, int(years * eio((lt - 0.4) / (dur - 1.0))) if lt > 0.4 else 1))
    tc(d, 250, f"{n} YEAR" + ("S" if n != 1 else ""), F("sans_black", 150), RED, 0); tc(d, 420, "of a craftsman's wages", F("serif_bold", 60), INK)
    for i in range(n):
        cols = 11 if years > 16 else 8; x = (W - cols * 84) / 2 + (i % cols) * 84; y = 530 + (i // cols) * 84
        d.rounded_rectangle((x, y, x + 72, y + 80), 10, fill=(255, 255, 255), outline=INK, width=3); d.rectangle((x, y, x + 76, y + 22), fill=RED)
        d.text((x + 38 - d.textlength(str(i + 1), font=F("sans_black", 34)) / 2, y + 28), str(i + 1), font=F("sans_black", 34), fill=INK)
    return img

def auction(lt, dur, T, label="HAARLEM · FEBRUARY 1637"):
    img = bg("curtain").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, label, CREAM, (0, 0, 0, 170), 40)
    look = math.sin(lt * 3.2); gy = 700 + 20 * math.sin(T * 6)
    merchant(d, 790, 1060, 0.75, T, "shock" if lt > dur * 0.5 else "happy", look=look, arm=(930, gy))
    d.line([(930, gy), (950, gy - 40)], fill=(110, 70, 40), width=12); d.rectangle((905, gy - 80, 995, gy - 40), fill=(110, 70, 40))
    d.rectangle((640, 900, 940, 1180), fill=(90, 56, 34)); d.rectangle((620, 880, 960, 910), fill=(120, 80, 50))
    for r in range(2):
        for c in range(4):
            x = 90 + c * 150 + r * 40; y = 1060 + r * 120
            d.rectangle((x, y - 110, x + 90, y - 92), fill=(80, 50, 30)); d.rectangle((x, y - 40, x + 90, y - 26), fill=(80, 50, 30))
            d.line([(x + 6, y - 92), (x + 6, y + 40)], fill=(80, 50, 30), width=8); d.line([(x + 84, y - 26), (x + 84, y + 40)], fill=(80, 50, 30), width=8)
    if lt > 0.6:
        e = back((lt - 0.6) / 0.35); tc(d, 330 - 30 * (1 - e), "?", F("serif_bold", 200), CREAM + (int(255 * clamp(e)),), 8, INK, x=860)
    e = back((lt - 0.3) / 0.4); tc(d, 640, "NO ONE", F("sans_black", 110), CREAM + (int(255 * clamp(e)),), 8, INK, x=300); tc(d, 760, "CAME", F("sans_black", 110), CREAM + (int(255 * clamp(e)),), 8, INK, x=300)
    return img

def crash(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA")
    X0, X1, Y0, Y1 = 120, 980, 1180, 580
    for i in range(5): y = Y0 - i * (Y0 - Y1) / 4; d.line([(X0, y), (X1, y)], fill=(255, 255, 255, 22), width=2)
    tc(d, 250, "TULIP PRICES", F("sans_black", 70), CREAM); tc(d, 330, "illustrative shape", F("sans_med", 34), (150, 156, 170))
    for lab, u in [("NOV 1636", 0.05), ("JAN 1637", 0.5), ("FEB", 0.75), ("MAY", 0.97)]:
        tc(d, Y0 + 20, lab, F("sans_bold", 32), (150, 156, 170), x=X0 + (X1 - X0) * u)
    def val(u):
        return (0.08 + 0.92 * (u / 0.75) ** 3) if u < 0.75 else 0.06 + 0.94 * math.exp(-(u - 0.75) * 45)
    p = 0.75 * eio(lt / 0.55) if lt < 0.8 else 0.75 + 0.25 * eio((lt - 0.8) / 0.6)
    us = np.linspace(0, p, 120); pts = [(X0 + (X1 - X0) * u, Y0 - (Y0 - Y1) * val(u)) for u in us]
    crashed = lt > 0.8; col = RED if crashed else (70, 210, 120)
    d.polygon(pts + [(pts[-1][0], Y0), (X0, Y0)], fill=col + (40,)); d.line(pts, fill=col, width=10, joint="curve")
    d.ellipse((pts[-1][0] - 14, pts[-1][1] - 14, pts[-1][0] + 14, pts[-1][1] + 14), fill=col)
    if crashed:
        e = back((lt - 0.85) / 0.35); f = F("sans_black", 150); tc(d, 400 - 40 * (1 - e), "CRASH", f, RED + (int(255 * clamp(e)),), 10, (20, 4, 6))
        if lt < 1.0: d.rectangle((0, 0, W, H), fill=(255, 40, 40, int(90 * (1 - (lt - 0.8) / 0.2))))
    return img

def twist(lt, dur, T):
    img = Image.new("RGB", (W, H), (10, 8, 8)); d = ImageDraw.Draw(img, "RGBA")
    rays(d, T * 3, (214, 40, 58, 22), 20, 540, 820)
    f = F("sans_black", 190); e = back(lt / 0.35); j = 10 if int(T * 20) % 4 == 0 else 0
    for off, col in [(-j, (0, 220, 255, 160)), (j, (255, 40, 80, 160)), (0, CREAM + (255,))]:
        tc(d, 640 - 30 * (1 - e), "THE", f, col, x=540 + off); tc(d, 840 - 30 * (1 - e), "TWIST", f, col if off == 0 else col, x=540 + off)
    return img

def archive(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 230, "BUYERS WHO PAID", F("sans_black", 68), INK); tc(d, 315, "over ƒ300 for a bulb", F("serif_bold", 60), RED)
    n = min(37, int(37 * eio((lt - 0.4) / (dur - 1.2)))) if lt > 0.4 else 0
    for i in range(n):
        row = i // 8; in_row = min(8, n - row * 8); x = (W - (in_row - 1) * 116) / 2 + (i % 8) * 116; y = 460 + row * 142
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=INK); d.rounded_rectangle((x - 34, y + 28, x + 34, y + 100), 22, fill=INK)
        d.rectangle((x - 30, y - 40, x + 30, y - 30), fill=INK); d.rectangle((x - 18, y - 70, x + 18, y - 36), fill=INK)
    tc(d, 1196, f"{n}", F("sans_black", 100), RED)
    tc(d, 1324, "Source: Anne Goldgar, Tulipmania (2007)", F("serif", 34), INK)
    return img

def pamphlet(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    pg = Image.new("RGBA", (760, 900), (0, 0, 0, 0)); pd = ImageDraw.Draw(pg)
    pd.rectangle((0, 0, 759, 899), fill=(246, 236, 210), outline=INK, width=8); pd.rectangle((24, 24, 735, 875), outline=INK, width=3)
    for i, (s, fz) in enumerate([("THE TULIP", 92), ("MADNESS!", 110)]):
        w = pd.textlength(s, font=F("serif_bold", fz)); pd.text(((760 - w) / 2, 60 + i * 120), s, font=F("serif_bold", fz), fill=INK)
    tulip(pd, 380, 840, 1.25, col=(150, 40, 40), stripes=1)
    pg = pg.resize((560, 663), Image.LANCZOS).rotate(4, expand=True, resample=Image.BICUBIC); img.paste(pg, ((W - pg.width) // 2, 210), pg); d = ImageDraw.Draw(img, "RGBA")
    if lt > 0.35:
        from tulip_v2 import stamp_img, slam
        slam(img, stamp_img("EXAGGERATED", RED, 84, -6), lt, 0.35, 540, 1040); d = ImageDraw.Draw(img, "RGBA")
    for i, s in enumerate(["MASS RUIN", "ECONOMIC COLLAPSE"]):
        st0 = dur * (0.4 + 0.25 * i)
        if lt > st0:
            y = 1250 + i * 68; e = eio((lt - st0) / 0.3); f = F("sans_black", 52); w = d.textlength("✗ " + s, font=F("sans_black", 52))
            d.text(((W - w) / 2, y), "✗ " + s, font=f, fill=INK); d.line([((W - w) / 2, y + 36), ((W - w) / 2 + w * e, y + 36)], fill=RED, width=10)
    return img

def ending(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 16))
    pop_t = dur * 0.55
    if lt < pop_t:
        r = 60 + 300 * eio(lt / pop_t); wob = 1 + 0.03 * math.sin(T * 14)
        tulip(d, 540, 1250, 1.2, stripes=1, sway=math.sin(T * 2) * 0.2)
        cx, cy = 540, 760; d.ellipse((cx - r * wob, cy - r / wob, cx + r * wob, cy + r / wob), fill=(255, 230, 200, 50), outline=(255, 240, 220, 200), width=6)
        d.ellipse((cx - r * 0.55, cy - r * 0.7, cx - r * 0.2, cy - r * 0.35), fill=(255, 255, 255, 120))
        tc(d, 240, "THE FIRST BUBBLE…", F("serif_bold", 80), GOLD)
    else:
        u = lt - pop_t; tulip(d, 540, 1250, 1.2, stripes=1, sway=math.sin(T * 2) * 0.2)
        rng = np.random.default_rng(3)
        for i in range(30):
            a = rng.uniform(0, 2 * math.pi); sp = rng.uniform(300, 900); x = 540 + math.cos(a) * sp * u; y = 760 + math.sin(a) * sp * u + 400 * u * u
            al = int(255 * clamp(1 - u / 0.7)); d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(255, 240, 220, al))
        e = back(u / 0.35); tc(d, 240, "…WAS A BUBBLE?", F("serif_bold", 80), GOLD + (int(255 * clamp(e)),))
        e2 = back((u - 0.5) / 0.4)
        pass
    return img

CHANNEL = "DOOLIAN DOLLARS"


def brand_coin(d, x, y, r):
    """Small version of the Doolian Dollars gold coin logo."""
    d.ellipse((x - r, y - r, x + r, y + r), fill=(140, 96, 28))
    d.ellipse((x - r * 0.9, y - r * 0.9, x + r * 0.9, y + r * 0.9), fill=(238, 194, 96))
    d.ellipse((x - r * 0.74, y - r * 0.74, x + r * 0.74, y + r * 0.74), outline=(140, 96, 28), width=max(int(r * 0.08), 2))
    d.text((x + r * 0.04, y + r * 0.05), "DD", font=F("serif_bold", int(r * 0.95)), fill=(140, 96, 28), anchor="mm")
    d.text((x, y), "DD", font=F("serif_bold", int(r * 0.95)), fill=(184, 128, 40), anchor="mm")


def chrome(d, t, total):
    # channel badge: gold coin + name on a dark pill, centred at the top
    f = F("sans_black", 32); tw = d.textlength(CHANNEL, font=f); r = 26
    w = r * 2 + 14 + tw + 40; x0 = (W - w) / 2; y0 = 92
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 2 * r + 16), r + 8, fill=(12, 10, 10, 200), outline=(212, 170, 80), width=3)
    brand_coin(d, x0 + 8 + r, y0 + 8 + r, r)
    d.text((x0 + 8 + 2 * r + 14, y0 + 8 + r), CHANNEL, font=f, fill=(246, 210, 120), anchor="lm")
    d.rectangle((0, H - 10, W * t / total, H), fill=GOLD)

theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
