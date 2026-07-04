# test_final_state.py

import os
import pytest

def test_output_fixed_csv_exists():
    output_file = "/home/user/calc_metrics/output_fixed.csv"
    assert os.path.isfile(output_file), f"The output file '{output_file}' does not exist. Did you run the compiled program and save the output?"

def test_output_fixed_csv_contents():
    output_file = "/home/user/calc_metrics/output_fixed.csv"

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected = """1,2.0000
2,0.0000
3,0.0000
4,4.0000
5,0.2500
6,0.0000
---HISTOGRAM---
0:4
1:0
2:1
3:0
4:1
5:0
6:0
7:0
8:0
9:0"""

    expected_lines = [line.strip() for line in expected.splitlines() if line.strip()]
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output_fixed.csv, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} of output_fixed.csv is incorrect. Expected '{expected}', got '{actual}'."