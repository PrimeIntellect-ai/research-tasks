# test_final_state.py

import os
import json
import math

def test_diffusion_metrics_exists():
    assert os.path.isfile("/home/user/diffusion_metrics.json"), "The file /home/user/diffusion_metrics.json does not exist."

def test_diffusion_metrics_format():
    with open("/home/user/diffusion_metrics.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "The file /home/user/diffusion_metrics.json is not valid JSON."

    assert "kde_values" in data, "Missing 'kde_values' in JSON."
    assert "analytical_values" in data, "Missing 'analytical_values' in JSON."
    assert "max_diff" in data, "Missing 'max_diff' in JSON."

    assert isinstance(data["kde_values"], list), "'kde_values' should be a list."
    assert len(data["kde_values"]) == 5, "'kde_values' should have exactly 5 elements."
    assert all(isinstance(x, (int, float)) for x in data["kde_values"]), "All 'kde_values' must be numbers."

    assert isinstance(data["analytical_values"], list), "'analytical_values' should be a list."
    assert len(data["analytical_values"]) == 5, "'analytical_values' should have exactly 5 elements."
    assert all(isinstance(x, (int, float)) for x in data["analytical_values"]), "All 'analytical_values' must be numbers."

    assert isinstance(data["max_diff"], (int, float)), "'max_diff' should be a number."

def test_diffusion_metrics_values():
    with open("/home/user/diffusion_metrics.json", "r") as f:
        data = json.load(f)

    kde_vals = data["kde_values"]
    ana_vals = data["analytical_values"]
    max_diff = data["max_diff"]

    # The analytical solution for N=100 steps of uniform(-sqrt(3), sqrt(3)) 
    # is very close to a Gaussian with mean 0 and variance 100.
    # p(x) ~ (1 / sqrt(200 * pi)) * exp(-x^2 / 200)
    # At x = 0: ~0.03989
    # At x = +/- 5: ~0.03520
    # At x = +/- 10: ~0.02419

    expected_approx = [0.02419, 0.03520, 0.03989, 0.03520, 0.02419]

    for i, (val, expected) in enumerate(zip(ana_vals, expected_approx)):
        assert math.isclose(val, expected, abs_tol=1e-2), f"Analytical value at index {i} ({val}) is not close to expected ~{expected}."

    # Check if max_diff is correctly computed
    computed_max_diff = max(abs(k - a) for k, a in zip(kde_vals, ana_vals))
    assert math.isclose(max_diff, computed_max_diff, abs_tol=1e-5), f"max_diff {max_diff} does not match computed max absolute difference {computed_max_diff}."