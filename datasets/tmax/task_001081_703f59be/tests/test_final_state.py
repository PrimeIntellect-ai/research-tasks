# test_final_state.py

import os
import subprocess
import pytest

def test_libgsl_dev_installed():
    """Check if libgsl-dev is installed."""
    # We can check for the presence of a key GSL header file
    gsl_header_path = "/usr/include/gsl/gsl_math.h"
    dpkg_check = subprocess.run(["dpkg", "-l", "libgsl-dev"], capture_output=True, text=True)

    assert os.path.isfile(gsl_header_path) or dpkg_check.returncode == 0, \
        "libgsl-dev package does not appear to be installed."

def test_process_data_c_exists():
    """Check if the C source file exists."""
    c_file = "/home/user/process_data.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."

def test_process_data_executable_exists():
    """Check if the compiled executable exists and is executable."""
    executable = "/home/user/process_data"
    assert os.path.isfile(executable), f"Compiled executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_run_experiments_sh_exists():
    """Check if the bash script exists and is executable."""
    script = "/home/user/run_experiments.sh"
    assert os.path.isfile(script), f"Bash script {script} is missing."
    assert os.access(script, os.X_OK), f"File {script} is not executable."

def test_tracker_csv_content():
    """Check if tracker.csv exists and has the correct output."""
    tracker_file = "/home/user/tracker.csv"
    assert os.path.isfile(tracker_file), f"Tracker file {tracker_file} is missing."

    with open(tracker_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "/home/user/data/exp1.csv,6.3333",
        "/home/user/data/exp2.csv,0.0000",
        "/home/user/data/exp3.csv,SCHEMA_ERROR",
        "/home/user/data/exp4.csv,SCHEMA_ERROR"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in tracker.csv, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in tracker.csv is incorrect. Expected: '{expected}', Got: '{actual}'"