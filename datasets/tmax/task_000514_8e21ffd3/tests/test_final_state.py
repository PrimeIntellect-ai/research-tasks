# test_final_state.py

import os
import math
import re

def test_etl_stats_cpp_exists():
    """Verify that the C++ source file exists."""
    cpp_path = "/home/user/etl_stats.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} is missing."
    assert os.path.isfile(cpp_path), f"{cpp_path} is not a file."

def test_etl_report_exists_and_correct():
    """Verify that the report file exists and contains the correct statistics."""
    report_path = "/home/user/etl_report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} is missing."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        content = f.read().strip()

    # The expected values are:
    # Mean: 3.1000
    # CI: [2.0561, 4.1439]

    # Parse the content
    mean_match = re.search(r"Mean:\s*([0-9.]+)", content)
    assert mean_match is not None, "Could not find 'Mean: <value>' in the report file."

    ci_match = re.search(r"CI:\s*\[([0-9.]+),\s*([0-9.]+)\]", content)
    assert ci_match is not None, "Could not find 'CI: [<lower>, <upper>]' in the report file."

    actual_mean = float(mean_match.group(1))
    actual_lower = float(ci_match.group(1))
    actual_upper = float(ci_match.group(2))

    expected_mean = 3.1000
    expected_lower = 2.0561
    expected_upper = 4.1439

    assert math.isclose(actual_mean, expected_mean, abs_tol=0.0002), \
        f"Expected Mean to be ~{expected_mean:.4f}, but got {actual_mean:.4f}"

    assert math.isclose(actual_lower, expected_lower, abs_tol=0.0002), \
        f"Expected Lower CI to be ~{expected_lower:.4f}, but got {actual_lower:.4f}"

    assert math.isclose(actual_upper, expected_upper, abs_tol=0.0002), \
        f"Expected Upper CI to be ~{expected_upper:.4f}, but got {actual_upper:.4f}"

    # Also check exact string formatting if possible
    assert "Mean: 3.1000" in content, "The Mean value must be formatted to exactly 4 decimal places."
    assert "CI: [2.0561, 4.1439]" in content, "The CI values must be formatted to exactly 4 decimal places."