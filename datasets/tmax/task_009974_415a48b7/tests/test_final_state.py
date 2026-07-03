# test_final_state.py

import os
import json
import math
import pytest

PROJECT_DIR = "/home/user/sim_project"
SO_FILE = os.path.join(PROJECT_DIR, "libintegrator.so")
PY_FILE = os.path.join(PROJECT_DIR, "run_sim.py")
RESULTS_FILE = os.path.join(PROJECT_DIR, "results.json")

def test_shared_library_exists():
    """Test that the C code was compiled into a shared library."""
    assert os.path.exists(SO_FILE), f"Shared library {SO_FILE} does not exist."
    assert os.path.isfile(SO_FILE), f"Path {SO_FILE} is not a file."

def test_python_script_exists():
    """Test that the Python script was created."""
    assert os.path.exists(PY_FILE), f"Python script {PY_FILE} does not exist."
    assert os.path.isfile(PY_FILE), f"Path {PY_FILE} is not a file."

def test_results_json_exists_and_valid():
    """Test that results.json exists, is valid JSON, and has the correct keys."""
    assert os.path.exists(RESULTS_FILE), f"Results file {RESULTS_FILE} does not exist."

    with open(RESULTS_FILE, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_FILE} does not contain valid JSON.")

    expected_keys = {"error_dt_0.1", "error_dt_0.01", "error_dt_0.001"}
    assert set(results.keys()) == expected_keys, f"JSON keys do not match expected keys. Found: {list(results.keys())}"

    for key in expected_keys:
        assert isinstance(results[key], (int, float)), f"Value for {key} is not a number."

def test_results_values():
    """Test that the computed errors are within expected bounds."""
    with open(RESULTS_FILE, 'r') as f:
        results = json.load(f)

    err_01 = results["error_dt_0.1"]
    err_001 = results["error_dt_0.01"]
    err_0001 = results["error_dt_0.001"]

    # Check instability for dt=0.1 (RK4 is unstable for lambda*dt = -100 * 0.1 = -10)
    assert math.isnan(err_01) or math.isinf(err_01) or err_01 > 1000.0, \
        f"Expected large error for dt=0.1 due to instability, got {err_01}"

    # Check convergence for stable dt
    assert 1e-6 < err_001 < 1e-4, f"Unexpected error for dt=0.01: {err_001}. Expected between 1e-6 and 1e-4."
    assert 1e-10 < err_0001 < 1e-7, f"Unexpected error for dt=0.001: {err_0001}. Expected between 1e-10 and 1e-7."