# test_final_state.py

import os
import pytest

def test_audit_scanner_script_exists():
    """Check that the audit_scanner.sh script was created."""
    script_path = "/home/user/audit_scanner.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_audit_trail_log_content():
    """Verify the contents of the audit_trail.log."""
    log_path = "/home/user/audit_trail.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "VULNERABLE_BINARY:app2,BLOCKED_IP:192.168.50.5",
        "VULNERABLE_BINARY:app3,BLOCKED_IP:172.16.0.25"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(lines)}."

    for expected, actual in zip(expected_lines, lines):
        assert actual == expected, f"Expected line '{expected}', but got '{actual}' in {log_path}."

def test_block_ips_script_content():
    """Verify the contents of the block_ips.sh script."""
    script_path = "/home/user/block_ips.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 1, f"The script {script_path} is empty."
    assert lines[0] == "#!/bin/bash", f"The first line of {script_path} must be '#!/bin/bash'."

    expected_iptables = [
        "iptables -A OUTPUT -d 192.168.50.5 -j DROP",
        "iptables -A OUTPUT -d 172.16.0.25 -j DROP"
    ]

    # Extract the iptables commands
    actual_iptables = [line for line in lines[1:] if line.startswith("iptables")]

    assert len(actual_iptables) == len(expected_iptables), f"Expected {len(expected_iptables)} iptables commands, found {len(actual_iptables)}."

    for expected, actual in zip(expected_iptables, actual_iptables):
        # We allow multiple spaces, so we normalize
        assert " ".join(actual.split()) == " ".join(expected.split()), f"Expected command '{expected}', but got '{actual}' in {script_path}."