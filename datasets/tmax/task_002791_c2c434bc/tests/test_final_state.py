# test_final_state.py
import os
import pytest

def test_find_path_c_exists():
    """Test that the C source file exists."""
    file_path = "/home/user/find_path.c"
    assert os.path.isfile(file_path), f"C source file {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, f"C source file {file_path} is empty."

def test_find_path_executable_exists():
    """Test that the compiled executable exists and is executable."""
    file_path = "/home/user/find_path"
    assert os.path.isfile(file_path), f"Executable file {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_path_result_content():
    """Test that the path_result.txt file contains the correct shortest path."""
    file_path = "/home/user/path_result.txt"
    assert os.path.isfile(file_path), f"Result file {file_path} is missing."

    expected_path = "raw_users,dim_fast_track,mart_revenue"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_path, f"Expected path '{expected_path}', but got '{content}'."