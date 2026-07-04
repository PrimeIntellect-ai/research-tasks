# test_final_state.py

import os
import json
import pytest

def test_pipeline_log_exists_and_not_empty():
    """Check that the logging requirement was met."""
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file missing at {log_path}"
    assert os.path.getsize(log_path) > 0, f"Log file {log_path} is empty."

def test_similarities_json_structure_and_values():
    """Check that the similarities.json file exists, is valid JSON, and has the correct distances."""
    json_path = "/home/user/similarities.json"
    assert os.path.isfile(json_path), f"Output JSON file missing at {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "distances" in data, "JSON must contain a 'distances' key at the root."
    distances = data["distances"]

    expected_keys = {"Device_B", "Device_C", "Device_D", "Device_E"}
    actual_keys = set(distances.keys())
    assert actual_keys == expected_keys, f"Expected devices {expected_keys}, but got {actual_keys}"

    # Expected values derived from the deterministic setup
    expected_values = {
        "Device_B": 0.78,
        "Device_C": 3.88,
        "Device_D": 10.95,
        "Device_E": 12.22
    }

    for device, expected_val in expected_values.items():
        actual_val = distances[device]
        assert isinstance(actual_val, (int, float)), f"Value for {device} must be a number."
        # Allow a small floating point tolerance due to potential minor differences in pandas/numpy versions,
        # but the task requires rounding to exactly 2 decimal places.
        assert abs(actual_val - expected_val) <= 0.05, \
            f"Expected distance for {device} to be near {expected_val}, but got {actual_val}"