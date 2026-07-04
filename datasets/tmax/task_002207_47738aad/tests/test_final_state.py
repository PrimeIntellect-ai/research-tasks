# test_final_state.py

import os
import re
import stat
import pytest

def test_cwe_report():
    file_path = "/home/user/pentest_audit/cwe_report.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content.upper() == "CWE-798", f"Expected CWE-798 in {file_path}, but found: {content}"

def test_cracked_pin():
    file_path = "/home/user/pentest_audit/cracked_pin.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "4829", f"Expected cracked PIN to be 4829 in {file_path}, but found: {content}"

def test_redacted_logs():
    file_path = "/home/user/pentest_audit/redacted_logs.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    expected_logs = [
        "[INFO] 192.168.1.50 Attempted login user=guest PIN=XXXX",
        "[INFO] 10.0.0.5 Attempted login user=admin PIN=XXXX",
        "[INFO] 10.0.0.5 Attempted login user=admin PIN=XXXX",
        "[INFO] 10.0.0.5 Attempted login user=admin PIN=XXXX",
        "[INFO] 10.0.0.5 Attempted login user=admin PIN=XXXX",
        "[INFO] 192.168.1.100 Attempted login user=admin PIN=XXXX",
        "[INFO] 172.16.0.4 Attempted login user=guest PIN=XXXX"
    ]

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_logs), f"Expected {len(expected_logs)} lines in {file_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_logs)):
        assert actual == expected, f"Line {i+1} in {file_path} does not match expected redacted format. Expected: '{expected}', Actual: '{actual}'"

def test_firewall_rule():
    file_path = "/home/user/pentest_audit/firewall_rule.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    # Check if executable
    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {file_path} is not executable."

    with open(file_path, "r") as f:
        content = f.read().strip()

    # Remove shebang if present and any extra whitespace
    commands = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
    assert len(commands) >= 1, f"No valid commands found in {file_path}"

    cmd = commands[-1]

    # Check for functionally identical iptables syntax
    assert "iptables" in cmd, f"iptables command missing in {file_path}"
    assert "-A INPUT" in cmd or "--append INPUT" in cmd, f"Missing append to INPUT chain in {file_path}"
    assert "-s 10.0.0.5" in cmd or "--source 10.0.0.5" in cmd, f"Missing source IP 10.0.0.5 in {file_path}"
    assert "-j DROP" in cmd or "--jump DROP" in cmd, f"Missing jump DROP in {file_path}"