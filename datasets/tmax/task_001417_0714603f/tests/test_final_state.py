# test_final_state.py

import os
import subprocess
import json
import pytest

def test_pytest_passes():
    """
    Ensure that the test_fit.py suite passes, which verifies that the
    floating-point reduction issue in compute_metric has been fixed.
    """
    test_file = "/home/user/project/test_fit.py"
    assert os.path.isfile(test_file), f"Test file {test_file} is missing."

    result = subprocess.run(
        ["pytest", test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest failed on {test_file}. Output:\n{result.stdout}\n{result.stderr}"

def test_output_nc_exists_and_correct():
    """
    Ensure that output.nc is created correctly with the required dimensions,
    variable name, and data type. We use subprocess to avoid direct third-party
    imports in the test file itself.
    """
    output_nc = "/home/user/project/output.nc"
    assert os.path.isfile(output_nc), f"Output file {output_nc} is missing. Did you run save_to_netcdf?"

    script = f"""
import sys
import json
try:
    import netCDF4 as nc
except ImportError:
    print(json.dumps({{"error": "netCDF4 not installed"}}))
    sys.exit(1)

try:
    ds = nc.Dataset('{output_nc}', 'r')
    if 'power_spectrum' not in ds.variables:
        print(json.dumps({{"error": "Variable 'power_spectrum' not found"}}))
        sys.exit(2)

    var = ds.variables['power_spectrum']

    # Check dimensions
    dims = list(ds.dimensions.keys())

    print(json.dumps({{
        "shape": list(var.shape),
        "dtype": str(var.dtype),
        "dimensions": dims
    }}))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
    sys.exit(3)
"""
    result = subprocess.run(
        ["python3", "-c", script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Failed to inspect {output_nc}. Output:\n{result.stdout}\n{result.stderr}"

    try:
        info = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON from inspection script. Output: {result.stdout}")

    if "error" in info:
        pytest.fail(f"Error inspecting netCDF file: {info['error']}")

    # Check shape: 10 rows, 1024 elements -> rfft gives 1024 // 2 + 1 = 513
    expected_shape = [10, 513]
    assert info["shape"] == expected_shape, f"Expected shape {expected_shape}, got {info['shape']}"

    # Check dtype is float64 / f8
    assert info["dtype"] in ["float64", "f8", ">f8", "<f8"], f"Expected float64/f8 dtype, got {info['dtype']}"

    # Check dimensions names
    assert "row" in info["dimensions"], "Dimension 'row' missing in netCDF file."
    assert "freq" in info["dimensions"], "Dimension 'freq' missing in netCDF file."