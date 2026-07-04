# test_final_state.py

import os
import pytest

def test_final_summary_file():
    """
    Validates the final state of the filesystem after the student performs the task.
    Ensures that final_summary.txt exists and contains the correct sorted output.
    """
    final_summary_path = "/home/user/final_summary.txt"
    go_program_path = "/home/user/process_dataset.go"

    # Check if the Go program exists
    assert os.path.isfile(go_program_path), f"Go program missing: {go_program_path}"

    # Check if the final summary exists
    assert os.path.isfile(final_summary_path), f"Final summary file missing: {final_summary_path}"

    expected_lines = [
        "sensor_A1.txt:42",
        "sensor_A2.txt:15",
        "sensor_B1.txt:99",
        "sensor_B2.txt:7"
    ]

    with open(final_summary_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {final_summary_path} do not match the expected sorted output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )