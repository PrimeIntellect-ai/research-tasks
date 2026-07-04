# test_final_state.py

import os
import subprocess
import pytest

def test_venv_exists():
    """Verify that the virtual environment exists and contains a Python executable."""
    venv_python = "/home/user/venv/bin/python"
    assert os.path.exists(venv_python), f"Virtual environment Python executable not found at {venv_python}"

def test_simulate_script_exists():
    """Verify that the simulation script was created."""
    assert os.path.exists("/home/user/simulate.py"), "/home/user/simulate.py does not exist."

def test_integral_estimate():
    """Verify that the integral estimate text file exists and contains the correct value."""
    estimate_file = "/home/user/integral_estimate.txt"
    assert os.path.exists(estimate_file), f"{estimate_file} does not exist."

    with open(estimate_file, "r") as f:
        content = f.read().strip()

    # Compute the expected value using the venv's python and numpy
    script = """
import numpy as np
np.random.seed(42)
x = np.random.uniform(0, 2, 1000000)
y = np.random.uniform(0, 1, 1000000)
under = y < np.exp(-x**2)
integral = 2.0 * np.sum(under) / 1000000
print(f"{integral:.5f}")
"""
    result = subprocess.run(["/home/user/venv/bin/python", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run numpy in the virtual environment. Is numpy installed?"

    expected = result.stdout.strip()
    assert content == expected, f"Integral estimate mismatch. Expected '{expected}', got '{content}'."

def test_h5_file():
    """Verify that the HDF5 file exists and contains the correct dataset."""
    h5_file = "/home/user/simulation.h5"
    assert os.path.exists(h5_file), f"{h5_file} does not exist."

    # Validate the HDF5 file contents using the venv's python and h5py
    script = """
import sys
try:
    import h5py
except ImportError:
    print("h5py is not installed")
    sys.exit(1)

try:
    with h5py.File('/home/user/simulation.h5', 'r') as f:
        if 'mc_epochs' not in f:
            print("Dataset 'mc_epochs' not found in HDF5 file.")
            sys.exit(1)
        ds = f['mc_epochs']
        if ds.shape != (1000, 1000):
            print(f"Dataset 'mc_epochs' has incorrect shape. Expected (1000, 1000), got {ds.shape}.")
            sys.exit(1)
        if not str(ds.dtype).startswith('int'):
            print(f"Dataset 'mc_epochs' has incorrect dtype. Expected an integer type, got {ds.dtype}.")
            sys.exit(1)
except Exception as e:
    print(f"Error reading HDF5 file: {e}")
    sys.exit(1)
"""
    result = subprocess.run(["/home/user/venv/bin/python", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"HDF5 validation failed:\n{result.stdout.strip()}"