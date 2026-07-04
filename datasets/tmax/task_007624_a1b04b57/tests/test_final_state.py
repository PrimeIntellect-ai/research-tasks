# test_final_state.py
import os
import json
import pytest

RESULTS_PATH = "/home/user/results.json"

def test_results_file_exists():
    """Verify that the results.json file has been created."""
    assert os.path.isfile(RESULTS_PATH), f"Expected results file at {RESULTS_PATH} is missing."

def test_results_json_format_and_keys():
    """Verify the JSON structure and required keys."""
    assert os.path.isfile(RESULTS_PATH), f"Missing {RESULTS_PATH}"

    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON.")

    required_keys = {"k", "variance_explained", "benchmark_ms"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"Missing required keys in JSON: {missing_keys}"

def test_results_values():
    """Verify the computed values in the results.json file."""
    assert os.path.isfile(RESULTS_PATH), f"Missing {RESULTS_PATH}"

    with open(RESULTS_PATH, 'r') as f:
        data = json.load(f)

    # Check k
    k_val = data.get("k")
    assert isinstance(k_val, int), f"'k' must be an integer, got {type(k_val)}"
    assert k_val == 6, f"Expected k to be 6, got {k_val}"

    # Check variance_explained
    var_val = data.get("variance_explained")
    assert isinstance(var_val, float), f"'variance_explained' must be a float, got {type(var_val)}"
    assert 0.90 < var_val < 0.91, f"Expected variance_explained to be between 0.90 and 0.91, got {var_val}"

    # Check benchmark_ms
    bench_val = data.get("benchmark_ms")
    assert isinstance(bench_val, (int, float)), f"'benchmark_ms' must be a number, got {type(bench_val)}"
    assert bench_val > 0, f"Expected benchmark_ms to be a positive number, got {bench_val}"