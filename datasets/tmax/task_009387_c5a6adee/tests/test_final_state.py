# test_final_state.py

import os
import hashlib

def test_audit_report_exists():
    report_path = '/home/user/audit_report.txt'
    assert os.path.exists(report_path), f"Audit report not found at {report_path}"
    assert os.path.isfile(report_path), f"{report_path} is not a regular file"

def test_audit_report_line1_integrity():
    report_path = '/home/user/audit_report.txt'
    server_path = '/home/user/app/server.py'
    baseline_path = '/home/user/compliance/baseline.sha256'

    assert os.path.exists(server_path), "Server file missing"
    assert os.path.exists(baseline_path), "Baseline file missing"

    with open(server_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()

    with open(baseline_path, 'r') as f:
        baseline_hash = f.read().strip()

    expected_status = "MATCH" if current_hash == baseline_hash else "MISMATCH"
    expected_line = f"Integrity: {expected_status}"

    with open(report_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) >= 1, "Audit report is empty"
    assert lines[0] == expected_line, f"Line 1 of audit report is incorrect. Expected '{expected_line}', got '{lines[0]}'"

def test_audit_report_line2_token():
    report_path = '/home/user/audit_report.txt'
    expected_token = "SECURE_COMPLIANCE_99812"
    expected_line = f"Token: {expected_token}"

    with open(report_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, "Audit report does not have a second line"
    assert lines[1] == expected_line, f"Line 2 of audit report is incorrect. Expected '{expected_line}', got '{lines[1]}'"

def test_audit_report_line3_pubkey():
    report_path = '/home/user/audit_report.txt'
    pubkey_path = '/home/user/.ssh/compliance_key.pub'

    assert os.path.exists(pubkey_path), f"Public key not found at {pubkey_path}"

    with open(pubkey_path, 'r') as f:
        pubkey_contents = f.read().strip()

    expected_line = f"PubKey: {pubkey_contents}"

    with open(report_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) >= 3, "Audit report does not have a third line"
    assert lines[2] == expected_line, f"Line 3 of audit report is incorrect. Expected '{expected_line}', got '{lines[2]}'"

def test_ssh_config_hardening():
    config_path = '/home/user/.ssh/config'
    assert os.path.exists(config_path), f"SSH config not found at {config_path}"

    with open(config_path, 'r') as f:
        config_content = f.read()

    # Check for required directives in the config
    assert "Host audit-vault" in config_content, "SSH config missing 'Host audit-vault'"
    assert "Hostname 127.0.0.1" in config_content or "HostName 127.0.0.1" in config_content, "SSH config missing Hostname for audit-vault"
    assert "IdentityFile /home/user/.ssh/compliance_key" in config_content, "SSH config missing correct IdentityFile"
    assert "Ciphers chacha20-poly1305@openssh.com" in config_content, "SSH config missing correct Ciphers restriction"
    assert "MACs hmac-sha2-512-etm@openssh.com" in config_content, "SSH config missing correct MACs restriction"

def test_ssh_private_key_exists():
    key_path = '/home/user/.ssh/compliance_key'
    assert os.path.exists(key_path), f"Private key not found at {key_path}"

    with open(key_path, 'r') as f:
        key_content = f.read()

    assert "BEGIN OPENSSH PRIVATE KEY" in key_content, "File does not appear to be a valid OpenSSH private key"