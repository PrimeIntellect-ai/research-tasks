# test_final_state.py

import os
import stat
import pytest

def test_evaluate_rs_exists():
    path = "/home/user/evaluate.rs"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "fn main" in content, "evaluate.rs does not appear to be a valid Rust program (missing fn main)."

def test_evaluate_executable_exists():
    path = "/home/user/evaluate"
    assert os.path.isfile(path), f"Executable missing: {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File is not executable: {path}"

def test_valid_ids_content():
    path = "/home/user/valid_ids.txt"
    assert os.path.isfile(path), f"File missing: {path}"

    expected_ids = ["1", "2", "3", "5", "7"]

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_ids, f"Content of {path} does not match the expected valid IDs. Got {lines}, expected {expected_ids}."

def test_experiment_log_content():
    path = "/home/user/experiment_log.txt"
    assert os.path.isfile(path), f"File missing: {path}"

    expected_log = "Run 1: 5 valid models"

    with open(path, "r") as f:
        content = f.read().strip()

    assert expected_log in content, f"Expected '{expected_log}' to be in {path}, but got '{content}'."