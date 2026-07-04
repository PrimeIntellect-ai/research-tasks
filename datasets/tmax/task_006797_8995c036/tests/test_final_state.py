# test_final_state.py
import os
import json
import pytest

def test_summary_json_exists():
    summary_path = "/home/user/rust_log_parser/summary.json"
    assert os.path.isfile(summary_path), f"The file {summary_path} does not exist. Did you run the main.py script?"

def test_summary_json_content():
    summary_path = "/home/user/rust_log_parser/summary.json"

    try:
        with open(summary_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {summary_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected the JSON in {summary_path} to be a list, but got {type(data).__name__}."
    assert len(data) == 2, f"Expected exactly 2 errors in {summary_path}, but found {len(data)}. The state machine bug might not be fully fixed."

    codes = [item.get("code") for item in data if isinstance(item, dict)]
    assert "E0596" in codes, "Expected error code 'E0596' to be present in the parsed errors."
    assert "E0382" in codes, "Expected error code 'E0382' to be present in the parsed errors."