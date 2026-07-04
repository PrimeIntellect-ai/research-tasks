# test_final_state.py

import json
import os
import pytest

def test_results_json_exists():
    """Check if the results.json file exists."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Missing results file: {results_path}"

def test_results_json_content():
    """Check the content of results.json against expected values."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), "results.json does not exist."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    assert "weights" in data, "Missing 'weights' key in results.json"
    assert "residual_mean" in data, "Missing 'residual_mean' key in results.json"
    assert "residual_std" in data, "Missing 'residual_std' key in results.json"

    weights = data['weights']
    mean = data['residual_mean']
    std = data['residual_std']

    assert isinstance(weights, list), "'weights' must be a list"
    assert len(weights) == 5, f"Expected 5 weights, got {len(weights)}"

    expected_weights = [1.5, 0.0, 0.8, 2.2, 0.0]
    for i, (w, ew) in enumerate(zip(weights, expected_weights)):
        assert isinstance(w, (int, float)), f"Weight at index {i} must be a float"
        assert abs(w - ew) < 0.1, f"Weight at index {i} ({w}) does not match expected {ew} within 0.1 tolerance"

    assert isinstance(mean, (int, float)), "'residual_mean' must be a float"
    assert abs(mean - 0.0) < 0.05, f"Mean {mean} is too far from expected 0.0 (tolerance 0.05)"

    assert isinstance(std, (int, float)), "'residual_std' must be a float"
    assert abs(std - 0.05) < 0.02, f"Std {std} is too far from expected 0.05 (tolerance 0.02)"