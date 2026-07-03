# test_final_state.py

import os
import math

def test_posterior_params():
    file_path = "/home/user/posterior_params.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist. The Bayesian inference step might have failed or the file was saved to the wrong location."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "23,12", f"Expected '23,12' in {file_path}, but got '{content}'."

def test_regression_coefs():
    file_path = "/home/user/regression_coefs.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist. The Classification Modeling step might have failed."

    with open(file_path, "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 3, f"Expected 3 comma-separated values in {file_path}, but got {len(parts)}."

    try:
        intercept = float(parts[0])
        coef_temp = float(parts[1])
        coef_pressure = float(parts[2])
    except ValueError:
        assert False, f"Could not parse the contents of {file_path} as floats. Content: '{content}'"

    expected_intercept = -468.2709
    expected_temp = 24.4604
    expected_pressure = -35.1226

    tolerance = 1e-2

    assert math.isclose(intercept, expected_intercept, abs_tol=tolerance), f"Intercept {intercept} is not within {tolerance} of {expected_intercept}."
    assert math.isclose(coef_temp, expected_temp, abs_tol=tolerance), f"Temperature coefficient {coef_temp} is not within {tolerance} of {expected_temp}."
    assert math.isclose(coef_pressure, expected_pressure, abs_tol=tolerance), f"Pressure coefficient {coef_pressure} is not within {tolerance} of {expected_pressure}."