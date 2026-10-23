"""Reproduce the M06 real-TTS baseline (NOT run in CI/tests: needs a venv with torch and ~310 MB weights).
Pins: code OpenMOSS/MOSS-TTS-Nano@8b7bcc9341b3b4ef3a3a58ba1338a7d85ff133eb (Apache-2.0, LICENSE file);
weights OpenMOSS-Team/MOSS-TTS-Nano-100M@44502f80dbf9743528fa921cc544d662c685ebec and
OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano@6aa02b01e445cc585582cf0ba480bc3ea6c8dd68 (model-card license: apache-2.0).
Run from the MOSS-TTS-Nano checkout with HF_HUB_OFFLINE=1:
  python infer.py --checkpoint MODELS/MOSS-TTS-Nano --audio-tokenizer-pretrained-name-or-path MODELS/MOSS-Audio-Tokenizer-Nano \
    --mode continuation --text TEXT --device cpu --dtype float32 --seed 20261023 --disable-wetext-processing --output-audio-path OUT/ID.wav
Then: python3 tools/run_moss_tts_nano.py measure OUT_DIR_A OUT_DIR_B > tests/receipts/m06_tts_baseline.json"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from persian_pronunciation_tts_evaluation import audio_stats, items
def measure(a, b):
    root = pathlib.Path(__file__).resolve().parents[1]
    its = {i["id"]: i["text_raw"] for i in items.load_csv(root / "inputs/starter_sentences.csv")}
    pa = {k: audio_stats.stats(pathlib.Path(a) / f"{k}.wav") for k in its}
    pb = {k: audio_stats.stats(pathlib.Path(b) / f"{k}.wav")["sha256"] for k in its}
    return {"system": "MOSS-TTS-Nano-100M continuation mode (no voice prompt), CPU float32, seed 20261023",
            "generated": f"{len(pa)}/{len(its)}", "deterministic_rerun_identical": f"{sum(pa[k]['sha256'] == pb[k] for k in its)}/{len(its)}",
            "per_item": pa, "summary": audio_stats.summarize(pa, its),
            "not_measured": ["pronunciation correctness (needs native listener; reference_pronunciation is null)", "intelligibility/ASR", "naturalness/MOS"],
            "audio_committed": False, "audio_note": "WAVs kept off-repo on the box (~9 MB); sha256 per item recorded for verification."}
if __name__ == "__main__" and sys.argv[1] == "measure": print(json.dumps(measure(sys.argv[2], sys.argv[3]), indent=1, ensure_ascii=False))
