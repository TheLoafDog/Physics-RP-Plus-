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
