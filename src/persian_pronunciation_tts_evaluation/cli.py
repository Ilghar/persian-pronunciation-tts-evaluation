import argparse, hashlib, json, pathlib, sys
from .items import load_csv, assign_splits
from .score import score
def main(argv=None):
    ap = argparse.ArgumentParser(prog="persian_pronunciation_tts_evaluation"); ap.add_argument("cmd", choices=["score"])
    ap.add_argument("items"); ap.add_argument("ratings"); ap.add_argument("--out", required=True); a = ap.parse_args(argv)
    items = load_csv(a.items); dups = assign_splits(items); rraw = pathlib.Path(a.ratings).read_bytes()
    rep = {"items_sha256": hashlib.sha256(pathlib.Path(a.items).read_bytes()).hexdigest(), "ratings_sha256": hashlib.sha256(rraw).hexdigest(),
           "n_items": len(items), "normalized_duplicates": dups, **score(items, json.loads(rraw)["ratings"])}
    o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
    (o / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    (o / "items.json").write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"n_items": len(items), "baseline_runs": list(rep["baseline_table"]), "errors": len(rep["errors"])})); return 0
if __name__ == "__main__": sys.exit(main())
