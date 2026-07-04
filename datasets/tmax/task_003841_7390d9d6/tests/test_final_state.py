# test_final_state.py

import os
import pytest

def test_gd_awk_exists():
    """Test that the gradient descent awk script exists."""
    assert os.path.isfile("/home/user/gd.awk"), "File /home/user/gd.awk is missing."

def test_analytical_awk_exists():
    """Test that the analytical awk script exists."""
    assert os.path.isfile("/home/user/analytical.awk"), "File /home/user/analytical.awk is missing."

def test_test_sh_exists():
    """Test that the test bash script exists."""
    assert os.path.isfile("/home/user/test.sh"), "File /home/user/test.sh is missing."

def test_gd_result_content():
    """Test the output of the gradient descent script."""
    result_file = "/home/user/gd_result.txt"
    assert os.path.isfile(result_file), f"File {result_file} is missing."
    with open(result_file, "r") as f:
        content = f.read().strip()

    # Gradient descent with lr=0.5, 500 epochs will converge to the analytical solution.
    assert content == "2.0030,1.0233", f"Content of {result_file} is incorrect. Expected '2.0030,1.0233', got '{content}'."

def test_analytical_result_content():
    """Test the output of the analytical script."""
    result_file = "/home/user/analytical_result.txt"
    assert os.path.isfile(result_file), f"File {result_file} is missing."
    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content == "2.0030,1.0233", f"Content of {result_file} is incorrect. Expected '2.0030,1.0233', got '{content}'."

def test_regression_log_content():
    """Test the output of the regression test script."""
    log_file = "/home/user/regression.log"
    assert os.path.isfile(log_file), f"File {log_file} is missing."
    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content == "PASS", f"Content of {log_file} is incorrect. Expected 'PASS', got '{content}'."