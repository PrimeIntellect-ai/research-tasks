# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Test that the C source file exists."""
    assert os.path.isfile("/home/user/fast_match.c"), "The C source file /home/user/fast_match.c is missing."

def test_c_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.isfile("/home/user/fast_match"), "The executable /home/user/fast_match is missing."
    assert os.access("/home/user/fast_match", os.X_OK), "/home/user/fast_match is not executable."

def test_recommendations_csv_correct():
    """Test that the recommendations.csv file contains the correct aggregated output."""
    output_file = "/home/user/recommendations.csv"
    assert os.path.isfile(output_file), f"The output file {output_file} is missing."

    expected_output = [
        "U001,3",
        "U002,2",
        "U003,1",
        "U005,2"
    ]

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_output, (
        f"The content of {output_file} does not match the expected output.\n"
        f"Expected: {expected_output}\n"
        f"Got: {lines}"
    )