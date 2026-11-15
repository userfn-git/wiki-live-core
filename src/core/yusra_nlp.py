class YusraNLP:
    GLOSSARY = {"Blob":"كائن ثنائي","Tree":"شجرة مسارات","Commit":"التزام مرجعي","Snapshot":"لقطة معرفية"}
    @classmethod
    def synthesize(cls, title: str, items: list) -> str: return f"# [Yusra Synthesis] {title}\n" + "\n".join([f"- {i}" for i in items])
