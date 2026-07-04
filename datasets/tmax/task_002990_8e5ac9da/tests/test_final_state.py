# test_final_state.py

import os
import pytest

def test_audit_report_matches_secret():
    secret_path = "/home/user/secret_permissions.txt"
    report_path = "/home/user/audit_report.txt"

    assert os.path.exists(secret_path), f"Secret file missing: {secret_path}"
    assert os.path.exists(report_path), f"Audit report missing: {report_path}. The exploit may not have been run or output redirected."

    with open(secret_path, "r") as f:
        expected_content = f.read().strip()

    with open(report_path, "r") as f:
        actual_content = f.read().strip()

    assert expected_content == actual_content, (
        f"Contents of {report_path} do not match {secret_path}. "
        f"Expected '{expected_content}', got '{actual_content}'."
    )

def test_compiled_binary_exists():
    binary_path = "/home/user/validator"
    assert os.path.exists(binary_path), f"Compiled binary missing: {binary_path}"
    assert os.path.isfile(binary_path), f"Not a file: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_exploit_script_exists():
    script_path = "/home/user/exploit.py"
    assert os.path.exists(script_path), f"Exploit script missing: {script_path}"
    assert os.path.isfile(script_path), f"Not a file: {script_path}"