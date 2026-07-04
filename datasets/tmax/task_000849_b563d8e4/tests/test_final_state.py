# test_final_state.py
import os
import pytest

def test_c_source_file_exists():
    path = "/home/user/aggregate.c"
    assert os.path.isfile(path), f"File {path} is missing. You must write the C program."

def test_c_executable_exists():
    path = "/home/user/aggregate"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the C program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_report_txt_exists_and_correct():
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the C program to generate the report?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Biology: 337",
        "Computer Science: 245",
        "Physics: 85"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {path} is incorrect. Expected '{expected}', got '{actual}'."