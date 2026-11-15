from src.core.snapshot import YusraSnapshot
from src.cloud.gcp_adapter import CloudAdapter
def handle_request(payload: dict) -> dict:
    st=YusraSnapshot().capture(payload.get("id","SNAP-0001"), payload.get("topic","Init"), payload.get("decisions",[]))
    cloud=CloudAdapter().sync_object("firestore_commits", st["id"], st)
    return {"status":200,"snapshot":st,"cloud":cloud}
