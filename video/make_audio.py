#!/usr/bin/env python3
"""ElevenLabs cinematic score (text-to-sound) fuer den 15s elunic-Spot."""
import json, pathlib, urllib.request, urllib.error, sys

ROOT = pathlib.Path("/Users/clarence/Desktop/Automated Applications/bewerbungen/elunic-ai-consultant/video")
ENV  = pathlib.Path("/Users/clarence/Desktop/HYPERFRAMES/.env").read_text()
KEY  = next(l.split("=",1)[1].strip() for l in ENV.splitlines() if l.startswith("ELEVENLABS_API_KEY="))
OUT  = ROOT / "score.mp3"

PROMPT = ("Premium cinematic corporate technology trailer score, inspiring and confident, deep tech atmosphere, "
          "soft pulsing synth arpeggio, warm sub bass, gentle rising strings building to an uplifting swell, "
          "subtle whoosh transitions, clean resolved ending, modern, futuristic, no vocals, no spoken word.")

body = json.dumps({
    "text": PROMPT,
    "duration_seconds": 15,
    "prompt_influence": 0.35,
}).encode()

req = urllib.request.Request(
    "https://api.elevenlabs.io/v1/sound-generation",
    data=body,
    headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"},
    method="POST")
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        OUT.write_bytes(r.read())
    print(f"[11labs] DONE -> {OUT}  ({OUT.stat().st_size} bytes)")
except urllib.error.HTTPError as e:
    print(f"[11labs] HTTP {e.code}: {e.read().decode()[:400]}")
    sys.exit(2)
