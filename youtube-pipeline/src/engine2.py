"""Shorts renderer v2: full-frame scenes, transitions, shake, SFX, word-highlight captions."""
import math, os, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
from engine import tts, tts_scene, split_sentences, check_words, font, ease, clamp, W, H, FPS, SR

def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x, k=1.70158): x = clamp(x) - 1; return 1 + x * x * ((k + 1) * x + k)
def tc(d, y, s, f, fill, stroke=0, sf_=None, x=None):
    w = d.textlength(s, font=f); d.text(((W - w) / 2 if x is None else x - w / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sf_)

# ---------- sound effects ----------
def _t(d): return np.arange(int(d * SR)) / SR
def sfx(name):
    rng = np.random.default_rng(len(name))
    if name == "whoosh":
        t = _t(0.45); n = rng.normal(0, 1, len(t)); out = np.zeros_like(n); a = 0
        cut = np.linspace(0.02, 0.35, len(t)) * np.sin(np.pi * t / 0.45)
        for i in range(len(n)): a += cut[i] * (n[i] - a); out[i] = a
        return out * np.sin(np.pi * t / 0.45) ** 2 * 0.9
    if name == "pop":
        t = _t(0.16); f = 700 * np.exp(-t * 18) + 180; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28) * 0.8
    if name == "coin":
        t = _t(0.5); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in [(2637, 9), (3951, 12), (5274, 16)]) * 0.18
    if name == "boom":
        t = _t(1.4); f = 70 * np.exp(-t * 2) + 32
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 1.0 + rng.normal(0, 0.25, len(t)) * np.exp(-t * 8)) * np.exp(-t * 2.6) * 0.9
    if name == "thud":
        t = _t(0.35); f = 140 * np.exp(-t * 14) + 50; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12) * 0.9
    if name == "ding":
        t = _t(0.9); return (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t * 5) * 0.22
    if name == "tick":
        t = _t(0.05); return np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 90) * 0.3
    if name == "riser":
        t = _t(1.2); f = 200 + 900 * (t / 1.2) ** 2
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / 1.2) ** 2 * 0.12 + rng.normal(0, 0.05, len(t)) * (t / 1.2) ** 3
    if name == "stamp":
        return np.concatenate([sfx("thud") * 1.1, np.zeros(10)])
    raise KeyError(name)

def music(dur, bpm, chords, amp, drops=()):
    t = _t(dur); out = np.zeros_like(t); beat = 60 / bpm
    nbeats = int(dur / beat) + 1
    for b in range(nbeats):
        ch = chords[(b // 8) % len(chords)]; st = int(b * beat * SR)
        lt = _t(beat * 1.6); f = ch[b % len(ch)] * 2
        note = (np.sin(2 * np.pi * f * lt) + 0.25 * np.sin(4 * np.pi * f * lt)) * np.exp(-lt * 5)
        seg = out[st: st + len(note)]; seg += note[: len(seg)] * 0.55
        if b % 8 == 0:  # pad
            pl = _t(beat * 8.5); pad = sum(np.sin(2 * np.pi * fr * pl) for fr in ch) / len(ch)
            pad *= np.minimum(pl / 0.6, 1) * np.clip((beat * 8.5 - pl) / 0.6, 0, 1)
            s2 = out[st: st + len(pad)]; s2 += pad[: len(s2)] * 0.5
        if b % 2 == 0:  # soft kick for momentum
            kl = _t(0.18); k = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-kl * 20) + 45) / SR) * np.exp(-kl * 22)
            s3 = out[st: st + len(k)]; s3 += k[: len(s3)] * 0.5
    env = np.ones_like(t)
    for a, b in drops:  # silence the music for impact moments
        env *= 1 - np.clip(np.minimum((t - a) / 0.05, (b - t) / 0.4), 0, 1)
    fade = np.minimum(np.minimum(t / 0.8, 1), np.clip((dur - t) / 1.5, 0, 1))
    return (out * env * fade * amp).astype(np.float32)

# ---------- captions show digits, the voice says words ----------
CAP_MAP = [("one hundred and eight dollars", "$108"), ("A thousand dollars", "$1,000"), ("almost thirteen percent", "almost 13%"),
    ("another twelve", "another 12%"), ("October twenty fourth", "October 24"), ("two thousand six hundred years", "2,600 years"), ("Around two hundred", "Around 200"), ("three hundred and eighty one", "381"), ("seventeen twenty nine", "1729"),
    ("sixteen ninety four", "1694"), ("nineteen twenty nine", "1929"), ("nineteen thirty two", "1932"), ("nineteen fifty four", "1954"),
    ("October twenty ninth", "October 29"), ("October fifteenth", "October 15"), ("September third", "September 3"),
    ("almost ninety percent", "almost 90%"), ("five hundred livres", "500 livres"), ("around ten thousand", "around 10,000"),
    ("five thousand years", "5,000 years"), ("a thousand years", "1,000 years"), ("twenty five years", "25 years"),
    ("sixteen million", "16 million"), ("ten twenty four", "1024"), ("forty one", "41"), ("a hundred and thirty thousand euros", "€130,000"), ("over two million dollars", "over $2 million"),
    ("ten thousand guilders", "10,000 guilders"), ("three hundred guilders", "300 guilders"), ("thirty seven people", "37 people"),
    ("more than thirty years", "more than 30 years"), ("sixteen thirty seven", "1637"), ("sixteen thirty six", "1636"),
    ("nineteen fourteen", "1914"), ("nineteen twenty three", "1923"), ("seventeen twenty", "1720"),
    ("four point two trillion", "4.2 trillion"), ("four point two", "4.2"), ("one trillion", "1 trillion"),
    ("twenty thousand pounds", "£20,000"), ("a thousand pounds", "£1,000"), ("one US dollar", "$1"), ("World War One", "WW1")]
def cap_text(s):
    for a, b in CAP_MAP: s = s.replace(a, b).replace(a[0].upper() + a[1:], b)
    return s

# ---------- render ----------
def render(spec, out_path):
    check_words([sc["say"] for sc in spec["scenes"]])
    gapd = spec.get("gap", 0.22)
    timeline, t0 = [], 0.25
    for sc in spec["scenes"]:
        if spec.get("one_take"):
            a, spans = tts_scene(sc["say"], spec["voice"], spec.get("speed", 1.08))
        else:
            a = tts(sc["say"], spec["voice"], spec.get("speed", 1.0)); spans = None
        dur = len(a) / SR; sc["_spans"] = spans
        timeline.append(dict(st=t0, dur=dur, sc=sc, audio=a)); t0 += dur + sc.get("gap", gapd)
    total = t0 + spec.get("tail", 0.8)
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    for x in timeline: s = int(x["st"] * SR); voice[s: s + len(x["audio"])] += x["audio"]
    voice = voice / (np.abs(voice).max() + 1e-6) * 0.92
    fx = np.zeros(n, np.float32); drops = []
    for i, x in enumerate(timeline):
        evs = list(x["sc"].get("sfx", []))
        if i > 0 and x["sc"].get("tr", "whip") not in (None, "none"): evs.append((-0.12, "whoosh"))
        for off, name in evs:
            if isinstance(off, str): off = x["dur"] - float(off[4:])  # "END-1.0" = 1s before scene end
            s = max(int((x["st"] + off) * SR), 0); clip = sfx(name).astype(np.float32); fx[s: s + len(clip)] += clip[: n - s]
        for a, b in x["sc"].get("drop", []): drops.append((x["st"] + a, x["st"] + b))
    mus = music(n / SR, spec.get("bpm", 100), spec["chords"], spec.get("music_amp", 0.05), drops)
    mus = np.pad(mus, (0, max(0, n - len(mus))))[:n]  # guard float rounding
    mix = voice + fx * 0.55 + mus
    wav = out_path + ".wav"; sf.write(wav, np.clip(mix, -1, 1), SR)

    caps = []
    for x in timeline:
        spans = x["sc"].get("_spans")
        if spans:   # one caption group never crosses a full stop; timed to the real sentence audio
            sents = split_sentences(x["sc"]["say"])
            for si, (sent, (s0, s1)) in enumerate(zip(sents, spans)):
                words = cap_text(sent).split()
                if not words: continue
                # phrase groups: break at commas first, then into balanced chunks of up to 3 words
                clauses, cur = [], []
                for wi, w in enumerate(words):
                    cur.append(w)
                    nxt_w = words[wi + 1] if wi + 1 < len(words) else ""
                    is_date = w[:-1].isdigit() and nxt_w[:1].isdigit()   # keep "3, 1929" together
                    if w.endswith((",", ";", ":")) and not is_date: clauses.append(cur); cur = []
                if cur: clauses.append(cur)
                merged = []
                for c in clauses:
                    if merged and (len(c) == 1 or len(merged[-1]) == 1) and len(merged[-1]) + len(c) <= 4: merged[-1] = merged[-1] + c
                    else: merged.append(c)
                sizes = []
                for c in merged:
                    if len(c) <= 4 and sum(len(w) for w in c) <= 19: sizes.append(len(c)); continue   # short phrase: keep whole
                    n = max(1, -(-len(c) // 3)); sizes += [len(c) // n + (1 if k < len(c) % n else 0) for k in range(n)]
                w8 = [len(w) + 3 for w in words]; tot = sum(w8); acc = 0; wt = []
                for w, k in zip(words, w8): wt.append((x["st"] + s0 + (s1 - s0) * acc / tot, w)); acc += k
                nxt = x["st"] + spans[si + 1][0] if si + 1 < len(spans) else x["st"] + x["dur"] + 0.15
                i = 0
                for sz in sizes:
                    ch = wt[i:i + sz]; end = wt[i + sz][0] if i + sz < len(wt) else nxt
                    caps.append((ch[0][0], end, ch)); i += sz
            continue
        words = cap_text(x["sc"]["say"]).split(); w8 = [len(w) + 3 for w in words]; tot = sum(w8); acc = 0; wt = []
        for w, k in zip(words, w8): wt.append((x["st"] + x["dur"] * acc / tot, w)); acc += k
        step = 3
        for i in range(0, len(wt), step):
            ch = wt[i:i + step]; end = wt[i + step][0] if i + step < len(wt) else x["st"] + x["dur"] + 0.15
            caps.append((ch[0][0], end, ch))
    th = spec["theme"]
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)
    prev_last, cur_idx = None, -1; nframes = int(total * FPS); TR = 0.32
    for fi in range(nframes):
        t = fi / FPS
        idx = max([i for i, x in enumerate(timeline) if x["st"] - 0.12 <= t] or [0])
        if idx != cur_idx:
            if cur_idx >= 0: prev_last = last_frame
            cur_idx = idx
        x = timeline[idx]; sc = x["sc"]; lt = t - x["st"]
        img = sc["draw"](lt, x["dur"], t).convert("RGB")
        for (a, dd, amp) in sc.get("shake", []):
            if a <= lt < a + dd:
                k = amp * (1 - (lt - a) / dd); rng = np.random.default_rng(fi)
                img = Image.fromarray(np.roll(np.asarray(img), (int(rng.integers(-k, k + 1)), int(rng.integers(-k, k + 1))), (0, 1)))
        last_frame = img.copy()
        tr = sc.get("tr", "whip"); p = (lt + 0.12) / TR
        if idx > 0 and prev_last is not None and tr not in (None, "none") and p < 1:
            e = eio(p)
            if tr == "whip":
                c = Image.new("RGB", (W, H)); c.paste(prev_last, (int(-W * e), 0)); c.paste(img, (int(W * (1 - e)), 0)); img = c
            elif tr == "zoom":
                s = 1 + 0.25 * (1 - e); z = img.resize((int(W * s), int(H * s)), Image.BILINEAR)
                z = z.crop(((z.width - W) // 2, (z.height - H) // 2, (z.width - W) // 2 + W, (z.height - H) // 2 + H))
                img = Image.blend(prev_last, z, e)
            elif tr == "flash":
                img = Image.blend(Image.new("RGB", (W, H), (255, 250, 240)), img, e)
            elif tr == "drop":
                c = prev_last.copy(); c.paste(img, (0, int(-H * (1 - e)))); img = c
        d = ImageDraw.Draw(img, "RGBA")
        th["chrome"](d, t, total)
        for cs, ce, ch in caps:
            if cs <= t < ce:
                parts = [w.upper() for _, w in ch]; sp = 20
                for size in (80, 72, 64, 58, 52):
                    f = font("sans_black", size); ws = [d.textlength(p_, font=f) for p_ in parts]
                    if sum(ws) + sp * (len(parts) - 1) < W - 120: break
                xx = (W - sum(ws) - sp * (len(parts) - 1)) / 2; pop = 1 - ease((t - cs) / 0.1); y = th.get("cap_y", 1440) + 12 * pop
                for (wt_, _), p_, w in zip(ch, parts, ws):
                    on = wt_ <= t
                    d.text((xx, y), p_, font=f, fill=th["cap_hi"] if on else th["cap"], stroke_width=9, stroke_fill=th["cap_stroke"])
                    xx += w + sp
                break
        ff.stdin.write(img.tobytes())
        if fi % 300 == 0: print(f"  frame {fi}/{nframes}", flush=True)
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("wrote", out_path, f"{total:.1f}s")
    return timeline
