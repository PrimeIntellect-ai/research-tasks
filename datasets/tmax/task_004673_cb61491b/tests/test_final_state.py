# test_final_state.py
import os
import pytest

def test_top_sv_file():
    path = '/home/user/top_sv.txt'
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {path}, found {len(lines)}."

    expected_values = ["18.239300", "2.502985", "2.434674"]
    for i, (actual, expected) in enumerate(zip(lines, expected_values)):
        assert actual == expected, f"Line {i+1} in {path} is '{actual}', expected '{expected}'."

def test_sv_error_file():
    path = '/home/user/sv_error.txt'
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_mae = "0.056667"
    assert content == expected_mae, f"Expected MAE in {path} to be '{expected_mae}', got '{content}'."