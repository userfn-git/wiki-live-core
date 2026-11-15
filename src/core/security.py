import hashlib
class SecurityGuard:
    @staticmethod
    def verify_sha(c: str, sha: str) -> bool: return hashlib.sha256(f"blob:{len(c)}:{c}".encode("utf-8")).hexdigest() == sha
    @staticmethod
    def sanitize(t: str) -> str: return t.strip()
