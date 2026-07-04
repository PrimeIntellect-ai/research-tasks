# test_final_state.py

import os
import subprocess
import pytest

def test_executable_exists():
    exe_path = "/home/user/generate_data"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_sensor_data_exists():
    data_path = "/home/user/sensor_data.txt"
    assert os.path.exists(data_path), f"Data file {data_path} does not exist."
    with open(data_path, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1000, f"Expected 1000 lines in {data_path}, found {len(lines)}."

def test_venv_exists():
    python_path = "/home/user/venv/bin/python"
    assert os.path.exists(python_path), f"Virtual environment Python {python_path} does not exist."

def test_ci_results():
    data_path = "/home/user/sensor_data.txt"
    results_path = "/home/user/ci_results.txt"
    python_path = "/home/user/venv/bin/python"

    assert os.path.exists(results_path), f"Results file {results_path} does not exist."

    # Compute expected results using the user's venv (which has numpy installed)
    script = f"""
import numpy as np

data = np.loadtxt('{data_path}')
np.random.seed(42)
n = len(data)
n_bootstraps = 10000

bootstrapped_medians = []
for _ in range(n_bootstraps):
    sample = np.random.choice(data, size=n, replace=True)
    bootstrapped_medians.append(np.median(sample))

lower = np.percentile(bootstrapped_medians, 2.5)
upper = np.percentile(bootstrapped_medians, 97.5)

print(f"Lower: {{lower:.4f}}")
print(f"Upper: {{upper:.4f}}")
"""
    try:
        result = subprocess.run([python_path, "-c", script], capture_output=True, text=True, check=True)
        expected_output = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected results using {python_path}. Is numpy installed? Error: {e.stderr}")

    with open(results_path, "r") as f:
        actual_output = f.read().strip().split('\n')

    assert len(actual_output) == 2, f"Expected 2 lines in {results_path}, found {len(actual_output)}."

    expected_lower = expected_output[0].strip()
    expected_upper = expected_output[1].strip()

    actual_lower = actual_output[0].strip()
    actual_upper = actual_output[1].strip()

    assert actual_lower == expected_lower, f"Lower bound mismatch. Expected '{expected_lower}', got '{actual_lower}'."
    assert actual_upper == expected_upper, f"Upper bound mismatch. Expected '{expected_upper}', got '{actual_upper}'."