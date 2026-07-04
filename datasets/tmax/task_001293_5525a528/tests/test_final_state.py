# test_final_state.py

import os
import pytest

def test_analyze_go_exists():
    """Check that the Go source file /home/user/analyze.go exists."""
    file_path = "/home/user/analyze.go"
    assert os.path.exists(file_path), f"Missing expected Go source file: {file_path}"
    assert os.path.isfile(file_path), f"Expected a file, but found a directory: {file_path}"

def test_result_txt_content():
    """Check that /home/user/result.txt exists and contains the correct output."""
    file_path = "/home/user/result.txt"
    assert os.path.exists(file_path), f"Missing required output file: {file_path}"
    assert os.path.isfile(file_path), f"Expected a file, but found a directory: {file_path}"

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    expected_content = "Seq3,Seq4,0.3698"
    assert actual_content == expected_content, f"Content of {file_path} is incorrect. Expected '{expected_content}', got '{actual_content}'."