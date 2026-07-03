# test_final_state.py
import os

def test_c_source_exists():
    path = "/home/user/detect.c"
    assert os.path.isfile(path), f"C source file {path} is missing."

def test_executable_exists():
    path = "/home/user/detect"
    assert os.path.isfile(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_audit_report_contents():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "102,103,10,20",
        "104,105,80,90",
        "106,107,100,110",
        "108,109,120,130"
    ]

    assert lines == expected_lines, f"Contents of {report_path} do not match the expected output. Got: {lines}"