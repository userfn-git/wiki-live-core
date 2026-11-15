import json, pathlib
from src.core.objects import Blob, Tree, Commit
class YusraSnapshot:
    def __init__(self, root='docs/snapshots'):
        self.root = pathlib.Path(root); self.root.mkdir(parents=True, exist_ok=True)
    def capture(self, sid: str, topic: str, decisions: list) -> dict:
        md = f'# Yusra Cognitive Snapshot: {sid}\n- Topic: {topic}\n- Branch: PATH02-BR05 & BR06\n## Decisions\n' + '\n'.join([f'- {d}' for d in decisions])
        b_md = Blob(md); b_meta = Blob(json.dumps({'id': sid, 'topic': topic, 'decisions': decisions}))
        tree = Tree({f'{sid}.md': b_md.sha, f'{sid}.json': b_meta.sha})
        head_file = self.root / 'HEAD.json'
        parent = json.loads(head_file.read_text())['commit'] if head_file.exists() else None
        commit = Commit(tree.sha, f'snapshot({sid}): {topic}', parent)
        (self.root / f'{sid}.md').write_text(md, encoding='utf-8')
        state = {'id': sid, 'commit': commit.sha, 'tree': tree.sha, 'blob_md': b_md.sha, 'parent': parent, 'timestamp': commit.timestamp}
        head_file.write_text(json.dumps(state, indent=2), encoding='utf-8')
        return state
