# test_final_state.py

import os
import subprocess
import pytest

def test_derivatives_txt_exists_and_correct():
    obs_path = "/home/user/observations.txt"
    deriv_path = "/home/user/derivatives.txt"

    assert os.path.isfile(deriv_path), f"Missing file: {deriv_path}"

    with open(obs_path, "r") as f:
        data = [float(x) for x in f.read().split()]

    assert len(data) == 500, "observations.txt does not contain 500 floats."

    # Compute expected derivatives in pure Python
    expected_dy_dt = []
    for i in range(100):
        row = data[i*5:(i+1)*5]
        y = sum(row) / 5.0
        dt = 0.001
        for _ in range(1000):
            y += dt * (-y * y)
        expected_dy_dt.append(-y * y)

    with open(deriv_path, "r") as f:
        actual_lines = f.read().strip().split()

    assert len(actual_lines) == 100, f"Expected 100 lines in {deriv_path}, found {len(actual_lines)}"

    for i, (actual_str, expected) in enumerate(zip(actual_lines, expected_dy_dt)):
        try:
            actual = float(actual_str)
        except ValueError:
            pytest.fail(f"Line {i+1} in {deriv_path} is not a valid float: {actual_str}")

        assert abs(actual - expected) < 1e-4, f"Derivative mismatch at index {i}. Expected {expected}, got {actual}"

def test_calc_ci_py_exists():
    script_path = "/home/user/calc_ci.py"
    assert os.path.isfile(script_path), f"Missing Python script: {script_path}"

def test_ci_txt_exists_and_correct():
    ci_path = "/home/user/ci.txt"
    assert os.path.isfile(ci_path), f"Missing file: {ci_path}"

    # Use a subprocess to run numpy/scipy logic to get the exact expected CI string
    # This avoids importing third-party libraries directly into the test suite.
    canonical_script = """
import numpy as np
from scipy.stats import bootstrap

with open('/home/user/observations.txt', 'r') as f:
    data = np.array([float(x) for x in f.read().split()])

ic = data.reshape(100, 5).mean(axis=1)

dt = 0.001
y = ic.copy()
for _ in range(1000):
    y += dt * (-y*y)

dy_dt = -y*y

rng = np.random.default_rng(42)
res = bootstrap((dy_dt,), np.mean, confidence_level=0.95, n_resamples=9999, method='percentile', random_state=rng)

print(f"[{res.confidence_interval.low:.4f}, {res.confidence_interval.high:.4f}]")
"""
    result = subprocess.run(
        ['python3', '-c', canonical_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Failed to compute canonical CI: {result.stderr}"
    expected_ci = result.stdout.strip()

    with open(ci_path, "r") as f:
        actual_ci = f.read().strip()

    assert actual_ci == expected_ci, f"CI mismatch in {ci_path}. Expected '{expected_ci}', got '{actual_ci}'"