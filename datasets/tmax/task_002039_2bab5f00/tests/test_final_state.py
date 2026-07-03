# test_final_state.py

import os
import json
import pytest

def test_spectral_result_exists():
    """Test that the spectral_result.json file was created."""
    file_path = "/home/user/spectral_result.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The Rust program did not create the output file."

def test_spectral_result_content():
    """Test that the spectral_result.json file contains the correct extracted parameters."""
    file_path = "/home/user/spectral_result.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert "k" in data, "The JSON result is missing the 'k' key."
    assert "A" in data, "The JSON result is missing the 'A' key."
    assert "phi" in data, "The JSON result is missing the 'phi' key."

    # Expected values derived from the sequence
    expected_k = 16
    expected_A = 1.80
    expected_phi = 2.55

    assert data["k"] == expected_k, f"Expected k to be {expected_k}, but got {data['k']}."

    # Check A and phi with a small tolerance for floating point variations, 
    # though they should be exactly rounded to 2 decimal places.
    assert abs(data["A"] - expected_A) < 1e-3, f"Expected A to be {expected_A}, but got {data['A']}."
    assert abs(data["phi"] - expected_phi) < 1e-3, f"Expected phi to be {expected_phi}, but got {data['phi']}."