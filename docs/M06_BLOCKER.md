# M06 blocked: no actual TTS baseline can be measured without a user decision

M06 requires "measured actual baselines". The pipeline (M04/M05) runs on mock tone audio, which is labelled and excluded from baselines. A real baseline needs at least one of:
1. Running an upstream synthesizer locally (e.g. MOSS-TTS-Nano fork reference) — requires a license check, a model download, CPU time and an explicit OK (brief: no model download/GPU by default).
2. User-recorded or consented audio for FA01–FA12.
3. A native-speaker review pass to fill `reference_pronunciation` and judge outputs.
Until one is chosen, M06 stays `blocked`; no number will be reported.
