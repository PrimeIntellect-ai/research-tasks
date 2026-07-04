# test_final_state.py

import os
import json
import subprocess
import math

def test_profiler_script_exists_and_executable():
    """Verify that /home/user/profiler.sh exists and is executable."""
    script_path = "/home/user/profiler.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_profiler_script_execution_and_output():
    """Run the profiler script and verify the resulting JSON output."""
    script_path = "/home/user/profiler.sh"
    results_path = "/home/user/results.json"

    # Remove results.json if it exists to ensure the script creates it
    if os.path.exists(results_path):
        os.remove(results_path)

    # Run the script
    try:
        subprocess.run([script_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Execution of {script_path} failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}"

    # Check if results.json was created
    assert os.path.exists(results_path), f"The script did not create {results_path}."

    # Read and parse the JSON
    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{results_path} does not contain valid JSON."

    # Check keys
    expected_keys = {"kde_110", "cholesky_norm", "optimal_x"}
    assert set(data.keys()) == expected_keys, f"JSON keys {set(data.keys())} do not match expected keys {expected_keys}."

    # Check values
    expected_values = {
        "kde_110": 0.0215,
        "cholesky_norm": 3137.9576,
        "optimal_x": 99.7208
    }

    for key, expected_val in expected_values.items():
        val = data[key]
        assert isinstance(val, (int, float)), f"Value for {key} is not a number."
        assert math.isclose(val, expected_val, rel_tol=1e-4, abs_tol=1e-4), \
            f"Value for {key} is {val}, expected approximately {expected_val}."