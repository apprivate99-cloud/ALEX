import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit import *
from tulip_v2 import stamp_img, slam
STEEL=(60, 64, 72); NOTE=(196, 186, 150); NOTE_D=(110, 96, 70)

def note(d, x, y, s, label="1 MILLION", a=255):
    d.rounded_rectangle((x - 90 * s, y - 46 * s, x + 90 * s, y + 46 * s), int(6 * s), fill=NOTE + (a,), outline=NOTE_D + (a,), width=max(int(4 * s), 1))
    d.ellipse((x + 30 * s, y - 30 * s, x + 80 * s, y + 30 * s), outline=NOTE_D + (a,), width=max(int(3 * s), 1))
    f = F("serif_bold", max(int(26 * s), 6)); d.text((x - 80 * s, y - 36 * s), label, font=f, fill=NOTE_D + (a,))
    d.text((x - 80 * s, y + 4 * s), "MARK", font=F("serif_bold", max(int(30 * s), 6)), fill=NOTE_D + (a,))

def hook(lt, dur, T, phase):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA")
    if phase == 0:
        e = back(lt / 0.4); tc(d, 250, "1914", F("serif_bold", 160), GOLD + (int(255 * clamp(e)),))
        tc(d, 560, "$1 =", F("sans_black", 150), CREAM); tc(d, 740, "4.2 MARKS", F("sans_black", 150), (120, 220, 140))
        for i in range(4): note(d, 300 + i * 160, 1080 + 10 * math.sin(T * 3 + i), 0.8, "1")
        return img
    rng = np.random.default_rng(1)
    for i in range(int(min(lt / dur, 1) * 90)):  # notes flood the screen
        x, y = rng.uniform(0, W), rng.uniform(140, 1380); note(d, x, y + 20 * math.sin(T * 2 + i), rng.uniform(0.6, 1.1), "1 MILLION", 230)
    d.rounded_rectangle((50, 220, W - 50, 1060), 40, fill=(14, 16, 22, 245), outline=(70, 60, 50), width=4)
    e = back(lt / 0.4); tc(d, 250, "1923", F("serif_bold", 160), RED + (int(255 * clamp(e)),), 8, (10, 10, 10))
    zeros = min(12, int(12 * eio((lt - 0.3) / (dur * 0.7))))
    num = f"{4.2 * 10 ** zeros:,.0f}" if zeros else "4.2"
    tc(d, 560, "$1 =", F("sans_black", 150), CREAM, 8, (10, 10, 10))
    sz = 150
    while d.textlength(num, font=F("sans_black", sz)) > W - 180: sz -= 6
    tc(d, 760, num, F("sans_black", sz), RED, 8, (10, 10, 10)); tc(d, 760 + sz + 20, "MARKS", F("sans_black", 110), CREAM, 8, (10, 10, 10))
    return img

def ruhr(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, 9 - 3.5 * k, 50.5 - 0.3 * k, 62 + 18 * k, T, hl=("DEU",))
    rx, ry = pr(7.2, 51.45)
    if lt < dur * 0.45:
        pill(d, 250, "AFTER WWI: HUGE REPARATIONS", CREAM, (0, 0, 0, 170), 40)
    else:
        u = eio((lt - dur * 0.45) / 0.8)
        for lon, lat, nm in [(2.35, 48.86, "FRANCE"), (4.35, 50.85, "BELGIUM")]:
            sx, sy = pr(lon, lat); tc(d, sy + (30 if nm == "FRANCE" else -80), nm, F("sans_black", 40), CREAM, 6, (10, 20, 30), x=max(sx - (0 if nm == "FRANCE" else 90), 150)); ex, ey = sx + (rx - sx) * u, sy + (ry - sy) * u
            d.line([(sx, sy), (ex, ey)], fill=RED, width=16); ang = math.atan2(ey - sy, ex - sx)
            d.polygon([(ex + 30 * math.cos(ang), ey + 30 * math.sin(ang)), (ex + 26 * math.cos(ang + 2.3), ey + 26 * math.sin(ang + 2.3)), (ex + 26 * math.cos(ang - 2.3), ey + 26 * math.sin(ang - 2.3))], fill=RED)
        r = 40 + 10 * math.sin(T * 6); d.ellipse((rx - r, ry - r, rx + r, ry + r), outline=RED, width=10)
        pill(d, 250, "1923 · RUHR OCCUPIED", CREAM, (150, 20, 30), 44)
        tc(d, ry + 60, "RUHR", F("sans_black", 56), CREAM, 6, (10, 20, 30), x=rx)
    return img

def press(lt, dur, T):
    img = radial((80, 84, 92), (20, 22, 26)); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "THE GOVERNMENT'S FIX", CREAM, (0, 0, 0, 170), 40)
    d.rectangle((230, 820, 850, 1180), fill=STEEL); d.rectangle((200, 1150, 880, 1200), fill=(40, 42, 48))
    for cx in (400, 680):
        d.ellipse((cx - 110, 720, cx + 110, 940), fill=(90, 94, 104), outline=(30, 30, 34), width=8)
        for k2 in range(6):
            a = T * 8 + k2 * math.pi / 3; d.line([(cx, 830), (cx + 100 * math.cos(a), 830 + 100 * math.sin(a))], fill=(40, 42, 48), width=10)
    rng = np.random.default_rng(3)
    for i in range(60):
        st = i * 0.08; u = lt - st
        if u > 0:
            vx, vy = rng.uniform(-420, 420), rng.uniform(-800, -500); x = 540 + vx * u; y = 760 + vy * u + 1700 * u * u
            if y < 1400: note(d, x, y, 0.7)
    v = 10 ** (3 + 9 * eio(lt / dur)); tc(d, 360, f"{v:,.0f}", F("sans_black", 110), (120, 220, 140), 8, (10, 10, 10)); tc(d, 500, "marks printed", F("sans_bold", 56), CREAM)
    return img

def prices(lt, dur, T):
    img = radial((120, 96, 70), (40, 30, 22)); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "PRICES ROSE BY THE HOUR", CREAM, (150, 20, 30), 40)
    d.rounded_rectangle((80, 330, 760, 720), 20, fill=(30, 30, 30), outline=(150, 110, 60), width=10)
    tc(d, 360, "BREAD", F("serif_bold", 70), CREAM, x=420); v = 10 ** (3 + 8 * eio(lt / dur)); num = f"{v:,.0f}"
    sz = 110
    while d.textlength(num, font=F("sans_black", sz)) > 620: sz -= 6
    tc(d, 480, num, F("sans_black", sz), (255, 210, 80), x=420); tc(d, 620, "marks", F("sans_bold", 50), CREAM, x=420)
    cx, cy, R = 910, 525, 110; d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=CREAM, outline=INK, width=10)
    for a, l, wd in [(T * 12, 90, 8), (T * 1, 60, 12)]: d.line([(cx, cy), (cx + l * math.sin(a), cy - l * math.cos(a))], fill=INK, width=wd)
    x = -150 + (W + 300) * ((lt / dur) % 1.0)
    merchant(d, x, 1300, 0.7, T * 2, "shock", coat=(70, 70, 90), cap=True, beard=False, arm=(x + 110, 1150))
    d.polygon([(x + 110, 1150), (x + 330, 1130), (x + 300, 1230), (x + 140, 1230)], fill=(120, 80, 50)); d.ellipse((x + 270, 1220, x + 330, 1280), fill=(40, 30, 20))
    for i in range(5): note(d, x + 220 + (i % 2) * 20, 1120 - i * 28, 0.6)
    return img

def worthless(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 250, "WORTH LESS THAN PAPER", F("sans_black", 70), INK)
    n = int(14 * eio(lt / (dur * 0.6)))
    for i in range(n):
        note(d, 350 + (i % 2) * 24 - 12, 1120 - i * 46, 0.85)
    merchant(d, 120, 1200, 0.55, T, "happy", coat=(60, 90, 140), cap=True, beard=False, arm=(230, 1080))
    tc(d, 1240, "TOYS", F("sans_black", 64), RED, x=270)
    d.rectangle((640, 860, 960, 1200), fill=(30, 30, 34)); d.rectangle((760, 400, 820, 860), fill=(30, 30, 34))
    d.rectangle((680, 940, 920, 1100), fill=(20, 16, 14))
    for k2 in range(7):
        fx = 700 + k2 * 32; h = 90 + 50 * math.sin(T * 9 + k2 * 1.7)
        d.polygon([(fx, 1100), (fx + 16, 1100 - h), (fx + 32, 1100)], fill=(255, 120 + 60 * (k2 % 2), 30))
    u = (lt * 0.9) % 1; note(d, 600 + 160 * u, 900 + 120 * u, 0.5, a=int(255 * (1 - u)))
    tc(d, 1240, "FUEL", F("sans_black", 64), RED, x=800)
    return img

DATA = [(1914.5, 4.2), (1919.0, 8.9), (1920.0, 64.8), (1921.0, 64.9), (1922.0, 191.8), (1922.5, 493.2), (1923.0, 17972), (1923.5, 353412),
        (1923.62, 4620455), (1923.7, 98860000), (1923.79, 25260208000), (1923.87, 4.2e12)]
def chart_w(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA"); X0, X1, Y0, Y1 = 150, 980, 1220, 500
    tc(d, 250, "MARKS PER $1", F("sans_black", 76), CREAM); tc(d, 340, "log scale · approximate", F("sans_med", 34), (150, 156, 170))
    for p_ in range(0, 13, 3):
        y = Y0 - (Y0 - Y1) * p_ / 12.7; d.line([(X0, y), (X1, y)], fill=(255, 255, 255, 25), width=2)
        d.text((20, y - 18), ["1", "1K", "1M", "1B", "1T"][p_ // 3], font=F("sans_bold", 32), fill=(150, 156, 170))
    for yr in (1914, 1918, 1922): x = X0 + (X1 - X0) * (yr - 1914) / 10; tc(d, Y0 + 16, str(yr), F("sans_bold", 32), (150, 156, 170), x=x)
    tc(d, Y0 + 16, "1923", F("sans_bold", 32), RED, x=X1 - 40)
    p = eio(lt / (dur * 0.75)); xs = np.linspace(1914.5, 1914.5 + (1923.87 - 1914.5) * p, 200)
    ys = np.interp(xs, [a for a, _ in DATA], [math.log10(b) for _, b in DATA])
    pts = [(X0 + (X1 - X0) * (x - 1914) / 10, Y0 - (Y0 - Y1) * y / 12.7) for x, y in zip(xs, ys)]
    d.line(pts, fill=RED, width=10, joint="curve"); d.ellipse((pts[-1][0] - 14, pts[-1][1] - 14, pts[-1][0] + 14, pts[-1][1] + 14), fill=RED)
    if p > 0.98: e = back((lt - dur * 0.75) / 0.35); tc(d, 400 + 30 * (1 - e), "4.2 TRILLION", F("sans_black", 110), RED + (int(255 * clamp(e)),), 8, (10, 10, 10))
    return img

def renten(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "NOVEMBER 1923", CREAM, (40, 40, 40), 40)
    for i in range(18): note(d, 270 + (i % 3) * 40 - 40, 1050 - (i // 3) * 70 - (i % 3) * 8, 0.95)
    tc(d, 1150, "1,000,000,000,000", F("sans_black", 50), INK, x=270); tc(d, 1210, "old marks", F("serif", 44), INK, x=270)
    e = eio((lt - 0.6) / 0.5); tc(d, 760, "=", F("sans_black", 160), INK + (int(255 * e),), x=540)
    if lt > 1.0:
        e2 = back((lt - 1.0) / 0.4); s = 1.6 * clamp(e2)
        d.rounded_rectangle((800 - 110 * s, 860 - 60 * s, 800 + 110 * s, 860 + 60 * s), 10, fill=(170, 200, 170), outline=(40, 90, 50), width=6)
        d.text((800 - 90 * s, 860 - 50 * s), "1", font=F("sans_black", max(int(80 * s), 6)), fill=(30, 80, 40))
        tc(d, 1150, "1", F("sans_black", 50), INK, x=800); tc(d, 1210, "Rentenmark", F("serif", 44), INK, x=800)
    slam(img, stamp_img("IT WORKED", (30, 120, 60), 100), lt, dur - 1.6, 540, 470)
    return img

def end_w(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA"); rng = np.random.default_rng(4)
    for i in range(40):
        ny = (rng.uniform(0, H) + T * 60) % (H + 100) - 50
        if not 200 < ny < 1150: note(d, rng.uniform(0, W), ny, 0.7, a=60)
    e = back(lt / 0.4); tc(d, 380 + 30 * (1 - e), "MONEY", F("sans_black", 170), CREAM); tc(d, 560, "IS JUST", F("sans_black", 110), (150, 156, 170))
    tc(d, 690, "TRUST", F("sans_black", 220), GOLD)
    if lt > dur * 0.5: e2 = back((lt - dur * 0.5) / 0.4); pill(d, 1000 + 40 * (1 - e2), "FOLLOW FOR MORE MONEY HISTORY", INK, GOLD, 50)
    return img

theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
S = lambda say, draw, **kw: dict(say=say, draw=draw, **kw)
spec = dict(theme=theme, voice=26, speed=1.32, bpm=96, music_amp=0.06, gap=0.12,
    chords=[[110, 130.8, 164.8], [98, 123.5, 146.8], [87.3, 110, 130.8], [82.4, 103.8, 123.5]],
    scenes=[
        S("In nineteen fourteen, one US dollar was worth four point two German marks.", lambda l, d_, T: hook(l, d_, T, 0), sfx=[(0.3, "coin")]),
        S("Just nine years later, that same dollar was worth four point two trillion marks.", lambda l, d_, T: hook(l, d_, T, 1), tr="flash", sfx=[(0.3 + 0.12 * i, "tick") for i in range(12)] + [("END-0.2", "boom")], shake=[(2.0, 0.4, 16)]),
        S("So how did this happen? After World War One, Germany owed enormous reparations. Then, in nineteen twenty three, France and Belgium occupied the Ruhr, Germany's industrial heartland.", ruhr, tr="zoom", sfx=[("END-3.2", "thud")]),
        S("The workers there went on strike, and the government kept paying them by printing more and more money.", press, tr="whip", sfx=[(0.5 + 0.25 * i, "tick") for i in range(16)]),
        S("Soon, prices were rising by the hour. Some workers were paid twice a day, and they rushed to the shops before their wages lost value.", prices, tr="whip", sfx=[(0.4 + 0.3 * i, "tick") for i in range(20)]),
        S("Banknotes became so worthless that children played with bundles of them, and people burned them in their stoves for heat.", worthless, tr="whip"),
        S("By late nineteen twenty three, the mark was effectively worthless, and a lifetime of savings had been wiped out.", chart_w, tr="whip", sfx=[("END-1.8", "boom")], shake=[(3.5, 0.4, 18)]),
        S("Finally, in November nineteen twenty three, Germany launched a new currency called the Rentenmark, swapping one new mark for one trillion old ones. Remarkably, it worked.", renten, tr="whip", sfx=[(1.0, "pop"), ("END-1.6", "stamp")]),
        S("The lesson? Money only works as long as people trust it. Follow for more money history.", end_w, tr="zoom"),
    ])

if __name__ == "__main__":
    render(spec, sys.argv[1])
