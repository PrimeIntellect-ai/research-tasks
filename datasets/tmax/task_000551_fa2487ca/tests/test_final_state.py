# test_final_state.py

import os
import subprocess
import pytest

def test_secure_audit_script_exists_and_executable():
    script_path = "/home/user/secure_audit.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_secure_audit_script_uses_bwrap():
    script_path = "/home/user/secure_audit.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "bwrap" in content, "The script does not use 'bwrap' as required."
    assert "--unshare-all" in content, "The script does not use '--unshare-all' with bwrap."
    assert "--ro-bind / /" in content, "The script does not use '--ro-bind / /' with bwrap."
    assert "--tmpfs /tmp" in content, "The script does not use '--tmpfs /tmp' with bwrap."

def test_audit_log_contents():
    log_path = "/home/user/audit_log.txt"
    assert os.path.isfile(log_path), f"Audit log {log_path} does not exist."

    # Recompute the expected fingerprint for key2
    key2_path = "/home/user/artifacts/ssh_keys/key2"
    try:
        output = subprocess.check_output(["ssh-keygen", "-lf", key2_path], stderr=subprocess.STDOUT)
        expected_fingerprint = output.decode("utf-8").strip().split()[1]
    except Exception as e:
        pytest.fail(f"Failed to compute fingerprint for {key2_path}: {e}")

    expected_line1 = f"Vulnerable Key Fingerprint: {expected_fingerprint}"
    expected_line2 = "/home/user/artifacts/certs/leaf.pem: OK"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Audit log {log_path} does not contain enough lines."
    assert lines[0] == expected_line1, f"Line 1 mismatch. Expected: '{expected_line1}', Got: '{lines[0]}'"
    assert lines[1] == expected_line2, f"Line 2 mismatch. Expected: '{expected_line2}', Got: '{lines[1]}'"