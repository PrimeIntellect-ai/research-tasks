# test_final_state.py

import os
import json
import math
import pytest

FINAL_JSON_PATH = "/home/user/final_analysis.json"

def test_final_analysis_file_exists():
    """Verify that the final JSON output file exists."""
    assert os.path.exists(FINAL_JSON_PATH), f"The file {FINAL_JSON_PATH} does not exist."
    assert os.path.isfile(FINAL_JSON_PATH), f"The path {FINAL_JSON_PATH} is not a file."

def test_final_analysis_json_structure():
    """Verify that the JSON file contains the correct keys and data types."""
    with open(FINAL_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Could not parse {FINAL_JSON_PATH} as JSON: {e}")

    assert isinstance(data, dict), "The JSON root must be an object (dictionary)."

    expected_keys = {"mu_estimated", "analytical_prob", "mc_transmitted_count"}
    actual_keys = set(data.keys())

    missing_keys = expected_keys - actual_keys
    assert not missing_keys, f"Missing expected keys in JSON: {missing_keys}"

    assert isinstance(data["mu_estimated"], (int, float)), "mu_estimated must be a number."
    assert isinstance(data["analytical_prob"], (int, float)), "analytical_prob must be a number."
    assert isinstance(data["mc_transmitted_count"], int), "mc_transmitted_count must be an integer."

def test_final_analysis_values():
    """Verify that the estimated and calculated values are within acceptable bounds."""
    with open(FINAL_JSON_PATH, 'r') as f:
        data = json.load(f)

    mu = data["mu_estimated"]
    prob = data["analytical_prob"]
    mc_count = data["mc_transmitted_count"]

    # Check mu_estimated
    expected_mu = 0.145
    assert math.isclose(mu, expected_mu, rel_tol=0.01), (
        f"Expected mu_estimated to be close to {expected_mu}, but got {mu}."
    )

    # Check analytical_prob
    expected_prob = 0.1136
    assert math.isclose(prob, expected_prob, rel_tol=0.01), (
        f"Expected analytical_prob to be close to {expected_prob}, but got {prob}."
    )

    # Check mc_transmitted_count
    assert 112000 <= mc_count <= 115000, (
        f"Expected mc_transmitted_count to be between 112000 and 115000, but got {mc_count}."
    )