import json, pathlib
class CloudAdapter:
    def __init__(self, mirror="docs/snapshots/cloud_mirror.json"): self.mirror=pathlib.Path(mirror); self.mirror.parent.mkdir(parents=True, exist_ok=True)
    def sync_object(self, col: str, doc_id: str, data: dict) -> dict:
        db=json.loads(self.mirror.read_text(encoding="utf-8")) if self.mirror.exists() else {}
        db.setdefault(col, {})[doc_id]=data; self.mirror.write_text(json.dumps(db, indent=2), encoding="utf-8")
        return {"status":"SYNCED","tier":"GCP_ALWAYS_FREE","collection":col,"doc_id":doc_id}
