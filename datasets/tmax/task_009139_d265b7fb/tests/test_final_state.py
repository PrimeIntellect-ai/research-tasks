# test_final_state.py

import os
import pytest

SCRIPT_PATH = "/home/user/fit_models.sh"
RESULTS_PATH = "/home/user/regression_results.csv"

EXPECTED_RESULTS = [
    "Jupiter,3.00,2.00",
    "Mars,10.00,0.00",
    "Saturn,10.00,-60.00",
    "Venus,-10.00,110.00"
]

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_results_file_exists():
    assert os.path.isfile(RESULTS_PATH), f"Results file {RESULTS_PATH} is missing."

def test_results_content():
    with open(RESULTS_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(EXPECTED_RESULTS), f"Expected {len(EXPECTED_RESULTS)} lines in {RESULTS_PATH}, found {len(lines)}."

    for i, expected_line in enumerate(EXPECTED_RESULTS):
        assert lines[i] == expected_line, f"Line {i+1} mismatch. Expected '{expected_line}', got '{lines[i]}'."