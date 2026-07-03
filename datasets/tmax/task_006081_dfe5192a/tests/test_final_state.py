# test_final_state.py

import os
import pytest

def test_executable_exists_and_runnable():
    exe_path = "/home/user/pipeline/project"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_output_file_exists():
    out_path = "/home/user/pipeline/output.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing. Did you run the executable?"

def test_output_file_content():
    out_path = "/home/user/pipeline/output.txt"
    with open(out_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["1.40", "4.40", "7.40"]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output.txt, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in output.txt is incorrect. Expected '{expected}', got '{actual}'."