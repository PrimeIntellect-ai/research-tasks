# test_final_state.py

import os
import subprocess
import pytest

def test_cleaned_data_exists():
    """Test that the cleaned_data.h5 file was created."""
    file_path = "/home/user/cleaned_data.h5"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_hdf5_content():
    """Test that the HDF5 file contains the correct deduplicated matrix."""
    # We use a subprocess to run a script that uses h5py and numpy, 
    # which are available in the container environment, while keeping 
    # the test suite itself restricted to the standard library.
    script = """
import h5py
import numpy as np
import sys

try:
    with h5py.File('/home/user/cleaned_data.h5', 'r') as f:
        if '/unique_matrix' not in f:
            print("Dataset '/unique_matrix' not found.")
            sys.exit(1)

        data = f['/unique_matrix'][:]

        # Expected deduplicated sequences converted to numeric values
        # A=1, C=2, G=3, T=4
        expected = np.array([
            [1., 2., 3., 4., 1., 2., 3., 4., 1., 2., 3., 4.],
            [2., 2., 2., 2., 3., 3., 3., 3., 4., 4., 4., 4.],
            [1., 4., 1., 4., 1., 4., 1., 4., 1., 4., 1., 4.],
            [4., 4., 4., 4., 4., 4., 4., 4., 4., 4., 4., 4.]
        ], dtype=np.float64)

        if data.shape != expected.shape:
            print(f"Expected shape {expected.shape}, got {data.shape}")
            sys.exit(1)

        if not np.allclose(data, expected):
            print("Matrix values do not match expected deduplicated values.")
            sys.exit(1)

except Exception as e:
    print(f"Exception: {e}")
    sys.exit(1)

sys.exit(0)
"""
    result = subprocess.run(
        ["python3", "-c", script],
        capture_output=True,
        text=True
    )

    error_msg = f"HDF5 validation failed.\nSTDOUT: {result.stdout.strip()}\nSTDERR: {result.stderr.strip()}"
    assert result.returncode == 0, error_msg