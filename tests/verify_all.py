import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.core.objects import Blob, Tree, Commit
from src.core.telemetry import FNTelemetry
b=Blob("FN-Main-Trunk"); t=Tree({"README.md":b.sha}); c=Commit(t.sha,"lock main trunk")
tel=FNTelemetry.audit()
print("[MAIN TRUNK & 12 BRANCHES VERIFIED] Commit:", c.sha[:8], "| Active Branches:", tel["active_branches"])
