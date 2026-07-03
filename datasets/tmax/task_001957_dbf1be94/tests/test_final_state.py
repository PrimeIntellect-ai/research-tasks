# test_final_state.py
import os
import json
import math
import pytest

def test_histogram_exists():
    """Verify that the histogram image was created."""
    file_path = "/home/user/response_histogram.png"
    assert os.path.isfile(file_path), f"File not found: {file_path}"
    assert os.path.getsize(file_path) > 0, f"File is empty: {file_path}"

def test_simulation_results_json():
    """Verify the JSON file contains the correct statistics."""
    file_path = "/home/user/simulation_results.json"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert "mean_R" in data, "Key 'mean_R' missing from JSON."
    assert "std_R" in data, "Key 'std_R' missing from JSON."

    # Expected values derived from the deterministic random seed (42)
    expected_mean_R = 0.0210086
    expected_std_R = 0.0033199

    mean_R = data["mean_R"]
    std_R = data["std_R"]

    assert isinstance(mean_R, (int, float)), "'mean_R' must be a number."
    assert isinstance(std_R, (int, float)), "'std_R' must be a number."

    assert math.isclose(mean_R, expected_mean_R, abs_tol=1e-4), \
        f"Expected mean_R ~ {expected_mean_R}, got {mean_R}"
    assert math.isclose(std_R, expected_std_R, abs_tol=1e-4), \
        f"Expected std_R ~ {expected_std_R}, got {std_R}"