import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit import *

def stamp_img(text, col=RED, size=110, rot=-12):
    f = F("sans_black", size); tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1))); w = tmp.textlength(text, font=f)
    st = Image.new("RGBA", (int(w + 80), size + 90), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle((6, 6, st.width - 6, st.height - 6), 20, outline=col, width=14); sd.text((40, 30), text, font=f, fill=col)
    return st.rotate(rot, expand=True, resample=Image.BICUBIC)
def slam(img, st, lt, t0, cx, cy):
    if lt < t0: return
    e = eio((lt - t0) / 0.18); s = 1 + 0.8 * (1 - e)
    s2 = st.resize((max(1, int(st.width * s)), max(1, int(st.height * s))))
    s2.putalpha(s2.getchannel("A").point(lambda v: int(v * e * 0.95))); img.paste(s2, (int(cx - s2.width / 2), int(cy - s2.height / 2)), s2)

def alkmaar(lt, dur, T):
    img = bg("curtain").copy(); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "THE PEAK · EARLY 1637", CREAM, (0, 0, 0, 170), 40)
    hit = dur - 1.0; gy = 700 - (60 if lt < hit else 0) + 20 * math.sin(T * 6)
    merchant(d, 820, 1060, 0.75, T, "happy" if lt < hit else "shock", look=-1, arm=(950, gy))
    d.line([(950, gy), (970, gy - 40)], fill=(110, 70, 40), width=12); d.rectangle((925, gy - 80, 1015, gy - 40), fill=(110, 70, 40))
    d.rectangle((680, 900, 960, 1180), fill=(90, 56, 34)); d.rectangle((660, 880, 980, 910), fill=(120, 80, 50))
    d.polygon([(330, 0), (100, 1150), (560, 1150)], fill=(255, 230, 170, 30))
    d.rectangle((210, 1000, 450, 1180), fill=(110, 20, 30)); d.rectangle((190, 980, 470, 1010), fill=(150, 30, 40))
    bulb(d, 330, 890 + 6 * math.sin(T * 2), 0.9); tc(d, 1100, "SEMPER AUGUSTUS", fit(d, "SEMPER AUGUSTUS", "serif_bold", 34, 210), GOLD, x=330)
    v = 10000 * eio((lt - 0.4) / (hit - 0.5)); tc(d, 380, f"ƒ{v:,.0f}", F("sans_black", 160), GOLD, 10, INK)
    tc(d, 580, "for ONE bulb", F("serif_bold", 60), CREAM, 6, INK)
    slam(img, stamp_img("REPORTEDLY", GOLD, 80, -4), lt, hit, 540, 1270)
    return img

def today(lt, dur, T):
    img = radial((236, 246, 240), (190, 214, 200)); d = ImageDraw.Draw(img, "RGBA")
    pill(d, 230, "IN TODAY'S MONEY", (255, 255, 255), (20, 120, 70), 46)
    half = dur * 0.42
    e1 = eio((lt - 0.2) / 0.9); tc(d, 360, "ADJUSTED FOR PRICES", F("sans_bold", 44), (60, 80, 70))
    tc(d, 420, f"€{130000 * e1:,.0f}", F("sans_black", 120), (60, 90, 80))
    if lt > half:
        e2 = eio((lt - half) / (dur - half - 0.8)); tc(d, 640, "MEASURED IN WAGES", F("sans_bold", 44), (20, 110, 60))
        tc(d, 700, f"${2000000 * e2:,.0f}+", F("sans_black", 150), (20, 110, 60), 0)
        tc(d, 880, "33 years × ~$60k salary", F("sans_med", 40), (60, 80, 70))
        for side in (-1, 1):
            for j in range(int(14 * e2)):
                x = 540 + side * 290; y = 1330 - j * 26
                d.rounded_rectangle((x - 110, y - 22, x + 110, y + 22), 6, fill=(120, 180, 120), outline=(40, 100, 50), width=3)
                d.text((x - 12, y - 22), "$", font=F("sans_black", 36), fill=(30, 90, 40))
    tulip(d, 540, 1370, 0.85, stripes=1, sway=math.sin(T * 2) * 0.2)
    return img

def unpaid(lt, dur, T):
    img = bg("paper").copy(); d = ImageDraw.Draw(img, "RGBA")
    pg = Image.new("RGBA", (760, 900), (0, 0, 0, 0)); pd = ImageDraw.Draw(pg)
    pd.rectangle((0, 0, 759, 899), fill=(250, 242, 220), outline=INK, width=6)
    for i, (txt, f, c) in enumerate([("BILL OF SALE", F("serif_bold", 70), INK), ("tulip bulbs, 1637", F("serif", 56), INK), ("ƒ10,000", F("sans_black", 130), (30, 110, 50)), ("Payment due: on delivery", F("serif", 40), INK)]):
        w = pd.textlength(txt, font=f); pd.text(((760 - w) / 2, [50, 170, 270, 460][i]), txt, font=f, fill=c)
    pd.line([(120, 590), (640, 590)], fill=INK, width=3); pd.text((120, 600), "signature", font=F("serif", 30), fill=INK)
    pg = pg.rotate(-3, expand=True, resample=Image.BICUBIC); img.paste(pg, ((W - pg.width) // 2, 230), pg)
    slam(img, stamp_img("NEVER PAID?", RED, 72, -5), lt, 0.5, 540, 1000)
    return img

theme = dict(chrome=chrome, cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)
S = lambda say, draw, **kw: dict(say=say, draw=draw, **kw)
spec = dict(theme=theme, voice=26, speed=1.08, one_take=True, bpm=104, music_amp=0.06, gap=0.16,
    chords=[[146.8, 174.6, 220], [116.5, 146.8, 174.6], [130.8, 164.8, 196], [110, 138.6, 164.8]],
    scenes=[
        S("Did you know that in sixteen thirty seven, a single tulip bulb could cost as much as a house?", lambda l, d_, T: scale_scene(l, d_, T, 0), sfx=[(0.78, "thud")], shake=[(0.78, 0.25, 14)]),
        S("Then, almost overnight, nobody would buy one.", lambda l, d_, T: scale_scene(l, d_, T, 1), tr=None, sfx=[(0.1, "boom")], shake=[(0.1, 0.35, 18)], drop=[(0.05, 1.2)]),
        S("To understand why, we need to go back to the Dutch Republic, which was booming, with ships trading all across the world.", map_a, tr="zoom"),
        S("Tulips had arrived from the Ottoman Empire, and rare striped varieties became the ultimate status symbol for the rich.", map_b, tr=None, sfx=[(4.0, "ding")]),
        S("By the winter of sixteen thirty six, merchants and craftsmen were piling in. They traded bulbs that were still in the ground, in taverns, using contracts instead of cash.",
          lambda l, d_, T: tavern(l, d_, T, 0), tr="whip", sfx=[(1.15 * (i + 1), "coin") for i in range(5)]),
        S("The Dutch called it the wind trade, because buyers were really trading in thin air.", lambda l, d_, T: tavern(l, d_, T, 1), tr=None, sfx=[(0.0, "whoosh"), (0.2, "whoosh")]),
        S("At the peak of the craze, the most famous bulb of all, the Semper Augustus, reportedly sold for ten thousand guilders.",
          alkmaar, tr="drop", sfx=[(0.6 + 0.3 * i, "tick") for i in range(12)] + [("END-1.0", "thud")]),
        S("At the time, a skilled craftsman earned about three hundred guilders a year, so that one bulb was worth more than thirty years of wages.",
          lambda l, d_, T: wages(l, d_, T, 1, years=33, price=10000), tr="whip", sfx=[(0.6 + 0.08 * i, "tick") for i in range(33)]),
        S("In today's money, that's around a hundred and thirty thousand euros if you adjust for prices. But if you measure it in wages, it's like paying over two million dollars for a single flower.", today, tr="zoom", sfx=[(0.3, "coin"), ("END-3.0", "riser")]),
        S("Then, in February sixteen thirty seven, buyers suddenly stopped showing up to the auctions.", lambda l, d_, T: auction(l, d_, T, "FEBRUARY 1637"), tr="whip"),
        S("Panic spread through the taverns, and prices collapsed.", crash, tr="whip", sfx=[(0.8, "boom")], shake=[(0.8, 0.5, 24)], drop=[(0.75, 2.0)]),
        S("In fact, many of those sky-high deals were probably never even paid.", unpaid, tr="whip", sfx=[(0.5, "stamp")], shake=[(0.52, 0.25, 16)]),
        S("But here's the real twist.", twist, tr="flash", sfx=[(-0.9, "riser")]),
        S("When historian Anne Goldgar searched the Dutch archives, she found only thirty seven people who had paid more than three hundred guilders for a bulb.",
          archive, tr="whip", sfx=[(0.5 + 0.15 * i, "pop") for i in range(0, 37, 3)]),
        S("There was no wave of ruin, and no economic collapse.", pamphlet, tr="whip", sfx=[(0.36, "stamp")], shake=[(0.38, 0.25, 16)]),
        S("So the world's most famous bubble might itself have been a bit of a bubble. Follow for more money history.", ending, tr="zoom", sfx=[(2.4, "pop")]),
    ])

if __name__ == "__main__":
    import engine2
    render(spec, sys.argv[1])
