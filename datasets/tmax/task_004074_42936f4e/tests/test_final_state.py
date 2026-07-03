# test_final_state.py
import os
import re
import pytest

def test_calibration_result_exists_and_valid():
    result_file = "/home/user/calibration_result.txt"
    assert os.path.isfile(result_file), f"Result file {result_file} is missing"

    with open(result_file, 'r') as f:
        content = f.read()

    scale_match = re.search(r'scale=([0-9\.\-]+)', content)
    shift_match = re.search(r'shift=([0-9\.\-]+)', content)
    mse_match = re.search(r'mse=([0-9\.\-]+)', content)

    assert scale_match, "Format error: 'scale=<float>' not found in calibration_result.txt"
    assert shift_match, "Format error: 'shift=<float>' not found in calibration_result.txt"
    assert mse_match, "Format error: 'mse=<float>' not found in calibration_result.txt"

    try:
        scale = float(scale_match.group(1))
        shift = float(shift_match.group(1))
    except ValueError:
        pytest.fail("Could not parse scale or shift as floats.")

    # Ground truth parameters
    target_scale = 1.45
    target_shift = -2.10

    # Proxy for the MSE metric used by the scorer
    error = (scale - target_scale)**2 + (shift - target_shift)**2

    assert error <= 0.02, f"Error metric {error:.5f} exceeds the threshold of 0.02. Found scale={scale}, shift={shift}"

def test_calibrate_script_exists_and_executable():
    script_file = "/home/user/calibrate.sh"
    assert os.path.isfile(script_file), f"Script file {script_file} is missing"
    assert os.access(script_file, os.X_OK), f"Script file {script_file} is not executable"