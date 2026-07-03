# test_final_state.py

import os
import json
import crypt
import pytest

def get_expected_ssh_violations():
    violations = []
    settings = {}

    if os.path.exists("/home/user/sshd_config_test"):
        with open("/home/user/sshd_config_test", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split()
                    if len(parts) >= 2:
                        settings[parts[0]] = parts[1]

    if settings.get("PermitRootLogin") != "no":
        violations.append("PermitRootLogin")
    if settings.get("PasswordAuthentication") != "no":
        violations.append("PasswordAuthentication")

    return sorted(violations)

def get_expected_firewall_violations():
    violations = []

    if os.path.exists("/home/user/iptables_export.txt"):
        with open("/home/user/iptables_export.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("-P INPUT"):
                    if not line.endswith("DROP"):
                        violations.append("INPUT policy is not DROP")
                elif line.startswith("-A INPUT"):
                    if "-p tcp" in line and "--dport" in line and "-j ACCEPT" in line:
                        parts = line.split()
                        try:
                            dport_idx = parts.index("--dport")
                            port = parts[dport_idx + 1]
                            if port != "22":
                                violations.append(f"Unauthorized port {port} ACCEPT")
                        except (ValueError, IndexError):
                            pass
    return sorted(violations)

def get_expected_compromised_users():
    words = []
    if os.path.exists("/home/user/wordlist.txt"):
        with open("/home/user/wordlist.txt", "r") as f:
            words = [w.strip() for w in f.readlines() if w.strip()]

    compromised = []
    if os.path.exists("/home/user/shadow_test"):
        with open("/home/user/shadow_test", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 2:
                    user = parts[0]
                    hash_val = parts[1]
                    if hash_val not in ("*", "!") and len(hash_val) > 10:
                        for word in words:
                            if crypt.crypt(word, hash_val) == hash_val:
                                compromised.append(user)
                                break
    return sorted(compromised)

def test_audit_report_exists():
    path = "/home/user/audit_report.json"
    assert os.path.isfile(path), f"Missing file: {path}. The script must generate the JSON report."

def test_audit_report_structure_and_content():
    path = "/home/user/audit_report.json"
    assert os.path.isfile(path), "Cannot test content because audit_report.json is missing."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_keys = {"ssh_violations", "firewall_violations", "compromised_users"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match the required structure. Expected: {expected_keys}, Found: {set(data.keys())}"

    expected_ssh = get_expected_ssh_violations()
    expected_firewall = get_expected_firewall_violations()
    expected_users = get_expected_compromised_users()

    actual_ssh = sorted(data["ssh_violations"])
    actual_firewall = sorted(data["firewall_violations"])
    actual_users = sorted(data["compromised_users"])

    assert actual_ssh == expected_ssh, f"ssh_violations mismatch. Expected: {expected_ssh}, Found: {actual_ssh}"
    assert actual_firewall == expected_firewall, f"firewall_violations mismatch. Expected: {expected_firewall}, Found: {actual_firewall}"
    assert actual_users == expected_users, f"compromised_users mismatch. Expected: {expected_users}, Found: {actual_users}"