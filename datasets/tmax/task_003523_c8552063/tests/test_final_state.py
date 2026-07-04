# test_final_state.py

import os
import pytest

def test_train_model_c_exists():
    path = "/home/user/train_model.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_train_model_executable_exists():
    path = "/home/user/train_model"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_model_output_txt():
    path = "/home/user/model_output.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "Intercept: 0.0300, Slope: 2.0100"
    assert content == expected, f"Content of {path} is incorrect. Expected: '{expected}', Got: '{content}'"

def test_experiment_log_txt():
    path = "/home/user/experiment_log.txt"
    assert os.path.isfile(path), f"Log file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    expected_line = "Run 1042: c0=0.0300, c1=2.0100"
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert any(expected_line in line for line in lines), f"Expected line '{expected_line}' not found in {path}."