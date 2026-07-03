# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    file_path = "/home/user/compute_corr.c"
    assert os.path.isfile(file_path), f"The C source file {file_path} is missing. Did you write your code to the correct path?"

def test_correlation_result_file_exists_and_correct():
    file_path = "/home/user/correlation_result.txt"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing. Did you run your compiled program?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected = "Correlation: -0.9888"
    assert content == expected, f"The contents of {file_path} are incorrect. Expected '{expected}', got '{content}'."