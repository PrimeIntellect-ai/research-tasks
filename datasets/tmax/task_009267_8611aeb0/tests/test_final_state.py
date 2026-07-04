# test_final_state.py
import json
import os
import math

def test_mcmc_sampler_fixed():
    path = '/home/user/mcmc_sampler.py'
    assert os.path.exists(path), f"{path} is missing."
    with open(path, 'r') as f:
        content = f.read()

    # Check that pinv is used with the correct rcond
    assert 'np.linalg.pinv' in content, "mcmc_sampler.py does not use np.linalg.pinv."
    assert '1e-5' in content, "mcmc_sampler.py does not use rcond=1e-5."

def test_analysis_script_exists():
    path = '/home/user/analysis.py'
    assert os.path.exists(path), f"{path} is missing."

def test_results_json_values():
    path = '/home/user/results.json'
    assert os.path.exists(path), f"{path} is missing."

    with open(path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    # Expected values derived from the deterministic setup
    expected = {
        "dim_0": {"mean": -0.0150, "ci_lower": -0.0469, "ci_upper": 0.0163},
        "dim_1": {"mean": 0.0468, "ci_lower": 0.0125, "ci_upper": 0.0822},
        "dim_2": {"mean": -0.0076, "ci_lower": -0.0359, "ci_upper": 0.0211}
    }

    for dim in expected:
        assert dim in results, f"Missing key '{dim}' in results.json."
        for metric in expected[dim]:
            assert metric in results[dim], f"Missing metric '{metric}' in {dim}."

            actual_val = results[dim][metric]
            expected_val = expected[dim][metric]

            assert isinstance(actual_val, (int, float)), f"Value for {dim}.{metric} is not a number."
            assert math.isclose(actual_val, expected_val, abs_tol=1e-3), \
                f"Expected {dim}.{metric} to be near {expected_val}, but got {actual_val}."