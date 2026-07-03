# test_final_state.py
import os
import json
import pytest

def test_vulnerable_client_remediated():
    path = "/home/user/vulnerable_client.py"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # Check for removal of --token
    assert "--token" not in content, "The vulnerable client still contains the '--token' argument."

    # Check for usage of SECRET_TOKEN
    assert "SECRET_TOKEN" in content, "The client does not appear to use the 'SECRET_TOKEN' environment variable."

    # Check for certificate validation
    assert "verify=False" not in content, "The client still contains 'verify=False'."
    assert "/home/user/certs/root_ca.pem" in content, "The client does not reference the root CA path for validation."

def test_audit_report_content():
    path = "/home/user/audit_report.json"
    assert os.path.isfile(path), f"Audit report {path} was not created."

    with open(path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert report.get("token_env_var_used") == "SECRET_TOKEN", "Incorrect or missing 'token_env_var_used'."
    assert report.get("ca_cert_path") == "/home/user/certs/root_ca.pem", "Incorrect or missing 'ca_cert_path'."
    assert report.get("decoded_payload") == "Compliance_Audit_Success_Data_9921", "Incorrect or missing 'decoded_payload'."

    insecure_cookies = report.get("insecure_cookies")
    assert isinstance(insecure_cookies, list), "'insecure_cookies' must be a list."
    assert "legacy_session" in insecure_cookies, "'legacy_session' missing from 'insecure_cookies'."