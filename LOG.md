# Log

## 2026-11-10 — bootstrap
- Explored the repo: single-file Tkinter + matplotlib app (`Main.py`), practical data in `RP info.txt` (hash table of dict literals) generated from `hashing.py`.
- Added CLAUDE.md (project overview, run/check commands, session rules), ROADMAP.md (Phase 1 structure/tooling, Phase 2 features) and this log.
- No code changes. Noted bugs and physics questions as roadmap items; RP7/RP8/RP12 data and the RP3 equation text are tagged [needs Brandon].

## 2026-11-11 — README
- README now covers what the app does, requirements, install/run and how to use it.
- Docs only. Merged by Claude (interactive session with Brandon).

## 2026-11-11 — requirements.txt + .gitignore
- Added requirements.txt (matplotlib, numpy) and a Python .gitignore; README install step now uses requirements.txt.
- Merged by Claude (interactive session with Brandon).

## 2026-11-11 — rp_data module
- New tkinter-free `rp_data.py` (hashKey, loadTable, hashGet); Main.py and hashing.py both import it, duplicate hashGet removed.
- `RP info.txt` now resolved next to the script, so the app runs from any directory; a missing name raises KeyError instead of looping/crashing.
- Checked: py_compile, all 12 practical names resolve, hashing.py prints RP11 from another directory. Merged by Claude.

## 2026-11-11 — __main__ guards
- Main.py only creates Tk() and calls main() when run directly; hashing.py only prints its data check when run directly.
- Running `python3 Main.py` behaves as before. Merged by Claude.

## 2026-11-11 — transform_point
- New tkinter-free `transforms.py` with `transform_point(x, y, mode)`; `refreshGraph` calls it instead of inlining the mode 0–3 maths.
- Dropped the label-string mode re-detection in `refreshGraph` (it always matched the stored `mode` for every filled practical) so new rows keep the mode passed in.
- Checked: py_compile, hashing.py data check, transform_point spot-checks for all four modes and error cases. Merged by Claude (autonomous run).

## 2026-11-11 — pytest harness
- Added `tests/` (conftest adds the repo root to sys.path, `pytest.ini` sets testpaths): hashGet finds all 12 RPs with the expected fields, raises KeyError when missing, probes past collisions; transform_point covered for modes 0–3 and its error cases.
- Noted: `RP info.txt` has 100 lines (97 slots + 3 trailing blanks); the test allows that. Merged by Claude (autonomous run).

## 2026-11-11 — CI workflow
- Added `.github/workflows/ci.yml`: Python 3.12, installs requirements + pytest, runs py_compile, `hashing.py` and pytest on push and pull_request.
- Merged by Claude (autonomous run); the first Actions run happens on the merge commit itself, so check the Actions tab if it is red.

## 2026-11-11 — createEntryRow helper
- The three identical "build an entry row" blocks (first row in `createDataEntryFrame`, two in `refreshGraph`) are now one `createEntryRow(entryListFrame, row, ...)` helper.
- Pure refactor; py_compile and pytest pass. No Tk in the sandbox, so not run interactively. Merged by Claude (autonomous run).

## 2026-11-11 — x/y naming untangled
- `openRP` now takes `(xAxis, yAxis, ...)` in the order the sidebar passes them, and every RP dict's `xAxis`/`yAxis` are now the labels actually drawn on the x and y axes (values swapped in hashing.py and `RP info.txt`). Displayed graphs are unchanged.
- Replaced the broken commented-out generator with `buildTable`/`writeTable` (`python3 hashing.py --write`); new tests check the dicts match the data file and that axis labels match each practical's transform mode.
- py_compile, data check and pytest pass. Merged by Claude (autonomous run).
