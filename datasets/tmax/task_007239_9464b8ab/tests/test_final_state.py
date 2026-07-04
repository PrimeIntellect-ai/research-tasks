# test_final_state.py

import os
import pytest

def test_mean_error_file_exists_and_valid():
    error_file = "/home/user/mean_error.txt"
    assert os.path.isfile(error_file), f"Verification failed: {error_file} not found."

    with open(error_file, "r") as f:
        content = f.read().strip()

    try:
        error_val = float(content)
    except ValueError:
        pytest.fail(f"Verification failed: Contents of {error_file} cannot be parsed as a float. Found: {content}")

    assert error_val < 0.1, f"Verification failed: Error {error_val} is not less than 0.1"

def test_mcmc_sampler_cpp_fixes():
    cpp_file = "/home/user/mcmc_sampler.cpp"
    assert os.path.isfile(cpp_file), f"Missing file: {cpp_file}"

    with open(cpp_file, "r") as f:
        content = f.read()

    # Check that the original bugs are removed
    assert "double delta = 10000.0;" not in content, "The proposal step size (delta) is still set to the astronomically large value of 10000.0."
    assert "target_pdf(current) / target_pdf(proposed)" not in content, "The acceptance ratio calculation is still incorrect (flipped)."

    # Check that the correct logic is likely present
    assert "target_pdf(proposed) / target_pdf(current)" in content.replace(" ", ""), "The correct acceptance ratio (target_pdf(proposed) / target_pdf(current)) was not found."