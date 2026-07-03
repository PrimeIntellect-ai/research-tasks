# test_final_state.py

import os
import json
import pytest

def test_metadata_file_exists():
    """Test that the degradation_metadata.json file was created."""
    file_path = "/home/user/degradation_metadata.json"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} exists but is not a file."

def test_metadata_structure_and_types():
    """Test that the metadata JSON has the exact required keys and float values."""
    file_path = "/home/user/degradation_metadata.json"
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} is not valid JSON.")

    expected_keys = {"a", "b", "c", "b_ci_lower", "b_ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, but found {set(data.keys())}."

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

def test_metadata_values_plausible():
    """Test that the fitted parameters are close to the expected true parameters."""
    file_path = "/home/user/degradation_metadata.json"
    with open(file_path, 'r') as f:
        data = json.load(f)

    # True parameters are approximately a=1.5, b=0.005, c=0.2
    # We allow a generous margin since noise is added and we cannot re-run scipy in stdlib
    assert 1.0 < data["a"] < 2.0, f"Parameter 'a' ({data['a']}) is outside the expected range."
    assert 0.001 < data["b"] < 0.01, f"Parameter 'b' ({data['b']}) is outside the expected range."
    assert 0.0 < data["c"] < 0.5, f"Parameter 'c' ({data['c']}) is outside the expected range."

    # Confidence interval checks
    assert data["b_ci_lower"] < data["b"], "b_ci_lower should be less than the estimate of b."
    assert data["b_ci_upper"] > data["b"], "b_ci_upper should be greater than the estimate of b."
    assert data["b_ci_lower"] > 0, "b_ci_lower should be positive."
    assert data["b_ci_upper"] < 0.02, "b_ci_upper is unexpectedly large."