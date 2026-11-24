import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "wikilife-yusra"
ALLOWED_ROOTS = [
    os.path.abspath(r"D:\projects\wiki-live-core"),
    os.path.abspath(r"D:\projects\fn_physics_engine"),
    os.path.abspath(r"D:\Lua"),
    os.path.abspath(r"D:\terminals\config"),
]
AUDIT_LOG = r"D:\projects\fn_physics_engine\math\math_hub_audit.log"
SYNC_QUEUE = r"D:\projects\wiki-live-core\docs\offline_sync_queue.jsonl"

SYSTEM_GUARD = (
    "You are WIKI, the local terminal and workspace agent under WikiLife Core "
    "(4 Paths / 12 Branches). Never invent fictional files or fake Git pushes. "
    "Always report real files only from D:\\projects\\wiki-live-core, D:\\projects\\fn_physics_engine, "
    "D:\\projects\\fn_physics_engine\\math, or D:\\Lua. "
    "Write explanations in clean colloquial Saudi Arabic outside code blocks, with pure English code/commands."
)

def record_event(branch: str, action: str, target: str, detail: str = "") -> None:
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    os.makedirs(os.path.dirname(SYNC_QUEUE), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{branch}] [WIKI:{action}] Target={target} | {detail}"
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    entry = {
        "timestamp": ts,
        "branch": branch,
        "action": action,
        "target": target,
        "detail": detail,
        "synced": False,
    }
    with open(SYNC_QUEUE, "a", encoding="utf-8") as q:
        q.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(line)

def resolve_safe(path_str: str) -> str:
    full = os.path.abspath(path_str)
    for root in ALLOWED_ROOTS:
        if full == root or full.startswith(root + os.sep):
            return full
    raise PermissionError(f"Path outside local workspace scope: {full}")

def list_dir(path: str, branch: str = "PATH01-BR01") -> str:
    target = resolve_safe(path)
    if not os.path.isdir(target):
        return f"[ERR] Not a directory: {target}"
    items = sorted(os.listdir(target))
    record_event(branch, "INSPECT_DIR", target, f"Entries={len(items)}")
    return "\n".join(items) if items else "(empty directory)"

def read_file(path: str, branch: str = "PATH02-BR04") -> str:
    target = resolve_safe(path)
    if not os.path.isfile(target):
        return f"[ERR] File not found: {target}"
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        data = f.read()
    record_event(branch, "READ_FILE", target, f"Chars={len(data)}")
    return data[:24000]

def run_local_terminal(command: str, cwd: str = r"D:\projects\fn_physics_engine\math", branch: str = "PATH03-BR07") -> str:
    safe_cwd = resolve_safe(cwd)
    blocked = ("invoke-webrequest", "curl ", "wget ", "start-bitstransfer")
    low = command.lower()
    if any(b in low for b in blocked):
        return "[BLOCKED] Offline terminal policy: external web downloads disabled in local mode."
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        cwd=safe_cwd,
        capture_output=True,
        text=True,
        timeout=45,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    record_event(branch, "EXEC_PS", safe_cwd, f"Exit={proc.returncode} | Cmd={command[:80]}")
    return out.strip()[:12000] if out.strip() else f"[OK] ExitCode={proc.returncode}"

def post_chat(body: dict) -> dict:
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

def call_ollama(messages) -> dict:
    body = {"model": MODEL_NAME, "messages": messages, "stream": False}
    try:
        return post_chat(body)
    except urllib.error.HTTPError as exc:
        err_detail = ""
        try:
            err_detail = exc.read().decode("utf-8", errors="replace").strip()
        except Exception:
            err_detail = str(exc)
        raise RuntimeError(f"Ollama HTTP {exc.code}: {err_detail}") from exc

def run_task(prompt: str) -> None:
    math_dir = r"D:\projects\fn_physics_engine\math"
    snapshot_files = list_dir(math_dir, "PATH01-BR01")
    math_file_path = os.path.join(math_dir, "fn_1v1_curve_math.py")
    math_preview = read_file(math_file_path, "PATH02-BR04") if os.path.isfile(math_file_path) else "(no fn_1v1_curve_math.py yet)"

    enriched_prompt = (
        f"{prompt}\n\n"
        f"[GROUNDED WORKSPACE SNAPSHOT]\n"
        f"Directory: {math_dir}\n"
        f"Entries:\n{snapshot_files}\n\n"
        f"File: {math_file_path}\n"
        f"Content:\n{math_preview[:4000]}"
    )

    messages = [
        {"role": "system", "content": SYSTEM_GUARD},
        {"role": "user", "content": enriched_prompt},
    ]
    res = call_ollama(messages)
    msg = res.get("message", {})
    print("\n--- WIKI LOCAL TERMINAL RESPONSE ---")
    print(msg.get("content", ""))

if __name__ == "__main__":
    task = (
        " ".join(sys.argv[1:]).strip()
        if len(sys.argv) > 1
        else "Inspect D:\\projects\\fn_physics_engine\\math under PATH01-BR01 and summarize the math files."
    )
    run_task(task)