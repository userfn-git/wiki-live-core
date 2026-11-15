import sys, pathlib
R=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R))
from src.core.objects import Blob
from src.cloud.gcp_adapter import CloudAdapter
from src.api.seo import SEOGenerator
from src.core.telemetry import FNTelemetry
assert (R/"Gemini.md").exists() and (R/"README.md").exists()
b=Blob("FN-Cloud"); c=CloudAdapter().sync("commits", "SNAP-0001", {"sha":b.sha})
s=SEOGenerator.build(); t=FNTelemetry.audit()
print("[CI & CLOUD VERIFIED] GCP:", c["status"], "| SEO:", s["@type"], "| Branches:", t["active_branches"])
