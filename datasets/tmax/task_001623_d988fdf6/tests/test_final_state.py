# test_final_state.py

import os
import pytest

def test_qa_success_log_exists():
    log_path = "/home/user/gateway_test/qa_success.log"
    assert os.path.isfile(log_path), (
        f"The verification log {log_path} does not exist. "
        "Did you compile and run the fixed executable?"
    )

def test_qa_success_log_content():
    log_path = "/home/user/gateway_test/qa_success.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()

    expected_substring = "Path: /api/v2/users, Param: SuperLongParameter1234567890, PackedSize:"
    assert expected_substring in content, (
        f"The log file {log_path} does not contain the expected output. "
        f"Expected to find '{expected_substring}' in the log file. "
        f"Actual content: {content}"
    )

def test_gateway_executable_exists():
    exe_path = "/home/user/gateway_test/gateway_test"
    assert os.path.isfile(exe_path), (
        f"The executable {exe_path} does not exist. "
        "Did you run 'make' after fixing the code?"
    )
    assert os.access(exe_path, os.X_OK), (
        f"The file {exe_path} is not executable."
    )