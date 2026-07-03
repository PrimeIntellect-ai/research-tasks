# test_final_state.py
import os
import ssl
import hashlib
import pytest

def test_secure_report_exists():
    """Verify that the secure report was generated."""
    report_path = '/home/user/secure_report.html'
    assert os.path.isfile(report_path), f"The secure report file was not found at {report_path}."

def test_report_contents():
    """Verify that the secure report contains the correct CSP, integrity status, fingerprint, and config."""
    report_path = '/home/user/secure_report.html'
    assert os.path.isfile(report_path), "Cannot verify contents because secure_report.html is missing."

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Check CSP
    expected_csp = """<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none';">"""
    assert expected_csp in content, "The required exact Content-Security-Policy meta tag is missing."

    # 2. Check Integrity status
    assert "Integrity: OK" in content, "The string 'Integrity: OK' is missing from the report."

    # 3. Check Config plaintext
    # We can read the expected plaintext from the setup logic or just hardcode the known truth from setup
    # However, to be robust, we'll check for the expected dictionary string.
    expected_config = '{"db_host": "secure-db.local", "port": 5432, "feature_flag": true}'
    assert expected_config in content, "The decrypted configuration plaintext is missing from the report."

    # 4. Check Certificate Fingerprint
    cert_path = '/home/user/server.crt'
    assert os.path.isfile(cert_path), f"Certificate file missing at {cert_path}."

    with open(cert_path, 'r') as f:
        pem_data = f.read()

    der_data = ssl.PEM_cert_to_DER_cert(pem_data)
    fingerprint_hex = hashlib.sha256(der_data).hexdigest()
    expected_fingerprint = ':'.join(fingerprint_hex[i:i+2] for i in range(0, len(fingerprint_hex), 2))

    assert expected_fingerprint in content, f"The expected certificate fingerprint ({expected_fingerprint}) is missing from the report."

def test_deploy_script_no_args():
    """Verify that the refactored script no longer uses sys.argv[1] for the key."""
    script_path = '/home/user/deploy.py'
    assert os.path.isfile(script_path), f"Script missing: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    assert "sys.argv[1]" not in content, "The deploy.py script still appears to read from sys.argv[1]."