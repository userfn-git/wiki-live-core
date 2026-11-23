"""
WikiLife Core - Local Yusra AI Adapter (PATH03-BR08)
Connects directly to local Ollama REST API (http://localhost:11434) using Python 3.12 stdlib.
"""

import json
import sys
import urllib.error
import urllib.request
from typing import Generator, Optional

OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "wikilife-yusra"


class LocalYusraClient:
    def __init__(self, model: str = DEFAULT_MODEL, host: str = OLLAMA_HOST) -> None:
        self.model = model
        self.host = host.rstrip("/")

    def is_alive(self) -> bool:
        """Check if local Ollama daemon is running and reachable."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except (urllib.error.URLError, TimeoutError):
            return False

    def chat(
        self,
        prompt: str,
        stream: bool = True,
        json_mode: bool = False,
        keep_alive: str = "5m",
    ) -> str | Generator[str, None, None]:
        """Send a prompt to wikilife-yusra and return full text or token stream."""
        payload: dict = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream,
            "keep_alive": keep_alive,
        }
        if json_mode:
            payload["format"] = "json"

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        if not stream:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result.get("message", {}).get("content", "")

        def _stream_generator() -> Generator[str, None, None]:
            with urllib.request.urlopen(req, timeout=120) as resp:
                for raw_line in resp:
                    if not raw_line.strip():
                        continue
                    chunk = json.loads(raw_line.decode("utf-8"))
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if chunk.get("done", False):
                        break

        return _stream_generator()

    def unload_vram(self) -> bool:
        """Immediately free 6GB VRAM by setting keep_alive to 0."""
        payload = {"model": self.model, "keep_alive": 0}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except urllib.error.URLError:
            return False


def main() -> None:
    # Ensure UTF-8 console output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    client = LocalYusraClient()
    if not client.is_alive():
        print("[ERROR] Ollama service is not running on http://localhost:11434", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) > 1:
        if sys.argv[1] == "--unload":
            ok = client.unload_vram()
            print("[WikiLife Core] VRAM unloaded." if ok else "[ERROR] Failed to unload VRAM.")
            return
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = "أكدي جاهزية المحرك المحلي ويكي لايف في سطرين."

    for token in client.chat(user_prompt, stream=True):
        print(token, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
