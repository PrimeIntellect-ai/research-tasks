# test_final_state.py

import os
import pytest

def test_final_result_exists():
    """Check if the final result file exists."""
    assert os.path.isfile("/home/user/final_result.txt"), "The file /home/user/final_result.txt does not exist."

def test_final_result_value():
    """Check if the final result file contains the correct computed value."""
    with open("/home/user/final_result.txt", "r") as f:
        content = f.read().strip()

    assert content, "The file /home/user/final_result.txt is empty."

    try:
        result_val = float(content)
    except ValueError:
        pytest.fail(f"The content of /home/user/final_result.txt ('{content}') is not a valid floating-point number.")

    # The expected value is 42.42 * sum(1.0 to 100.0) = 42.42 * 5050.0 = 214221.0
    expected_val = 214221.0

    assert result_val == expected_val, f"Expected the final result to be {expected_val}, but got {result_val}. Check your PCAP extraction, Git forensics, and race condition fix."