# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Verify that the C source code exists."""
    path = "/home/user/process.c"
    assert os.path.exists(path), f"Source file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a regular file."

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    path = "/home/user/process"
    assert os.path.exists(path), f"Executable {path} is missing."
    assert os.path.isfile(path), f"{path} is not a regular file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_output_csv_content():
    """Verify the content of the generated hourly_status.csv."""
    path = "/home/user/hourly_status.csv"
    assert os.path.exists(path), f"Output file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a regular file."

    expected_lines = [
        "2023-10-01 00:00:00,OFFLINE",
        "2023-10-01 01:00:00,OFFLINE",
        "2023-10-01 02:00:00,OFFLINE",
        "2023-10-01 03:00:00,OFFLINE",
        "2023-10-01 04:00:00,MAINTENANCE",
        "2023-10-01 05:00:00,MAINTENANCE",
        "2023-10-01 06:00:00,MAINTENANCE",
        "2023-10-01 07:00:00,MAINTENANCE",
        "2023-10-01 08:00:00,ACTIVE",
        "2023-10-01 09:00:00,WARNING",
        "2023-10-01 10:00:00,WARNING",
        "2023-10-01 11:00:00,WARNING",
        "2023-10-01 12:00:00,ACTIVE",
        "2023-10-01 13:00:00,ACTIVE",
        "2023-10-01 14:00:00,ACTIVE",
        "2023-10-01 15:00:00,ACTIVE",
        "2023-10-01 16:00:00,ERROR",
        "2023-10-01 17:00:00,ERROR",
        "2023-10-01 18:00:00,ERROR",
        "2023-10-01 19:00:00,ERROR",
        "2023-10-01 20:00:00,MAINTENANCE",
        "2023-10-01 21:00:00,MAINTENANCE",
        "2023-10-01 22:00:00,MAINTENANCE",
        "2023-10-01 23:00:00,MAINTENANCE"
    ]

    with open(path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1}:\nExpected: {expected}\nActual:   {actual}"