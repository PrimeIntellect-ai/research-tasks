# test_final_state.py

import os
import pytest

PROCESSED_SENSORS_PATH = "/home/user/processed_sensors.csv"

def test_processed_sensors_exists():
    assert os.path.exists(PROCESSED_SENSORS_PATH), f"File {PROCESSED_SENSORS_PATH} is missing. Did you run your C++ program and output to the correct path?"
    assert os.path.isfile(PROCESSED_SENSORS_PATH), f"{PROCESSED_SENSORS_PATH} should be a file."

def test_processed_sensors_content():
    expected_content = """timestamp,sensor_id,temperature,humidity,temp_rollavg,hum_rollavg
1000000000,S1,20.00,50.00,20.00,50.00
1000000060,S1,21.00,52.00,20.50,51.00
1000000120,S1,22.00,54.00,21.00,52.00
1000000180,S1,23.00,56.00,21.50,53.00
1000000240,S1,24.00,58.00,22.00,54.00
1000000000,S2,10.00,80.00,10.00,80.00
1000000060,S2,12.00,82.00,11.00,81.00
1000000120,S2,14.00,84.00,12.00,82.00
1000000180,S2,16.00,86.00,13.00,83.00
1000000240,S2,18.00,88.00,14.00,84.00"""

    with open(PROCESSED_SENSORS_PATH, "r") as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(actual_lines)} lines in {PROCESSED_SENSORS_PATH}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1}:\nExpected: {expected}\nActual:   {actual}"