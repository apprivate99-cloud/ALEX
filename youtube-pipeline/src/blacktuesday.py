"""Black Tuesday, 1929: the 'permanently high plateau', margin debt, and a 25-year recovery."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit2 import *
import kit
kit.ERA = "1920s"
kit.COIN_SYM = "$"

# Dow Jones Industrial Average, approximate (x = year)
DOW = [(1928.0, 200), (1928.5, 210), (1929.0, 300), (1929.67, 381), (1929.82, 230), (1929.87, 199), (1930.29, 294), (1930.95, 165), (1931.95, 78), (1932.52, 41)]
X_A, X_B = 1928.0, 1932.6
def dow_pts(): return [((x - X_A) / (X_B - X_A), v) for x, v in DOW]
XLAB = [(0.0, "1928"), ((1929 - X_A) / (X_B - X_A), "1929"), ((1930 - X_A) / (X_B - X_A), "1930"), ((1931 - X_A) / (X_B - X_A), "1931"), ((1932 - X_A) / (X_B - X_A), "1932")]
YLAB = [(100, "100"), (200, "200"), (300, "300"), (400, "400")]
FISHER_COAT = (60, 60, 70)


US_BBOX = (-130, -60, 20, 55)


def us_map(img, d, T, mood, zoom=0.0):
    pr = draw_map(img, d, -95 + 20 * zoom, 38 + 1 * zoom, 12.5 + 14 * zoom, T, hl=("USA",), cy=760, bbox=US_BBOX)
    fx, fy = pr(-99, 39.5)
    map_face(d, fx, fy, 2.0, mood, T)
    return pr


def hook_map(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA")
    pr = us_map(img, d, T, "happy" if lt < 0.6 else "shock")
    nx, ny = pr(-74.0, 40.7)
    d.ellipse((nx - 16, ny - 16, nx + 16, ny + 16), fill=RED, outline=CREAM, width=4)
    tc(d, ny - 80, "WALL STREET", F("sans_black", 38), CREAM, 5, (10, 20, 30), x=nx - 90)
    if lt > 0.6: coin_drain(d, nx, ny + 40, T, n=12, spread=60, fall=380)
    pill(d, 230, "OCTOBER 1929", INK, GOLD, 50)
    v = 23 * eio((lt - 0.6) / (dur * 0.5))
    tc(d, 1130, f"-{v:.0f}%", F("sans_black", 170), RED, 10, (20, 4, 6))
    tc(d, 1330, "in just two days", F("serif_bold", 54), CREAM, 5, (10, 20, 30))
    return img


def fisher(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "OCTOBER 15, 1929", CREAM, (40, 40, 40), 46)
    words = ["Stock prices have reached", "what looks like a", "permanently high plateau."]
    lines = [(ln, "serif_bold" if i == 2 else "serif", 60, INK + (int(255 * eio((lt - 0.3 - i * 0.5) / 0.4)),)) for i, ln in enumerate(words)]
    card(d, (90, 360, 990, 760), [("“", "serif_bold", 120, RED)] + lines + [("Irving Fisher, economist", "sans_bold", 38, (110, 80, 50, int(255 * eio((lt - 1.8) / 0.4))))])
    merchant(d, 540, 1360, 0.8, T, "smug", coat=FISHER_COAT, hat=False, beard=False)
    hx, hy = 540, 1360 - 410 * 0.8 + math.sin(T * 5 + 540) * 4 * 0.8
    d.ellipse((hx - 46, hy - 26, hx - 4, hy + 8), outline=INK, width=5); d.ellipse((hx + 4, hy - 26, hx + 46, hy + 8), outline=INK, width=5)
    return img


def bankers(lt, dur, T):
    img = deco_bg(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "OCTOBER 24 · AFTERNOON", INK, GOLD, 44)
    tc(d, 330, "Top bankers step in", F("serif_bold", 60), CREAM)
    for i, (x, c) in enumerate([(220, (30, 30, 40)), (540, (40, 40, 60)), (860, (30, 40, 34))]):
        merchant(d, x, 1240, 0.8, T + i, "smug", coat=c, arm=(x + 90, 820 + 20 * math.sin(T * 4 + i)))
        coin(d, x + 90, 790 + 20 * math.sin(T * 4 + i), 1.6)
    e = back((lt - dur * 0.55) / 0.4)
    if lt > dur * 0.55: pill(d, 470 + 20 * (1 - e), "IT WORKED... FOR A FEW DAYS", CREAM, (150, 20, 34), 44)
    return img


def two_days(lt, dur, T):
    img = deco_bg(); d = ImageDraw.Draw(img, "RGBA")
    for i, (day, name, pct) in enumerate([(28, "MONDAY", 12.8), (29, "TUESDAY", 11.7)]):
        st = 0.2 + i * dur * 0.32; e = back((lt - st) / 0.4)
        if lt < st: continue
        x = 300 + i * 480
        calendar(d, x, 470, 0.95, "OCT", day, 1929)
        tc(d, 660, f"BLACK {name}", F("sans_black", 52), RED, 5, (10, 10, 10), x=x)
        tc(d, 740 + 20 * (1 - e), f"-{pct * clamp(e):.1f}%", F("sans_black", 100), CREAM + (int(255 * clamp(e)),), 6, (10, 10, 10), x=x)
    if lt > dur * 0.65:
        e = back((lt - dur * 0.65) / 0.4)
        n = 16410030 * eio((lt - dur * 0.65) / 1.2)
        tc(d, 960, f"{n:,.0f}", F("sans_black", 96), DECO, 6, (10, 10, 10))
        tc(d, 1080, "shares traded on Tuesday", F("serif_bold", 50), CREAM)
    return img


def spiral(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "THE DEATH SPIRAL", F("sans_black", 96), RED)
    cx, cy, R = 540, 820, 290
    steps = ["PRICES FALL", "MARGIN CALLS", "FORCED SELLING"]
    active = int((lt * 1.2) % 3)
    for k in range(3):  # arrows around the circle
        a0 = math.radians(-90 + k * 120 + 25); a1 = math.radians(-90 + (k + 1) * 120 - 25)
        d.arc((cx - R, cy - R, cx + R, cy + R), math.degrees(a0), math.degrees(a1), fill=(200, 60, 60), width=14)
        ax, ay = cx + R * math.cos(a1), cy + R * math.sin(a1); tang = a1 + math.pi / 2
        d.polygon([(ax + 30 * math.cos(tang), ay + 30 * math.sin(tang)), (ax + 22 * math.cos(tang + 2.4), ay + 22 * math.sin(tang + 2.4)), (ax + 22 * math.cos(tang - 2.4), ay + 22 * math.sin(tang - 2.4))], fill=(200, 60, 60))
    for k, lab in enumerate(steps):
        a = math.radians(-90 + k * 120); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        e = clamp((lt - 0.3 - k * 0.5) / 0.3)
        if e <= 0: continue
        on = k == active and lt > 1.8
        pill(d, y - 38, lab, CREAM if on else INK, (200, 30, 40) if on else GOLD, 40, x=min(max(x, 230), W - 230))
    v = 381 - 150 * eio(lt / dur)
    tc(d, cy - 60, f"{v:,.0f}", F("sans_black", 110), RED, x=cx); tc(d, cy + 60, "DOW", F("sans_bold", 40), CREAM, x=cx)
    return img


def thousand(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "$1,000 INVESTED AT THE PEAK", fit(d, "$1,000 INVESTED AT THE PEAK", "sans_black", 70, W - 100), INK)
    tc(d, 320, "was worth, by July 1932...", F("serif_bold", 54), (110, 80, 50))
    k = eio((lt - 0.4) / (dur * 0.6)); val = 1000 - (1000 - 108) * k
    n = max(1, int(round(10 * (1 - 0.9 * k))))
    for i in range(n):  # stack of $100 notes shrinking
        y = 1040 - i * 46
        d.rounded_rectangle((360, y - 30, 720, y + 30), 8, fill=(140, 190, 140), outline=(40, 100, 50), width=4)
        tc(d, y - 24, "$100", F("sans_black", 40), (30, 90, 40))
    tc(d, 1160, f"${val:,.0f}", F("sans_black", 150), RED if k > 0.5 else (30, 110, 60))
    return img


def banks(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA")
    pr = us_map(img, d, T, "sad")
    pill(d, 230, "THE GREAT DEPRESSION", CREAM, (150, 20, 34), 48)
    spots = [(-74.0, 41.5), (-84.4, 33.7), (-87.6, 44.0), (-118.2, 34.0), (-122.4, 44.0), (-95.4, 29.8), (-111.9, 40.8)]
    for i, (lon, lat) in enumerate(spots):
        st = 0.3 + i * 0.25
        if lt < st: continue
        x, y = pr(lon, lat); e = back((lt - st) / 0.3)
        us_bank(d, x, y + 40, 0.42 * clamp(e) + 0.01, closed=True)
    tc(d, 1240, "thousands of banks failed", F("serif_bold", 56), CREAM, 5, (10, 20, 30))
    return img


def roaring(lt, dur, T):
    img = deco_bg(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "THE ROARING TWENTIES", fit(d, "THE ROARING TWENTIES", "sans_black", 84, W - 100), DECO)
    for i, (x, c) in enumerate([(170, (30, 26, 30)), (400, (60, 40, 70)), (630, (40, 60, 50)), (860, (70, 50, 30))]):
        jump = 24 * abs(math.sin(T * 5 + i))
        merchant(d, x, 1260 - jump, 0.72, T + i, "happy", coat=c, arm=(x + 80, 870 - jump))
    rng = np.random.default_rng(3)
    for i in range(14):
        u = (T * 0.5 + i / 14) % 1; coin(d, rng.uniform(80, 1000), 500 + 360 * u, 1.2, int(255 * (1 - u)))
    tc(d, 350, "STOCKS ↑", F("sans_black", 90), GREEN_UP)
    return img


def margin(lt, dur, T):
    img = bg("ledger").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "BUYING ON MARGIN", F("sans_black", 80), INK)
    tc(d, 320, "a small deposit, the rest borrowed", F("serif_bold", 50), RED)
    X0, X1, Y = 140, 940, 560; e = eio((lt - 0.2) / 1.0); split = X0 + (X1 - X0) * 0.25
    d.rounded_rectangle((X0, Y, X0 + (split - X0) * e, Y + 140), 16, fill=(40, 140, 80))
    if lt > 0.9:
        e2 = eio((lt - 0.9) / 0.9); d.rounded_rectangle((split, Y, split + (X1 - split) * e2, Y + 140), 16, fill=RED)
        tc(d, Y + 170, "BORROWED", F("sans_black", 48), RED, x=(split + X1) / 2)
    tc(d, Y + 170, "YOURS", F("sans_black", 48), (40, 140, 80), x=(X0 + split) / 2)
    merchant(d, 540, 1260, 0.75, T, "happy", coat=(40, 40, 60), arm=(660, 1000))
    return img


def peak(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "DOW JONES", F("sans_black", 76), CREAM); tc(d, 300, "approximate", F("sans_med", 34), (150, 156, 170))
    p = (1929.67 - X_A) / (X_B - X_A) * eio(lt / (dur * 0.8))
    v, (x, y) = line_chart(d, dow_pts(), 190, 980, 1180, 520, 420, p, GREEN_UP, xlabels=XLAB, ylabels=YLAB)
    tc(d, 390, f"{v:,.0f}", F("sans_black", 90), GREEN_UP)
    if lt > dur * 0.8: e = back((lt - dur * 0.8) / 0.3); pill(d, 1250 + 20 * (1 - e), "RECORD HIGH · SEPTEMBER 3", INK, GOLD, 40)
    return img


def thursday(lt, dur, T):
    img = deco_bg(); d = ImageDraw.Draw(img, "RGBA")
    calendar(d, 540, 470, 1.0, "OCT", 24, 1929)
    tc(d, 680, "BLACK THURSDAY", F("sans_black", 84), RED, 6, (10, 10, 10))
    ticker(d, 260, 980, 1.2, T, 10 + 40 * clamp(lt / dur))
    tc(d, 1250, "the ticker tape couldn't keep up", F("serif_bold", 46), CREAM)
    return img


def tuesday(lt, dur, T):
    img = deco_bg(); d = ImageDraw.Draw(img, "RGBA")
    calendar(d, 540, 470, 1.0, "OCT", 29, 1929)
    tc(d, 680, "BLACK TUESDAY", F("sans_black", 90), RED, 6, (10, 10, 10))
    n = 16410030 * eio((lt - 0.3) / (dur * 0.7)); tc(d, 860, f"{n:,.0f}", F("sans_black", 110), CREAM, 6, (10, 10, 10))
    tc(d, 1000, "shares traded in one day", F("serif_bold", 54), DECO)
    if lt > dur * 0.6: e = back((lt - dur * 0.6) / 0.35); pill(d, 1130 + 20 * (1 - e), "A RECORD", INK, GOLD, 50)
    return img


def margin_call(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "MARGIN CALL", F("sans_black", 110), RED)
    tc(d, 360, "lenders want their money back", F("serif_bold", 54), CREAM)
    merchant(d, 400, 1260, 0.9, T, "shock", coat=(40, 40, 60), arm=(600, 820))
    ring = 8 * math.sin(T * 40) if int(T * 3) % 2 == 0 else 0
    d.rounded_rectangle((560 + ring, 760, 760 + ring, 880), 18, fill=(30, 30, 30)); d.ellipse((610 + ring, 720, 710 + ring, 780), fill=(30, 30, 30))
    for k in range(3): d.arc((760 + ring - 20 + k * 30, 740 - k * 20, 840 + ring + k * 30, 900 + k * 20), -50, 50, fill=CREAM, width=6)
    if lt > dur * 0.55: slam(img, stamp_img("WIPED OUT", RED, 90, -4), lt, dur * 0.55, 540, 560)
    return img


def slide(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "DOW JONES", F("sans_black", 76), CREAM); tc(d, 300, "approximate", F("sans_med", 34), (150, 156, 170))
    start = (1929.67 - X_A) / (X_B - X_A); p = start + (1 - start) * eio(lt / (dur * 0.8))
    v, (x, y) = line_chart(d, dow_pts(), 190, 980, 1180, 520, 420, p, RED, xlabels=XLAB, ylabels=YLAB)
    tc(d, 390, f"{v:,.0f}", F("sans_black", 90), RED)
    if lt > dur * 0.8: e = back((lt - dur * 0.8) / 0.3); pill(d, 1250 + 20 * (1 - e), "-89% FROM THE PEAK", CREAM, (150, 20, 34), 48)
    return img


def recovery(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "BACK TO THE OLD HIGH IN", F("sans_black", 64), INK)
    yr = int(1929 + 25 * eio(lt / (dur * 0.8))); tc(d, 330, str(yr), F("sans_black", 220), RED)
    n = yr - 1929
    for i in range(n):
        row = i // 9; in_row = min(9, n - row * 9); x = (W - in_row * 92 + 16) / 2 + (i % 9) * 92; y = 640 + row * 110
        d.rounded_rectangle((x, y, x + 76, y + 86), 10, fill=(255, 255, 255), outline=INK, width=3); d.rectangle((x, y, x + 76, y + 22), fill=RED)
        lab = f"'{(1930 + i) % 100:02d}"; d.text((x + 38 - d.textlength(lab, font=F("sans_black", 30)) / 2, y + 34), lab, font=F("sans_black", 30), fill=INK)
    if lt > dur * 0.8: e = back((lt - dur * 0.8) / 0.3); pill(d, 1020 + 20 * (1 - e), "25 YEARS", CREAM, (150, 20, 34), 60)
    return img


def lesson(lt, dur, T):
    img = deco_bg(); d = ImageDraw.Draw(img, "RGBA")
    e = back(lt / 0.4)
    tc(d, 230 + 20 * (1 - e), "BORROWING", F("sans_black", 120), CREAM); tc(d, 370, "TO BUY AT THE TOP", F("sans_black", 76), DECO)
    tc(d, 480, "turns a crash into", F("serif_bold", 56), CREAM); tc(d, 560, "A CATASTROPHE", F("sans_black", 96), RED)
    merchant(d, 540, 1250, 0.8, T, "sad", coat=(40, 40, 60))
    if lt > dur * 0.55: e2 = back((lt - dur * 0.55) / 0.4); pill(d, 720 + 20 * (1 - e2), "FOLLOW FOR MORE MONEY HISTORY", INK, GOLD, 44)
    return img


theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
S = lambda say, draw, **kw: dict(say=say, draw=draw, **kw)
spec = dict(theme=theme, voice=26, speed=1.08, one_take=True, bpm=112, music_amp=0.06, gap=0.16,
    chords=[[110, 138.6, 164.8], [123.5, 146.8, 185], [98, 123.5, 146.8], [110, 130.8, 164.8]],
    scenes=[
        S("Did you know that in just two days in October nineteen twenty nine, the American stock market lost almost a quarter of its value? And that was only the beginning.", hook_map, sfx=[(0.6, "boom")], shake=[(0.62, 0.4, 18)]),
        S("To understand how it happened, we need to go back to the roaring twenties. The economy was booming, and stock prices had been climbing for years.", roaring, tr="zoom", sfx=[(0.4 + 0.35 * i, "coin") for i in range(5)]),
        S("Ordinary people wanted in, and many didn't even use their own money. They bought on margin, putting down a small deposit, and borrowing the rest.", margin, tr="whip", sfx=[(1.6, "riser")]),
        S("On September third, nineteen twenty nine, the Dow hit a record high of three hundred and eighty one.", peak, tr="whip", sfx=[("END-0.9", "ding")]),
        S("Even the experts were convinced. In mid October, the famous economist Irving Fisher said stocks had reached what looks like a permanently high plateau.", fisher, tr="whip"),
        S("Nine days later, the panic began. On Black Thursday, October twenty fourth, prices fell so fast that the ticker tape fell far behind.", thursday, tr="whip", sfx=[(0.6 + 0.2 * i, "tick") for i in range(16)]),
        S("That afternoon, top bankers pooled their money and bought shares to calm the market. It worked, but only for a few days.", bankers, tr="whip", sfx=[(0.6, "coin"), (1.0, "coin"), ("END-2.4", "thud")]),
        S("On Monday, the Dow fell almost thirteen percent. On Tuesday, it fell another twelve. A record sixteen million shares changed hands on Black Tuesday alone.", two_days, tr="flash", sfx=[(0.3, "boom"), (2.6, "boom")], shake=[(0.32, 0.3, 14), (2.62, 0.3, 14)]),
        S("So why did it fall so fast? Prices had raced far ahead of real company profits. When they started falling, lenders demanded their margin loans back. Investors were forced to sell, which pushed prices even lower, and triggered even more margin calls.", spiral, tr="whip", sfx=[(0.3 + 0.5 * i, "tick") for i in range(3)]),
        S("And the fall kept going. By July nineteen thirty two, the Dow was down almost ninety percent from its peak.", slide, tr="whip", sfx=[("END-1.0", "thud")]),
        S("A thousand dollars invested at the top was now worth around one hundred and eight dollars.", thousand, tr="whip", sfx=[(0.5 + 0.25 * i, "tick") for i in range(9)]),
        S("Thousands of banks failed, and America sank into the Great Depression.", banks, tr="zoom", sfx=[(0.3 + 0.25 * i, "pop") for i in range(9)]),
        S("It took twenty five years, until nineteen fifty four, for the Dow to get back to its old high.", recovery, tr="whip", sfx=[(0.3 + 0.1 * i, "tick") for i in range(25)]),
        S("The lesson? Borrowing to buy at the top can turn a crash into a catastrophe. Follow for more money history.", lesson, tr="zoom"),
    ])

if __name__ == "__main__":
    render(spec, sys.argv[1])
