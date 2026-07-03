# test_final_state.py
import os
import json
import pytest

JSON_PATH = '/home/user/optimal_path.json'
EXPECTED_PATH = ["gateway-alpha", "router-b", "switch-d", "storage-omega"]

def test_optimal_path_json_exists():
    assert os.path.exists(JSON_PATH), f"The output file {JSON_PATH} does not exist."
    assert os.path.isfile(JSON_PATH), f"The path {JSON_PATH} is not a file."

def test_optimal_path_json_content():
    assert os.path.exists(JSON_PATH), f"Cannot check content, {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {JSON_PATH} as JSON: {e}")

    assert isinstance(data, list), f"Expected JSON root to be a list, but got {type(data).__name__}."
    assert data == EXPECTED_PATH, f"The computed optimal path is incorrect. Expected {EXPECTED_PATH}, but got {data}."