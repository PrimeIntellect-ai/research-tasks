# test_final_state.py

import os
import json
import pytest

OUTPUT_DIR = '/home/user/output'
OUTPUT_FILE = '/home/user/output/processed_sensors.jsonl'

def test_output_directory_exists():
    """Verify that the output directory was created."""
    assert os.path.isdir(OUTPUT_DIR), f"The output directory {OUTPUT_DIR} does not exist."

def test_output_file_exists():
    """Verify that the output JSON Lines file exists."""
    assert os.path.isfile(OUTPUT_FILE), f"The output file {OUTPUT_FILE} does not exist."

def test_output_file_content():
    """Verify that the output file contains the correct JSON objects in the correct order."""
    expected = [
        {"timestamp": "2023-10-01T09:59:00Z", "sensor_id": "S5", "temp_rolling_avg": 10.0, "notes": "Early reading"},
        {"timestamp": "2023-10-01T10:00:00Z", "sensor_id": "S1", "temp_rolling_avg": 15.0, "notes": "All good"},
        {"timestamp": "2023-10-01T10:03:00Z", "sensor_id": "S3", "temp_rolling_avg": 18.67, "notes": "Normal"},
        {"timestamp": "2023-10-01T10:05:00Z", "sensor_id": "S1", "temp_rolling_avg": 22.33, "notes": "Okay"},
        {"timestamp": "2023-10-01T10:06:00Z", "sensor_id": "S3", "temp_rolling_avg": 21.67, "notes": "Cooling"}
    ]

    actual = []
    with open(OUTPUT_FILE, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                actual.append(data)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {OUTPUT_FILE} is not valid JSON: {line}")

    assert len(actual) == len(expected), f"Expected {len(expected)} records, but found {len(actual)} in {OUTPUT_FILE}."

    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act == exp, f"Record at index {i} does not match expected.\nExpected: {exp}\nActual: {act}"