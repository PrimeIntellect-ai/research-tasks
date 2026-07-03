# test_final_state.py

import os
import pytest

def test_clean_stats_csv_exists_and_content():
    """Check if the output file exists and has the correct deduplicated rolling averages."""
    output_path = "/home/user/clean_stats.csv"

    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_lines = [
        "id,rolling_cpu",
        "1,50.00",
        "2,55.00",
        "3,60.00",
        "4,50.00",
        "5,40.00",
        "6,30.00",
        "7,50.00",
        "8,45.00"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_path}, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."