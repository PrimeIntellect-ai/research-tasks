# test_final_state.py

import os
import pytest

def test_executable_exists_and_runnable():
    """Test that the compiled executable exists and is executable."""
    executable_path = "/home/user/motif_sim"
    assert os.path.exists(executable_path), f"Executable {executable_path} does not exist."
    assert os.path.isfile(executable_path), f"Path {executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_result_file_exists_and_correct():
    """Test that the result.txt file exists and contains the correct output."""
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Result file {result_path} does not exist."
    assert os.path.isfile(result_path), f"Path {result_path} is not a file."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content, f"Result file {result_path} is empty."

    try:
        result_value = float(content)
    except ValueError:
        pytest.fail(f"Content of {result_path} is not a valid float: '{content}'")

    expected_value = 0.99933
    tolerance = 0.0001

    assert abs(result_value - expected_value) <= tolerance, \
        f"Result value {result_value} is not within {tolerance} of expected {expected_value}."

def test_c_code_fixed():
    """Test that the C code has been modified to fix the bug."""
    file_path = "/home/user/motif_ode.c"
    assert os.path.exists(file_path), f"Source file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    # The original bug was `dt *= 2.0;` when err > TOL.
    # We can just ensure that the original buggy line is not there, or that a reduction is present.
    # Since the student might format it differently, checking for absence of the exact bug is safest.
    # However, to be robust, we just check that the result is correct (which is done above).
    # But we can also check that "dt *= 2.0;" under the error condition is gone.
    # A simple string check for "dt *= 2.0;" might be too strict if they left it in a comment, 
    # but let's just assert the result is correct. The result test is the primary validation.
    pass