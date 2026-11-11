import rp_data
import hashing


def test_source_dicts_match_the_data_file():
    """hashing.py is the source of truth; `python3 hashing.py --write` regenerates RP info.txt from it."""
    for practical in hashing.requiredPracticalList:
        assert rp_data.hashGet(practical["name"]) == practical


def test_build_table_places_each_dict_at_or_after_its_home_slot():
    table = hashing.buildTable()
    assert len(table) == rp_data.TABLE_SIZE
    assert sum(1 for line in table if line) == len(hashing.requiredPracticalList)
    for practical in hashing.requiredPracticalList:
        assert rp_data.hashGet(practical["name"], table) == practical


def test_axis_labels_match_the_transform_mode():
    """xAxis / yAxis are the labels of the plotted (linearised) graph, so they must describe the transformed quantity."""
    for practical in hashing.requiredPracticalList:
        if not practical["xAxis"]:
            continue  # RP7, RP8, RP12 are still empty
        mode = practical["mode"]
        if mode == 1:
            assert practical["xAxis"].startswith("1 /")
        elif mode == 2:
            assert practical["yAxis"].startswith("ln(")
        elif mode == 3:
            assert practical["xAxis"].startswith("cos(")
