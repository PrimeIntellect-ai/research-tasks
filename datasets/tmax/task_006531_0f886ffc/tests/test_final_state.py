# test_final_state.py
import os
import json
import subprocess
import pytest
import math

def test_run_e2e_script_and_results():
    script_path = "/home/user/run_e2e.sh"
    results_path = "/home/user/e2e_results.json"

    # Clean up previous results if they exist to ensure we're testing the script's execution
    if os.path.exists(results_path):
        os.remove(results_path)

    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} does not have executable permissions."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"The script {script_path} failed with return code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    assert os.path.exists(results_path), f"The results file {results_path} was not created by the script."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {results_path}: {e}")

    assert "collatz_27" in data, "The key 'collatz_27' is missing from the JSON results."
    assert isinstance(data["collatz_27"], int), "The value for 'collatz_27' must be an integer."
    assert data["collatz_27"] == 111, f"Expected 'collatz_27' to be 111, but got {data['collatz_27']}."

    assert "determinant" in data, "The key 'determinant' is missing from the JSON results."
    assert isinstance(data["determinant"], (int, float)), "The value for 'determinant' must be a number."
    assert math.isclose(data["determinant"], 4.0, rel_tol=1e-5), (
        f"Expected 'determinant' to be approximately 4.0, but got {data['determinant']}."
    )