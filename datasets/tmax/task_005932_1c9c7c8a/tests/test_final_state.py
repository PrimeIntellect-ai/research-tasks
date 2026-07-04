# test_final_state.py

import os
import subprocess
import pytest

def test_run_sh_exists_and_executable():
    """Test that the master script run.sh exists and is executable."""
    file_path = "/home/user/ml_data_prep/run.sh"
    assert os.path.isfile(file_path), f"Master script does not exist: {file_path}"
    assert os.access(file_path, os.X_OK), f"Master script is not executable: {file_path}"

def test_filtered_csv_exists():
    """Test that the intermediate filtered.csv file was created."""
    file_path = "/home/user/ml_data_prep/filtered.csv"
    assert os.path.isfile(file_path), f"Filtered CSV does not exist: {file_path}"

    with open(file_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "filtered.csv is empty, expected some valid signals."

    # Check that rows have 100 columns
    for i, line in enumerate(lines):
        parts = line.strip().split(',')
        assert len(parts) == 100, f"Line {i+1} in filtered.csv does not have 100 values."

def test_spectra_h5_exists_and_valid():
    """Test that spectra.h5 exists and contains the correct dataset and shape.
    Since we cannot import third-party libraries directly in the pytest suite,
    we use a subprocess to run a verification script using h5py and numpy,
    which the student was instructed to install.
    """
    file_path = "/home/user/ml_data_prep/spectra.h5"
    assert os.path.isfile(file_path), f"HDF5 file does not exist: {file_path}"

    verify_script = """
import sys
try:
    import h5py
    import numpy as np
except ImportError as e:
    print(f"Missing required library: {e}", file=sys.stderr)
    sys.exit(1)

file_path = '/home/user/ml_data_prep/spectra.h5'
try:
    with h5py.File(file_path, 'r') as f:
        if 'signals' not in f:
            print("Dataset 'signals' not found.", file=sys.stderr)
            sys.exit(1)

        data = f['signals'][:]

        if len(data.shape) != 2:
            print(f"Dataset should be 2D, got shape {data.shape}", file=sys.stderr)
            sys.exit(1)

        if data.shape[1] != 100:
            print(f"Expected 100 points per signal, got {data.shape[1]}", file=sys.stderr)
            sys.exit(1)

        if data.dtype != np.float64:
            print(f"Dataset is not float64, got {data.dtype}", file=sys.stderr)
            sys.exit(1)

        for i, row in enumerate(data):
            if np.max(row) <= 0.5:
                print(f"Signal max too low on row {i}", file=sys.stderr)
                sys.exit(1)

except Exception as e:
    print(f"HDF5 verification failed: {e}", file=sys.stderr)
    sys.exit(1)
"""
    result = subprocess.run(
        ["python3", "-c", verify_script],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"HDF5 content verification failed:\n{result.stderr}"