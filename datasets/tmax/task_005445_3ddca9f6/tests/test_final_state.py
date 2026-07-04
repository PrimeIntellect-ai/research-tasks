# test_final_state.py

import os
import re

def test_plot_exists():
    """Verify that the plot file was created."""
    plot_path = '/home/user/plot.png'
    assert os.path.exists(plot_path), f"Missing required file: {plot_path}"
    assert os.path.isfile(plot_path), f"Expected a file, but found a directory: {plot_path}"
    assert os.path.getsize(plot_path) > 0, f"Plot file is empty: {plot_path}"

def test_report_exists_and_content():
    """Verify that the report file was created and contains the correct metrics."""
    report_path = '/home/user/report.txt'
    assert os.path.exists(report_path), f"Missing required file: {report_path}"
    assert os.path.isfile(report_path), f"Expected a file, but found a directory: {report_path}"

    with open(report_path, 'r') as f:
        content = f.read()

    # Expected values
    expected_mse = 0.005118
    expected_maxdiff = 0.000020
    expected_integral = -1.385317
    tolerance = 1e-5

    # Extract MSE
    mse_match = re.search(r'MSE:\s*(-?\d+\.\d+)', content)
    assert mse_match is not None, "Could not find 'MSE: <value>' in report.txt"
    mse_val = float(mse_match.group(1))
    assert abs(mse_val - expected_mse) <= tolerance, f"MSE value {mse_val} is not within tolerance of {expected_mse}"

    # Extract MaxDiff
    maxdiff_match = re.search(r'MaxDiff:\s*(-?\d+\.\d+)', content)
    assert maxdiff_match is not None, "Could not find 'MaxDiff: <value>' in report.txt"
    maxdiff_val = float(maxdiff_match.group(1))
    assert abs(maxdiff_val - expected_maxdiff) <= tolerance, f"MaxDiff value {maxdiff_val} is not within tolerance of {expected_maxdiff}"

    # Extract Integral
    integral_match = re.search(r'Integral:\s*(-?\d+\.\d+)', content)
    assert integral_match is not None, "Could not find 'Integral: <value>' in report.txt"
    integral_val = float(integral_match.group(1))
    assert abs(integral_val - expected_integral) <= tolerance, f"Integral value {integral_val} is not within tolerance of {expected_integral}"