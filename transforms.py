"""Data transforms applied to a reading before it is plotted (tkinter-free).

Each required practical stores a `mode` saying how to linearise its data:
  0 - plot (x, y) as entered
  1 - x -> 1 / x          (e.g. RP1: frequency against 1 / length)
  2 - y -> ln(y)          (e.g. RP9: ln(V) against time)
  3 - x -> cos(x degrees) (e.g. RP11: emf against cos(theta))
"""

import math

MODE_NONE = 0
MODE_RECIPROCAL_X = 1
MODE_LN_Y = 2
MODE_COS_X = 3


def transform_point(x, y, mode):
    """Return the linearised (x, y) pair for `mode`.

    `x` and `y` may be strings as typed by the user; they are converted with
    float(). Raises ValueError for non-numeric input or ln of a non-positive
    value, and ZeroDivisionError for 1 / 0.
    """
    x = float(x)
    y = float(y)
    if mode == MODE_RECIPROCAL_X:
        x = 1 / x
    elif mode == MODE_LN_Y:
        y = math.log(y)
    elif mode == MODE_COS_X:
        x = math.cos(math.radians(x))
    return x, y
