# test_final_state.py

import os
import json
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/detect_deadlocks.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_json_output_exists_and_correct():
    json_path = "/home/user/deadlocks.json"
    assert os.path.exists(json_path), f"Output file {json_path} does not exist."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected_deadlocks = ["T100", "T101", "T102", "T107", "T108", "T109"]

    assert isinstance(data, list), f"JSON output should be a list, got {type(data).__name__}."
    assert sorted(data) == sorted(expected_deadlocks), f"JSON output does not match expected deadlocked transactions. Expected: {expected_deadlocks}, Got: {data}"

    # Check if it's sorted alphabetically as requested
    assert data == sorted(data), "The JSON array is not sorted alphabetically."