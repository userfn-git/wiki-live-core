import json
import sys
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"

def build_blueprint(user_spec: str):
    prompt = (
        "Act as WikiLife Yusra Repo & Pipeline Builder (PATH03-BR07). "
        "Generate a complete, pure-English PowerShell execution script (zero Arabic inside code) "
        "with D:\\projects isolation, git userfn-git config, .gitignore, and verification steps for:\n"
        f"{user_spec}"
    )
    payload = json.dumps({
        "model": "wikilife-yusra",
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("\n=== [WIKILIFE YUSRA REPO BUILDER] ===\n")
        print(data.get("response", ""))

if __name__ == "__main__":
    spec = " ".join(sys.argv[1:]).strip()
    if not spec:
        print("Usage: python yusra_repo_builder.py \"<describe repo or feature to build>\"")
    else:
        build_blueprint(spec)