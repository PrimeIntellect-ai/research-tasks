# test_final_state.py

import os
import pytest

def test_recovery_output_exists():
    path = "/home/user/recovery_output.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. Did you run the extraction script?"

def test_recovery_output_content():
    path = "/home/user/recovery_output.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

    expected_lines = [
        "1:ALPHA-992",
        "2:BRAVO-713",
        "3:CHARLIE-404",
        "4:DELTA-505"
    ]

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(content)}."

    for i, expected in enumerate(expected_lines):
        assert content[i].strip() == expected, f"Line {i+1} mismatch: expected '{expected}', got '{content[i].strip()}'."

def test_script_bug_fixed():
    path = "/home/user/scripts/extract_secrets.py"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "range(len(records) + 1)" not in content, "The extraction script still contains the off-by-one bug `range(len(records) + 1)`."