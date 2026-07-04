# test_final_state.py
import os
import json
import subprocess
import math

def test_venv_exists():
    venv_python = "/home/user/venv/bin/python"
    assert os.path.exists(venv_python), f"Virtual environment python not found at {venv_python}"

def test_plot_exists():
    plot_path = "/home/user/fit_plot.png"
    assert os.path.exists(plot_path), f"Plot {plot_path} does not exist"
    assert os.path.getsize(plot_path) > 0, f"Plot {plot_path} is empty"

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"{results_path} does not exist"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{results_path} is not valid JSON"

    expected_keys = ["bootstrap_ci_lower", "bootstrap_ci_upper", "optimized_a", "optimized_b"]
    for key in expected_keys:
        assert key in results, f"Key '{key}' missing in results.json"
        assert isinstance(results[key], (float, int)), f"Value for '{key}' is not a number"

    # Compute expected values using the venv's python to ensure we use the same libraries
    script = """
import numpy as np
import pandas as pd
from scipy.stats import bootstrap
from scipy.optimize import minimize
import json

df = pd.read_csv('/home/user/discrepancies.csv')
N = df['N'].values
error = df['error'].values

res = bootstrap((error,), np.mean, method='percentile', n_resamples=10000, random_state=42)
ci_lower = float(res.confidence_interval.low)
ci_upper = float(res.confidence_interval.high)

def mse(params):
    a, b = params
    pred = a * (N ** b)
    return np.mean((error - pred) ** 2)

opt = minimize(mse, [1e-16, 1.0], method='Nelder-Mead')
opt_a, opt_b = float(opt.x[0]), float(opt.x[1])

print(json.dumps({
  "bootstrap_ci_lower": ci_lower,
  "bootstrap_ci_upper": ci_upper,
  "optimized_a": opt_a,
  "optimized_b": opt_b
}))
"""
    try:
        out = subprocess.check_output(
            ["/home/user/venv/bin/python", "-c", script], 
            text=True, 
            stderr=subprocess.STDOUT
        )
        expected = json.loads(out)
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to run verification script using venv python. Did you install numpy, pandas, and scipy? Output: {e.output}"
    except Exception as e:
        assert False, f"Failed to compute expected values: {e}"

    for key in expected_keys:
        assert math.isclose(results[key], expected[key], rel_tol=1e-4), \
            f"Value for {key} does not match expected. Got {results[key]}, expected {expected[key]}"