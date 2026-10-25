"""Regression tests for findings in docs/REVIEW_M01_M07.md (AI self-review)."""
import json, pathlib, re, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
class Review(unittest.TestCase):
    def test_score_run_kinds_equal_schema_enum(self):
        enum = json.loads((ROOT / "schemas/rating.schema.json").read_text(encoding="utf-8"))["properties"]["run_kind"]["enum"]
        src = (ROOT / "src/persian_pronunciation_tts_evaluation/score.py").read_text(encoding="utf-8")
        self.assertEqual(set(re.search(r'not in \(([^)]*)\)', src).group(1).replace('"', "").replace(" ", "").split(",")), set(enum))
    def test_docs_have_no_box_paths(self):
        for p in (ROOT / "docs").glob("*.md"): self.assertNotIn("/workspace/", p.read_text(encoding="utf-8"), p.name)
if __name__ == "__main__": unittest.main()
