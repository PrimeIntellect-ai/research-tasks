# test_final_state.py

import os
import subprocess
import pytest

def test_run_regression_script_exists_and_executable():
    script_path = "/home/user/run_regression.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution_and_outputs():
    script_path = "/home/user/run_regression.sh"

    # Clean up previous runs if any
    if os.path.exists("/home/user/current_runs.txt"):
        os.remove("/home/user/current_runs.txt")
    if os.path.exists("/home/user/regression_result.log"):
        os.remove("/home/user/regression_result.log")

    # Execute the script as user
    try:
        subprocess.run(['su', '-', 'user', '-c', script_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with return code {e.returncode}. Stderr: {e.stderr}")

    # Check current_runs.txt
    runs_file = "/home/user/current_runs.txt"
    assert os.path.isfile(runs_file), f"{runs_file} was not created."

    with open(runs_file, 'r') as f:
        lines = f.read().strip().split('\n')

    # Filter out any empty lines
    lines = [line for line in lines if line.strip()]
    assert len(lines) == 50, f"Expected 50 runs in {runs_file}, found {len(lines)}."

    # Check regression_result.log
    result_file = "/home/user/regression_result.log"
    assert os.path.isfile(result_file), f"{result_file} was not created."

    with open(result_file, 'r') as f:
        result = f.read().strip()

    assert result == "PASS", f"Expected 'PASS' in {result_file}, got '{result}'."