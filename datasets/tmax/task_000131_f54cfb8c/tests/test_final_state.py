# test_final_state.py

import os
import json
import base64
import subprocess
import pytest

def decode_base64url(s):
    # Add padding if necessary
    s = s.replace('-', '+').replace('_', '/')
    padding = len(s) % 4
    if padding:
        s += '=' * (4 - padding)
    return base64.b64decode(s).decode('utf-8')

def get_expected_jwt_vulns():
    vulns = []
    tokens_dir = "/home/user/tokens"
    if not os.path.exists(tokens_dir):
        return vulns
    for fname in os.listdir(tokens_dir):
        if not fname.endswith('.jwt'):
            continue
        filepath = os.path.join(tokens_dir, fname)
        with open(filepath, 'r') as f:
            content = f.read().strip()
        parts = content.split('.')
        if len(parts) > 0:
            header_b64 = parts[0]
            try:
                header_json = decode_base64url(header_b64)
                header = json.loads(header_json)
                if header.get("alg", "").lower() == "none":
                    vulns.append(f"JWT_VULN: {fname}")
            except Exception:
                pass
    return vulns

def get_expected_injection_vulns():
    vulns = []
    log_file = "/home/user/logs/access.log"
    if not os.path.exists(log_file):
        return vulns
    with open(log_file, 'r') as f:
        for i, line in enumerate(f, start=1):
            if "<script>" in line or "UNION SELECT" in line:
                vulns.append(f"INJECTION_VULN: line {i}")
    return vulns

def get_expected_cert_vulns():
    ca_file = "/home/user/certs/ca.pem"
    server_file = "/home/user/certs/server.pem"
    if not os.path.exists(ca_file) or not os.path.exists(server_file):
        return []

    result = subprocess.run(
        ["openssl", "verify", "-CAfile", ca_file, server_file],
        capture_output=True
    )
    if result.returncode != 0:
        return ["CERT_VULN: server.pem is invalid"]
    return []

def get_expected_perm_vulns():
    vulns = []
    keys_dir = "/home/user/keys"
    if not os.path.exists(keys_dir):
        return vulns
    for fname in os.listdir(keys_dir):
        filepath = os.path.join(keys_dir, fname)
        if os.path.isfile(filepath):
            mode = os.stat(filepath).st_mode
            if (mode & 0o777) != 0o600:
                vulns.append(f"PERM_VULN: {fname}")
    return vulns

def test_audit_script_exists_and_executable():
    script_path = "/home/user/audit_policy.sh"
    assert os.path.exists(script_path), f"Audit script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Audit script {script_path} is not executable."

def test_audit_report_contents():
    report_path = "/home/user/audit_report.txt"
    assert os.path.exists(report_path), f"Audit report {report_path} does not exist."

    with open(report_path, 'r') as f:
        report_lines = [line.strip() for line in f if line.strip()]

    expected_lines = []
    expected_lines.extend(get_expected_jwt_vulns())
    expected_lines.extend(get_expected_injection_vulns())
    expected_lines.extend(get_expected_cert_vulns())
    expected_lines.extend(get_expected_perm_vulns())

    for expected in expected_lines:
        assert expected in report_lines, f"Expected line '{expected}' not found in {report_path}."