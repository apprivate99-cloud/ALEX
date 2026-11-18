"""Where did money come from? Barter myth -> clay-tablet credit -> Lydian coins -> Song paper money -> digital."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit2 import *


def hook(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 14))
    e = back(lt / 0.4)
    tc(d, 230 - 30 * (1 - e), "WHERE DID", F("sans_black", 110), CREAM + (int(255 * clamp(e)),))
    tc(d, 360 - 30 * (1 - e), "MONEY", F("sans_black", 170), GOLD + (int(255 * clamp(e)),))
    tc(d, 540 - 30 * (1 - e), "COME FROM?", F("sans_black", 110), CREAM + (int(255 * clamp(e)),))
    bob = lambda k: 14 * math.sin(T * 2 + k)
    coin(d, 230, 860 + bob(0), 2.2); lion_coin(d, 830, 880 + bob(1), 90)
    sack(d, 300, 1260 + bob(2), 0.8); tablet(img, 790, 1140 + bob(3), 0.42, [], T)
    d = ImageDraw.Draw(img, "RGBA"); tc(d, 940, "?", F("serif_bold", 260), CREAM, 8, (40, 10, 14), x=540)
    return img


def barter(lt, dur, T, phase):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "THE TEXTBOOK STORY", CREAM, (40, 40, 40), 44)
    tc(d, 340, "barter: swap what you have", F("serif_bold", 54), INK)
    merchant(d, 150, 1230, 0.7, T, "happy", coat=(90, 60, 40), cap=True, beard=False)
    cow(d, 360, 1230, 0.95, T)
    merchant(d, 930, 1230, 0.7, T + 1, "happy", coat=(60, 80, 120), cap=True)
    sack(d, 740, 1230, 0.9)
    u = (T * 0.7) % 1
    for y, sgn in ((660, 1), (760, -1)):  # swap arrows
        x0, x1 = (330, 750) if sgn > 0 else (750, 330)
        d.line([(x0, y), (x1, y)], fill=RED, width=10)
        d.polygon([(x1, y), (x1 - sgn * 40, y - 24), (x1 - sgn * 40, y + 24)], fill=RED)
    if phase == 1:
        slam(img, stamp_img("MYTH?", RED, 110, -6), lt, 0.4, 540, 510)
    return img


def mesopotamia(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, 42 - 2 * k, 35, 38 + 20 * k, T, hl=("IRQ",))
    x, y = pr(44.4, 33.3); d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=RED, outline=CREAM, width=4)
    pill(d, 230, "MESOPOTAMIA · ~3500 BC", INK, GOLD, 46)
    tc(d, y + 40, "modern-day Iraq", F("sans_black", 44), CREAM, 6, (10, 20, 30), x=x)
    return img


def tablet_scene(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "THE FIRST MONEY WAS DEBT", CREAM, (150, 20, 34), 44)
    e = back(lt / 0.5)
    tablet(img, 540, 800 + 60 * (1 - e), 1.15, ["Owed to the temple:", "3 sacks of barley"], T)
    return img


def shekel(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 230, "MEASURED IN", F("sans_black", 70), INK)
    px, py, L = 540, 620, 300; a = math.radians(6 * math.sin(T * 1.5))
    d.rectangle((px - 14, py, px + 14, 1150), fill=(150, 110, 50)); d.polygon([(px - 120, 1200), (px + 120, 1200), (px + 30, 1140), (px - 30, 1140)], fill=(110, 80, 40))
    lx, ly, rx, ry = px - L * math.cos(a), py - L * math.sin(a), px + L * math.cos(a), py + L * math.sin(a)
    d.line([(lx, ly), (rx, ry)], fill=GOLD, width=20); d.ellipse((px - 24, py - 24, px + 24, py + 24), fill=GOLD)
    for ex, ey, what in ((lx, ly, "barley"), (rx, ry, "silver")):
        pan = ey + 240
        d.line([(ex, ey), (ex - 100, pan)], fill=(230, 190, 110), width=4); d.line([(ex, ey), (ex + 100, pan)], fill=(230, 190, 110), width=4)
        if what == "barley":
            for k2 in range(16): d.ellipse((ex - 70 + (k2 % 8) * 18, pan - 40 - (k2 // 8) * 20, ex - 56 + (k2 % 8) * 18, pan - 22 - (k2 // 8) * 20), fill=(220, 180, 90))
        else:
            for k2 in range(3): d.rounded_rectangle((ex - 60 + k2 * 40, pan - 50, ex - 26 + k2 * 40, pan - 4), 6, fill=(200, 204, 214), outline=(120, 126, 140), width=3)
        d.chord((ex - 120, pan - 36, ex + 120, pan + 44), 0, 180, fill=GOLD)
        tc(d, pan + 60, what.upper(), F("sans_black", 54), INK, x=ex)
    if lt > dur * 0.5:
        e = back((lt - dur * 0.5) / 0.4); pill(d, 330 + 30 * (1 - e), "silver: weighed in SHEKELS", INK, GOLD, 46)
    return img


def lydia(lt, dur, T):
    img = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(img, "RGBA"); k = eio(lt / dur)
    pr = draw_map(img, d, 30 - 2 * k, 39, 40 + 22 * k, T, hl=("TUR",))
    x, y = pr(28.0, 38.5); d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=RED, outline=CREAM, width=4)
    pill(d, 230, "LYDIA · ~630 BC", INK, GOLD, 50)
    tc(d, y + 40, "modern-day Turkey", F("sans_black", 44), CREAM, 6, (10, 20, 30), x=min(max(x, 240), W - 240))
    if lt > dur * 0.45:
        e = back((lt - dur * 0.45) / 0.4); pill(d, 330 + 30 * (1 - e), "THE WORLD'S FIRST COINS", CREAM, (150, 20, 34), 46)
    return img


def electrum(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    e = back(lt / 0.5); lion_coin(d, 540, 780, 300 * clamp(e) + 1)
    tc(d, 230, "ELECTRUM", F("sans_black", 110), ELECTRUM)
    tc(d, 370, "natural gold + silver", F("serif_bold", 58), CREAM)
    if lt > dur * 0.5: e2 = back((lt - dur * 0.5) / 0.4); pill(d, 1150 + 30 * (1 - e2), "STAMPED WITH A LION", INK, GOLD, 46)
    return img


def iron(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "CHINA · ~1,000 YEARS AGO", INK, GOLD, 44)
    tc(d, 340, "heavy strings of iron coins", F("serif_bold", 56), CREAM)
    merchant(d, 300, 1240, 0.85, T, "shock", coat=(120, 40, 40), cap=True, arm=(420, 880))
    iron_string(d, 420, 880, 8, 34, sag=110 + 10 * math.sin(T * 3))
    if lt > dur * 0.55:
        e = back((lt - dur * 0.55) / 0.4)
        d.rounded_rectangle((640, 520, 960, 700), 12, fill=(240, 230, 200, int(255 * clamp(e))), outline=(110, 80, 50), width=5)
        tc(d, 550, "RECEIPT", F("serif_bold", 50), INK + (int(255 * clamp(e)),), x=800); tc(d, 620, "= 1,000 coins", F("serif", 40), INK + (int(255 * clamp(e)),), x=800)
    return img


def paper(lt, dur, T):
    img = bg("burgundy").copy(); d = ImageDraw.Draw(img, "RGBA"); rays(d, T, (255, 200, 120, 12))
    pill(d, 230, "1024 · SONG DYNASTY", INK, GOLD, 48)
    tc(d, 330, "the first official paper money", F("serif_bold", 54), CREAM)
    e = back(lt / 0.5); jiaozi(img, 540, 860 + 80 * (1 - e), 1.3, T)
    return img


def collapse(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 230, "TOO MUCH PRINTING", F("sans_black", 76), INK)
    n = int(8 + 22 * eio(lt / dur))
    for i in range(n): jiaozi(img, 240 + (i % 6) * 120, 1060 - (i // 6) * 90 - (i % 2) * 10, 0.36, i)
    d = ImageDraw.Draw(img, "RGBA")
    v = 100 * (1 - eio(lt / dur) * 0.97)
    d.rounded_rectangle((140, 420, 940, 500), 20, fill=(255, 255, 255), outline=INK, width=4)
    d.rounded_rectangle((146, 426, 146 + 788 * v / 100, 494), 16, fill=RED)
    tc(d, 520, f"value of a note: {v:.0f}%", F("sans_black", 54), RED)
    return img


def digital(lt, dur, T):
    img = radial((236, 240, 246), (190, 198, 214)); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 230, "MONEY TODAY", F("sans_black", 90), INK)
    tc(d, 350, "mostly just numbers in computers", F("serif_bold", 50), (60, 70, 90))
    v = 12483.20 * eio(lt / dur); phone(d, 540, 860, 1.35, f"£{v:,.2f}")
    return img


def circle(lt, dur, T):
    img = bg("dark").copy(); d = ImageDraw.Draw(img, "RGBA")
    tc(d, 220, "FULL CIRCLE", F("sans_black", 110), GOLD)
    tablet(img, 290, 760, 0.72, ["who owes", "what"], T); d = ImageDraw.Draw(img, "RGBA")
    phone(d, 790, 760, 0.95, "£12,483.20")
    tc(d, 1070, "3500 BC", F("sans_black", 52), CREAM, x=290); tc(d, 1070, "TODAY", F("sans_black", 52), CREAM, x=790)
    tc(d, 680, "=", F("sans_black", 140), CREAM, x=540)
    if lt > dur * 0.55: e = back((lt - dur * 0.55) / 0.4); pill(d, 1190 + 30 * (1 - e), "FOLLOW FOR MORE MONEY HISTORY", INK, GOLD, 46)
    return img


theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
S = lambda say, draw, **kw: dict(say=say, draw=draw, **kw)
spec = dict(theme=theme, voice=26, speed=1.32, bpm=100, music_amp=0.06, gap=0.12,
    chords=[[130.8, 164.8, 196], [110, 130.8, 164.8], [146.8, 174.6, 220], [98, 123.5, 146.8]],
    scenes=[
        S("The story you were taught about where money came from is probably wrong.", hook, sfx=[(0.3, "pop")]),
        S("Most textbooks say people used to barter, swapping a cow for sacks of grain, until money made trading easier.", lambda l, d_, T: barter(l, d_, T, 0), tr="zoom"),
        S("But anthropologists have found almost no evidence of societies that actually ran on barter.", lambda l, d_, T: barter(l, d_, T, 1), tr=None, sfx=[(0.42, "stamp")], shake=[(0.44, 0.25, 14)]),
        S("Instead, the earliest records point to credit. Over five thousand years ago, in Mesopotamia,", mesopotamia, tr="whip"),
        S("temples recorded who owed what, on clay tablets.", tablet_scene, tr="whip", sfx=[(0.4, "thud")]),
        S("Debts were counted in barley, and in silver, weighed out in units called shekels.", shekel, tr="whip", sfx=[("END-2.0", "coin")]),
        S("Then, about two thousand six hundred years ago, the kingdom of Lydia, in what's now Turkey, made the world's first coins.", lydia, tr="zoom", sfx=[("END-2.4", "ding")]),
        S("They were lumps of electrum, a natural mix of gold and silver, stamped with a lion's head.", electrum, tr="whip", sfx=[(0.3, "coin")]),
        S("Around a thousand years ago in China, merchants were sick of hauling heavy strings of iron coins, so they started swapping paper receipts instead.", iron, tr="whip", sfx=[("END-2.6", "pop")]),
        S("In ten twenty four, the government took over, and issued the world's first official paper money.", paper, tr="zoom", sfx=[(0.3, "riser")]),
        S("But it printed too much, and over time, the notes lost almost all their value.", collapse, tr="whip", sfx=[("END-1.0", "thud")]),
        S("Today, most money isn't coins or paper at all. It's just numbers, recorded in bank computers.", digital, tr="whip"),
        S("So after five thousand years, money has come full circle, back to a record of who owes what. Follow for more money history.", circle, tr="zoom"),
    ])

if __name__ == "__main__":
    render(spec, sys.argv[1])
