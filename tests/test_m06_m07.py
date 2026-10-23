import json, pathlib, struct, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from persian_pronunciation_tts_evaluation import failure, audio_stats
class M06(unittest.TestCase):
    def test_receipt_is_real_run_with_denominators_and_no_quality_claim(self):
        d = json.loads((ROOT / "tests/receipts/m06_tts_baseline.json").read_text(encoding="utf-8"))
        self.assertEqual(d["generated"], "12/12"); self.assertEqual(len(d["per_item"]), 12)
        self.assertFalse(d["audio_committed"]); self.assertTrue(any("pronunciation" in x for x in d["not_measured"]))
        self.assertTrue(all(len(v["sha256"]) == 64 and v["sample_rate"] == 48000 for v in d["per_item"].values()))
    def test_reader_float32_and_pcm16_agree_on_duration(self):
        for tag, bits, data in ((1, 16, b"\x00\x40" * 800), (3, 32, struct.pack("<800f", *([0.5] * 800)))):
            p = failure._wav(tag, bits, data=data)
            with self.subTest(tag=tag): s = audio_stats.stats(p); self.assertEqual(s["duration_s"], 0.1); self.assertAlmostEqual(s["rms_dbfs"], -6.02, places=1)
            pathlib.Path(p).unlink()
class M07(unittest.TestCase):
    def test_adversarial_suite_all_pass(self):
        r = failure.run(); self.assertEqual(r["passed"], r["n"], [x for x in r["rows"] if not x["pass"]])
    def test_real_run_analysis(self):
        a = failure.analyze_real_run(ROOT / "tests/receipts/m06_tts_baseline.json")
        self.assertEqual(a["determinism"], "0/12"); self.assertIn("FA09", a["flagged_items"])
if __name__ == "__main__": unittest.main()
