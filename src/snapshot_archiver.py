"""
WikiLife Core - Local Tree Snapshot Archiver (PATH02-BR05)
Uses LocalYusraClient (json_mode=True) to structure raw notes/sessions into JSON snapshots.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from local_yusra import LocalYusraClient

SNAPSHOTS_DIR = Path(__file__).resolve().parent.parent / "docs" / "snapshots"


def create_tree_snapshot(raw_notes: str, branch_tag: str = "PATH02-BR05") -> Path:
    client = LocalYusraClient()
    if not client.is_alive():
        raise RuntimeError("Local Ollama service is offline at http://localhost:11434")

    prompt = (
        "Convert the following session log into a strict JSON object with keys: "
        "'title', 'branch', 'summary', 'decisions' (list of strings), and 'next_actions' (list of strings).\n\n"
        f"Branch: {branch_tag}\nNotes:\n{raw_notes}"
    )

    raw_json = client.chat(prompt, stream=False, json_mode=True)
    parsed = json.loads(raw_json)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    parsed["archived_at_utc"] = timestamp
    parsed["branch"] = branch_tag

    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    out_file = SNAPSHOTS_DIR / f"snapshot_{branch_tag}_{timestamp}.json"
    out_file.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_file


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    notes_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Initialized local offline Yusra engine and CI pipeline."
    saved_path = create_tree_snapshot(notes_input)
    print(f"[WikiLife Core] Snapshot saved: {saved_path}")
