# test_final_state.py

import os
import json
import pytest

def test_results_file_exists():
    """Test that the results.json file exists in the correct location."""
    file_path = '/home/user/results.json'
    assert os.path.exists(file_path), f"File {file_path} is missing. The script must generate this file."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_results_file_content():
    """Test that the results.json file contains the correct keys and valid values."""
    file_path = '/home/user/results.json'

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not a valid JSON file.")

    assert "convergence_error" in data, "Key 'convergence_error' is missing from results.json."
    assert "wasserstein_distance" in data, "Key 'wasserstein_distance' is missing from results.json."

    conv_err = data["convergence_error"]
    wass_dist = data["wasserstein_distance"]

    assert isinstance(conv_err, (int, float)), "'convergence_error' must be a number."
    assert isinstance(wass_dist, (int, float)), "'wasserstein_distance' must be a number."

    # Check if the values are within the expected tolerance bands
    assert 0.0 < conv_err < 0.05, f"'convergence_error' ({conv_err}) is outside the expected range (0.0, 0.05)."
    assert 0.0 <= wass_dist < 0.1, f"'wasserstein_distance' ({wass_dist}) is outside the expected range [0.0, 0.1)."