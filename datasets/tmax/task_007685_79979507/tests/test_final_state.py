# test_final_state.py

import os
import json
import math
import pytest

def test_experiment_json_exists_and_correct():
    """Verify that experiment.json exists and contains the correct summary metrics."""
    log_path = "/home/user/logs/experiment.json"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {log_path} is not valid JSON.")

    expected = {
        "total_rows": 5,
        "outliers_capped": 2,
        "missing_filled": 2
    }

    assert "total_rows" in data, "Missing key 'total_rows' in experiment.json"
    assert "outliers_capped" in data, "Missing key 'outliers_capped' in experiment.json"
    assert "missing_filled" in data, "Missing key 'missing_filled' in experiment.json"

    assert data["total_rows"] == expected["total_rows"], f"Expected total_rows to be {expected['total_rows']}, got {data['total_rows']}"
    assert data["outliers_capped"] == expected["outliers_capped"], f"Expected outliers_capped to be {expected['outliers_capped']}, got {data['outliers_capped']}"
    assert data["missing_filled"] == expected["missing_filled"], f"Expected missing_filled to be {expected['missing_filled']}, got {data['missing_filled']}"

def test_clean_sensors_jsonl_exists_and_correct():
    """Verify that clean_sensors.jsonl exists and contains the correct transformed data."""
    output_path = "/home/user/data/clean_sensors.jsonl"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    expected_lines = [
        {"timestamp": 1600000000, "sensor_proj": 21.0, "sensor_c": 50.0},
        {"timestamp": 1600000001, "sensor_proj": 17.6, "sensor_c": 100.0},
        {"timestamp": 1600000002, "sensor_proj": 6.0, "sensor_c": 40.0},
        {"timestamp": 1600000003, "sensor_proj": 27.5, "sensor_c": 100.0},
        {"timestamp": 1600000004, "sensor_proj": 22.3, "sensor_c": 90.0}
    ]

    parsed_lines = []
    with open(output_path, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed_lines.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {output_path} is not valid JSON.")

    assert len(parsed_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_path}, got {len(parsed_lines)}."

    for i, (actual, expected) in enumerate(zip(parsed_lines, expected_lines)):
        assert "timestamp" in actual, f"Line {i+1} missing 'timestamp' key."
        assert "sensor_proj" in actual, f"Line {i+1} missing 'sensor_proj' key."
        assert "sensor_c" in actual, f"Line {i+1} missing 'sensor_c' key."

        assert actual["timestamp"] == expected["timestamp"], f"Line {i+1} timestamp mismatch."
        assert math.isclose(actual["sensor_proj"], expected["sensor_proj"], rel_tol=1e-5), f"Line {i+1} sensor_proj mismatch. Expected {expected['sensor_proj']}, got {actual['sensor_proj']}."
        assert math.isclose(actual["sensor_c"], expected["sensor_c"], rel_tol=1e-5), f"Line {i+1} sensor_c mismatch. Expected {expected['sensor_c']}, got {actual['sensor_c']}."