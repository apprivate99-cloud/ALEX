"""John Law: convicted murderer, France's money man, and the Mississippi Bubble."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit2 import *
import kit
kit.ERA = "1700s"
kit.COIN_SYM = ""

LAW_COAT, WIG_B, WIG_BD = (40, 50, 90), (120, 84, 50), (90, 60, 34)


def law(d, x, y, s, t, mood="smug", arm=None):
    """John Law: dark blue coat, long brown wig."""
    b = math.sin(t * 5 + x) * 4 * s; hy = y + b - 410 * s
    for side in (-1, 1):
        for k in range(4):
            cx = x + side * (60 + 6 * k) * s; cy = hy - 10 * s + k * 44 * s
            d.ellipse((cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s), fill=WIG_B, outline=WIG_BD, width=max(int(3 * s), 1))
    merchant(d, x, y, s, t, mood, coat=LAW_COAT, hat=False, beard=False, arm=arm)
    for k in range(5):
        cx = x + (-52 + k * 26) * s; d.ellipse((cx - 26 * s, hy - 92 * s, cx + 26 * s, hy - 40 * s), fill=WIG_B, outline=WIG_BD, width=max(int(3 * s), 1))


def hook(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 14))
    tc(d, 220, "JOHN LAW", F("serif_bold", 120), GOLD); tc(d, 360, "1671 – 1729", F("serif", 52), CREAM)
    law(d, 540, 1290, 1.05, T, "smug")
    slam(img, stamp_img("CONVICTED MURDERER", RED, 60, -4), lt, 0.6, 540, 505)
    if lt > dur * 0.55:
        d = ImageDraw.Draw(img, "RGBA"); e = back((lt - dur * 0.55) / 0.4); pill(d, 615 + 15 * (1 - e), "RAN FRANCE'S ECONOMY", INK, GOLD, 40)
    return img


def duel(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "1694 · LONDON", CREAM, (0, 0, 0, 170), 46)
    hit = dur * 0.45
    law(d, 300, 1220, 0.85, T, "shock" if lt > hit else "smug", arm=(470, 840))
    if lt < hit:
        merchant(d, 800, 1220, 0.85, T + 1, "smug", coat=(120, 30, 40), arm=(640, 840)); swords(d, 470, 640, 840, T, lt > hit * 0.6)
    else:
        u = eio((lt - hit) / 0.6)  # opponent falls
        fig = Image.new("RGBA", (900, 900), (0, 0, 0, 0)); fd = ImageDraw.Draw(fig, "RGBA")
        merchant(fd, 450, 760, 0.85, T + 1, "shock", coat=(120, 30, 40))
        fig = fig.rotate(-80 * u, resample=Image.BICUBIC, center=(450, 760))  # pivot on the feet, no cropping
        img.paste(fig, (int(640 - 450 - 60 * u), int(1220 - 760)), fig); d = ImageDraw.Draw(img, "RGBA")
        d.line([(300 + 170, 840), (600, 860)], fill=(210, 214, 222), width=8)
        if lt > hit + 0.4: e = back((lt - hit - 0.4) / 0.35); pill(d, 400 + 20 * (1 - e), "SENTENCED TO DEATH", CREAM, (150, 20, 34), 48)
    return img


def prison(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "PRISON, LONDON", CREAM, (0, 0, 0, 170), 46)
    k = eio((lt - 0.3) / 0.8)
    law(d, 540 + 380 * eio((lt - 1.3) / 1.0), 1110, 0.8, T, "smug")
    bars(d, 200, 360, 880, 1160, k)
    if lt > 1.4: slam(img, stamp_img("ESCAPED", RED, 90, -5), lt, 1.4, 540, 1270)
    return img


def gambler(lt, dur, T):
    img = bg("tavern").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "A PROFESSIONAL GAMBLER", CREAM, (0, 0, 0, 170), 46)
    tc(d, 330, "who studied money and banking", F("serif_bold", 50), CREAM, 5, INK)
    law(d, 540, 1080, 0.85, T, "smug")
    d.rounded_rectangle((120, 1000, 960, 1180), 30, fill=(30, 100, 60), outline=(90, 60, 40), width=14)
    for i, (sym, col) in enumerate([("A", RED), ("K", INK), ("Q", RED), ("J", INK)]):
        x = 260 + i * 120 + 6 * math.sin(T * 2 + i); y = 1040
        d.rounded_rectangle((x - 44, y, x + 44, y + 120), 10, fill=(250, 250, 246), outline=(180, 180, 180), width=3)
        d.text((x - 16, y + 30), sym, font=F("serif_bold", 52), fill=col)
    for i in range(6): coin(d, 820 + (i % 3) * 30, 1110 - (i // 3) * 26, 1.2)
    return img


def france(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, 2.5, 46.5, 60 + 20 * k, T, hl=("FRA",))
    fx, fy = pr(2.6, 46.9)
    map_face(d, fx, fy, 2.4, "sad" if lt > 0.5 else "worried", T)
    coin_drain(d, fx, fy + 140, T, n=12, spread=120, fall=330)
    meter(d, 540, 1090, 640, eio(lt / dur), "DEBT")
    pill(d, 230, "FRANCE · 1715", INK, GOLD, 48)
    if lt > dur * 0.4:
        e = back((lt - dur * 0.4) / 0.4); d.rectangle((0, 1240, W, 1340), fill=(120, 16, 28, 235))
        tc(d, 1256, "DROWNING IN WAR DEBT", F("sans_black", 56), CREAM + (int(255 * clamp(e)),))
    return img


def idea(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "LAW'S BIG IDEA", F("sans_black", 90), INK)
    for i in range(5): coin(d, 200 + (i % 3) * 60, 900 - (i // 3) * 50, 1.6)
    tc(d, 1010, "gold & silver", F("serif_bold", 50), INK, x=260)
    tc(d, 820, "→", F("sans_black", 140), RED, x=540)
    e = back((lt - 0.6) / 0.4)
    if lt > 0.6:
        d.rounded_rectangle((680, 780, 980, 940), 12, fill=(236, 226, 196), outline=(90, 70, 40), width=6)
        tc(d, 800, "BANK NOTE", F("serif_bold", 40), INK, x=830); tc(d, 860, "100 livres", F("serif", 36), INK, x=830)
        tc(d, 1010, "paper money", F("serif_bold", 50), INK, x=830)
    return img


def louisiana(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, -45, 38, 9.5, T, hl=("FRA",), cy=780, bbox=(-110, 20, 10, 60))
    px, py = pr(2.35, 48.86); nx, ny = pr(-90.07, 29.95)
    p = eio((lt - 0.3) / (dur * 0.6)); cx, cy = (px + nx) / 2, min(py, ny) - 160
    pts = [((1 - u) ** 2 * px + 2 * u * (1 - u) * cx + u * u * nx, (1 - u) ** 2 * py + 2 * u * (1 - u) * cy + u * u * ny) for u in np.linspace(0, max(p, 0.01), 40)]
    for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=CREAM, width=8)
    ship(d, pts[-1][0], pts[-1][1], 1.1)
    if p > 0.95: coin_flow(d, (nx, ny), (px, py), T, n=7, arc=-200)
    fx, fy = pr(2.6, 46.6); map_face(d, fx, fy + 6, 0.55, "happy", T)
    for (x, y), lab in [((px, py), "PARIS"), ((nx, ny), "LOUISIANA")]:
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=RED, outline=CREAM, width=4); tc(d, y + 26, lab, F("sans_black", 44), CREAM, 6, (10, 20, 30), x=min(max(x, 200), W - 200))
    pill(d, 230, "THE MISSISSIPPI COMPANY", INK, GOLD, 48)
    if lt < dur * 0.4: d.rectangle((0, 1240, W, 1340), fill=(10, 20, 30, 230)); tc(d, 1256, "1716: FRANCE GIVES LAW A BANK", F("sans_black", 50), GOLD)
    return img


def frenzy(lt, dur, T):
    img = bg("curtain").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "PARIS GOES WILD", CREAM, (0, 0, 0, 170), 48)
    tc(d, 340, "“a land of untold riches”", F("serif_bold", 54), GOLD, 5, INK)
    for i, (x, c) in enumerate([(160, (30, 26, 30)), (380, (60, 30, 40)), (600, (40, 60, 50)), (820, (70, 50, 30))]):
        merchant(d, x, 1230 - 20 * abs(math.sin(T * 6 + i)), 0.7, T + i, "happy", coat=c, arm=(x + 70, 820 - 30 * abs(math.sin(T * 6 + i))))
        d.rounded_rectangle((x + 40, 740 - 30 * abs(math.sin(T * 6 + i)), x + 120, 800 - 30 * abs(math.sin(T * 6 + i))), 6, fill=(236, 226, 196), outline=(90, 70, 40), width=3)
    return img


PTS = [(0, 500), (0.35, 600), (0.55, 2500), (0.75, 6000), (0.95, 10000), (1.0, 10000)]
def chart_up(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "MISSISSIPPI SHARES", F("sans_black", 70), CREAM); tc(d, 300, "livres per share, 1719 · approximate", F("sans_med", 34), (150, 156, 170))
    v, _ = line_chart(d, PTS, 170, 980, 1180, 520, 11000, eio(lt / (dur * 0.85)), GREEN_UP,
                      xlabels=[(0.02, "JAN"), (0.35, "MAY"), (0.62, "AUG"), (0.95, "DEC")], ylabels=[(2500, "2.5K"), (5000, "5K"), (7500, "7.5K"), (10000, "10K")])
    tc(d, 390, f"{v:,.0f} livres", F("sans_black", 80), GREEN_UP)
    return img


def millionaire(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "A NEW WORD", F("sans_black", 90), INK)
    e = clamp(lt / 1.2); word = "millionaire"[: max(1, int(11 * e))]
    d.rounded_rectangle((110, 400, 970, 1000), 20, fill=(250, 244, 226), outline=INK, width=5)
    tc(d, 470, word, F("serif_bold", 120), INK)
    for i, (ln, f, c) in enumerate([("(noun)", F("serif", 46), (110, 80, 50)), ("someone whose wealth", F("serif", 56), INK), ("runs into the millions", F("serif", 56), INK)]):
        tc(d, 660 + i * 84, ln, f, c)
    if lt > dur * 0.55: e2 = back((lt - dur * 0.55) / 0.4); pill(d, 1090 + 20 * (1 - e2), "POPULARISED IN 1720", CREAM, (150, 20, 34), 44)
    return img


def controller(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 16))
    tc(d, 220, "JANUARY 1720", F("serif_bold", 100), GOLD)
    law(d, 540, 1250, 1.1, T, "smug")
    e = back((lt - 0.4) / 0.4)
    if lt > 0.4: pill(d, 380 + 20 * (1 - e), "CONTROLLER GENERAL OF FINANCES", INK, GOLD, 40); tc(d, 480, "in charge of France's economy", F("serif_bold", 50), CREAM)
    return img


PTS2 = PTS[:-1] + [(1.0, 10000), (1.25, 9000), (1.55, 5000), (1.85, 2500), (2.0, 2000)]
def chart_down(lt, dur, T):
    img = bg("chart").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "MISSISSIPPI SHARES", F("sans_black", 70), CREAM); tc(d, 300, "livres per share, 1719–1720 · illustrative", F("sans_med", 34), (150, 156, 170))
    pts = [(x / 2, v) for x, v in PTS2]
    p = 0.5 + 0.5 * eio((lt - 0.8) / (dur * 0.6))
    v, _ = line_chart(d, pts, 170, 980, 1180, 520, 11000, p, RED if p > 0.55 else GREEN_UP,
                      xlabels=[(0.02, "JAN 1719"), (0.5, "JAN 1720"), (0.97, "DEC")], ylabels=[(2500, "2.5K"), (5000, "5K"), (7500, "7.5K"), (10000, "10K")])
    tc(d, 390, f"{v:,.0f} livres", F("sans_black", 80), RED if p > 0.55 else GREEN_UP)
    return img


def riots(lt, dur, T):
    img = bg("curtain").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "PARIS · 1720", CREAM, (0, 0, 0, 170), 48)
    for i, (x, c) in enumerate([(160, (30, 26, 30)), (380, (60, 30, 40)), (600, (40, 60, 50)), (820, (70, 50, 30))]):
        merchant(d, x + 6 * math.sin(T * 20 + i), 1230, 0.7, T + i, "shock", coat=c, arm=(x + 80, 760 + 40 * math.sin(T * 9 + i)))
    if lt > dur * 0.5: e = back((lt - dur * 0.5) / 0.4); pill(d, 400 + 20 * (1 - e), "LAW FLEES FRANCE", CREAM, (150, 20, 34), 54)
    return img


def venice(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "VENICE · 1729", CREAM, (0, 0, 0, 170), 48)
    for i in range(6): d.rectangle((60 + i * 170, 1130, 160 + i * 170, 1160), fill=(40, 70, 90))
    law(d, 540, 1130, 1.0, T, "sad")
    tc(d, 380, "died nearly broke", F("serif_bold", 70), CREAM)
    return img


def twist(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 14))
    tc(d, 220, "THE TWIST", F("sans_black", 110), GOLD)
    card(d, (190, 420, 890, 840), [("PAPER MONEY", "serif_bold", 74, INK), ("backed by", "serif", 52, INK), ("TRUST", "sans_black", 96, RED)], fill=(236, 226, 196), outline=(90, 70, 40))
    d.rounded_rectangle((214, 444, 866, 816), 12, outline=(90, 70, 40), width=3)
    tc(d, 900, "is how money works today", F("serif_bold", 56), CREAM)
    if lt > dur * 0.6: e = back((lt - dur * 0.6) / 0.4); pill(d, 1060 + 20 * (1 - e), "FOLLOW FOR MORE MONEY HISTORY", INK, GOLD, 46)
    return img


theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
S = lambda say, draw, **kw: dict(say=say, draw=draw, **kw)
spec = dict(theme=theme, voice=26, speed=1.12, bpm=104, music_amp=0.06, gap=0.16,
    chords=[[110, 130.8, 164.8], [87.3, 110, 130.8], [98, 123.5, 146.8], [82.4, 103.8, 123.5]],
    scenes=[
        S("Did you know that France once handed its entire economy to a Scottish gambler, who'd been sentenced to death for murder?", hook, sfx=[(0.6, "stamp")], shake=[(0.62, 0.25, 14)]),
        S("His name was John Law. In sixteen ninety four, he killed a man in a duel in London, and the court sentenced him to death.", duel, tr="zoom", sfx=[(1.0, "tick"), (1.4, "tick"), ("END-3.2", "thud")]),
        S("Somehow, he escaped from prison, and slipped away to mainland Europe.", prison, tr="whip", sfx=[(0.5, "thud"), (1.4, "stamp")]),
        S("For years he lived as a gambler, while studying money and banking. Then he found the perfect place to test his ideas.", gambler, tr="whip", sfx=[(0.5, "coin"), (1.2, "coin")]),
        S("After decades of war, France was drowning in debt.", france, tr="zoom"),
        S("And Law had a bold solution: replace gold and silver with paper money.", idea, tr="whip", sfx=[(0.6, "pop")]),
        S("France gave him a bank to try it. Then he took control of a trading company with rights to French Louisiana: the Mississippi Company.", louisiana, tr="whip"),
        S("Law sold Louisiana as a land of untold riches, and Paris went wild for the shares.", frenzy, tr="whip", sfx=[(0.4 + 0.3 * i, "coin") for i in range(6)]),
        S("In a single year, the share price shot up from about five hundred livres to around ten thousand.", chart_up, tr="whip", sfx=[("END-1.2", "ding")]),
        S("So many people got rich so fast that a new word took off: millionaire.", millionaire, tr="whip", sfx=[(0.1 + 0.11 * i, "tick") for i in range(11)]),
        S("By January seventeen twenty, the gambler from Scotland was in charge of France's entire economy.", controller, tr="zoom", sfx=[(0.4, "ding")]),
        S("But there was a catch. The boom was fuelled by printing more and more paper money. And when investors tried to swap their paper for gold, the whole thing came apart.", chart_down, tr="whip", sfx=[("END-2.4", "boom")], shake=[(3.6, 0.4, 18)]),
        S("Prices crashed, angry crowds filled the streets, and by the end of the year, Law had fled France for good.", riots, tr="whip"),
        S("He died nearly broke, in Venice, in seventeen twenty nine.", venice, tr="whip"),
        S("And yet, here's the twist. Law's big idea, paper money backed by trust instead of gold, is exactly how almost all money works today. Follow for more money history.", twist, tr="flash", sfx=[(-0.9, "riser")]),
    ])

if __name__ == "__main__":
    render(spec, sys.argv[1])
