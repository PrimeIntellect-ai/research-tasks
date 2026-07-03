# test_final_state.py

import os
import re
import math

def test_validation_log_exists_and_format():
    """Test that the validation.log file exists and has the correct format and values."""
    log_path = "/home/user/validation.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you run your C program?"

    with open(log_path, 'r') as f:
        text = f.read()

    ana_match = re.search(r'Analytical:\s*([0-9.]+)', text)
    num_match = re.search(r'Numerical:\s*([0-9.]+)', text)
    err_match = re.search(r'Error:\s*([0-9.]+)', text)

    assert ana_match is not None, "Could not find 'Analytical: <value>' in validation.log"
    assert num_match is not None, "Could not find 'Numerical: <value>' in validation.log"
    assert err_match is not None, "Could not find 'Error: <value>' in validation.log"

    ana_val = float(ana_match.group(1))
    num_val = float(num_match.group(1))
    err_val = float(err_match.group(1))

    # Calculate expected analytical value
    alpha = 0.001
    expected_ana = (2.0 / alpha) * math.atan(1.0 / alpha)

    assert abs(ana_val - expected_ana) < 0.001, f"Analytical value {ana_val} is incorrect. Expected ~{expected_ana:.6f}"

    # Check numerical value is close to analytical
    assert abs(num_val - expected_ana) < 0.01, f"Numerical value {num_val} is too far from analytical value."

    # Check reported error is small
    assert err_val < 0.01, f"Reported error {err_val} is too high."

    # Also check if reported error matches the absolute difference
    expected_err = abs(ana_val - num_val)
    assert abs(err_val - expected_err) < 0.001, f"Reported error {err_val} does not match actual difference {expected_err:.6f}"