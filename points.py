"""Helpers for the plotted data arrays (tkinter-free, so they can be tested headless).

`Main.py` keeps the entered readings as two parallel numpy arrays `x` and `y`;
a reading is the pair (x[i], y[i]).
"""

import numpy as np


def find_point(x, y, px, py):
    """Return the index of the first reading equal to the pair (px, py), or None if there isn't one."""
    matches = np.where((x == px) & (y == py))[0]
    return int(matches[0]) if len(matches) else None


def remove_point(x, y, px, py):
    """Return copies of `x` and `y` with the first reading equal to (px, py) removed.

    Raises ValueError if that pair is not present. Matching on the pair (rather
    than on x and y separately) means removing (1, 2) from [(1, 5), (3, 2)] fails
    instead of deleting x from one reading and y from another.
    """
    index = find_point(x, y, px, py)
    if index is None:
        raise ValueError(f"({px}, {py}) is not a plotted reading")
    return np.delete(x, index), np.delete(y, index)
