# test_final_state.py

import os
import pytest

def test_statistics_file_exists():
    """Test that the output statistics.txt file exists."""
    file_path = "/home/user/statistics.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist. The program may not have run or failed to write the output."

def test_statistics_file_contents():
    """Test that the output statistics.txt file contains the correct calculated values."""
    file_path = "/home/user/statistics.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip().splitlines()

    assert len(content) == 2, f"Output file {file_path} should contain exactly two lines, but found {len(content)} lines."

    expected_mean_line = "Global Mean: 61.75"
    expected_variance_line = "Global Variance: 833.25"

    assert content[0].strip() == expected_mean_line, f"First line of output is incorrect. Expected '{expected_mean_line}', got '{content[0].strip()}'."
    assert content[1].strip() == expected_variance_line, f"Second line of output is incorrect. Expected '{expected_variance_line}', got '{content[1].strip()}'."