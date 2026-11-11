import numpy as np
import pytest

from points import find_point, remove_point


def test_find_point_matches_the_pair_not_the_coordinates_separately():
    x = np.array([1.0, 3.0])
    y = np.array([5.0, 2.0])
    assert find_point(x, y, 3.0, 2.0) == 1
    assert find_point(x, y, 1.0, 2.0) is None  # x from one reading, y from another


def test_remove_point_removes_only_the_matching_pair():
    x = np.array([1.0, 2.0, 1.0])
    y = np.array([5.0, 5.0, 7.0])
    nx, ny = remove_point(x, y, 1.0, 7.0)
    assert nx.tolist() == [1.0, 2.0]
    assert ny.tolist() == [5.0, 5.0]


def test_remove_point_removes_first_duplicate_only():
    x = np.array([4.0, 4.0])
    y = np.array([1.0, 1.0])
    nx, ny = remove_point(x, y, 4.0, 1.0)
    assert nx.tolist() == [4.0] and ny.tolist() == [1.0]


def test_remove_point_raises_when_pair_is_absent():
    with pytest.raises(ValueError):
        remove_point(np.array([1.0, 3.0]), np.array([5.0, 2.0]), 1.0, 2.0)


from points import axis_limits


def test_axis_limits_positive_data_starts_at_zero():
    assert axis_limits(np.array([2.0, 5.0])) == (0.0, pytest.approx(5.5))


def test_axis_limits_negative_data_extends_below_zero():
    low, high = axis_limits(np.array([-2.0, -0.5]))
    assert low == pytest.approx(-2.2)
    assert high == 0.0


def test_axis_limits_mixed_data_includes_both_signs():
    assert axis_limits(np.array([-1.0, 3.0])) == (pytest.approx(-1.1), pytest.approx(3.3))


def test_axis_limits_never_returns_an_empty_range():
    low, high = axis_limits(np.array([0.0]))
    assert low < 0 < high
