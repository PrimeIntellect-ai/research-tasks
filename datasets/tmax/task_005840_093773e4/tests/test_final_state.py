# test_final_state.py

import os
import stat
import json
import subprocess
import pytest

def test_pipeline_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Expected pipeline script not found at {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pipeline script at {path} is not executable"

def test_pipeline_invalid_csv():
    path = "/home/user/pipeline.sh"
    invalid_csv = "/home/user/invalid.csv"

    result = subprocess.run([path, invalid_csv], capture_output=True)
    assert result.returncode == 1, f"Expected exit code 1 when running with invalid CSV, got {result.returncode}"

def test_pipeline_valid_csv():
    path = "/home/user/pipeline.sh"
    valid_csv = "/home/user/valid.csv"

    # Ensure any previous artifacts are removed
    if os.path.exists("output_plot.png"):
        os.remove("output_plot.png")
    if os.path.exists("/home/user/results.json"):
        os.remove("/home/user/results.json")

    result = subprocess.run([path, valid_csv], capture_output=True, cwd="/home/user")
    assert result.returncode == 0, f"Expected exit code 0 when running with valid CSV, got {result.returncode}. stderr: {result.stderr.decode()}"

def test_output_plot_created():
    # After running the valid CSV, the plot should exist
    plot_path = "/home/user/output_plot.png"
    assert os.path.isfile(plot_path), "output_plot.png was not created. Ensure matplotlib headless backend is configured properly."

def test_results_json_structure():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"{results_path} was not created."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    expected_keys = {"mean_threads_1", "mean_threads_4", "p_value"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match. Expected {expected_keys}, got {set(data.keys())}"

    for key in expected_keys:
        val = data[key]
        assert isinstance(val, (int, float)), f"Value for {key} should be a float, got {type(val)}"