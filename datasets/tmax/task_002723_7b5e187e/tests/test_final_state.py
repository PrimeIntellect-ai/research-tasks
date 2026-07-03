# test_final_state.py
import os
import json
import pytest

RESULTS_PATH = "/home/user/results.json"

def test_results_file_exists():
    assert os.path.isfile(RESULTS_PATH), f"File {RESULTS_PATH} is missing. The Go program must generate this file."

def test_results_json_format():
    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not a valid JSON file.")

    expected_keys = {
        "ols_alpha",
        "ols_beta",
        "mcmc_alpha",
        "mcmc_beta",
        "accuracy_pass",
        "mcmc_time_seconds"
    }

    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"The JSON file is missing required keys: {missing_keys}"

def test_results_values():
    with open(RESULTS_PATH, 'r') as f:
        data = json.load(f)

    ols_alpha = data.get("ols_alpha")
    ols_beta = data.get("ols_beta")
    mcmc_alpha = data.get("mcmc_alpha")
    mcmc_beta = data.get("mcmc_beta")
    accuracy_pass = data.get("accuracy_pass")
    mcmc_time = data.get("mcmc_time_seconds")

    # Check types
    assert isinstance(ols_alpha, (int, float)), "ols_alpha must be a number"
    assert isinstance(ols_beta, (int, float)), "ols_beta must be a number"
    assert isinstance(mcmc_alpha, (int, float)), "mcmc_alpha must be a number"
    assert isinstance(mcmc_beta, (int, float)), "mcmc_beta must be a number"
    assert isinstance(accuracy_pass, bool), "accuracy_pass must be a boolean"
    assert isinstance(mcmc_time, (int, float)), "mcmc_time_seconds must be a number"

    # Check values
    assert abs(ols_alpha - 2.222) <= 0.05, f"ols_alpha is {ols_alpha}, expected ~2.222"
    assert abs(ols_beta - 1.332) <= 0.05, f"ols_beta is {ols_beta}, expected ~1.332"

    assert accuracy_pass is True, "accuracy_pass must be true"

    assert abs(mcmc_alpha - ols_alpha) <= 0.05, f"mcmc_alpha {mcmc_alpha} is not within 0.05 of ols_alpha {ols_alpha}"
    assert abs(mcmc_beta - ols_beta) <= 0.05, f"mcmc_beta {mcmc_beta} is not within 0.05 of ols_beta {ols_beta}"

    assert mcmc_time > 0, f"mcmc_time_seconds must be a positive float, got {mcmc_time}"