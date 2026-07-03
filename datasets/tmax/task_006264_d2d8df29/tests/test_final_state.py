# test_final_state.py
import os
import json
import pytest

def test_fixed_script_exists_and_executable():
    script_path = "/home/user/process_metrics_fixed.sh"
    assert os.path.isfile(script_path), f"The fixed script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_decoded_metrics_json_is_valid_and_correct():
    json_path = "/home/user/decoded_metrics.json"
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"The file {json_path} does not contain valid JSON: {e}")

    expected_data = [
        {
            "id": "1",
            "metric": "CPU_LOAD=80%"
        },
        {
            "id": "2",
            "metric": "MEMORY_USAGE=4GB"
        },
        {
            "id": "3",
            "metric": "AABBB"
        },
        {
            "id": "4",
            "metric": "ERROR=\"Out of memory\""
        }
    ]

    assert isinstance(data, list), "The JSON root must be a list (array)."
    assert len(data) == 4, f"Expected 4 items in the JSON array, found {len(data)}."

    for i, expected_item in enumerate(expected_data):
        assert data[i] == expected_item, f"Item at index {i} does not match the expected output. Expected: {expected_item}, Got: {data[i]}"