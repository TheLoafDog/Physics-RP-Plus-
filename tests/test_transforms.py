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
