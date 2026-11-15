import json, pathlib
from src.core.objects import Blob, Tree, Commit
from src.core.yusra_nlp import YusraNLP
class YusraSnapshot:
    def __init__(self, root="docs/snapshots"): self.root=pathlib.Path(root); self.root.mkdir(parents=True, exist_ok=True)
    def capture(self, sid: str, topic: str, decisions: list) -> dict:
        md=YusraNLP.synthesize(f"{sid}: {topic}", decisions); b_md=Blob(md); b_meta=Blob(json.dumps({"id":sid,"topic":topic,"decisions":decisions}))
        tree=Tree({f"{sid}.md":b_md.sha, f"{sid}.json":b_meta.sha}); hf=self.root/"HEAD.json"
        parent=json.loads(hf.read_text(encoding="utf-8"))["commit"] if hf.exists() else None
        c=Commit(tree.sha, f"snapshot({sid}): {topic}", parent); (self.root/f"{sid}.md").write_text(md, encoding="utf-8")
        st={"id":sid,"commit":c.sha,"tree":tree.sha,"blob_md":b_md.sha,"parent":parent,"timestamp":c.timestamp}
        hf.write_text(json.dumps(st, indent=2), encoding="utf-8"); return st
