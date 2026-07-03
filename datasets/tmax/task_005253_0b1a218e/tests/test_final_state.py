# test_final_state.py
import os
import re

def test_process_c_exists():
    path = "/home/user/process.c"
    assert os.path.isfile(path), f"Source file {path} was not created."

def test_process_executable_exists():
    path = "/home/user/process"
    assert os.path.isfile(path), f"Executable {path} was not compiled."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_results_log():
    path = "/home/user/results.log"
    assert os.path.isfile(path), f"Results log {path} was not created."

    with open(path, "r") as f:
        content = f.read().strip()

    # We expect exactly 3 lines in a specific format
    # Slope: 3.1415
    # Intercept: -2.7182
    # MSE: 0.0000

    lines = content.splitlines()
    assert len(lines) >= 3, "results.log does not contain enough lines."

    slope_match = re.search(r"Slope:\s*([\d\.\-]+)", content)
    intercept_match = re.search(r"Intercept:\s*([\d\.\-]+)", content)
    mse_match = re.search(r"MSE:\s*([\d\.\-]+)", content)

    assert slope_match is not None, "results.log is missing the 'Slope: [m]' line."
    assert intercept_match is not None, "results.log is missing the 'Intercept: [c]' line."
    assert mse_match is not None, "results.log is missing the 'MSE: [mse]' line."

    slope = float(slope_match.group(1))
    intercept = float(intercept_match.group(1))
    mse = float(mse_match.group(1))

    assert abs(slope - 3.1415) < 1e-3, f"Expected Slope close to 3.1415, got {slope}"
    assert abs(intercept - (-2.7182)) < 1e-3, f"Expected Intercept close to -2.7182, got {intercept}"
    assert abs(mse - 0.0) < 1e-3, f"Expected MSE close to 0.0000, got {mse}"

    # Also check exact formatting if possible
    assert "Slope: 3.1415" in content, "Slope not formatted to exactly 4 decimal places as 'Slope: 3.1415'."
    assert "Intercept: -2.7182" in content, "Intercept not formatted to exactly 4 decimal places as 'Intercept: -2.7182'."
    assert "MSE: 0.0000" in content, "MSE not formatted to exactly 4 decimal places as 'MSE: 0.0000'."