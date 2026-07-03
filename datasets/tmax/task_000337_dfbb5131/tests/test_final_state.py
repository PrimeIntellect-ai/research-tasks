# test_final_state.py

import os
import pytest

WORKSPACE_DIR = "/home/user/traffic_data"
FIREWALL_RULE_PATH = os.path.join(WORKSPACE_DIR, "firewall_rule.sh")
EXPECTED_CMD = "iptables -A INPUT -s 198.51.100.123 -j DROP"

def test_firewall_rule_exists():
    assert os.path.exists(FIREWALL_RULE_PATH), f"File {FIREWALL_RULE_PATH} does not exist."
    assert os.path.isfile(FIREWALL_RULE_PATH), f"{FIREWALL_RULE_PATH} is not a file."

def test_firewall_rule_is_executable():
    assert os.path.exists(FIREWALL_RULE_PATH), f"File {FIREWALL_RULE_PATH} does not exist."
    assert os.access(FIREWALL_RULE_PATH, os.X_OK), f"File {FIREWALL_RULE_PATH} is not executable."

def test_firewall_rule_content():
    assert os.path.exists(FIREWALL_RULE_PATH), f"File {FIREWALL_RULE_PATH} does not exist."
    with open(FIREWALL_RULE_PATH, "r") as f:
        content = f.read().strip()

    # Check if the expected command is in the file
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#") and not line.strip() == "#!/bin/bash" and not line.strip() == "#!/bin/sh"]

    assert any(EXPECTED_CMD in line for line in lines), f"Expected command '{EXPECTED_CMD}' not found in {FIREWALL_RULE_PATH}."