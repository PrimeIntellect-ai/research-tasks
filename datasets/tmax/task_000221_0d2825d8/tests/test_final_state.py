# test_final_state.py
import os
import json
import pytest

def test_telemetry_success_file_exists():
    file_path = '/home/user/build_telemetry/telemetry_success.json'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist. Did the C program run successfully and send the POST request?"

def test_telemetry_success_content():
    file_path = '/home/user/build_telemetry/telemetry_success.json'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_data = {
        "apk_size": 15400230,
        "dex_count": 3,
        "lint_errors": 12
    }

    for key, expected_value in expected_data.items():
        assert key in data, f"Missing key '{key}' in the telemetry JSON output."
        assert data[key] == expected_value, f"Expected '{key}' to be {expected_value}, but got {data[key]}."

    assert len(data) == len(expected_data), f"Expected exactly {len(expected_data)} keys in the JSON output, but found {len(data)}."