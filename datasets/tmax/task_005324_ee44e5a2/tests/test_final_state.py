# test_final_state.py

import os
import re
import hashlib
import pytest

LOG_FILE = "/home/user/api_requests.log"
C_SOURCE_FILE = "/home/user/revoke_keys.c"
EXECUTABLE_FILE = "/home/user/revoke_keys"
OUTPUT_FILE = "/home/user/revoked_hashes.txt"

def test_c_source_exists():
    assert os.path.exists(C_SOURCE_FILE), f"C source file {C_SOURCE_FILE} does not exist."
    assert os.path.isfile(C_SOURCE_FILE), f"Path {C_SOURCE_FILE} is not a file."

def test_executable_exists():
    assert os.path.exists(EXECUTABLE_FILE), f"Executable {EXECUTABLE_FILE} does not exist."
    assert os.path.isfile(EXECUTABLE_FILE), f"Path {EXECUTABLE_FILE} is not a file."
    assert os.access(EXECUTABLE_FILE, os.X_OK), f"File {EXECUTABLE_FILE} is not executable."

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."
    assert os.path.isfile(OUTPUT_FILE), f"Path {OUTPUT_FILE} is not a file."

def test_output_file_contents():
    # Derive expected hashes from the log file
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} is missing."

    malicious_keys = set()
    with open(LOG_FILE, 'r') as f:
        for line in f:
            # Match IP and Auth Bearer
            # Format: [YYYY-MM-DD HH:MM:SS] IP: <ip_address> Method: <method> Path: <path> Auth: Bearer <api_key> Status: <status_code>
            ip_match = re.search(r"IP:\s*([0-9\.]+)", line)
            if ip_match:
                ip_addr = ip_match.group(1)
                if ip_addr.startswith("198.51.100."):
                    auth_match = re.search(r"Auth:\s*Bearer\s*(\S+)", line)
                    if auth_match:
                        malicious_keys.add(auth_match.group(1))

    expected_hashes = []
    for key in malicious_keys:
        sha256_hash = hashlib.sha256(key.encode('utf-8')).hexdigest()
        expected_hashes.append(sha256_hash)

    expected_hashes.sort()
    expected_content = "\n".join(expected_hashes) + "\n" if expected_hashes else ""

    with open(OUTPUT_FILE, 'r') as f:
        actual_content = f.read()

    # Standardize newlines for comparison
    actual_lines = [line.strip() for line in actual_content.strip().split('\n') if line.strip()]
    expected_lines = [line.strip() for line in expected_content.strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {OUTPUT_FILE} do not match the expected sorted, unique SHA-256 hashes."