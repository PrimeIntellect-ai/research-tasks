# test_final_state.py

import os
import math
import pytest

def test_decay_table_exists():
    """Check that /home/user/decay_table.txt exists and is a file."""
    path = "/home/user/decay_table.txt"
    assert os.path.exists(path), f"File {path} was not generated."
    assert os.path.isfile(path), f"Path {path} is not a regular file."

def test_decay_table_content():
    """Check that /home/user/decay_table.txt contains exactly the expected 50 values."""
    path = "/home/user/decay_table.txt"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 50, f"Expected exactly 50 lines in {path}, but found {len(lines)}."

    for i in range(50):
        expected_val = math.exp(-i / 10.0)
        expected_str = f"{expected_val:.6f}"
        actual_str = lines[i].strip()

        assert actual_str == expected_str, (
            f"Line {i+1} mismatch: expected '{expected_str}', got '{actual_str}'. "
            "Ensure the precision loss issue and boundary errors are fixed."
        )