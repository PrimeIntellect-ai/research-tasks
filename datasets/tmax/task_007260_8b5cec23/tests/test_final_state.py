# test_final_state.py

import os
import re
import pytest

REPORT_PATH = '/home/user/report.txt'

def test_report_exists():
    """Verify that the report file was created."""
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

def test_isolated_batch_mean():
    """Verify the Isolated Batch 2 Data Mean is exactly 0.00 or -0.00."""
    with open(REPORT_PATH, 'r') as f:
        content = f.read()

    match = re.search(r'Isolated Batch 2 Data Mean:\s*(-?\d+\.\d+)', content)
    assert match is not None, "Could not find 'Isolated Batch 2 Data Mean' in the report."

    val = float(match.group(1))
    assert val == 0.0, f"Isolated Batch 2 Data Mean should be 0.00, but got {match.group(1)}"

def test_leaky_batch_mean():
    """Verify the Leaky Batch 2 Data Mean is between 0.10 and 0.20."""
    with open(REPORT_PATH, 'r') as f:
        content = f.read()

    match = re.search(r'Leaky Batch 2 Data Mean:\s*(-?\d+\.\d+)', content)
    assert match is not None, "Could not find 'Leaky Batch 2 Data Mean' in the report."

    val = float(match.group(1))
    assert 0.10 < val < 0.20, f"Leaky Batch 2 Data Mean should be between 0.10 and 0.20, but got {val}"

def test_confidence_intervals_format():
    """Verify the confidence intervals are formatted correctly."""
    with open(REPORT_PATH, 'r') as f:
        content = f.read()

    isolated_ci_match = re.search(r'Isolated Time 95% CI:\s*\[\[(-?\d+\.\d+)\],\s*\[(-?\d+\.\d+)\]\]', content)
    assert isolated_ci_match is not None, "Isolated Time 95% CI format is incorrect or missing."

    leaky_ci_match = re.search(r'Leaky Time 95% CI:\s*\[\[(-?\d+\.\d+)\],\s*\[(-?\d+\.\d+)\]\]', content)
    assert leaky_ci_match is not None, "Leaky Time 95% CI format is incorrect or missing."

    # Check that lower <= upper
    iso_lower, iso_upper = map(float, isolated_ci_match.groups())
    assert iso_lower <= iso_upper, f"Isolated CI lower bound ({iso_lower}) > upper bound ({iso_upper})"

    leaky_lower, leaky_upper = map(float, leaky_ci_match.groups())
    assert leaky_lower <= leaky_upper, f"Leaky CI lower bound ({leaky_lower}) > upper bound ({leaky_upper})"

def test_mean_time_format():
    """Verify the mean time format is correct."""
    with open(REPORT_PATH, 'r') as f:
        content = f.read()

    iso_time_match = re.search(r'Isolated Mean Time:\s*(-?\d+\.\d+)\s*us', content)
    assert iso_time_match is not None, "Isolated Mean Time format is incorrect or missing."

    leaky_time_match = re.search(r'Leaky Mean Time:\s*(-?\d+\.\d+)\s*us', content)
    assert leaky_time_match is not None, "Leaky Mean Time format is incorrect or missing."