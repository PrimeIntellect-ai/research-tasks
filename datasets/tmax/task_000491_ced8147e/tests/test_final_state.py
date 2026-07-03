# test_final_state.py

import os
import re
import subprocess
import pytest

def test_executables_exist():
    assert os.path.isfile("/home/user/generator"), "/home/user/generator executable is missing."
    assert os.access("/home/user/generator", os.X_OK), "/home/user/generator is not executable."
    assert os.path.isfile("/home/user/bootstrap"), "/home/user/bootstrap executable is missing."
    assert os.access("/home/user/bootstrap", os.X_OK), "/home/user/bootstrap is not executable."

def test_training_data():
    data_file = "/home/user/training_data.txt"
    assert os.path.isfile(data_file), f"Missing {data_file}"

    with open(data_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 5000, f"Expected 5000 lines in {data_file}, but found {len(lines)}."

    # Check that they are valid floats
    for line in lines:
        try:
            float(line.strip())
        except ValueError:
            pytest.fail(f"Invalid float found in {data_file}: {line.strip()}")

def test_convergence_log():
    log_file = "/home/user/convergence_log.txt"
    assert os.path.isfile(log_file), f"Missing {log_file}"

    with open(log_file, "r") as f:
        content = f.read().strip()

    parts = content.split()
    assert len(parts) == 2, f"Expected exactly two values in {log_file}, found {len(parts)}."

    n_val, width_val = parts
    assert n_val == "5000", f"Expected N=5000 in {log_file}, found {n_val}."

    try:
        width = float(width_val)
    except ValueError:
        pytest.fail(f"Invalid float for CI width in {log_file}: {width_val}")

    assert width < 0.12, f"Expected CI width < 0.12, but got {width}."
    assert width > 0.05, f"CI width {width} seems suspiciously low for N=5000."