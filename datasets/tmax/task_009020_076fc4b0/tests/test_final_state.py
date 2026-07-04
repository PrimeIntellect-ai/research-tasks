# test_final_state.py

import os
import pytest

def test_analyze_c_exists():
    """Test that the C source code file exists."""
    c_file_path = "/home/user/analyze.c"
    assert os.path.exists(c_file_path), f"Missing required file: {c_file_path}"
    assert os.path.isfile(c_file_path), f"Expected {c_file_path} to be a file."

def test_results_txt_exists():
    """Test that the results.txt file was generated."""
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"Missing required file: {results_path}"
    assert os.path.isfile(results_path), f"Expected {results_path} to be a file."

def test_results_txt_content():
    """Test that the results.txt file contains the correct output."""
    results_path = "/home/user/results.txt"

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {results_path}, found {len(lines)}"

    assert lines[0] == "2", f"Expected first line of {results_path} to be '2', but got '{lines[0]}'"
    assert lines[1] == "5", f"Expected second line of {results_path} to be '5', but got '{lines[1]}'"