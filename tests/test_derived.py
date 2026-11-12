import math

from derived import DERIVED, derived_quantities, derived_text
from hashing import requiredPracticalList


def test_every_derived_practical_exists():
    names = {rp["name"] for rp in requiredPracticalList}
    assert set(DERIVED) <= names


def test_rp6_emf_is_intercept_and_r_is_minus_gradient():
    assert derived_quantities("RP6 Internal resistance and emf", -1.0, 1.5) == ["E = 1.50 V", "r = 1.00 Ω"]


def test_rp9_time_constant_and_initial_voltage():
    # ln(V) = -t/RC + ln(V0) with RC = 2 s and V0 = 6 V
    results = derived_quantities("RP9 Charging and Discharging Capacitors", -0.5, math.log(6))
    assert results == ["RC = 2.00 s", "V₀ = 6.00 V"]


def test_rp9_zero_gradient_is_unavailable_not_a_crash():
    results = derived_quantities("RP9 Charging and Discharging Capacitors", 0.0, 1.0)
    assert results[0] == "RC unavailable"
    assert results[1] == "V₀ = 2.72 V"


def test_rp3_g_is_gradient_and_u_is_half_intercept():
    assert derived_quantities("RP3 Determination of g", 9.81, 1.0) == ["g = 9.81 m/s²", "u = 0.500 m/s"]


def test_rp1_wave_speed_is_twice_gradient():
    assert derived_quantities("RP1 Stationary Waves on a String", 15.0, 0.0) == ["v = 30.0 m/s"]


def test_practicals_without_direct_quantities_give_nothing():
    assert derived_quantities("RP5 Determination of Resistivity of a Wire", 1.0, 2.0) == []
    assert derived_text("RP5 Determination of Resistivity of a Wire", 1.0, 2.0) == ""


def test_derived_text_joins_quantities():
    assert derived_text("RP6 Internal resistance and emf", -1.0, 1.5) == "E = 1.50 V,   r = 1.00 Ω"


def test_numpy_zero_gradient_is_unavailable_not_inf():
    import numpy as np
    from derived import derived_quantities
    results = derived_quantities("RP9 Charging and Discharging Capacitors", np.float64(0.0), np.float64(1.0))
    assert results[0] == "RC unavailable"
