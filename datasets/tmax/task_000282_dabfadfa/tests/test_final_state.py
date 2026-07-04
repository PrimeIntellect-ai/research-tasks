# test_final_state.py

import os
import json
import pytest

def test_analyzer_go_exists():
    """Test that the Go program exists at the specified location."""
    file_path = "/home/user/analyzer.go"
    assert os.path.exists(file_path), f"Missing Go program: {file_path}"
    assert os.path.isfile(file_path), f"Expected a file, but found a directory: {file_path}"

def test_results_json_exists_and_valid():
    """Test that the results.json file exists and has the correct schema and values."""
    file_path = "/home/user/results.json"
    assert os.path.exists(file_path), f"Missing results file: {file_path}"
    assert os.path.isfile(file_path), f"Expected a file, but found a directory: {file_path}"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {file_path} is not valid JSON.")

    required_keys = {"exact_mean", "bootstrap_mean", "ci_lower", "ci_upper", "reject_null"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    # Validate exact_mean
    exact_mean = data['exact_mean']
    assert isinstance(exact_mean, (int, float)), "exact_mean must be a number"
    assert abs(exact_mean - 1366.032) < 0.1, f"Exact mean incorrect. Expected ~1366.032, got: {exact_mean}"

    # Validate bootstrap_mean
    bootstrap_mean = data['bootstrap_mean']
    assert isinstance(bootstrap_mean, (int, float)), "bootstrap_mean must be a number"
    assert abs(bootstrap_mean - 1366.032) < 50, f"Bootstrap mean too far from exact mean. Got: {bootstrap_mean}"

    # Validate confidence intervals
    ci_lower = data['ci_lower']
    ci_upper = data['ci_upper']
    assert isinstance(ci_lower, (int, float)), "ci_lower must be a number"
    assert isinstance(ci_upper, (int, float)), "ci_upper must be a number"

    assert 400 < ci_lower < 900, f"ci_lower out of expected bounds (400, 900): {ci_lower}"
    assert 1800 < ci_upper < 2500, f"ci_upper out of expected bounds (1800, 2500): {ci_upper}"
    assert ci_lower < ci_upper, f"ci_lower ({ci_lower}) should be less than ci_upper ({ci_upper})"

    # Validate reject_null logic
    reject_null = data['reject_null']
    assert isinstance(reject_null, bool), "reject_null must be a boolean"
    expected_reject = ci_lower > 600
    assert reject_null == expected_reject, f"reject_null logic incorrect. Based on ci_lower ({ci_lower}), expected {expected_reject}, got {reject_null}"