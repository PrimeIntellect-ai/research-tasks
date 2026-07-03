# test_final_state.py

import os
import json
import math
import pytest

def test_steady_states_json_exists_and_correct():
    """Test that steady_states.json exists and contains the correct analytical means."""
    json_path = "/home/user/steady_states.json"
    assert os.path.isfile(json_path), f"The file {json_path} does not exist. Did you run the script?"

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected = {
        "1": 0.4851259169604859,
        "2": 0.4891152069695679,
        "3": 0.5186938920150536,
        "4": 0.5401828519137887
    }

    for seed, expected_mean in expected.items():
        assert seed in results, f"Seed '{seed}' is missing from the JSON output."
        actual_mean = results[seed]
        assert isinstance(actual_mean, float), f"Value for seed '{seed}' should be a float."
        assert math.isclose(actual_mean, expected_mean, rel_tol=1e-9), \
            f"Mean for seed '{seed}' is incorrect. Expected {expected_mean}, got {actual_mean}."

def test_run_diffusion_script_modifications():
    """Test that the run_diffusion.py script was properly optimized and modified."""
    script_path = "/home/user/run_diffusion.py"
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # 1. Integrator fix
    has_stiff_solver = any(method in content for method in ["method='BDF'", 'method="BDF"', "method='LSODA'", 'method="LSODA"', "method='Radau'", 'method="Radau"'])
    assert has_stiff_solver, "The script does not use a stiff solver (BDF, LSODA, or Radau) in solve_ivp."
    assert "method='RK45'" not in content and 'method="RK45"' not in content, "The script should no longer use the 'RK45' method."

    # 2. Parallelization
    assert "multiprocessing.Pool" in content or "Pool(" in content, "The script does not appear to use multiprocessing.Pool."

    # 3. Analytical Validation
    assert "assert" in content, "The script is missing an assert statement for validation."
    assert "1e-5" in content or "0.00001" in content, "The script is missing the 1e-5 tolerance check in the assert statement."