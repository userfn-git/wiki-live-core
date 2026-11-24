import json
import os
import subprocess
import sys
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
    "You are Yusra (يسرى), strictly a local terminal and workspace agent under WikiLife Core "
    "(4 Paths / 12 Branches). Never invent fictional files, zodiac/astrology topics, or fake Git pushes. "
    "Always inspect real directories/files in D:\\projects\\wiki-live-core, D:\\projects\\fn_physics_engine, "
    "D:\\projects\\fn_physics_engine\\math, or D:\\Lua before reporting file states. "
    "Write explanations in clean colloquial Saudi Arabic outside code blocks, with pure English code/commands."
)

def record_event(branch: str, action: str, target: str, detail: str = "") -> None:
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    os.makedirs(os.path.dirname(SYNC_QUEUE), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{branch}] [YUSRA:{action}] Target={target} | {detail}"
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

def write_file(path: str, content: str, branch: str = "PATH03-BR07") -> str:
    target = resolve_safe(path)
    existed = os.path.isfile(target)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    op = "UPDATED" if existed else "CREATED"
    record_event(branch, op, target, f"Bytes={os.path.getsize(target)}")
    return f"[OK] {op} ({branch}): {target}"

def delete_file(path: str, branch: str = "PATH01-BR01") -> str:
    target = resolve_safe(path)
    if not os.path.isfile(target):
        return f"[SKIP] File not found: {target}"
    os.remove(target)
    record_event(branch, "DELETED", target, "Removed locally in terminal mode")
    return f"[OK] DELETED ({branch}): {target}"

def run_local_terminal(command: str, cwd: str = r"D:\projects\wiki-live-core", branch: str = "PATH03-BR07") -> str:
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

TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files in an allowed local workspace directory.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "branch": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read UTF-8 file content in an allowed local workspace.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "branch": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or update a UTF-8 file in an allowed local workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                    "branch": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Remove an obsolete file in an allowed local workspace.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "branch": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_local_terminal",
            "description": "Run a local PowerShell command inside an allowed workspace without internet access.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "cwd": {"type": "string"},
                    "branch": {"type": "string"},
                },
                "required": ["command"],
            },
        },
    },
]

TOOL_FN = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "delete_file": delete_file,
    "run_local_terminal": run_local_terminal,
}

def call_ollama(messages):
    payload = json.dumps(
        {"model": MODEL_NAME, "messages": messages, "tools": TOOLS_SPEC, "stream": False}
    ).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_task(prompt: str) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_GUARD},
        {"role": "user", "content": prompt},
    ]
    for _ in range(12):
        res = call_ollama(messages)
        msg = res.get("message", {})
        messages.append(msg)
        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            print("\n--- YUSRA LOCAL TERMINAL RESPONSE ---")
            print(msg.get("content", ""))
            return
        for tc in tool_calls:
            fn_info = tc.get("function", {})
            name = fn_info.get("name", "")
            args = fn_info.get("arguments", {})
            if isinstance(args, str):
                args = json.loads(args)
            try:
                out = TOOL_FN[name](**args) if name in TOOL_FN else f"[ERR] Unknown tool: {name}"
            except Exception as exc:
                out = f"[ERR] {exc}"
            messages.append({"role": "tool", "content": str(out)})

if __name__ == "__main__":
    task = (
        " ".join(sys.argv[1:]).strip()
        if len(sys.argv) > 1
        else "Inspect D:\\projects\\wiki-live-core, D:\\projects\\fn_physics_engine\\math, and D:\\Lua under PATH01-BR01 using tools and report real files only."
    )
    run_task(task)