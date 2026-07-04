# test_final_state.py

import os
import re
import subprocess
import pytest

def test_cwe_report():
    report_path = "/home/user/cwe_report.txt"
    assert os.path.isfile(report_path), f"File missing: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().upper()

    assert "CWE-78" in content, "CWE-78 (OS Command Injection) missing from report"
    assert "CWE-79" in content, "CWE-79 (Cross-Site Scripting) missing from report"

def test_certificates():
    cert_path = "/home/user/new_cert.pem"
    key_path = "/home/user/new_key.pem"

    assert os.path.isfile(cert_path), f"Certificate missing: {cert_path}"
    assert os.path.isfile(key_path), f"Key missing: {key_path}"

    # Check certificate Subject CN
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to parse certificate"
    assert "CN" in result.stdout and "localhost" in result.stdout, "Certificate Subject CN is not localhost"

    # Check RSA key
    result_key = subprocess.run(
        ["openssl", "rsa", "-in", key_path, "-check", "-noout"],
        capture_output=True, text=True
    )
    assert result_key.returncode == 0, "Key is not a valid RSA key"

def test_code_changes():
    cpp_file = "/home/user/rotate_cli.cpp"
    binary_file = "/home/user/rotate_cli"

    assert os.path.isfile(cpp_file), f"File missing: {cpp_file}"
    assert os.path.isfile(binary_file), f"Compiled binary missing: {binary_file}"

    with open(cpp_file, "r") as f:
        content = f.read()

    assert "system(" not in content, "Vulnerable system() call still present in C++ code"
    assert "<filesystem>" in content, "Missing #include <filesystem> in C++ code"

def test_functional_verification():
    binary_file = "/home/user/rotate_cli"
    cert_path = "/home/user/new_cert.pem"
    key_path = "/home/user/new_key.pem"

    # Test 1: XSS Mitigation
    xss_payload = "<script>alert(1)</script>"
    subprocess.run(
        [binary_file, cert_path, key_path, xss_payload],
        capture_output=True
    )

    status_file = "/home/user/deploy/status.html"
    assert os.path.isfile(status_file), f"Status report missing: {status_file}"

    with open(status_file, "r") as f:
        status_content = f.read()

    assert "<script>" not in status_content, "XSS vulnerability still present: <script> tag found in HTML output"
    assert "&lt;script&gt;" in status_content, "XSS mitigation failed: payload was not properly HTML-encoded"

    # Test 2: Command Injection Mitigation
    pwned_file = "/home/user/pwned"
    if os.path.exists(pwned_file):
        os.remove(pwned_file)

    cmd_payload = "test; touch /home/user/pwned"
    subprocess.run(
        [binary_file, cmd_payload, key_path, "msg"],
        capture_output=True
    )

    assert not os.path.exists(pwned_file), "Command injection vulnerability still present: arbitrary command executed"