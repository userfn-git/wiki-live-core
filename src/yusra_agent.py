import json
import os
import subprocess
import sys
import urllib.request

OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "wikilife-yusra"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_powershell",
            "description": "Execute a pure-English PowerShell command on Windows 11 (Drive D: workspace) and return stdout/stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Pure English PowerShell command to run (no Arabic characters inside code)."
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_project_file",
            "description": "Write UTF-8 (no BOM) content to a file inside D:\\projects.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path under D:\\projects"},
                    "content": {"type": "string", "description": "File content"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_project_file",
            "description": "Read text content from a file on Drive D:.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute file path"}
                },
                "required": ["path"]
            }
        }
    }
]

def exec_tool(name: str, args: dict, auto_approve: bool = False) -> str:
    if name == "run_powershell":
        cmd = args.get("command", "")
        print(f"\n[YUSRA TOOL -> PowerShell]\n{cmd}\n")
        if not auto_approve:
            ans = input("Execute this command? [y/N]: ").strip().lower()
            if ans != "y":
                return "Execution denied by user."
        res = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        out = (res.stdout or "") + (res.stderr or "")
        return out.strip() if out.strip() else f"(ExitCode={res.returncode}, no output)"

    if name == "write_project_file":
        path = args.get("path", "")
        if not path.lower().startswith("d:\\projects\\"):
            return "Security policy: writes restricted to D:\\projects\\ only."
        print(f"\n[YUSRA TOOL -> Write File] {path}")
        if not auto_approve:
            ans = input("Allow file write? [y/N]: ").strip().lower()
            if ans != "y":
                return "Write denied by user."
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(args.get("content", ""))
        return f"Successfully wrote {path}"

    if name == "read_project_file":
        path = args.get("path", "")
        if not os.path.isfile(path):
            return f"File not found: {path}"
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()[:12000]

    return f"Unknown tool: {name}"

def chat_loop(auto_approve: bool = False):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Yusra (يسرى), the autonomous local execution agent under WikiLife Core. "
                "You have direct terminal and file tools (run_powershell, write_project_file, read_project_file). "
                "When the user asks to inspect, build, git-push, or modify anything in D:\\projects, "
                "call your tools directly using pure English PowerShell commands (zero Arabic inside PowerShell code). "
                "Respond to the user in clear Saudi Arabic outside tool calls."
            )
        }
    ]
    mode_label = "AUTO-EXEC" if auto_approve else "SAFE-CONFIRM"
    print("============================================================")
    print(f"  WIKILIFE-YUSRA LOCAL AGENT ({MODEL_NAME}) [{mode_label}]")
    print("  Type your instruction (or 'exit' to quit)")
    print("============================================================")

    while True:
        try:
            user_input = input("\nFN > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})

        while True:
            payload = json.dumps({
                "model": MODEL_NAME,
                "messages": messages,
                "tools": TOOLS,
                "stream": False
            }).encode("utf-8")
            req = urllib.request.Request(OLLAMA_CHAT_URL, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            msg = data.get("message", {})
            messages.append(msg)
            tool_calls = msg.get("tool_calls") or []

            if not tool_calls:
                print(f"\n[Yusra]:\n{msg.get('content', '')}")
                break

            for tc in tool_calls:
                fn = tc.get("function", {})
                fn_name = fn.get("name", "")
                fn_args = fn.get("arguments", {})
                if isinstance(fn_args, str):
                    fn_args = json.loads(fn_args)
                result = exec_tool(fn_name, fn_args, auto_approve=auto_approve)
                messages.append({"role": "tool", "content": result})

if __name__ == "__main__":
    auto_flag = "--auto" in sys.argv
    chat_loop(auto_approve=auto_flag)