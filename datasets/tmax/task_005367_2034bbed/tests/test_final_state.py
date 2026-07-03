# test_final_state.py

import os
import pytest

def test_detect_c_exists():
    """Test that the C program source file exists."""
    path = "/home/user/detect.c"
    assert os.path.isfile(path), f"Missing C source file: {path}"

def test_detect_executable_exists():
    """Test that the compiled C program exists and is executable."""
    path = "/home/user/detect"
    assert os.path.isfile(path), f"Missing compiled executable: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_query_sql_exists():
    """Test that the generated SQL script exists."""
    path = "/home/user/query.sql"
    assert os.path.isfile(path), f"Missing generated SQL script: {path}"

def test_deadlocks_txt_content():
    """Test that deadlocks.txt exists and contains the correct transaction IDs."""
    path = "/home/user/deadlocks.txt"
    assert os.path.isfile(path), f"Missing output file: {path}"

    expected_lines = ["1", "2", "3", "7", "8"]

    with open(path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {path} does not match expected deadlocks. "
        f"Expected: {expected_lines}, Got: {actual_lines}"
    )