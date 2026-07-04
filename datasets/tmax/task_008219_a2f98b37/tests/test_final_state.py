# test_final_state.py

import os
import pytest

def test_merger_c_exists():
    file_path = "/home/user/merger.c"
    assert os.path.isfile(file_path), f"Source file missing: {file_path}"

def test_merger_executable_exists():
    file_path = "/home/user/merger"
    assert os.path.isfile(file_path), f"Compiled executable missing: {file_path}"
    assert os.access(file_path, os.X_OK), f"File is not executable: {file_path}"

def test_matches_csv_correct():
    file_path = "/home/user/matches.csv"
    assert os.path.isfile(file_path), f"Output file missing: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "btn_save,save_btn,2,2",
        "btn_start,start_btn,4,2"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in matches.csv, but got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"