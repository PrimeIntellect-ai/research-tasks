# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_results_file_exists_and_valid():
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"{results_path} does not exist. Did you run the pipeline?"
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"{results_path} does not contain a valid float. Found: {content}")

    assert 0.01 <= val <= 0.08, f"Wasserstein distance {val} in {results_path} is outside expected bounds [0.01, 0.08]."

def test_mcmc_script_exists():
    script_path = "/home/user/mcmc_gc.py"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_run_pipeline_script_exists():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_test_mcmc_script_exists_and_passes():
    script_path = "/home/user/test_mcmc.py"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    # Run the student's pytest script
    result = subprocess.run([sys.executable, "-m", "pytest", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest {script_path} failed. Output:\n{result.stdout}\n{result.stderr}"