# test_final_state.py

import os
import json
import pytest
import math

def test_summary_json_exists():
    """Check if the output summary file exists."""
    assert os.path.isfile("/home/user/summary.json"), "The file /home/user/summary.json does not exist."

def test_summary_json_content():
    """Validate the structure and values of the summary JSON file."""
    file_path = "/home/user/summary.json"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_keys = {"valid_count", "invalid_count", "average_joint_prob"}
    actual_keys = set(data.keys())

    assert expected_keys.issubset(actual_keys), f"Missing keys in summary.json. Expected: {expected_keys}, Found: {actual_keys}"

    assert data["valid_count"] == 5, f"Expected valid_count to be 5, but got {data['valid_count']}."
    assert data["invalid_count"] == 3, f"Expected invalid_count to be 3, but got {data['invalid_count']}."

    # Use pytest.approx or math.isclose to handle float precision issues
    expected_avg = 0.332
    actual_avg = data["average_joint_prob"]
    assert math.isclose(actual_avg, expected_avg, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected average_joint_prob to be near {expected_avg}, but got {actual_avg}."

def test_go_script_exists():
    """Check if the Go pipeline script was created."""
    assert os.path.isfile("/home/user/etl_pipeline.go"), "The Go script /home/user/etl_pipeline.go does not exist."