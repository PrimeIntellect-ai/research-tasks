# test_final_state.py

import os
import stat
import pytest
import re

def test_regression_cpp_fixed():
    filepath = "/home/user/regression.cpp"
    assert os.path.exists(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        content = f.read()

    assert "#pragma omp atomic" not in content, f"File {filepath} still contains '#pragma omp atomic'."
    assert "schedule(dynamic, 1000)" not in content, f"File {filepath} still contains 'schedule(dynamic, 1000)'."

    # Check for reduction clause
    assert "reduction" in content, f"File {filepath} does not contain a 'reduction' clause."
    assert "sum_x" in content and "sum_y" in content and "sum_xy" in content and "sum_x2" in content, \
        f"File {filepath} reduction clause might be missing variables."

def test_executable_exists_and_runnable():
    filepath = "/home/user/regression_fixed"
    assert os.path.exists(filepath), f"Executable {filepath} does not exist."
    assert os.path.isfile(filepath), f"{filepath} is not a file."

    # Check if executable
    st = os.stat(filepath)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {filepath} is not executable."

def test_output_txt_content():
    filepath = "/home/user/output.txt"
    assert os.path.exists(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "3.14159,2.71828", f"File {filepath} contains '{content}', expected '3.14159,2.71828'."