# test_final_state.py

import os
import subprocess
import pytest

def test_cwe_report():
    report_path = "/home/user/report_cwe.txt"
    assert os.path.isfile(report_path), f"CWE report file missing: {report_path}"
    with open(report_path, "r") as f:
        content = f.read().strip()
    assert "CWE-22" in content.upper(), f"Expected CWE-22 in {report_path}, found: {content}"

def test_client_certificate_exists():
    cert_path = "/home/user/certs/client.crt"
    key_path = "/home/user/certs/client.key"
    assert os.path.isfile(cert_path), f"Client certificate missing: {cert_path}"
    assert os.path.isfile(key_path), f"Client key missing: {key_path}"

def test_client_certificate_subject():
    cert_path = "/home/user/certs/client.crt"
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to read certificate subject: {result.stderr}"
    assert "CN" in result.stdout and "admin_inspector" in result.stdout, \
        f"Subject does not contain CN=admin_inspector. Subject: {result.stdout}"

def test_client_certificate_issuer_and_verification():
    cert_path = "/home/user/certs/client.crt"
    ca_path = "/home/user/ca/ca.crt"

    # Verify issuer
    result_issuer = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-issuer"],
        capture_output=True, text=True
    )
    assert result_issuer.returncode == 0, "Failed to read certificate issuer."
    assert "Local Root CA" in result_issuer.stdout, f"Issuer is not Local Root CA. Issuer: {result_issuer.stdout}"

    # Verify signature
    result_verify = subprocess.run(
        ["openssl", "verify", "-CAfile", ca_path, cert_path],
        capture_output=True, text=True
    )
    assert result_verify.returncode == 0, f"Certificate verification failed: {result_verify.stderr or result_verify.stdout}"
    assert "OK" in result_verify.stdout, f"Certificate not OK: {result_verify.stdout}"

def test_exploit_success():
    token_path = "/home/user/admin_token.txt"
    assert os.path.isfile(token_path), f"Token file missing: {token_path}"
    with open(token_path, "r") as f:
        content = f.read().strip()
    assert content == "EXPLOITED", f"Token file was not successfully exploited. Content found: {content}"