# test_final_state.py

import os
import json
import pytest

def test_json_file_exists():
    """Test that the clean_summary.json file was created."""
    file_path = "/home/user/clean_summary.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run the Go program?"

def test_json_file_valid_and_correct():
    """Test that clean_summary.json is valid JSON and contains the correct aggregations."""
    file_path = "/home/user/clean_summary.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    # Expected aggregations based on the setup data:
    # alpha:
    # 150.5 (valid)
    # -50.0 (invalid, < 0)
    # 100.5,E01 (invalid, error_code)
    # 49.5 (valid)
    # -> count: 2, sum: 200.0, avg: 100.0
    #
    # beta:
    # 200.0 (valid)
    # 1001.0 (invalid, > 1000)
    # -> count: 1, sum: 200.0, avg: 200.0
    #
    # gamma:
    # 500.0 (valid)
    # -> count: 1, sum: 500.0, avg: 500.0

    assert "alpha" in data, "Missing 'alpha' key in the JSON output."
    assert data["alpha"].get("count") == 2, f"Expected alpha count to be 2, got {data['alpha'].get('count')}"
    assert float(data["alpha"].get("average")) == 100.0, f"Expected alpha average to be 100.0, got {data['alpha'].get('average')}"

    assert "beta" in data, "Missing 'beta' key in the JSON output."
    assert data["beta"].get("count") == 1, f"Expected beta count to be 1, got {data['beta'].get('count')}"
    assert float(data["beta"].get("average")) == 200.0, f"Expected beta average to be 200.0, got {data['beta'].get('average')}"

    assert "gamma" in data, "Missing 'gamma' key in the JSON output."
    assert data["gamma"].get("count") == 1, f"Expected gamma count to be 1, got {data['gamma'].get('count')}"
    assert float(data["gamma"].get("average")) == 500.0, f"Expected gamma average to be 500.0, got {data['gamma'].get('average')}"

    # Ensure no extra unexpected keys
    expected_keys = {"alpha", "beta", "gamma"}
    actual_keys = set(data.keys())
    assert actual_keys == expected_keys, f"Expected keys {expected_keys}, but got {actual_keys}"