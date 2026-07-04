# test_final_state.py

import os

def test_report_csv_exists_and_correct():
    report_path = "/home/user/output/report.csv"
    assert os.path.isfile(report_path), f"Report file missing: {report_path}"

    expected_lines = [
        "P5,3",
        "P1,2",
        "P2,1",
        "P4,1"
    ]

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report.csv, but got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"