# test_final_state.py

import os
import pytest

def test_hello_txt_merged_correctly():
    target_path = "/home/user/project_root/docs/hello.txt"
    assert os.path.isfile(target_path), f"Expected merged file was not created at {target_path}."

    with open(target_path, "rb") as f:
        content = f.read()

    expected_content = b"Hello World!"
    assert content == expected_content, f"Content of {target_path} is incorrect. Expected {expected_content}, but got {content}."

def test_security_log_contents():
    log_path = "/home/user/logs/security.log"
    assert os.path.isfile(log_path), f"Security log file was not created at {log_path}."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_violation = "VIOLATION: ../user/evil.txt"
    expected_checksum_error = "CHECKSUM_ERROR: docs/bad.txt"

    assert expected_violation in lines, f"Security log is missing the expected path traversal violation. Expected to find: '{expected_violation}'"
    assert expected_checksum_error in lines, f"Security log is missing the expected checksum error. Expected to find: '{expected_checksum_error}'"

def test_invalid_files_not_written():
    evil_path_1 = "/home/user/project_root/../user/evil.txt"
    evil_path_2 = "/home/user/evil.txt"
    bad_path = "/home/user/project_root/docs/bad.txt"

    assert not os.path.exists(evil_path_1) and not os.path.exists(evil_path_2), "Path traversal vulnerability detected! The file evil.txt was written outside the project root."
    assert not os.path.exists(bad_path), f"File with invalid checksum was written to {bad_path}. It should have been rejected."