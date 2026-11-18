#!/bin/bash
# One-time setup: Python packages, the narrator voice model and map data.
# Needs: python3, ffmpeg, curl. Run from the youtube-pipeline folder.
set -e
cd "$(dirname "$0")"
pip install "sherpa-onnx==2.0.1" soundfile numpy pillow onnxruntime
mkdir -p voices data
if [ ! -d voices/kokoro-multi-lang-v1_0 ]; then
  curl -fL -o voices/k.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2
  tar xjf voices/k.tar.bz2 -C voices && rm voices/k.tar.bz2
fi
[ -f data/countries.geojson ] || curl -fL -o data/countries.geojson \
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
echo "Setup done."
