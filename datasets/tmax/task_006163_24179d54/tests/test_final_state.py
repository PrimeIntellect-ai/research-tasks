# test_final_state.py

import os
import pytest

def test_analyze_c_exists():
    path = "/home/user/analyze.c"
    assert os.path.isfile(path), f"Source file missing at {path}"

def test_analyze_executable_exists():
    path = "/home/user/analyze"
    assert os.path.isfile(path), f"Executable missing at {path}"
    assert os.access(path, os.X_OK), f"File at {path} is not executable"

def test_flagged_txt_correct():
    path = "/home/user/flagged.txt"
    assert os.path.isfile(path), f"Output file missing at {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["client2.crt", "client3.crt"]

    assert lines == expected, f"Expected {expected} in {path}, but got {lines}"