# test_final_state.py

import os
import json
import subprocess
import pytest

def test_certs_generated_and_valid():
    crt_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.isfile(crt_path), f"{crt_path} is missing."
    assert os.path.isfile(key_path), f"{key_path} is missing."

    # Check Subject CN
    cmd_subject = ["openssl", "x509", "-in", crt_path, "-noout", "-subject"]
    result_subject = subprocess.run(cmd_subject, capture_output=True, text=True)
    assert result_subject.returncode == 0, "Failed to read certificate subject."
    assert "CN = policy.local" in result_subject.stdout or "CN=policy.local" in result_subject.stdout, \
        "Certificate Subject CN is not 'policy.local'."

    # Check RSA 2048-bit key
    cmd_key = ["openssl", "rsa", "-in", key_path, "-noout", "-text"]
    result_key = subprocess.run(cmd_key, capture_output=True, text=True)
    assert result_key.returncode == 0, "Failed to read private key."
    assert "Private-Key: (2048 bit" in result_key.stdout, "Private key is not RSA 2048-bit."

def test_redaction_log_content():
    clean_log_path = "/home/user/data/transactions_clean.log"
    assert os.path.isfile(clean_log_path), f"{clean_log_path} is missing."

    with open(clean_log_path, "r") as f:
        content = f.read().strip()

    expected_content = "User Alice paid with **************** today. Valid until 12/25. Another user Bob used **************** for his transaction. Order 98765 is complete."
    assert content == expected_content, "Redacted log content is incorrect. 16-digit sequences were not redacted properly."

def test_audit_json_report():
    report_path = "/home/user/audit.json"
    assert os.path.isfile(report_path), f"{report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    assert "suid_files" in data, "'suid_files' key is missing from JSON report."
    assert "unauthorized_ports" in data, "'unauthorized_ports' key is missing from JSON report."

    expected_suid = [
        "/home/user/jail/bin/backdoor",
        "/home/user/jail/bin/sneaky_suid"
    ]
    expected_ports = [3306, 8080]

    # Check values and ensure they are sorted as required by the spec
    assert data["suid_files"] == expected_suid, f"'suid_files' list is incorrect or not sorted alphabetically. Expected: {expected_suid}"
    assert data["unauthorized_ports"] == expected_ports, f"'unauthorized_ports' list is incorrect or not sorted numerically. Expected: {expected_ports}"