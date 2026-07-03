# test_final_state.py

import os
import pytest

def test_optimal_params_file_exists():
    """Test that the optimal_params.txt file was created."""
    assert os.path.isfile("/home/user/optimal_params.txt"), (
        "The file /home/user/optimal_params.txt does not exist. "
        "Make sure your script creates it."
    )

def test_optimal_params_content():
    """Test that optimal_params.txt contains the correct optimal parameters and SSE."""
    expected_content = "m=2.00, b=1.10, SSE=0.09"

    with open("/home/user/optimal_params.txt", "r") as f:
        content = f.read().strip()

    assert content == expected_content, (
        f"The content of /home/user/optimal_params.txt is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Found: '{content}'\n"
        "Check your grid search logic, SSE calculation, and formatting."
    )