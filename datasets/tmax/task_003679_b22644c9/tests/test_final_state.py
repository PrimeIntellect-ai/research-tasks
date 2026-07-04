# test_final_state.py
import os
import pytest

def test_fixed_report_exists_and_correct():
    report_path = "/home/user/fixed_report.txt"
    assert os.path.isfile(report_path), f"The final report file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1700000000 120",
        "1700000010 110",
        "1700000020 100",
        "1700000030 0",
        "1700000040 200",
        "1700000050 0",
        "1700000060 100"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in the report, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        actual_parts = actual.split()
        expected_parts = expected.split()
        assert actual_parts == expected_parts, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."

def test_awk_script_modified():
    awk_path = "/home/user/calculate_cooling.awk"
    assert os.path.isfile(awk_path), f"The script {awk_path} is missing."

    with open(awk_path, "r") as f:
        content = f.read()

    # The original script had no conditional logic. 
    # The fixed script should have some logic to handle CPU_TEMP <= 20.
    # We check for the presence of '20' and '0' or conditional statements, 
    # but the primary validation is the output report.
    assert "20" in content, "The awk script does not seem to contain the threshold value 20."