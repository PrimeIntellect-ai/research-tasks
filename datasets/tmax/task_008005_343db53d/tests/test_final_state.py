# test_final_state.py

import os
import pytest

def test_analyzer_c_exists():
    path = "/home/user/analyzer.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_analyzer_executable_exists():
    path = "/home/user/analyzer"
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_anomaly_txt_content():
    path = "/home/user/anomaly.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_date = "2023-10-05"
    assert content == expected_date, f"Expected '{expected_date}' in {path}, but got '{content}'."