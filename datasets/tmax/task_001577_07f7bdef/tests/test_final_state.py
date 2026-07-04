# test_final_state.py

import os
import re

def test_c_source_exists():
    source_path = "/home/user/posterior.c"
    assert os.path.isfile(source_path), f"C source file {source_path} is missing. You must create it."

def test_posterior_result():
    result_path = "/home/user/posterior_result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected = "beta1=2.207, beta2=1.831"
    assert content == expected, f"Content of {result_path} is incorrect. Expected '{expected}', got '{content}'."

def test_c_source_contains_main():
    source_path = "/home/user/posterior.c"
    if os.path.isfile(source_path):
        with open(source_path, "r") as f:
            content = f.read()
        assert "main" in content, "The C source file does not appear to contain a main() function."