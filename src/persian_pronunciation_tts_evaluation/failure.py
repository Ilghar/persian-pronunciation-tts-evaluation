"""M07: adversarial/malformed inputs for scoring, rating ingest and audio measurement, plus analysis of the real M06 run."""
import io, json, pathlib, struct, tempfile
from . import score as sc, slice as sl, audio_stats as au
ITEMS = [{"id": "FA01", "phenomena": ["p"]}, {"id": "FA02", "phenomena": ["p"]}]
def R(item="FA01", rid="r1", verdict="correct", **kw):
    return dict({"item_id": item, "run_id": "real", "run_kind": "synthesized", "reviewer_id": rid, "audio": {"path": "x"}, "target_judgments": [{"target_id": "t1", "verdict": verdict}]}, **kw)
def _wav(tag=1, bits=16, ch=1, sr=8000, data=b"\x00\x00" * 80, truncate=False):
    fmt = struct.pack("<HHIIHH", tag, ch, sr, sr * ch * bits // 8, ch * bits // 8, bits)
    b = b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE" + b"fmt " + struct.pack("<I", 16) + fmt + b"data" + struct.pack("<I", len(data)) + data
    f = tempfile.NamedTemporaryFile(suffix=".wav", delete=False); f.write(b[:30] if truncate else b); f.close(); return f.name
SCORE = [  # (name, ratings, predicate)
    ("clean", [R()], lambda o: o["runs"]["real"]["error_rate"]["denominator"] == 1 and not o["errors"]),
    ("bool_intelligibility_rejected", [R(intelligibility=True)], lambda o: any("intelligibility" in e for e in o["errors"])),
    ("unknown_verdict_rejected", [R(verdict="maybe")], lambda o: any("verdict" in e for e in o["errors"]) and o["runs"]["real"]["error_rate"]["denominator"] == 0),
    ("judgment_not_dict_no_crash", [R(target_judgments=["correct"])], lambda o: any("judgment" in e for e in o["errors"])),
    ("missing_run_kind_no_crash", [{k: v for k, v in R().items() if k != "run_kind"}], lambda o: any("run_kind" in e for e in o["errors"])),
    ("duplicate_reviewer_rejected", [R(), R(verdict="incorrect")], lambda o: any("duplicate" in e for e in o["errors"]) and o["runs"]["real"]["error_rate"]["denominator"] == 1),
    ("two_reviewers_disagree_counted", [R(), R(rid="r2", verdict="incorrect")], lambda o: o["disagreements"] == 1 and o["needs_adjudication"] == 1),
    ("correct_vs_uncertain_adjudication", [R(), R(rid="r2", verdict="uncertain")], lambda o: o["disagreements"] == 0 and o["needs_adjudication"] == 1),
    ("mock_never_baseline", [R(run_kind="mock")], lambda o: o["baseline_table"] == {}),
]
CSV_H = "blind_id,verdict,intelligibility,prosody,reviewer_id\n"
KEY = {"B001": "FA01"}; MAN = [{"item_id": "FA01", "path": "a.wav", "sha256": "0" * 64}]
INGEST = [
    ("ingest_clean", CSV_H + "B001,correct,4,3,r1\n", lambda recs, un: len(recs) == 1 and recs[0]["target_judgments"]),
    ("ingest_verdict_case_whitespace", CSV_H + "B001, Correct ,4,3,r1\n", lambda recs, un: recs[0]["target_judgments"] == [{"target_id": "t1", "verdict": "correct"}]),
    ("ingest_persian_digits", CSV_H + "B001,correct,۴,۳,r1\n", lambda recs, un: recs[0]["intelligibility"] == 4 and recs[0]["prosody"] == 3),
    ("ingest_missing_reviewer_column_no_crash", "blind_id,verdict,intelligibility,prosody\nB001,correct,4,3\n", lambda recs, un: recs[0]["reviewer_id"] == "unknown"),
    ("ingest_unknown_blind_id_reported", CSV_H + "B999,correct,4,3,r1\n", lambda recs, un: un == ["B999"] and not recs),
]
AUDIO = [  # (name, path factory, expect: "ok" | "error")
    ("pcm16_ok", lambda: _wav(), "ok"), ("float32_ok", lambda: _wav(3, 32, data=struct.pack("<80f", *([0.5] * 80))), "ok"),
    ("pcm8_rejected", lambda: _wav(1, 8, data=b"\x80" * 80), "error"), ("truncated_rejected", lambda: _wav(truncate=True), "error"),
    ("not_wav_rejected", lambda: (lambda f: (f.write(b"ID3...."), f.close(), f.name)[2])(tempfile.NamedTemporaryFile(delete=False)), "error"),
    ("empty_data_no_crash", lambda: _wav(data=b""), "error"),
    ("float_over_full_scale_flagged", lambda: _wav(3, 32, data=struct.pack("<4f", 1.5, -1.2, 0.1, 0.0)), "clip"),
]
def _try(f):
    try: return f(), None
    except Exception as e: return None, f"{type(e).__name__}: {e}"
def run():
    rows = []
    for name, rs, pred in SCORE:
        o, err = _try(lambda: sc.score(ITEMS, rs)); ok = False
        if o is not None: ok, err2 = _try(lambda: bool(pred(o))); ok = bool(ok); err = err or err2
        rows.append({"group": "score", "name": name, "exception": err, "pass": ok})
    for name, csv_text, pred in INGEST:
        o, err = _try(lambda: sl.ingest(csv_text, KEY, MAN)); ok = False
        if o is not None: ok, err2 = _try(lambda: bool(pred(*o))); ok = bool(ok); err = err or err2
        rows.append({"group": "ingest", "name": name, "exception": err, "pass": ok})
    for name, mk, exp in AUDIO:
        p = mk(); o, err = _try(lambda: au.stats(p)); pathlib.Path(p).unlink()
        ok = (exp == "error" and isinstance(err, str) and err.startswith("ValueError")) or (exp == "ok" and o is not None) or (exp == "clip" and o is not None and o["clipped_samples"] == 2)
        rows.append({"group": "audio", "name": name, "exception": err, "pass": ok})
    return {"n": len(rows), "passed": sum(r["pass"] for r in rows), "rows": rows}
def analyze_real_run(receipt):
    d = json.loads(pathlib.Path(receipt).read_text(encoding="utf-8")); pi = d["per_item"]
    flags = {k: [f for f, c in (("clipping", v["clipped_samples"] > 0), ("mostly_silent", v["silent_frame_fraction"] > 0.5), ("over_full_scale", v["peak_abs"] > 1.0)) if c] for k, v in pi.items()}
    return {"source": pathlib.Path(receipt).name, "determinism": d["deterministic_rerun_identical"], "flagged_items": {k: v for k, v in flags.items() if v},
            "diagnosis": ["Seeded CPU reruns produced different bytes for every item: the upstream pipeline is not bit-reproducible with --seed alone, so any score must be tied to the exact audio sha256, not to the command.",
                          "Items flagged by objective audio checks need listening before any pronunciation verdict; the flags are not pronunciation errors."],
            "not_fixed": "Upstream nondeterminism is not patched here (would modify third-party code); recorded as a limitation."}
