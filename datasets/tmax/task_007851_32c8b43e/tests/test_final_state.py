# test_final_state.py

import os
import pytest

def test_executable_exists():
    path = "/home/user/proc_spec"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile the C program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_smoothed_dat_exists():
    path = "/home/user/smoothed.dat"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run the compiled executable?"
    expected_size = 500 * 500 * 4
    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, f"Expected {path} to be {expected_size} bytes, but got {actual_size}."

def test_report_txt_contents():
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"Report file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {path}, but found {len(lines)}."

    assert lines[0] == "apply_filter", f"Line 1 of report.txt is incorrect. Expected 'apply_filter', got '{lines[0]}'."
    assert lines[1] == "15,25", f"Line 2 of report.txt is incorrect. Expected '15,25', got '{lines[1]}'."