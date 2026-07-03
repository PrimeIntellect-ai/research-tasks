# test_final_state.py

import os
import json
import subprocess
import pytest

def test_integrity_log():
    """Test that integrity.log exists and contains PASS."""
    log_file = "/home/user/integrity.log"
    assert os.path.exists(log_file), f"Missing file: {log_file}"
    with open(log_file, "r") as f:
        content = f.read().strip()
    assert content == "PASS", f"Expected 'PASS' in {log_file}, got '{content}'"

def test_private_key():
    """Test that new_key.pem is a valid RSA private key."""
    key_file = "/home/user/app_data/new_key.pem"
    assert os.path.exists(key_file), f"Missing file: {key_file}"

    # Check if it's a valid RSA key using openssl
    result = subprocess.run(
        ["openssl", "rsa", "-in", key_file, "-check", "-noout"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Invalid RSA key in {key_file}: {result.stderr}"

def test_certificate():
    """Test that new_cert.pem is a valid cert with CN=secure.internal."""
    cert_file = "/home/user/app_data/new_cert.pem"
    assert os.path.exists(cert_file), f"Missing file: {cert_file}"

    # Check subject using openssl
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_file, "-noout", "-subject"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Invalid certificate in {cert_file}: {result.stderr}"
    subject = result.stdout.strip()
    assert "CN = secure.internal" in subject or "CN=secure.internal" in subject, \
        f"Certificate subject does not contain CN=secure.internal. Got: {subject}"

def test_firewall_policy():
    """Test that firewall_policy.json matches the expected structure."""
    policy_file = "/home/user/firewall_policy.json"
    assert os.path.exists(policy_file), f"Missing file: {policy_file}"

    with open(policy_file, "r") as f:
        try:
            policy = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {policy_file} is not valid JSON")

    expected_policy = {
        "inbound_allow": [
            "192.168.1.50",
            "10.0.0.15",
            "172.16.20.5"
        ],
        "default_action": "deny"
    }

    assert policy == expected_policy, f"Policy JSON does not match expected structure. Got: {policy}"

def test_app_py_credential_rotation():
    """Test that the hardcoded credential in app.py was rotated correctly."""
    app_file = "/home/user/app_data/app.py"
    assert os.path.exists(app_file), f"Missing file: {app_file}"

    with open(app_file, "r") as f:
        content = f.read()

    expected_token = "cm90YXRlZF9zZWN1cmVfdG9rZW5fOTk5"
    assert expected_token in content, f"Expected base64 token '{expected_token}' not found in {app_file}"
    assert 'SECRET_TOKEN = "cm90YXRlZF9zZWN1cmVfdG9rZW5fOTk5"' in content or \
           "SECRET_TOKEN = 'cm90YXRlZF9zZWN1cmVfdG9rZW5fOTk5'" in content, \
           "SECRET_TOKEN variable was not updated correctly."