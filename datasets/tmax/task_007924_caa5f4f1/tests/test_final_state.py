# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Test that the C source code file exists."""
    c_file = "/home/user/analyze.c"
    assert os.path.isfile(c_file), f"C source file missing at {c_file}"

def test_executable_exists_and_executable():
    """Test that the compiled executable exists and is executable."""
    exe_file = "/home/user/analyze"
    assert os.path.isfile(exe_file), f"Executable missing at {exe_file}"
    assert os.access(exe_file, os.X_OK), f"File at {exe_file} is not executable"

def test_results_csv_content():
    """Test that the results.csv file exists and contains the correct data."""
    csv_file = "/home/user/results.csv"
    assert os.path.isfile(csv_file), f"Results CSV missing at {csv_file}"

    expected_lines = [
        "Control,105,15.2,1",
        "Control,100,10.5,2",
        "Control,110,10.5,2",
        "Treatment,101,22.1,1",
        "Treatment,102,22.1,1",
        "Treatment,103,18.4,2"
    ]

    with open(csv_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, found {len(actual_lines)}"

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        # Convert float to float for comparison to avoid string formatting issues (e.g., 15.2 vs 15.20)
        exp_parts = expected.split(',')
        act_parts = actual.split(',')

        assert len(exp_parts) == 4 and len(act_parts) == 4, f"Line {i+1} is malformed: {actual}"

        assert act_parts[0] == exp_parts[0], f"Line {i+1} group mismatch: expected {exp_parts[0]}, got {act_parts[0]}"
        assert act_parts[1] == exp_parts[1], f"Line {i+1} timestamp mismatch: expected {exp_parts[1]}, got {act_parts[1]}"
        assert abs(float(act_parts[2]) - float(exp_parts[2])) < 1e-6, f"Line {i+1} primary_metric mismatch: expected {exp_parts[2]}, got {act_parts[2]}"
        assert act_parts[3] == exp_parts[3], f"Line {i+1} rank mismatch: expected {exp_parts[3]}, got {act_parts[3]}"