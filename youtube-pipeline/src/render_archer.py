"""Render a video using a supplied ElevenLabs recording: python3 render_archer.py <module> <narration.wav> <out.mp4>"""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine2
m = importlib.import_module(sys.argv[1])
m.spec["narration"] = sys.argv[2]
engine2.render(m.spec, sys.argv[3])
