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


def inverse_transform_point(x, y, mode):
    """Return the raw reading that `transform_point` would turn into the linearised pair (x, y).

    Used when importing a CSV the app itself exported, which holds linearised values
    (e.g. 1 / L, ln(V) or cos(θ)) rather than the readings a student typed in.
    Raises ZeroDivisionError for 1 / 0 (mode 1) and ValueError for a cos value
    outside [-1, 1] (mode 3) or non-numeric input.
    """
    x = float(x)
    y = float(y)
    if mode == MODE_RECIPROCAL_X:
        x = 1 / x
    elif mode == MODE_LN_Y:
        y = math.exp(y)
    elif mode == MODE_COS_X:
        x = math.degrees(math.acos(x))
    return x, y


def input_error_message(x, y, mode):
    """Return a short message saying why transform_point(x, y, mode) would fail, or "" if it wouldn't.

    Used by the app to tell the user what to fix instead of silently ignoring the click.
    """
    for label, value in (("x", x), ("y", y)):
        if str(value).strip() == "":
            return f"Enter a value for {label}"
        try:
            float(value)
        except ValueError:
            return f"{label} must be a number, not '{value}'"
    x = float(x)
    y = float(y)
    if mode == MODE_RECIPROCAL_X and x == 0:
        return "x must not be 0 (the graph plots 1 / x)"
    if mode == MODE_LN_Y and y <= 0:
        return "y must be positive (the graph plots ln(y))"
    return ""
