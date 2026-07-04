# test_final_state.py
import os
import json
import numpy as np
import pytest

def get_expected_results():
    data_a = np.loadtxt('/home/user/latency_a.txt')
    data_b = np.loadtxt('/home/user/latency_b.txt')

    # 1. Bootstrap
    np.random.seed(42)
    diffs = []
    n_a = len(data_a)
    n_b = len(data_b)
    for _ in range(10000):
        samp_a = np.random.choice(data_a, n_a, replace=True)
        samp_b = np.random.choice(data_b, n_b, replace=True)
        diffs.append(np.median(samp_b) - np.median(samp_a))

    ci_lower = np.percentile(diffs, 2.5)
    ci_upper = np.percentile(diffs, 97.5)

    # 2. MCMC
    def log_likelihood(data, mu):
        if mu <= 0 or mu > 200:
            return -np.inf
        return -len(data)*np.log(mu) - np.sum(data)/mu

    def run_mcmc(data, seed):
        np.random.seed(seed)
        mu_current = 50.0
        ll_current = log_likelihood(data, mu_current)
        samples = []

        for i in range(10000):
            mu_prop = np.random.normal(mu_current, 2.0)
            ll_prop = log_likelihood(data, mu_prop)

            if ll_prop > -np.inf:
                ratio = ll_prop - ll_current
                if np.log(np.random.uniform(0, 1)) < ratio:
                    mu_current = mu_prop
                    ll_current = ll_prop

            samples.append(mu_current)

        return np.mean(samples[2000:])

    mcmc_a = run_mcmc(data_a, 100)
    mcmc_b = run_mcmc(data_b, 200)

    return {
        "bootstrap_ci_lower": float(ci_lower),
        "bootstrap_ci_upper": float(ci_upper),
        "mcmc_mu_a": float(mcmc_a),
        "mcmc_mu_b": float(mcmc_b)
    }

def test_notebook_exists():
    path = "/home/user/profile_analysis.ipynb"
    assert os.path.isfile(path), f"Notebook file {path} is missing."

def test_plot_exists():
    path = "/home/user/posterior_plot.png"
    assert os.path.isfile(path), f"Plot file {path} is missing."

def test_results_json():
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"Results file {path} is missing."

    with open(path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected = get_expected_results()

    assert "bootstrap_ci_lower" in results, "Missing key 'bootstrap_ci_lower' in results.json"
    assert "bootstrap_ci_upper" in results, "Missing key 'bootstrap_ci_upper' in results.json"
    assert "mcmc_mu_a" in results, "Missing key 'mcmc_mu_a' in results.json"
    assert "mcmc_mu_b" in results, "Missing key 'mcmc_mu_b' in results.json"

    assert abs(results["bootstrap_ci_lower"] - expected["bootstrap_ci_lower"]) <= 0.05, \
        f"bootstrap_ci_lower is incorrect. Expected ~{expected['bootstrap_ci_lower']}, got {results['bootstrap_ci_lower']}"

    assert abs(results["bootstrap_ci_upper"] - expected["bootstrap_ci_upper"]) <= 0.05, \
        f"bootstrap_ci_upper is incorrect. Expected ~{expected['bootstrap_ci_upper']}, got {results['bootstrap_ci_upper']}"

    assert abs(results["mcmc_mu_a"] - expected["mcmc_mu_a"]) <= 0.1, \
        f"mcmc_mu_a is incorrect. Expected ~{expected['mcmc_mu_a']}, got {results['mcmc_mu_a']}"

    assert abs(results["mcmc_mu_b"] - expected["mcmc_mu_b"]) <= 0.1, \
        f"mcmc_mu_b is incorrect. Expected ~{expected['mcmc_mu_b']}, got {results['mcmc_mu_b']}"