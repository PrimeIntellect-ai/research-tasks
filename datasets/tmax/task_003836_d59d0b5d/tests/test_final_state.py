# test_final_state.py

import os
import subprocess
import pytest

def test_ssh_key_rotated():
    private_key_path = "/home/user/.ssh/id_ed25519_rotated"

    # 1. Check if the private key exists
    assert os.path.exists(private_key_path), f"Private key not found at {private_key_path}"
    assert os.path.isfile(private_key_path), f"{private_key_path} is not a file"

    # 2. Check if it is an ED25519 key using ssh-keygen
    try:
        result = subprocess.run(
            ["ssh-keygen", "-l", "-f", private_key_path],
            capture_output=True,
            text=True,
            check=True
        )
        assert "ED25519" in result.stdout.upper(), f"Key at {private_key_path} is not an ED25519 key. Output: {result.stdout}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to inspect the SSH key with ssh-keygen. Error: {e.stderr}")

def test_redacted_auth_log():
    redacted_log_path = "/home/user/redacted_auth.log"

    # Check if the redacted log exists
    assert os.path.exists(redacted_log_path), f"Redacted log not found at {redacted_log_path}"
    assert os.path.isfile(redacted_log_path), f"{redacted_log_path} is not a file"

    expected_content = """Jan 15 10:00:01 server sshd[1234]: Failed password for invalid user [REDACTED] from 192.168.1.100 port 50000 ssh2
Jan 15 10:05:00 server sshd[1235]: Failed password for [REDACTED] from 10.0.0.5 port 50001 ssh2
Jan 15 10:10:00 server sshd[1236]: Accepted publickey for alice from 192.168.1.50 port 50002 ssh2
Jan 15 10:15:00 server sshd[1237]: Invalid user bob from 10.0.0.6
Jan 15 10:20:00 server sshd[1238]: Failed password for secret_password123 from 10.0.0.7 port 50003 ssh2
Jan 15 10:25:00 server sshd[1239]: Invalid user [REDACTED] from 192.168.1.101
"""

    with open(redacted_log_path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The redacted auth log does not match the expected output. Ensure all redaction rules are correctly applied."