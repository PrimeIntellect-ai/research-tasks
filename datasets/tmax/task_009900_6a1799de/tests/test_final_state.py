# test_final_state.py

import os
import math
import random
import pytest

def solve_ode_fixed(theta, t_max):
    dt = 0.1
    t = 0.0
    x = 10.0
    res = {0.0: x}
    while t < t_max:
        x = x - theta * x * dt
        t += dt
        for target in range(1, int(t_max) + 1):
            if abs(t - target) < dt/2:
                res[float(target)] = x
    return res

def log_likelihood_fixed(theta, data):
    if theta <= 0: return -1e9
    preds = solve_ode_fixed(theta, 5.0)
    ll = 0.0
    for row in data:
        t = float(row['t'])
        obs = float(row['x'])
        pred = preds.get(t, obs)
        ll -= 0.5 * ((obs - pred)/0.5)**2
    return ll

def get_expected_mean():
    random.seed(42)
    true_theta = 0.5
    t_vals = [0, 1, 2, 3, 4, 5]
    data = [{"t": t, "x": 10.0 * math.exp(-true_theta * t)} for t in t_vals]

    current_theta = 0.2
    current_ll = log_likelihood_fixed(current_theta, data)
    samples = []

    for _ in range(2500):
        prop_theta = current_theta + random.gauss(0, 0.05)
        prop_ll = log_likelihood_fixed(prop_theta, data)

        if math.log(random.random()) < prop_ll - current_ll:
            current_theta = prop_theta
            current_ll = prop_ll

        samples.append(current_theta)

    burn_in = samples[500:]
    return round(sum(burn_in) / len(burn_in), 3)

def test_mcmc_ode_fixed():
    path = "/home/user/mcmc_ode.py"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read()

    # Check that dt was changed to 0.1
    assert "0.1" in content, "The step size dt does not appear to be changed to 0.1 in mcmc_ode.py"
    assert "dt = 2.0" not in content, "The old step size dt = 2.0 is still present in mcmc_ode.py"

def test_posterior_mean():
    path = "/home/user/posterior_mean.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_mean = get_expected_mean()
    assert str(expected_mean) in content, f"Expected posterior mean {expected_mean} not found in {path}. Found: {content}"

def test_trace_plot_exists():
    path = "/home/user/trace_plot.png"
    assert os.path.isfile(path), f"Missing file: {path}"
    assert os.path.getsize(path) > 0, f"File {path} is empty"

def test_pipeline_script():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Missing file: {path}"
    assert os.access(path, os.X_OK), f"File {path} is not executable"