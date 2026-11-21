"""Generates a timed voiceover track with Piper TTS (offline neural voice).
Usage: python3 voiceover.py <voice.onnx> out/01-clough-leeds.vo.wav 55.5
Each line starts at its cue time, or straight after the previous line if that runs long.
Spellings like "Cluff" are phonetic on purpose, so the voice pronounces the names correctly.
"""
import sys, wave, io
import numpy as np
from piper import PiperVoice, SynthesisConfig

SCRIPT = [
    (0.4,  "What if Brian Cluff had stayed at Leeds?"),
    (3.0,  "He lasted forty-four days."),
    (4.7,  "Summer, seventy-four. Leeds are champions of England."),
    (7.5,  "But Don Reevee leaves, to manage England."),
    (10.4, "His replacement? Their fiercest critic."),
    (11.9, "Brian Cluff."),
    (13.4, "Day one, he tells the players to bin their medals. They never won them fairly."),
    (17.5, "Forty-four days of chaos followed."),
    (20.0, "Six games. One win. Players in revolt."),
    (22.2, "Sacked."),
    (24.3, "What happened next?"),
    (25.2, "Cluff took Forest from the Second Division, to champions, to two European Cups."),
    (29.9, "And Leeds? Relegated by eighty-two."),
    (33.2, "But what if he'd stayed?"),
    (35.6, "Picture it."),
    (36.6, "Peter Taylor follows him to Elland Road."),
    (38.8, "Cluff wins over Bremner and Jyles."),
    (41.0, "Leeds beat Bayern in Paris. Champions of Europe."),
    (43.2, "And Forest? Stuck in Division Two."),
    (45.7, "Leeds United. Kings of Europe?"),
    (49.0, "Dynasty... or disaster?"),
    (50.5, "Would Cluff have built an empire, or burned it down?"),
    (52.7, "Comment your verdict, and follow for number two."),
]

voice = PiperVoice.load(sys.argv[1])
out, dur = sys.argv[2], float(sys.argv[3])
SR = voice.config.sample_rate
track = np.zeros(int(SR * (dur + 3)))
cursor = 0.0
for t, text in SCRIPT:
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        voice.synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=0.84, noise_scale=0.6, noise_w_scale=0.7))
    buf.seek(0)
    with wave.open(buf) as r:
        a = np.frombuffer(r.readframes(r.getnframes()), '<i2').astype(float) / 32768
    nz = np.nonzero(np.abs(a) > .01)[0]
    a = a[nz[0]: nz[-1] + int(.05 * SR)]  # trim leading/trailing silence
    start = max(t, cursor + .08)
    late = start - t
    i = int(start * SR); track[i:i + len(a)] += a
    cursor = start + len(a) / SR
    print(f"{t:5.1f}s  {'(+%.1fs late) ' % late if late > .05 else ''}{len(a)/SR:4.1f}s  {text}")
track = track[: int(SR * dur)]
track /= np.abs(track).max() / .95
with wave.open(out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype('<i2').tobytes())
print('ends at %.1fs (video is %.1fs)' % (cursor, dur))
