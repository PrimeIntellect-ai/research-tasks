# test_final_state.py

import os
import stat
import pytest

def test_gsl_installed():
    """Verify that GSL headers are installed."""
    header_path = "/usr/include/gsl/gsl_rng.h"
    assert os.path.isfile(header_path), f"GSL development libraries do not appear to be installed. Expected to find {header_path}."

def test_c_source_code_exists():
    """Verify that the C source code file was created."""
    source_path = "/home/user/bootstrap_ci.c"
    assert os.path.isfile(source_path), f"C source file missing at {source_path}."

def test_executable_exists_and_runnable():
    """Verify that the compiled executable exists and has execute permissions."""
    exe_path = "/home/user/bootstrap_ci"
    assert os.path.isfile(exe_path), f"Compiled executable missing at {exe_path}."

    st = os.stat(exe_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {exe_path} is not executable."

def test_experiment_log_exists_and_content():
    """Verify that the experiment log exists and contains the correct appended output."""
    log_path = "/home/user/experiment_log.txt"
    assert os.path.isfile(log_path), f"Experiment log missing at {log_path}."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) > 0, f"Log file {log_path} is empty."

    expected_line = "Feature: measurement_b, Filter: category=X, CI_Lower: 2.0143, CI_Upper: 2.2714"

    # The task requires the result to be appended to the log file.
    # We check if the expected line is the last line or present in the file.
    assert lines[-1] == expected_line, (
        f"The last line of {log_path} does not match the expected output.\n"
        f"Expected: '{expected_line}'\n"
        f"Found: '{lines[-1]}'"
    )