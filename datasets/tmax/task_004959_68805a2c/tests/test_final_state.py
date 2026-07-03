# test_final_state.py

import os
import pytest

def test_artifact_report_exists():
    """Check that the artifact_report.csv file was created."""
    report_path = '/home/user/artifact_report.csv'
    assert os.path.exists(report_path), f"Missing required file: {report_path}"
    assert os.path.isfile(report_path), f"Path is not a file: {report_path}"

def test_artifact_report_contents():
    """Check that the artifact_report.csv file contains the correct sorted data."""
    report_path = '/home/user/artifact_report.csv'

    expected_lines = [
        "filename,version,description",
        "alpha.bin,1,Alpha_Component",
        "beta.bin,2,Beta_Module",
        "delta.bin,3,Delta_Core",
        "gamma.bin,1,Gamma_Service"
    ]

    with open(report_path, 'r', encoding='utf-8') as f:
        # Read lines and strip trailing whitespace/newlines
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Report contains {len(actual_lines)} lines, expected {len(expected_lines)}"
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch.\nExpected: '{expected}'\nActual: '{actual}'"
        )