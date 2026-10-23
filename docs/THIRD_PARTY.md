# Third-party components (checked 2026-10-23 ~11:25 Europe/Berlin)

Nothing below is vendored into this repo. The adapter only invokes an external checkout; no upstream code, weights or generated audio are committed.

| Component | Pin | License evidence | Size |
|---|---|---|---|
| OpenMOSS/MOSS-TTS-Nano (code) | commit `8b7bcc9341b3b4ef3a3a58ba1338a7d85ff133eb` | GitHub license API: Apache-2.0; root `LICENSE` file is the Apache License 2.0 text | ~ repo only |
| OpenMOSS-Team/MOSS-TTS-Nano-100M (weights) | revision `44502f80dbf9743528fa921cc544d662c685ebec` | Hugging Face model-card metadata `license: apache-2.0`; not gated; **no separate LICENSE file in the HF repo** | 237.8 MB |
| OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano | revision `6aa02b01e445cc585582cf0ba480bc3ea6c8dd68` | HF model-card metadata `license: apache-2.0`; not gated; no separate LICENSE file | 88.1 MB |

Caveats:
- Both READMEs say "follow the root LICENSE … if not yet published, treat as not licensed for redistribution". The code repo's root LICENSE exists (Apache-2.0). For the weights, the only license statement is the card metadata. That is enough for **local evaluation**; redistributing weights or audio would need a closer look and is not done.
- The upstream README lists Persian (`fa`) among its supported languages. Quality for Persian is not claimed by this repo.
- `pytorch_model.bin` is a pickle-format checkpoint from the official org repo. It was loaded with torch 2.7 (default `weights_only` loading). The `trust_remote_code` modules were grep-checked for network, subprocess and exec use before running (none found).
- Run mode: `continuation` with no prompt audio, so no voice cloning of any person.
