# test_final_state.py
import os
import re
import pytest

def test_results_file_exists():
    assert os.path.exists('/home/user/results.txt'), "The results file /home/user/results.txt is missing."

def test_results_content():
    with open('/home/user/results.txt', 'r') as f:
        content = f.read()

    alpha_match = re.search(r'Alpha:\s*([0-9.]+)', content)
    assert alpha_match is not None, "Alpha value not found in results.txt. Check the output format."
    alpha = float(alpha_match.group(1))
    assert abs(alpha - 0.963) <= 0.005, f"Expected Alpha to be approximately 0.963, but got {alpha}"

    integral_match = re.search(r'Integral:\s*([0-9.]+)', content)
    assert integral_match is not None, "Integral value not found in results.txt. Check the output format."
    integral = float(integral_match.group(1))
    assert abs(integral - 1063.310) <= 0.05, f"Expected Integral to be approximately 1063.310, but got {integral}"

def test_cpp_file_exists():
    assert os.path.exists('/home/user/analyze_network.cpp'), "The source code file /home/user/analyze_network.cpp is missing."