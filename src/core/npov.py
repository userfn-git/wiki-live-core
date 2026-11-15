class NPOVValidator:
    BIAS = ["obviously","undoubtedly","best ever"]
    @classmethod
    def check(cls, text: str) -> dict: v=[w for w in cls.BIAS if w in text.lower()]; return {"npov_compliant": len(v)==0, "violations": v}
