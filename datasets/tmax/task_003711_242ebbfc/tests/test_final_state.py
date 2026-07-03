# test_final_state.py

import os
import re
import pytest

def is_valid_token(token: str) -> bool:
    """Python implementation of the C validation logic."""
    if len(token) < 5:
        return False
    sum_val = sum(ord(c) for c in token[:4])
    expected = chr((sum_val % 26) + ord('A'))
    return token[4] == expected

def get_expected_blocked_ips() -> list:
    """Parse the log file and determine which IPs should be blocked."""
    log_path = "/home/user/server.log"
    if not os.path.exists(log_path):
        return []

    blocked_ips = set()
    with open(log_path, "r") as f:
        for line in f:
            # Extract IP and Token
            match = re.search(r"IP:\s+([^\s]+)\s+-\s+Token:\s+([^\s]+)", line)
            if match:
                ip = match.group(1)
                token = match.group(2)
                if not is_valid_token(token):
                    blocked_ips.add(ip)

    # Sort IPs numerically by octets (equivalent to sort -V for IPs)
    def ip_key(ip_str):
        try:
            return [int(part) for part in ip_str.split('.')]
        except ValueError:
            return [0]

    return sorted(list(blocked_ips), key=ip_key)

def test_validate_executable_exists_and_runnable():
    """Test that the validate.c file was compiled into an executable named validate."""
    executable_path = "/home/user/validate"
    assert os.path.isfile(executable_path), f"Compiled executable not found at {executable_path}."
    assert os.access(executable_path, os.X_OK), f"The file at {executable_path} is not executable."

def test_blocked_ips_report():
    """Test that the blocked_ips.txt report contains the correct IPs in the correct order."""
    report_path = "/home/user/blocked_ips.txt"
    assert os.path.isfile(report_path), f"Audit report file not found at {report_path}."

    expected_ips = get_expected_blocked_ips()

    with open(report_path, "r") as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_ips, (
        f"The contents of {report_path} are incorrect.\n"
        f"Expected: {expected_ips}\n"
        f"Found:    {actual_ips}"
    )