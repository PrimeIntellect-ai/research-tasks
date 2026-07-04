# test_final_state.py
import os
import re

def test_new_certificates_exist():
    """Verify that the new certificate and key files exist."""
    cert_path = '/home/user/new_cert.pem'
    key_path = '/home/user/new_key.pem'

    assert os.path.exists(cert_path), f"New certificate not found at {cert_path}."
    assert os.path.exists(key_path), f"New key not found at {key_path}."

    with open(cert_path, 'r') as f:
        cert_content = f.read()
    assert "BEGIN CERTIFICATE" in cert_content, f"{cert_path} does not appear to be a valid PEM certificate."

    with open(key_path, 'r') as f:
        key_content = f.read()
    assert "PRIVATE KEY" in key_content, f"{key_path} does not appear to be a valid private key."

def test_app_py_updated():
    """Verify that app.py has been updated with the required security changes."""
    app_path = '/home/user/app.py'
    assert os.path.exists(app_path), f"{app_path} is missing."

    with open(app_path, 'r') as f:
        app_code = f.read()

    assert '127.0.0.1' in app_code, "app.py is not bound to 127.0.0.1."
    assert '0.0.0.0' not in app_code, "app.py is still bound to 0.0.0.0."
    assert 'NEW_ROTATED_TOKEN_2024' in app_code, "app.py does not contain the rotated token NEW_ROTATED_TOKEN_2024."
    assert 'new_cert.pem' in app_code, "app.py does not reference new_cert.pem."
    assert 'new_key.pem' in app_code, "app.py does not reference new_key.pem."
    assert 'Content-Security-Policy' in app_code, "app.py does not contain Content-Security-Policy."

def test_audit_log_contents():
    """Verify that the audit log exists and contains the correct values."""
    log_path = '/home/user/audit_log.txt'
    assert os.path.exists(log_path), f"Audit log missing at {log_path}."

    with open(log_path, 'r') as f:
        log_data = f.read()

    assert re.search(r'Status:\s*200', log_data), "Audit log does not show HTTP Status 200."
    assert re.search(r"CSP:\s*default-src\s+'self';", log_data), "Audit log does not correctly report the CSP header."

    # Check body for expected JSON content, tolerant of spacing
    assert '"data"' in log_data, "Audit log Body missing 'data' key."
    assert '"secure sensitive data"' in log_data, "Audit log Body missing 'secure sensitive data' value."