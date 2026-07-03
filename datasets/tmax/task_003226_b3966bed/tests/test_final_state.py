# test_final_state.py
import os
import subprocess
import sys
import pytest

def get_expected_mse():
    script = """
import numpy as np
V_noisy = np.loadtxt('/home/user/noisy_data.csv', delimiter=',')
V_ref = np.loadtxt('/home/user/reference.csv', delimiter=',')
np.random.seed(0)
n, m = V_noisy.shape
k = 5
W = np.random.rand(n, k)
H = np.random.rand(k, m)
for _ in range(1000):
    H = H * (W.T @ V_noisy) / (W.T @ W @ H + 1e-9)
    W = W * (V_noisy @ H.T) / (W @ H @ H.T + 1e-9)
V_rec = W @ H
print(f"{np.mean((V_rec - V_ref)**2):.4f}")
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Failed to compute expected MSE using numpy: {result.stderr}")
    return result.stdout.strip()

def test_mse_file_exists():
    path = "/home/user/mse.txt"
    assert os.path.isfile(path), f"Missing MSE output file: {path}"

def test_mse_value_correct():
    path = "/home/user/mse.txt"
    assert os.path.isfile(path), "Missing MSE output file."

    with open(path, 'r') as f:
        actual_val = f.read().strip()

    expected_val = get_expected_mse()

    assert actual_val == expected_val, f"MSE value in {path} is incorrect. Expected {expected_val}, got {actual_val}"

def test_mf_script_modifications():
    path = "/home/user/mf.py"
    assert os.path.isfile(path), "Missing NMF script."

    with open(path, 'r') as f:
        content = f.read()

    assert "1e-9" in content, "The script /home/user/mf.py does not contain the epsilon '1e-9' to prevent division by zero."