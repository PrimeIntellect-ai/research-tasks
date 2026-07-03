# test_final_state.py

import os
import pytest

def test_cpp_file_exists():
    """Check if the C++ source file exists."""
    file_path = "/home/user/find_chains.cpp"
    assert os.path.isfile(file_path), f"C++ source file {file_path} is missing."

def test_executable_exists():
    """Check if the compiled executable exists and is executable."""
    file_path = "/home/user/find_chains"
    assert os.path.isfile(file_path), f"Compiled executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_output_file_exists():
    """Check if the output chains.txt file exists."""
    file_path = "/home/user/chains.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

def test_output_file_content():
    """Check if the output chains.txt file has the correct content and is sorted."""
    file_path = "/home/user/chains.txt"

    expected_lines = [
        "Extract_Root -> Clean_Data -> Transform_Agg -> Load_Final",
        "Extract_Root -> Clean_Data -> Transform_Join -> Load_Final",
        "Extract_Root -> Clean_Data -> Transform_Join -> Side_Effect_Task -> Load_Final",
        "Extract_Root -> Validate_Schema -> Transform_Join -> Load_Final",
        "Extract_Root -> Validate_Schema -> Transform_Join -> Side_Effect_Task -> Load_Final"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {file_path} does not match the expected chains or is not sorted properly.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )