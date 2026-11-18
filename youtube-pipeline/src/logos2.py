import sys, os, math; sys.path.insert(0, os.path.dirname(__file__))
from logos import *   # canvas, ctext, goldcoin, S, GOLD2, GOLD_D, OUT
SILVER, SILVER_D = (214, 218, 226), (120, 126, 140)

def taler_tales():  # silver taler (origin of "dollar") + tall-tale scroll
    im = canvas((30, 44, 74), (8, 12, 24)); d = ImageDraw.Draw(im, "RGBA"); cx, cy, r = 500, 500, 330
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SILVER_D); d.ellipse((cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), fill=SILVER)
    d.ellipse((cx - r + 46, cy - r + 46, cx + r - 46, cy + r - 46), outline=SILVER_D, width=8)
    for i in range(48):
        a = i * math.pi / 24; d.ellipse((cx + (r - 30) * math.cos(a) - 6, cy + (r - 30) * math.sin(a) - 6, cx + (r - 30) * math.cos(a) + 6, cy + (r - 30) * math.sin(a) + 6), fill=SILVER_D)
    ctext(d, 300, "T", F("serif_bold", 380), (40, 50, 80), cx=430, word=False); ctext(d, 360, "T", F("serif_bold", 280), (150, 40, 50), cx=590, word=False)
    return im

def gilt_ruin():  # gilded column with a crack
    im = canvas((40, 34, 30), (8, 6, 6)); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((300, 260, 700, 300), fill=GOLD2); d.rectangle((330, 300, 670, 330), fill=GOLD_D)
    for i in range(5): d.rectangle((360 + i * 60, 330, 400 + i * 60, 720), fill=GOLD2 if i % 2 == 0 else (232, 186, 80))
    d.rectangle((330, 720, 670, 750), fill=GOLD_D); d.rectangle((290, 750, 710, 790), fill=GOLD2)
    d.line([(560, 270), (520, 380), (585, 470), (500, 590), (560, 700), (520, 790)], fill=(8, 6, 6), width=16)
    for x, y, s in [(640, 820, 26), (690, 850, 18), (350, 830, 20)]: d.polygon([(x, y), (x + s, y + s // 2), (x + s // 2, y + s)], fill=GOLD_D)
    return im

def florin_folly():  # florin coin wearing a jester's hat
    im = canvas((24, 90, 70), (6, 30, 22)); d = ImageDraw.Draw(im, "RGBA")
    goldcoin(d, 500, 580, 270); ctext(d, 455, "ƒ", F("serif_bold", 260), GOLD_D, word=False)
    hat = [(310, 360), (690, 360), (710, 210), (600, 300), (500, 150), (400, 300), (290, 210)]
    d.polygon(hat, fill=(170, 30, 44)); d.polygon([(500, 150), (600, 300), (500, 360), (400, 300)], fill=(40, 70, 150))
    d.rounded_rectangle((290, 340, 710, 390), 20, fill=GOLD2)
    for x, y in [(290, 210), (500, 150), (710, 210)]: d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=GOLD2, outline=GOLD_D, width=5)
    return im

def bourse_files():  # case-file folder with a stock-exchange facade
    im = canvas((70, 60, 50), (20, 16, 12)); d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(170, 300), (420, 300), (460, 250), (830, 250), (830, 780), (170, 780)], fill=(210, 170, 100))
    d.rectangle((170, 340, 830, 780), fill=(232, 196, 124))
    d.polygon([(300, 470), (500, 380), (700, 470)], fill=(60, 44, 30)); d.rectangle((310, 470, 690, 490), fill=(60, 44, 30))
    for i in range(5): d.rectangle((330 + i * 76, 500, 362 + i * 76, 660), fill=(60, 44, 30))
    d.rectangle((300, 660, 700, 690), fill=(60, 44, 30))
    d.rounded_rectangle((520, 700, 800, 760), 10, fill=(170, 30, 44)); w = d.textlength("CLASSIFIED", font=F("sans_black", 34)); d.text((660 - w / 2, 712), "CLASSIFIED", font=F("sans_black", 34), fill=CREAM)
    return im

def bubblewright():  # a quill drawing a bubble with a chart inside
    im = canvas((50, 20, 70), (12, 4, 20)); d = ImageDraw.Draw(im, "RGBA"); cx, cy, r = 470, 450, 270
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(200, 160, 255, 50), outline=(230, 210, 255), width=12); d.ellipse((cx - 190, cy - 210, cx - 90, cy - 140), fill=(255, 255, 255, 150))
    d.line([(cx - 180, cy + 120), (cx - 60, cy + 70), (cx + 30, cy - 40), (cx + 110, cy - 150)], fill=GOLD2, width=26, joint="curve")
    d.polygon([(640, 900), (700, 680), (860, 560), (760, 760)], fill=CREAM); d.line([(640, 900), (790, 650)], fill=GOLD_D, width=8)
    return im

def ledgerlore():  # ledger with a candle
    im = canvas((60, 30, 26), (16, 8, 6)); d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(150, 520), (490, 560), (490, 820), (150, 780)], fill=CREAM); d.polygon([(850, 520), (510, 560), (510, 820), (850, 780)], fill=(236, 226, 200))
    for i in range(5): d.line([(190, 590 + i * 36), (450, 620 + i * 36)], fill=(160, 140, 120), width=3); d.line([(810, 590 + i * 36), (550, 620 + i * 36)], fill=(160, 140, 120), width=3)
    d.rectangle((640, 300, 700, 520), fill=CREAM); d.ellipse((620, 500, 720, 540), fill=GOLD_D)
    gl = Image.new("L", (S, S)); ImageDraw.Draw(gl).ellipse((520, 140, 820, 420), fill=140); gl = gl.filter(ImageFilter.GaussianBlur(50))
    im = Image.composite(Image.new("RGB", (S, S), (255, 200, 110)), im, gl); d = ImageDraw.Draw(im, "RGBA")
    d.polygon([(670, 180), (700, 260), (670, 300), (640, 260)], fill=(255, 190, 70)); d.polygon([(670, 220), (685, 265), (670, 290), (655, 265)], fill=(255, 245, 200))
    ctext(d, 230, "ƒ", F("serif_bold", 260), GOLD2, cx=360, word=False)
    return im

NEW = [("Taler Tales", taler_tales), ("Gilt & Ruin", gilt_ruin), ("Florin & Folly", florin_folly),
       ("The Bourse Files", bourse_files), ("Bubblewright", bubblewright), ("Ledgerlore", ledgerlore)]
if __name__ == "__main__":
    tiles = []
    for name, fn in NEW:
        im = fn(); slug = name.lower().replace(" & ", "_").replace(" ", "_"); im.save(os.path.join(OUT, "new_" + slug + "_avatar.png"))
        mask = Image.new("L", (S, S)); ImageDraw.Draw(mask).ellipse((0, 0, S, S), fill=255)
        circ = Image.new("RGB", (S, S), (245, 245, 245)); circ.paste(im, (0, 0), mask); tiles.append((name, circ))
    TW = 440; sheet = Image.new("RGB", (TW * 3 + 80, 2 * (TW + 150) + 130), (245, 245, 245)); d = ImageDraw.Draw(sheet)
    d.text((40, 30), "New channel concepts (no existing channel found)", font=F("sans_bold", 40), fill=(30, 30, 30))
    for i, (name, c) in enumerate(tiles):
        x = 40 + (i % 3) * TW; y = 110 + (i // 3) * (TW + 150)
        sheet.paste(c.resize((TW - 60, TW - 60), Image.LANCZOS), (x, y))
        small = c.resize((88, 88), Image.LANCZOS); m2 = Image.new("L", (88, 88)); ImageDraw.Draw(m2).ellipse((0, 0, 88, 88), fill=255)
        sheet.paste(small, (x, y + TW - 40), m2)
        d.text((x + 100, y + TW - 30), name, font=F("sans_black", 34), fill=(20, 20, 20)); d.text((x + 100, y + TW + 12), "@" + name.replace(" & ", "And").replace(" ", ""), font=F("sans_med", 26), fill=(110, 110, 110))
    sheet.save(os.path.join(OUT, "new_logo_sheet.png")); print("ok")
