# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE = "/home/user/workspace"

def test_required_files_exist():
    """Verify that the required source files exist in the workspace."""
    required_files = ["Makefile", "mcmc_fitter.c", "test.sh"]
    for filename in required_files:
        filepath = os.path.join(WORKSPACE, filename)
        assert os.path.isfile(filepath), f"Required file is missing: {filepath}"

def test_test_script_execution():
    """Verify that test.sh runs successfully and generates the HDF5 file."""
    test_script = os.path.join(WORKSPACE, "test.sh")

    # Ensure it's executable
    os.chmod(test_script, 0o755)

    # Run the script
    result = subprocess.run(
        ["bash", test_script],
        cwd=WORKSPACE,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"test.sh failed to execute.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Check that chain.h5 was produced
    hdf5_file = os.path.join(WORKSPACE, "chain.h5")
    assert os.path.isfile(hdf5_file), f"HDF5 output file was not created at {hdf5_file}"

def test_hdf5_output_validity():
    """Verify the contents of the generated HDF5 file using a Python subprocess."""
    hdf5_file = os.path.join(WORKSPACE, "chain.h5")
    assert os.path.isfile(hdf5_file), "Cannot verify HDF5 contents because chain.h5 is missing."

    # We use a subprocess to run h5py and numpy since third-party imports are restricted in the test file itself.
    verify_script = f"""
import sys
import h5py
import numpy as np

try:
    with h5py.File('{hdf5_file}', 'r') as f:
        if '/K' not in f or '/e' not in f:
            sys.exit(10)

        K = f['/K'][:]
        e = f['/e'][:]

        if len(K) != 10000 or len(e) != 10000:
            sys.exit(11)

        K_mean = np.mean(K[5000:])
        e_mean = np.mean(e[5000:])

        if not (45.0 < K_mean < 55.0):
            sys.exit(12)

        if not (0.2 < e_mean < 0.4):
            sys.exit(13)
except Exception as exc:
    sys.exit(14)
"""
    result = subprocess.run(["python3", "-c", verify_script])

    if result.returncode == 10:
        pytest.fail("HDF5 file does not contain the required datasets '/K' and '/e'.")
    elif result.returncode == 11:
        pytest.fail("Datasets '/K' and '/e' do not have exactly 10,000 elements.")
    elif result.returncode == 12:
        pytest.fail("MCMC did not converge correctly: Mean of K (last 5000 steps) is out of bounds (45.0 - 55.0).")
    elif result.returncode == 13:
        pytest.fail("MCMC did not converge correctly: Mean of e (last 5000 steps) is out of bounds (0.2 - 0.4).")
    elif result.returncode == 14:
        pytest.fail("An exception occurred while attempting to read the HDF5 file.")
    elif result.returncode != 0:
        pytest.fail(f"HDF5 verification script failed with unexpected exit code {result.returncode}.")