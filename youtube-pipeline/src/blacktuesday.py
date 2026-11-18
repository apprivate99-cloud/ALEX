"""Black Tuesday, 1929: the 'permanently high plateau', margin debt, and a 25-year recovery."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit2 import *

# Dow Jones Industrial Average, approximate (x = year)
DOW = [(1928.0, 200), (1928.5, 210), (1929.0, 300), (1929.67, 381), (1929.82, 230), (1929.87, 199), (1930.29, 294), (1930.95, 165), (1931.95, 78), (1932.52, 41)]
X_A, X_B = 1928.0, 1932.6
def dow_pts(): return [((x - X_A) / (X_B - X_A), v) for x, v in DOW]
XLAB = [(0.0, "1928"), ((1929 - X_A) / (X_B - X_A), "1929"), ((1930 - X_A) / (X_B - X_A), "1930"), ((1931 - X_A) / (X_B - X_A), "1931"), ((1932 - X_A) / (X_B - X_A), "1932")]
YLAB = [(100, "100"), (200, "200"), (300, "300"), (400, "400")]
FISHER_COAT = (60, 60, 70)


def hook(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "OCTOBER 15, 1929", F("sans_black", 76), INK)
    d.rounded_rectangle((90, 340, 990, 800), 20, fill=(250, 244, 226), outline=INK, width=5)
    tc(d, 330, "“", F("serif_bold", 160), RED)
    for i, ln in enumerate(["Stock prices have reached", "what looks like a", "permanently high", "plateau."]):
        e = eio((lt - 0.3 - i * 0.3) / 0.4); tc(d, 470 + i * 72, ln, F("serif_bold" if i >= 2 else "serif", 56), INK + (int(255 * e),))
    tc(d, 760, "— Irving Fisher, economist", F("serif", 34), (110, 80, 50))
    merchant(d, 540, 1300, 0.85, T, "smug", coat=FISHER_COAT, hat=False, beard=False)
    hx, hy = 540, 1300 - 410 * 0.85 + math.sin(T * 5 + 540) * 4 * 0.85
    d.ellipse((hx - 46, hy - 26, hx - 4, hy + 8), outline=INK, width=5); d.ellipse((hx + 4, hy - 26, hx + 46, hy + 8), outline=INK, width=5)
    return img


def two_weeks(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA")
    flip = lt > 0.5
    calendar(d, 540, 600, 1.4, "OCT", 29 if flip else 15, 1929, RED if flip else (40, 120, 70))
    if flip: tc(d, 300, "TWO WEEKS LATER", F("sans_black", 70), CREAM)
    slam(img, stamp_img("CRASH", RED, 130, -6), lt, 0.9, 540, 1080)
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
        x = 130 + (i % 9) * 92; y = 640 + (i // 9) * 110
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
spec = dict(theme=theme, voice=26, speed=1.32, bpm=112, music_amp=0.06, gap=0.12,
    chords=[[110, 138.6, 164.8], [123.5, 146.8, 185], [98, 123.5, 146.8], [110, 130.8, 164.8]],
    scenes=[
        S("On October fifteenth, nineteen twenty nine, a famous economist said stock prices had reached what looks like a permanently high plateau.", hook),
        S("Two weeks later, the stock market crashed.", two_weeks, tr="flash", sfx=[(0.5, "pop"), (0.9, "boom")], shake=[(0.92, 0.4, 20)], drop=[(0.85, 2.0)]),
        S("In the roaring twenties, stock prices soared, and ordinary people rushed to get rich.", roaring, tr="zoom", sfx=[(0.4 + 0.35 * i, "coin") for i in range(5)]),
        S("Many bought on margin, paying a small part of the price, and borrowing the rest.", margin, tr="whip", sfx=[(0.9, "riser")]),
        S("On September third, nineteen twenty nine, the Dow hit a record of three hundred and eighty one.", peak, tr="whip", sfx=[("END-0.9", "ding")]),
        S("Then, in late October, the selling began. On Black Thursday, prices plunged so fast that the ticker tape couldn't keep up.", thursday, tr="whip", sfx=[(0.6 + 0.2 * i, "tick") for i in range(16)]),
        S("Then came Black Tuesday, October twenty ninth. A record sixteen million shares were traded in a single day.", tuesday, tr="flash", sfx=[(0.3, "boom")], shake=[(0.32, 0.4, 18)]),
        S("People who had bought with borrowed money were wiped out, as their lenders demanded to be repaid.", margin_call, tr="whip", sfx=[("END-1.6", "stamp")]),
        S("And the fall kept going. By July nineteen thirty two, the Dow was down to just forty one, almost ninety percent below its peak.", slide, tr="whip", sfx=[("END-1.0", "thud")]),
        S("It took twenty five years, until nineteen fifty four, for the Dow to get back to its old high.", recovery, tr="whip", sfx=[(0.3 + 0.1 * i, "tick") for i in range(25)]),
        S("The lesson? Borrowing to buy at the top can turn a crash into a catastrophe. Follow for more money history.", lesson, tr="zoom"),
    ])

if __name__ == "__main__":
    render(spec, sys.argv[1])
