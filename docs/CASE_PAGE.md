# Persian pronunciation and expressive TTS evaluation

> How can a small reproducible Persian evaluation expose pronunciation, ezafe, numeral, register and code-switching errors without confusing subjective prosody with intelligibility?

**Status:** Pipeline implemented on mock audio; no synthesis results. Private work in progress.

## Problem
How can a small reproducible Persian evaluation expose pronunciation, ezafe, numeral, register and code-switching errors without confusing subjective prosody with intelligibility?

## Existing contribution
Ilghar Dadgostari: problem framing, requirements and evaluation direction. Implementation AI-assisted (Grok Bot), reviewed only by Grok Bot so far.

## Architecture
See `architecture.mmd` (authoritative) and `architecture.svg` (fallback). Stages: Original text + phenomenon tags → Human-reviewed reference pronunciations when available → Optional credited upstream synthesizer adapter → Consented audio or recorded-output manifest → Blind human ratings + timing metadata → Reproducible baseline and limitations

## Example
See README *Vertical slice* and `tests/receipts/`.

## Measured results
- None yet.

## Limitations
- No TTS model has been run; mock tone audio is not speech and is never a baseline.
- Reference pronunciations and spans are unreviewed.
- 12 items; deterministic split gives 11 dev / 1 test, too small for a test claim.

## Next step
See `handoff/NEXT.md`.
