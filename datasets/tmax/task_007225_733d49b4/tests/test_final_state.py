# test_final_state.py

import os
import subprocess

def test_venv_exists():
    """Verify that the virtual environment exists and has a python executable."""
    venv_dir = '/home/user/etl_venv'
    python_exec = os.path.join(venv_dir, 'bin', 'python')

    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."
    assert os.path.isfile(python_exec), f"Python executable not found at {python_exec}."
    assert os.access(python_exec, os.X_OK), f"Python executable at {python_exec} is not executable."

def test_packages_installed():
    """Verify that numpy and pandas are installed in the virtual environment."""
    python_exec = '/home/user/etl_venv/bin/python'

    # Check numpy
    result_numpy = subprocess.run([python_exec, '-c', 'import numpy'], capture_output=True)
    assert result_numpy.returncode == 0, "numpy is not installed in the virtual environment."

    # Check pandas
    result_pandas = subprocess.run([python_exec, '-c', 'import pandas'], capture_output=True)
    assert result_pandas.returncode == 0, "pandas is not installed in the virtual environment."

def test_script_exists():
    """Verify that the python script exists."""
    script_path = '/home/user/test_etl_bootstrap.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_results_file_and_content():
    """Verify that the results file exists and contains the correct bootstrap confidence interval."""
    results_path = '/home/user/bootstrap_results.txt'
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    with open(results_path, 'r') as f:
        content = f.read().strip()

    expected_content = "98.02,101.48"
    assert content == expected_content, f"Expected results file content '{expected_content}', but found '{content}'."