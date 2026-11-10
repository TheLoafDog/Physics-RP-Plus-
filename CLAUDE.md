# CLAUDE.md

## Project
Physics RP Plus — a FinCode Hacks hackathon submission. A desktop app that helps A-level physics
students graph data from the required practicals (RP1–RP12): pick a practical from the sidebar,
type in (x, y) readings, and the app plots the (linearised) graph with a best-fit line, gradient
and y-intercept, alongside the original and linearised equations.

## Stack and layout
- Python 3 + Tkinter (GUI), matplotlib (embedded via `FigureCanvasTkAgg`), numpy (`polyfit`).
- `Main.py` — the whole app: sidebar, graph, data-entry rows, `refreshGraph`, `openRP`. Runs `Tk()`
  and `main()` at import time.
- `RP info.txt` — the practical "database": one Python dict literal per line, stored in a
  97-slot table at index `sum(ord(c) for c in name) % 97` (linear probing). Read by `hashGet`.
- `hashing.py` — the source dicts for each RP plus the (commented-out) generator for `RP info.txt`,
  and a duplicate of `hashGet`.
- Data-transform `mode`: 0 = none, 1 = x → 1/x, 2 = y → ln(y), 3 = x (degrees) → cos(x).

## How to run and check
- Install: `pip install matplotlib numpy` (Tkinter comes with most Python installs; on Debian/Ubuntu
  `apt install python3-tk`).
- Run: `python3 Main.py` from the repo root (it opens `RP info.txt` by relative path).
- Syntax check (works headless, no Tk needed): `python3 -m py_compile Main.py hashing.py`
- Data check: `python3 hashing.py` should print the RP11 dict.
- There is no test suite or linter yet (see ROADMAP Phase 1). Once `pytest` tests exist, run
  `python3 -m pytest -q` as well.
- The cloud sandbox has no Tkinter, so GUI behaviour can't be run there; keep logic that needs
  testing in plain functions that don't import tkinter.

## Rules for Claude sessions
- Start by reading the latest LOG.md entry and ROADMAP.md. Don't re-explore the whole repo.
- Do ONE unchecked roadmap item per session; skip items tagged [needs Brandon].
- Work on a branch `claude/<short-task-name>`; never commit to main.
- Keep diffs small and reviewable. Preserve existing behaviour unless the item says otherwise.
- Physics content must be correct (standard A-level formulas, symbols and SI units). If unsure,
  add a `TODO(Brandon)` comment instead of guessing.
- Add or keep tests where practical.
- Never invent facts about Brandon, his teammates or the hackathon. Never add personal data.
- Every PR is left open for Brandon to review — Claude does not merge.
- At the end: tick the item in ROADMAP.md and append a 3–5 line dated entry to LOG.md, in the same branch.
