# test_final_state.py
import os
import pytest

def test_source_file_exists():
    """Test that the C source code file was created."""
    file_path = "/home/user/process_loc.c"
    assert os.path.exists(file_path), f"Missing required file: {file_path}"
    assert os.path.isfile(file_path), f"Path is not a file: {file_path}"

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    file_path = "/home/user/process_loc"
    assert os.path.exists(file_path), f"Missing compiled executable: {file_path}"
    assert os.path.isfile(file_path), f"Path is not a file: {file_path}"
    assert os.access(file_path, os.X_OK), f"File is not executable: {file_path}"

def test_hourly_stats_content():
    """Test that the output CSV file contains the correct aggregated statistics."""
    file_path = "/home/user/hourly_stats.csv"
    assert os.path.exists(file_path), f"Missing output file: {file_path}"
    assert os.path.isfile(file_path), f"Path is not a file: {file_path}"

    expected_lines = [
        "1699999200,20",
        "1700002800,29",
        "1700006400,11"
    ]

    with open(file_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {file_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )