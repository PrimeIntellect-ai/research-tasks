# test_final_state.py

import os
import pytest

def test_anomalies_csv_exists_and_correct():
    file_path = "/home/user/anomalies.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = """timestamp,sensor_id,value,rolling_avg
1004,S1,30.00,11.00
1008,S2,110.00,51.00
1010,S1,50.00,18.67"""

    # Compare line by line to give a better error message
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in anomalies.csv, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i + 1}:\nExpected: {expected}\nActual:   {actual}"