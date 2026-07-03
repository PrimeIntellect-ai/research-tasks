# test_final_state.py

import os
import json
import math

def test_analysis_results_exist_and_format():
    file_path = '/home/user/analysis_results.json'
    assert os.path.exists(file_path), f"The expected output file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a regular file."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} does not contain valid JSON."

    expected_keys = {
        "num_events",
        "integral_value",
        "gaussian_A",
        "gaussian_mu",
        "gaussian_sigma"
    }

    actual_keys = set(data.keys())
    assert actual_keys == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, but got {actual_keys}."

def test_analysis_results_values():
    file_path = '/home/user/analysis_results.json'
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Check types
    assert isinstance(data["num_events"], int), "num_events must be an integer."
    assert isinstance(data["integral_value"], (float, int)), "integral_value must be a float."
    assert isinstance(data["gaussian_A"], (float, int)), "gaussian_A must be a float."
    assert isinstance(data["gaussian_mu"], (float, int)), "gaussian_mu must be a float."
    assert isinstance(data["gaussian_sigma"], (float, int)), "gaussian_sigma must be a float."

    # Check values based on the deterministic seed used in setup
    assert data["num_events"] == 6, f"Expected num_events to be 6, got {data['num_events']}."

    # Tolerances are used to account for minor floating point differences across platforms
    assert math.isclose(data["integral_value"], 21741.05, abs_tol=0.05), \
        f"Expected integral_value to be approx 21741.05, got {data['integral_value']}."

    assert math.isclose(data["gaussian_A"], 5.215, abs_tol=0.01), \
        f"Expected gaussian_A to be approx 5.215, got {data['gaussian_A']}."

    assert math.isclose(data["gaussian_mu"], 230.137, abs_tol=0.01), \
        f"Expected gaussian_mu to be approx 230.137, got {data['gaussian_mu']}."

    assert math.isclose(data["gaussian_sigma"], 36.219, abs_tol=0.01), \
        f"Expected gaussian_sigma to be approx 36.219, got {data['gaussian_sigma']}."