# test_final_state.py

import os
import json
import pytest

def test_detect_deadlocks_script_exists():
    script_path = "/home/user/detect_deadlocks.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_deadlocks_json_exists_and_correct():
    json_path = "/home/user/deadlocks.json"
    assert os.path.exists(json_path), f"The output file {json_path} does not exist."
    assert os.path.isfile(json_path), f"The path {json_path} is not a file."

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_deadlocks = ["T1", "T2", "T3", "T4", "T5"]

    assert isinstance(data, list), f"Expected the JSON output to be a list, but got {type(data).__name__}."
    assert data == expected_deadlocks, f"The deadlocks list is incorrect. Expected {expected_deadlocks}, but got {data}."