# test_final_state.py

import os
import json
import math
import pytest

def test_rust_project_created():
    """Verify that the Rust project was created using Cargo."""
    cargo_toml_path = "/home/user/gc_estimator/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Rust project configuration {cargo_toml_path} does not exist. Did you create the project?"

def test_json_output_exists():
    """Verify that the output JSON file exists."""
    json_path = "/home/user/gc_distribution.json"
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

def test_json_output_content():
    """Verify that the JSON output contains the correct mean and std_dev."""
    json_path = "/home/user/gc_distribution.json"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "mean" in data, "JSON output is missing the 'mean' key."
    assert "std_dev" in data, "JSON output is missing the 'std_dev' key."

    # Expected values
    expected_mean = 3 / 7
    expected_variance = (0 + (4/7)**2 + (-3/7)**2 + (-1/7)**2) / 4
    expected_std_dev = math.sqrt(expected_variance)

    actual_mean = data["mean"]
    actual_std_dev = data["std_dev"]

    assert isinstance(actual_mean, float), "'mean' must be a float."
    assert isinstance(actual_std_dev, float), "'std_dev' must be a float."

    assert math.isclose(actual_mean, expected_mean, rel_tol=1e-7, abs_tol=1e-9), \
        f"Expected mean to be close to {expected_mean}, but got {actual_mean}."

    assert math.isclose(actual_std_dev, expected_std_dev, rel_tol=1e-7, abs_tol=1e-9), \
        f"Expected std_dev to be close to {expected_std_dev}, but got {actual_std_dev}."