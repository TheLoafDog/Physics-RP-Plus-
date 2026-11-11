import ast

import pytest

import rp_data

PRACTICALS = [
    "RP1 Stationary Waves on a String",
    "RP2 Interference Effects",
    "RP3 Determination of g",
    "RP4 Determination of Young's Modulus",
    "RP5 Determination of Resistivity of a Wire",
    "RP6 Internal resistance and emf",
    "RP7 Simple Harmonic Motion",
    "RP8 Boyle's Law",
    "RP9 Charging and Discharging Capacitors",
    "RP10 Magnetic Force on a Wire",
    "RP11 Magnetic Flux Linkage",
    "RP12 Inverse Square Law",
]

FIELDS = {"name", "xAxis", "yAxis", "xEntryTitle", "yEntryTitle", "originalEquation", "linearisedEquation", "mode"}


def test_table_has_at_least_97_slots():
    # The file may carry trailing blank lines beyond the 97 real slots.
    assert len(rp_data.RP_dicts) >= rp_data.TABLE_SIZE
    assert all(line == "" for line in rp_data.RP_dicts[rp_data.TABLE_SIZE:])


@pytest.mark.parametrize("name", PRACTICALS)
def test_every_practical_is_found(name):
    entry = rp_data.hashGet(name)
    assert entry["name"] == name
    assert FIELDS <= set(entry)
    assert entry["mode"] in (0, 1, 2, 3)


def test_missing_name_raises_keyerror():
    with pytest.raises(KeyError):
        rp_data.hashGet("RP99 Not a practical")


def test_each_stored_dict_sits_at_or_after_its_home_slot():
    """Linear probing only moves entries forward, and nothing in the file wraps past slot 96."""
    for index, line in enumerate(rp_data.RP_dicts):
        if line:
            name = ast.literal_eval(line)["name"]
            home = rp_data.hashKey(name)
            assert home <= index < rp_data.TABLE_SIZE


def test_hashGet_probes_past_a_collision():
    table = [""] * 5
    a = {"name": "a", "mode": 0}
    b = {"name": "b", "mode": 0}
    slot = rp_data.hashKey("a") % 5
    table[slot] = repr(a)
    table[(slot + 1) % 5] = repr(b)
    assert rp_data.hashGet("b", table) == b
