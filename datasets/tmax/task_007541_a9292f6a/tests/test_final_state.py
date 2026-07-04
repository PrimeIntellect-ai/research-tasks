# test_final_state.py

import os
import subprocess
import pytest

def test_venv_exists():
    """Check if the Python virtual environment is set up."""
    venv_dir = "/home/user/venv"
    python_exe = os.path.join(venv_dir, "bin", "python")
    assert os.path.isdir(venv_dir), f"Virtual environment directory not found: {venv_dir}"
    assert os.path.isfile(python_exe), f"Python executable not found in venv: {python_exe}"

def test_results_h5_exists():
    """Check if the results.h5 file was created."""
    results_file = "/home/user/results.h5"
    assert os.path.isfile(results_file), f"Results file not found: {results_file}"

def test_h5py_installed_and_results_correct():
    """
    Use the venv's Python to verify that h5py is installed and 
    the HDF5 file contains the correct dataset and values.
    """
    script = """
import sys
try:
    import h5py
except ImportError:
    print("h5py not installed in the virtual environment")
    sys.exit(1)

try:
    with h5py.File('/home/user/results.h5', 'r') as f:
        if '/optimal_P' not in f:
            print("Dataset '/optimal_P' not found in HDF5 file")
            sys.exit(1)

        data = list(f['/optimal_P'])
        expected = [1.0, 2.0, 3.0]

        if len(data) != len(expected):
            print(f"Dataset length mismatch: expected {len(expected)}, got {len(data)}")
            sys.exit(1)

        for d, e in zip(data, expected):
            if abs(d - e) > 0.1:
                print(f"Value mismatch: expected {expected}, got {data}")
                sys.exit(1)

        print("Success")
except Exception as e:
    print(f"Error reading HDF5 file: {e}")
    sys.exit(1)
"""
    script_path = "/tmp/check_h5.py"
    with open(script_path, "w") as f:
        f.write(script)

    python_exe = "/home/user/venv/bin/python"
    result = subprocess.run([python_exe, script_path], capture_output=True, text=True)

    assert result.returncode == 0, f"Verification script failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert "Success" in result.stdout, f"Verification script did not succeed.\nSTDOUT: {result.stdout}"