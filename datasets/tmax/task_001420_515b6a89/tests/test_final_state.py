# test_final_state.py

import os
import subprocess
import pytest

def test_venv_exists():
    """Verify that the virtual environment was created successfully."""
    venv_dir = '/home/user/venv'
    python_bin = '/home/user/venv/bin/python'
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."
    assert os.path.isfile(python_bin), f"Python executable not found at {python_bin}. Is the venv properly created?"

def test_results_file_exists():
    """Verify that the results.h5 file was created."""
    results_file = '/home/user/results.h5'
    assert os.path.isfile(results_file), f"Output file {results_file} does not exist."

def test_results_contents_and_accuracy():
    """
    Verify the contents of results.h5 using the packages installed in the venv.
    Checks for presence of datasets, shapes, absence of NaNs, and convergence to the steady state.
    """
    checker_script = """
import sys
try:
    import h5py
    import numpy as np
except ImportError as e:
    print(f"Missing required package: {e}")
    sys.exit(1)

try:
    with h5py.File('/home/user/results.h5', 'r') as f:
        if 'time' not in f:
            print("Dataset 'time' missing from results.h5")
            sys.exit(1)
        if 'frequency' not in f:
            print("Dataset 'frequency' missing from results.h5")
            sys.exit(1)

        times = f['time'][:]
        freqs = f['frequency'][:]

        if len(times) != 1000:
            print(f"Expected 1000 time points, got {len(times)}")
            sys.exit(1)
        if len(freqs) != 1000:
            print(f"Expected 1000 frequency points, got {len(freqs)}")
            sys.exit(1)

        if np.isnan(freqs).any():
            print("Simulation results contain NaNs. The integration is still unstable.")
            sys.exit(1)

        # The steady state of dy/dt = r*y*(1-y) - m*y is y* = 1 - m/r
        # For r=150, m=30, y* = 0.8
        final_freq = freqs[-1]
        if not np.isclose(final_freq, 0.8, atol=1e-3):
            print(f"Numerical integration did not converge to correct steady state. Expected ~0.8, got {final_freq}")
            sys.exit(1)

except Exception as e:
    print(f"Unexpected error while reading HDF5: {e}")
    sys.exit(1)
"""
    python_bin = '/home/user/venv/bin/python'
    result = subprocess.run([python_bin, '-c', checker_script], capture_output=True, text=True)

    error_message = result.stdout.strip() or result.stderr.strip()
    assert result.returncode == 0, f"Results verification failed: {error_message}"