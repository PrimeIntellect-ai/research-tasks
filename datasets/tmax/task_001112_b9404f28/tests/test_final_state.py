# test_final_state.py

import os
import re
import sys
import pytest

def extract_values(path):
    vals = []
    try:
        with open(path, 'r') as f:
            for line in f:
                match = re.search(r'Rolling Avg:\s*([-\d\.]+)', line)
                if match:
                    vals.append(float(match.group(1)))
    except Exception:
        pass
    return vals

def test_rolling_report_mse():
    """
    Validates that the rolling report exists, has the correct number of lines,
    and that the Mean Squared Error (MSE) of the rolling averages compared to
    the expected ground truth is within the acceptable threshold.
    """
    report_path = '/home/user/rolling_report.txt'
    assert os.path.isfile(report_path), f"Report file not found at {report_path}"

    actual = extract_values(report_path)

    # Expected hidden ground truth array based on the seed data and offsets
    expected = [15.0, 22.0, 16.5, 20.5, 18.2]

    assert len(actual) == len(expected), (
        f"Expected {len(expected)} rolling average values, but found {len(actual)}. "
        f"Actual values extracted: {actual}"
    )

    mse = sum((a - e) ** 2 for a, e in zip(actual, expected)) / len(expected)

    threshold = 0.1
    assert mse <= threshold, (
        f"MSE of rolling averages is {mse:.4f}, which exceeds the threshold of {threshold}. "
        f"Expected: {expected}, Actual: {actual}"
    )