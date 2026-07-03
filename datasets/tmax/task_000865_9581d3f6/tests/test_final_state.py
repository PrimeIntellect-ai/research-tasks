# test_final_state.py

import os
import subprocess
import pytest

def test_run_pipeline_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_cargo_project_exists():
    cargo_toml = "/home/user/diffusion_data/Cargo.toml"
    assert os.path.exists(cargo_toml), f"Cargo project not found at {cargo_toml}."

def test_hdf5_output_valid():
    hdf5_path = "/home/user/training_data.h5"
    assert os.path.exists(hdf5_path), f"The output file {hdf5_path} does not exist."

    # Use a subprocess to validate HDF5 contents since we are restricted to the standard library
    # but the environment contains numpy and h5py which are necessary to read the HDF5 file easily.
    validation_script = """
import numpy as np
import h5py
import sys

x = np.linspace(0, 1, 50)
data = []
for i in range(10):
    u = np.sin(np.pi * x * (i + 1)) + 0.5 * np.sin(3 * np.pi * x)
    u[0] = 0
    u[-1] = 0
    data.append(u)
data = np.array(data)

alpha = 0.01
dx = 1.0 / 49.0
dt = 0.0001
c = alpha * dt / (dx**2)

expected_res = []
for i in range(10):
    u = data[i].copy()
    while True:
        u_new = u.copy()
        for j in range(1, 49):
            u_new[j] = u[j] + c * (u[j+1] - 2*u[j] + u[j-1])
        diff = np.max(np.abs(u_new - u))
        u = u_new
        if diff < 1e-6:
            break
    expected_res.append(u)
expected_res = np.array(expected_res)

try:
    with h5py.File('/home/user/training_data.h5', 'r') as f:
        if 'converged_states' not in f:
            print("Dataset 'converged_states' not found.")
            sys.exit(1)
        actual_res = f['converged_states'][:]

        if actual_res.shape != (10, 50):
            print(f"Expected shape (10, 50), got {actual_res.shape}")
            sys.exit(1)

        max_diff = np.max(np.abs(actual_res - expected_res))
        if max_diff >= 1e-5:
            print(f"Max difference {max_diff} exceeds tolerance 1e-5.")
            sys.exit(1)

except Exception as e:
    print(f"Exception during validation: {e}")
    sys.exit(1)
"""
    result = subprocess.run(
        ["python3", "-c", validation_script],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"HDF5 validation failed:\n{result.stdout}\n{result.stderr}"