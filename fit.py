"""Formatting of the best-fit line's gradient and intercept (tkinter-free, so it can be tested headless).

The app shows the gradient and y-intercept from `np.polyfit`. Raw floats such as
-1.0000000000000002 are not what a student writes down, so they are rounded to a
sensible number of significant figures and given a unit worked out from the axis
labels: the intercept has the y-axis unit and the gradient has (y unit) / (x unit).
"""

import math

SIG_FIGS = 3  # A-level convention for a value read off a graph


def axis_unit(label):
    """Return the unit in a trailing " (unit)" of an axis label, or None if it has none.

    "Frequency (Hz)" -> "Hz"; "1 / Length (1 / m)" -> "1 / m". A label that is a
    function, such as "ln(V)" or "cos(θ)", has no space before its bracket and is
    dimensionless, so it gives None.
    """
    label = label.strip()
    if not label.endswith(")"):
        return None
    start = label.rfind(" (")
    if start == -1:
        return None
    unit = label[start + 2:-1].strip()
    return unit or None


def _bracketed(unit):
    """Wrap a compound unit (one with a space or a slash) in brackets so a / b is unambiguous."""
    return f"({unit})" if ("/" in unit or " " in unit) else unit


def gradient_unit(x_unit, y_unit):
    """Return the unit of dy/dx for the given axis units (either may be None), or "" if both are dimensionless."""
    if y_unit is None and x_unit is None:
        return ""
    if x_unit is None:
        return y_unit
    if y_unit is None:
        return f"{x_unit}⁻¹" if _bracketed(x_unit) == x_unit else f"1 / ({x_unit})"
    return f"{_bracketed(y_unit)} / {_bracketed(x_unit)}"


def format_value(value, sig_figs = SIG_FIGS):
    """Return `value` rounded to `sig_figs` significant figures, keeping trailing zeros (1.5 -> "1.50").

    Very large or very small values use scientific notation (1.23e+07, 4.56e-05).
    """
    value = float(value)
    if value == 0 or math.isnan(value) or math.isinf(value):
        return "0" if value == 0 else str(value)
    rounded = float(f"{value:.{sig_figs}g}")  # Round first so 9.996 becomes 10.0 before the exponent is chosen
    exponent = math.floor(math.log10(abs(rounded)))
    if exponent >= 6 or exponent <= -5:
        return f"{rounded:.{sig_figs - 1}e}"
    decimals = max(sig_figs - 1 - exponent, 0)
    return f"{rounded:.{decimals}f}"


def with_unit(text, unit):
    """Join a formatted number and its unit, leaving the number alone when there is no unit."""
    return f"{text} {unit}" if unit else text


def format_fit(gradient, intercept, x_label, y_label, sig_figs = SIG_FIGS):
    """Return (gradient text, intercept text) for the info panel, e.g. ("-1.00 V / A", "1.50 V")."""
    x_unit = axis_unit(x_label)
    y_unit = axis_unit(y_label)
    gradient_text = with_unit(format_value(gradient, sig_figs), gradient_unit(x_unit, y_unit))
    intercept_text = with_unit(format_value(intercept, sig_figs), y_unit or "")
    return gradient_text, intercept_text
