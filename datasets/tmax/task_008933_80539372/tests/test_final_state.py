# test_final_state.py

import os
import pytest

def test_results_file_exists():
    """Check if the results.txt file was created."""
    filepath = "/home/user/sensor_analysis/results.txt"
    assert os.path.exists(filepath), f"File {filepath} does not exist. Did the Rust program run and create it?"

def test_results_content():
    """Verify the computed statistics in results.txt."""
    filepath = "/home/user/sensor_analysis/results.txt"
    if not os.path.exists(filepath):
        pytest.fail(f"File {filepath} does not exist.")

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_content = (
        "Valid rows: 6\n"
        "Mean A: 11.833\n"
        "Mean B: 22.017\n"
        "Correlation: 0.996"
    )

    assert content == expected_content, (
        f"The content of {filepath} is incorrect.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Got:\n{content}"
    )