# test_final_state.py
import os
import json
import pytest

def test_final_metrics_json_exists():
    """Test that the final_metrics.json file was created."""
    path = '/home/user/analysis/final_metrics.json'
    assert os.path.isfile(path), f"Output file {path} is missing."

def test_final_metrics_json_structure():
    """Test that the JSON file contains the correct structure and data types."""
    path = '/home/user/analysis/final_metrics.json'
    if not os.path.isfile(path):
        pytest.fail(f"Output file {path} is missing.")

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("final_metrics.json is not valid JSON.")

    assert "kde_at_05" in data, "Key 'kde_at_05' not found in JSON."

    results = data["kde_at_05"]
    assert isinstance(results, list), "'kde_at_05' should be a list."
    assert len(results) == 100, f"Expected exactly 100 values in 'kde_at_05', got {len(results)}."

    for i, val in enumerate(results):
        assert isinstance(val, (int, float)), f"Value at index {i} is not a number: {val}"