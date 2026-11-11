# Roadmap

Ordered checklist. Up to 4 items per Claude session; each should fit in one small PR.
Items tagged [needs Brandon] are skipped by unattended runs.

## Phase 1 — Structure and tooling
- [x] README: add requirements, install and run instructions, and a short description of how to use the app.
- [x] Add `requirements.txt` (matplotlib, numpy) and a `.gitignore` for Python (`__pycache__/`, venvs).
- [x] Move practical data and `hashGet` into a tkinter-free module (e.g. `rp_data.py`) used by both `Main.py` and `hashing.py`, removing the duplicated `hashGet`; resolve `RP info.txt` relative to the script file so the app runs from any directory.
- [x] Guard the app start-up with `if __name__ == "__main__":` so modules can be imported without opening a window.
- [x] Move the data-transform logic (`mode` 0–3) into a pure function (e.g. `transform_point(x, y, mode)`) and drop the label-string mode re-detection inside `refreshGraph`.
- [x] Add a pytest harness with tests for `hashGet` (all 12 RPs found) and the transform function.
- [x] Add a GitHub Actions workflow running `py_compile` and `pytest` on push/PR.
- [x] Remove the duplicated "create new entry row" code in `refreshGraph` (three near-identical blocks) into one helper.
- [x] Untangle the x/y naming: `openRP(mainFrame, yAxis, xAxis, ...)` receives `xAxis` as `yAxis`, and the RP dicts' `xAxis`/`yAxis` fields are swapped relative to the entry titles. Make the field names mean what they say without changing what's displayed.
- [x] Fix removal of a data point: it currently checks `newX in x and newY in y` independently and deletes by separate x/y indices, so it can remove the wrong pair. Match on the (x, y) pair instead.
- [x] Replace the bare `except:` in `refreshGraph` with specific exceptions (ValueError, ZeroDivisionError) and show a short message for invalid input (e.g. ln of a non-positive value).
- [x] Axis limits: allow negative values (e.g. RP9 ln(V) data, RP6 if plotted with offsets) instead of always starting at 0.

## Phase 2 — New implementations
- [ ] [needs Brandon] Fill in RP7 (Simple Harmonic Motion): choose which graph the app should plot (e.g. T² against l for a pendulum, or T² against m for a mass-spring) and its axes/equations.
- [ ] [needs Brandon] Fill in RP8 (Boyle's Law): confirm the graph (e.g. p against 1/V) and axes/equations.
- [ ] [needs Brandon] Fill in RP12 (Inverse Square Law): confirm the graph (e.g. 1/√C against d, or C against 1/d²) and the transform mode needed.
- [ ] [needs Brandon] Check RP3's "original equation" text: it reads `s = ut + 1/2(at)²`, but the standard SUVAT form is `s = ut + ½at²`.
- [ ] Show gradient and intercept rounded to sensible significant figures, with units derived from the axis labels where possible.
- [ ] Show the physical quantity derived from the gradient/intercept for practicals where it's direct (e.g. RP6: E = intercept, r = −gradient; RP9: RC = −1/gradient).
- [ ] Add a "Clear data" button that resets the current practical's points.
- [ ] Export: save the current graph as PNG and the entered data as CSV.
- [ ] Import data from a CSV file into the current practical.
- [ ] Uncertainty: optional error bars per point, plus worst-fit (max/min gradient) lines and the percentage uncertainty in the gradient.
- [ ] Show the coefficient of determination (R²) for the best-fit line.
