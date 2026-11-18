"""Fast layout check: draw every scene at several moments without TTS or encoding."""
import sys, os, importlib; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
mod = importlib.import_module(sys.argv[1]); out = sys.argv[2]; DUR = 4.5
frames = []
for i, sc in enumerate(mod.spec["scenes"]):
    for frac in (0.15, 0.5, 0.95):
        lt = DUR * frac; img = sc["draw"](lt, DUR, 10 + i * 5 + lt).convert("RGB")
        d = ImageDraw.Draw(img, "RGBA"); mod.theme["chrome"](d, 1, 2)
        d.rectangle((60, 1440, 1020, 1540), fill=(255, 0, 255, 90))  # caption zone
        frames.append(img.resize((216, 384)))
cols = 12; rows = (len(frames) + cols - 1) // cols; sheet = Image.new("RGB", (216 * cols, 384 * rows), (255, 255, 255))
for k, f in enumerate(frames): sheet.paste(f, ((k % cols) * 216, (k // cols) * 384))
sheet.save(out); print(len(frames), "frames")
