# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    c_file = "/home/user/analyze_backups.c"
    assert os.path.exists(c_file), f"C source file {c_file} does not exist."
    assert os.path.isfile(c_file), f"Path {c_file} is not a file."

def test_binary_executable_exists():
    binary_file = "/home/user/analyze_backups"
    assert os.path.exists(binary_file), f"Compiled binary {binary_file} does not exist."
    assert os.path.isfile(binary_file), f"Path {binary_file} is not a file."
    assert os.access(binary_file, os.X_OK), f"File {binary_file} is not executable."

def test_top_backups_txt_content():
    output_file = "/home/user/top_backups.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

    expected_lines = [
        "db_core,9",
        "db_users,4",
        "db_logs,2",
        "db_orders,2",
        "db_analytics,1"
    ]

    with open(output_file, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual.strip()}'."