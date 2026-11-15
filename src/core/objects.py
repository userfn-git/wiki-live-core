import hashlib, json, time
class WikiObject:
    def digest(self, data: str) -> str: return hashlib.sha256(data.encode('utf-8')).hexdigest()
class Blob(WikiObject):
    def __init__(self, content: str):
        self.type = 'blob'; self.content = content; self.sha = self.digest(f'blob:{len(content)}:{content}')
class Tree(WikiObject):
    def __init__(self, entries: dict):
        self.type = 'tree'; self.entries = entries; raw = json.dumps(entries, sort_keys=True); self.sha = self.digest(f'tree:{raw}')
class Commit(WikiObject):
    def __init__(self, tree_sha: str, message: str, parent: str = None):
        self.type = 'commit'; self.tree_sha = tree_sha; self.message = message; self.parent = parent; self.timestamp = int(time.time()); self.sha = self.digest(f'commit:{tree_sha}:{parent}:{self.timestamp}:{message}')
