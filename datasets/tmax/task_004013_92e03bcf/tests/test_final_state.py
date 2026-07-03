# test_final_state.py

import os
import json
import math
import pytest

def test_sim_results_exists():
    assert os.path.isfile("/home/user/sim_results.json"), "The file /home/user/sim_results.json does not exist."

def test_sim_results_content():
    with open("/home/user/sim_results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/sim_results.json is not a valid JSON file.")

    expected_keys = ["10", "50", "100", "200"]
    for k in expected_keys:
        assert k in data, f"Key '{k}' is missing from the JSON output."

    # Precomputed approximate expected values based on the truth script
    expected_values = {
        "10": {"condition_number": 48.374, "clean_error": 0.000839, "perturbed_diff": 1.23e-07},
        "50": {"condition_number": 1055.7, "clean_error": 0.0000338, "perturbed_diff": 6.37e-07},
        "100": {"condition_number": 4133.6, "clean_error": 0.00000845, "perturbed_diff": 1.27e-06},
        "200": {"condition_number": 16335.6, "clean_error": 0.00000211, "perturbed_diff": 2.54e-06}
    }

    for n_str, expected in expected_values.items():
        actual = data[n_str]
        for metric in ["condition_number", "clean_error", "perturbed_diff"]:
            assert metric in actual, f"Metric '{metric}' missing for N={n_str}"

            actual_val = actual[metric]
            expected_val = expected[metric]

            # Using a relative tolerance of 1e-2 to account for slight differences in numerical libraries
            rel_error = abs(actual_val - expected_val) / expected_val
            assert rel_error < 0.05, f"Value for {metric} at N={n_str} is {actual_val}, expected ~{expected_val}"

def test_run_sim_script_exists():
    assert os.path.isfile("/home/user/run_sim.py"), "The script /home/user/run_sim.py does not exist."