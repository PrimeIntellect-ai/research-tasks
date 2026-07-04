# test_final_state.py

import os
import subprocess
import pytest

def test_env_var_txt():
    path = "/home/user/env_var.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "MALLOC_PERTURB_", f"Expected 'MALLOC_PERTURB_' in {path}, got '{content}'."

def test_trace_txt():
    path = "/home/user/trace.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "11", f"Expected '11' in {path}, got '{content}'."

def test_regression_sh():
    path = "/home/user/regression.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Execute the regression script
    result = subprocess.run([path], cwd="/home/user", capture_output=True)
    assert result.returncode == 0, f"Expected {path} to exit with 0, but exited with {result.returncode}."