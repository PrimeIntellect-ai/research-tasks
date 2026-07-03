# test_final_state.py

import os
import json
import pytest

def test_libtensor_so_exists():
    """Test that the compiled shared library exists."""
    so_file = "/home/user/src/libtensor.so"
    assert os.path.isfile(so_file), f"Compiled library {so_file} does not exist."

def test_profile_ops_script_exists():
    """Test that the profiling script exists."""
    script_file = "/home/user/profile_ops.py"
    assert os.path.isfile(script_file), f"Profiling script {script_file} does not exist."

def test_profiling_results_json():
    """Test that the profiling results JSON exists and has the correct structure/values."""
    results_file = "/home/user/profiling_results.json"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    with open(results_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON.")

    # Check keys
    required_keys = {"N_values", "times", "exponent_b"}
    assert required_keys.issubset(data.keys()), f"JSON missing keys. Expected {required_keys}, found {list(data.keys())}."

    # Check N_values
    expected_n_values = [50, 100, 150, 200, 250]
    assert data["N_values"] == expected_n_values, f"Expected N_values {expected_n_values}, got {data['N_values']}."

    # Check times
    times = data["times"]
    assert isinstance(times, list), "'times' should be a list."
    assert len(times) == 5, f"Expected 5 time values, got {len(times)}."
    assert all(isinstance(t, (int, float)) for t in times), "All time values must be numeric."

    # Check exponent_b
    b = data["exponent_b"]
    assert isinstance(b, (int, float)), "'exponent_b' must be numeric."
    assert 2.5 <= b <= 3.5, f"Exponent {b} is far from the expected ~3.0 (must be between 2.5 and 3.5)."