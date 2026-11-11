# CLAUDE.md

## Project
Physics RP Plus — a FinCode Hacks hackathon submission. A desktop app that helps A-level physics
students graph data from the required practicals (RP1–RP12): pick a practical from the sidebar,
type in (x, y) readings, and the app plots the (linearised) graph with a best-fit line, gradient
and y-intercept, alongside the original and linearised equations.

## Stack and layout
- Python 3 + Tkinter (GUI), matplotlib (embedded via `FigureCanvasTkAgg`), numpy (`polyfit`).
- `Main.py` — the whole app: sidebar, graph, data-entry rows, `refreshGraph`, `openRP`. Creates `Tk()`
  and calls `main()` only under `if __name__ == "__main__":`, so it can be imported without a window.
- `RP info.txt` — the practical "database": one Python dict literal per line, stored in a
  97-slot table at index `sum(ord(c) for c in name) % 97` (linear probing).
- `rp_data.py` — tkinter-free loader: `hashKey`, `loadTable`, `hashGet(name)` (raises KeyError if
  missing). Resolves `RP info.txt` next to the script, so the app runs from any directory.
- `hashing.py` — the source dicts for each RP plus the (commented-out) generator for `RP info.txt`;
  imports `hashGet` from `rp_data`.
- `transforms.py` — tkinter-free `transform_point(x, y, mode)` used by `refreshGraph`.
  Data-transform `mode`: 0 = none, 1 = x → 1/x, 2 = y → ln(y), 3 = x (degrees) → cos(x).

## How to run and check
- Install: `pip install matplotlib numpy` (Tkinter comes with most Python installs; on Debian/Ubuntu
  `apt install python3-tk`).
- Run: `python3 Main.py` (works from any directory).
- Syntax check (works headless, no Tk needed): `python3 -m py_compile *.py`
- Data check: `python3 hashing.py` should print the RP11 dict.
- There is no test suite or linter yet (see ROADMAP Phase 1). Once `pytest` tests exist, run
  `python3 -m pytest -q` as well.
- The cloud sandbox has no Tkinter, so GUI behaviour can't be run there; keep logic that needs
  testing in plain functions that don't import tkinter.

## Rules for Claude sessions
- Start by reading the latest LOG.md entry and ROADMAP.md. Don't re-explore the whole repo.
- Do up to 4 roadmap items per session, top to bottom, one branch + PR each; skip items tagged [needs Brandon].
- Work on a branch `claude/<short-task-name>`; never commit to main.
- Keep diffs small and reviewable. Preserve existing behaviour unless the item says otherwise.
- Physics content must be correct (standard A-level formulas, symbols and SI units). If unsure,
  add a `TODO(Brandon)` comment instead of guessing.
- Add or keep tests where practical.
- Never invent facts about Brandon, his teammates or the hackathon. Never add personal data.
- Autonomous merge policy: Claude merges its own PR (squash, via `gh api -X PUT .../pulls/<n>/merge -f merge_method=squash`)
  once the checks above pass and behaviour is preserved. Leave a PR open for Brandon, saying why in the body, when checks
  fail and can't be fixed, it rewrites or deletes a large part of the app, it touches licence/credits/personal or
  authorship info, it adds a paid or external service, or Claude is unsure it's correct. Never push to main directly,
  never force-push main, never rewrite history. Delete the remote `claude/` branch after merging.
- For each item: tick it in ROADMAP.md and append a 2–4 line dated entry to LOG.md (say merged or left open), in the same branch.
