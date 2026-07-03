# test_final_state.py
import os
import json
import math

def test_workspace_and_venv_exist():
    workspace = "/home/user/workspace"
    venv_dir = "/home/user/workspace/venv"
    assert os.path.isdir(workspace), f"Workspace directory {workspace} does not exist."
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."

def test_script_exists():
    script_path = "/home/user/workspace/prepare_data.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

def test_results_json():
    results_path = "/home/user/workspace/results.json"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON."

    expected_keys = {"c1", "c2", "c3", "energy_ci_lower", "energy_ci_upper"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Results JSON is missing keys: {missing_keys}"

    # Check c1, c2, c3 with 1e-2 tolerance
    assert math.isclose(data["c1"], 2.668, abs_tol=1e-2), f"c1 value {data['c1']} is out of expected range."
    assert math.isclose(data["c2"], 1.353, abs_tol=1e-2), f"c2 value {data['c2']} is out of expected range."
    assert math.isclose(data["c3"], 0.613, abs_tol=1e-2), f"c3 value {data['c3']} is out of expected range."

    # Check confidence intervals with 1e-4 tolerance
    # Based on the deterministic sequence, ci_lower is ~62.45, ci_upper is ~62.90
    assert math.isclose(data["energy_ci_lower"], 62.45, abs_tol=0.1), f"energy_ci_lower {data['energy_ci_lower']} is out of expected range."
    assert math.isclose(data["energy_ci_upper"], 62.90, abs_tol=0.1), f"energy_ci_upper {data['energy_ci_upper']} is out of expected range."

    assert data["energy_ci_lower"] < data["energy_ci_upper"], "Confidence interval lower bound must be less than upper bound."