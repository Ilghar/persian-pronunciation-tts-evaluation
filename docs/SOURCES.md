# Source and access register (M01)

Machine-readable: `inputs/source_register.jsonl`.

## Existing evidence
| ID | What | Status |
|---|---|---|
| S01 | 12 newly drafted Persian starter sentences (FA01–FA12) with phenomenon tags | In repo. **Unreviewed scaffolding, not gold.** Pronunciation/audio blank = *not evaluated*, never zero error. |
| S02 | Data review note: FA01–03 (شیر) are same-pronunciation semantic-homonym controls | Summarized; not heteronym evidence. |
| S03/S04 | Forks `Ilghar/MOSS-TTS-Nano`, `Ilghar/LLM-Powered-G2P` | Curated forks, reported **0 commits ahead** at inspection; upstream-authored; not Ilghar's models. Not re-inspected in this session. |
| S05/S06 | HF profile / HF audio course | References only. |

No model weights, audio, training checkpoint or measured synthesis baseline exists. Upstream code/models/data are **not copied**; licenses unreviewed.

## Access actually used (2026-10-23, Europe/Berlin)
Drive project-03 folder read via connector (all files except `.DS_Store`; `source_register.jsonl` was empty). GitHub `Ilghar` verified; repo private. Grok Library search unavailable (S07). No model download, no GPU, no audio.

## Plans
Everything in `docs/PRODUCT_CONTRACT.md` acceptance criteria and `docs/ARCHITECTURE.md` is planned until code + receipts exist.
