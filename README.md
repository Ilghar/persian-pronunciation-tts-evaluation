A small, reproducible evaluation of Persian pronunciation and expressive TTS, without treating subjective prosody as intelligibility.

This repository is public and still in progress. Synthetic inputs are in use. Real TTS output has been measured at signal level only; there is no pronunciation quality baseline yet.

<p align="center"><a href="https://github.com/Ilghar/persian-pronunciation-tts-evaluation">Repository</a> · <a href="https://ilghar.studio">ilghar.studio</a></p>

## How it's used

Install (M08), offline, no dependencies:

```sh
python3 -m pip install --no-index .   # console script: persian-pronunciation-tts-evaluation
sh examples/run.sh                     # temp venv; check outputs against examples/expected.sha256
```

See `docs/DEPENDENCIES.md`. Quickstart in a fresh environment (Python >= 3.11, no network):

```
git clone <this repo> && cd persian-pronunciation-tts-evaluation
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m persian_pronunciation_tts_evaluation score inputs/starter_sentences.csv fixtures/mock_ratings_m03.json --out out/
```

The fixture uses mock ratings for FA01–FA04 (no audio exists). It checks that mocks are excluded from the baseline. Receipts: `tests/receipts/`.

Vertical slice (M04):

```
PYTHONPATH=src python3 -m persian_pronunciation_tts_evaluation slice inputs/starter_sentences.csv fixtures/mock_blind_ratings_m04.csv --out out/m04
```

Mock tone WAVs are not speech and are never a baseline. No empirical TTS quality baseline exists yet.

## What it checks

Signal-level measures from a real MOSS-TTS-Nano CPU run are in `docs/RESULTS_TTS.md` (12/12 generations succeeded; seeded reruns were not bit-identical; FA09 clipped / was mostly silent). Those numbers are not a pronunciation or quality baseline: nobody has listened to the audio.

## What still fails

- Pronunciation correctness, intelligibility, and naturalness are unmeasured (no native ratings; `reference_pronunciation` is null).
- Seeded reruns are not bit-identical, so ratings must be keyed to audio sha256.
- The item set is small (12), and reference pronunciations are unreviewed.

## How it works

- Tagged source text can go through an optional credited synthesizer, then consented audio or a recorded-output manifest.
- Blind human ratings and timing metadata are meant to feed a reproducible baseline, with limitations stated.
- Longer notes live in `docs/` (`PRODUCT_CONTRACT.md`, `ARCHITECTURE.md`, `RESULTS_TTS.md`, `FAILURE_ANALYSIS.md`). The workflow diagram is `docs/architecture.svg`.

License: not yet chosen.

<sub>ilghar.studio</sub>
