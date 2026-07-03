# test_final_state.py

import os
import pytest

def test_test_report_exists():
    """
    Check that the generated test report exists.
    """
    report_file = "/home/user/test_report.txt"
    assert os.path.exists(report_file), f"Output report file is missing: {report_file}"
    assert os.path.isfile(report_file), f"Path is not a file: {report_file}"

def test_test_report_contents():
    """
    Check the contents of the test report for the correct format and values.
    """
    report_file = "/home/user/test_report.txt"
    assert os.path.exists(report_file), f"Output report file is missing: {report_file}"

    expected_output = (
        "Calculated Peak Frequency: 125.00 Hz\n"
        "Baseline Peak Frequency: 125.00 Hz\n"
        "Regression Test: PASS"
    )

    with open(report_file, "r") as f:
        content = f.read().strip()

    assert expected_output in content, (
        f"The contents of {report_file} do not match the expected output.\n"
        f"Expected:\n{expected_output}\n"
        f"Got:\n{content}"
    )