# test_final_state.py

import os
import pytest

def test_bootstrap_mean_file_exists():
    """Check if the output file bootstrap_mean.txt exists."""
    file_path = '/home/user/bootstrap_mean.txt'
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Ensure you saved your result."

def test_bootstrap_mean_value():
    """Check if the calculated bootstrap mean matches the expected truth."""
    output_file = '/home/user/bootstrap_mean.txt'
    truth_file = '/home/user/.expected_truth'

    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing. Setup might have failed."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, 'r') as f:
        user_output = f.read().strip()

    with open(truth_file, 'r') as f:
        expected_output = f.read().strip()

    assert user_output == expected_output, (
        f"The calculated mean in {output_file} ({user_output}) "
        f"does not match the expected value ({expected_output}). "
        "Check your filtering logic, random seed, and rounding."
    )