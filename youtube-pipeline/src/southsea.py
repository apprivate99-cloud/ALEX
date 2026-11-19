import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit import *
import kit
kit.ERA = "1700s"
kit.COIN_SYM = "£"
from tulip_v2 import stamp_img, slam
from kit2 import map_face
WIG=(236, 232, 222); WIG_D=(196, 190, 176); NAVY=(16, 30, 60)

def newton(d, x, y, s, t, mood="happy", look=0, arm=None):
    b = math.sin(t * 5 + x) * 4 * s; hy = y + b - 410 * s
    for side in (-1, 1):  # curls behind the face
        for k in range(4):
            cx = x + side * (58 + 6 * k) * s; cy = hy - 20 * s + k * 42 * s
            d.ellipse((cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s), fill=WIG, outline=WIG_D, width=max(int(3 * s), 1))
    merchant(d, x, y, s, t, mood, coat=(90, 50, 40), hat=False, beard=False, look=look, arm=arm)
    for k in range(5):  # curls on top
        cx = x + (-52 + k * 26) * s; d.ellipse((cx - 26 * s, hy - 92 * s, cx + 26 * s, hy - 40 * s), fill=WIG, outline=WIG_D, width=max(int(3 * s), 1))

def hook(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 14))
    tc(d, 220, "ISAAC NEWTON", F("serif_bold", 100), GOLD); tc(d, 335, "genius. physicist. investor?", F("serif", 52), CREAM)
    shock = lt > dur * 0.62
    newton(d, 540, 1250, 1.2, T, "shock" if shock else "happy")
    hy = 1250 - 410 * 1.2; u = lt / 0.9
    ay = (430 + (hy - 140 - 430) * u * u) if u < 1 else hy - 140 - 160 * math.sin(min((lt - 0.9) / 0.6, 1) * math.pi) * math.exp(-(lt - 0.9))
    ax = 560 + (0 if u < 1 else 260 * min((lt - 0.9) / 0.6, 1.5))
    if lt < 1.5:  # apple drops, bounces off, then is gone
        d.ellipse((ax - 40, ay - 40, ax + 40, ay + 40), fill=(200, 30, 40)); d.line([(ax, ay - 40), (ax + 8, ay - 64)], fill=(80, 50, 20), width=8)
        d.ellipse((ax + 8, ay - 70, ax + 44, ay - 54), fill=LEAF)
    slam(img, stamp_img("LOST A FORTUNE", RED, 66, -4), lt, dur * 0.62, 540, 515)
    return img

def atlantic(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, -32 + 4 * k, 12, 11, T, hl=("GBR",), cy=860, bbox=(-120, 40, -60, 72))
    lx, ly = pr(-0.12, 51.5); sx, sy = pr(-60, -12)
    p = eio((lt - 0.4) / (dur * 0.6)); cx, cy = (lx + sx) / 2 - 120, (ly + sy) / 2
    pts = [((1 - u) ** 2 * lx + 2 * u * (1 - u) * cx + u * u * sx, (1 - u) ** 2 * ly + 2 * u * (1 - u) * cy + u * u * sy) for u in np.linspace(0, p, 40)]
    for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=CREAM, width=8)
    ship(d, pts[-1][0], pts[-1][1], 1.2)
    bx, by = pr(-1.8, 53.0); map_face(d, bx, by, 0.5, "happy" if lt < dur * 0.55 else "shock", T)
    if lt > dur * 0.55:
        for i in range(5):
            x = 470 + i * 125; e = back((lt - dur * 0.55 - i * 0.12) / 0.3)
            if e <= 0: continue
            ship(d, x, 1190, 1.0)
            if i > 0: d.line([(x - 40, 1130), (x + 40, 1210)], fill=RED, width=10); d.line([(x + 40, 1130), (x - 40, 1210)], fill=RED, width=10)
    for (x, y), lab in [((lx, ly), "LONDON"), ((sx, sy), "SOUTH AMERICA")]:
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=RED, outline=CREAM, width=4); tc(d, y + 26, lab, F("sans_black", 44), CREAM, 6, (10, 20, 30), x=min(max(x, 220), W - 220))
    pill(d, 230, "1720 · THE SOUTH SEA COMPANY", INK, GOLD, 40)
    if lt > dur * 0.15:
        late = lt > dur * 0.55; e = back((lt - (dur * 0.55 if late else dur * 0.15)) / 0.4)
        d.rectangle((0, 1240, W, 1340), fill=(120, 16, 28, 235) if late else (10, 20, 30, 230))
        txt = "SPAIN'S LIMIT: 1 SHIP A YEAR" if late else "promised: riches from trade"
        tc(d, 1256, txt, fit(d, txt, "sans_black" if late else "serif_bold", 54, W - 100), (CREAM if late else GOLD) + (int(255 * clamp(e)),))
    return img

def hype(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 240, "SOUTH SEA COMPANY", F("serif_bold", 76), INK)
    for i, (lab, val, col) in enumerate([("REAL PROFITS", 0.06, (90, 90, 90)), ("HYPE", 1.0, RED)]):
        st = 0.2 + i * (dur * 0.45); e = eio((lt - st) / 0.7); x = 230 + i * 420; top = 1150 - 750 * val * e
        d.rectangle((x, top, x + 200, 1150), fill=col); tc(d, 1170, lab, F("sans_black", 50), INK, x=x + 100)
    return img

PTS = [(0, 128), (1, 175), (2, 330), (3, 350), (4, 550), (5, 890), (5.7, 1050), (6.5, 1000), (7.5, 900), (8.5, 190), (9.5, 210), (11, 124)]
MONTHS = ["JAN", "", "MAR", "", "MAY", "", "JUL", "", "SEP", "", "NOV", ""]
def chart_ss(lt, dur, T, m0, m1, marks=(), crash=False, title="SOUTH SEA SHARES (£)"):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA"); X0, X1, Y0, Y1 = 150, 980, 1180, 560
    tc(d, 240, title, F("sans_black", 64), CREAM); tc(d, 320, "approximate prices, 1720", F("sans_med", 34), (150, 156, 170))
    for v in (250, 500, 750, 1000):
        y = Y0 - (Y0 - Y1) * v / 1100; d.line([(X0, y), (X1, y)], fill=(255, 255, 255, 25), width=2); d.text((30, y - 18), f"£{v}", font=F("sans_bold", 30), fill=(150, 156, 170))
    for i, m in enumerate(MONTHS):
        if m: tc(d, Y0 + 16, m, F("sans_bold", 30), (150, 156, 170), x=X0 + (X1 - X0) * i / 11)
    P = lambda m, v: (X0 + (X1 - X0) * m / 11, Y0 - (Y0 - Y1) * v / 1100)
    mm = m0 + (m1 - m0) * eio(lt / max(dur * 0.7, 0.5)); xs = np.linspace(0, mm, 200)
    ys = np.interp(xs, [a for a, _ in PTS], [b for _, b in PTS]); pts = [P(a, b) for a, b in zip(xs, ys)]
    col = RED if crash and mm > 7.6 else (70, 210, 120)
    d.polygon(pts + [(pts[-1][0], Y0), (X0, Y0)], fill=col + (40,)); d.line(pts, fill=col, width=10, joint="curve")
    d.ellipse((pts[-1][0] - 14, pts[-1][1] - 14, pts[-1][0] + 14, pts[-1][1] + 14), fill=col)
    for k2, (m, v, lab, c) in enumerate(marks):
        if mm >= m:
            x, y = P(m, v); d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=c, outline=CREAM, width=5)
            n_ = str(k2 + 1); f = F("sans_black", 32); d.text((x - d.textlength(n_, font=f) / 2, y - 19), n_, font=f, fill=CREAM)
            ly = 400 + k2 * 60; d.ellipse((150, ly, 194, ly + 44), fill=c); d.text((172 - d.textlength(n_, font=f) / 2, ly + 4), n_, font=f, fill=CREAM)
            d.text((210, ly + 2), lab, font=F("sans_bold", 36), fill=CREAM)
    v_now = float(np.interp(mm, [a for a, _ in PTS], [b for _, b in PTS])); f2 = F("sans_black", 70); s2 = f"£{v_now:,.0f}"
    d.text((X1 - d.textlength(s2, font=f2), 400), s2, font=f2, fill=col)
    return img

SOLD = (3, 350, "Newton sells (April)", (40, 120, 70)); BUY = (5.3, 700, "Newton buys back (June)", (190, 40, 50))

def fomo(lt, dur, T):
    img = bg("tavern").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "LONDON COFFEE HOUSE · SUMMER 1720", CREAM, (0, 0, 0, 160), 36)
    merchant(d, 200, 1180, 0.8, T, "happy", arm=(300, 820 + 30 * math.sin(T * 8)))
    merchant(d, 470, 1180, 0.8, T + 2, "smug", coat=(60, 30, 40), arm=(560, 820 + 30 * math.sin(T * 8 + 1)))
    for i in range(8):
        u = (T * 1.3 + i * 0.37) % 1; coin(d, 250 + i * 40, 800 - 300 * math.sin(u * math.pi), 1.0)
    newton(d, 840, 1180, 0.8, T, "sad", look=-1)
    bx, by = 840, 520; d.ellipse((bx - 150, by - 90, bx + 150, by + 90), fill=CREAM); d.ellipse((bx - 30, by + 100, bx, by + 130), fill=CREAM); d.ellipse((bx - 10, by + 140, bx + 8, by + 158), fill=CREAM)
    tc(d, by - 50, "£££ ?", F("sans_black", 80), RED, x=bx)
    return img

def loss(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    v = 20000 * eio((lt - 0.2) / (dur * 0.5)); tc(d, 280, f"-£{v:,.0f}", F("sans_black", 160), RED, 8, (10, 4, 6))
    tc(d, 470, "reportedly", F("serif", 52), CREAM)
    if lt > dur * 0.55: e = back((lt - dur * 0.55) / 0.4); pill(d, 560 + 30 * (1 - e), "≈ MILLIONS IN TODAY'S MONEY", INK, GOLD, 48)
    newton(d, 540, 1300, 1.0, T, "sad")
    rng = np.random.default_rng(7)
    for i in range(16):
        u = ((lt * 0.6 + i / 16) % 1); side = 1 if i % 2 else -1; a = rng.uniform(-0.5, 0.3)
        coin(d, 540 + side * (90 + math.cos(a) * 600 * u), 1060 + math.sin(a) * 600 * u + 300 * u * u, 0.9, int(255 * (1 - u)))
    return img

def quote(lt, dur, T, phase=0):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((90, 300, 990, 1050), fill=(250, 242, 222), outline=INK, width=5); tc(d, 300, "“", F("serif_bold", 220), RED)
    lines = ["I can calculate", "the motions of the", "heavenly bodies,", "but not the", "madness of people."]
    for i, ln in enumerate(lines):
        e = 1 if phase else eio((lt - 0.2 - i * 0.35) / 0.4); tc(d, 520 + i * 92, ln, F("serif", 68), INK + (int(255 * e),))
    tc(d, 985, "— attributed to Isaac Newton", F("serif", 40), INK)
    if phase: slam(img, stamp_img("NO SOLID EVIDENCE", RED, 72, -5), lt, 0.5, 540, 1190)
    return img

def end_ss(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 14))
    e = back(lt / 0.4); tc(d, 250 + 30 * (1 - e), "EVEN GENIUSES", F("sans_black", 110), CREAM); tc(d, 380, "GET FOMO", F("sans_black", 150), GOLD)
    newton(d, 540, 1250, 1.0, T, "smug" if lt > 1 else "happy")
    if lt > dur * 0.5: e2 = back((lt - dur * 0.5) / 0.4); pill(d, 580 + 40 * (1 - e2), "FOLLOW FOR MORE MONEY HISTORY", INK, GOLD, 48)
    return img

ERMINE = (250, 248, 240)
def king(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 14))
    tc(d, 220, "SOUTH SEA COMPANY", fit(d, "SOUTH SEA COMPANY", "serif_bold", 90, W - 120), GOLD)
    tc(d, 330, "London, 1720", F("serif", 52), CREAM)
    x, y, s = 540, 1250, 1.1
    merchant(d, x, y, s, T, "smug", coat=(150, 20, 34), hat=False, beard=False)
    hy = y + math.sin(T * 5 + x) * 4 * s - 410 * s
    d.polygon([(x - 64 * s, hy - 50 * s), (x - 70 * s, hy - 130 * s), (x - 32 * s, hy - 90 * s), (x, hy - 150 * s), (x + 32 * s, hy - 90 * s), (x + 70 * s, hy - 130 * s), (x + 64 * s, hy - 50 * s)], fill=GOLD, outline=(150, 104, 30))
    for cx in (x - 70 * s, x, x + 70 * s): d.ellipse((cx - 12, hy - 150 * s - 4 if cx == x else hy - 130 * s - 4, cx + 12, (hy - 150 * s if cx == x else hy - 130 * s) + 20), fill=RED)
    if lt > dur * 0.35:
        e = back((lt - dur * 0.35) / 0.4); pill(d, 430 + 30 * (1 - e), "GOVERNOR: KING GEORGE I", INK, GOLD, 52)
    return img

def bubble_cos(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "COPYCAT 'BUBBLE' COMPANIES", fit(d, "COPYCAT 'BUBBLE' COMPANIES", "sans_black", 66, W - 120), INK)
    n = int(16 * eio(lt / (dur * 0.5)))
    for i in range(n):
        x = 180 + (i % 4) * 240; y = 340 + (i // 4) * 120
        d.rounded_rectangle((x - 105, y, x + 105, y + 96), 12, fill=(246, 236, 210), outline=(110, 80, 50), width=5)
        tc(d, y + 10, "& CO.", F("serif_bold", 40), INK, x=x); tc(d, y + 56, f"No. {i * 12 + 1}", F("serif", 30), (110, 80, 50), x=x)
    cnt = int(200 * eio(lt / (dur * 0.5)))
    tc(d, 830, f"~{cnt} sprang up", F("sans_black", 80), RED)
    if lt > dur * 0.6:
        slam(img, stamp_img("BANNED", RED, 100, -6), lt, dur * 0.6, 540, 1060)
        d = ImageDraw.Draw(img, "RGBA"); e = eio((lt - dur * 0.6) / 0.4)
        pill(d, 1240, "THE BUBBLE ACT · JUNE 1720", CREAM, (150, 20, 34, int(255 * e)), 40)
    return img

def hutcheson(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "ONE MAN SAW IT COMING", fit(d, "ONE MAN SAW IT COMING", "sans_black", 74, W - 120), INK)
    tc(d, 320, "Archibald Hutcheson, politician", F("serif_bold", 50), RED)
    merchant(d, 270, 1250, 0.95, T, "smug", coat=(30, 60, 50), arm=(470, 900))
    pg = Image.new("RGBA", (420, 540), (0, 0, 0, 0)); pd = ImageDraw.Draw(pg)
    pd.rectangle((0, 0, 419, 539), fill=(250, 242, 220), outline=INK, width=6); pd.rectangle((16, 16, 403, 523), outline=INK, width=2)
    for i, (txt, sz) in enumerate([("A WARNING", 56), ("on South-Sea", 36), ("Stock", 36), ("1720", 34)]):
        f = fit(pd, txt, "serif_bold", sz, 360); w = pd.textlength(txt, font=f); pd.text(((420 - w) / 2, [50, 140, 190, 460][i]), txt, font=f, fill=INK if i != 0 else RED)
    for k in range(6): pd.line([(60, 270 + k * 28), (360, 270 + k * 28)], fill=(160, 140, 120), width=3)
    e = eio(lt / 0.5); pg = pg.rotate(5 * (1 - e) + 3, expand=True, resample=Image.BICUBIC)
    img.paste(pg, (int(560 + 200 * (1 - e)), 520), pg)
    return img

theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
S = lambda say, draw, **kw: dict(say=say, draw=draw, **kw)
spec = dict(theme=theme, voice=26, speed=1.08, one_take=True, bpm=108, music_amp=0.06, gap=0.16,
    chords=[[130.8, 164.8, 196], [110, 130.8, 164.8], [87.3, 110, 130.8], [98, 123.5, 146.8]],
    scenes=[
        S("Did you know that Isaac Newton, one of the smartest people who ever lived, lost a fortune on a single stock?", hook, sfx=[(0.9, "pop"), ("END-1.9", "stamp")], shake=[(0.9, 0.2, 10)]),
        S("In seventeen twenty, everyone in London wanted shares in the South Sea Company. Even King George the First was its governor.", king, tr="zoom", sfx=[("END-2.2", "ding")]),
        S("It promised huge riches from trade with South America. But Spain allowed it just one trading ship a year.", atlantic, tr="whip", sfx=[("END-2.0", "thud")]),
        S("Real profits were tiny, but the hype was enormous, and insiders even bribed politicians to keep the price climbing.", hype, tr="whip", sfx=[("END-1.8", "riser")]),
        S("Around two hundred copycat bubble companies sprang up, so the South Sea Company pushed through a law, the Bubble Act, to shut its rivals down.",
          bubble_cos, tr="whip", sfx=[(0.3 + 0.12 * i, "pop") for i in range(0, 20, 2)] + [("END-1.0", "stamp")]),
        S("As the shares took off, Newton got in early. He sold in April, and walked away with a healthy profit.",
          lambda l, d_, T: chart_ss(l, d_, T, 0, 3, [SOLD]), tr="whip", sfx=[("END-1.5", "coin"), ("END-1.4", "ding")]),
        S("But the price kept climbing. By the summer, shares had hit around a thousand pounds, and his friends were getting rich.",
          lambda l, d_, T: chart_ss(l, d_, T, 3, 5.7, [SOLD]), tr=None),
        S("Newton couldn't bear to watch from the sidelines.", fomo, tr="whip"),
        S("So he jumped back in, just as the price was near its peak.", lambda l, d_, T: chart_ss(l, d_, T, 5.0, 5.4, [SOLD, BUY]), tr="whip", sfx=[(0.6, "thud")]),
        S("Not everyone was fooled. A politician named Archibald Hutcheson published pamphlets warning that the share price made no sense.", hutcheson, tr="whip"),
        S("Then the bubble burst. By December, the shares had fallen right back to where they started the year.",
          lambda l, d_, T: chart_ss(l, d_, T, 5.4, 11, [SOLD, BUY], crash=True), tr="whip", sfx=[(1.2, "boom")], shake=[(1.2, 0.5, 22)], drop=[(1.1, 2.6)]),
        S("Newton reportedly lost around twenty thousand pounds, which would be millions in today's money.", loss, tr="whip"),
        S("He's often quoted as saying: I can calculate the motions of the heavenly bodies, but not the madness of people.", quote, tr="whip"),
        S("The funny thing is, there's no solid evidence that he ever actually said it.", lambda l, d_, T: quote(l, d_, T, 1), tr=None, sfx=[(0.5, "stamp")], shake=[(0.52, 0.25, 14)]),
        S("The lesson? Even geniuses can fall for the fear of missing out. Follow for more money history.", end_ss, tr="zoom"),
    ])

if __name__ == "__main__":
    render(spec, sys.argv[1])
