# test_final_state.py

import os
import pytest

def test_tvd_result_exists():
    """Check if the output file was created."""
    file_path = "/home/user/tvd_result.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

def test_tvd_result_content():
    """Check if the output file contains the correct TVD value."""
    file_path = "/home/user/tvd_result.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_tvd = "0.0333"
    assert content == expected_tvd, f"Expected '{expected_tvd}' in {file_path}, but got '{content}'."