# test_final_state.py
import os
import json
import pytest

def test_cpp_file_exists():
    path = "/home/user/process_signals.cpp"
    assert os.path.isfile(path), f"C++ source file is missing: {path}"

def test_executable_exists():
    path = "/home/user/process_signals"
    assert os.path.isfile(path), f"Executable file is missing: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_profiling_results_json():
    path = "/home/user/profiling_results.json"
    assert os.path.isfile(path), f"Profiling results JSON is missing: {path}"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("profiling_results.json is not a valid JSON file.")

    assert "num_threads_used" in data, "Key 'num_threads_used' is missing from JSON."
    assert "max_absolute_error" in data, "Key 'max_absolute_error' is missing from JSON."

    # Check exact format requirement (only these two keys)
    assert len(data.keys()) == 2, f"JSON should contain exactly two keys, found: {list(data.keys())}"

    assert data["num_threads_used"] == 4, f"Expected 4 threads, but got: {data['num_threads_used']}"

    mae = data["max_absolute_error"]
    assert isinstance(mae, (int, float)), "max_absolute_error must be a number."
    assert abs(mae) < 1e-4, f"max_absolute_error is too high: {mae} (expected < 1e-4)"