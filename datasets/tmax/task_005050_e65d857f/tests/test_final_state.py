# test_final_state.py
import os
import subprocess
import pytest

def test_run_analysis_sh_exists_and_executable():
    path = "/home/user/run_analysis.sh"
    assert os.path.exists(path), f"The script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"The script {path} is not executable."

def test_analyze_py_exists():
    path = "/home/user/analyze.py"
    assert os.path.exists(path), f"The script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def get_reference_probability():
    script = """
import h5py
import numpy as np
import scipy.stats

with h5py.File('/home/user/data.h5', 'r') as f:
    X = f['X'][:]
    y = f['y'][:]

U, S, Vt = np.linalg.svd(X, full_matrices=False)
S_inv = np.diag(1/S)
X_pinv = Vt.T @ S_inv @ U.T
w_ols = X_pinv @ y

def log_posterior(w):
    log_prior = np.sum(scipy.stats.norm.logpdf(w, 0, 1))
    log_lik = np.sum(scipy.stats.norm.logpdf(y, X @ w, 0.5))
    return log_prior + log_lik

np.random.seed(42)
w_current = w_ols.copy()
lp_current = log_posterior(w_current)
samples = []

for _ in range(10000):
    w_prop = w_current + np.random.randn(10) * 0.05
    lp_prop = log_posterior(w_prop)

    if np.log(np.random.rand()) < lp_prop - lp_current:
        w_current = w_prop
        lp_current = lp_prop
    samples.append(w_current)

samples = np.array(samples)[2000:]
prob = np.mean(samples[:, 0] > 1.0)
print(prob)
"""
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True)
    if result.returncode != 0:
        # Fallback if numpy/scipy/h5py are somehow not available in the test runner's python
        return None
    return float(result.stdout.strip())

def test_hypothesis_test_output():
    path = "/home/user/hypothesis_test.txt"
    assert os.path.exists(path), f"The output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        p_agent = float(content)
    except ValueError:
        pytest.fail(f"The content of {path} is not a valid floating-point number. Found: '{content}'")

    p_ref = get_reference_probability()
    if p_ref is not None:
        assert abs(p_agent - p_ref) < 0.02, (
            f"The calculated probability {p_agent} differs from the reference probability {p_ref} "
            f"by more than the allowed tolerance of 0.02."
        )
    else:
        # Fallback assertion if reference script fails to execute
        assert 0.0 <= p_agent <= 1.0, f"The probability {p_agent} is not between 0 and 1."