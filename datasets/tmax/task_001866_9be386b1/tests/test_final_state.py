# test_final_state.py

import os
import subprocess

def test_script_exists():
    """Ensure the student created the script."""
    script_path = "/home/user/analyze_covariances.py"
    assert os.path.isfile(script_path), f"Student script {script_path} does not exist."

def test_results_file_content():
    """Compute the expected output and verify results.txt matches exactly."""
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    # Compute expected output using the container's installed libraries
    # to avoid importing third-party libraries directly in the pytest suite.
    truth_script = """
import numpy as np
from scipy.stats import gaussian_kde
import math

np.random.seed(42)
A = np.random.randn(2500, 5, 5)
M = A @ A.transpose(0, 2, 1) + 0.01 * np.eye(5)

L = np.linalg.cholesky(M)
s = np.linalg.svd(L, compute_uv=False)
max_s = s[:, 0]

sorted_max_s = sorted(max_s.tolist())
exact_sum = math.fsum(sorted_max_s)
stable_mean = exact_sum / 2500.0

kde = gaussian_kde(max_s)
kde_val = kde(6.0)[0]

print(f"Stable Mean: {stable_mean:.6f}")
print(f"KDE at 6.0: {kde_val:.6f}")
"""
    try:
        expected_output = subprocess.check_output(
            ["python3", "-c", truth_script],
            text=True,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to compute expected truth values. Error:\n{e.output}"

    with open(results_path, "r") as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), (
        f"Contents of {results_path} do not match the expected output.\n"
        f"Expected:\n{expected_output.strip()}\n"
        f"Actual:\n{actual_output.strip()}"
    )