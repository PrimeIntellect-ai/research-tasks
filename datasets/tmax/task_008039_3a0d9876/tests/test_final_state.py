# test_final_state.py

import os
import subprocess
import pytest

def test_failing_input_file():
    path = "/home/user/failing_input.txt"
    assert os.path.isfile(path), f"Expected file {path} to exist."
    with open(path, "r") as f:
        val = f.read().strip()
    assert val in ["0", "1"], f"Expected {path} to contain '0' or '1', but got '{val}'."

def test_fixed_executable_exists():
    path = "/home/user/fixed_newton_root"
    assert os.path.isfile(path), f"Expected executable {path} to exist."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_convergence_failure_handling():
    # Read the failing input from the file
    path = "/home/user/failing_input.txt"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} is missing, cannot test convergence failure.")

    with open(path, "r") as f:
        val = f.read().strip()

    if val not in ["0", "1"]:
        val = "0"  # fallback to a known failing input if file is incorrect

    executable = "/home/user/fixed_newton_root"
    if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
        pytest.fail(f"Executable {executable} is missing or not executable.")

    result = subprocess.run([executable, val], capture_output=True, text=True)

    assert result.returncode == 1, f"Expected exit code 1 for failing input {val}, got {result.returncode}."
    assert "Convergence failed" in result.stdout or "Convergence failed" in result.stderr, \
        f"Expected 'Convergence failed' in output for failing input {val}, got: {result.stdout}{result.stderr}"

def test_normal_convergence():
    executable = "/home/user/fixed_newton_root"
    if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
        pytest.fail(f"Executable {executable} is missing or not executable.")

    result = subprocess.run([executable, "2"], capture_output=True, text=True)

    assert result.returncode == 0, f"Expected exit code 0 for valid input '2', got {result.returncode}."
    assert "Root found" in result.stdout, f"Expected 'Root found' in output for valid input '2', got: {result.stdout}"