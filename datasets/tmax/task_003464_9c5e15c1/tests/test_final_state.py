# test_final_state.py

import os
import re
import pytest

def test_minimal_crash_file():
    path = "/home/user/minimal_crash.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert "3,0,1,1,1" in content, f"File {path} does not contain the correct minimal crash line."

def test_fixed_output_file():
    path = "/home/user/fixed_output.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "ID: 1, Weight: 16",
        "ID: 2, Weight: 13",
        "Corrupted record ID: 3",
        "ID: 4, Weight: 25"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"File {path} contents do not match the expected output. Got: {actual_lines}"

def test_processor_c_fixed_formula():
    path = "/home/user/processor.c"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check that the buggy formula is gone or replaced with the correct one
    # Correct formula: a + (b * c) or a + b * c
    # Buggy formula was: (a + b) * c
    assert "(a + b) * c" not in content.replace(" ", ""), f"File {path} still contains the buggy weight calculation."

    # Check for the correct formula logic
    # We can use regex to find something like a + b * c or a + (b * c)
    cleaned_content = content.replace(" ", "")
    assert "a+b*c" in cleaned_content or "a+(b*c)" in cleaned_content, f"File {path} does not contain the corrected weight calculation formula."

def test_processor_binary_exists():
    path = "/home/user/processor"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."