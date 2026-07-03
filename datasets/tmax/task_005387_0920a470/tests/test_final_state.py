# test_final_state.py
import os
import subprocess
import pytest

def test_executable_exists():
    exe_path = "/home/user/fit_data"
    assert os.path.exists(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_coeffs_txt_exists_and_format():
    coeffs_path = "/home/user/coeffs.txt"
    assert os.path.exists(coeffs_path), f"{coeffs_path} is missing."

    with open(coeffs_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 13, f"Expected exactly 13 lines in {coeffs_path}, found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Line {i+1} in {coeffs_path} is not a valid floating-point number: '{line}'")

def test_coeffs_correctness():
    # We use the container's Python environment (which has numpy and h5py installed)
    # to read the HDF5 file and verify the math, as we are restricted to stdlib in the test suite itself.
    verify_script = """
import sys
import numpy as np
import h5py

try:
    with h5py.File('/home/user/data.h5', 'r') as f:
        x = f['x'][:]
        y = f['y'][:]

    X = np.vander(x, 13, increasing=True)
    A = X.T @ X
    B = X.T @ y
    A += 0.001 * np.eye(13)
    coeffs_ridge = np.linalg.solve(A, B)

    loaded_coeffs = np.loadtxt('/home/user/coeffs.txt')

    if len(loaded_coeffs) != 13:
        print(f"Expected 13 coefficients, got {len(loaded_coeffs)}")
        sys.exit(1)

    if not np.allclose(loaded_coeffs, coeffs_ridge, atol=1e-4):
        print("Coefficients do not match expected Ridge Regression values within tolerance.")
        sys.exit(1)

except Exception as e:
    print(f"Error during verification: {e}")
    sys.exit(2)
"""
    result = subprocess.run(["python3", "-c", verify_script], capture_output=True, text=True)

    if result.returncode == 2:
        pytest.fail(f"Verification script encountered an error:\n{result.stdout}\n{result.stderr}")
    elif result.returncode == 1:
        pytest.fail(f"Math verification failed:\n{result.stdout}")

    assert result.returncode == 0, "Unknown error occurred during coefficient verification."