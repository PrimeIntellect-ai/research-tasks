# test_final_state.py

import os
import re

def test_blocked_ips_created_and_correct():
    """Test that blocked_ips.txt contains the correct unique IPs."""
    blocked_ips_path = '/home/user/blocked_ips.txt'
    assert os.path.isfile(blocked_ips_path), f"File {blocked_ips_path} is missing."

    with open(blocked_ips_path, 'r') as f:
        content = f.read().strip()

    ips = [line.strip() for line in content.splitlines() if line.strip()]

    expected_ips = ["10.0.5.99", "192.168.1.15"]

    assert sorted(ips) == expected_ips, f"Expected IPs {expected_ips}, but got {sorted(ips)}"
    assert len(ips) == len(set(ips)), "Duplicate IPs found in blocked_ips.txt"

def test_syslog_redacted_created_and_correct():
    """Test that syslog_redacted.txt is created and correctly redacts private keys."""
    redacted_syslog_path = '/home/user/syslog_redacted.txt'
    original_syslog_path = '/home/user/syslog.txt'

    assert os.path.isfile(redacted_syslog_path), f"File {redacted_syslog_path} is missing."

    with open(redacted_syslog_path, 'r') as f:
        redacted_content = f.read()

    # Check that the sensitive data is gone
    assert "BEGIN OPENSSH PRIVATE KEY" not in redacted_content, "Found 'BEGIN OPENSSH PRIVATE KEY' in redacted syslog."
    assert "END OPENSSH PRIVATE KEY" not in redacted_content, "Found 'END OPENSSH PRIVATE KEY' in redacted syslog."
    assert "b3BlbnNzaC1rZXktdjE" not in redacted_content, "Found key body data in redacted syslog."

    # Check that [REDACTED] was inserted
    assert "[REDACTED]" in redacted_content, "The string '[REDACTED]' was not found in the redacted syslog."

    # Check that non-sensitive lines are preserved
    assert "Linux version 5.15.0" in redacted_content, "Original non-sensitive lines were altered or removed."
    assert "Failed password for root from 192.168.1.15" in redacted_content, "Original non-sensitive lines were altered or removed."
    assert "Started cron utility." in redacted_content, "Original non-sensitive lines were altered or removed."

    # Check that the original file was not modified
    if os.path.isfile(original_syslog_path):
        with open(original_syslog_path, 'r') as f:
            original_content = f.read()
        assert "BEGIN OPENSSH PRIVATE KEY" in original_content, "The original syslog.txt file was modified."