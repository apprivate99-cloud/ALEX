"""Render short voice-comparison clips: same lines, different British narrators."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from kit2 import *
import kit
kit.ERA = "1920s"; kit.COIN_SYM = "$"

LINES = [
    "Did you know the American stock market once lost almost a quarter of its value in just two days? It happened in October nineteen twenty nine.",
    "It became known as the Wall Street Crash, and it was only the beginning.",
    "Within weeks, around thirty billion dollars in share value had been wiped out. Could it happen again? Follow for more finance history.",
]
VOICES = [(24, "DANIEL", "male"), (25, "FABLE", "male"), (27, "LEWIS", "male"), (21, "EMMA", "female"), (22, "ISABELLA", "female"), (26, "GEORGE", "male · current voice")]


def card(name, desc, idx):
    def draw(lt, dur, T):
        img = deco_bg(); d = ImageDraw.Draw(img, "RGBA")
        pill(d, 230, f"VOICE {idx}", INK, GOLD, 50)
        tc(d, 380, name, F("sans_black", 170), CREAM, 8, (10, 10, 10))
        tc(d, 590, desc, F("serif_bold", 60), DECO)
        r = 90 + 12 * math.sin(T * 8)   # pulsing speaker icon
        d.ellipse((540 - r, 900 - r, 540 + r, 900 + r), outline=DECO, width=8)
        d.polygon([(500, 870), (530, 870), (580, 830), (580, 970), (530, 930), (500, 930)], fill=CREAM)
        return img
    return draw


theme = dict(chrome=lambda d, t, total: d.rectangle((0, H - 10, W * t / total, H), fill=GOLD), cap=(255, 255, 255), cap_hi=(255, 206, 72), cap_stroke=(0, 0, 0), cap_y=1450)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for i, (sid, name, desc) in enumerate(VOICES, 1):
        spec = dict(theme=theme, voice=sid, speed=1.08, one_take=True, bpm=100, music_amp=0.035, gap=0.35, tail=0.6,
                    chords=[[110, 138.6, 164.8], [98, 123.5, 146.8]],
                    scenes=[dict(say=line, draw=card(name, desc, i), tr="none" if k else "none") for k, line in enumerate(LINES)])
        render(spec, os.path.join(out, f"voice_{i}_{name.lower()}.mp4"))
