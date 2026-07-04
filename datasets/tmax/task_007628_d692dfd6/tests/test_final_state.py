# test_final_state.py

import os
import pytest

def test_c_source_exists():
    path = "/home/user/detect_cycles.c"
    assert os.path.isfile(path), f"Expected C source file {path} does not exist."

def test_executable_exists():
    path = "/home/user/detect_cycles"
    assert os.path.isfile(path), f"Expected executable {path} does not exist. Did you compile the program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_deadlocks_output():
    path = "/home/user/deadlocks.out"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "JobA,JobB,JobC",
        "JobG,JobH,JobI"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} cycles, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."