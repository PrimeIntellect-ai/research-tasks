# test_final_state.py
import os
import subprocess
import re
import pytest

INCIDENT_DIR = "/home/user/incident"
AUTH_SERVER_BIN = os.path.join(INCIDENT_DIR, "auth_server")
CERT_FILE = os.path.join(INCIDENT_DIR, "cert.pem")
KEY_FILE = os.path.join(INCIDENT_DIR, "key.pem")
SSHD_CONFIG = os.path.join(INCIDENT_DIR, "sshd_config")
TEST_SH = os.path.join(INCIDENT_DIR, "test.sh")
TEST_OUTPUT = os.path.join(INCIDENT_DIR, "test_output.log")

def test_auth_server_compiled_and_patched():
    assert os.path.isfile(AUTH_SERVER_BIN), f"{AUTH_SERVER_BIN} is missing. Did you compile the C code?"
    assert os.access(AUTH_SERVER_BIN, os.X_OK), f"{AUTH_SERVER_BIN} is not executable."

    # Test evil.com
    result1 = subprocess.run([AUTH_SERVER_BIN, "redirect_to=http://evil.com"], capture_output=True, text=True)
    out1 = result1.stdout
    assert "Location: /error\r\n" in out1, "auth_server did not redirect http://evil.com to /error"
    assert "Content-Security-Policy: default-src 'self';\r\n" in out1, "auth_server did not include the correct CSP header"

    # Test //evil.com
    result2 = subprocess.run([AUTH_SERVER_BIN, "redirect_to=//evil.com"], capture_output=True, text=True)
    out2 = result2.stdout
    assert "Location: /error\r\n" in out2, "auth_server did not redirect //evil.com to /error"

    # Test /dashboard
    result3 = subprocess.run([AUTH_SERVER_BIN, "redirect_to=/dashboard"], capture_output=True, text=True)
    out3 = result3.stdout
    assert "Location: /dashboard\r\n" in out3, "auth_server did not redirect /dashboard to /dashboard"
    assert "Content-Security-Policy: default-src 'self';\r\n" in out3, "auth_server did not include the correct CSP header"

def test_tls_certificate():
    assert os.path.isfile(CERT_FILE), f"{CERT_FILE} is missing."
    assert os.path.isfile(KEY_FILE), f"{KEY_FILE} is missing."

    # Check key
    key_check = subprocess.run(["openssl", "rsa", "-in", KEY_FILE, "-check", "-noout"], capture_output=True, text=True)
    assert key_check.returncode == 0, "Private key is invalid or requires a passphrase."

    # Check cert
    cert_text = subprocess.run(["openssl", "x509", "-in", CERT_FILE, "-text", "-noout"], capture_output=True, text=True)
    assert cert_text.returncode == 0, "Certificate is invalid."
    out = cert_text.stdout
    assert "CN = localhost" in out or "CN=localhost" in out, "Certificate Common Name is not localhost."
    assert "Public-Key: (2048 bit)" in out, "Certificate is not RSA 2048-bit."

def test_sshd_config():
    assert os.path.isfile(SSHD_CONFIG), f"{SSHD_CONFIG} is missing."
    with open(SSHD_CONFIG, "r") as f:
        content = f.read()

    assert re.search(r"^\s*PermitRootLogin\s+no\s*$", content, re.MULTILINE), "PermitRootLogin is not set to 'no' in sshd_config."
    assert re.search(r"^\s*PasswordAuthentication\s+no\s*$", content, re.MULTILINE), "PasswordAuthentication is not set to 'no' in sshd_config."

def test_test_script_and_output():
    assert os.path.isfile(TEST_SH), f"{TEST_SH} is missing."
    assert os.path.isfile(TEST_OUTPUT), f"{TEST_OUTPUT} is missing. Did you run test.sh?"

    with open(TEST_OUTPUT, "r") as f:
        content = f.read()

    # We expect two responses in the log.
    blocks = content.strip().split("HTTP/1.1 302 Found")
    assert len(blocks) >= 3, "test_output.log does not contain two HTTP 302 responses."

    block1 = blocks[1]
    block2 = blocks[2]

    assert "Location: /error" in block1, "First run in test_output.log did not redirect to /error."
    assert "Content-Security-Policy: default-src 'self';" in block1, "First run in test_output.log missing CSP header."

    assert "Location: /dashboard" in block2, "Second run in test_output.log did not redirect to /dashboard."
    assert "Content-Security-Policy: default-src 'self';" in block2, "Second run in test_output.log missing CSP header."