# test_final_state.py

import os
import pytest

def test_logistic_euler_fixed():
    script_path = "/home/user/logistic_euler.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that the step size was changed to 0.01
    assert "0.01" in content, "The script does not seem to use the dt=0.01 step size as requested."
    assert "dt = 2" not in content, "The script still contains the bad step size dt = 2."

def test_mae_calculated():
    mae_path = "/home/user/mae.txt"
    assert os.path.isfile(mae_path), f"File {mae_path} does not exist."

    with open(mae_path, "r") as f:
        mae_str = f.read().strip()

    assert mae_str, "mae.txt is empty."

    try:
        mae_val = float(mae_str)
    except ValueError:
        pytest.fail(f"mae.txt does not contain a valid floating-point number. Found: '{mae_str}'")

    # The expected MAE with dt=0.01 is approximately 0.16165.
    # Depending on floating-point precision and loop bounds (1000 vs 1001 iterations), 
    # the exact value might vary slightly. We allow a reasonable tolerance.
    expected_mae = 0.16165
    tolerance = 0.01

    assert abs(mae_val - expected_mae) <= tolerance, \
        f"MAE value {mae_val} is not within the expected range (expected ~{expected_mae})."