import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.core.objects import Blob
from src.core.security import SecurityGuard
from src.api.handler import handle_request
from src.api.seo import SEOGenerator
from src.core.npov import NPOVValidator
from src.core.telemetry import FNTelemetry
b=Blob("WikiLife-Core"); assert SecurityGuard.verify_sha("WikiLife-Core", b.sha)
res=handle_request({"id":"SNAP-0001","topic":"Full 12-Branch Activation","decisions":["PATH-01..04 Active"]})
SEOGenerator.build(); assert NPOVValidator.check("Neutral technical documentation.")["npov_compliant"]
tel=FNTelemetry.audit()
print("[MASTER BUILD VERIFIED] Branches:", tel["active_branches"], "| Snapshot:", res["snapshot"]["commit"][:8], "| Cloud:", res["cloud"]["status"])
