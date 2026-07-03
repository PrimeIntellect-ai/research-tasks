# test_final_state.py

import os
import pytest

def test_clean_telemetry_csv_exists_and_content():
    """Test that the clean_telemetry.csv file exists and contains the correct processed data."""
    output_file = "/home/user/output/clean_telemetry.csv"

    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did you run your C++ program?"

    expected_lines = [
        "timestamp,sensor,temperature,status",
        "2023-10-12T08:14:00Z,S100,45.2,active",
        "2023-10-12T08:15:00Z,S101,12.1,ok",
        "2023-10-12T08:16:00Z,S103,59.9,warn"
    ]

    with open(output_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {output_file} does not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )