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

## 2026-11-11 — point removal matches the (x, y) pair
- `refreshGraph` now decides add vs remove from the row's button colour, remembers the reading each row added (`button.addedPoint`) and removes exactly that pair via new tkinter-free `points.remove_point` (tested). Removal no longer parses the entry boxes, so a row can be removed even if its text was edited or cleared.
- Checked with pytest plus a headless stub-tkinter smoke run of add/remove. Merged by Claude (autonomous run).

## 2026-11-11 — input error messages
- `refreshGraph` catches only `ValueError` / `ZeroDivisionError` from `transform_point` and shows a short red message under the entry rows (new `messageString` label in `createDataEntryFrame`): blank or non-numeric box, 1 / 0, ln of a non-positive value, or the 16-reading limit. Cleared on the next valid click.
- Message text comes from tkinter-free `transforms.input_error_message` (tested). pytest + headless smoke run pass. Merged by Claude (autonomous run).

## 2026-11-11 — axis limits allow negative values
- `refreshGraph` sets limits with new `points.axis_limits`: still 0 → 1.1 × max for positive data, but the axis now extends below 0 when readings are negative (RP9 ln(V) for V < 1 V), and never gets an empty range.
- Tested in `tests/test_points.py`. Merged by Claude (autonomous run).

## 2026-11-11 — gradient and intercept rounded with units
- The info panel now shows the fit as e.g. "-1.00 V / A" and "1.50 V" instead of raw floats: new tkinter-free `fit.format_fit` rounds to 3 s.f. (scientific notation for very large/small values) and takes units from the trailing "(unit)" of the axis labels; `ln(V)` and `cos(θ)` are treated as dimensionless, so RP9's gradient is in s⁻¹ and its intercept has no unit.
- Tested in `tests/test_fit.py`; pytest plus a headless xvfb smoke run of RP6 pass. Merged by Claude (autonomous run).

## 2026-11-11 — derived quantities from the fit
- New `derived.py` lists, per practical, the quantities that come straight from the gradient/intercept: RP1 v = 2 × gradient; RP3 g = gradient, u = intercept / 2; RP6 E = intercept, r = −gradient; RP9 RC = −1 / gradient, V₀ = e^intercept. Shown on a new line under the gradient/intercept (blank for RP2/4/5/10/11, which need a separately measured A, s, n, N…). `openRP` now also receives the practical's name.
- To fit the extra line without covering the graph, the four bold title labels in the info panel are height 1 instead of 2. pytest (`tests/test_derived.py`) plus a headless xvfb run of RP6 and RP9 (RC = 2.00 s, V₀ = 6.00 V from generated data) pass. Merged by Claude (autonomous run).

## 2026-11-11 — Clear button
- A red "Clear" button at the bottom right of the data-entry panel (next to the error message, which is now left-aligned and a little narrower) destroys every entry row, resets `x`/`y`/`rowIndex`, redraws the placeholder graph, sets the gradient/intercept back to "Unavailable" and leaves one empty row.
- The placeholder-graph reset moved out of `createGraph` into `resetGraph`, shared with `clearData`. pytest plus a headless xvfb run (add 3 readings, clear, add again) pass. Merged by Claude (autonomous run).

## 2026-11-11 — export PNG / CSV
- New "Export" panel under the data-entry panel with "Save graph as PNG" (matplotlib `savefig`, 150 dpi) and "Save data as CSV" (header = the two axis labels, then the plotted, linearised readings; UTF-8). Both open a save-as dialog with a filesystem-safe default name from the practical's name; cancelling does nothing.
- Logic is in tkinter-free `export.py` (`tests/test_export.py`). pytest plus a headless xvfb run with the dialog stubbed pass. Merged by Claude (autonomous run).

## 2026-11-12 — import data from CSV
- New "Import data from CSV" button in the (renamed) Import / Export panel: each row of the file is typed into the next empty entry row and added as if its button were pressed, so transforms, validation and the 16-reading limit all apply; the message label then says how many readings were imported/skipped. A CSV the app exported (header = axis labels) holds linearised values, so `transforms.inverse_transform_point` turns them back into raw readings first.
- Parsing is in tkinter-free `export.read_csv` / `parse_readings` (tested). pytest plus a headless xvfb run (raw CSV with bad rows, then export → clear → re-import) pass. Merged by Claude (autonomous run).
