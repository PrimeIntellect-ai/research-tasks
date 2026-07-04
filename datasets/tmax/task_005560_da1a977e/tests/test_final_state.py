# test_final_state.py

import os
import json
import pytest

def test_executable_exists_and_is_executable():
    """Test that the compiled executable exists and is executable."""
    executable_path = "/home/user/sim/run_sim"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_results_txt():
    """Test that results.txt exists and contains exactly 500 lines of floats."""
    results_path = "/home/user/data/results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    with open(results_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 500, f"Expected exactly 500 lines in {results_path}, but found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            float(line.strip())
        except ValueError:
            pytest.fail(f"Line {i+1} in {results_path} is not a valid float: '{line.strip()}'")

def test_executed_notebook_exists():
    """Test that the executed Jupyter notebook exists."""
    executed_notebook_path = "/home/user/analysis/bootstrap_ci_executed.ipynb"
    assert os.path.isfile(executed_notebook_path), f"Executed notebook {executed_notebook_path} does not exist."

def test_final_ci_json():
    """Test that final_ci.json exists, is valid JSON, and contains the correct keys."""
    json_path = "/home/user/data/final_ci.json"
    assert os.path.isfile(json_path), f"JSON file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "ci_lower" in data, f"Key 'ci_lower' missing from {json_path}."
    assert "ci_upper" in data, f"Key 'ci_upper' missing from {json_path}."

    assert isinstance(data["ci_lower"], float), "'ci_lower' should be a float."
    assert isinstance(data["ci_upper"], float), "'ci_upper' should be a float."