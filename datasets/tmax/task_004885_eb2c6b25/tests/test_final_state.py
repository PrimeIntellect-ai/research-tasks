# test_final_state.py

import os
import pytest

def test_results_log_exists():
    filepath = "/home/user/results.log"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing."

def test_results_log_content():
    filepath = "/home/user/results.log"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Stationary A: 0.2863",
        "Stationary B: 0.3524",
        "Stationary C: 0.3612",
        "KL_Divergence: 0.0005"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {filepath}."

    # Also check exact order and length if possible, but at least ensure all expected lines are present
    assert len(lines) == 4, f"Expected exactly 4 lines in {filepath}, but found {len(lines)}."
    assert lines == expected_lines, f"Contents of {filepath} do not match the expected output exactly."