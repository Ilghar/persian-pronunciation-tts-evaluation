"""Score target judgments. Missing audio/judgments => not_evaluated; mock runs never in baselines."""
from collections import Counter, defaultdict
def score(items, ratings):
    phen = {i["id"]: i["phenomena"][0] for i in items}
    per_run = defaultdict(lambda: {"incorrect": 0, "correct": 0, "uncertain": 0, "not_evaluated": 0, "by_phenomenon": defaultdict(Counter), "kind": None})
    disagreement = defaultdict(set); errors = []
    rated = defaultdict(set); seen = set()
    VERDICTS = {"correct", "incorrect", "uncertain"}
    for r in ratings:
        if not isinstance(r, dict) or r.get("run_kind") not in ("mock", "synthesized", "recorded"):
            errors.append(f"missing/invalid run_kind on rating {r.get('item_id') if isinstance(r, dict) else r!r}"); continue
        run = per_run[r["run_id"]]; run["kind"] = r["run_kind"]
        if r.get("item_id") not in phen: errors.append(f"unknown item {r.get('item_id')}"); continue
        dk = (r["run_id"], r["item_id"], r.get("reviewer_id"))
        if dk in seen: errors.append(f"duplicate rating by reviewer {r.get('reviewer_id')} on {r['item_id']} (first kept)"); continue
        seen.add(dk)
        for k in ("intelligibility", "prosody"):
            v = r.get(k)
            if v is not None and (isinstance(v, bool) or not (isinstance(v, int) and 1 <= v <= 5)): errors.append(f"{k} out of range {r['item_id']}")
        js = r.get("target_judgments") or []
        bad = [j for j in js if not isinstance(j, dict) or j.get("verdict") not in VERDICTS]
        if bad: errors.append(f"invalid target judgment/verdict on {r['item_id']}: {bad!r}"); r = dict(r, target_judgments=[j for j in js if j not in bad])
        if r.get("latency_seconds") is not None and r["run_kind"] != "synthesized": errors.append(f"latency on non-measured run {r['run_id']}")
        rated[r["run_id"]].add(r["item_id"])
        if r.get("audio") is None or not r.get("target_judgments"):
            run["not_evaluated"] += 1; continue
        for j in r["target_judgments"]:
            run[j["verdict"]] += 1; run["by_phenomenon"][phen[r["item_id"]]][j["verdict"]] += 1
            disagreement[(r["run_id"], r["item_id"], j["target_id"])].add(j["verdict"])
    out = {}
    for rid, run in sorted(per_run.items()):
        run["not_evaluated"] += len(set(phen) - rated[rid])
        judged = run["correct"] + run["incorrect"]
        out[rid] = {"run_kind": run["kind"], "eligible_for_baseline": run["kind"] != "mock",
                    "error_rate": {"incorrect": run["incorrect"], "denominator": judged, "value": None if judged == 0 else round(run["incorrect"] / judged, 6)},
                    "uncertain": run["uncertain"], "not_evaluated_items": run["not_evaluated"],
                    "by_phenomenon": {k: dict(sorted(v.items())) for k, v in sorted(run["by_phenomenon"].items())}}
    baseline = {k: v for k, v in out.items() if v["eligible_for_baseline"]}
    return {"runs": out, "baseline_table": baseline, "disagreements": sum(1 for v in disagreement.values() if {"correct", "incorrect"} <= v),
            "needs_adjudication": sum(1 for v in disagreement.values() if len(v) > 1), "errors": errors}
