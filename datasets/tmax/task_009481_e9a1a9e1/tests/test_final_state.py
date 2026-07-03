# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

def test_run_sh_exists_and_executable():
    """Verify that /home/user/run.sh exists and is executable."""
    run_sh_path = "/home/user/run.sh"
    assert os.path.exists(run_sh_path), f"File not found: {run_sh_path}"
    assert os.path.isfile(run_sh_path), f"Path is not a file: {run_sh_path}"

    st = os.stat(run_sh_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {run_sh_path} is not executable"

def test_train_py_exists():
    """Verify that /home/user/train.py exists."""
    train_py_path = "/home/user/train.py"
    assert os.path.exists(train_py_path), f"File not found: {train_py_path}"
    assert os.path.isfile(train_py_path), f"Path is not a file: {train_py_path}"

def test_run_sh_execution():
    """Verify that /home/user/run.sh executes successfully."""
    run_sh_path = "/home/user/run.sh"

    # Remove results.json if it exists to ensure the script creates it
    results_path = "/home/user/results.json"
    if os.path.exists(results_path):
        os.remove(results_path)

    try:
        result = subprocess.run(
            [run_sh_path],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"{run_sh_path} failed to execute with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

def test_results_json():
    """Verify that /home/user/results.json is created and has the correct format."""
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"File not found: {results_path}. Did train.py run successfully?"

    try:
        with open(results_path, 'r') as f:
            results = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {results_path} is not valid JSON.")

    assert "best_alpha" in results, f"Key 'best_alpha' missing in {results_path}"
    assert "best_score" in results, f"Key 'best_score' missing in {results_path}"

    assert isinstance(results["best_alpha"], (int, float)), "best_alpha must be a number"
    assert isinstance(results["best_score"], (int, float)), "best_score must be a number"

    assert results["best_alpha"] in [0.1, 1.0, 10.0], f"best_alpha {results['best_alpha']} is not one of the grid values [0.1, 1.0, 10.0]"