# test_final_state.py

import os
import pytest

def test_valid_logs_exists():
    path = "/home/user/valid_logs.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist. Did the Rust pipeline run successfully?"

def test_valid_logs_content():
    path = "/home/user/valid_logs.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    try:
        actual_ids = [int(line) for line in lines]
    except ValueError:
        pytest.fail(f"File {path} contains non-integer values. It should only contain valid log IDs.")

    expected_ids = [1, 2, 4, 6, 8]

    assert actual_ids == expected_ids, (
        f"The contents of {path} do not match the expected valid IDs. "
        f"Expected: {expected_ids}, but got: {actual_ids}. "
        "Check your distance calculation, threshold logic, and sorting."
    )