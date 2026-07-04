# test_final_state.py

import os
import json
import subprocess
import pytest

WORKSPACE_DIR = '/home/user/workspace'
LIBPARSER_PATH = os.path.join(WORKSPACE_DIR, 'libparser.so')
RESULT_JSON_PATH = os.path.join(WORKSPACE_DIR, 'result.json')

def test_libparser_so_exists_and_is_shared():
    assert os.path.isfile(LIBPARSER_PATH), f"{LIBPARSER_PATH} does not exist. Did you run make?"

    # Check if it's a shared object
    try:
        output = subprocess.check_output(['file', LIBPARSER_PATH], text=True)
        assert "shared object" in output.lower(), f"{LIBPARSER_PATH} is not a valid shared object. Check your Makefile flags."
    except subprocess.CalledProcessError:
        pytest.fail(f"Failed to run 'file' command on {LIBPARSER_PATH}")

def test_result_json_exists_and_correct():
    assert os.path.isfile(RESULT_JSON_PATH), f"{RESULT_JSON_PATH} does not exist. Did you run test.py?"

    try:
        with open(RESULT_JSON_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{RESULT_JSON_PATH} does not contain valid JSON.")

    expected_key1 = "admin_status_ov"
    expected_val1 = "true"
    expected_key2 = "normal_k"
    expected_val2 = "normal_v"

    assert expected_key1 in data, f"Key '{expected_key1}' not found in result.json. Truncation logic might be incorrect."
    assert data[expected_key1] == expected_val1, f"Expected value for '{expected_key1}' to be '{expected_val1}', got '{data[expected_key1]}'."

    assert expected_key2 in data, f"Key '{expected_key2}' not found in result.json."
    assert data[expected_key2] == expected_val2, f"Expected value for '{expected_key2}' to be '{expected_val2}', got '{data[expected_key2]}'."