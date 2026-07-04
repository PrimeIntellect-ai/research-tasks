# test_final_state.py

import os
import pytest

def test_source_files_exist():
    cpp_file = "/home/user/quota_analyzer.cpp"
    sh_file = "/home/user/deploy_check.sh"

    assert os.path.isfile(cpp_file), f"Missing C++ source file: {cpp_file}"
    assert os.path.isfile(sh_file), f"Missing Bash script file: {sh_file}"

def test_deployment_status_log_content():
    log_file = "/home/user/deployment_status.log"
    assert os.path.isfile(log_file), f"Log file not found at {log_file}. Did the script run successfully?"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[EXCEEDS] /opt/app/backend requires 150 MB more quota",
        "[EXCEEDS] /opt/app/cache requires 200 MB more quota",
        "[OK] /opt/app/frontend requires 0 MB more quota",
        "[EXCEEDS] /opt/app/logs requires 50 MB more quota"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in log, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: '{expected}'\nActual:   '{actual}'"

def test_executable_exists():
    exe_file = "/home/user/quota_analyzer"
    assert os.path.isfile(exe_file), f"Compiled executable not found at {exe_file}. Ensure the bash script compiles the C++ program."
    assert os.access(exe_file, os.X_OK), f"The file at {exe_file} is not executable."