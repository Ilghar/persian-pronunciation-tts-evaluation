# M07 failure analysis (Bot-authored, not independently reviewed)

Reproduce: `PYTHONPATH=src python3 -m persian_pronunciation_tts_evaluation failure . --out out/m07` (receipt `tests/receipts/m07_failure.json`).

## Adversarial / malformed inputs (21 rows: score 9, rating ingest 5, audio reader 7)
| Code version | Passed |
|---|---|
| before M07 fixes (commit c98240e + M06 audio reader) | 10/21 (`tests/receipts/m07_prefix_run.json`) |
| M07 | 21/21 |

Fixed:
- **`score`:**
  - A bool rating was accepted.
  - An unknown verdict, a non-dict judgment, or a missing `run_kind` **crashed** it.
  - A duplicate rating from the same reviewer on the same item was double-counted.
  - New `needs_adjudication` counts any split verdict (e.g. correct vs uncertain). `disagreements` (correct vs incorrect) is kept.
- **`ingest`:**
  - `" Correct "` was silently dropped as no judgment; it is now normalized.
  - A missing `reviewer_id` column **crashed** it.
  - Persian digits were already handled and are now tested.
- **Audio reader:**
  - A truncated fmt chunk raised a raw `struct.error`.
  - Empty data produced stats from zero frames.
  - Both now raise `ValueError`.

## Analysis of the real M06 run
- **Nondeterminism:** 0/12 items were bit-identical across seeded CPU reruns. Ratings must therefore be keyed to the audio sha256, which the blind packet already records. The upstream code is not patched.
- **FA09** (longest text): clipping, peak above full scale and 69% silent frames. It must be listened to before any verdict.
- These are signal flags, not pronunciation errors. No pronunciation failure analysis is possible without ratings.
