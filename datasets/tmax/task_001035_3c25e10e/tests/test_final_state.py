# test_final_state.py

import os
import json
import pytest

MINIMAL_JSON_PATH = "/home/user/minimal.json"

def test_minimal_json_exists():
    assert os.path.isfile(MINIMAL_JSON_PATH), f"Expected file {MINIMAL_JSON_PATH} does not exist. Did you save your result?"

def test_minimal_json_content():
    try:
        with open(MINIMAL_JSON_PATH, 'r') as f:
            result = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {MINIMAL_JSON_PATH} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {MINIMAL_JSON_PATH}: {e}")

    assert "data" in result, f"JSON in {MINIMAL_JSON_PATH} is missing the 'data' key."
    assert isinstance(result["data"], list), f"The 'data' key in {MINIMAL_JSON_PATH} must be a list."

    expected_data = [2, 17, 41]
    actual_data = result["data"]

    assert actual_data == expected_data, f"Expected data array to be {expected_data}, but got {actual_data}. Make sure it is the minimal crashing payload and sorted in ascending order."