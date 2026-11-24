import ctypes, json, math, mmap, os, struct, urllib.request
from datetime import datetime

FMT = '<IIffffffffIiQ'
SIZE = struct.calcsize(FMT)
OUT_MD = r'D:\projects\wiki-live-core\docs\telemetry\latest_live_curve_yusra.md'
OUT_JSON = r'D:\projects\wiki-live-core\docs\telemetry\latest_live_curve_state.json'

def eval_pro_127(v: float, dz: float = 0.05, gain: float = 1.27) -> float:
    av = abs(v)
    if av <= dz:
        return 0.0
    s = -1.0 if v < 0.0 else 1.0
    u = min(1.0, (av - dz) / max(1e-6, 1.0 - dz))
    return s * (math.tanh(gain * u) / math.tanh(gain))

def read_shm():
    try:
        shm = mmap.mmap(-1, SIZE, tagname='Local\\FN_PHYSICS_SHM', access=mmap.ACCESS_READ)
        raw = shm.read(SIZE)
        shm.close()
        magic, seq, rx, ry, cx, cy, roll, cval, rexp, dz, mask, wdelta, qpc = struct.unpack(FMT, raw)
        if magic == 0x464E5348:
            return {
                "connected": True,
                "seq": seq,
                "raw_x": round(rx, 3),
                "raw_y": round(ry, 3),
                "curved_x_127": round(eval_pro_127(rx, dz, 1.27), 3),
                "curved_y_127": round(eval_pro_127(ry, dz, 1.27), 3),
                "roll": round(roll, 3),
                "deadzone": round(dz, 3),
                "keys_mask": mask,
                "wheel_delta": wdelta
            }
    except Exception:
        pass
    return {
        "connected": False, "seq": 0, "raw_x": 0.0, "raw_y": 0.0,
        "curved_x_127": 0.0, "curved_y_127": 0.0, "roll": 0.0,
        "deadzone": 0.05, "keys_mask": 0, "wheel_delta": 0
    }

state = read_shm()
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

yusra_note = "Ollama (wikilife-yusra) snapshot saved to WikiLive telemetry folder."
try:
    req_tags = urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2)
    tags_data = json.loads(req_tags.read().decode("utf-8"))
    models = [m.get("name", "") for m in tags_data.get("models", [])]
    model_name = next((m for m in models if "wikilife-yusra" in m), models[0] if models else "wikilife-yusra")

    prompt = (
        f"Analyze this live Rocket League input/curve snapshot concisely in Arabic as Yusra: "
        f"SHM_Connected={state['connected']}, Seq={state['seq']}, "
        f"Curved127=({state['curved_x_127']}, {state['curved_y_127']}), Roll={state['roll']}, "
        f"Deadzone={state['deadzone']}, KeysMask={state['keys_mask']}. "
        f"Give 2 sharp notes on curve smoothness and steering/roll balance."
    )
    payload = json.dumps({"model": model_name, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        if res_json.get("response"):
            yusra_note = res_json["response"].strip()
except Exception as e:
    yusra_note = f"Ollama endpoint standby ({e}); telemetry JSON/MD archived in WikiLive."

md_lines = [
    "# WikiLive Live Telemetry Snapshot (Pro 1.27)",
    f"- **Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"- **SHM Connected:** `{state['connected']}` | **Seq:** `{state['seq']}`",
    f"- **Pro 1.27 Vector (X, Y):** `({state['curved_x_127']}, {state['curved_y_127']})` | **Roll:** `{state['roll']}` | **DZ:** `{state['deadzone']}`",
    f"- **KeysMask:** `{state['keys_mask']}` | **WheelDelta:** `{state['wheel_delta']}`",
    "",
    "## Yusra Live Curve Evaluation",
    yusra_note
]
with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines) + "\n")

print(f"[WIKILIVE + OLLAMA] Saved -> {OUT_MD}")
print(yusra_note)