# test_final_state.py

import os
import pytest

def test_executable_exists():
    exe_path = "/home/user/project/spectral_analyzer"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you compile the C++ code?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_results_log_exists():
    log_path = "/home/user/project/results.log"
    assert os.path.isfile(log_path), f"Results log {log_path} does not exist. Did you pipe the output?"

def test_results_log_content():
    log_path = "/home/user/project/results.log"
    if not os.path.isfile(log_path):
        pytest.fail(f"Results log {log_path} does not exist.")

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Mean: 1000000.3000",
        "Variance: 0.0200",
        "Calibration Coefficient: 1.1414"
    ]

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert len(actual_lines) == 3, f"Expected 3 lines of output, got {len(actual_lines)}. Content:\n{content}"

    assert actual_lines[0] == expected_lines[0], f"Expected first line to be '{expected_lines[0]}', got '{actual_lines[0]}'"
    assert actual_lines[1] == expected_lines[1], f"Expected second line to be '{expected_lines[1]}', got '{actual_lines[1]}'"
    assert actual_lines[2] == expected_lines[2], f"Expected third line to be '{expected_lines[2]}', got '{actual_lines[2]}'"