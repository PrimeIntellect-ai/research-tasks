# test_final_state.py

import os
import pytest

OUTPUT_FILE = '/home/user/total_successful_backup_size.txt'
EXPECTED_SUM = 520

def test_output_file_exists():
    """Verify that the output file has been created."""
    assert os.path.exists(OUTPUT_FILE), f"The output file '{OUTPUT_FILE}' does not exist."
    assert os.path.isfile(OUTPUT_FILE), f"The path '{OUTPUT_FILE}' is not a regular file."

def test_output_file_content():
    """Verify that the output file contains the correct aggregated size."""
    assert os.path.exists(OUTPUT_FILE), f"The output file '{OUTPUT_FILE}' does not exist."

    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()

    assert content, f"The file '{OUTPUT_FILE}' is empty."

    try:
        calculated_sum = int(content)
    except ValueError:
        pytest.fail(f"The content of '{OUTPUT_FILE}' is not a valid integer. Found: '{content}'")

    assert calculated_sum == EXPECTED_SUM, (
        f"The calculated sum is incorrect. "
        f"Expected {EXPECTED_SUM}, but found {calculated_sum}."
    )