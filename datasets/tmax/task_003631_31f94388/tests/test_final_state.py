# test_final_state.py

import os
import json
import math
import random
import pytest

RESULTS_FILE = "/home/user/results.txt"
ANALYSIS_FILE = "/home/user/analysis.json"

def test_results_file_exists_and_valid():
    assert os.path.isfile(RESULTS_FILE), f"Results file missing: {RESULTS_FILE}"

    with open(RESULTS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1000, f"Expected exactly 1000 results, found {len(lines)}"

    try:
        data = [float(x) for x in lines]
    except ValueError:
        pytest.fail("Not all lines in results.txt are valid floating-point numbers.")

def test_analysis_json_exists_and_valid():
    assert os.path.isfile(ANALYSIS_FILE), f"Analysis JSON missing: {ANALYSIS_FILE}"

    with open(ANALYSIS_FILE, "r") as f:
        try:
            ans = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("analysis.json is not a valid JSON file.")

    required_keys = {"robust_mean", "ci_lower", "ci_upper", "kde_at_mean"}
    for key in required_keys:
        assert key in ans, f"Missing key '{key}' in analysis.json"
        assert isinstance(ans[key], (int, float)), f"Value for '{key}' must be a number"

def test_analysis_values():
    if not os.path.isfile(RESULTS_FILE) or not os.path.isfile(ANALYSIS_FILE):
        pytest.skip("Missing required files.")

    with open(RESULTS_FILE, "r") as f:
        data = [float(line.strip()) for line in f if line.strip()]

    with open(ANALYSIS_FILE, "r") as f:
        ans = json.load(f)

    # 1. Robust Mean via Bisection
    def f_mu(mu):
        return sum(math.tanh(x - mu) for x in data)

    low, high = min(data), max(data)
    for _ in range(100):
        mid = (low + high) / 2.0
        val = f_mu(mid)
        if abs(val) < 1e-9:
            break
        if val > 0:
            low = mid
        else:
            high = mid

    true_robust_mean = (low + high) / 2.0

    assert abs(ans['robust_mean'] - true_robust_mean) < 1e-4, \
        f"robust_mean is {ans['robust_mean']}, expected ~{true_robust_mean}"

    # 2. KDE at Robust Mean
    h = 0.01
    N = len(data)
    kde_sum = 0.0
    for x in data:
        u = (x - true_robust_mean) / h
        kde_sum += math.exp(-0.5 * u**2)
    true_kde = kde_sum / (N * h * math.sqrt(2 * math.pi))

    assert abs(ans['kde_at_mean'] - true_kde) < 1e-2, \
        f"kde_at_mean is {ans['kde_at_mean']}, expected ~{true_kde}"

    # 3. Bootstrap CI (Approximation check)
    # Using normal approximation of the sample mean to check bounds realistically
    # since seed varies and we want a robust test.
    sample_mean = sum(data) / N
    variance = sum((x - sample_mean)**2 for x in data) / (N - 1)
    std_err = math.sqrt(variance / N)

    # 95% CI is roughly mean +/- 1.96 * std_err
    approx_lower = sample_mean - 1.96 * std_err
    approx_upper = sample_mean + 1.96 * std_err

    # We use a loose tolerance (3%) because bootstrap vs normal approx can differ slightly
    assert approx_lower * 0.97 <= ans['ci_lower'] <= approx_lower * 1.03, \
        f"ci_lower {ans['ci_lower']} is out of expected probabilistic range around {approx_lower}"

    assert approx_upper * 0.97 <= ans['ci_upper'] <= approx_upper * 1.03, \
        f"ci_upper {ans['ci_upper']} is out of expected probabilistic range around {approx_upper}"