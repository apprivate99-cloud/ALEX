#!/bin/bash
# audit.sh video.mp4 prefix step : contact sheets of frames every <step> seconds, 10 per sheet
v=$1; p=$2; step=${3:-1.5}; dir=audit_$p; rm -rf $dir; mkdir -p $dir
ffmpeg -loglevel error -i $v -vf "fps=1/$step,scale=270:-1" $dir/f_%03d.png
python3 - "$dir" "$p" <<'PY'
import sys, glob
from PIL import Image, ImageDraw
d, p = sys.argv[1], sys.argv[2]; fs = sorted(glob.glob(f"{d}/f_*.png")); ims = [Image.open(f) for f in fs]; w, h = ims[0].size
for k in range(0, len(ims), 10):
    part = ims[k:k+10]; o = Image.new("RGB", (w * len(part), h + 30), (255, 255, 255)); dr = ImageDraw.Draw(o)
    for i, im in enumerate(part): o.paste(im, (i * w, 30)); dr.text((i * w + 6, 6), f"#{k+i+1}", fill=(0, 0, 0))
    o.save(f"{d}/sheet_{k//10}.png")
print(len(ims), "frames")
PY
