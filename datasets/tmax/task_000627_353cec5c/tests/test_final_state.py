# test_final_state.py

import os
import re
import pytest

def test_executable_exists():
    exe_path = "/home/user/ticket_4092/sensor_parser"
    assert os.path.isfile(exe_path), f"Executable {exe_path} was not built. Did you run make?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_report_file_exists():
    report_path = "/home/user/ticket_4092/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

def test_report_content():
    report_path = "/home/user/ticket_4092/report.txt"
    with open(report_path, "r") as f:
        content = f.read().strip()

    # The expected average is 20.475 C. Depending on float/double precision and rounding modes,
    # it might be formatted as 20.47 or 20.48.
    avg_match = re.search(r"Average Temperature:\s*20\.4[78]\s*C", content)
    assert avg_match, (
        "The 'Average Temperature' line is missing or incorrect. "
        "Expected something like 'Average Temperature: 20.48 C'."
    )

    records_match = re.search(r"Valid Records:\s*4", content)
    assert records_match, (
        "The 'Valid Records' line is missing or incorrect. "
        "Expected 'Valid Records: 4'."
    )