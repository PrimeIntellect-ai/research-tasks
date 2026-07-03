# test_final_state.py

import os
import pytest

def test_unstable_log():
    log_path = "/home/user/profiling/unstable.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you create it?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["mat_2.txt", "mat_3.txt", "mat_5.txt"]

    assert lines == expected, (
        f"Contents of {log_path} do not match expected sorted list of unstable matrices. "
        f"Expected {expected}, but got {lines}."
    )

def test_optim_results_log():
    log_path = "/home/user/profiling/optim_results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you run the optimization script?"

    with open(log_path, "r") as f:
        lines = sorted([line.strip() for line in f if line.strip()])

    expected = [
        "Successfully optimized: mat_1.txt",
        "Successfully optimized: mat_4.txt",
        "Successfully optimized: mat_6.txt"
    ]

    assert lines == expected, (
        f"Contents of {log_path} do not match expected stable matrices. "
        f"Expected {expected}, but got {lines}."
    )