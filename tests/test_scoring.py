import json, pathlib, subprocess, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from persian_pronunciation_tts_evaluation.items import load_csv, normalize, assign_splits
class Items(unittest.TestCase):
    def test_raw_text_preserved_including_zwnj(self):
        items = load_csv(ROOT / "inputs/starter_sentences.csv")
        raw = {i["id"]: i["text_raw"] for i in items}
        self.assertIn("\u200c", raw["FA02"]); self.assertEqual(len(items), 12)
        self.assertTrue(all(i["reference_pronunciation"] is None and i["review_status"] == "needs_native_review" for i in items))
    def test_normalized_duplicates_detected_and_split_stable(self):
        its = [{"id": "a", "text_normalized": normalize("میخواهم ۲ كتاب")}, {"id": "b", "text_normalized": normalize("می\u200cخواهم 2 کتاب")}]
        self.assertEqual(assign_splits(its), [["a", "b"]]); self.assertEqual(its[0]["split"], its[1]["split"])
class Scoring(unittest.TestCase):
    def test_mock_excluded_missing_not_evaluated(self):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, "-m", "persian_pronunciation_tts_evaluation", "score", "inputs/starter_sentences.csv", "fixtures/mock_ratings_m03.json", "--out", t], check=True, cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src")}, capture_output=True)
            r = json.loads((pathlib.Path(t) / "report.json").read_text())
        run = r["runs"]["mock-run"]
        self.assertEqual(r["baseline_table"], {}); self.assertFalse(run["eligible_for_baseline"])
        self.assertEqual(run["error_rate"], {"incorrect": 1, "denominator": 3, "value": 0.333333})
        self.assertEqual(run["uncertain"], 1)
        self.assertEqual(run["not_evaluated_items"], 9)  # FA03 no audio + 8 unrated items
        self.assertEqual(r["disagreements"], 1)
        self.assertEqual(sorted(r["errors"]), ["latency on non-measured run mock-run", "prosody out of range FA04"])
if __name__ == "__main__": unittest.main()
