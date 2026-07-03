# test_final_state.py

import os
import re
import pytest

def test_stability_report_exists_and_correct():
    """Verify that the stability report was generated with the correct confidence intervals."""
    report_path = '/home/user/stability_report.txt'
    assert os.path.isfile(report_path), f"The expected output file {report_path} is missing."

    with open(report_path, 'r') as f:
        content = f.read()

    lower_match = re.search(r'Lower CI:\s*([0-9.]+)', content)
    upper_match = re.search(r'Upper CI:\s*([0-9.]+)', content)

    assert lower_match is not None, "Could not find 'Lower CI: <value>' in the report."
    assert upper_match is not None, "Could not find 'Upper CI: <value>' in the report."

    lower_val = float(lower_match.group(1))
    upper_val = float(upper_match.group(1))

    # Expected values based on the setup seed and bootstrap method
    expected_lower = 0.000494
    expected_upper = 0.000506

    # Allow a small tolerance for minor floating point variance across different numpy versions
    tolerance = 2e-6

    assert abs(lower_val - expected_lower) <= tolerance, \
        f"Lower CI value {lower_val} is not within acceptable tolerance of expected {expected_lower}."
    assert abs(upper_val - expected_upper) <= tolerance, \
        f"Upper CI value {upper_val} is not within acceptable tolerance of expected {expected_upper}."

def test_script_exists():
    """Check if the analyze_stability.py script exists."""
    script_path = '/home/user/analyze_stability.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."