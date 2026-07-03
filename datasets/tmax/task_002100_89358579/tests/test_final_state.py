# test_final_state.py

import os
import pytest

def test_report_exists():
    """Check if the report file was created."""
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

def test_report_contents():
    """Check if the report file contains the correct results sorted alphabetically."""
    report_path = "/home/user/report.txt"

    if not os.path.isfile(report_path):
        pytest.fail(f"Report file {report_path} does not exist.")

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "exp1.csv: PASS",
        "exp2.csv: FAIL",
        "exp3.csv: FAIL"
    ]

    assert lines == expected_lines, (
        f"Report file contents do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(lines)}"
    )

def test_go_program_updated():
    """Check if the Go program was modified to remove the TODOs."""
    go_path = "/home/user/check_accuracy.go"

    if not os.path.isfile(go_path):
        pytest.fail(f"Go program {go_path} does not exist.")

    with open(go_path, "r") as f:
        content = f.read()

    assert "TODO:" not in content, "Go program still contains 'TODO:' comments."