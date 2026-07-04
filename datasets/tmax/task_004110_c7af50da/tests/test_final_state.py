# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_auth_helper_fixed_exists_and_executable():
    path = "/home/user/audit/auth_helper_fixed"
    assert os.path.isfile(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_auth_helper_fixed_behavior_with_env_var():
    path = "/home/user/audit/auth_helper_fixed"
    env = os.environ.copy()
    env["AUTH_PASS"] = "verify_pass_123"

    try:
        result = subprocess.run([path], env=env, capture_output=True, text=True, timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to execute {path}: {e}")

    assert result.returncode == 0, f"Expected exit code 0 when AUTH_PASS is set, got {result.returncode}."
    expected_output = "Processing with secret: verify_pass_123\n"
    assert result.stdout == expected_output, f"Unexpected output. Expected '{expected_output}', got '{result.stdout}'."

def test_auth_helper_fixed_behavior_without_env_var():
    path = "/home/user/audit/auth_helper_fixed"
    env = os.environ.copy()
    if "AUTH_PASS" in env:
        del env["AUTH_PASS"]

    try:
        result = subprocess.run([path], env=env, capture_output=True, text=True, timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to execute {path}: {e}")

    assert result.returncode == 1, f"Expected exit code 1 when AUTH_PASS is not set, got {result.returncode}."

def test_report_exists_and_format():
    report_path = "/home/user/audit/report.txt"
    c_file_path = "/home/user/audit/auth_helper.c"

    assert os.path.isfile(report_path), f"Report file {report_path} is missing."
    assert os.path.isfile(c_file_path), f"Source file {c_file_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) >= 3, f"Expected at least 3 lines in {report_path}, found {len(lines)}."

    # Line 1: CWE-214
    assert lines[0].upper() == "CWE-214", f"Line 1 should be 'CWE-214', got '{lines[0]}'."

    # Line 2: VALID
    assert lines[1].upper() == "VALID", f"Line 2 should be 'VALID', got '{lines[1]}'."

    # Line 3: SHA256 of auth_helper.c
    with open(c_file_path, "rb") as f:
        c_content = f.read()
    expected_hash = hashlib.sha256(c_content).hexdigest()

    assert lines[2].lower() == expected_hash.lower(), f"Line 3 should be the SHA-256 hash of auth_helper.c ({expected_hash}), got '{lines[2]}'."