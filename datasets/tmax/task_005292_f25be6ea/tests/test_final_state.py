# test_final_state.py

import os
import subprocess
import sys
import math

def get_expected_values():
    """
    Dynamically compute the expected coefficients and MSE by calling out to
    Python with numpy/h5py, since the test itself must only use the stdlib.
    """
    code = """
import h5py
import numpy as np
with h5py.File('/home/user/signal.h5', 'r') as f:
    t = f['t'][:]
    signal = f['signal'][:]
coeffs_fit = np.polyfit(t, signal, 12)
mse = np.mean((np.polyval(coeffs_fit, t) - signal)**2)
for c in coeffs_fit:
    print(f"{c:.8f}")
print(f"{mse:.8f}")
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to compute expected values: {result.stderr}")

    lines = result.stdout.strip().split('\n')
    expected_coeffs = lines[:13]
    expected_mse = lines[13]
    return expected_coeffs, expected_mse

def test_stable_fit_script_exists():
    """Check that the stable_fit.py script exists."""
    script_path = '/home/user/stable_fit.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_coefficients_file():
    """Check that coeffs.txt contains the correct polynomial coefficients."""
    coeffs_path = '/home/user/coeffs.txt'
    assert os.path.isfile(coeffs_path), f"The file {coeffs_path} is missing."

    expected_coeffs, _ = get_expected_values()

    with open(coeffs_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 13, f"Expected 13 coefficients, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_coeffs)):
        # Allow small floating point differences in the string representation if they are very close
        assert abs(float(actual) - float(expected)) < 1e-6, \
            f"Coefficient at index {i} (degree {12-i}) does not match. Expected {expected}, got {actual}."

def test_mse_file():
    """Check that mse.txt contains the correct Mean Squared Error."""
    mse_path = '/home/user/mse.txt'
    assert os.path.isfile(mse_path), f"The file {mse_path} is missing."

    _, expected_mse = get_expected_values()

    with open(mse_path, 'r') as f:
        actual_mse_str = f.read().strip()

    assert actual_mse_str, "The mse.txt file is empty."

    actual_mse = float(actual_mse_str)
    expected_mse_val = float(expected_mse)

    assert abs(actual_mse - expected_mse_val) < 1e-6, \
        f"MSE does not match. Expected {expected_mse}, got {actual_mse_str}."