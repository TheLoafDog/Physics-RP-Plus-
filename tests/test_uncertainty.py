import math

import numpy as np
import pytest

from uncertainty import (gradient_uncertainty, has_uncertainties, parse_uncertainty, transform_uncertainty,
                         uncertainty_text, worst_fit_lines)


def test_parse_uncertainty_blank_is_zero():
    assert parse_uncertainty("") == 0.0
    assert parse_uncertainty("  ") == 0.0
    assert parse_uncertainty("0.05") == 0.05


@pytest.mark.parametrize("bad", ["abc", "-1"])
def test_parse_uncertainty_rejects_bad_text(bad):
    with pytest.raises(ValueError):
        parse_uncertainty(bad)


def test_transform_uncertainty_only_changes_for_ln_y():
    assert transform_uncertainty(5, 0.2, 0) == 0.2
    assert transform_uncertainty(5, 0.2, 1) == 0.2
    assert transform_uncertainty(5, 0.2, 2) == pytest.approx(0.04)  # Δ(ln y) = Δy / y
    assert transform_uncertainty(5, 0.2, 3) == 0.2


def test_has_uncertainties():
    assert not has_uncertainties(np.array([0.0, 0.0]))
    assert not has_uncertainties(np.array([]))
    assert has_uncertainties(np.array([0.0, 0.1]))


def test_worst_fit_lines_through_first_and_last_error_bars():
    # y = 2x exactly, ± 1 on each point: steepest joins (0, -1) to (2, 5), shallowest (0, 1) to (2, 3)
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 2.0, 4.0])
    dy = np.array([1.0, 1.0, 1.0])
    (m1, c1), (m2, c2) = worst_fit_lines(x, y, dy)
    assert (m1, c1) == pytest.approx((3.0, -1.0))
    assert (m2, c2) == pytest.approx((1.0, 1.0))


def test_worst_fit_lines_use_extreme_x_regardless_of_order():
    x = np.array([2.0, 0.0, 1.0])
    y = np.array([4.0, 0.0, 2.0])
    dy = np.array([0.5, 0.5, 0.0])
    (m1, _), (m2, _) = worst_fit_lines(x, y, dy)
    assert m1 == pytest.approx(2.5)
    assert m2 == pytest.approx(1.5)


def test_worst_fit_lines_need_two_distinct_x():
    assert worst_fit_lines(np.array([1.0, 1.0]), np.array([1.0, 2.0]), np.array([0.1, 0.1])) is None


def test_gradient_uncertainty_is_half_the_spread():
    absolute, percent = gradient_uncertainty(2.0, 3.0, 1.0)
    assert absolute == 1.0
    assert percent == pytest.approx(50.0)
    assert gradient_uncertainty(0.0, 1.0, -1.0) == (1.0, None)


def test_uncertainty_text():
    assert uncertainty_text(2.0, 2.5, 1.5, "V / A") == "± 0.500 V / A (25.0 %)"
    assert uncertainty_text(2.0, 2.5, 1.5, "") == "± 0.500 (25.0 %)"
