# test_final_state.py

import os
import json
import subprocess
import math
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_graph.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution_and_results():
    script_path = "/home/user/process_graph.sh"
    results_path = "/home/user/results.json"

    # Remove results.json if it exists to ensure the script creates it
    if os.path.exists(results_path):
        os.remove(results_path)

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. STDERR: {result.stderr}"

    # Check if results.json was created
    assert os.path.isfile(results_path), f"File {results_path} was not created by the script."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected_values = {
        "mean_degree": 2.0000,
        "std_degree": 0.6325,
        "slope": 0.3750,
        "intercept": -0.4600,
        "critical_threshold": 2.5600
    }

    for key, expected in expected_values.items():
        assert key in data, f"Key '{key}' is missing from the JSON output."
        actual = data[key]
        assert isinstance(actual, (int, float)), f"Value for '{key}' must be a number."
        assert math.isclose(actual, expected, abs_tol=1e-4), \
            f"Value for '{key}' is {actual}, expected {expected} (rounded to 4 decimal places)."