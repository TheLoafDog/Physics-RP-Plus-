import csv

import matplotlib
import numpy as np

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt

from export import csv_rows, default_filename, has_readings, save_png, write_csv


def test_placeholder_has_no_readings():
    assert not has_readings(np.array([0]), np.array([0]))
    assert has_readings(np.array([0.0]), np.array([2.0]))
    assert has_readings(np.array([1.0, 2.0]), np.array([3.0, 4.0]))


def test_csv_rows_header_then_readings():
    rows = csv_rows(np.array([0.1, 0.2]), np.array([1.4, 1.3]), "Current (A)", "Voltage (V)")
    assert rows == [["Current (A)", "Voltage (V)"], [0.1, 1.4], [0.2, 1.3]]


def test_csv_rows_placeholder_is_header_only():
    assert csv_rows(np.array([0]), np.array([0]), "x", "y") == [["x", "y"]]


def test_write_csv_round_trips_with_unicode_labels(tmp_path):
    path = tmp_path / "out.csv"
    write_csv(path, np.array([1.0, 2.0]), np.array([3.0, 4.5]), "Resistance (Ω)", "cos(θ)")
    with open(path, newline = "", encoding = "utf-8") as file:
        rows = list(csv.reader(file))
    assert rows == [["Resistance (Ω)", "cos(θ)"], ["1.0", "3.0"], ["2.0", "4.5"]]


def test_save_png_writes_a_png(tmp_path):
    figure, axes = plt.subplots()
    axes.plot([0, 1], [0, 1])
    path = tmp_path / "graph.png"
    save_png(figure, path)
    plt.close(figure)
    assert path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_default_filename_is_filesystem_safe():
    assert default_filename("RP4 Determination of Young's Modulus", ".csv") == "RP4_Determination_of_Youngs_Modulus.csv"
    assert default_filename("RP8 Boyle's Law", ".png") == "RP8_Boyles_Law.png"
    assert default_filename("", ".png") == "graph.png"


from export import parse_readings, read_csv


def test_read_csv_skips_blank_lines_and_bom(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text("﻿x,y\n1, 2\n\n3,4\n", encoding = "utf-8")
    assert read_csv(path) == [["x", "y"], ["1", "2"], ["3", "4"]]


def test_parse_readings_raw_with_header():
    readings, linearised, skipped = parse_readings([["Length (m)", "Frequency (Hz)"], ["0.5", "100"], ["0.25", "200"]], "1 / Length (1 / m)", "Frequency (Hz)")
    assert readings == [("0.5", "100", ""), ("0.25", "200", "")]
    assert not linearised
    assert skipped == 0


def test_parse_readings_without_header():
    readings, linearised, skipped = parse_readings([["1", "2"], ["3", "4"]], "x", "y")
    assert readings == [("1", "2", ""), ("3", "4", "")]
    assert not linearised


def test_parse_readings_recognises_own_export_header():
    rows = csv_rows(np.array([2.0, 4.0]), np.array([1.0, 2.0]), "1 / Length (1 / m)", "Frequency (Hz)")
    rows = [[str(cell) for cell in row] for row in rows]
    readings, linearised, skipped = parse_readings(rows, "1 / Length (1 / m)", "Frequency (Hz)")
    assert linearised
    assert readings == [("2.0", "1.0", ""), ("4.0", "2.0", "")]


def test_parse_readings_counts_short_rows_as_skipped():
    readings, _, skipped = parse_readings([["x", "y"], ["1"], ["2", "3"], []], "x", "y")
    assert readings == [("2", "3", "")]
    assert skipped == 2


def test_parse_readings_keeps_optional_uncertainty_column():
    readings, _, _ = parse_readings([["x", "y", "± y"], ["1", "2", "0.1"], ["3", "4"]], "x", "y")
    assert readings == [("1", "2", "0.1"), ("3", "4", "")]
