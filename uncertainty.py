"""Error bars and worst-fit lines (tkinter-free, so it can be tested headless).

A student may give each reading an absolute uncertainty in y (the "± y" box).
Following the usual A-level method, the worst acceptable lines are the steepest
and shallowest straight lines through the ends of the first and last points'
error bars, and the uncertainty in the gradient is half the difference between
their gradients:

    Δm = (m_steepest − m_shallowest) / 2,    % uncertainty = Δm / |m_best| × 100
"""

import math

import numpy as np

from fit import format_value, with_unit
from transforms import MODE_LN_Y


def parse_uncertainty(text):
    """Return the absolute uncertainty typed in the "± y" box as a non-negative float; blank means 0.

    Raises ValueError for non-numeric or negative text.
    """
    text = str(text).strip()
    if text == "":
        return 0.0
    value = float(text)
    if value < 0:
        raise ValueError("uncertainty must not be negative")
    return value


def transform_uncertainty(y_raw, dy, mode):
    """Return the uncertainty in the plotted y for a raw reading `y_raw` ± `dy`.

    Only mode 2 changes y (y -> ln y), for which Δ(ln y) = Δy / y. The other
    modes transform x, so the y uncertainty is unchanged.
    """
    y_raw = float(y_raw)
    dy = float(dy)
    if mode == MODE_LN_Y:
        return dy / y_raw
    return dy


def has_uncertainties(dy):
    """True if any reading was given a non-zero uncertainty."""
    return len(dy) > 0 and bool(np.any(np.asarray(dy, dtype = float) != 0))


def line_through(x1, y1, x2, y2):
    """Return (gradient, intercept) of the straight line through two points."""
    gradient = (y2 - y1) / (x2 - x1)
    return gradient, y1 - gradient * x1


def worst_fit_lines(x, y, dy):
    """Return ((m_steep, c_steep), (m_shallow, c_shallow)) for readings `x`, `y` with y uncertainties `dy`.

    The lines join the ends of the error bars of the reading with the smallest x
    and the reading with the largest x: the steepest from (x_first, y_first − dy)
    to (x_last, y_last + dy), the shallowest from (x_first, y_first + dy) to
    (x_last, y_last − dy). Returns None if there are fewer than two distinct x
    values, since no line can then be drawn.
    """
    x = np.asarray(x, dtype = float)
    y = np.asarray(y, dtype = float)
    dy = np.asarray(dy, dtype = float)
    first = int(np.argmin(x))
    last = int(np.argmax(x))
    if x[first] == x[last]:
        return None
    steep = line_through(x[first], y[first] - dy[first], x[last], y[last] + dy[last])
    shallow = line_through(x[first], y[first] + dy[first], x[last], y[last] - dy[last])
    return steep, shallow


def gradient_uncertainty(best_gradient, steep_gradient, shallow_gradient):
    """Return (absolute, percentage) uncertainty in the gradient; the percentage is None when the best gradient is 0."""
    absolute = abs(steep_gradient - shallow_gradient) / 2
    if best_gradient == 0 or math.isnan(best_gradient):
        return absolute, None
    return absolute, absolute / abs(best_gradient) * 100


def uncertainty_text(best_gradient, steep_gradient, shallow_gradient, gradient_unit):
    """Return the second info-panel line for the gradient, e.g. "± 0.25 V / A (12.5 %)"."""
    absolute, percent = gradient_uncertainty(best_gradient, steep_gradient, shallow_gradient)
    text = "± " + with_unit(format_value(absolute), gradient_unit)
    if percent is not None:
        text += f" ({format_value(percent)} %)"
    return text
