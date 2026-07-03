# test_final_state.py

import os
import pytest

def test_analysis_py_exists():
    """Check if the python script was generated."""
    script_path = '/home/user/analysis.py'
    assert os.path.exists(script_path), f"Expected script {script_path} does not exist. Did you convert the notebook?"
    assert os.path.isfile(script_path), f"Expected {script_path} to be a file."

def test_analysis_py_fixed():
    """Check if the bug in the ODE derivative was fixed."""
    script_path = '/home/user/analysis.py'
    assert os.path.exists(script_path), f"Cannot check fix, {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # The fix should make dSdt negative
    assert "-beta * S * I" in content or "- beta * S * I" in content or "-1 * beta" in content or "-(beta" in content or "- (beta" in content, \
        "The mathematical bug in the ODE derivative function (dSdt) does not appear to be fixed. It should be negative."

def test_fitted_params_csv():
    """Check if the fitted_params.csv is generated correctly."""
    csv_path = '/home/user/fitted_params.csv'
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist. Did you run the fixed script?"

    with open(csv_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"Expected exactly two comma-separated values in {csv_path}, got: {content}"

    try:
        beta = float(parts[0])
        gamma = float(parts[1])
    except ValueError:
        pytest.fail(f"Could not parse beta and gamma as floats from {csv_path}. Content: {content}")

    assert 0.38 < beta < 0.42, f"Fitted beta value {beta} is out of expected bounds. Is the ODE correct?"
    assert 0.08 < gamma < 0.12, f"Fitted gamma value {gamma} is out of expected bounds. Is the ODE correct?"

    # Check 4 decimal places format
    assert len(parts[0].split('.')[-1]) == 4, f"Beta value {parts[0]} is not formatted to 4 decimal places."
    assert len(parts[1].split('.')[-1]) == 4, f"Gamma value {parts[1]} is not formatted to 4 decimal places."