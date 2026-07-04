# test_final_state.py

import os
import subprocess
import pytest

def test_ssh_config_hardened():
    config_path = "/home/user/target_sshd_config"
    assert os.path.exists(config_path), f"Missing file: {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    assert "PermitRootLogin no" in content, "PermitRootLogin was not changed to 'no'"
    assert "PasswordAuthentication no" in content, "PasswordAuthentication was not changed to 'no'"

    assert "PermitRootLogin yes" not in content, "PermitRootLogin 'yes' is still present"
    assert "PasswordAuthentication yes" not in content, "PasswordAuthentication 'yes' is still present"

def test_encrypted_report_exists_and_valid():
    report_path = "/home/user/report.enc"
    key_path = "/home/user/aes_key.txt"

    assert os.path.exists(report_path), f"Missing encrypted report: {report_path}"
    assert os.path.exists(key_path), f"Missing key file: {key_path}"

    with open(key_path, "r") as f:
        hex_key = f.read().strip()

    assert len(hex_key) == 64, "AES key should be 64 hex characters"

    # Decrypt using openssl
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-in", report_path,
        "-K", hex_key,
        "-iv", "00000000000000000000000000000000"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Failed to decrypt the report. OpenSSL error: {result.stderr}"

    expected_json = '{"vulnerabilities":["PermitRootLogin","PasswordAuthentication"]}'
    assert result.stdout == expected_json, f"Decrypted JSON does not match expected output. Got: {result.stdout}"