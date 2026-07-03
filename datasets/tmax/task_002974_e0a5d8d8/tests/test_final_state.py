# test_final_state.py

import os
import stat
import base64
import hashlib
import pytest

def test_secure_audit_log_exists_and_permissions():
    log_file = "/home/user/secure_audit.log"
    assert os.path.isfile(log_file), f"File {log_file} does not exist."

    file_stat = os.stat(log_file)
    mode = stat.S_IMODE(file_stat.st_mode)
    assert mode == 0o400, f"Permissions of {log_file} are {oct(mode)}, expected 0o400."

def test_secure_audit_log_contents():
    raw_file = "/home/user/raw_audits.txt"
    log_file = "/home/user/secure_audit.log"

    assert os.path.isfile(raw_file), f"File {raw_file} is missing."
    assert os.path.isfile(log_file), f"File {log_file} is missing."

    with open(raw_file, "r") as f:
        raw_lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = []
    for line in raw_lines:
        decoded_bytes = base64.b64decode(line)
        sha256_hex = hashlib.sha256(decoded_bytes).hexdigest()
        decoded_text = decoded_bytes.decode('utf-8', errors='replace')
        expected_lines.append(f"{sha256_hex}:{decoded_text}")

    with open(log_file, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_file}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {log_file} does not match expected output.\nExpected: {expected}\nActual: {actual}"