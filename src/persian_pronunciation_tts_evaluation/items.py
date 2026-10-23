"""Load items keeping text_raw byte-identical; normalized view is separate and derived."""
import csv, hashlib, unicodedata
def normalize(s):
    s = unicodedata.normalize("NFC", s).replace("\u064a", "\u06cc").replace("\u0643", "\u06a9")
    s = s.translate({0x06F0 + i: 0x30 + i for i in range(10)} | {0x0660 + i: 0x30 + i for i in range(10)})
    return " ".join(s.replace("\u200c", "").split())
def load_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [{"id": r["id"], "text_raw": r["text"], "text_normalized": normalize(r["text"]), "phenomena": [r["phenomenon"]],
                 "review_status": r["review_status"], "source_kind": r["source_kind"],
                 "reference_pronunciation": r["gold_pronunciation"] or None} for r in csv.DictReader(f)]
def assign_splits(items, test_fraction_mod=4):
    """Deterministic: hash of normalized text; duplicates share a split and are flagged."""
    seen, dups = {}, []
    for it in items:
        k = it["text_normalized"]
        if k in seen: dups.append([seen[k], it["id"]])
        else: seen[k] = it["id"]
        it["split"] = "test" if int(hashlib.sha256(k.encode()).hexdigest(), 16) % test_fraction_mod == 0 else "dev"
    return dups
