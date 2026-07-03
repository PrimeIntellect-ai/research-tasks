# test_final_state.py

import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/analyzer"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file not found at {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_result = "3000000000"
    assert content == expected_result, f"Expected result to be {expected_result}, but got {content}"