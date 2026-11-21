"""Synthesises a soundtrack (dark pulse bed + SFX) from the cue file written by render.js.
Usage: python3 audio.py out/01-clough-leeds.cues.json out/01-clough-leeds.wav 55.5
"""
import json, sys, wave
import numpy as np

SR = 44100
cues = json.load(open(sys.argv[1]))
dur = float(sys.argv[3])
N = int(SR * dur)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * (1 - max(pan, 0))
    R[i:i + len(sig)] += sig * (1 + min(pan, 0))


def env(n, a, d):  # attack / exp decay
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


def lowpass(x, k):  # one-pole
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc); y[i] = acc
    return y


def kick():
    n = int(.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, .16)


def hat():
    n = int(.06 * SR); x = rng.standard_normal(n); x = x - lowpass(x, .3)
    return x * env(n, .001, .015)


def impact():
    n = int(1.6 * SR); t = np.arange(n) / SR
    f = 30 + 90 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .003, .55)
    nz = lowpass(rng.standard_normal(n), .08) * env(n, .001, .25) * 1.6
    return np.tanh((boom + nz) * 1.6)


def hit():
    n = int(.6 * SR); t = np.arange(n) / SR
    f = 60 + 120 * np.exp(-t * 20)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, .14)
    return s + lowpass(rng.standard_normal(n), .25) * env(n, .001, .05) * .6


def tick(freq=2200):
    n = int(.05 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t) * env(n, .0005, .008)


def whoosh(length=.55):
    n = int(length * SR); x = rng.standard_normal(n)
    k = np.linspace(.02, .35, n) ** 1.5
    y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += k[i] * (x[i] - acc); y[i] = acc
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return y * e * 1.4


def riser(length):
    n = int(length * SR); t = np.arange(n) / SR
    f = 200 * (6 ** (t / length))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * .25
    nz = rng.standard_normal(n); nz = nz - lowpass(nz, .1)
    return (tone + nz * .35) * (t / length) ** 2


def clink():
    n = int(.4 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * a for f, a in [(2400, .5), (3730, .35), (5210, .2)]) * env(n, .0005, .08)


def rewind(length):
    n = int(length * SR); t = np.arange(n) / SR
    f = 900 + 600 * np.sin(2 * np.pi * 7 * t) - 300 * t
    tone = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .12
    nz = rng.standard_normal(n) * .25
    return (tone + nz) * np.minimum(t / .1, 1) * np.minimum((length - t) / .1, 1)


# ---- music bed: 100 bpm pulse with a minor drone ----
bpm = 100; beat = 60 / bpm
k = kick(); h = hat()
quiet = [(c[0] - .1, c[1]) for c in cues['rewind']]
def in_quiet(t): return any(a <= t < b for a, b in quiet)
t = 0.0; i = 0
while t < dur - 1.5:
    if not in_quiet(t):
        add(k, t, .55)
        if t > 17.2:  # hats once the 44-day countdown starts
            add(h, t + beat / 2, .18, .3); add(h, t, .08, -.3)
    t += beat; i += 1

# drone: root per section (A, F, D, E minor feel)
sections = [(0, 10.4, 55.0), (10.4, 17.2, 43.65), (17.2, 24.2, 36.71), (24.2, 33.2, 43.65), (35.5, 45.6, 41.2), (45.6, dur, 55.0)]
for a, b, f0 in sections:
    n = int((b - a) * SR); tt = np.arange(n) / SR
    saw = sum(np.sin(2 * np.pi * f0 * m * tt + m) / m for m in range(1, 7))
    fifth = sum(np.sin(2 * np.pi * f0 * 1.5 * m * tt) / m for m in range(1, 4))
    pulse = .7 + .3 * np.sin(2 * np.pi * tt / (beat * 2))
    e = np.minimum(tt / .4, 1) * np.minimum((b - a - tt) / .4, 1)
    add((saw + .5 * fifth) * pulse * e, a, .07)

# ---- SFX ----
for c in cues['impact']: add(impact(), c - .02, .9)
for c in cues['hit']: add(hit(), c - .01, .6)
for c in cues['tick']: add(tick(), c, .35)
for c in cues['count']: add(tick(1600), c, .3)
for c in cues['type']: add(tick(3200), c, .25, .2)
for c in cues['whoosh']: add(whoosh(), c - .15, .5)
for c in cues['clink']: add(clink(), c, .45, -.2)
for a, b in cues['riser']: add(riser(b - a), a, .5)
for a, b in cues['rewind']: add(rewind(b - a), a, .6)

mix = np.stack([L, R], 1)
fade = int(1.2 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix = np.tanh(mix * 1.2) ; mix /= np.abs(mix).max() / .89
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[2])
