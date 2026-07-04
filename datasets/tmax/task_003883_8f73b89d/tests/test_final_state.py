# test_final_state.py

import os
import re

def test_cracker_c_exists():
    path = "/home/user/cracker.c"
    assert os.path.isfile(path), f"Missing C program: {path}"

def test_new_key_exists_and_valid():
    priv_path = "/home/user/new_key"
    pub_path = "/home/user/new_key.pub"

    assert os.path.isfile(priv_path), f"Missing new private key: {priv_path}"
    assert os.path.isfile(pub_path), f"Missing new public key: {pub_path}"

    with open(priv_path, "r") as f:
        priv_content = f.read()

    assert "OPENSSH PRIVATE KEY" in priv_content, f"The file {priv_path} does not appear to be a valid unencrypted OpenSSH private key."

def test_rotation_summary():
    summary_path = "/home/user/rotation_summary.txt"
    pub_path = "/home/user/new_key.pub"

    assert os.path.isfile(summary_path), f"Missing summary file: {summary_path}"
    assert os.path.isfile(pub_path), f"Missing public key file: {pub_path}"

    with open(pub_path, "r") as f:
        pub_key_content = f.read().strip()

    with open(summary_path, "r") as f:
        summary_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(summary_lines) >= 2, f"Summary file {summary_path} does not have enough lines."
    assert summary_lines[0] == "Old Passphrase: wolf", f"Line 1 of summary file is incorrect. Expected 'Old Passphrase: wolf', got '{summary_lines[0]}'"

    expected_line_2 = f"New Public Key: {pub_key_content}"
    assert summary_lines[1] == expected_line_2, f"Line 2 of summary file is incorrect. Expected '{expected_line_2}', got '{summary_lines[1]}'"

def test_audit_log_redacted():
    log_path = "/home/user/audit.log"
    assert os.path.isfile(log_path), f"Missing audit log file: {log_path}"

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "wolf" not in log_content, "The audit log still contains the plaintext passphrase 'wolf'."
    assert "-----BEGIN ENCRYPTED PRIVATE KEY-----" not in log_content, "The audit log still contains the old encrypted private key header."
    assert "-----END ENCRYPTED PRIVATE KEY-----" not in log_content, "The audit log still contains the old encrypted private key footer."

    assert "[REDACTED_PASS]" in log_content, "The audit log does not contain the required '[REDACTED_PASS]' string."
    assert "[REDACTED_KEY]" in log_content, "The audit log does not contain the required '[REDACTED_KEY]' string."