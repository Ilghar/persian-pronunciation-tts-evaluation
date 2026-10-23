# Review of M01–M03

## Reviewer and method
Second-pass skeptical review by Grok Bot on 2026-10-23, done in a separate pass against `common/MILESTONES.json`. **This is not independent human review**; that remains pending and is required before any external claim.

## Verdicts
| Milestone | Verdict | Notes |
|---|---|---|
| M01 | accepted | Register separates evidence vs plans; contract has user/problem/non-goals/criteria/rights. |
| M02 | accepted with caveat | Schemas, failure cases, test strategy, deps, license plan and ADR are substantive. "Reviewed" is satisfied only by Bot review. |
| M03 | accepted after fixes | Fresh-env instructions, CLI, synthetic fixture, tests with receipts verified by re-running in a clean copy. |

## Findings common to all three
- F1: ARCHITECTURE listed modules (e.g. `schema.py`) that were never built and JSON schemas are **not enforced by code**; fixed by adding an implementation-status section. Schema enforcement stays a gap.
- F2: M01–M03 acceptance was self-review only; recorded here; no upgrade to "independently reviewed".

## Project-specific findings
- F3 (fixed in M04): first blind-packet draft leaked item IDs through audio filenames; now uses blind-ID copies, test asserts no `FA` in packet.
- F4 (fixed): unknown blind IDs in ratings were silently dropped; now reported as `unmatched_blind_ids`.
- F5 (documented): starter phenomena match the item schema enum (checked); targets/spans and reference pronunciations are absent pending native review, so per-target scoring uses a single placeholder target `t1`.
