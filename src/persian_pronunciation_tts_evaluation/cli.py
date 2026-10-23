import argparse, hashlib, json, pathlib, sys
from .items import load_csv, assign_splits
from .score import score
def main(argv=None):
    ap = argparse.ArgumentParser(prog="persian_pronunciation_tts_evaluation"); ap.add_argument("cmd", choices=["score","slice","collection","failure"])
    ap.add_argument("items"); ap.add_argument("ratings", nargs="?"); ap.add_argument("--out", required=True); a = ap.parse_args(argv)
    if a.cmd == "failure":
        from .failure import run as frun, analyze_real_run
        rep = {"adversarial": frun(), "real_run": analyze_real_run(pathlib.Path(a.items) / "tests/receipts/m06_tts_baseline.json")}
        o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
        (o / "failure.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        print(json.dumps({"passed": f'{rep["adversarial"]["passed"]}/{rep["adversarial"]["n"]}', "flagged": rep["real_run"]["flagged_items"]})); return 0 if rep["adversarial"]["passed"] == rep["adversarial"]["n"] else 1
    if a.cmd == "collection":
        from .collection import build
        m = build(a.items); o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
        (o / "manifest.json").write_text(json.dumps(m, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        print(json.dumps({k: m[k] for k in ("splits", "errors", "reference_pronunciations_present", "normalized_duplicates")})); return 1 if m["errors"] else 0
    items = load_csv(a.items)
    if a.cmd == "slice":
        import csv
        from .slice import run
        res = run(items, a.out, pathlib.Path(a.ratings).read_text(encoding="utf-8") if a.ratings else None); o = pathlib.Path(a.out)
        with open(o / "blind_packet.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(res["packet"][0])); w.writeheader(); w.writerows(res.pop("packet"))
        (o / "blind_key.json").write_text(json.dumps(res.pop("blind_key"), indent=1) + "\n")
        (o / "report.json").write_text(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        print(json.dumps({"items": len(items), "audio": len(res["manifest"]), "baseline_runs": list(res["score"]["baseline_table"]), "warning": res["warning"]}, ensure_ascii=False)); return 0
    dups = assign_splits(items); rraw = pathlib.Path(a.ratings).read_bytes()
    rep = {"items_sha256": hashlib.sha256(pathlib.Path(a.items).read_bytes()).hexdigest(), "ratings_sha256": hashlib.sha256(rraw).hexdigest(),
           "n_items": len(items), "normalized_duplicates": dups, **score(items, json.loads(rraw)["ratings"])}
    o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
    (o / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    (o / "items.json").write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"n_items": len(items), "baseline_runs": list(rep["baseline_table"]), "errors": len(rep["errors"])})); return 0
if __name__ == "__main__": sys.exit(main())
