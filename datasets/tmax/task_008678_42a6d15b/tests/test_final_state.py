# test_final_state.py

import os
import pytest

def test_final_uptime_file_exists_and_correct():
    """Check if the final_uptime.txt file exists and contains the correct calculated uptime."""
    output_file = "/home/user/final_uptime.txt"

    assert os.path.isfile(output_file), f"Missing file: {output_file}. Did you save the output as requested?"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content != "", f"The file {output_file} is empty."

    try:
        uptime_val = int(content)
    except ValueError:
        pytest.fail(f"The file {output_file} does not contain a valid integer. Found: '{content}'")

    expected_uptime = 20
    assert uptime_val == expected_uptime, f"Calculated uptime is incorrect. Expected {expected_uptime}, but got {uptime_val}."