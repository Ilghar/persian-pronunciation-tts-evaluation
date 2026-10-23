# Product contract (M01)

## User
A Persian-speaking reviewer or TTS/G2P practitioner who wants a small, reproducible check of pronunciation-relevant phenomena (ezafe, numerals, register, ZWNJ, code-switching, question intonation) in synthesized or recorded speech.

## Problem
Persian TTS errors are often judged by overall "naturalness". That hides concrete, countable pronunciation failures and confuses subjective prosody with intelligibility. Missing audio or ratings is frequently reported as zero error.

## Bounded scope
- Text/phenomenon schema preserving raw Unicode (incl. ZWNJ U+200C, Persian digits, kasre-ezafe U+0650, hamze U+0654) with a *separate* normalized field — never destructive replacement.
- Pronunciation-review workflow: per-target human judgments (correct / incorrect / uncertain) with reviewer, dialect/register metadata.
- Missing-audio-safe scorer: absent audio or ratings → `not_evaluated`, excluded from denominators and counted separately.
- Reproducible reports. CPU-only, offline. Mock runs labeled `mock` and never counted as a model baseline.

## Non-goals
- No model training/fine-tuning claim, no voice cloning, no paid GPU, no model download by default.
- Starter sentences are not gold; no claimed pronunciation dataset.
- Speaker similarity is not a pronunciation proxy.
- Forked repos are not presented as Ilghar-authored models.

## Acceptance criteria for the finished tool (planned)
1. Raw Persian strings round-trip byte-identically; normalization is a separate field.
2. Missing audio/ratings yields `not_evaluated`, never 0 errors.
3. Mock runs carry `run_kind: mock` and are excluded from baseline tables.
4. Prompt splits prevent duplicate text (after normalization) across splits.
5. Per-target error rate reported with denominators; intelligibility and prosody ratings reported separately; annotator disagreement reported.
6. Latency/RTF only for actually measured runs.
7. Offline; receipts under `tests/receipts/`.

## Data rights and gaps
Only newly drafted text in repo. Any future audio requires consent + license record; no real person's voice supplied. Upstream licenses (MOSS-TTS-Nano, LLM-Powered-G2P) must be checked before any adapter uses them. No repo license chosen yet (M10). Gaps: no native review, no gold pronunciations, no audio.

## Contribution
Ilghar: problem framing, phenomenon selection direction, fork curation. Implementation: AI-assisted (Grok Bot), attributed per commit.
