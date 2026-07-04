# test_final_state.py

import os
import re
import stat
import pytest

def test_recovered_evidence_exists_and_permissions():
    evidence_path = "/home/user/recovered_evidence.txt"
    assert os.path.exists(evidence_path), f"Evidence file not found: {evidence_path}"
    assert os.path.isfile(evidence_path), f"Evidence path is not a file: {evidence_path}"

    file_stat = os.stat(evidence_path)
    permissions = stat.S_IMODE(file_stat.st_mode)

    # 0o400 is 256 in decimal
    assert permissions == 0o400, f"Incorrect permissions on {evidence_path}. Expected 0400, got {oct(permissions)}"

def test_recovered_evidence_contents():
    log_path = "/home/user/exfil.log"
    assert os.path.exists(log_path), f"Log file missing: {log_path}"

    # Derive the expected content from the log file
    with open(log_path, "r") as f:
        log_content = f.read()

    # Extract all auth_token hex strings
    hex_strings = re.findall(r"auth_token=([0-9a-fA-F]+)", log_content)
    assert hex_strings, "Could not find auth_token data in log file to compute expected truth"

    combined_hex = "".join(hex_strings)
    raw_bytes = bytes.fromhex(combined_hex)

    # XOR key derived from the task setup (0x4F)
    xor_key = 0x4F
    expected_bytes = bytes([b ^ xor_key for b in raw_bytes])
    expected_text = expected_bytes.decode('utf-8', errors='replace')

    evidence_path = "/home/user/recovered_evidence.txt"
    assert os.path.exists(evidence_path), f"Evidence file not found: {evidence_path}"

    with open(evidence_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_text.strip(), (
        f"Contents of {evidence_path} do not match the expected decrypted data. "
        f"Expected: '{expected_text}', Got: '{actual_content}'"
    )