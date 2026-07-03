# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_output_file_exists():
    output_path = '/home/user/results/output.h5'
    assert os.path.exists(output_path), f"Expected output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

def test_output_contents_and_accuracy():
    output_path = '/home/user/results/output.h5'
    data_path = '/home/user/data/signal.h5'

    # We use a subprocess to run the verification using numpy/scipy/h5py, 
    # since these are required to be installed by the task, while keeping 
    # the pytest file restricted to the standard library.
    verification_script = f"""
import sys
try:
    import numpy as np
    import h5py
    from scipy.fft import fft, ifft, fftfreq
    from scipy.stats import norm
except ImportError as e:
    print(f"Missing required library: {{e}}", file=sys.stderr)
    sys.exit(1)

try:
    with h5py.File('{data_path}', 'r') as f:
        raw_signal = f['raw_signal'][:]
except Exception as e:
    print(f"Failed to read input data: {{e}}", file=sys.stderr)
    sys.exit(1)

# 1. Filtering (Expected)
n = len(raw_signal)
freqs = fftfreq(n, d=1/1000)
fft_vals = fft(raw_signal)
fft_vals[np.abs(freqs) > 50] = 0
expected_smoothed = np.real(ifft(fft_vals))

# 2. Density Estimation (Expected)
residual = raw_signal - expected_smoothed
expected_mu, expected_sigma = norm.fit(residual)

# 3. Stability Test (Expected)
np.random.seed(42)
perturbations = np.random.uniform(-1e-6, 1e-6, size=(50, n))
sigmas = []

for i in range(50):
    p_sig = raw_signal + perturbations[i]
    p_fft_vals = fft(p_sig)
    p_fft_vals[np.abs(freqs) > 50] = 0
    p_smoothed = np.real(ifft(p_fft_vals))
    p_residual = p_sig - p_smoothed
    _, p_sigma = norm.fit(p_residual)
    sigmas.append(p_sigma)

expected_stability_std = np.std(sigmas, ddof=0)

try:
    with h5py.File('{output_path}', 'r') as f:
        assert 'smoothed_signal' in f, "Dataset 'smoothed_signal' missing"
        assert 'noise_params' in f, "Dataset 'noise_params' missing"
        assert 'stability_std' in f, "Dataset 'stability_std' missing"

        out_smoothed = f['smoothed_signal'][:]
        out_noise = f['noise_params'][:]

        # Handle scalar dataset correctly
        out_std_ds = f['stability_std']
        out_std = out_std_ds[()] if out_std_ds.shape == () else out_std_ds[0]
except Exception as e:
    print(f"Failed to read output file or missing datasets: {{e}}", file=sys.stderr)
    sys.exit(1)

# Assertions
if not np.allclose(out_smoothed, expected_smoothed, atol=1e-5):
    print("smoothed_signal values do not match expected results within tolerance.", file=sys.stderr)
    sys.exit(1)

if not np.allclose(out_noise, [expected_mu, expected_sigma], atol=1e-5):
    print(f"noise_params mismatch. Expected {[expected_mu, expected_sigma]}, got {{out_noise}}", file=sys.stderr)
    sys.exit(1)

if not np.isclose(out_std, expected_stability_std, atol=1e-9):
    print(f"stability_std mismatch. Expected {{expected_stability_std}}, got {{out_std}}", file=sys.stderr)
    sys.exit(1)

print("SUCCESS")
"""

    result = subprocess.run(
        [sys.executable, "-c", verification_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Verification failed:\n{result.stderr}\n{result.stdout}"
    assert "SUCCESS" in result.stdout, "Verification script did not complete successfully."