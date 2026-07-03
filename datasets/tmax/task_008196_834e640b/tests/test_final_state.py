# test_final_state.py

import os
import subprocess
import pytest

def test_venv_exists():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} does not exist."

    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found in virtual environment at {python_bin}."

def test_packages_installed():
    python_bin = "/home/user/venv/bin/python"

    # Check for numpy, scipy, pandas
    for pkg in ["numpy", "scipy", "pandas"]:
        result = subprocess.run(
            [python_bin, "-c", f"import {pkg}"],
            capture_output=True
        )
        assert result.returncode == 0, f"Package '{pkg}' is not installed in the virtual environment."

def test_filter_data_script_exists():
    script_path = "/home/user/filter_data.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

def test_valid_runs_output():
    output_path = "/home/user/valid_runs.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["run_0.csv", "run_3.csv"]

    assert lines == expected, f"Content of {output_path} is incorrect. Expected {expected}, got {lines}."