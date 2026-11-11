import pytest

from fit import axis_unit, format_fit, format_value, gradient_unit
from hashing import requiredPracticalList


@pytest.mark.parametrize("label, unit", [
    ("Frequency (Hz)", "Hz"),
    ("1 / Length (1 / m)", "1 / m"),
    ("Height x 2 / Time (m/s)", "m/s"),
    ("ε₀ (V)", "V"),
    ("ln(V)", None),       # a function, not a unit
    ("cos(θ)", None),
    ("Time", None),
    ("", None),
])
def test_axis_unit(label, unit):
    assert axis_unit(label) == unit


@pytest.mark.parametrize("x_unit, y_unit, expected", [
    ("A", "V", "V / A"),
    ("s", "m/s", "(m/s) / s"),
    ("1 / m", "Hz", "Hz / (1 / m)"),
    ("s", None, "s⁻¹"),
    ("1 / m", None, "1 / (1 / m)"),
    (None, "V", "V"),
    (None, None, ""),
])
def test_gradient_unit(x_unit, y_unit, expected):
    assert gradient_unit(x_unit, y_unit) == expected


@pytest.mark.parametrize("value, text", [
    (-1.0000000000000002, "-1.00"),
    (1.4999999999999998, "1.50"),
    (0.0123456, "0.0123"),
    (123456, "123000"),
    (9.996, "10.0"),       # rounding carries into a new digit
    (0, "0"),
    (12345678.9, "1.23e+07"),
    (0.0000123, "1.23e-05"),
])
def test_format_value_three_sig_figs(value, text):
    assert format_value(value) == text


def test_format_value_other_sig_figs():
    assert format_value(3.14159, 4) == "3.142"
    assert format_value(2, 1) == "2"


def test_format_fit_rp6_style_labels():
    gradient, intercept = format_fit(-1.0000000000000002, 1.4999999999999998, "Current (A)", "Voltage (V)")
    assert gradient == "-1.00 V / A"
    assert intercept == "1.50 V"


def test_format_fit_dimensionless_axes_have_no_unit():
    gradient, intercept = format_fit(2.5, -0.25, "Time (s)", "ln(V)")
    assert gradient == "2.50 s⁻¹"
    assert intercept == "-0.250"
    gradient, intercept = format_fit(2.5, 0.5, "cos(θ)", "ε₀ (V)")
    assert gradient == "2.50 V"
    assert intercept == "0.500 V"


def test_every_filled_in_practical_formats():
    for rp in requiredPracticalList:
        if rp["xAxis"]:
            gradient, intercept = format_fit(1.0, 2.0, rp["xAxis"], rp["yAxis"])
            assert gradient.startswith("1.00") and intercept.startswith("2.00")
