# test_final_state.py

import os
import hashlib
import base64
import re
import pytest

EVIDENCE_FILE = "/home/user/forensics/evidence.txt"
LOG_FILE = "/home/user/forensics/logs/http_req.log"
SYSTEM_ROOT = "/home/user/forensics/system_root"

def find_suid_binary(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                st = os.stat(filepath)
                if st.st_mode & 0o4000:  # SUID bit
                    return filepath
    return None

def get_file_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        sha256.update(f.read())
    return sha256.hexdigest()

def extract_and_decode_malcookie(log_path):
    with open(log_path, "r") as f:
        content = f.read()

    match = re.search(r"Cookie:\s*MalCookie=([A-Za-z0-9+/=]+)", content)
    if match:
        encoded_val = match.group(1)
        return base64.b64decode(encoded_val).decode('utf-8')
    return None

def test_evidence_file_exists():
    assert os.path.isfile(EVIDENCE_FILE), f"The evidence file {EVIDENCE_FILE} does not exist."

def test_evidence_file_contents():
    assert os.path.isfile(EVIDENCE_FILE), f"The evidence file {EVIDENCE_FILE} does not exist."

    # Derive expected values
    suid_binary_path = find_suid_binary(SYSTEM_ROOT)
    assert suid_binary_path is not None, "Could not find SUID binary in system_root to compute expected truth."

    expected_hash = get_file_sha256(suid_binary_path)
    expected_exfil = extract_and_decode_malcookie(LOG_FILE)
    assert expected_exfil is not None, "Could not extract MalCookie from logs to compute expected truth."

    expected_lines = [
        f"SUID_BINARY: {suid_binary_path}",
        f"SUID_HASH: {expected_hash}",
        f"EXFIL_DATA: {expected_exfil}"
    ]
    expected_content = "\n".join(expected_lines) + "\n"

    with open(EVIDENCE_FILE, "r") as f:
        actual_content = f.read()

    # Strip trailing whitespace/newlines for a robust comparison, but ensure exact line-by-line match
    actual_lines = [line.strip() for line in actual_content.strip().split("\n") if line.strip()]

    assert len(actual_lines) == 3, f"Evidence file should have exactly 3 lines, found {len(actual_lines)}."

    assert actual_lines[0] == expected_lines[0], f"First line mismatch. Expected: '{expected_lines[0]}', Got: '{actual_lines[0]}'"
    assert actual_lines[1] == expected_lines[1], f"Second line mismatch. Expected: '{expected_lines[1]}', Got: '{actual_lines[1]}'"
    assert actual_lines[2] == expected_lines[2], f"Third line mismatch. Expected: '{expected_lines[2]}', Got: '{actual_lines[2]}'"