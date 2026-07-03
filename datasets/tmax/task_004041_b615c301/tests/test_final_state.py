# test_final_state.py
import os
import json
import re
import subprocess
import pytest

def test_capacity_report_exists_and_valid():
    report_path = "/home/user/capacity_report.json"
    assert os.path.exists(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "target_mount" in data, "Key 'target_mount' is missing in the report."
    assert data["target_mount"] == "/home/user/app_data", f"Expected target_mount to be '/home/user/app_data', got {data['target_mount']}."

    assert "service_status" in data, "Key 'service_status' is missing in the report."
    assert data["service_status"] == "DOWN", f"Expected service_status to be 'DOWN', got {data['service_status']}."

    assert "timestamp" in data, "Key 'timestamp' is missing in the report."
    timestamp = data["timestamp"]
    assert re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST$", timestamp), \
        f"Timestamp '{timestamp}' does not match the required format 'YYYY-MM-DD HH:MM:SS JST'."

def test_tls_files_exist():
    cert_path = "/home/user/tls.crt"
    key_path = "/home/user/tls.key"
    assert os.path.exists(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.exists(key_path), f"Private key file {key_path} does not exist."

def test_tls_certificate_valid():
    cert_path = "/home/user/tls.crt"

    # Check if CN is localhost
    cmd_cert = ["openssl", "x509", "-in", cert_path, "-text", "-noout"]
    try:
        result = subprocess.run(cmd_cert, capture_output=True, text=True, check=True)
        assert "CN = localhost" in result.stdout or "CN=localhost" in result.stdout, \
            "The certificate Common Name (CN) is not set to 'localhost'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read certificate with openssl: {e.stderr}")

def test_tls_key_valid():
    key_path = "/home/user/tls.key"

    # Check if key is a valid RSA key
    cmd_key = ["openssl", "rsa", "-in", key_path, "-check", "-noout"]
    try:
        result = subprocess.run(cmd_key, capture_output=True, text=True, check=True)
        assert "RSA key ok" in result.stdout, "The private key is not a valid RSA key."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to verify private key with openssl: {e.stderr}")