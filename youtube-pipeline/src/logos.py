import sys, os, math; sys.path.insert(0, os.path.dirname(__file__))
from kit import *
OUT = os.path.join(os.path.dirname(__file__), "..", "logos")
S = 1000; GOLD2 = (246, 200, 96); GOLD_D = (150, 104, 30)

def canvas(c1, c2):
    yy, xx = np.mgrid[0:S, 0:S]; r = np.clip(np.sqrt((xx - S / 2) ** 2 + (yy - S * 0.42) ** 2) / (S * 0.75), 0, 1)[..., None]
    return Image.fromarray((np.array(c1) * (1 - r) + np.array(c2) * r).astype(np.uint8))
TEXT = [True]
def ctext(d, y, s, f, fill, cx=S / 2, word=True, **kw):
    if word and not TEXT[0]: return
    w = d.textlength(s, font=f); d.text((cx - w / 2, y), s, font=f, fill=fill, **kw)
def goldcoin(d, cx, cy, r, ring=True):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD_D); d.ellipse((cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14), fill=GOLD2)
    if ring:
        d.ellipse((cx - r + 40, cy - r + 40, cx + r - 40, cy + r - 40), outline=GOLD_D, width=8)
        for i in range(60):
            a = i * math.pi / 30; d.line([(cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a)), (cx + (r - 32) * math.cos(a), cy + (r - 32) * math.sin(a))], fill=GOLD_D, width=4)

def fortune_folly():
    im = canvas((130, 30, 42), (40, 8, 14)); d = ImageDraw.Draw(im, "RGBA")
    goldcoin(d, 500, 470, 330); tulip(d, 500, 720, 1.05, col=(170, 30, 44), stripes=1)
    ctext(d, 820, "FORTUNE & FOLLY", F("serif_bold", 64), CREAM)
    return im

def bubbles_busts():
    im = canvas((24, 40, 70), (6, 10, 22)); d = ImageDraw.Draw(im, "RGBA")
    cx, cy, r = 500, 440, 300
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(120, 190, 255, 40), outline=(200, 230, 255), width=14)
    d.ellipse((cx - 210, cy - 230, cx - 90, cy - 150), fill=(255, 255, 255, 140))
    pts = [(cx - 230, cy + 150), (cx - 120, cy + 110), (cx - 30, cy + 40), (cx + 50, cy - 80), (cx + 110, cy - 190), (cx + 150, cy - 40), (cx + 230, cy + 170)]
    d.line(pts, fill=GOLD2, width=30, joint="curve"); d.line([(cx + 120, cy - 300), (cx + 150, cy - 250), (cx + 125, cy - 215), (cx + 160, cy - 170)], fill=(255, 90, 90), width=12)
    ctext(d, 790, "BUBBLES", F("sans_black", 104), CREAM); ctext(d, 890, "& BUSTS", F("sans_black", 64), GOLD2)
    return im

def gilded_ledger():
    im = canvas((22, 70, 52), (6, 22, 16)); d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(150, 300), (490, 340), (490, 720), (150, 680)], fill=CREAM); d.polygon([(850, 300), (510, 340), (510, 720), (850, 680)], fill=(236, 226, 200))
    d.polygon([(150, 680), (490, 720), (510, 720), (850, 680), (850, 700), (510, 745), (490, 745), (150, 700)], fill=GOLD2)
    for i in range(8):
        y = 380 + i * 38; d.line([(190, y), (450, y + 34)], fill=(160, 180, 200), width=3); d.line([(810, y), (550, y + 34)], fill=(160, 180, 200), width=3)
    ctext(d, 350, "G", F("serif_bold", 300), (22, 70, 52), cx=330, word=False); ctext(d, 350, "L", F("serif_bold", 300), (22, 70, 52), cx=680, word=False)
    ctext(d, 800, "THE GILDED LEDGER", F("serif_bold", 66), GOLD2)
    return im

def paper_fortunes():
    im = canvas((242, 232, 206), (196, 176, 136)); d = ImageDraw.Draw(im, "RGBA")
    nt = Image.new("RGBA", (700, 380), (0, 0, 0, 0)); nd = ImageDraw.Draw(nt)
    nd.rounded_rectangle((0, 0, 699, 379), 24, fill=(216, 200, 160), outline=(110, 70, 40), width=12); nd.rounded_rectangle((30, 30, 669, 349), 16, outline=(110, 70, 40), width=4)
    nd.ellipse((440, 70, 640, 310), outline=(110, 70, 40), width=8); w = nd.textlength("PF", font=F("serif_bold", 150)); nd.text((540 - w / 2, 95), "PF", font=F("serif_bold", 150), fill=(140, 30, 40))
    nd.text((70, 70), "ONE", font=F("serif_bold", 70), fill=(110, 70, 40)); nd.text((70, 160), "FORTUNE", font=F("serif_bold", 56), fill=(110, 70, 40)); nd.text((70, 270), "No. 1637", font=F("mono", 34), fill=(140, 30, 40))
    nt = nt.rotate(8, expand=True, resample=Image.BICUBIC); im.paste(nt, ((S - nt.width) // 2, 230), nt)
    ctext(d, 800, "PAPER FORTUNES", F("serif_bold", 80), (60, 36, 20))
    return im

def coin_crown():
    im = canvas((70, 34, 100), (20, 8, 30)); d = ImageDraw.Draw(im, "RGBA")
    goldcoin(d, 500, 520, 260); ctext(d, 400, "$£ƒ", F("serif_bold", 150), GOLD_D, word=False)
    d.polygon([(330, 260), (360, 120), (430, 210), (500, 90), (570, 210), (640, 120), (670, 260)], fill=GOLD2, outline=GOLD_D, width=8)
    for x in (360, 500, 640): d.ellipse((x - 18, [120, 90, 120][(x - 360) // 140] - 36, x + 18, [120, 90, 120][(x - 360) // 140]), fill=(214, 40, 58))
    ctext(d, 820, "COIN & CROWN", F("serif_bold", 84), CREAM)
    return im

def money_archive():
    im = canvas((60, 62, 70), (16, 16, 20)); d = ImageDraw.Draw(im, "RGBA")
    cx, cy, r = 500, 440, 300; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(120, 124, 134), outline=(40, 40, 46), width=16)
    d.ellipse((cx - 200, cy - 200, cx + 200, cy + 200), fill=(90, 94, 104), outline=(40, 40, 46), width=10)
    for i in range(8):
        a = i * math.pi / 4; d.line([(cx + 60 * math.cos(a), cy + 60 * math.sin(a)), (cx + 180 * math.cos(a), cy + 180 * math.sin(a))], fill=GOLD2, width=22)
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=GOLD2, outline=GOLD_D, width=8); ctext(d, cy - 55, "ƒ", F("serif_bold", 100), GOLD_D, word=False)
    for i in range(6): d.rectangle((cx + r - 20, cy - 160 + i * 60, cx + r + 30, cy - 130 + i * 60), fill=(40, 40, 46))
    ctext(d, 770, "THE MONEY", F("sans_black", 84), CREAM); ctext(d, 855, "ARCHIVE", F("sans_black", 90), GOLD2)
    return im

LOGOS = [("Fortune & Folly", fortune_folly), ("Bubbles & Busts", bubbles_busts), ("The Gilded Ledger", gilded_ledger),
         ("Paper Fortunes", paper_fortunes), ("Coin & Crown", coin_crown), ("The Money Archive", money_archive)]
CENTERS = {"Fortune & Folly": (500, 470, 380), "Bubbles & Busts": (500, 440, 360), "The Gilded Ledger": (500, 510, 400),
           "Paper Fortunes": (500, 420, 380), "Coin & Crown": (500, 420, 370), "The Money Archive": (500, 440, 360)}
if __name__ == "__main__":
    tiles = []
    for name, fn in LOGOS:
        slug = name.lower().replace(" & ", "_").replace(" ", "_")
        TEXT[0] = True; fn().save(os.path.join(OUT, slug + "_wordmark.png"))
        TEXT[0] = False; full = fn(); cx, cy, r = CENTERS[name]
        av = full.crop((cx - r, cy - r, cx + r, cy + r)).resize((S, S), Image.LANCZOS)
        # re-fill the background so the crop edge is clean
        bgc = full.getpixel((10, 10)); base = full.resize((S, S)).filter(ImageFilter.GaussianBlur(60))
        mask = Image.new("L", (S, S)); ImageDraw.Draw(mask).ellipse((0, 0, S, S), fill=255)
        av.save(os.path.join(OUT, slug + "_avatar.png"))
        circ = Image.new("RGB", (S, S), (245, 245, 245)); circ.paste(av, (0, 0), mask); tiles.append((name, circ))
    TW = 440; sheet = Image.new("RGB", (TW * 3 + 80, 2 * (TW + 150) + 130), (245, 245, 245)); d = ImageDraw.Draw(sheet)
    d.text((40, 30), "Channel avatar concepts (circle crop, with real 88px size)", font=F("sans_bold", 40), fill=(30, 30, 30))
    for i, (name, c) in enumerate(tiles):
        x = 40 + (i % 3) * TW; y = 110 + (i // 3) * (TW + 150)
        sheet.paste(c.resize((TW - 60, TW - 60), Image.LANCZOS), (x, y))
        small = c.resize((88, 88), Image.LANCZOS); m2 = Image.new("L", (88, 88)); ImageDraw.Draw(m2).ellipse((0, 0, 88, 88), fill=255)
        sheet.paste(small, (x, y + TW - 40), m2)
        d.text((x + 100, y + TW - 30), name, font=F("sans_black", 34), fill=(20, 20, 20)); d.text((x + 100, y + TW + 12), "@" + name.replace(" & ", "And").replace(" ", ""), font=F("sans_med", 26), fill=(110, 110, 110))
    sheet.save(os.path.join(OUT, "logo_sheet.png"))
    # wordmark sheet for banners
    wm = [Image.open(os.path.join(OUT, n.lower().replace(" & ", "_").replace(" ", "_") + "_wordmark.png")).resize((400, 400), Image.LANCZOS) for n, _ in LOGOS]
    ws = Image.new("RGB", (400 * 3 + 40, 400 * 2 + 40), (245, 245, 245))
    for i, im in enumerate(wm): ws.paste(im, (10 + (i % 3) * 410, 10 + (i // 3) * 410))
    ws.save(os.path.join(OUT, "wordmark_sheet.png")); print("ok")
