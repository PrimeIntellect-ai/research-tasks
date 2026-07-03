# test_final_state.py

import os
import pytest

def test_verify_c_exists():
    """Test that the C program source file exists."""
    assert os.path.isfile("/home/user/verify.c"), "The C source file /home/user/verify.c does not exist."

def test_verify_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/verify"
    assert os.path.isfile(exe_path), f"The executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_summary_log_content():
    """Test that summary.log exists, contains the correct results, and is sorted."""
    log_path = "/home/user/summary.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    expected_lines = [
        "/home/user/data/setA/nested/sample2.rle OK",
        "/home/user/data/setA/sample1.rle OK",
        "/home/user/data/setB/sample3.rle CORRUPT",
        "/home/user/data/setB/sample4.rle CORRUPT"
    ]

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"The contents of {log_path} do not match the expected sorted output."