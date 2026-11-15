import hashlib, json, time
class WikiObject:
    def digest(self, d: str) -> str: return hashlib.sha256(d.encode("utf-8")).hexdigest()
class Blob(WikiObject):
    def __init__(self, c: str): self.type="blob"; self.content=c; self.sha=self.digest(f"blob:{len(c)}:{c}")
class Tree(WikiObject):
    def __init__(self, e: dict): self.type="tree"; self.entries=e; self.sha=self.digest("tree:"+json.dumps(e,sort_keys=True))
class Commit(WikiObject):
    def __init__(self, t: str, m: str, p: str=None): self.type="commit"; self.tree_sha=t; self.message=m; self.parent=p; self.timestamp=int(time.time()); self.sha=self.digest(f"commit:{t}:{p}:{self.timestamp}:{m}")
