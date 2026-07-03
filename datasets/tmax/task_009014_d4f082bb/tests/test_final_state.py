# test_final_state.py

import os
import re
import pytest

def test_fit_results_exists():
    """Check if the results file was created."""
    file_path = "/home/user/fit_results.txt"
    assert os.path.exists(file_path), f"The expected output file '{file_path}' does not exist."
    assert os.path.isfile(file_path), f"'{file_path}' is not a regular file."

def test_fit_results_format_and_values():
    """Check the format and the correctness of the estimated values."""
    file_path = "/home/user/fit_results.txt"
    assert os.path.exists(file_path), f"Cannot test values because '{file_path}' is missing."

    with open(file_path, "r") as f:
        content = f.read()

    # Parse f_est
    f_est_match = re.search(r'f_est:\s*([0-9.]+)', content)
    assert f_est_match is not None, "Could not find 'f_est: <float>' in the output file."
    f_est = float(f_est_match.group(1))

    # Parse A_mean
    A_mean_match = re.search(r'A_mean:\s*([0-9.]+)', content)
    assert A_mean_match is not None, "Could not find 'A_mean: <float>' in the output file."
    A_mean = float(A_mean_match.group(1))

    # Parse phi_mean
    phi_mean_match = re.search(r'phi_mean:\s*([0-9.]+)', content)
    assert phi_mean_match is not None, "Could not find 'phi_mean: <float>' in the output file."
    phi_mean = float(phi_mean_match.group(1))

    # Validate f_est
    assert 2.9 <= f_est <= 3.1, f"Expected f_est to be between 2.9 and 3.1, but got {f_est}."

    # Validate A_mean
    assert 2.2 <= A_mean <= 2.8, f"Expected A_mean to be between 2.2 and 2.8, but got {A_mean}."

    # Validate phi_mean
    assert 0.9 <= phi_mean <= 1.5, f"Expected phi_mean to be between 0.9 and 1.5, but got {phi_mean}."