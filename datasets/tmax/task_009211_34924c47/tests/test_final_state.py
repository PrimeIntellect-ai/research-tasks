# test_final_state.py

import os
import pytest

def test_analyze_cpp_exists():
    path = "/home/user/analyze.cpp"
    assert os.path.isfile(path), f"File {path} is missing. The C++ source code must be created."

def test_result_txt_exists():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} is missing. The program must produce this output file."

def test_result_txt_content():
    path = "/home/user/result.txt"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} is missing.")

    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = "0 4 0.6124"
    assert content == expected_content, f"Content of {path} is incorrect. Expected '{expected_content}', but got '{content}'."