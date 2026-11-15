import json, pathlib
class SEOGenerator:
    @staticmethod
    def build(root="docs/seo") -> dict:
        p=pathlib.Path(root); p.mkdir(parents=True, exist_ok=True)
        jld={"@context":"https://schema.org","@type":"TechArticle","headline":"WikiLife Core","author":{"@type":"Person","name":"Yusra"}}
        (p/"schema.json").write_text(json.dumps(jld, indent=2), "utf-8")
        (p/"sitemap.xml").write_text("<urlset><url><loc>https://fnpro.space/wikilife</loc></url></urlset>", "utf-8"); return jld
