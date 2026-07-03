# test_final_state.py

import os
import json
import math
import pytest

def test_results_json_exists():
    assert os.path.exists('/home/user/results.json'), "/home/user/results.json not found"

def test_posterior_png_exists():
    assert os.path.exists('/home/user/posterior.png'), "/home/user/posterior.png not found"
    assert os.path.getsize('/home/user/posterior.png') > 0, "/home/user/posterior.png is empty"

def test_results_values():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"{results_path} not found"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    required_keys = ["analytical_mean", "analytical_var", "mcmc_mean", "mcmc_var"]
    for key in required_keys:
        assert key in results, f"Key '{key}' missing from results.json"

    expected_mean = 17 / 24
    expected_var = 119 / 14400

    assert math.isclose(results['analytical_mean'], expected_mean, abs_tol=1e-4), \
        f"Analytical mean incorrect: expected ~{expected_mean}, got {results['analytical_mean']}"

    assert math.isclose(results['analytical_var'], expected_var, abs_tol=1e-4), \
        f"Analytical variance incorrect: expected ~{expected_var}, got {results['analytical_var']}"

    assert math.isclose(results['mcmc_mean'], expected_mean, abs_tol=0.01), \
        f"MCMC mean out of bounds: expected ~{expected_mean}, got {results['mcmc_mean']}"

    assert math.isclose(results['mcmc_var'], expected_var, abs_tol=0.002), \
        f"MCMC variance out of bounds: expected ~{expected_var}, got {results['mcmc_var']}"