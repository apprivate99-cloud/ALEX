# Taler Tales — money-history Shorts pipeline

Turns a researched script into a finished vertical Short (1080×1920, 30 fps):
narration → animated scenes (maps, charts, characters, stamps) → word-highlighted
captions → music and sound effects → `.mp4`. Everything is generated locally; no
stock footage or copyrighted music.

## Setup (once)

Needs Python 3, `ffmpeg` and `curl`.

```bash
./setup.sh      # installs Python packages, downloads the voice model and map data
```

## Make a video

```bash
cd src
python3 tulip_v2.py tulip_mania.mp4
python3 weimar.py   weimar_hyperinflation.mp4
python3 southsea.py south_sea_newton.mp4
```

A ~60s video takes about 2 minutes to render.

## Check a video before uploading

```bash
python3 preview.py weimar check.png   # every scene at 3 moments, no rendering (seconds)
./audit.sh weimar.mp4 weimar 1.5      # contact sheets of the finished video, a frame every 1.5s
```

`preview.py` marks the caption area in magenta so overlaps are easy to spot.

## How it fits together

| File | What it does |
|---|---|
| `src/engine.py` | Narrator voice (Kokoro v1.0, British "George", speaker 26) and the word check |
| `src/engine2.py` | Renderer: scene timing, transitions, screen shake, sound effects, music, captions |
| `src/kit.py` | Shared drawing kit: characters, tulips, coins, maps, charts, stamps, backgrounds, `fit()` for text in boxes |
| `src/tulip_v2.py`, `weimar.py`, `southsea.py` | One file per video: the script and its scenes |
| `src/lexicon-extra.txt` | Pronunciations for words the voice doesn't know |
| `src/logos.py`, `logos2.py` | Channel logo concepts (output in `logos/`) |

### Writing a new video

Copy one of the video files and change `spec["scenes"]`. Each scene has:

- `say` — the narration. Write numbers as words ("sixteen thirty seven"); captions show them as digits automatically (see `CAP_MAP` in `engine2.py`).
- `draw` — a function that draws the frame at time `lt` within the scene.
- optional `tr` (transition: `whip`, `zoom`, `flash`, `drop`, `None`), `sfx`, `shake`, `drop` (music cut).

### Pronunciation safety

The voice silently **skips** any word it has no pronunciation for. Every render
first checks the whole script and stops with a list of unknown words — add them
to `src/lexicon-extra.txt` (copy the phoneme style of a similar word from
`voices/kokoro-multi-lang-v1_0/lexicon-gb-en.txt`).

### Switching to ElevenLabs later

All narration goes through `tts()` in `src/engine.py`. Replace its body with an
ElevenLabs API call that returns 24 kHz float samples; nothing else changes.

## Fact-checking

Every script was checked against sources before rendering. Uncertain claims are
phrased "reportedly", and charts built from approximate data are labelled so.
Keep doing this for new topics — popular history "facts" are often wrong.

## Finished videos

`videos/` holds the current renders of the three samples. `logos/` holds avatar
and wordmark concepts; the chosen name is **Taler Tales**.
