# test_final_state.py

import os
import re

def test_c_source_exists():
    path = "/home/user/validate_model.c"
    assert os.path.exists(path), f"Missing C source file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_executable_exists():
    path = "/home/user/validate_model"
    assert os.path.exists(path), f"Missing executable: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_results_log_exists():
    path = "/home/user/results.log"
    assert os.path.exists(path), f"Missing results log file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_results_log_contents():
    log_path = "/home/user/results.log"
    golden_path = "/home/user/.golden_results"

    assert os.path.exists(log_path), f"Missing file: {log_path}"
    assert os.path.exists(golden_path), f"Missing golden file: {golden_path}"

    with open(log_path, 'r') as f:
        log_lines = [line.strip() for line in f.readlines() if line.strip()]

    with open(golden_path, 'r') as f:
        golden_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(log_lines) == 6, f"Expected exactly 6 non-empty lines in {log_path}, found {len(log_lines)}"

    # Check first 5 lines against golden results
    for i in range(5):
        assert log_lines[i] == golden_lines[i], (
            f"Line {i+1} mismatch.\n"
            f"Expected: '{golden_lines[i]}'\n"
            f"Got:      '{log_lines[i]}'"
        )

    # Check 6th line regex
    compute_time_line = log_lines[5]
    pattern = r"^Compute Time: \d+\.\d{6} seconds$"
    assert re.match(pattern, compute_time_line), (
        f"Line 6 does not match the required format.\n"
        f"Expected format: 'Compute Time: [float.6f] seconds'\n"
        f"Got: '{compute_time_line}'"
    )