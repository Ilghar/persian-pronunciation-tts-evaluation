# ADR 0001 — Scope and boundaries
Status: accepted (internal self-review, 2026-10-23); independent review pending.

## Decision
- Build an original evaluation layer, not a TTS model; upstream forks remain references.
- `text_raw` is immutable; normalization lives in a separate field.
- Missing audio/ratings ⇒ `not_evaluated`, excluded from error denominators and reported separately.
- `run_kind: mock` records can exercise code paths but never appear in baseline tables.
- CPU-only, offline, stdlib; no model download, GPU or voice cloning by default.
- Starter sentences stay `needs_native_review`; no gold until reviewed.

## Consequences
No synthesis-quality number exists until a real permitted run with consented/synthetic audio and human ratings.
