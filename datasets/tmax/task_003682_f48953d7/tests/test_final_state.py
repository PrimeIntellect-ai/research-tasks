# test_final_state.py

import os
import ctypes
import pytest

PROJECT_DIR = "/home/user/sim_project"
MAKEFILE_PATH = os.path.join(PROJECT_DIR, "Makefile")
SIMULATE_CPP_PATH = os.path.join(PROJECT_DIR, "simulate.cpp")
DIAGNOSTIC_LOG_PATH = os.path.join(PROJECT_DIR, "diagnostic.log")
OUTPUT_CSV_PATH = os.path.join(PROJECT_DIR, "output.csv")
BASELINE_CSV_PATH = os.path.join(PROJECT_DIR, "baseline.csv")

def compute_expected_divergence():
    """
    Simulates the C++ float precision loss bug to find the exact iteration
    where the absolute difference strictly exceeds 0.01.
    """
    val_double = 1.0
    val_buggy = 1.0

    for i in range(1, 101):
        # Baseline step
        val_double = val_double * 1.05

        # Buggy step: cast to float, then passed to compute_step_v2 which does * 1.05 in double
        temp = ctypes.c_float(val_buggy).value
        val_buggy = temp * 1.05

        if abs(val_double - val_buggy) > 0.01:
            return i

    return -1

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile is missing at {MAKEFILE_PATH}"
    with open(MAKEFILE_PATH, 'r') as f:
        content = f.read()

    assert "-lsimmath_v2" in content, "Makefile was not updated to link against libsimmath_v2."
    assert "-lsimmath_v1" not in content, "Makefile still contains the incorrect libsimmath_v1 link."

def test_simulate_cpp_fixed():
    assert os.path.isfile(SIMULATE_CPP_PATH), f"simulate.cpp is missing at {SIMULATE_CPP_PATH}"
    with open(SIMULATE_CPP_PATH, 'r') as f:
        content = f.read()

    assert "float" not in content, "simulate.cpp still contains 'float' which causes precision loss."
    assert "compute_step_v2" in content, "simulate.cpp should call compute_step_v2."

def test_diagnostic_log():
    assert os.path.isfile(DIAGNOSTIC_LOG_PATH), f"diagnostic.log is missing at {DIAGNOSTIC_LOG_PATH}"
    with open(DIAGNOSTIC_LOG_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_iteration = compute_expected_divergence()

    expected_line1 = f"First divergence iteration: {expected_iteration}"
    expected_line2 = "Library linked: libsimmath_v2.so"

    assert any(expected_line1 in line for line in lines), f"diagnostic.log does not contain the correct divergence iteration. Expected: '{expected_line1}'"
    assert any(expected_line2 in line for line in lines), f"diagnostic.log does not contain the correct library linked. Expected: '{expected_line2}'"

def test_output_csv_matches_baseline():
    assert os.path.isfile(OUTPUT_CSV_PATH), f"output.csv is missing at {OUTPUT_CSV_PATH}. Did you run the compiled executable?"
    assert os.path.isfile(BASELINE_CSV_PATH), f"baseline.csv is missing at {BASELINE_CSV_PATH}."

    with open(OUTPUT_CSV_PATH, 'r') as f:
        output_lines = f.read().strip().split('\n')

    with open(BASELINE_CSV_PATH, 'r') as f:
        baseline_lines = f.read().strip().split('\n')

    assert len(output_lines) == len(baseline_lines), "output.csv does not have the same number of lines as baseline.csv."

    # Skip header
    for i in range(1, len(baseline_lines)):
        out_iter, out_val = output_lines[i].split(',')
        base_iter, base_val = baseline_lines[i].split(',')

        assert out_iter == base_iter, f"Iteration mismatch at row {i+1}: expected {base_iter}, got {out_iter}"

        diff = abs(float(out_val) - float(base_val))
        assert diff < 1e-5, f"Value mismatch at iteration {out_iter}: expected {base_val}, got {out_val} (diff: {diff})"