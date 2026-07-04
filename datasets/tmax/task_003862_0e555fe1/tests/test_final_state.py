# test_final_state.py

import os
import re
import hashlib
import pytest

def test_redacted_logs_exists_and_content():
    """Test that redacted_logs.txt exists and contains correctly redacted session IDs."""
    redacted_file = '/home/user/redacted_logs.txt'
    assert os.path.isfile(redacted_file), f"File missing: {redacted_file}"

    with open(redacted_file, 'r') as f:
        content = f.read()

    lines = [line for line in content.splitlines() if line.strip()]
    assert len(lines) == 4, "redacted_logs.txt should contain exactly 4 lines."

    for line in lines:
        assert "session_id=[REDACTED]" in line, f"Session ID not redacted correctly in line: {line}"
        # Make sure no original session IDs are left
        assert not re.search(r"session_id=(?!\[REDACTED\])[a-zA-Z0-9]+", line), f"Unredacted session ID found in line: {line}"

def test_redirect_targets_exists_and_content():
    """Test that redirect_targets.txt contains the correct sorted external URLs."""
    targets_file = '/home/user/redirect_targets.txt'
    assert os.path.isfile(targets_file), f"File missing: {targets_file}"

    with open(targets_file, 'r') as f:
        content = f.read().strip()

    expected_targets = [
        "http://malware.site/download",
        "https://evil.phish.com/login"
    ]

    actual_targets = [line.strip() for line in content.splitlines() if line.strip()]
    assert actual_targets == expected_targets, f"redirect_targets.txt content is incorrect. Expected {expected_targets}, got {actual_targets}"

def test_log_checksum_exists_and_matches():
    """Test that log_checksum.txt contains the correct SHA256 hash of redacted_logs.txt."""
    checksum_file = '/home/user/log_checksum.txt'
    redacted_file = '/home/user/redacted_logs.txt'

    assert os.path.isfile(checksum_file), f"File missing: {checksum_file}"
    assert os.path.isfile(redacted_file), f"File missing: {redacted_file}"

    # Calculate actual SHA256 of the redacted_logs.txt file
    sha256_hash = hashlib.sha256()
    with open(redacted_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    actual_hash = sha256_hash.hexdigest()

    with open(checksum_file, 'r') as f:
        checksum_content = f.read().strip()

    # The format should be "<hash>  /home/user/redacted_logs.txt" or similar
    # We just check if the actual hash is in the file
    assert actual_hash in checksum_content, f"Checksum file does not contain the correct hash. Expected hash: {actual_hash}"

def test_poc_exists_and_content():
    """Test that poc.txt contains the correct PoC URL."""
    poc_file = '/home/user/poc.txt'
    assert os.path.isfile(poc_file), f"File missing: {poc_file}"

    with open(poc_file, 'r') as f:
        content = f.read().strip()

    expected_poc = "http://127.0.0.1:5000/login?redirect_to=http://attacker.com/steal"
    assert content == expected_poc, f"poc.txt content is incorrect. Expected '{expected_poc}', got '{content}'"