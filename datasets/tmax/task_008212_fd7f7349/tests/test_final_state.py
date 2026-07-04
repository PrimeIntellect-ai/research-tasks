# test_final_state.py

import os
import pytest

def test_c_program_exists():
    c_file = "/home/user/workspace/process_telemetry.c"
    assert os.path.isfile(c_file), f"Expected C program at {c_file} is missing."

def test_processed_telemetry_file_exists():
    processed_file = "/home/user/remote_server/archive/processed_telemetry.csv"
    assert os.path.isfile(processed_file), f"Expected processed data file at {processed_file} is missing."

def test_processed_telemetry_content():
    processed_file = "/home/user/remote_server/archive/processed_telemetry.csv"
    assert os.path.isfile(processed_file), f"File {processed_file} does not exist."

    expected_lines = [
        "1001,S001,50.00",
        "1006,S006,60.00",
        "1007,S123,0.00",
        "1008,S999,0.00"
    ]

    with open(processed_file, "r") as f:
        content = f.read().strip().splitlines()

    # Remove any empty lines
    actual_lines = [line.strip() for line in content if line.strip()]

    assert actual_lines == expected_lines, (
        f"Processed telemetry data is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )

def test_no_leftover_processed_csv():
    # Check that it was moved, not just copied
    leftover_file = "/home/user/workspace/processed.csv"
    assert not os.path.exists(leftover_file), (
        f"File {leftover_file} should have been moved, but it still exists in the workspace."
    )