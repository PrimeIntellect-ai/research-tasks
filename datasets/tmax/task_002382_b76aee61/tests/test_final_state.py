# test_final_state.py

import os
import json
import pytest

def test_massive_data_recovered():
    file_path = "/home/user/pipeline/massive_data.yaml"
    assert os.path.exists(file_path), f"{file_path} was not recovered."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_c_extension_available():
    try:
        from yaml import CSafeLoader
    except ImportError:
        pytest.fail("yaml.CSafeLoader could not be imported. The PyYAML C-extension was not properly compiled and installed.")

def test_benchmark_results_and_metric():
    results_path = "/home/user/pipeline/benchmark_results.json"
    assert os.path.exists(results_path), f"{results_path} does not exist. Did you run the benchmark script?"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {results_path} as valid JSON.")

    assert "time_taken" in data, f"'time_taken' key not found in {results_path}."

    time_taken = data["time_taken"]
    assert isinstance(time_taken, (int, float)), "'time_taken' must be a number."

    assert time_taken < 0.5, f"Execution time metric failed: expected < 0.5 seconds, got {time_taken} seconds."