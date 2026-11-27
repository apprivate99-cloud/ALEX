"""The con man who sold a country that didn't exist: Gregor MacGregor and Poyais (1820s)."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit2 import *
import kit
kit.ERA = "1700s"; kit.COIN_SYM = "£"

UNIFORM, SASH = (160, 24, 36), (40, 70, 150)
GOLDC, GOLDD = (240, 196, 90), (150, 104, 30)
JUNGLE, JUNGLE_D = (46, 110, 52), (24, 70, 32)
AMER_BBOX = (-110, 20, 5, 60)


def macgregor(d, x, y, s, t, mood="smug", arm=None):
    """MacGregor in a red military uniform with gold epaulettes, a blue sash and medals."""
    merchant(d, x, y, s, t, mood, coat=UNIFORM, hat=False, beard=False, arm=arm)
    b = math.sin(t * 5 + x) * 4 * s; top = y + b
    hy = top - 410 * s
    d.chord((x - 62 * s, hy - 70 * s, x + 62 * s, hy + 10 * s), 180, 360, fill=(120, 70, 36))        # hair
    for sx in (-1, 1):                                                                                   # epaulettes
        ex = x + sx * 78 * s
        d.ellipse((ex - 30 * s, top - 346 * s, ex + 30 * s, top - 316 * s), fill=GOLDC)
        for k in range(5): d.line([(ex - 24 * s + k * 12 * s, top - 320 * s), (ex - 24 * s + k * 12 * s, top - 300 * s)], fill=GOLDD, width=max(int(4 * s), 1))
    d.line([(x - 70 * s, top - 320 * s), (x + 80 * s, top - 120 * s)], fill=SASH, width=int(26 * s))      # sash
    for k in range(3):                                                                                   # medals
        mx, my = x - 40 * s + k * 24 * s, top - 250 * s
        d.rectangle((mx - 6 * s, my - 26 * s, mx + 6 * s, my - 6 * s), fill=SASH)
        d.ellipse((mx - 10 * s, my - 8 * s, mx + 10 * s, my + 12 * s), fill=GOLDC)


def settler(d, x, y, s, t, mood="happy", grey=0.0):
    coat = mix((110, 80, 50), (120, 120, 120), grey)
    merchant(d, x, y, s, t, mood, coat=coat, cap=True, beard=False)


def palm(d, x, base, s, a=255):
    pts = [(x + 30 * s * math.sin(u * 1.5), base - 260 * s * u) for u in np.linspace(0, 1, 12)]
    d.line(pts, fill=(120, 86, 50, a), width=max(int(16 * s), 2))
    tx, ty = pts[-1]
    for k in range(6):
        ang = -math.pi / 2 + (k - 2.5) * 0.55
        d.polygon([(tx, ty), (tx + 120 * s * math.cos(ang - 0.15), ty + 120 * s * math.sin(ang - 0.15) + 40 * s), (tx + 130 * s * math.cos(ang), ty + 130 * s * math.sin(ang) + 50 * s)], fill=(60, 140, 70, a))


def golden_city(d, cx, base, s, a=255):
    """The imaginary capital: domes, towers and a gate, all in gold."""
    g, gd = GOLDC + (a,), GOLDD + (a,)
    d.rectangle((cx - 300 * s, base - 120 * s, cx + 300 * s, base), fill=g, outline=gd, width=max(int(4 * s), 1))
    for dx, w, h in ((-230, 70, 260), (-120, 90, 200), (0, 140, 320), (130, 90, 220), (240, 70, 280)):
        x0 = cx + dx * s - w * s / 2; d.rectangle((x0, base - h * s, x0 + w * s, base - 110 * s), fill=g, outline=gd, width=max(int(3 * s), 1))
        d.pieslice((x0, base - h * s - w * s / 2, x0 + w * s, base - h * s + w * s / 2), 180, 360, fill=g, outline=gd)
        d.line([(x0 + w * s / 2, base - h * s - w * s / 2), (x0 + w * s / 2, base - h * s - w * s / 2 - 40 * s)], fill=gd, width=max(int(4 * s), 1))
        for r in range(3): d.rectangle((x0 + w * s * 0.35, base - h * s + 30 * s + r * 50 * s, x0 + w * s * 0.65, base - h * s + 60 * s + r * 50 * s), fill=(255, 246, 210, a))
    d.chord((cx - 50 * s, base - 110 * s, cx + 50 * s, base + 10 * s), 180, 360, fill=gd)


def jungle(d, base, k, seed=3):
    """Dense trees that grow in as k goes 0 -> 1."""
    rng = np.random.default_rng(seed)
    for i in range(26):
        x = rng.uniform(-40, W + 40); r = rng.uniform(70, 150) * k; y = base - rng.uniform(40, 360) * k
        if r < 4: continue
        d.ellipse((x - r, y - r, x + r, y + r), fill=(JUNGLE if i % 2 else JUNGLE_D) + (int(255 * min(1, k * 1.4)),))
    d.rectangle((0, base - 10, W, H), fill=(40, 70, 36))


def brochure_page(s=1.0):
    pg = Image.new("RGBA", (int(820 * s), int(1000 * s)), (0, 0, 0, 0)); pd = ImageDraw.Draw(pg, "RGBA")
    w, h = pg.size
    pd.rectangle((0, 0, w - 1, h - 1), fill=(250, 242, 220), outline=(120, 80, 40), width=max(int(8 * s), 2))
    pd.rectangle((24 * s, 24 * s, w - 24 * s, h - 24 * s), outline=(120, 80, 40), width=max(int(3 * s), 1))
    pd.text((w / 2, 110 * s), "POYAIS", font=F("serif_bold", int(120 * s)), fill=(150, 30, 40), anchor="mm")
    pd.text((w / 2, 200 * s), "A NEW LAND OF OPPORTUNITY", font=F("sans_bold", int(36 * s)), fill=(90, 60, 30), anchor="mm")
    pd.rectangle((70 * s, 260 * s, w - 70 * s, 700 * s), fill=(150, 200, 230))
    pd.rectangle((70 * s, 600 * s, w - 70 * s, 700 * s), fill=(90, 150, 80))
    golden_city(pd, w / 2, 620 * s, 0.85 * s)
    palm(pd, 140 * s, 690 * s, 0.6 * s); palm(pd, w - 140 * s, 690 * s, 0.6 * s)
    for i, ln in enumerate(["Fertile soil", "Rivers full of gold", "A capital city awaits"]):
        pd.text((w / 2, 770 * s + i * 62 * s), "•  " + ln + "  •", font=F("serif_bold", int(44 * s)), fill=(60, 40, 20), anchor="mm")
    return pg


def poyais_note(d, x, y, s, a=255):
    d.rounded_rectangle((x - 200 * s, y - 100 * s, x + 200 * s, y + 100 * s), int(14 * s), fill=(232, 222, 190, a), outline=(110, 70, 40, a), width=max(int(6 * s), 2))
    d.rounded_rectangle((x - 180 * s, y - 80 * s, x + 180 * s, y + 80 * s), int(10 * s), outline=(110, 70, 40, a), width=max(int(2 * s), 1))
    d.text((x, y - 48 * s), "BANK OF POYAIS", font=F("serif_bold", int(34 * s)), fill=(110, 40, 40, a), anchor="mm")
    d.text((x, y + 14 * s), "ONE DOLLAR", font=F("sans_black", int(50 * s)), fill=(60, 40, 20, a), anchor="mm")
    d.ellipse((x + 120 * s - 34 * s, y + 20 * s, x + 120 * s + 34 * s, y + 88 * s), outline=(110, 40, 40, a), width=max(int(3 * s), 1))


# ======================= scenes =======================
def hook(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA")
    pr = draw_map(img, d, -84, 17, 34, T, hl=(), cy=820, bbox=AMER_BBOX)
    x, y = pr(-84.5, 15.0)
    glow = 0.5 + 0.5 * math.sin(T * 4)
    r = 70 + 10 * glow
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 210, 90, 70), outline=GOLDC, width=8)
    pill(d, y - 170, "POYAIS", INK, GOLDC, 60, x=x)
    tc(d, 260, "A COUNTRY FOR SALE", fit(d, "A COUNTRY FOR SALE", "sans_black", 96, W - 140), CREAM, 8, INK)
    if lt > dur * 0.55: slam(img, stamp_img("DIDN'T EXIST", RED, 110, -6), lt, dur * 0.55, 540, 1210)
    return img


def portrait(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 14))
    e = back(lt / 0.4)
    tc(d, 230, "GREGOR MacGREGOR", fit(d, "GREGOR MacGREGOR", "serif_bold", 100, W - 100), GOLDC + (int(255 * clamp(e)),))
    tc(d, 350, "Scottish soldier · adventurer", F("serif", 50), CREAM)
    d.rounded_rectangle((260, 470, 820, 1290), 20, fill=(60, 40, 20), outline=GOLDC, width=12)
    d.rounded_rectangle((290, 500, 790, 1260), 10, fill=(200, 180, 150))
    macgregor(d, 540, 1230, 1.0, T, "smug")
    return img


def to_london(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, -45 + 4 * k, 34, 9.5, T, hl=("GBR",), cy=800, bbox=AMER_BBOX)
    lx, ly = pr(-0.12, 51.5); px, py = pr(-84.5, 15.0)
    pill(d, 230, "LONDON · 1820s", INK, GOLDC, 50)
    d.ellipse((lx - 16, ly - 16, lx + 16, ly + 16), fill=RED, outline=CREAM, width=4)
    tc(d, ly + 26, "LONDON", F("sans_black", 44), CREAM, 6, (10, 20, 30), x=min(lx, W - 160))
    if lt > dur * 0.35:
        e = back((lt - dur * 0.35) / 0.4)
        d.ellipse((px - 22, py - 22, px + 22, py + 22), fill=GOLDC, outline=CREAM, width=4)
        pill(d, py + 40 + 20 * (1 - e), "POYAIS?", INK, GOLDC, 50, x=px)
        p = eio((lt - dur * 0.35) / (dur * 0.5)); cx, cy = (lx + px) / 2, min(ly, py) - 140
        pts = [((1 - u) ** 2 * lx + 2 * u * (1 - u) * cx + u * u * px, (1 - u) ** 2 * ly + 2 * u * (1 - u) * cy + u * u * py) for u in np.linspace(0, max(p, 0.01), 40)]
        for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=CREAM, width=7)
    macgregor(d, 880, 1300, 0.6, T, "smug")
    return img


def brochure(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    e = back(lt / 0.45); s = 0.7 + 0.25 * clamp(e)
    pg = brochure_page(s).rotate(-3 + 3 * (1 - clamp(e)), expand=True, resample=Image.BICUBIC)
    img.paste(pg, ((W - pg.width) // 2, 830 - pg.height // 2), pg); d = ImageDraw.Draw(img, "RGBA")
    for i in range(8):   # twinkling gold sparkles
        a = i * math.pi / 4 + T * 1.2; r = 430 + 20 * math.sin(T * 5 + i); x, y = 540 + r * 1.05 * math.cos(a), 830 + r * 1.2 * math.sin(a)
        z = 14 + 8 * math.sin(T * 6 + i); d.polygon([(x, y - z), (x + z * 0.3, y), (x, y + z), (x - z * 0.3, y)], fill=(255, 220, 120)); d.polygon([(x - z, y), (x, y + z * 0.3), (x + z, y), (x, y - z * 0.3)], fill=(255, 220, 120))
    tc(d, 220, "THE SALES PITCH", F("sans_black", 76), INK)
    return img


def notes(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 230, "HE EVEN PRINTED MONEY", fit(d, "HE EVEN PRINTED MONEY", "sans_black", 86, W - 100), GOLDC)
    n = int(1 + 7 * eio(lt / (dur * 0.6)))
    for i in range(n):
        poyais_note(d, 540 + (i % 2) * 30 - 15, 1240 - i * 56, 1.4)
    if lt > dur * 0.55:
        e = back((lt - dur * 0.55) / 0.4)
        card(d, (180, 360, 900, 520), [("LAND FOR SALE", "serif_bold", 70, (150, 30, 40)), ("in the new nation of Poyais", "serif", 40, INK)], fill=(250, 242, 220), outline=(120, 80, 40))
    return img


def loan(lt, dur, T):
    img = bg("curtain").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "LONDON'S INVESTORS LOVED IT", CREAM, (0, 0, 0, 170), 44)
    v = 200000 * eio((lt - 0.4) / (dur * 0.6))
    tc(d, 350, f"£{v:,.0f}", F("sans_black", 150), GOLDC, 8, INK)
    tc(d, 530, "raised for a country that didn't exist", F("serif_bold", 46), CREAM, 5, INK)
    for i, (x, c) in enumerate([(170, (30, 26, 30)), (390, (60, 30, 40)), (610, (40, 60, 50)), (830, (70, 50, 30))]):
        hop = 18 * abs(math.sin(T * 5 + i))
        merchant(d, x, 1240 - hop, 0.7, T + i, "happy", coat=c, arm=(x + 80, 860 - hop))
        coin(d, x + 80, 830 - hop, 1.5)
    return img


def voyage(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA")
    pr = draw_map(img, d, -45, 34, 9.5, T, hl=(), cy=800, bbox=AMER_BBOX)
    lx, ly = pr(-0.12, 51.5); px, py = pr(-84.5, 15.0)
    p = eio(lt / (dur * 0.9)); cx, cy = (lx + px) / 2, min(ly, py) - 140
    pts = [((1 - u) ** 2 * lx + 2 * u * (1 - u) * cx + u * u * px, (1 - u) ** 2 * ly + 2 * u * (1 - u) * cy + u * u * py) for u in np.linspace(0, max(p, 0.01), 40)]
    for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=CREAM, width=7)
    for k in range(3):
        q = max(0, min(len(pts) - 1, len(pts) - 1 - k * 4)); ship(d, pts[q][0], pts[q][1] - k * 6, 1.1 - k * 0.15)
    pill(d, 230, "1822 · THE SETTLERS SAIL", INK, GOLDC, 46)
    tc(d, 340, "ready for their new lives", F("serif_bold", 54), CREAM, 5, (10, 20, 30))
    for (x, y), lab in [((lx, ly), "LONDON"), ((px, py), "POYAIS")]:
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=RED, outline=CREAM, width=4)
        tc(d, y + 26, lab, F("sans_black", 42), CREAM, 6, (10, 20, 30), x=min(max(x, 200), W - 200))
    return img


def arrival(lt, dur, T):
    """The dream city fades away and the jungle takes over."""
    img = Image.new("RGB", (W, H), (150, 200, 230)); d = ImageDraw.Draw(img, "RGBA")
    k = eio((lt - 0.3) / (dur * 0.55))
    golden_city(d, 540, 1120, 1.4, int(255 * (1 - k)))
    jungle(d, 1180, k)
    for i in range(3):
        settler(d, 260 + i * 260, 1300, 0.6, T + i, "shock" if k > 0.6 else "happy")
    lines = ["NO CAPITAL CITY", "NO GOLD", "NO COUNTRY"]
    for i, ln in enumerate(lines):
        st = dur * 0.25 + i * dur * 0.18
        if lt > st:
            e = back((lt - st) / 0.3); tc(d, 230 + i * 110 + 15 * (1 - e), ln, F("sans_black", 90), RED + (int(255 * clamp(e)),), 8, CREAM)
    return img


def stranded(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 230, "STRANDED", F("sans_black", 130), RED)
    tc(d, 380, "disease spread quickly", F("serif_bold", 56), CREAM)
    total = 20; dead = int(11 * eio((lt - 0.6) / (dur * 0.6)))
    for i in range(total):
        x = 190 + (i % 5) * 175; y = 600 + (i // 5) * 170
        col = (90, 90, 96) if i < dead else (220, 200, 160)
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=col); d.rounded_rectangle((x - 40, y + 32, x + 40, y + 120), 26, fill=col)
    if lt > dur * 0.5:
        e = back((lt - dur * 0.5) / 0.35); pill(d, 1300 + 15 * (1 - e), "MORE THAN HALF DIED", CREAM, (150, 20, 34), 50)
    return img


def escape(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, 1, 49, 55 + 15 * k, T, hl=("FRA",), cy=780)
    lx, ly = pr(-0.12, 51.5); fx, fy = pr(2.35, 48.86)
    pill(d, 230, "MacGREGOR SLIPS AWAY", INK, GOLDC, 48)
    u = eio((lt - 0.2) / (dur * 0.6)); x = lx + (fx - lx) * u; y = ly + (fy - ly) * u
    d.line([(lx, ly), (x, y)], fill=CREAM, width=8)
    macgregor(d, x, y + 40, 0.35, T * 2, "smug")
    if lt > dur * 0.55: slam(img, stamp_img("SAME TRICK AGAIN", RED, 80, -6), lt, dur * 0.55, 540, 1240)
    return img


def free_man(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 230, "INCREDIBLY…", F("sans_black", 100), GOLDC)
    k = eio((lt - 0.3) / 0.8)
    macgregor(d, 540 + 360 * eio((lt - 1.1) / 1.2), 1180, 0.85, T, "smug")
    bars(d, 200, 420, 880, 1200, k)
    if lt > dur * 0.5:
        e = back((lt - dur * 0.5) / 0.35); pill(d, 1300 + 15 * (1 - e), "KEPT GOING FOR YEARS", CREAM, (150, 20, 34), 50)
    return img


def lesson(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    e = back(lt / 0.4)
    tc(d, 240 + 20 * (1 - e), "THE LESSON", F("sans_black", 110), INK)
    card(d, (120, 420, 960, 760), [("Always check that", "serif", 60, INK), ("what you're investing in", "serif", 60, INK), ("ACTUALLY EXISTS", "sans_black", 84, RED)])
    cx, cy, R = 520, 1060, 150   # magnifying glass revealing jungle where the "country" should be
    lens = Image.new("RGB", (W, H), (150, 200, 230)); ld = ImageDraw.Draw(lens, "RGBA"); jungle(ld, cy + 90, 0.45, seed=5)
    m = Image.new("L", (W, H)); ImageDraw.Draw(m).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
    img.paste(lens, (0, 0), m); d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(60, 40, 26), width=16)
    d.line([(cx + R * 0.72, cy + R * 0.72), (cx + R * 1.5, cy + R * 1.5)], fill=(60, 40, 26), width=40)
    return img


def map_icon(img, d, x, y, T):
    d.ellipse((x - 120, y - 120, x + 120, y + 120), fill=JUNGLE, outline=GOLDC, width=8)
    pill(d, y - 30, "POYAIS?", INK, GOLDC, 50, x=x)


theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
S = lambda say, draw, **kw: dict(say=say, draw=draw, **kw)
spec = dict(theme=theme, voice=25, speed=1.18, one_take=True, breath=0.0, bpm=100, music_amp=0.06, gap=0.06,
    chords=[[110, 130.8, 164.8], [98, 123.5, 146.8], [87.3, 110, 130.8], [98, 116.5, 146.8]],
    scenes=[
        S("Did you know a Scottish con man once convinced people to invest in a country that didn't exist?", hook, sfx=[("END-1.2", "stamp")], shake=[(2.6, 0.25, 12)]),
        S("His name was Gregor MacGregor.", portrait, tr="zoom", sfx=[(0.3, "ding")]),
        S("In the eighteen twenties, he arrived in London claiming to be the ruler of a land called Poyais, in Central America.", to_london, tr="whip"),
        S("He described a paradise: fertile soil, rivers full of gold, and a beautiful capital city waiting for settlers.", brochure, tr="zoom", sfx=[(0.3, "riser")]),
        S("He even printed Poyais banknotes, and sold land to eager investors.", notes, tr="whip", sfx=[(0.3 + 0.25 * i, "tick") for i in range(8)]),
        S("London's investors loved it. MacGregor raised a loan of around two hundred thousand pounds for his new nation.", loan, tr="whip", sfx=[(0.5 + 0.3 * i, "coin") for i in range(6)]),
        S("Then he sent the first settlers off to start their new lives.", voyage, tr="zoom"),
        S("When they arrived, there was no capital city. No gold. No country at all. Just untouched jungle, on the coast of what's now Honduras.", arrival, tr="whip", sfx=[("END-6.0", "thud"), ("END-4.6", "thud"), ("END-3.2", "thud")], drop=[(1.0, 3.0)]),
        S("The settlers were stranded. Disease spread quickly, and more than half of them died.", stranded, tr="whip"),
        S("MacGregor slipped away to France, and tried the same trick all over again.", escape, tr="whip", sfx=[("END-1.6", "stamp")]),
        S("Incredibly, he never spent long in prison, and kept running versions of the scheme for years.", free_man, tr="whip", sfx=[(0.5, "thud")]),
        S("The lesson? Always check that what you're investing in actually exists.", lesson, tr="zoom"),
        S("Would you have bought land in Poyais? Follow for more finance history.", lambda l, d_, T: cta_card(l, d_, T, "WOULD YOU HAVE", "BOUGHT LAND IN POYAIS?", lambda: bg("burgundy"), icon=map_icon), tr="flash", sfx=[(0.2, "riser")]),
    ])

if __name__ == "__main__":
    render(spec, sys.argv[1])
