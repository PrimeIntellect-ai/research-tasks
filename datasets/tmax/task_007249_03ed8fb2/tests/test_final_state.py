# test_final_state.py

import json
import os
import math

def test_results_json_exists_and_correct():
    results_file = "/home/user/results.json"
    assert os.path.exists(results_file), f"The file {results_file} does not exist."
    assert os.path.isfile(results_file), f"The path {results_file} is not a file."

    with open(results_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {results_file} does not contain valid JSON."

    assert "covariance" in data, "The key 'covariance' is missing from the JSON results."
    assert "posterior_mean_beta" in data, "The key 'posterior_mean_beta' is missing from the JSON results."

    try:
        cov = float(data["covariance"])
        pmb = float(data["posterior_mean_beta"])
    except ValueError:
        assert False, "The values in the JSON results could not be parsed as floats."

    # Using an absolute tolerance of 1e-3 to account for rounding to 4 decimal places
    assert math.isclose(cov, 10.0, abs_tol=1e-3), f"Expected covariance to be approximately 10.0, but got {cov}."
    assert math.isclose(pmb, 12.8571, abs_tol=1e-3), f"Expected posterior_mean_beta to be approximately 12.8571, but got {pmb}."