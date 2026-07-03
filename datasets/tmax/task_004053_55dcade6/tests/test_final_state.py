# test_final_state.py

import os
import json
import pytest

def test_root_cause_json_exists_and_correct():
    file_path = "/home/user/root_cause.json"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} is not valid JSON.")

    expected_data = {
        "api_key": "sk_live_9a8b7c6d5e4f3g2h1i0j",
        "deletion_time": "2023-10-27T03:01:15Z",
        "crash_time": "2023-10-27T03:01:18Z",
        "crash_line": 42
    }

    for key, expected_value in expected_data.items():
        assert key in data, f"Missing key '{key}' in {file_path}."
        assert data[key] == expected_value, f"Incorrect value for '{key}'. Expected {expected_value}, got {data[key]}."