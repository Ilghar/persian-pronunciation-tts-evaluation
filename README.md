# Persian pronunciation and expressive TTS evaluation

**Status: work in progress (private). 7/10 milestones (Bot-reviewed); synthetic inputs; real TTS output measured at signal level only.**

- Product contract: `docs/PRODUCT_CONTRACT.md`
- Sources/evidence vs plans: `docs/SOURCES.md`
- Architecture/experiment plan: `docs/ARCHITECTURE.md`, ADR `docs/adr/0001-scope-and-boundaries.md`
- Handoff: `handoff/`

Contribution: Ilghar — problem framing, requirements, evaluation direction. Implementation AI-assisted (Grok Bot). License: not yet chosen.

## Quickstart (fresh environment)
Requires Python >= 3.11, no dependencies, no network.
```
git clone <this repo> && cd persian-pronunciation-tts-evaluation
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m persian_pronunciation_tts_evaluation score inputs/starter_sentences.csv fixtures/mock_ratings_m03.json --out out/
```
Modules: items.py, score.py, cli.py. Fixture: mock ratings for FA01-FA04 (no audio exists); verifies mock exclusion from baseline and not_evaluated accounting. Receipts: `tests/receipts/`.

## Vertical slice (M04)
```
PYTHONPATH=src python3 -m persian_pronunciation_tts_evaluation slice inputs/starter_sentences.csv fixtures/mock_blind_ratings_m04.csv --out out/m04
```
Cleared FA01-FA12 -> phenomenon tags -> MOCK tone WAVs (not speech) + sha256 manifest -> blind packet -> mock ratings ingest -> scorer. Mock run excluded from baseline: NO empirical TTS baseline exists.
Review: `docs/REVIEW_M01_M03.md`.

## Collection and results
- Datasheet: `data/collection_v1/DATASHEET.md`
- Real-TTS baseline: `docs/RESULTS_TTS.md`; third-party licenses: `docs/THIRD_PARTY.md`
- Case page: `docs/CASE_PAGE.md`; static page: `site/index.html` (`python3 tools/export_site.py`); diagram `docs/architecture.mmd` + `docs/architecture.svg`
- Schema validation in code: `src/persian_pronunciation_tts_evaluation/schema.py` (stdlib subset)
- Failure analysis (M07): `docs/FAILURE_ANALYSIS.md`
- Illustration provenance: `assets/ASSETS.json` (image on Drive, not in git)
