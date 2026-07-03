# test_final_state.py
import os
import re
import math

def test_mcmc_files_exist():
    assert os.path.exists("/home/user/mcmc.cpp"), "/home/user/mcmc.cpp does not exist."
    assert os.path.exists("/home/user/mcmc"), "/home/user/mcmc executable does not exist."
    assert os.access("/home/user/mcmc", os.X_OK), "/home/user/mcmc is not executable."

def test_analysis_log():
    log_path = "/home/user/analysis.log"
    assert os.path.exists(log_path), f"File {log_path} not found."

    with open(log_path, 'r') as f:
        content = f.read()

    mean_match = re.search(r"Posterior Mean:\s*(-?\d+\.\d+)", content)
    ll_h0_match = re.search(r"LL H0:\s*(-?\d+\.\d+)", content)
    ll_h1_match = re.search(r"LL H1:\s*(-?\d+\.\d+)", content)

    assert mean_match is not None, "Could not parse 'Posterior Mean: X.XX' from analysis.log"
    assert ll_h0_match is not None, "Could not parse 'LL H0: X.XX' from analysis.log"
    assert ll_h1_match is not None, "Could not parse 'LL H1: X.XX' from analysis.log"

    mean_val = float(mean_match.group(1))
    ll_h0 = float(ll_h0_match.group(1))
    ll_h1 = float(ll_h1_match.group(1))

    # Read counts
    counts_path = "/home/user/counts.txt"
    assert os.path.exists(counts_path), f"File {counts_path} missing."
    with open(counts_path, 'r') as f:
        counts = [int(x) for x in f.read().split()]

    # Recompute log-likelihoods
    def log_likelihood(lam, data):
        ll = 0.0
        for k in data:
            ll += k * math.log(lam) - lam - math.log(math.factorial(k))
        return ll

    expected_ll_h0 = log_likelihood(3.0, counts)
    expected_ll_h1 = log_likelihood(mean_val, counts)

    # Assertions
    assert 4.70 <= mean_val <= 4.80, f"Posterior Mean {mean_val} is out of expected bounds (4.70 - 4.80)."
    assert math.isclose(ll_h0, expected_ll_h0, abs_tol=0.1), f"LL H0 {ll_h0} does not match expected {expected_ll_h0:.2f}."
    assert math.isclose(ll_h1, expected_ll_h1, abs_tol=0.1), f"LL H1 {ll_h1} does not match expected {expected_ll_h1:.2f}."