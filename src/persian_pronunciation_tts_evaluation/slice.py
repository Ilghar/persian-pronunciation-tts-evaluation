"""M04 vertical slice: cleared starter sentences -> text-phenomenon tagging -> MOCK synthesizer (tones, NOT speech)
-> audio manifest with sha256 -> blind rating packet (CSV) -> ratings ingest -> scorer.
MOCK AUDIO IS NOT A TTS BASELINE: run_kind='mock' is excluded from baseline tables by the scorer."""
import csv, hashlib, io, json, math, pathlib, random, struct, wave
from .score import score
def tag(text):
    return {"zwnj": text.count("\u200c"), "persian_digits": sum("\u06f0" <= c <= "\u06f9" for c in text),
            "ascii_digits": sum(c.isascii() and c.isdigit() for c in text), "arabic_yeh_kaf": sum(c in "\u064a\u0643" for c in text),
            "question": text.rstrip().endswith("؟"), "latin": sum(c.isascii() and c.isalpha() for c in text)}
def mock_wav(text, rate=8000):
    n = int(rate * (0.3 + 0.05 * len(text))); f = 220 + (int(hashlib.sha256(text.encode()).hexdigest(), 16) % 200)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(b"".join(struct.pack("<h", int(8000 * math.sin(2 * math.pi * f * i / rate))) for i in range(n)))
    return buf.getvalue()
def synthesize_mock(items, outdir):
    out = pathlib.Path(outdir) / "audio"; out.mkdir(parents=True, exist_ok=True); manifest = []
    for it in items:
        b = mock_wav(it["text_raw"]); p = out / f"{it['id']}.wav"; p.write_bytes(b)
        manifest.append({"item_id": it["id"], "path": f"audio/{it['id']}.wav", "sha256": hashlib.sha256(b).hexdigest(), "run_kind": "mock",
                         "system": {"name": "mock-tone-generator", "revision": "m04", "license_checked": True}, "consent": "synthetic_voice", "label": "MOCK TONE - NOT SPEECH"})
    return manifest
def blind_packet(manifest, seed=20261023):
    rows = sorted(manifest, key=lambda m: m["item_id"]); random.Random(seed).shuffle(rows)
    key = {f"B{i:03}": m["item_id"] for i, m in enumerate(rows, 1)}
    return key, [{"blind_id": b, "audio": f"blind_audio/{b}.wav", "verdict": "", "intelligibility": "", "prosody": "", "reviewer_id": ""} for b, m in zip(key, rows)]
def ingest(rating_csv, key, manifest, run_id="mock-tone-m04"):
    man = {m["item_id"]: m for m in manifest}; recs = []; unmatched = []
    for r in csv.DictReader(io.StringIO(rating_csv)):
        iid = key.get(r["blind_id"])
        if iid is None: unmatched.append(r["blind_id"]); continue
        v = r["verdict"].strip(); toint = lambda x: int(x) if x.strip().isdigit() else None
        recs.append({"item_id": iid, "run_id": run_id, "run_kind": "mock", "reviewer_id": r["reviewer_id"] or "unknown",
                     "audio": {"path": man[iid]["path"], "sha256": man[iid]["sha256"], "consent": "synthetic_voice"},
                     "target_judgments": [{"target_id": "t1", "verdict": v}] if v in ("correct", "incorrect", "uncertain") else [],
                     "intelligibility": toint(r["intelligibility"]), "prosody": toint(r["prosody"])})
    return recs, unmatched
def run(items, outdir, rating_csv=None):
    tags = {i["id"]: tag(i["text_raw"]) for i in items}
    manifest = synthesize_mock(items, outdir); key, packet = blind_packet(manifest)
    bd = pathlib.Path(outdir) / "blind_audio"; bd.mkdir(exist_ok=True)
    for b, iid in key.items(): (bd / f"{b}.wav").write_bytes((pathlib.Path(outdir) / f"audio/{iid}.wav").read_bytes())
    recs, unmatched = ingest(rating_csv, key, manifest) if rating_csv else ([], [])
    return {"tags": tags, "manifest": manifest, "blind_key": key, "packet": packet, "score": score(items, recs), "unmatched_blind_ids": unmatched,
            "warning": "MOCK tone audio; no TTS model run; results are pipeline checks, not a synthesis baseline"}
