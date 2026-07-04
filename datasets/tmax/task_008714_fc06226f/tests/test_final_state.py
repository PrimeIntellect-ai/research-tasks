# test_final_state.py
import os
import json
import pytest
import math

def test_notebook_exists():
    """Test that the Jupyter notebook was created."""
    notebook_path = "/home/user/heat_sim.ipynb"
    assert os.path.exists(notebook_path), f"Jupyter notebook {notebook_path} was not created."

def test_json_output():
    """Test that the JSON results file is created and contains the correct values."""
    json_path = "/home/user/sim_results.json"
    assert os.path.exists(json_path), f"Results file {json_path} was not created."

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file.")

    expected_keys = {"dt_max_N20", "dt_max_N40", "T_center_N20", "T_center_N40"}
    assert set(results.keys()) == expected_keys, f"JSON file must contain exactly keys: {expected_keys}"

    # Expected values derived from the problem statement
    expected_dt_max_20 = 0.0125
    expected_dt_max_40 = 0.003125
    expected_T_c_20 = 4.811568285918235
    expected_T_c_40 = 4.887293521035074

    assert math.isclose(results["dt_max_N20"], expected_dt_max_20, rel_tol=1e-5), \
        f"dt_max_N20 is incorrect. Expected {expected_dt_max_20}, got {results['dt_max_N20']}"

    assert math.isclose(results["dt_max_N40"], expected_dt_max_40, rel_tol=1e-5), \
        f"dt_max_N40 is incorrect. Expected {expected_dt_max_40}, got {results['dt_max_N40']}"

    assert math.isclose(results["T_center_N20"], expected_T_c_20, rel_tol=1e-5), \
        f"T_center_N20 is incorrect. Expected {expected_T_c_20}, got {results['T_center_N20']}"

    assert math.isclose(results["T_center_N40"], expected_T_c_40, rel_tol=1e-5), \
        f"T_center_N40 is incorrect. Expected {expected_T_c_40}, got {results['T_center_N40']}"