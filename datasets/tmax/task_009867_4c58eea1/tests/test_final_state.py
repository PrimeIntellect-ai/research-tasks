# test_final_state.py

import os
import json
import pytest

def test_posterior_means_exists():
    """Test that the posterior_means.json file exists."""
    file_path = '/home/user/posterior_means.json'
    assert os.path.isfile(file_path), f"Required output file {file_path} is missing."

def test_posterior_means_format_and_values():
    """Test that the JSON file has the correct format and values within the expected range."""
    file_path = '/home/user/posterior_means.json'
    assert os.path.isfile(file_path), f"Required output file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not a valid JSON.")

    assert "alpha" in data, "Key 'alpha' is missing from the JSON output."
    assert "beta" in data, "Key 'beta' is missing from the JSON output."

    alpha = data["alpha"]
    beta = data["beta"]

    assert isinstance(alpha, (int, float)), f"Expected 'alpha' to be a number, got {type(alpha)}."
    assert isinstance(beta, (int, float)), f"Expected 'beta' to be a number, got {type(beta)}."

    assert 1.80 <= alpha <= 2.20, f"Alpha value {alpha} is out of the expected range [1.80, 2.20]."
    assert 0.05 <= beta <= 0.15, f"Beta value {beta} is out of the expected range [0.05, 0.15]."