# test_final_state.py

import os
import pytest

SIM_DIR = "/home/user/profiling_sim"

def test_libmatrix_compiled():
    """Ensure libmatrix.so was successfully compiled."""
    lib_path = os.path.join(SIM_DIR, "libmatrix.so")
    assert os.path.exists(lib_path), "libmatrix.so was not compiled. Make sure build.sh is fixed and executed."

def test_simulate_py_fixed():
    """Check that simulate.py was modified to fix the known bugs."""
    sim_path = os.path.join(SIM_DIR, "simulate.py")
    assert os.path.exists(sim_path), "simulate.py is missing."

    with open(sim_path, "r") as f:
        content = f.read()

    assert "if guess == next_guess:" not in content, (
        "The infinite recursion bug in calculate_sqrt was not fixed. "
        "The exact equality check 'guess == next_guess' is still present."
    )

    assert "SUM(duration)" not in content, (
        "The SQL query bug was not fixed. "
        "The script is still querying SUM(duration) instead of the average."
    )

def test_final_report_content():
    """Ensure final_report.txt contains the correct output."""
    report_path = os.path.join(SIM_DIR, "final_report.txt")
    assert os.path.exists(report_path), "final_report.txt was not created."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_output = "Average execution time: 17.5 ms"
    assert expected_output in content, (
        f"final_report.txt does not contain the correct output.\n"
        f"Expected to find: '{expected_output}'\n"
        f"Actual content: '{content}'"
    )