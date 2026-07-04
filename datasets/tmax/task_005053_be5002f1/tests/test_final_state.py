# test_final_state.py

import os
import json
import re
from collections import defaultdict
import pytest

def get_expected_brute_force_ips(log_path):
    counts = defaultdict(int)
    pattern = re.compile(r"Failed password for admin from (\S+)")
    with open(log_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                counts[match.group(1)] += 1
    return {ip for ip, count in counts.items() if count > 3}

def get_expected_sudo_users(sudoers_path):
    users = set()
    # Pattern looks for username, then any (ALL) or (ALL:ALL), then NOPASSWD: ALL
    # The task says: "look for lines matching the pattern where a user is granted NOPASSWD: ALL"
    # excluding root.
    pattern = re.compile(r"^([a-zA-Z0-9_-]+)\s+.*NOPASSWD:\s*ALL\b")
    with open(sudoers_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            match = pattern.match(line)
            if match:
                user = match.group(1)
                if user != "root":
                    users.add(user)
    return users

def get_expected_open_ports(ports_path):
    with open(ports_path, 'r') as f:
        data = json.load(f)
    unauthorized = set()
    authorized = {22, 80, 443}
    for item in data:
        if item.get("state") == "open" and item.get("port") not in authorized:
            unauthorized.add(item.get("port"))
    return unauthorized

def test_compliance_report_exists():
    report_path = "/home/user/compliance_report.json"
    assert os.path.isfile(report_path), f"Compliance report missing at {report_path}"

def test_compliance_report_schema_and_content():
    report_path = "/home/user/compliance_report.json"
    assert os.path.isfile(report_path), "Compliance report missing."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Compliance report is not a valid JSON file.")

    expected_keys = {"brute_force_ips", "unauthorized_sudo_users", "unauthorized_open_ports"}
    assert set(report.keys()) == expected_keys, f"Report keys must exactly match {expected_keys}"

    # Compute expected truth
    log_path = "/home/user/audit_env/logs/auth.log"
    sudoers_path = "/home/user/audit_env/config/sudoers"
    ports_path = "/home/user/audit_env/network/ports.json"

    expected_ips = get_expected_brute_force_ips(log_path)
    expected_users = get_expected_sudo_users(sudoers_path)
    expected_ports = get_expected_open_ports(ports_path)

    # Validate brute_force_ips
    assert isinstance(report["brute_force_ips"], list), "'brute_force_ips' must be a list."
    assert set(report["brute_force_ips"]) == expected_ips, f"Expected brute force IPs {expected_ips}, but got {set(report['brute_force_ips'])}"

    # Validate unauthorized_sudo_users
    assert isinstance(report["unauthorized_sudo_users"], list), "'unauthorized_sudo_users' must be a list."
    assert set(report["unauthorized_sudo_users"]) == expected_users, f"Expected unauthorized sudo users {expected_users}, but got {set(report['unauthorized_sudo_users'])}"

    # Validate unauthorized_open_ports
    assert isinstance(report["unauthorized_open_ports"], list), "'unauthorized_open_ports' must be a list."
    assert set(report["unauthorized_open_ports"]) == expected_ports, f"Expected unauthorized open ports {expected_ports}, but got {set(report['unauthorized_open_ports'])}"