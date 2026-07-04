# test_final_state.py

import os
import subprocess
import pytest

def test_exploit_id_correct():
    path = "/home/user/exploit_id.txt"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "TKN-03", f"Expected exploit_id.txt to contain 'TKN-03', but got '{content}'"

def test_audit_trail_correct():
    path = "/home/user/audit_trail.log"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[TKN-01] ACCEPTED: VALID_SIGNATURE",
        "[TKN-02] REJECTED: INVALID_SIGNATURE",
        "[TKN-03] REJECTED: INSECURE_ALG",
        "[TKN-04] ACCEPTED: VALID_SIGNATURE"
    ]

    assert lines == expected_lines, f"Audit trail content does not match expected output. Got: {lines}"

def test_auth_server_binary_exists():
    path = "/home/user/auth_server"
    assert os.path.isfile(path), f"Missing compiled binary: {path}"
    assert os.access(path, os.X_OK), f"Binary {path} is not executable"

def test_auth_server_patched_behavior():
    path = "/home/user/auth_server"
    assert os.path.isfile(path), f"Missing compiled binary: {path}"

    # Test malicious token
    malicious_token = "eyJhbGciOiJub25lIn0.malicious_payload."
    result = subprocess.run(
        [path, malicious_token],
        capture_output=True,
        text=True
    )
    assert "REJECTED: INSECURE_ALG" in result.stdout, "Patched binary did not output 'REJECTED: INSECURE_ALG' for alg=none token"
    assert result.returncode == 1, f"Patched binary should exit with status 1 for malicious token, got {result.returncode}"

def test_auth_server_normal_behavior():
    path = "/home/user/auth_server"
    assert os.path.isfile(path), f"Missing compiled binary: {path}"

    # Test valid token
    valid_token = "eyJhbGciOiJIUzI1NiJ9.payload.VALID_SIG"
    result = subprocess.run(
        [path, valid_token],
        capture_output=True,
        text=True
    )
    assert "ACCEPTED: VALID_SIGNATURE" in result.stdout, "Patched binary failed to accept valid token"
    assert result.returncode == 0, f"Patched binary should exit with status 0 for valid token, got {result.returncode}"