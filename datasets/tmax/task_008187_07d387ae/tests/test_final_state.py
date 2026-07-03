# test_final_state.py

import json
import os

def test_results_json_exists():
    path = '/home/user/results.json'
    assert os.path.exists(path), f"File {path} does not exist. The notebook may not have been executed or saved the output correctly."
    assert os.path.isfile(path), f"Expected {path} to be a file."

def test_results_json_format_and_invariants():
    path = '/home/user/results.json'
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not a valid JSON file."

    expected_keys = {
        "integral_0_10",
        "derivative_at_5",
        "bootstrap_ci_lower",
        "bootstrap_ci_upper",
        "pc1_variance_explained",
        "first_row_projected"
    }

    actual_keys = set(data.keys())
    missing_keys = expected_keys - actual_keys
    extra_keys = actual_keys - expected_keys

    assert not missing_keys, f"Missing expected keys in results.json: {missing_keys}"
    assert not extra_keys, f"Unexpected extra keys in results.json: {extra_keys}"

    # Type checking
    assert isinstance(data["integral_0_10"], (int, float)), "integral_0_10 must be a number"
    assert isinstance(data["derivative_at_5"], (int, float)), "derivative_at_5 must be a number"
    assert isinstance(data["bootstrap_ci_lower"], (int, float)), "bootstrap_ci_lower must be a number"
    assert isinstance(data["bootstrap_ci_upper"], (int, float)), "bootstrap_ci_upper must be a number"
    assert isinstance(data["pc1_variance_explained"], (int, float)), "pc1_variance_explained must be a number"

    assert isinstance(data["first_row_projected"], list), "first_row_projected must be a list"
    assert len(data["first_row_projected"]) == 2, "first_row_projected must contain exactly 2 elements"
    assert isinstance(data["first_row_projected"][0], (int, float)), "first_row_projected[0] must be a number"
    assert isinstance(data["first_row_projected"][1], (int, float)), "first_row_projected[1] must be a number"

    # Logical invariants
    assert 0.0 <= data["pc1_variance_explained"] <= 1.0, "pc1_variance_explained must be a ratio between 0.0 and 1.0"
    assert data["bootstrap_ci_lower"] <= data["bootstrap_ci_upper"], "bootstrap_ci_lower must be less than or equal to bootstrap_ci_upper"