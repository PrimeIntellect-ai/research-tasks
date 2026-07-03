# test_final_state.py

import os
import stat
import json
import math
import pytest
import subprocess

def test_c_source_exists():
    path = "/home/user/src/pareto_fit.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

def test_regression_script_exists_and_executable():
    path = "/home/user/src/regression.sh"
    assert os.path.isfile(path), f"Regression script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Regression script {path} is not executable."

def test_executable_exists():
    path = "/home/user/src/pareto_fit"
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_regression_script_passes():
    path = "/home/user/src/regression.sh"
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression script failed with return code {result.returncode}. Stderr: {result.stderr}"

def test_fit_results_json():
    target_data_path = "/home/user/data/target_data.txt"
    assert os.path.isfile(target_data_path), f"Data file {target_data_path} is missing."

    with open(target_data_path, "r") as f:
        data = [float(line.strip()) for line in f if line.strip()]

    assert len(data) > 0, "Target data is empty."

    expected_xm = min(data)
    sum_ln = sum(math.log(x / expected_xm) for x in data)
    expected_alpha = len(data) / sum_ln

    expected_xm_rounded = round(expected_xm, 3)
    expected_alpha_rounded = round(expected_alpha, 3)

    json_path = "/home/user/fit_results.json"
    assert os.path.isfile(json_path), f"Results JSON file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "xm" in results, f"Key 'xm' missing from {json_path}"
    assert "alpha" in results, f"Key 'alpha' missing from {json_path}"

    assert math.isclose(results["xm"], expected_xm_rounded, rel_tol=1e-3), \
        f"Expected xm ~ {expected_xm_rounded}, got {results['xm']}"
    assert math.isclose(results["alpha"], expected_alpha_rounded, rel_tol=1e-3), \
        f"Expected alpha ~ {expected_alpha_rounded}, got {results['alpha']}"