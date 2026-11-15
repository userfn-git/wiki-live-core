import json, pathlib
from src.core.objects import Blob, Tree, Commit
class YusraSnapshot:
    def __init__(self, root="docs/snapshots"): self.root=pathlib.Path(root); self.root.mkdir(parents=True, exist_ok=True)
    def capture(self, sid: str, topic: str, notes: list) -> dict:
        md=f"# [Yusra Snapshot] {sid} - {topic}\n\n" + "\n".join([f"- {n}" for n in notes]) + "\n"
        b=Blob(md); t=Tree({f"{sid}.md":b.sha}); hf=self.root/"HEAD.json"
        p=json.loads(hf.read_text(encoding="utf-8"))["commit"] if hf.exists() else None
        c=Commit(t.sha, f"snapshot({sid}): {topic}", p); (self.root/f"{sid}.md").write_text(md, encoding="utf-8")
        st={"id":sid,"topic":topic,"commit":c.sha,"tree":t.sha,"blob":b.sha,"parent":p,"timestamp":c.timestamp}
        hf.write_text(json.dumps(st, indent=2), encoding="utf-8"); return st
