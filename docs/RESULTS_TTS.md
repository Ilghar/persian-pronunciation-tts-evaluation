# M06 real-TTS technical baseline (P03)

System: MOSS-TTS-Nano-100M, continuation mode (no voice prompt), CPU float32, `--seed 20261023`, WeTextProcessing off, offline. Pins and licenses: `docs/THIRD_PARTY.md`. Reproduce with `tools/run_moss_tts_nano.py`. Receipt: `tests/receipts/m06_tts_baseline.json`.

| Measure | Result | Denominator |
|---|---|---|
| Generation succeeded (exit 0 + WAV written) | 12 | 12 |
| Bit-identical on seeded rerun | **0** | 12 |
| Duration (s) min / median / max | 1.76 / 3.60 / 6.88 | 12 |
| Seconds per non-space character, min–max | 0.088–0.372 | 12 |
| Items with samples at or above full scale (clipping) | 1 (FA09) | 12 |
| Items with >50% silent 20 ms frames (−40 dBFS) | 1 (FA09) | 12 |
| Wall clock per call incl. model load (s) min / median / max | 4.10 / 5.09 / 6.54 | 12 |

Output: 48 kHz, 2-channel, IEEE float32 WAV.

**Not measured:**
- Pronunciation correctness (error rate denominator = 0): there are no native ratings, and `reference_pronunciation` is null for all items.
- Intelligibility and naturalness.
- Whether the audio is Persian speech at all: nobody has listened to it, Bot included.

The numbers above are signal-level only. They show the pipeline runs on real system output; they are **not** a quality baseline.

Audio is not committed (~9 MB, and the redistribution caveats are in THIRD_PARTY.md). WAVs stay on the shared box at `/workspace/tts/out/{a,b}/`, with per-item sha256 in the receipt.

Next step to get a quality baseline: create a blind packet from these WAVs, have a native speaker rate them, and run `score`.
