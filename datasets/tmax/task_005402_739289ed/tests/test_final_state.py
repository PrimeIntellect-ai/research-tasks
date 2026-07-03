# test_final_state.py

import os
import math

def test_peak_params_exists():
    """Check that the output file was created."""
    file_path = '/home/user/peak_params.csv'
    assert os.path.isfile(file_path), f"Error: {file_path} not found."

def test_peak_params_validity():
    """Check that the output file contains valid numbers within expected bounds."""
    file_path = '/home/user/peak_params.csv'
    assert os.path.isfile(file_path), f"Error: {file_path} not found."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 3, f"Error: Expected 3 comma-separated values, got {len(parts)} in '{content}'"

    try:
        a = float(parts[0])
        mu = float(parts[1])
        sigma_sq = float(parts[2])
    except ValueError:
        assert False, f"Error: Could not parse values as floats. Got: '{content}'"

    assert not math.isnan(a), "Error: Amplitude (A) is NaN."
    assert not math.isnan(mu), "Error: Mean_Frequency (mu) is NaN."
    assert not math.isnan(sigma_sq), "Error: Variance (sigma_sq) is NaN."

    assert 45.0 < a < 55.0, f"Error: Amplitude (A) out of bounds. Expected 45.0 < A < 55.0, got {a}"
    assert 95.0 < mu < 105.0, f"Error: Mean_Frequency (mu) out of bounds. Expected 95.0 < mu < 105.0, got {mu}"
    assert 2.0 < sigma_sq < 6.0, f"Error: Variance (sigma_sq) out of bounds. Expected 2.0 < sigma_sq < 6.0, got {sigma_sq}"