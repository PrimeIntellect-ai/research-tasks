# test_final_state.py

import os
import pytest

def test_deadlock_report_exists_and_correct():
    report_path = "/home/user/deadlock_report.txt"

    assert os.path.isfile(report_path), f"Expected output file {report_path} does not exist."

    expected_lines = [
        "T1:2",
        "T2:1",
        "T3:1",
        "T6:1",
        "T7:1",
        "T9:1"
    ]

    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    # Strip any trailing whitespace from each line
    content = [line.strip() for line in content if line.strip()]

    assert content == expected_lines, (
        f"Contents of {report_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {content}"
    )

def test_cpp_source_and_executable_exist():
    cpp_path = "/home/user/detect_deadlocks.cpp"
    exe_path = "/home/user/detect_deadlocks"

    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."