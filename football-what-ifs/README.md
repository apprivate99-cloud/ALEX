# Football's Biggest What Ifs: vertical shorts

Vertical (1080×1920, 30fps) animated videos for TikTok, YouTube Shorts and Reels.

| # | Episode | Video |
|---|---------|-------|
| 1 | What if Brian Clough had stayed at Leeds United? (55s) | `out/01-clough-leeds.mp4` (with soundtrack) · `out/01-clough-leeds.silent.mp4` (no audio, so you can add a trending sound) |

## How it's made
- `src/01-clough-leeds.html`: the animation. Open it in a browser to watch a live preview loop.
- `render.js`: screenshots every frame with Playwright and encodes it with ffmpeg. It also writes a cue file of every hit, whoosh and tick.
- `audio.py`: builds the soundtrack (pulse, drone, impacts, rewind effect) from that cue file.

```bash
node render.js src/01-clough-leeds.html out/01-clough-leeds          # -> out/01-clough-leeds.silent.mp4 + cues
python3 audio.py out/01-clough-leeds.cues.json out/01-clough-leeds.wav 55.5
ffmpeg -i out/01-clough-leeds.silent.mp4 -i out/01-clough-leeds.wav -c:v copy -c:a aac -shortest out/01-clough-leeds.mp4
```

Text sits inside the TikTok/Shorts safe area: nothing in the bottom ~400px or the right-hand button column.
Fonts: Anton, Bebas Neue and Inter (SIL OFL), via Fontsource.
