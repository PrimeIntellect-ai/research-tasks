# test_final_state.py

import os
import pytest

def test_results_file_exists():
    path = "/home/user/results.txt"
    assert os.path.isfile(path), f"Missing required output file: {path}"

def test_results_format_and_values():
    path = "/home/user/results.txt"
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in {path}, found {len(lines)}"

    # Line 1: p_0, p_1, p_2
    p_parts = lines[0].split(',')
    assert len(p_parts) == 3, f"Line 1 should have 3 comma-separated values, found {len(p_parts)}"
    try:
        p_vals = [float(x) for x in p_parts]
    except ValueError:
        pytest.fail("Line 1 does not contain valid floats")

    # Lines 2-5: single floats
    for i in range(1, 5):
        try:
            float(lines[i])
        except ValueError:
            pytest.fail(f"Line {i+1} does not contain a valid float: {lines[i]}")

def test_analyze_script_executable():
    path = "/home/user/analyze.sh"
    assert os.path.isfile(path), f"Missing required script: {path}"
    assert os.access(path, os.X_OK), f"Script {path} is not executable"