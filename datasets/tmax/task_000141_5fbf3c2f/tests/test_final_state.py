# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_hdf5_file_exists():
    """Test that the synthetic_data.h5 file was created."""
    file_path = "/home/user/synthetic_data.h5"
    assert os.path.isfile(file_path), f"The HDF5 file was not found at {file_path}"

def test_hdf5_data_validity():
    """
    Test that the HDF5 file contains the 'samples' dataset with the correct shape,
    mean, and covariance matrix. We use a subprocess to run the validation with
    numpy and h5py to adhere to the standard-library-only rule for the pytest file itself.
    """
    validation_script = """
import sys
try:
    import numpy as np
    import h5py
except ImportError:
    print("Missing required libraries (numpy, h5py).")
    sys.exit(1)

try:
    with h5py.File('/home/user/synthetic_data.h5', 'r') as f:
        if 'samples' not in f:
            print("Dataset 'samples' not found in HDF5 file.")
            sys.exit(1)

        data = f['samples'][:]

        if data.shape != (500000, 4):
            print(f"Incorrect shape. Expected (500000, 4), got {data.shape}")
            sys.exit(1)

        target_cov = np.array([
            [2.0, 0.8, 0.4, 0.2],
            [0.8, 2.0, 0.8, 0.4],
            [0.4, 0.8, 2.0, 0.8],
            [0.2, 0.4, 0.8, 2.0]
        ])

        empirical_cov = np.cov(data, rowvar=False)
        mean_vec = np.mean(data, axis=0)

        if np.max(np.abs(mean_vec)) > 0.05:
            print(f"Mean is not close to 0: {mean_vec}")
            sys.exit(1)

        max_diff = np.max(np.abs(empirical_cov - target_cov))
        if max_diff > 0.05:
            print(f"Empirical covariance differs from target by {max_diff}, which is > 0.05")
            sys.exit(1)

except Exception as e:
    print(f"Error reading or validating HDF5 file: {e}")
    sys.exit(1)
"""
    result = subprocess.run(
        [sys.executable, "-c", validation_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"HDF5 validation failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"