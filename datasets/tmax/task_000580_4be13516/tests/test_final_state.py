# test_final_state.py

import os
import pytest

def test_best_fit_log_exists():
    """Test that the output file best_fit.log exists."""
    output_file = '/home/user/best_fit.log'
    assert os.path.exists(output_file), f"Output file {output_file} is missing."
    assert os.path.isfile(output_file), f"{output_file} is not a file."

def test_best_fit_log_contents():
    """Test that the output file contains the correct expected result."""
    output_file = '/home/user/best_fit.log'
    expected_file = '/home/user/expected_best_fit.log'

    assert os.path.exists(output_file), f"Output file {output_file} is missing."
    assert os.path.exists(expected_file), f"Expected file {expected_file} is missing. Setup failed."

    with open(output_file, 'r') as f:
        actual_content = f.read().strip()

    with open(expected_file, 'r') as f:
        expected_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Contents of {output_file} do not match the expected result.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual: '{actual_content}'"
    )