# Review of M01–M07

**Type: AI self-review by a separate pass (Grok Bot, 2026-10-25). This is not a human or independent expert review.** The same agent that built M01–M07 wrote this review, so it cannot replace a human reviewer.

## Method
- Fresh copy of `main` rebuilt from the GitHub tree, with every listed blob SHA-1 matching the local tree. The tree listing was truncated at 20 kB, so a few `tools/` files were not compared.
- Full test suite rerun under `PYTHONHASHSEED` = 0, 1 and 12345 with `-W error`, on Python 3.13.5 and, via uv, CPython 3.11.17.
- Every README command rerun. Outputs compared with the committed receipts, and reruns compared with each other to check determinism.
- Every `schemas/*.json` checked with `unsupported_keywords`. Fixtures, inputs and outputs validated against their schemas.
- Grep for leaked emails, tokens, box paths and identifiers. Checked whether blind packets expose item IDs. License notes re-read.

## Common findings
| ID | Severity | Finding | Fix |
|---|---|---|---|
| R-01 | medium | `docs/CASE_PAGE.md` was hand-written and stale against the M06/M07 results. `site/project.json` evidence text was stale too. | `tools/export_site.py` now generates CASE_PAGE.md and index.html from project.json. `tests/test_site.py` fails if either drifts. |
| R-00 | info | README says "Python >= 3.11", which was previously unverified. | Verified: the suite passes on CPython 3.11.17 and 3.13.5. |
| — | ok | The README numbers reproduce exactly. Slice outputs are byte-identical across reruns. No leaked emails, tokens or IDs. Blind packets carry no item IDs. All schemas use only supported keywords. | — |

## Project-specific findings
| ID | Severity | Finding | Fix |
|---|---|---|---|
| R-01b | high (claim contradiction) | The case page and site said "No TTS model has been run" and listed no measured results, which contradicted the M06 MOSS-TTS-Nano run. | Fixed by R-01. The limitations now say the audio was never listened to and pronunciation is unmeasured. |
| R-03 | medium | `score.py` accepted the run_kind values `mock/synthesized/recorded`, but `rating.schema.json` allows `mock/recorded_human/synthesized`. A schema-valid human recording would have been rejected. | Aligned with the schema enum. `tests/test_review.py` pins the two to each other. |
| R-05 | low | `docs/RESULTS_TTS.md` contained a box-specific absolute path. | Replaced with the documented `OUT_DIR_A/OUT_DIR_B` arguments. A test bans absolute box paths in docs. |
| — | info | Historical M03 receipt differs from current output only by the `needs_adjudication` field added in M07. | — |
| — | info | License: MOSS code is Apache-2.0 (LICENSE file). Weights are labelled apache-2.0 only in HF card metadata, with no LICENSE file. Use is local evaluation only and no weights or audio are committed. Unchanged. | — |

## Not covered
No human listening, expert annotation or blind probe authoring took place. Milestone acceptance stays "Bot review only".
