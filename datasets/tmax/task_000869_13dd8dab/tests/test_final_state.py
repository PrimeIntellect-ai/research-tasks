# test_final_state.py

import os
import pytest

def test_best_alpha_file_exists():
    """Test that the best_alpha.txt file exists."""
    file_path = "/home/user/best_alpha.txt"
    assert os.path.exists(file_path), f"The output file is missing: {file_path}"
    assert os.path.isfile(file_path), f"The path exists but is not a file: {file_path}"

def test_best_alpha_content():
    """Test that the best_alpha.txt file contains the correct alpha value."""
    file_path = "/home/user/best_alpha.txt"
    assert os.path.exists(file_path), f"The output file is missing: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content != "", "The output file is empty."

    try:
        alpha_val = float(content)
    except ValueError:
        pytest.fail(f"The output file does not contain a valid float. Got: '{content}'")

    assert alpha_val == 10.0, f"The best alpha value is incorrect. Expected 10.0, but got {alpha_val}"