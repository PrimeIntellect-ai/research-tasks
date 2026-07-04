# test_final_state.py

import os
import pytest

def test_cpp_source_exists():
    cpp_path = "/home/user/audit.cpp"
    assert os.path.isfile(cpp_path), f"C++ source code file {cpp_path} does not exist."

def test_executable_exists():
    exe_path = "/home/user/audit"
    assert os.path.isfile(exe_path), f"Executable file {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_compliance_report_correct():
    report_path = "/home/user/compliance_report.txt"
    assert os.path.isfile(report_path), f"Compliance report file {report_path} does not exist."

    expected_output = "Violation Path: Web->Proxy->ProfileDB, Total Latency: 13"

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_output, f"Content of {report_path} is incorrect. Expected '{expected_output}', got '{content}'."