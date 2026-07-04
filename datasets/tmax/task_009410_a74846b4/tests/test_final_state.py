# test_final_state.py

import os
import re
import pytest

def test_simulate_executable_exists():
    path = "/home/user/simulate"
    assert os.path.isfile(path), f"Executable missing: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_experimental_data_csv_exists():
    path = "/home/user/experimental_data.csv"
    assert os.path.isfile(path), f"File missing: {path}"

def test_experimental_data_h5_exists():
    path = "/home/user/experimental_data.h5"
    assert os.path.isfile(path), f"File missing: {path}"

def test_fit_plot_exists():
    path = "/home/user/fit_plot.png"
    assert os.path.isfile(path), f"File missing: {path}"
    # Check if it's a valid PNG file by looking at the magic number
    with open(path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"File {path} is not a valid PNG image."

def test_result_txt():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    match = re.match(r"^k2=(\d+\.\d{3})$", content)
    assert match is not None, f"result.txt content '{content}' does not match the exact format 'k2=X.XXX'"

    k2_val = float(match.group(1))
    # The simulated data uses k2 = 0.8. The fitted value should be exactly 0.800.
    assert abs(k2_val - 0.800) < 0.05, f"Fitted k2 value {k2_val} is too far from the expected 0.800"