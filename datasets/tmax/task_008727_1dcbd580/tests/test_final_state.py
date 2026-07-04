# test_final_state.py

import os
import json
import pytest

def test_results_file_exists():
    """Check if the results JSON file was created."""
    file_path = '/home/user/results/params.json'
    assert os.path.exists(file_path), f"Expected results file {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a valid file."

def test_results_content():
    """Verify the content of the results JSON file."""
    file_path = '/home/user/results/params.json'
    assert os.path.exists(file_path), f"Cannot check content, {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    # Check for required keys
    for key in ['A', 't0', 'sigma']:
        assert key in data, f"Key '{key}' is missing from the results JSON."
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

    # Check if values are within the expected tolerance
    assert 0.045 < data['A'] < 0.055, f"Value for A ({data['A']}) is outside the expected range (0.045 - 0.055)."
    assert 4.45 < data['t0'] < 4.55, f"Value for t0 ({data['t0']}) is outside the expected range (4.45 - 4.55)."
    assert 0.25 < data['sigma'] < 0.35, f"Value for sigma ({data['sigma']}) is outside the expected range (0.25 - 0.35)."