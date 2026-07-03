# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    file_path = "/home/user/compute_path.c"
    assert os.path.exists(file_path), f"C source file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_output_file_exists():
    file_path = "/home/user/path_output.txt"
    assert os.path.exists(file_path), f"Output file {file_path} is missing. Did the C program run?"
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_output_file_content():
    file_path = "/home/user/path_output.txt"
    expected_lines = [
        "Path: N0->N2->N3->N10",
        "Weight: 11"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 2, f"Output file {file_path} must contain exactly two lines, got {len(content)}."

    assert content[0].strip() == expected_lines[0], f"First line of output is incorrect. Expected '{expected_lines[0]}', got '{content[0].strip()}'."
    assert content[1].strip() == expected_lines[1], f"Second line of output is incorrect. Expected '{expected_lines[1]}', got '{content[1].strip()}'."