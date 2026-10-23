"""M05: versioned item collection = raw starter text + Bot-proposed target spans (unreviewed) + splits + rights."""
import hashlib, json, pathlib
from collections import Counter
from .items import load_csv, assign_splits
from .schema import load_schema, validate
def build(root):
    root = pathlib.Path(root); items = load_csv(root / "inputs/starter_sentences.csv"); dups = assign_splits(items)
    tg = {t["item_id"]: t["targets"] for t in json.loads((root / "data/collection_v1/targets.json").read_text(encoding="utf-8"))["items"]}
    s = load_schema(root, "item.schema.json"); errors = []; recs = []
    for it in items:
        targets = tg.get(it["id"], [])
        for t in targets:
            a, b = t["span"]
            if it["text_raw"][a:b] != t["surface"]: errors.append(f"{it['id']}/{t['target_id']}: span does not match surface")
        rec = {"id": it["id"], "text_raw": it["text_raw"], "text_normalized": it["text_normalized"], "phenomena": it["phenomena"],
               "targets": [{k: t[k] for k in ("target_id", "span", "phenomenon", "reference_pronunciation")} for t in targets],
               "dialect": None, "register": "informal" if it["phenomena"][0] == "informal_register" else "formal",
               "review_status": it["review_status"], "source_kind": it["source_kind"], "split": it["split"]}
        errors += [f"{it['id']}: {e}" for e in validate(rec, s)]
        if not targets: errors.append(f"{it['id']}: no targets")
        recs.append(rec)
    return {"collection": "persian-pronunciation-items", "version": "1.0.0", "empirical_items": 0, "audio_items": 0,
            "files": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in ("inputs/starter_sentences.csv", "data/collection_v1/targets.json")},
            "splits": dict(sorted(Counter(r["split"] for r in recs).items())), "phenomena": dict(sorted(Counter(r["phenomena"][0] for r in recs).items())),
            "normalized_duplicates": dups, "reference_pronunciations_present": sum(1 for r in recs for t in r["targets"] if t["reference_pronunciation"]),
            "rights": "newly drafted text (Drive DATA_REVIEW); no audio, no real voices", "review": "needs_native_review for all items and spans",
            "edge_cases_covered": sorted({r["phenomena"][0] for r in recs}), "items": recs, "errors": errors}
