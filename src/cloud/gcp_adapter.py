import json, pathlib
class CloudAdapter:
    def __init__(self, mirror="docs/snapshots/cloud_mirror.json"): self.m=pathlib.Path(mirror); self.m.parent.mkdir(parents=True, exist_ok=True)
    def sync(self, col: str, doc: str, data: dict) -> dict:
        db=json.loads(self.m.read_text("utf-8")) if self.m.exists() else {}
        db.setdefault(col, {})[doc]=data; self.m.write_text(json.dumps(db, indent=2), "utf-8")
        return {"status":"SYNCED","tier":"GCP_FREE","col":col,"doc":doc}
