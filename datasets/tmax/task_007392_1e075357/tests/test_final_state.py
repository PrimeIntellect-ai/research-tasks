# test_final_state.py
import os
import re

def test_mse_validation_log_exists_and_correct():
    """Check that the MSE validation log exists and contains the correct MSE value."""
    log_path = "/home/user/mse_validation.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    # Expecting format "MSE: <value>"
    match = re.search(r"MSE:\s*([0-9]+\.[0-9]+)", content)
    assert match is not None, f"Could not find 'MSE: <value>' in {log_path}. Content was: {content}"

    mse_value = float(match.group(1))
    expected_mse = 0.015926
    tolerance = 0.000010

    assert abs(mse_value - expected_mse) <= tolerance, f"Calculated MSE {mse_value} is not within {tolerance} of expected {expected_mse}."

def test_go_module_and_simulate_exists():
    """Check that the Go module and simulate.go exist."""
    assert os.path.exists("/home/user/diffusion/go.mod"), "Go module was not initialized in /home/user/diffusion."
    assert os.path.exists("/home/user/diffusion/simulate.go"), "simulate.go was not found in /home/user/diffusion."