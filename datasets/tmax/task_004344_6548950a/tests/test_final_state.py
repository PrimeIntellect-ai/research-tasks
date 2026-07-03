# test_final_state.py
import os
import json
import pytest

METRICS_FILE = "/home/user/metrics.json"

def test_metrics_file_exists():
    """Check if the metrics.json file was created."""
    assert os.path.isfile(METRICS_FILE), f"File {METRICS_FILE} does not exist. The Rust program must create it."

def test_metrics_json_structure_and_values():
    """Check if the metrics.json file has the correct structure and values."""
    assert os.path.isfile(METRICS_FILE), f"File {METRICS_FILE} does not exist."

    with open(METRICS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {METRICS_FILE} as JSON: {e}")

    assert "l2_norm" in data, "The JSON file is missing the 'l2_norm' key."
    assert "compute_time_us" in data, "The JSON file is missing the 'compute_time_us' key."

    l2_norm = data["l2_norm"]
    time_us = data["compute_time_us"]

    assert isinstance(l2_norm, (int, float)), f"'l2_norm' must be a number, got {type(l2_norm).__name__}"
    assert isinstance(time_us, int), f"'compute_time_us' must be an integer, got {type(time_us).__name__}"
    assert not isinstance(time_us, bool), "'compute_time_us' must be an integer, not a boolean"

    assert time_us >= 0, f"'compute_time_us' should be non-negative, got {time_us}"

    # Expected L2 norm is sqrt(1_000_000 * 2.0^2) = 2000.0
    expected_norm = 2000.0
    assert abs(l2_norm - expected_norm) < 0.1, f"Incorrect L2 norm. Expected ~{expected_norm}, got {l2_norm}"