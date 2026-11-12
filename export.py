"""Saving the plotted data and graph to files, and reading data back in (tkinter-free, so it can be tested headless).

The CSV holds the plotted (linearised) readings under the graph's axis labels,
e.g. "1 / Length (1 / m),Frequency (Hz)", one reading per row. The PNG is just
matplotlib's own `savefig` of the figure.

Importing accepts two kinds of CSV: one the app exported (header = the axis
labels, values already linearised) or one of raw readings as a student would
type them (any other header, or no header), two columns, x then y.
"""

import csv

import numpy as np


def has_readings(x, y):
    """True if `x`, `y` hold entered readings rather than the (0, 0) placeholder the app starts with."""
    return not (len(x) == 1 and x[0] == 0 and y[0] == 0)


def csv_rows(x, y, x_label, y_label):
    """Return the CSV rows: a header of the two axis labels, then one [x, y] row per reading (none for the placeholder)."""
    rows = [[x_label, y_label]]
    if has_readings(x, y):
        rows.extend([float(px), float(py)] for px, py in zip(np.asarray(x), np.asarray(y)))
    return rows


def write_csv(path, x, y, x_label, y_label):
    """Write the plotted readings to `path` as CSV (UTF-8, so labels such as "Ω" and "θ" survive)."""
    with open(path, "w", newline = "", encoding = "utf-8") as file:
        csv.writer(file).writerows(csv_rows(x, y, x_label, y_label))


def is_number(text):
    """True if `text` converts with float()."""
    try:
        float(text)
    except (TypeError, ValueError):
        return False
    return True


def read_csv(path):
    """Return the non-blank rows of the CSV at `path` as lists of stripped strings (UTF-8, BOM tolerated)."""
    with open(path, newline = "", encoding = "utf-8-sig") as file:
        return [[cell.strip() for cell in row] for row in csv.reader(file) if any(cell.strip() for cell in row)]


def parse_readings(rows, x_label, y_label):
    """Split CSV `rows` into (readings, linearised, skipped).

    `readings` is a list of (x text, y text, ± y text) triples from the first
    three columns of each row (the third is "" when a row has only two). A first row whose two cells are not both numbers is taken as a
    header; `linearised` is True when that header is the app's own export header
    (the two axis labels), meaning the values are already transformed. `skipped`
    counts rows with fewer than two cells, which are left out.
    """
    linearised = False
    if rows and len(rows[0]) >= 2 and not (is_number(rows[0][0]) and is_number(rows[0][1])):
        linearised = rows[0][0] == x_label.strip() and rows[0][1] == y_label.strip()
        rows = rows[1:]
    elif rows and len(rows[0]) < 2 and rows[0] and not is_number(rows[0][0]):
        rows = rows[1:]  # a one-cell title line
    readings = [(row[0], row[1], row[2] if len(row) > 2 else "") for row in rows if len(row) >= 2]
    return readings, linearised, len(rows) - len(readings)


def save_png(figure, path):
    """Save `figure` to `path` as a PNG with a white background, as drawn in the app."""
    figure.savefig(path, format = "png", dpi = 150, facecolor = "white")


def default_filename(name, extension):
    """Return a file name for practical `name` safe on every OS, e.g. "RP5 Determination of Resistivity of a Wire" -> "RP5_Determination_of_Resistivity_of_a_Wire.csv"."""
    keep = "".join(c if (c.isalnum() or c in " -_") else "" for c in name).strip()
    return (keep.replace(" ", "_") or "graph") + extension
