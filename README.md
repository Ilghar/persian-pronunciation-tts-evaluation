# Persian pronunciation and expressive TTS evaluation

**Status: work in progress (private). 3/10 milestones; minimal stdlib tool on synthetic/mock fixtures only — no measured model results.**

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
