# test_final_state.py

import os
import pytest

def test_output_file_exists_and_correct():
    """Test that the output.txt file exists and contains the correct Bayesian update result."""
    output_path = "/home/user/output.txt"

    assert os.path.exists(output_path), f"Expected output file not found at {output_path}."
    assert os.path.isfile(output_path), f"Expected {output_path} to be a file."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = "N=8,K=6,PosteriorMean=0.7000"

    assert content == expected_content, (
        f"The content of {output_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{content}'"
    )