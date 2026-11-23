import json
import os
import socket
import subprocess
import sys
import urllib.request

OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME      = "wikilife-yusra"
ALLOWED_ROOT    = os.path.abspath(r"D:\projects")
RL_API_HOST     = "127.0.0.1"
RL_API_PORT     = 49125

VALID_COMMANDS = {
    "LoadReplay",
    "SeekReplay",
    "SetGameSpeed",
    "ChangePOV",
    "SetHUDVisibility",
    "SetMatchPaused"
}

VALID_PERSPECTIVES = {
    "Fly",
    "SoftAttach",
    "HardAttach",
    "PlayerView",
    "AutoCam",
    "Camera_Director"
}

def is_path_safe(target_path: str) -> bool:
    abs_p = os.path.abspath(target_path)
    return abs_p.startswith(ALLOWED_ROOT)

def run_powershell(command: str, auto_confirm: bool = False) -> str:
    if not auto_confirm:
        ans = input(f"\n[SAFE-CONFIRM] Execute PowerShell command?\n  > {command}\nApprove [y/N]: ").strip().lower()
        if ans not in ("y", "yes"):
            return "Execution denied by user."
    proc = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    return json.dumps({"exit_code": proc.returncode, "stdout": out[:4000], "stderr": err[:2000]})

def read_project_file(path: str) -> str:
    if not is_path_safe(path):
        return f"Access denied: path must be inside {ALLOWED_ROOT}"
    if not os.path.isfile(path):
        return f"File not found: {path}"
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()[:8000]

def write_project_file(path: str, content: str, auto_confirm: bool = False) -> str:
    if not is_path_safe(path):
        return f"Access denied: path must be inside {ALLOWED_ROOT}"
    if not auto_confirm:
        ans = input(f"\n[SAFE-CONFIRM] Write {len(content)} chars to {path}?\nApprove [y/N]: ").strip().lower()
        if ans not in ("y", "yes"):
            return "File write denied by user."
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return f"Successfully wrote {len(content)} chars to {path}"

def control_rocket_league_client(command: str, data: dict) -> str:
    """Sends an official Epic Games MatchStatsExporter_TA two-way JSON command over TCP 49125."""
    if command not in VALID_COMMANDS:
        return json.dumps({"status": "error", "message": f"Invalid Command '{command}'. Allowed: {sorted(VALID_COMMANDS)}"})

    if not isinstance(data, dict):
        return json.dumps({"status": "error", "message": "Data must be a JSON object."})

    # Validate official Epic Games schema constraints
    if command == "ChangePOV":
        focus = data.get("Focus")
        persp = data.get("Perspective")
        if focus is None and persp is None:
            return json.dumps({"status": "error", "message": "ChangePOV requires at least Focus or Perspective."})
        if focus is not None and focus != "Ball" and not str(focus).isdigit():
            return json.dumps({"status": "error", "message": "Focus must be 'Ball' or an all-digits player shortcut string (e.g. '1')."})
        if persp is not None and persp not in VALID_PERSPECTIVES:
            return json.dumps({"status": "error", "message": f"Invalid Perspective '{persp}'. Allowed: {sorted(VALID_PERSPECTIVES)}"})

    elif command == "LoadReplay":
        if not data.get("FileName") and not data.get("Path"):
            return json.dumps({"status": "error", "message": "LoadReplay requires FileName or Path."})

    elif command == "SeekReplay":
        if data.get("Frame") is None and data.get("TimeSeconds") is None:
            return json.dumps({"status": "error", "message": "SeekReplay requires Frame or TimeSeconds."})

    elif command == "SetGameSpeed":
        spd = data.get("Speed")
        if spd is None or float(spd) < 0.0:
            return json.dumps({"status": "error", "message": "SetGameSpeed requires Speed >= 0."})

    elif command == "SetHUDVisibility":
        if not isinstance(data.get("bVisible"), bool):
            return json.dumps({"status": "error", "message": "SetHUDVisibility requires boolean bVisible."})

    elif command == "SetMatchPaused":
        if not isinstance(data.get("bPaused"), bool):
            return json.dumps({"status": "error", "message": "SetMatchPaused requires boolean bPaused."})

    envelope = json.dumps({"Command": command, "Data": data}) + "\n"
    try:
        with socket.create_connection((RL_API_HOST, RL_API_PORT), timeout=3.0) as s:
            s.sendall(envelope.encode("utf-8"))
        return json.dumps({"status": "sent", "target": f"{RL_API_HOST}:{RL_API_PORT}", "payload": json.loads(envelope)})
    except Exception as exc:
        return json.dumps({"status": "socket_error", "message": f"Could not reach Rocket League Stats API on {RL_API_HOST}:{RL_API_PORT}: {exc}"})

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "run_powershell",
            "description": "Execute a PowerShell command on the Windows workstation.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_project_file",
            "description": "Read a file inside D:\\projects.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_project_file",
            "description": "Write or update a file inside D:\\projects.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_rocket_league_client",
            "description": (
                "Control Rocket League replay/spectator playback via Official Epic Games MatchStatsExporter_TA TCP 49125. "
                "Supports LoadReplay ({FileName or Path}), SeekReplay ({Frame or TimeSeconds}), "
                "SetGameSpeed ({Speed >= 0}), ChangePOV ({Focus: 'Ball'|'<digits>', Perspective: 'Fly'|'SoftAttach'|'HardAttach'|'PlayerView'|'AutoCam'|'Camera_Director'}), "
                "SetHUDVisibility ({bVisible: bool}), and SetMatchPaused ({bPaused: bool})."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "enum": sorted(VALID_COMMANDS)},
                    "data": {"type": "object"}
                },
                "required": ["command", "data"]
            }
        }
    }
]

def call_ollama_chat(messages: list) -> dict:
    payload = json.dumps({
        "model": MODEL_NAME,
        "messages": messages,
        "tools": TOOLS_SCHEMA,
        "think": False,
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_CHAT_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

def agent_loop(auto_confirm: bool = False):
    print("=========================================================================", flush=True)
    print(f"  WIKILIFE-YUSRA LOCAL AGENT ({MODEL_NAME}) | REPLAY DIRECTOR ARMED", flush=True)
    print(f"  Workspace Scope: {ALLOWED_ROOT} | RL Two-Way Socket: {RL_API_HOST}:{RL_API_PORT}", flush=True)
    print("  Type 'exit' or 'quit' to close.", flush=True)
    print("=========================================================================", flush=True)

    system_msg = (
        "You are Yusra (wikilife-yusra), the cognitive engineering co-pilot for WikiLife Core and FN Physics Engine. "
        "Respond in clear colloquial Saudi Arabic outside code blocks, while commands and code are pure English. "
        "You can inspect files in D:\\projects, run PowerShell commands, and direct Rocket League replays via "
        "control_rocket_league_client (LoadReplay, SeekReplay, SetGameSpeed, ChangePOV, SetHUDVisibility, SetMatchPaused)."
    )
    messages = [{"role": "system", "content": system_msg}]

    while True:
        try:
            user_input = input("\nyusra> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[AGENT EXIT]", flush=True)
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})

        while True:
            resp = call_ollama_chat(messages)
            msg = resp.get("message", {})
            messages.append(msg)
            tool_calls = msg.get("tool_calls") or []

            if not tool_calls:
                print("\n" + (msg.get("content") or "").strip(), flush=True)
                break

            for tc in tool_calls:
                fn = tc.get("function", {})
                fn_name = fn.get("name", "")
                args = fn.get("arguments") or {}
                if isinstance(args, str):
                    args = json.loads(args)

                print(f"[TOOL CALL] {fn_name}({json.dumps(args)})", flush=True)
                if fn_name == "run_powershell":
                    result = run_powershell(args.get("command", ""), auto_confirm=auto_confirm)
                elif fn_name == "read_project_file":
                    result = read_project_file(args.get("path", ""))
                elif fn_name == "write_project_file":
                    result = write_project_file(args.get("path", ""), args.get("content", ""), auto_confirm=auto_confirm)
                elif fn_name == "control_rocket_league_client":
                    result = control_rocket_league_client(args.get("command", ""), args.get("data", {}))
                else:
                    result = f"Unknown tool: {fn_name}"

                print(f"[TOOL RESULT] {result[:300]}", flush=True)
                messages.append({"role": "tool", "content": result})

if __name__ == "__main__":
    auto_mode = "--auto" in sys.argv
    agent_loop(auto_confirm=auto_mode)