# test_final_state.py

import os
import shutil

def test_gcc_make_installed():
    assert shutil.which("gcc") is not None, "gcc is not installed or not in PATH."
    assert shutil.which("make") is not None, "make is not installed or not in PATH."

def test_c_source_exists():
    path = "/home/user/src/search.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

def test_executable_exists():
    path = "/home/user/src/search"
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_file_exists():
    path = "/home/user/output/results.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

def test_output_file_content():
    path = "/home/user/output/results.csv"
    expected_lines = [
        "id,similarity",
        "2,0.8944",
        "4,0.7746",
        "5,0.7746"
    ]

    with open(path, "r") as f:
        content = f.read().strip().split("\n")

    assert len(content) == len(expected_lines), f"Output file should have {len(expected_lines)} lines, but has {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual.strip()}'."