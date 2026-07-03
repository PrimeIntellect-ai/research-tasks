# test_final_state.py

import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/prime_cruncher"
    assert os.path.exists(executable_path), f"Executable {executable_path} is missing. Did you compile the C code?"
    assert os.path.isfile(executable_path), f"Path {executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_debug_report_exists():
    report_path = "/home/user/debug_report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} is missing."
    assert os.path.isfile(report_path), f"Path {report_path} is not a file."

def test_debug_report_content():
    report_path = "/home/user/debug_report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Crashing Function: calculate_zeta_function",
        "Last Prime: 3571",
        "Sequence ID: 98765"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in {report_path}, but found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} of {report_path} is incorrect. Expected '{expected}', got '{lines[i]}'."