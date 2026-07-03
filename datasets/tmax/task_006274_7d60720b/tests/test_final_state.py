# test_final_state.py

import os
import pytest

def test_processed_sensors_csv():
    file_path = "/home/user/processed_sensors.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    expected_content = """timestamp,sensor_id,normalized_value
2023-10-01T10:00:00Z,temp_A,0.0000
2023-10-01T10:00:00Z,temp_B,0.0000
2023-10-01T10:00:00Z,temp_C,0.0000
2023-10-01T10:01:00Z,temp_A,0.0000
2023-10-01T10:01:00Z,temp_B,0.2500
2023-10-01T10:01:00Z,temp_C,0.9091
2023-10-01T10:02:00Z,temp_A,0.5000
2023-10-01T10:02:00Z,temp_B,0.2500
2023-10-01T10:02:00Z,temp_C,0.9545
2023-10-01T10:03:00Z,temp_A,1.0000
2023-10-01T10:03:00Z,temp_B,1.0000
2023-10-01T10:03:00Z,temp_C,1.0000"""

    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Content of {file_path} does not match expected output."

def test_sensor_report_md():
    file_path = "/home/user/sensor_report.md"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    expected_content = """# Sensor Report

## Sensor temp_A
- Min: 20.5
- Max: 21.5
- Data Points: 4
- Latest Normalized: 1.0000

## Sensor temp_B
- Min: 15.0
- Max: 15.8
- Data Points: 4
- Latest Normalized: 1.0000

## Sensor temp_C
- Min: 0.0
- Max: 11.0
- Data Points: 4
- Latest Normalized: 1.0000"""

    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Content of {file_path} does not match expected output."