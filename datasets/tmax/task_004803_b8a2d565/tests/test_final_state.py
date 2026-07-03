# test_final_state.py

import os
import pytest

def test_fixed_executable_exists():
    executable_path = "/home/user/log_parser_fixed"
    assert os.path.isfile(executable_path), f"The fixed executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_output_metrics_file():
    output_path = "/home/user/output_metrics.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "250", f"Expected output metrics to be '250', but got '{content}'."

def test_trace_report_file():
    report_path = "/home/user/trace_report.txt"
    assert os.path.isfile(report_path), f"The diagnostic report {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"The report {report_path} must contain at least two lines."

    line1 = lines[0]
    line2 = lines[1]

    assert "app_3.log" in line1, f"Expected the first line to indicate 'app_3.log', but got '{line1}'."
    assert "read" in line2.lower(), f"Expected the second line to indicate the 'read' system call, but got '{line2}'."