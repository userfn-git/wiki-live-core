#!/usr/bin/env python3
"""
YUSRA AI COGNITIVE ENGINE (WikiLife Core - PATH02-BR06 / PATH04-BR12)
Offline-First Local Inference Engine via Ollama (GTX 1660 Ti 6GB Optimized)
"""
import os
import sys
import json
import urllib.request
from datetime import datetime
from pathlib import Path

WIKI_ROOT   = Path(r"D:\projects\wiki-live-core")
LUA_ROOT    = Path(r"D:\Lua")
SNAP_DIR    = WIKI_ROOT / "docs" / "snapshots"
OLLAMA_URL  = "http://127.0.0.1:11434/api/generate"
MODEL_NAME  = os.environ.get("YUSRA_LOCAL_MODEL", "wikilife-yusra")

SYSTEM_PROMPT_YUSRA = (
    "You are Yusra (يسرى), the cognitive architect of WikiLife Core. "
    "Respond in precise, structured, high-signal Arabic with clean English technical terms. "
    "Align outputs with the 4 Pathways & 12 Branches (PATH-01 Governance, PATH-02 Knowledge, "
    "PATH-03 Engineering, PATH-04 Distribution & FN Supervision)."
)

def scan_workspace_state() -> dict:
    releases = sorted([f.name for f in (LUA_ROOT / "releases").glob("*.lua")]) if (LUA_ROOT / "releases").exists() else []
    active_path = LUA_ROOT / "active" / "FN_Master_Active.lua"
    active_exists = active_path.exists()
    active_lines = len(active_path.read_text(encoding="utf-8", errors="ignore").splitlines()) if active_exists else 0
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active_lua": "FN_Master_Active.lua" if active_exists else "MISSING",
        "active_lua_lines": active_lines,
        "available_releases": releases,
        "local_model": MODEL_NAME,
    }

def create_tree_snapshot(note: str = "Automated State Checkpoint") -> Path:
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    state = scan_workspace_state()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_file = SNAP_DIR / f"TREE_SNAPSHOT_{ts}.md"
    releases_md = "\n".join([f"  - `{r}`" for r in state["available_releases"]]) or "  - None"
    content = f"""# WikiLife Core — Tree Snapshot (`PATH02-BR05`)
- **Timestamp:** `{state['timestamp']}`
- **Supervisor:** Yusra (`PATH02-BR06`) & Branch 12 (`PATH04-BR12`)
- **Inference Backend:** Local Ollama (`{state['local_model']}`)
- **Note:** {note}

## Active Runtime Telemetry
- **Active Lua Script:** `{state['active_lua']}` ({state['active_lua_lines']} lines)
- **Preserved Lua Releases (`D:\\Lua\\releases`):**
{releases_md}
"""
    snap_file.write_text(content, encoding="utf-8")
    return snap_file

def ask_yusra_local(prompt: str) -> str:
    state = scan_workspace_state()
    full_prompt = (
        f"{SYSTEM_PROMPT_YUSRA}\n\n"
        f"Workspace Context: {json.dumps(state, ensure_ascii=False)}\n\n"
        f"User Request: {prompt}"
    )
    # GTX 1660 Ti (6GB VRAM) safe envelope: num_ctx=4096 prevents VRAM spillover to system RAM
    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "num_ctx": 4096,
            "num_gpu": 99,
            "temperature": 0.3
        }
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as ex:
        return (
            f"[YUSRA OFFLINE ENGINE] Local Ollama server not reachable at {OLLAMA_URL} ({ex}).\n"
            f"Run 'ollama serve' or check installed models via 'ollama list'.\n"
            f"Current State: {json.dumps(state, ensure_ascii=False)}"
        )

def main():
    args = sys.argv[1:]
    if not args or args[0] == "status":
        print(json.dumps(scan_workspace_state(), indent=2, ensure_ascii=False))
    elif args[0] == "snapshot":
        note = " ".join(args[1:]) if len(args) > 1 else "Manual Yusra Snapshot"
        path = create_tree_snapshot(note)
        print(f"[YUSRA] Tree Snapshot saved -> {path}")
    else:
        print(ask_yusra_local(" ".join(args)))

if __name__ == "__main__":
    main()