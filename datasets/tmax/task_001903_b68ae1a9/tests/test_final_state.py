# test_final_state.py

import os
import pytest

def test_app_redacted_log():
    log_path = "/home/user/app_redacted.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    expected_lines = [
        "[2023-10-01 10:00:00] IP=10.0.0.5 GET /rotate?PASSWORD=*** HTTP/1.1",
        "[2023-10-01 10:05:00] IP=192.168.1.10 GET /status HTTP/1.1",
        "[2023-10-01 10:10:00] IP=172.16.0.4 POST /rotate?API_KEY=*** HTTP/1.1",
        "[2023-10-01 10:15:00] IP=10.0.0.5 GET /rotate?PASSWORD=*** HTTP/1.1",
        "[2023-10-01 10:20:00] IP=10.1.1.1 POST /login USER=admin HTTP/1.1"
    ]

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(actual_lines)}"

    for i, expected_line in enumerate(expected_lines):
        assert actual_lines[i] == expected_line, f"Line {i+1} mismatch. Expected: '{expected_line}', Actual: '{actual_lines[i]}'"

def test_block_ips_sh():
    script_path = "/home/user/block_ips.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    expected_rules = {
        "iptables -A INPUT -s 10.0.0.5 -j DROP",
        "iptables -A INPUT -s 172.16.0.4 -j DROP"
    }

    with open(script_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    actual_rules = set(actual_lines)

    assert len(actual_rules) == len(expected_rules), f"Expected {len(expected_rules)} unique rules in {script_path}, found {len(actual_rules)}"
    assert actual_rules == expected_rules, f"Mismatch in expected iptables rules. Expected: {expected_rules}, Actual: {actual_rules}"
    assert len(actual_lines) == len(expected_rules), "Duplicate or extra lines found in block_ips.sh"