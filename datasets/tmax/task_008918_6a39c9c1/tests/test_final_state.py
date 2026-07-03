# test_final_state.py

import os
import hashlib
import pytest

CLEAN_LOG_PATH = "/home/user/clean_traffic.log"
SHA256_PATH = "/home/user/clean_traffic.sha256"
BLOCK_SCRIPT_PATH = "/home/user/block_c2.sh"

def test_clean_traffic_log_content():
    assert os.path.isfile(CLEAN_LOG_PATH), f"File {CLEAN_LOG_PATH} is missing."

    expected_lines = [
        "[2023-10-25 10:00:01] [10.0.0.5] [192.168.1.50] USER:john SSN:XXX-XX-XXXX",
        "[2023-10-25 10:00:02] [192.168.1.100] [10.0.0.5] DECRYPTED: C2: 10.9.8.7",
        "[2023-10-25 10:00:03] [10.0.0.6] [192.168.1.51] USER:alice SSN:XXX-XX-XXXX"
    ]

    with open(CLEAN_LOG_PATH, "r") as f:
        content = f.read()

    actual_lines = [line for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {CLEAN_LOG_PATH}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} in {CLEAN_LOG_PATH} does not match expected output.\nExpected: {expected}\nActual: {actual.strip()}"

def test_clean_traffic_sha256():
    assert os.path.isfile(SHA256_PATH), f"File {SHA256_PATH} is missing."
    assert os.path.isfile(CLEAN_LOG_PATH), f"Cannot compute hash, {CLEAN_LOG_PATH} is missing."

    with open(CLEAN_LOG_PATH, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    with open(SHA256_PATH, "r") as f:
        stored_hash_content = f.read().strip()

    # The sha256sum output usually looks like: "<hash>  /path/to/file"
    # We just check if the actual hash is in the output
    assert actual_hash in stored_hash_content, f"The hash in {SHA256_PATH} does not match the actual SHA-256 hash of {CLEAN_LOG_PATH}.\nExpected to find: {actual_hash}"

def test_block_c2_script():
    assert os.path.isfile(BLOCK_SCRIPT_PATH), f"File {BLOCK_SCRIPT_PATH} is missing."

    # Check if executable
    assert os.access(BLOCK_SCRIPT_PATH, os.X_OK), f"File {BLOCK_SCRIPT_PATH} is not marked as executable."

    with open(BLOCK_SCRIPT_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"{BLOCK_SCRIPT_PATH} does not contain enough lines."
    assert lines[0] == "#!/bin/bash", f"First line of {BLOCK_SCRIPT_PATH} must be '#!/bin/bash'."

    expected_iptables = "iptables -A OUTPUT -d 10.9.8.7 -j DROP"
    has_iptables = any(expected_iptables in line for line in lines[1:])

    assert has_iptables, f"Could not find the exact iptables command in {BLOCK_SCRIPT_PATH}.\nExpected: {expected_iptables}"