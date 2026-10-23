import json, pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from persian_pronunciation_tts_evaluation.collection import build
from persian_pronunciation_tts_evaluation.schema import validate, load_schema
class Collection(unittest.TestCase):
    def test_collection_valid_spans_match_and_unreviewed(self):
        m = build(ROOT); self.assertEqual(m["errors"], []); self.assertEqual(len(m["items"]), 12)
        self.assertEqual(m["reference_pronunciations_present"], 0); self.assertEqual(m["audio_items"], 0); self.assertEqual(m["empirical_items"], 0)
        fa04 = next(i for i in m["items"] if i["id"] == "FA04"); a, b = fa04["targets"][0]["span"]
        self.assertEqual(fa04["text_raw"][a:b], "کتابِ"); self.assertIn("\u0650", fa04["text_raw"])
        self.assertEqual(len(m["edge_cases_covered"]), 10); self.assertNotIn("heteronym_contrast", m["edge_cases_covered"])  # schema enum has 11; true heteronyms await native review
    def test_item_schema_rejects_bad_records(self):
        s = load_schema(ROOT, "item.schema.json"); m = build(ROOT); good = m["items"][0]
        self.assertEqual(validate(good, s), [])
        self.assertTrue(validate(dict(good, id="X1"), s)); self.assertTrue(validate(dict(good, phenomena=["made_up"]), s))
        self.assertTrue(validate(dict(good, targets=[{"target_id": "t", "span": [1], "phenomenon": "x"}]), s))
    def test_span_mismatch_detected(self):
        import shutil, tempfile
        with tempfile.TemporaryDirectory() as t:
            for d in ("inputs", "schemas", "data"): shutil.copytree(ROOT / d, pathlib.Path(t) / d)
            p = pathlib.Path(t) / "data/collection_v1/targets.json"; d = json.loads(p.read_text()); d["items"][0]["targets"][0]["span"] = [0, 2]; p.write_text(json.dumps(d))
            self.assertTrue(any("span does not match" in e for e in build(t)["errors"]))
if __name__ == "__main__": unittest.main()
