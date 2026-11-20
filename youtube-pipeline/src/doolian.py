"""Doolian Dollars: channel avatars, banner and wordmark."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from kit import F, tulip, CREAM, INK, RED, GOLD

OUT = os.path.join(os.path.dirname(__file__), "..", "logos", "doolian")
os.makedirs(OUT, exist_ok=True)
S = 1000
GOLD_L, GOLD_D, GOLD_M = (250, 214, 120), (140, 96, 28), (226, 176, 70)
BURG_IN, BURG_OUT = (132, 30, 44), (34, 6, 12)
DECO_BG, DECO = (14, 14, 18), (212, 175, 90)
NOTE_G, NOTE_D = (196, 214, 186), (40, 84, 56)


def radial(size, c_in, c_out, cy=0.45, r=0.75):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.clip(np.sqrt(((xx - w / 2) / w) ** 2 + ((yy - h * cy) / w) ** 2) / r, 0, 1)[..., None]
    return Image.fromarray((np.array(c_in) * (1 - d) + np.array(c_out) * d).astype(np.uint8))


def rays(d, cx, cy, n, col, length=3000, spin=0.0):
    for i in range(n):
        a0 = i * 2 * math.pi / n + spin; a1 = a0 + math.pi / n
        d.polygon([(cx, cy), (cx + length * math.cos(a0), cy + length * math.sin(a0)), (cx + length * math.cos(a1), cy + length * math.sin(a1))], fill=col)


def gold_coin(img, cx, cy, r, monogram="DD", font="serif_bold", reeded=True, shadow=True):
    """A shaded gold coin with a beaded rim and an embossed monogram."""
    d = ImageDraw.Draw(img, "RGBA")
    if shadow:
        sh = Image.new("L", img.size); ImageDraw.Draw(sh).ellipse((cx - r + 14, cy - r + 24, cx + r + 14, cy + r + 24), fill=150)
        img.paste(Image.new("RGB", img.size, (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(r * 0.08)))
        d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD_D)
    # face with a soft highlight
    face = Image.new("RGB", (2 * r, 2 * r)); fa = radial((2 * r, 2 * r), GOLD_L, GOLD_M, cy=0.32, r=0.9); face.paste(fa)
    m = Image.new("L", (2 * r, 2 * r)); ImageDraw.Draw(m).ellipse((int(r * 0.07), int(r * 0.07), int(r * 1.93), int(r * 1.93)), fill=255)
    img.paste(face, (cx - r, cy - r), m); d = ImageDraw.Draw(img, "RGBA")
    if reeded:
        for i in range(72):
            a = i * 2 * math.pi / 72; rr = r * 0.86
            d.ellipse((cx + rr * math.cos(a) - r * 0.022, cy + rr * math.sin(a) - r * 0.022, cx + rr * math.cos(a) + r * 0.022, cy + rr * math.sin(a) + r * 0.022), fill=GOLD_D)
    d.ellipse((cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78), outline=GOLD_D, width=max(int(r * 0.025), 2))
    if monogram:
        f = F(font, int(r * (0.95 if len(monogram) == 2 else 1.2)))
        d.text((cx + r * 0.025, cy + r * 0.035), monogram, font=f, fill=GOLD_D, anchor="mm")       # emboss shadow
        d.text((cx - r * 0.012, cy - r * 0.012), monogram, font=f, fill=(255, 236, 170), anchor="mm")  # highlight
        d.text((cx, cy), monogram, font=f, fill=(184, 128, 40), anchor="mm")
    return img


def dollar_d(d, cx, cy, h, col, bar_col=None):
    """A 'D' struck through with two vertical bars, like a dollar sign."""
    f = F("serif_bold", int(h))
    d.text((cx, cy), "D", font=f, fill=col, anchor="mm")
    bw = max(int(h * 0.055), 3)
    for dx in (-0.08, 0.06):
        x = cx + h * dx
        d.rectangle((x - bw / 2, cy - h * 0.58, x + bw / 2, cy + h * 0.58), fill=bar_col or col)


# ---------------- avatars ----------------
def av_coin():
    img = radial((S, S), BURG_IN, BURG_OUT); d = ImageDraw.Draw(img, "RGBA")
    rays(d, 500, 500, 20, (255, 210, 130, 18))
    return gold_coin(img, 500, 500, 330)


def av_dollar_d():
    img = radial((S, S), BURG_IN, BURG_OUT); d = ImageDraw.Draw(img, "RGBA")
    rays(d, 500, 500, 20, (255, 210, 130, 16))
    gold_coin(img, 500, 500, 340, monogram=None)
    d = ImageDraw.Draw(img, "RGBA")
    dollar_d(d, 512, 512, 430, GOLD_D); dollar_d(d, 500, 500, 430, (184, 128, 40), (150, 100, 30))
    return img


def av_deco():
    img = Image.new("RGB", (S, S), DECO_BG); d = ImageDraw.Draw(img, "RGBA")
    for i in range(16):
        a = -math.pi / 2 + (i - 7.5) * 0.17
        d.line([(500, 980), (500 + 1400 * math.cos(a), 980 + 1400 * math.sin(a))], fill=(70, 58, 28), width=6)
    for k in range(4): d.arc((500 - 220 - k * 70, 760 - 220 - k * 70, 500 + 220 + k * 70, 760 + 220 + k * 70), 180, 360, fill=(110, 90, 40), width=5)
    d.rectangle((300, 270, 700, 730), outline=DECO, width=10); d.rectangle((326, 296, 674, 704), outline=DECO, width=3)
    d.text((500, 500), "DD", font=F("sans_black", 260), fill=DECO, anchor="mm")
    for x in (300, 700):
        for y in (270, 730): d.polygon([(x, y - 26), (x + 26, y), (x, y + 26), (x - 26, y)], fill=DECO)
    return img


def av_banknote():
    img = radial((S, S), (40, 90, 60), (8, 26, 16)); d = ImageDraw.Draw(img, "RGBA")
    nt = Image.new("RGBA", (760, 440), (0, 0, 0, 0)); nd = ImageDraw.Draw(nt)
    nd.rounded_rectangle((0, 0, 759, 439), 26, fill=NOTE_G, outline=NOTE_D, width=12)
    nd.rounded_rectangle((30, 30, 729, 409), 16, outline=NOTE_D, width=4)
    nd.ellipse((240, 80, 520, 360), fill=(176, 200, 168), outline=NOTE_D, width=6)
    nd.text((380, 222), "DD", font=F("serif_bold", 150), fill=NOTE_D, anchor="mm")
    for (x, y) in ((90, 90), (670, 90), (90, 350), (670, 350)):
        nd.ellipse((x - 42, y - 42, x + 42, y + 42), outline=NOTE_D, width=5); nd.text((x, y), "$", font=F("serif_bold", 54), fill=NOTE_D, anchor="mm")
    nt = nt.rotate(8, expand=True, resample=Image.BICUBIC)
    img.paste(nt, ((S - nt.width) // 2, (S - nt.height) // 2), nt)
    return img


def av_stack():
    img = radial((S, S), BURG_IN, BURG_OUT); d = ImageDraw.Draw(img, "RGBA")
    rays(d, 500, 460, 20, (255, 210, 130, 14))
    for k in range(6):   # coin stack edges
        y = 760 - k * 46
        d.ellipse((250, y - 50, 750, y + 50), fill=GOLD_D); d.rectangle((250, y - 50 + 50, 750, y + 46), fill=GOLD_D)
        d.ellipse((250, y - 50 - 6, 750, y + 50 - 6), fill=GOLD_M)
        for j in range(0, 500, 22): d.line([(250 + j, y), (250 + j, y + 40)], fill=(120, 80, 22), width=4)
    gold_coin(img, 500, 400, 250, shadow=False)
    return img


AVATARS = [("coin", "Gold coin", av_coin), ("dollar_d", "Dollar-sign D", av_dollar_d), ("deco", "Art deco", av_deco),
           ("banknote", "Banknote", av_banknote), ("stack", "Coin stack", av_stack)]


# ---------------- banner ----------------
BW, BH = 2560, 1440
SAFE = (BW - 1546) // 2, (BH - 423) // 2, (BW + 1546) // 2, (BH + 423) // 2   # visible on every device


def wordmark(d, x, y, h, col1=CREAM, col2=GOLD_L, shadow=(0, 0, 0)):
    f1, f2 = F("serif_bold", int(h)), F("sans_black", int(h * 0.95))
    w1 = d.textlength("DOOLIAN ", font=f1)
    d.text((x + 6, y + 8), "DOOLIAN", font=f1, fill=shadow, anchor="ls"); d.text((x, y), "DOOLIAN", font=f1, fill=col1, anchor="ls")
    d.text((x + w1 + 6, y + 8), "DOLLARS", font=f2, fill=shadow, anchor="ls"); d.text((x + w1, y), "DOLLARS", font=f2, fill=col2, anchor="ls")
    return w1 + d.textlength("DOLLARS", font=f2)


def scatter_props(img, T=1.0):
    """Decorations for the wide edges (seen on TV/desktop; outside the phone-safe area)."""
    d = ImageDraw.Draw(img, "RGBA"); rng = np.random.default_rng(7)
    for i in range(14):
        side = -1 if i % 2 else 1
        r = int(rng.uniform(60, 120))
        for _ in range(50):
            x = BW / 2 + side * rng.uniform(820, 1240); y = rng.uniform(120, BH - 120)
            if not (SAFE[0] - r - 60 < x < SAFE[2] + r + 60 and SAFE[1] - r - 60 < y < SAFE[3] + r + 60): break
        gold_coin(img, int(x), int(y), r, monogram="$" if i % 3 else "DD", shadow=False)
    d = ImageDraw.Draw(img, "RGBA")
    for x, y, rot in ((330, 1150, 18), (2230, 260, -14)):
        nt = Image.new("RGBA", (420, 220), (0, 0, 0, 0)); nd = ImageDraw.Draw(nt)
        nd.rounded_rectangle((0, 0, 419, 219), 14, fill=NOTE_G, outline=NOTE_D, width=8)
        nd.ellipse((150, 40, 270, 180), outline=NOTE_D, width=5); nd.text((210, 110), "$", font=F("serif_bold", 90), fill=NOTE_D, anchor="mm")
        nt = nt.rotate(rot, expand=True, resample=Image.BICUBIC); img.paste(nt, (x - nt.width // 2, y - nt.height // 2), nt)
    d = ImageDraw.Draw(img, "RGBA")
    tulip(d, 2380, 1400, 1.0, stripes=1, sway=0.1)


def banner(style):
    if style == "burgundy":
        img = radial((BW, BH), BURG_IN, BURG_OUT, cy=0.5, r=0.6); d = ImageDraw.Draw(img, "RGBA")
        rays(d, BW / 2, BH / 2, 36, (255, 210, 130, 14), length=3000)
    else:
        img = Image.new("RGB", (BW, BH), DECO_BG); d = ImageDraw.Draw(img, "RGBA")
        for i in range(30):
            a = -math.pi / 2 + (i - 14.5) * 0.105
            d.line([(BW / 2, BH + 200), (BW / 2 + 3000 * math.cos(a), BH + 200 + 3000 * math.sin(a))], fill=(60, 50, 26), width=7)
        for k in range(6): d.arc((BW / 2 - 500 - k * 130, BH - 300 - k * 130, BW / 2 + 500 + k * 130, BH + 700 + k * 130), 180, 360, fill=(90, 74, 36), width=6)
    scatter_props(img)
    d = ImageDraw.Draw(img, "RGBA")
    # centre content, all inside the safe area
    x0, y0, x1, y1 = SAFE
    d.rounded_rectangle((x0 - 10, y0 - 10, x1 + 10, y1 + 10), 40, fill=(0, 0, 0, 120))
    gold_coin(img, x0 + 210, (y0 + y1) // 2, 170)
    d = ImageDraw.Draw(img, "RGBA")
    avail = x1 - 40 - (x0 + 410); h = 150
    while h > 60 and (d.textlength("DOOLIAN ", font=F("serif_bold", h)) + d.textlength("DOLLARS", font=F("sans_black", int(h * 0.95)))) > avail: h -= 4
    wordmark(d, x0 + 410, (y0 + y1) // 2 + 20, h)
    tag = "THE WILDEST STORIES IN THE HISTORY OF MONEY"; th = 46
    while d.textlength(tag, font=F("sans_bold", th)) > avail: th -= 2
    d.text((x0 + 414, (y0 + y1) // 2 + 100), tag, font=F("sans_bold", th), fill=DECO if style == "deco" else (255, 220, 150), anchor="ls")
    return img


def preview_sheet(avatars):
    """How each avatar looks as YouTube shows it: circle crop at full size and at 88 px."""
    TW = 440; sheet = Image.new("RGB", (TW * len(avatars) + 60, TW + 200), (245, 245, 245)); d = ImageDraw.Draw(sheet)
    d.text((30, 24), "Doolian Dollars: avatar concepts (circle crop + real 88px size)", font=F("sans_bold", 40), fill=(30, 30, 30))
    for i, (key, name, im) in enumerate(avatars):
        x = 30 + i * TW; y = 100
        m = Image.new("L", (S, S)); ImageDraw.Draw(m).ellipse((0, 0, S, S), fill=255)
        c = Image.new("RGB", (S, S), (245, 245, 245)); c.paste(im, (0, 0), m)
        sheet.paste(c.resize((TW - 40, TW - 40), Image.LANCZOS), (x, y))
        sm = c.resize((88, 88), Image.LANCZOS); m2 = Image.new("L", (88, 88)); ImageDraw.Draw(m2).ellipse((0, 0, 88, 88), fill=255)
        sheet.paste(sm, (x, y + TW - 20), m2)
        d.text((x + 104, y + TW + 4), f"{i + 1}. {name}", font=F("sans_black", 34), fill=(20, 20, 20))
    return sheet


def banner_preview(img):
    """Banner with the device crop zones marked."""
    p = img.copy(); d = ImageDraw.Draw(p, "RGBA")
    d.rectangle(SAFE, outline=(0, 255, 120), width=8)
    d.rectangle(((BW - 2560) // 2, (BH - 423) // 2, (BW + 2560) // 2, (BH + 423) // 2), outline=(255, 220, 0), width=6)
    d.text((SAFE[0] + 10, SAFE[1] - 50), "safe area: visible on phones, desktop and TV", font=F("sans_bold", 36), fill=(0, 255, 120))
    d.text((40, (BH - 423) // 2 - 50), "desktop width", font=F("sans_bold", 36), fill=(255, 220, 0))
    d.text((40, 40), "full image: TV only", font=F("sans_bold", 36), fill=(255, 255, 255))
    return p.resize((BW // 2, BH // 2), Image.LANCZOS)


if __name__ == "__main__":
    avs = []
    for key, name, fn in AVATARS:
        im = fn(); im.save(os.path.join(OUT, f"avatar_{key}.png")); avs.append((key, name, im))
    preview_sheet(avs).save(os.path.join(OUT, "avatar_sheet.png"))
    for style in ("burgundy", "deco"):
        b = banner(style); b.save(os.path.join(OUT, f"banner_{style}.png"))
        banner_preview(b).save(os.path.join(OUT, f"banner_{style}_zones.png"))
    wm = Image.new("RGBA", (1800, 300), (0, 0, 0, 0)); wd = ImageDraw.Draw(wm)
    wordmark(wd, 20, 220, 170, col1=INK, col2=(184, 128, 40), shadow=(0, 0, 0, 0)); wm.save(os.path.join(OUT, "wordmark_light.png"))
    print("ok")
