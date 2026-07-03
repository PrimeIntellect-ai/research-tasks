# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_results_file_exists():
    """Check that the output HDF5 file was created."""
    results_file = "/home/user/results.h5"
    assert os.path.exists(results_file), f"The output file {results_file} does not exist."
    assert os.path.isfile(results_file), f"{results_file} is not a file."

def test_executable_exists():
    """Check that the compiled executable exists."""
    executable_path = "/home/user/src/analyze_spectra"
    assert os.path.exists(executable_path), f"The executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_results_contents():
    """
    Verify the contents of the results.h5 file against the expected SVD results.
    We use a subprocess to run a script that imports h5py, numpy, and scipy, 
    since they are installed in the base environment but we must only use stdlib in pytest.
    """
    script = """
import h5py
import numpy as np
from scipy.fft import fft
import sys

try:
    # Load input data to compute expected
    with h5py.File('/home/user/sequences.h5', 'r') as f:
        if '/dna_signals' not in f:
            print("Missing /dna_signals in sequences.h5")
            sys.exit(1)
        signals = f['/dna_signals'][:]

    N, M = signals.shape

    # Compute expected magnitude spectra
    mag_spectra = np.zeros_like(signals)
    for i in range(N):
        mag_spectra[i] = np.abs(fft(signals[i]))

    # SVD
    U, S, Vh = np.linalg.svd(mag_spectra, full_matrices=False)
    expected_s = S
    expected_v1 = Vh[0, :]

    # Load agent results
    with h5py.File('/home/user/results.h5', 'r') as f:
        if '/singular_values' not in f:
            print("Missing /singular_values in results.h5")
            sys.exit(1)
        if '/principal_spectrum' not in f:
            print("Missing /principal_spectrum in results.h5")
            sys.exit(1)

        agent_s = f['/singular_values'][:]
        agent_v1 = f['/principal_spectrum'][:]

    # Check singular values
    if not np.allclose(expected_s, agent_s, rtol=1e-3, atol=1e-3):
        print(f"Singular values mismatch. Expected: {expected_s}, Got: {agent_s}")
        sys.exit(1)

    # Check principal spectrum (allow sign flip, as SVD sign is arbitrary)
    sign_flip = 1.0
    if np.sign(agent_v1[0]) != np.sign(expected_v1[0]) and agent_v1[0] != 0:
        sign_flip = -1.0

    if not np.allclose(expected_v1, agent_v1 * sign_flip, rtol=1e-3, atol=1e-3):
        print("Principal spectrum mismatch.")
        sys.exit(1)

    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"Verification script failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"