# test_final_state.py
import os
import re

def test_cpp_file_exists():
    """Check if the C++ source file exists."""
    assert os.path.isfile("/home/user/det_sim.cpp"), "The file /home/user/det_sim.cpp does not exist."

def test_results_file_exists():
    """Check if the results file exists."""
    assert os.path.isfile("/home/user/sim_results.txt"), "The file /home/user/sim_results.txt does not exist."

def test_results_content():
    """Check if the results file contains the correct deterministic values."""
    with open("/home/user/sim_results.txt", "r") as f:
        content = f.read()

    # Define the expected values
    expected_values = {
        "Mean": "-0.001602",
        "CI_Lower": "-0.004419",
        "CI_Upper": "0.001300",
        "Prob_Near_Singular": "0.046920"
    }

    # Parse the content
    parsed_values = {}
    for line in content.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            parsed_values[key.strip()] = val.strip()

    for key, expected_val in expected_values.items():
        assert key in parsed_values, f"Key '{key}' missing in /home/user/sim_results.txt"
        assert parsed_values[key] == expected_val, f"Expected {key} to be {expected_val}, but got {parsed_values[key]}"