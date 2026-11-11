"""Saving the plotted data and graph to files (tkinter-free, so it can be tested headless).

The CSV holds the plotted (linearised) readings under the graph's axis labels,
e.g. "1 / Length (1 / m),Frequency (Hz)", one reading per row. The PNG is just
matplotlib's own `savefig` of the figure.
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


def save_png(figure, path):
    """Save `figure` to `path` as a PNG with a white background, as drawn in the app."""
    figure.savefig(path, format = "png", dpi = 150, facecolor = "white")


def default_filename(name, extension):
    """Return a file name for practical `name` safe on every OS, e.g. "RP5 Determination of Resistivity of a Wire" -> "RP5_Determination_of_Resistivity_of_a_Wire.csv"."""
    keep = "".join(c if (c.isalnum() or c in " -_") else "" for c in name).strip()
    return (keep.replace(" ", "_") or "graph") + extension
