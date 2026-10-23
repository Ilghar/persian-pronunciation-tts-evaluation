# Architecture and experiment plan (M02)

Diagram `docs/architecture.mmd`; ADR `docs/adr/0001-scope-and-boundaries.md`.

## Modules (`src/persian_pronunciation_tts_evaluation/`, planned M03)
| Module | Responsibility |
|---|---|
| `items.py` | Load CSV/JSON items; keep `text_raw` byte-identical; validate Persian codepoints (ZWNJ U+200C, Persian digits U+06F0–U+06F9, kasre U+0650, hamze U+0654) |
| `normalize.py` | Optional, *non-destructive* normalized view (separate field) used only for duplicate/split checks |
| `splits.py` | Deterministic split assignment; reject normalized-text duplicates across splits |
| `ratings.py` | Validate rating records; `audio: null` or missing judgments ⇒ `not_evaluated` |
| `score.py` | Per-target error rate = incorrect / judged (uncertain + not_evaluated reported separately); intelligibility and prosody separate; disagreement across reviewers; mock runs excluded from baseline tables |
| `cli.py` | `python -m persian_pronunciation_tts_evaluation score ITEMS RATINGS --out DIR` |
| `adapters/` (later) | Optional credited upstream synthesizer adapter, off by default, after license check |

## Failure cases to cover
ZWNJ dropped or replaced by space; Arabic ي/ك substituted for ی/ک; Persian vs ASCII digits; ezafe explicit vs implicit; missing audio file; ratings without audio; mock run in baseline table; duplicate text across splits; reviewer disagreement; out-of-range rating; latency on a non-measured run.

## Metrics
per-target pronunciation error with denominator (judged targets) plus counts of uncertain and not_evaluated; per-phenomenon breakdown; intelligibility and prosody distributions separately; reviewer disagreement; latency/RTF only for `synthesized` runs with measured timing. No speaker-similarity proxy.

## Deterministic tests
stdlib `unittest`; synthetic mock rating fixture explicitly `run_kind: mock`; canonical JSON outputs; receipts under `tests/receipts/`.

## Dependencies
Python ≥3.11 stdlib (`csv`, `unicodedata`). CPU-only. No audio libraries until a permitted real run (then pinned, inspected).

## License / consent plan
Only newly drafted text. Audio requires consent/synthetic-voice record + sha256. Upstream models/code (MOSS-TTS-Nano, LLM-Powered-G2P) not copied; license check required before adapter use. No voice cloning. Repo license at M10.

## Review
Bot self-review 2026-10-23; Persian-language native review of items and independent technical review pending.

## Implementation status (after M04)
Built: `items.py` (includes normalize + splits), `score.py`, `slice.py` (M04 tagging, MOCK tone synth, blind packet, ingest), `cli.py`. Planned not built: separate `ratings.py`, real synthesizer adapter.
Schemas are documentation + test references; they are not machine-enforced (stdlib, no jsonschema).
