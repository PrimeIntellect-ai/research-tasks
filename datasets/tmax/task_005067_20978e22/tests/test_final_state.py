# test_final_state.py

import os
import math

def test_result_file_exists():
    """Check if the result file was generated."""
    file_path = "/home/user/result.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_result_value():
    """Check if the computed frequency is within the expected range."""
    file_path = "/home/user/result.txt"
    with open(file_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {file_path} is not a valid float: '{content}'"

    assert abs(val - 0.0385) < 0.005, f"Frequency {val} is incorrect, expected approximately 0.0385 Hz."

def test_binary_exists():
    """Check if the compiled binary exists and is executable."""
    file_path = "/home/user/repressilator/sim"
    assert os.path.isfile(file_path), f"Compiled binary {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"Binary {file_path} is not executable."

def test_integrator_fixed():
    """Verify the bug in integrator.cpp was fixed."""
    file_path = "/home/user/repressilator/integrator.cpp"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().replace(" ", "")

    # The bug was `err/tol`, the fix should be `tol/err`
    assert "tol/err" in content, "The bug in integrator.cpp does not seem to be fixed (expected 'tol / err')."

def test_fftw3_installed():
    """Verify that FFTW3 development headers are installed."""
    assert os.path.isfile("/usr/include/fftw3.h"), "FFTW3 headers not found. Ensure libfftw3-dev is installed."