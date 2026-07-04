# test_final_state.py
import os
import re
import pytest

def test_passed_txt_content():
    path = "/home/user/pr-review/passed.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the Python script?"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "5.5+4.5 == 10.0 >= 9.0",
        "7.1+3.2 == 10.3 >= 10.0"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, "The contents of passed.txt do not match the expected filtered results. Check your C library logic and Python ABI setup."

def test_evaluate_c_memory_leak_fixed():
    path = "/home/user/pr-review/evaluate.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    # Check if expr_copy is freed
    assert re.search(r"free\s*\(\s*expr_copy\s*\)", content), "Memory leak not fixed in evaluate.c. You need to free the allocated string before returning."

def test_check_constraints_py_abi_fixed():
    path = "/home/user/pr-review/check_constraints.py"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "restype" in content and "c_double" in content, "ABI mismatch not fixed in check_constraints.py. You need to set the correct restype."
    assert "argtypes" in content, "ABI mismatch not fixed in check_constraints.py. You need to set the correct argtypes."