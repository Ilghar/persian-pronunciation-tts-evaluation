# Collection v1 — datasheet
- Version 1.0.0; `python -m persian_pronunciation_tts_evaluation collection . --out DIR`.
- 12 newly drafted items (FA01–FA12), `text_raw` byte-preserved; targets in `targets.json` (Bot-proposed spans, `reference_pronunciation: null`, `unreviewed_bot_proposed_span`). Code checks every span against the raw text.
- Splits by hash of normalized text: 11 dev / 1 test — not meaningful at n=12; treat all as dev until 30–60 reviewed items exist.
- 10 phenomena covered; `heteronym_contrast` not covered (FA01–03 are same-pronunciation controls).
- 0 empirical items, 0 audio items. Rights: new text; no real voices.
