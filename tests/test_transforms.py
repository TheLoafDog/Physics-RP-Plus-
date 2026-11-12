import math

import pytest

from transforms import transform_point


def test_mode_0_converts_strings_to_floats():
    assert transform_point("2", "3.5", 0) == (2.0, 3.5)


def test_mode_1_reciprocal_x():
    assert transform_point(4, 7, 1) == (0.25, 7.0)


def test_mode_2_ln_y():
    x, y = transform_point(1, math.e, 2)
    assert x == 1.0
    assert y == pytest.approx(1.0)


def test_mode_3_cos_of_degrees():
    x, _ = transform_point(60, 1, 3)
    assert x == pytest.approx(0.5)
    assert transform_point(0, 1, 3)[0] == pytest.approx(1.0)


@pytest.mark.parametrize("bad", [("a", 1, 0), ("", 1, 0), (1, "", 0)])
def test_non_numeric_raises_valueerror(bad):
    with pytest.raises(ValueError):
        transform_point(*bad)


def test_reciprocal_of_zero_raises():
    with pytest.raises(ZeroDivisionError):
        transform_point(0, 1, 1)


@pytest.mark.parametrize("y", [0, -1])
def test_ln_of_non_positive_raises(y):
    with pytest.raises(ValueError):
        transform_point(1, y, 2)


from transforms import input_error_message


@pytest.mark.parametrize("x, y, mode, expected", [
    ("1", "2", 0, ""),
    ("", "2", 0, "Enter a value for x"),
    ("1", " ", 0, "Enter a value for y"),
    ("abc", "2", 0, "x must be a number, not 'abc'"),
    ("1", "two", 0, "y must be a number, not 'two'"),
    ("0", "2", 1, "x must not be 0 (the graph plots 1 / x)"),
    ("1", "0", 2, "y must be positive (the graph plots ln(y))"),
    ("1", "-3", 2, "y must be positive (the graph plots ln(y))"),
    ("0", "2", 0, ""),
    ("1", "0", 3, ""),
])
def test_input_error_message(x, y, mode, expected):
    assert input_error_message(x, y, mode) == expected


@pytest.mark.parametrize("x, y, mode", [("", "1", 0), ("a", "1", 0), ("0", "1", 1), ("1", "0", 2), ("1", "-1", 2)])
def test_message_is_non_empty_exactly_when_transform_point_raises(x, y, mode):
    with pytest.raises((ValueError, ZeroDivisionError)):
        transform_point(x, y, mode)
    assert input_error_message(x, y, mode) != ""


@pytest.mark.parametrize("mode,raw", [(0, (2.0, 3.0)), (1, (4.0, 7.0)), (2, (1.0, 5.0)), (3, (60.0, 1.0))])
def test_inverse_transform_undoes_transform(mode, raw):
    from transforms import inverse_transform_point
    back = inverse_transform_point(*transform_point(*raw, mode), mode)
    assert back == pytest.approx(raw)


def test_inverse_transform_rejects_impossible_values():
    from transforms import inverse_transform_point
    with pytest.raises(ValueError):
        inverse_transform_point(1.5, 1, 3)  # cos(θ) can't exceed 1
    with pytest.raises(ZeroDivisionError):
        inverse_transform_point(0, 1, 1)
