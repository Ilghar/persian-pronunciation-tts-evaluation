import json, pathlib, subprocess, sys, tempfile, unittest, wave
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from persian_pronunciation_tts_evaluation.slice import tag, blind_packet
class Slice(unittest.TestCase):
    def test_tagging(self):
        t = tag("ساعت ۷ است؟ می\u200cروم كتاب"); self.assertEqual((t["zwnj"], t["persian_digits"], t["arabic_yeh_kaf"], t["question"]), (1, 1, 1, False))
    def test_blind_packet_hides_item_ids_and_is_deterministic(self):
        man = [{"item_id": f"FA{i:02}", "path": f"audio/FA{i:02}.wav"} for i in range(1, 6)]
        k1, p1 = blind_packet(man); k2, _ = blind_packet(list(reversed(man)))
        self.assertEqual(k1, k2); self.assertFalse(any("FA" in json.dumps(r) for r in p1))
    def test_end_to_end_mock_never_baseline(self):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, "-m", "persian_pronunciation_tts_evaluation", "slice", "inputs/starter_sentences.csv", "fixtures/mock_blind_ratings_m04.csv", "--out", t], check=True, cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src")}, capture_output=True)
            r = json.loads((pathlib.Path(t) / "report.json").read_text())
            with wave.open(str(pathlib.Path(t) / "blind_audio/B001.wav")) as w: self.assertEqual((w.getnchannels(), w.getframerate()), (1, 8000))
        self.assertEqual(len(r["manifest"]), 12); self.assertTrue(all(m["run_kind"] == "mock" and "NOT SPEECH" in m["label"] for m in r["manifest"]))
        s = r["score"]; self.assertEqual(s["baseline_table"], {})
        run = s["runs"]["mock-tone-m04"]; self.assertFalse(run["eligible_for_baseline"])
        self.assertEqual(run["error_rate"], {"incorrect": 1, "denominator": 1, "value": 1.0})  # B004 -> FA01
        self.assertEqual(run["uncertain"], 1); self.assertEqual(run["not_evaluated_items"], 10)  # B005 blank + 9 unrated; B999 unknown dropped
        self.assertIn("not a synthesis baseline", r["warning"]); self.assertEqual(r["unmatched_blind_ids"], ["B999"])
if __name__ == "__main__": unittest.main()
