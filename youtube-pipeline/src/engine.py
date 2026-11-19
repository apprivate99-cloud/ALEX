"""Minimal Shorts renderer: script -> TTS -> animated frames + captions -> mp4."""
import math, os, subprocess, sys, numpy as np, soundfile as sf, sherpa_onnx
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SR = 1080, 1920, 30, 24000
VOICE_DIR = os.path.join(os.path.dirname(__file__), "..", "voices", "kokoro-en-v0_19")
INTER = "/usr/share/fonts/opentype/inter/"
FONTS = {"sans_black": INTER + "InterDisplay-Black.otf", "sans_bold": INTER + "InterDisplay-Bold.otf",
         "sans_med": INTER + "InterDisplay-Medium.otf",
         "serif_bold": "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf",
         "serif": "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf",
         "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"}
_fc = {}
def font(name, size):
    k = (name, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[name], size)
    return _fc[k]

def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def clamp(x): return min(max(x, 0), 1)

_tts = {}
EXTRA_LEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexicon-extra.txt")
def check_words(texts, accent="gb"):
    """Fail before rendering if any word has no pronunciation (the TTS would silently drop it)."""
    import re
    known = set()
    for p in (os.path.join(VOICE_V1, f"lexicon-{accent}-en.txt"), EXTRA_LEX):
        known |= {l.split(" ", 1)[0] for l in open(p, encoding="utf-8")}
    missing = sorted({w.lower() for t in texts for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", t)} - known)
    if missing: raise SystemExit(f"Add pronunciations to lexicon-extra.txt for: {missing}")
VOICE_V1 = os.path.join(os.path.dirname(__file__), "..", "voices", "kokoro-multi-lang-v1_0")
def tts(text, sid, speed=1.05, accent="gb"):
    """Kokoro v1.0 with a proper British or American pronunciation lexicon."""
    if accent not in _tts:
        d = VOICE_V1
        _tts[accent] = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
            kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=d + "/model.onnx", voices=d + "/voices.bin",
                tokens=d + "/tokens.txt", data_dir=d + "/espeak-ng-data", dict_dir=d + "/dict",
                lexicon=d + f"/lexicon-{accent}-en.txt," + EXTRA_LEX, lang="en-gb" if accent == "gb" else "en-us"), num_threads=4)))
    # Speak one sentence at a time: shorter inputs keep the voice's intonation natural,
    # and real pauses between sentences stop it sounding like one long robotic run.
    import re
    parts = [p.strip() for p in re.split(r"(?<=[.?!:])\s+", text.strip()) if p.strip()]
    out = []
    for i, p in enumerate(parts):
        a = _tts[accent].generate(p, sid=sid, speed=speed)
        s = np.array(a.samples, dtype=np.float32)
        nz = np.where(np.abs(s) > 0.01)[0]
        if len(nz): s = s[max(nz[0] - 600, 0): nz[-1] + 1200]
        out.append(s)
        if i < len(parts) - 1:
            out.append(np.zeros(int(SR * (0.32 if p.endswith(("?", "!")) else 0.24)), np.float32))
    return np.concatenate(out) if out else np.zeros(1, np.float32)

def text_center(d, y, txt, f, fill, stroke=0, sfill=None):
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)

def music_bed(dur, chords, base_amp=0.05):
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros_like(t)
    seg = dur / len(chords) if chords else dur
    for i, ch in enumerate(chords):
        m = (t >= i * seg) & (t < (i + 1) * seg + 1.0)
        lt = t[m] - i * seg
        env = np.minimum(lt / 1.2, 1) * np.clip((seg + 1.0 - lt) / 1.0, 0, 1)
        for f in ch:
            out[m] += env * (np.sin(2 * np.pi * f * t[m]) + 0.3 * np.sin(4 * np.pi * f * t[m] + 0.5)) / len(ch)
    fade = np.minimum(np.minimum(t / 1.5, 1), np.clip((dur - t) / 2.0, 0, 1))
    return (out * fade * base_amp).astype(np.float32)

def render(spec, out_path):
    theme = spec["theme"]
    # 1) voice per scene
    gap = 0.28
    clips, timeline, t0 = [], [], 0.4
    for sc in spec["scenes"]:
        a = tts(sc["say"], spec["voice"], spec.get("speed", 1.05))
        dur = len(a) / SR
        timeline.append((t0, dur, sc)); clips.append((t0, a)); t0 += dur + gap
    total = t0 + 0.6
    voice = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for st, a in clips: voice[int(st * SR): int(st * SR) + len(a)] += a
    voice = voice / (np.abs(voice).max() + 1e-6) * 0.9
    mix = voice + music_bed(len(voice) / SR, spec["chords"], spec.get("music_amp", 0.05))
    wav = out_path + ".wav"; sf.write(wav, np.clip(mix, -1, 1), SR)

    # 2) captions: chunks of <=3 words timed by character weight
    caps = []
    for st, dur, sc in timeline:
        words = sc["say"].split(); w8 = [len(w) + 2 for w in words]; tot = sum(w8); acc = 0
        wt = []
        for w, k in zip(words, w8): wt.append((st + dur * acc / tot, w)); acc += k
        for i in range(0, len(wt), 3):
            chunk = wt[i:i + 3]
            end = wt[i + 3][0] if i + 3 < len(wt) else st + dur + gap
            caps.append((chunk[0][0], end, chunk))

    bg = theme["background"]()
    nframes = int(total * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)
    for fi in range(nframes):
        t = fi / FPS
        frame = theme["bg_frame"](bg, t)
        cur = [x for x in timeline if x[0] - 0.15 <= t] or timeline[:1]
        st, dur, sc = cur[-1]
        lt = t - st
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        sc["visual"](d, layer, lt, dur, theme)
        alpha = clamp((lt + 0.15) / 0.25)
        if alpha < 1:
            a = layer.getchannel("A").point(lambda v: int(v * alpha)); layer.putalpha(a)
        frame.alpha_composite(layer)
        d = ImageDraw.Draw(frame)
        theme["chrome"](d, t, total)
        for cs, ce, chunk in caps:
            if cs <= t < ce:
                parts = [w.upper() for _, w in chunk]; sp = 20
                for size in (78, 70, 62, 56, 50):
                    f = font("sans_black", size); widths = [d.textlength(p, font=f) for p in parts]
                    if sum(widths) + sp * (len(parts) - 1) < W - 120: break
                x = (W - sum(widths) - sp * (len(parts) - 1)) / 2
                pop = 1 - ease((t - cs) / 0.12)
                y = 1390 + 10 * pop
                for (wt_, _), p, w in zip(chunk, parts, widths):
                    col = theme["cap_hi"] if wt_ <= t else theme["cap"]
                    d.text((x, y), p, font=f, fill=col, stroke_width=8, stroke_fill=theme["cap_stroke"])
                    x += w + sp
                break
        ff.stdin.write(frame.convert("RGB").tobytes())
        if fi % 150 == 0: print(f"  frame {fi}/{nframes}", flush=True)
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("wrote", out_path, f"{total:.1f}s")


def split_sentences(text):
    import re
    return [p.strip() for p in re.split(r"(?<=[.?!])\s+", text.strip()) if p.strip()]


def tts_scene(text, sid, speed=1.08, accent="gb", breath=0.14):
    """Read a whole scene in ONE take so intonation flows across sentences like a real narrator.
    Returns (audio, spans) where spans[i] = (start_s, end_s) of sentence i, found from the
    model's own pauses. A short extra breath is added only at those sentence breaks."""
    tts("warm up.", sid, speed, accent)  # make sure the engine is loaded
    sents = split_sentences(text)
    raw = np.array(_tts[accent].generate(text, sid=sid, speed=speed).samples, np.float32)
    env = np.convolve(np.abs(raw), np.ones(240) / 240, "same")
    loud = np.where(env > 0.01)[0]
    if not len(loud): return raw, [(0, len(raw) / SR)]
    a0, a1 = max(loud[0] - 600, 0), min(loud[-1] + int(0.12 * SR), len(raw))
    s = raw[a0:a1].copy(); env = env[a0:a1]
    fade = int(0.03 * SR); s[-fade:] *= np.linspace(1, 0, fade)
    # quiet gaps the model chose (candidate sentence breaks)
    quiet = env < 0.004; gaps, st = [], None
    for i, q in enumerate(quiet):
        if q and st is None: st = i
        if (not q or i == len(quiet) - 1) and st is not None:
            if (i - st) > 0.07 * SR and st > 0 and i < len(quiet) - 1: gaps.append((st, i))
            st = None
    # expected break positions from character counts, then snap each to the nearest real gap
    lens = [len(x) for x in sents]; tot = sum(lens); cuts = []; last = 0
    for k in range(len(sents) - 1):
        est = len(s) * sum(lens[:k + 1]) / tot
        cands = [g for g in gaps if g[0] > last]
        if not cands: break
        g = min(cands, key=lambda g: abs((g[0] + g[1]) / 2 - est) - 0.4 * (g[1] - g[0]))
        cuts.append(g); last = g[1]
    # rebuild audio with a small breath inserted in the middle of each sentence break
    out, spans, pos, t = [], [], 0, 0.0
    for (g0, g1) in cuts:
        mid = (g0 + g1) // 2
        out.append(s[pos:mid]); spans.append((t, (t * SR + (g0 - pos)) / SR)); t += (mid - pos) / SR
        out.append(np.zeros(int(breath * SR), np.float32)); t += breath; pos = mid
    out.append(s[pos:]); spans.append((t, t + (len(s) - pos) / SR))
    while len(spans) < len(sents): spans.append(spans[-1])
    return np.concatenate(out), spans


# ---------- exact word timings ----------
ASR_DIR = os.path.join(os.path.dirname(__file__), "..", "voices", "sherpa-onnx-zipformer-small-en-2023-06-26")
_asr = None
def word_times(audio, script_words):
    """Return a start time (seconds) for every word in `script_words`, measured from the audio
    with a speech recogniser and matched back to the script. Unmatched words are interpolated."""
    global _asr
    import difflib, re
    if _asr is None:
        d = ASR_DIR
        _asr = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=d + "/encoder-epoch-99-avg-1.int8.onnx", decoder=d + "/decoder-epoch-99-avg-1.onnx",
            joiner=d + "/joiner-epoch-99-avg-1.int8.onnx", tokens=d + "/tokens.txt", num_threads=4, decoding_method="greedy_search")
    # the recogniser expects 16 kHz
    n16 = int(len(audio) * 16000 / SR)
    a16 = np.interp(np.linspace(0, len(audio) - 1, n16), np.arange(len(audio)), audio).astype(np.float32)
    st = _asr.create_stream(); st.accept_waveform(16000, a16); _asr.decode_stream(st)
    toks, ts = st.result.tokens, st.result.timestamps
    # rebuild recognised words (BPE pieces starting with ▁ begin a word)
    rec, rec_t = [], []
    for tk, t in zip(toks, ts):
        if tk.startswith(("▁", " ")) or not rec: rec.append(tk.lstrip("▁ ").lower()); rec_t.append(t)
        else: rec[-1] += tk.lower()
    norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
    sw = [norm(w) for w in script_words]
    out = [None] * len(sw)
    sm = difflib.SequenceMatcher(a=sw, b=[norm(w) for w in rec], autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): out[blk.a + k] = rec_t[blk.b + k]
    # fill gaps by interpolating between known neighbours
    known = [i for i, v in enumerate(out) if v is not None]
    total = len(audio) / SR
    if not known: return [total * i / max(len(sw), 1) for i in range(len(sw))]
    for i in range(len(out)):
        if out[i] is None:
            lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
            if lo is None: out[i] = out[hi] * i / max(hi, 1)
            elif hi is None: out[i] = out[lo] + (total - out[lo]) * (i - lo) / (len(out) - lo)
            else: out[i] = out[lo] + (out[hi] - out[lo]) * (i - lo) / (hi - lo)
    return out
