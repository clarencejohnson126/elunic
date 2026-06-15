#!/usr/bin/env python3
"""
Seedance 2.0 (Dreamina) Text-to-Video via BytePlus ARK.
Ein zusammenhaengender 15s-Clip fuer die elunic-Bewerbung: Industrie trifft KI.
Kein Talking-Head, sondern cinematische Sequenzen in elunic-Markenfarben.
"""
import json, time, pathlib, urllib.request, urllib.error, sys

ROOT = pathlib.Path("/Users/clarence/Desktop/Automated Applications/bewerbungen/elunic-ai-consultant/video")
OUT  = ROOT / "seedance_raw.mp4"
KEY  = pathlib.Path("/Users/clarence/Desktop/HYPERFRAMES/.secrets/bytedance_ark.key").read_text().strip()
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
MODEL = "dreamina-seedance-2-0-260128"

DURATION = int(sys.argv[1]) if len(sys.argv) > 1 else 15
RES = sys.argv[2] if len(sys.argv) > 2 else "720p"
FLAGS = f"--resolution {RES} --duration {DURATION} --ratio 16:9 --watermark false"

PROMPT = (
    "Cinematic 15-second single continuous sequence, no text, no captions, no logos, no people speaking. "
    "Anamorphic lens, shallow depth of field, refined color grade dominated by deep elunic brand blue "
    "(#0090d4) and a violet accent (#883ea7), dark premium background, subtle film grain, volumetric light. "
    "SHOT 1 (smart factory): a slow confident dolly glides through a futuristic, spotless smart-factory hall "
    "at blue hour; robotic arms move in synchronized precision, faint holographic data streams and glowing "
    "node networks float over the machines. "
    "SHOT 2 (AI optical inspection): smooth match-cut to an extreme macro of a robotic camera scanning a "
    "polished metal part on a conveyor; crisp cyan scan-lines sweep across the surface, tiny HUD markers and "
    "measurement overlays light up in blue, a flagged detail pulses violet. "
    "SHOT 3 (AI agents orchestration): match-cut into an abstract dark space where dozens of glowing agent "
    "nodes connect with flowing violet-to-blue energy threads, an orchestrated neural lattice expanding "
    "outward, elegant and intelligent. "
    "SHOT 4 (construction meets AI): seamless transition to a steel high-rise structure at dusk that "
    "transforms, beam by beam, into a glowing blue wireframe and live data, bridging the physical building "
    "site with digital intelligence. "
    "SHOT 5 (resolve): a smooth crane pull-back reveals the whole connected industrial landscape gently "
    "glowing in blue and violet, then the camera settles into a calm, clean hero hold with negative space on "
    "the left for a headline. "
    "Continuous energetic but premium camera motion, motion blur on movement, no morphing, no warping, "
    "photoreal, stable geometry. " + FLAGS
)

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)

def main():
    body = {"model": MODEL, "content": [{"type": "text", "text": PROMPT}]}
    print(f"[seedance] POST task  dur={DURATION}s res={RES}")
    try:
        task = api("POST", "/contents/generations/tasks", body)
    except urllib.error.HTTPError as e:
        print(f"POST {e.code}: {e.read().decode()[:400]}")
        sys.exit(2)
    tid = task["id"]
    print(f"[seedance] id={tid}  polling ...")
    for i in range(160):                 # bis ~16 min
        time.sleep(6)
        st = api("GET", f"/contents/generations/tasks/{tid}")
        s = st.get("status")
        if i % 5 == 0:
            print(f"[seedance] t={i*6}s status={s}")
        if s == "succeeded":
            url = st["content"]["video_url"]
            urllib.request.urlretrieve(url, OUT)
            print(f"[seedance] DONE -> {OUT}  usage={st.get('usage', {})}")
            return
        if s in ("failed", "cancelled"):
            print(f"[seedance] {s}: {st.get('error')}")
            sys.exit(3)
    print("[seedance] timeout")
    sys.exit(4)

if __name__ == "__main__":
    main()
