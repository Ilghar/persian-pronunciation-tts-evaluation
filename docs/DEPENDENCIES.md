# Dependencies (M08)

- **Runtime:** none. Python standard library only. `requires-python = ">=3.11"`, verified on CPython 3.11.17 and 3.13.5 (`tests/receipts/m08_run.json`).
- **Build:** none. `pyproject.toml` uses the in-tree stdlib backend `_build/backend.py` with `requires = []`, so `pip install --no-index .` works offline. The wheel is byte-reproducible (tested).
- **Lock:** with zero third-party packages there is nothing to lock. The empty lists are pinned by `tests/test_package.py`.
- **Install:** `python3 -m pip install --no-index .` installs the `persian-pronunciation-tts-evaluation` console script. Inputs and fixtures stay in the repo, and schemas ship inside the wheel.
- **Reproducible example:** `sh examples/run.sh` installs into a throwaway venv, reruns the README commands with the installed script, and checks the outputs against `examples/expected.sha256`.
- **CI:** not enabled. See `docs/ci-proposed/` and `handoff/REPORT.md`.

## Optional TTS environment (not a package dependency)
`tools/run_moss_tts_nano.py` runs outside this package in a separate venv. Its exact versions are recorded in `tests/receipts/m06_pip_freeze.txt` (torch 2.7.0+cpu, transformers 4.57.1, MOSS-TTS-Nano at commit 8b7bcc93). That environment is not needed for tests or examples.
