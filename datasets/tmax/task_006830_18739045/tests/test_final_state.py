# test_final_state.py

import os
import re
import pytest

def test_new_token_content():
    """Check if the new_token.txt file contains the correct Base64 encoded string without trailing newline."""
    token_path = "/home/user/new_token.txt"
    assert os.path.isfile(token_path), f"File {token_path} does not exist."

    with open(token_path, "r") as f:
        content = f.read()

    expected_token = "c2VjN3g5Ok5FV19BVVRIX0ZMT1c="
    assert content == expected_token, f"Content of {token_path} is incorrect. Expected '{expected_token}', got '{content}'."

def test_firewall_rules_content():
    """Check if the firewall.rules file has the correct iptables-save format and rules."""
    rules_path = "/home/user/firewall.rules"
    assert os.path.isfile(rules_path), f"File {rules_path} does not exist."

    with open(rules_path, "r") as f:
        content = f.read()

    lines = [line.strip() for line in content.splitlines()]

    assert "*filter" in lines, "Missing '*filter' table declaration."
    assert "COMMIT" in lines, "Missing 'COMMIT' keyword."

    # Check default policies
    assert any(line.startswith(":INPUT DROP") for line in lines), "Missing default policy ':INPUT DROP'."
    assert any(line.startswith(":FORWARD DROP") for line in lines), "Missing default policy ':FORWARD DROP'."
    assert any(line.startswith(":OUTPUT ACCEPT") for line in lines), "Missing default policy ':OUTPUT ACCEPT'."

    # Check specific rule
    rule_found = False
    for line in lines:
        if line.startswith("-A INPUT") or line.startswith("--append INPUT"):
            has_tcp = "-p tcp" in line or "--protocol tcp" in line
            has_source = "-s 10.0.0.45" in line or "--source 10.0.0.45" in line
            has_dport = "--dport 9999" in line or "--destination-port 9999" in line
            has_accept = "-j ACCEPT" in line or "--jump ACCEPT" in line

            if has_tcp and has_source and has_dport and has_accept:
                rule_found = True
                break

    assert rule_found, "Missing or incorrect rule for accepting TCP traffic on port 9999 from 10.0.0.45."