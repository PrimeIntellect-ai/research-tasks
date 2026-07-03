# test_final_state.py

import os
import pytest

def test_decryptor_rs_exists():
    """Verify that the student wrote the decryptor.rs file."""
    path = "/home/user/decryptor.rs"
    assert os.path.isfile(path), f"Expected decryptor source code at {path} is missing."

def test_decrypted_log_exists():
    """Verify that the decrypted log file was generated."""
    path = "/home/user/logs/decrypted_log.txt"
    assert os.path.isfile(path), f"Expected decrypted log at {path} is missing."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "[SECURE_LOG_V1]" in content, "The decrypted log does not contain the expected known plaintext header."
    assert "MALWARE_SIGNATURE_MATCH" in content, "The decrypted log does not contain the expected alert lines."

def test_flag_txt_correct():
    """Verify that the flag.txt contains the correctly extracted and sorted unique IP addresses."""
    path = "/home/user/flag.txt"
    assert os.path.isfile(path), f"Expected output file at {path} is missing."

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ips = [
        "10.0.0.42",
        "192.168.1.100"
    ]

    assert lines == expected_ips, f"The contents of {path} do not match the expected unique, sorted IP addresses. Got: {lines}"