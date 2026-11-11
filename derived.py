"""Physical quantities read straight off the best-fit line (tkinter-free, so it can be tested headless).

Only practicals whose linearised equation gives a quantity from the gradient or
intercept alone are listed here; the others (e.g. RP5, where the gradient is ρ/A)
need a separately measured value, so nothing is shown for them.

Each entry is (symbol, function(gradient, intercept) -> value, unit). The functions
may raise ZeroDivisionError or OverflowError for degenerate fits; those quantities
are then shown as "unavailable".
"""

import math

from fit import format_value

DERIVED = {
    # f = (v/2)(1/L): gradient = v/2
    "RP1 Stationary Waves on a String": [
        ("v", lambda gradient, intercept: 2 * gradient, "m/s"),
    ],
    # 2h/t = gt + 2u: gradient = g, intercept = 2u
    "RP3 Determination of g": [
        ("g", lambda gradient, intercept: gradient, "m/s²"),
        ("u", lambda gradient, intercept: intercept / 2, "m/s"),
    ],
    # V = (-r)I + E: gradient = -r, intercept = E
    "RP6 Internal resistance and emf": [
        ("E", lambda gradient, intercept: intercept, "V"),
        ("r", lambda gradient, intercept: -gradient, "Ω"),
    ],
    # ln(V) = (-1/RC)t + ln(V₀): gradient = -1/RC, intercept = ln(V₀)
    "RP9 Charging and Discharging Capacitors": [
        ("RC", lambda gradient, intercept: -1 / gradient, "s"),
        ("V₀", lambda gradient, intercept: math.exp(intercept), "V"),
    ],
}


def derived_quantities(name, gradient, intercept):
    """Return a list of "symbol = value unit" strings for practical `name`, or [] if it has none."""
    results = []
    for symbol, compute, unit in DERIVED.get(name, []):
        try:
            value = compute(gradient, intercept)
        except (ZeroDivisionError, OverflowError):
            results.append(f"{symbol} unavailable")
            continue
        results.append(f"{symbol} = {format_value(value)} {unit}")
    return results


def derived_text(name, gradient, intercept):
    """Return the derived quantities joined for the info panel ("E = 1.50 V,  r = 1.00 Ω"), or "" if none."""
    return ",   ".join(derived_quantities(name, gradient, intercept))
