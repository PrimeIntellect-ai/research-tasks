# test_final_state.py
import os
import json
import re
import pytest

RESULTS_DIR = "/home/user/audit_task/results"
RAW_DATA_DIR = "/home/user/audit_task/raw_data"

def test_results_directory_exists():
    assert os.path.isdir(RESULTS_DIR), f"Results directory missing: {RESULTS_DIR}"

def test_audit_summary():
    summary_file = os.path.join(RESULTS_DIR, "audit_summary.json")
    assert os.path.isfile(summary_file), f"Audit summary file missing: {summary_file}"

    with open(summary_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_file} is not valid JSON.")

    assert "compromised_file" in data, "Missing 'compromised_file' key in audit summary."
    assert data["compromised_file"] in ["ps", "bin/ps"], f"Incorrect compromised file identified: {data['compromised_file']}"

    assert "malicious_ips_count" in data, "Missing 'malicious_ips_count' key in audit summary."
    assert data["malicious_ips_count"] == 2, f"Incorrect malicious IPs count: {data['malicious_ips_count']}"

def test_firewall_rules():
    rules_file = os.path.join(RESULTS_DIR, "firewall_rules.txt")
    assert os.path.isfile(rules_file), f"Firewall rules file missing: {rules_file}"

    with open(rules_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "iptables -A INPUT -s 172.16.0.2 -j DROP",
        "iptables -A INPUT -s 192.168.1.50 -j DROP"
    ]

    assert lines == expected_lines, f"Firewall rules do not match expected sorted output. Got: {lines}"

def test_sshd_hardening():
    secure_sshd = os.path.join(RESULTS_DIR, "sshd_config.secure")
    assert os.path.isfile(secure_sshd), f"Secure SSH config missing: {secure_sshd}"

    with open(secure_sshd, "r") as f:
        content = f.read()

    lines = [line.strip() for line in content.splitlines()]

    # Check that the correct un-commented directives exist
    assert "PermitRootLogin no" in lines, "Missing or incorrect 'PermitRootLogin no' directive."
    assert "PasswordAuthentication no" in lines, "Missing or incorrect 'PasswordAuthentication no' directive."

    # Check that the insecure commented directives were removed/replaced
    assert not any(re.match(r"^\s*#\s*PermitRootLogin\s+yes", line) for line in lines), "Original commented '#PermitRootLogin yes' is still present."
    assert not any(re.match(r"^\s*#\s*PasswordAuthentication\s+yes", line) for line in lines), "Original commented '#PasswordAuthentication yes' is still present."

def test_redacted_logs():
    redacted_file = os.path.join(RESULTS_DIR, "redacted_logs.jsonl")
    assert os.path.isfile(redacted_file), f"Redacted logs file missing: {redacted_file}"

    with open(redacted_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 11, f"Expected exactly 11 log entries in redacted logs, but found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {redacted_file} is not valid JSON.")

        if "password" in entry:
            assert entry["password"] == "[REDACTED]", f"Password not correctly redacted on line {i+1}."
        if "secret_token" in entry:
            assert entry["secret_token"] == "[REDACTED]", f"Secret token not correctly redacted on line {i+1}."

        # Ensure no accidental plaintext leak
        assert "password123" not in line, f"Plaintext 'password123' leaked on line {i+1}."
        assert "abc123xyz" not in line, f"Plaintext 'abc123xyz' leaked on line {i+1}."