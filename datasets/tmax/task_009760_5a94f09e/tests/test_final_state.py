# test_final_state.py
import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/uptime_monitor/monitor"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing. Did you run 'make'?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_report_exists_and_correct():
    report_path = "/home/user/uptime_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Uptime: 60.00%"
    assert content == expected_content, f"Expected report content to be '{expected_content}', but got '{content}'."