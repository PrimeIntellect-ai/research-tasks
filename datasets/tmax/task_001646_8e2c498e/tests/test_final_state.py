# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_output_nc_exists():
    """Verify that the output NetCDF file was created."""
    output_file = "/home/user/output.nc"
    assert os.path.exists(output_file), f"Output file {output_file} is missing."
    assert os.path.isfile(output_file), f"{output_file} is not a file."
    assert os.path.getsize(output_file) > 0, f"{output_file} is empty."

def test_result_log_exists():
    """Verify that the result.log file was created."""
    log_file = "/home/user/result.log"
    assert os.path.exists(log_file), f"Log file {log_file} is missing."
    assert os.path.isfile(log_file), f"{log_file} is not a file."

def test_data_and_calculations():
    """
    Verify the calculations, including mesh refinement, probability distribution, 
    and KL divergence, by using the system's Python environment to read the NetCDF files.
    """
    verification_script = """
import sys
try:
    import netCDF4 as nc
    import numpy as np
except ImportError:
    print("Required libraries (netCDF4, numpy) are not installed in the system.")
    sys.exit(1)

# Read input to compute expected values
try:
    ds_in = nc.Dataset('/home/user/input.nc', 'r')
    coarse = ds_in.variables['coarse_data'][:]
    ds_in.close()
except Exception as e:
    print(f"Failed to read input.nc: {e}")
    sys.exit(1)

expected_refined = np.zeros(199)
expected_refined[0::2] = coarse
expected_refined[1::2] = (coarse[:-1] + coarse[1:]) / 2.0

expected_P = expected_refined / np.sum(expected_refined)
Q = 1.0 / 199.0
expected_KL = np.sum(expected_P * np.log(expected_P / Q))

# Verify log file
try:
    with open('/home/user/result.log', 'r') as f:
        log_content = f.read().strip()
except Exception as e:
    print(f"Failed to read result.log: {e}")
    sys.exit(1)

expected_log = f"KL: {expected_KL:.6f}"
if log_content != expected_log:
    print(f"Log content mismatch. Expected '{expected_log}', got '{log_content}'")
    sys.exit(1)

# Verify output.nc
try:
    ds_out = nc.Dataset('/home/user/output.nc', 'r')
except Exception as e:
    print(f"Failed to open output.nc: {e}")
    sys.exit(1)

if 'refined_data' not in ds_out.variables:
    print("Variable 'refined_data' missing from output.nc")
    sys.exit(1)
if 'P' not in ds_out.variables:
    print("Variable 'P' missing from output.nc")
    sys.exit(1)

out_refined = ds_out.variables['refined_data'][:]
out_P = ds_out.variables['P'][:]
ds_out.close()

if not np.allclose(out_refined, expected_refined, atol=1e-6):
    print("The 'refined_data' values in output.nc do not match the expected interpolated values.")
    sys.exit(1)

if not np.allclose(out_P, expected_P, atol=1e-6):
    print("The 'P' values in output.nc do not match the expected normalized distribution.")
    sys.exit(1)
"""

    result = subprocess.run(
        [sys.executable, "-c", verification_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Verification failed:\n{result.stdout}\n{result.stderr}"