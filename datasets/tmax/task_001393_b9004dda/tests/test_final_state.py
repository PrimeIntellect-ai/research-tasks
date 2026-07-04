# test_final_state.py

import os
import json
import math
import ctypes
import pytest

def test_librhs_so_exists_and_loadable():
    """Check if the shared library was compiled and can be loaded."""
    lib_path = "/home/user/sim_project/librhs.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist."

    try:
        lib = ctypes.CDLL(lib_path)
    except Exception as e:
        pytest.fail(f"Failed to load {lib_path} using ctypes: {e}")

    assert hasattr(lib, "robertson_rhs"), f"Function 'robertson_rhs' not found in {lib_path}."

def test_run_sim_script_exists():
    """Check if the Python simulation script exists."""
    script_path = "/home/user/sim_project/run_sim.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

def test_convergence_result_json():
    """Check if the convergence result JSON exists and contains expected values."""
    json_path = "/home/user/sim_project/convergence_result.json"
    assert os.path.isfile(json_path), f"JSON result file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "baseline_y1" in data, "Key 'baseline_y1' is missing from the JSON file."
    assert "threshold_rtol" in data, "Key 'threshold_rtol' is missing from the JSON file."

    baseline_y1 = data["baseline_y1"]
    threshold_rtol = data["threshold_rtol"]

    assert isinstance(baseline_y1, (int, float)), "baseline_y1 must be a number."
    assert isinstance(threshold_rtol, (int, float)), "threshold_rtol must be a number."

    # The expected baseline_y1 is approximately 0.80345.
    assert 0.800 < baseline_y1 < 0.805, f"baseline_y1 value {baseline_y1} is out of expected range (0.800 - 0.805)."

    # The threshold_rtol must be one of the tested relative tolerances
    valid_rtols = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    assert threshold_rtol in valid_rtols, f"threshold_rtol {threshold_rtol} is not one of the valid sequence values."