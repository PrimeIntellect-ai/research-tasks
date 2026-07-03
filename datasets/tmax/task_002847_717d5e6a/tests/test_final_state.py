# test_final_state.py

import os
import json
import math
import pytest

def test_simulation_cpp_fixed():
    """Check if simulation.cpp contains the reduction clause."""
    cpp_file = "/home/user/sim/simulation.cpp"
    assert os.path.exists(cpp_file), f"File {cpp_file} does not exist."

    with open(cpp_file, "r") as f:
        content = f.read()

    assert "reduction" in content and "global_sum" in content, "The C++ code does not seem to have the OpenMP reduction clause for global_sum."

def test_output_files_exist():
    """Check if the C++ program was compiled and run successfully."""
    assert os.path.exists("/home/user/sim/signal.txt"), "signal.txt was not generated."
    assert os.path.exists("/home/user/sim/sum.txt"), "sum.txt was not generated."

def test_analyze_py_exists():
    """Check if the Python analysis script exists."""
    assert os.path.exists("/home/user/sim/analyze.py"), "analyze.py does not exist."

def test_results_json():
    """Check if results.json is correctly formatted and contains expected values."""
    json_file = "/home/user/sim/results.json"
    assert os.path.exists(json_file), f"{json_file} does not exist."

    with open(json_file, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    expected_keys = {"global_sum", "dominant_freq", "ks_statistic", "p_value"}
    assert set(results.keys()) == expected_keys, f"results.json keys do not match expected keys. Found: {list(results.keys())}"

    for key in expected_keys:
        assert isinstance(results[key], (int, float)), f"Value for {key} must be a float."

    # Check dominant frequency
    assert math.isclose(results["dominant_freq"], 50.0, abs_tol=1.0), f"Dominant frequency should be 50 Hz, got {results['dominant_freq']}"

    # Check global sum
    # The sum of 10000 noise terms where each is roughly uniform [-0.5, 0.5] is around 0.
    # The actual deterministic sum is approximately -0.05.
    assert math.isclose(results["global_sum"], -0.05, abs_tol=0.1), f"Global sum is incorrect, got {results['global_sum']}"

    # Check that ks_statistic and p_value are valid probabilities/statistics
    assert 0.0 <= results["ks_statistic"] <= 1.0, "KS statistic must be between 0 and 1."
    assert 0.0 <= results["p_value"] <= 1.0, "p-value must be between 0 and 1."