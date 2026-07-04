# test_final_state.py

import os
import json
import pytest

def test_fixed_metrics_json_exists():
    json_path = "/home/user/fixed_metrics.json"
    assert os.path.exists(json_path), f"Output file {json_path} is missing. Did you run the script?"
    assert os.path.isfile(json_path), f"Path {json_path} is not a file."

def test_fixed_metrics_json_content():
    json_path = "/home/user/fixed_metrics.json"
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON root to be a list, but got {type(data).__name__}."
    assert len(data) == 4, f"Expected 4 records in the JSON output, but found {len(data)}."

    expected_data = [
        {"id": 1, "job_name": "DB_PROD_FULL", "size": 1000, "running_total": 1000},
        {"id": 2, "job_name": "DB_PROD_INC_1", "size": 100, "running_total": 1100},
        {"id": 3, "job_name": "DB_PROD_INC_2", "size": 150, "running_total": 1250},
        {"id": 4, "job_name": "DB_PROD_INC_3", "size": 120, "running_total": 1370}
    ]

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Record at index {i} is not a dictionary."

        # Check keys
        expected_keys = {"id", "job_name", "size", "running_total"}
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Record at index {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual["id"] == expected["id"], f"Record at index {i}: Expected id {expected['id']}, got {actual['id']}."
        assert actual["job_name"] == expected["job_name"], f"Record at index {i}: Expected job_name '{expected['job_name']}', got '{actual['job_name']}'."
        assert actual["size"] == expected["size"], f"Record at index {i}: Expected size {expected['size']}, got {actual['size']}."
        assert actual["running_total"] == expected["running_total"], f"Record at index {i}: Expected running_total {expected['running_total']}, got {actual['running_total']}."