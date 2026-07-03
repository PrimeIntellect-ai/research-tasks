# test_final_state.py

import os
import stat
import hashlib
import subprocess
import pytest

# Constants for paths
DEPLOY_BUNDLE = "/home/user/deploy_bundle.tar.gz"
DEPLOY_DIR = "/home/user/deploy"
APP_DIR = os.path.join(DEPLOY_DIR, "app")
CERTS_DIR = os.path.join(DEPLOY_DIR, "certs")
NGINX_CONF = os.path.join(DEPLOY_DIR, "nginx.conf")
CONFIG_JSON = os.path.join(APP_DIR, "config.json")
INDEX_HTML = os.path.join(APP_DIR, "index.html")
SERVER_CRT = os.path.join(CERTS_DIR, "server.crt")
SERVER_KEY = os.path.join(CERTS_DIR, "server.key")
AUDIT_LOG = "/home/user/audit_log.txt"

EXPECTED_CSP = 'add_header Content-Security-Policy "default-src \'self\'; script-src \'self\' https://trusted.cdn.com; object-src \'none\';";'
EXPECTED_PASSWORD = "Deploy2023_4921"

def test_decryption_and_extraction():
    """Verify the bundle was decrypted and extracted correctly."""
    assert os.path.isfile(DEPLOY_BUNDLE), f"Decrypted tarball not found at {DEPLOY_BUNDLE}."
    assert os.path.isdir(DEPLOY_DIR), f"Extracted directory not found at {DEPLOY_DIR}."
    assert os.path.isdir(APP_DIR), f"App directory not found at {APP_DIR}."
    assert os.path.isfile(CONFIG_JSON), f"config.json not extracted to {CONFIG_JSON}."

def test_tls_certificates():
    """Verify the TLS certificates were generated with the correct parameters."""
    assert os.path.isfile(SERVER_CRT), f"Certificate not found at {SERVER_CRT}."
    assert os.path.isfile(SERVER_KEY), f"Private key not found at {SERVER_KEY}."

    # Verify Common Name (CN) using openssl
    result = subprocess.run(
        ['openssl', 'x509', '-in', SERVER_CRT, '-noout', '-subject'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse certificate at {SERVER_CRT}."
    assert "secure.internal.dev" in result.stdout, \
        f"Certificate subject does not contain CN=secure.internal.dev. Got: {result.stdout.strip()}"

def test_nginx_csp_enforcement():
    """Verify the Nginx configuration has the strict CSP header."""
    assert os.path.isfile(NGINX_CONF), f"Nginx config not found at {NGINX_CONF}."

    with open(NGINX_CONF, 'r') as f:
        content = f.read()

    assert EXPECTED_CSP in content, \
        f"Strict CSP header not found in {NGINX_CONF}. Expected: {EXPECTED_CSP}"
    assert 'add_header Content-Security-Policy "default-src *";' not in content, \
        f"The overly permissive CSP header was not removed from {NGINX_CONF}."

def test_file_permissions():
    """Verify the principle of least privilege is applied to files and directories."""
    assert os.path.exists(APP_DIR), f"App directory missing: {APP_DIR}"
    assert os.path.exists(INDEX_HTML), f"Index file missing: {INDEX_HTML}"
    assert os.path.exists(CONFIG_JSON), f"Config file missing: {CONFIG_JSON}"

    # Check directory permissions (0755)
    app_dir_mode = stat.S_IMODE(os.stat(APP_DIR).st_mode)
    assert app_dir_mode == 0o755, f"Expected {APP_DIR} to have 0755 permissions, got {oct(app_dir_mode)}."

    # Check standard file permissions (0644)
    index_html_mode = stat.S_IMODE(os.stat(INDEX_HTML).st_mode)
    assert index_html_mode == 0o644, f"Expected {INDEX_HTML} to have 0644 permissions, got {oct(index_html_mode)}."

    # Check sensitive config file permissions (0400)
    config_json_mode = stat.S_IMODE(os.stat(CONFIG_JSON).st_mode)
    assert config_json_mode == 0o400, f"Expected {CONFIG_JSON} to have strict 0400 permissions, got {oct(config_json_mode)}."

def test_audit_log():
    """Verify the audit log contains exactly the required 4 lines with correct information."""
    assert os.path.isfile(AUDIT_LOG), f"Audit log not found at {AUDIT_LOG}."

    with open(AUDIT_LOG, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == 4, f"Audit log must contain exactly 4 lines. Found {len(lines)} lines."

    # Line 1: Discovered passphrase
    assert lines[0] == EXPECTED_PASSWORD, f"Line 1 (passphrase) is incorrect. Expected {EXPECTED_PASSWORD}, got {lines[0]}."

    # Line 2: SHA-256 of server.crt
    assert os.path.isfile(SERVER_CRT), f"Cannot compute SHA-256; {SERVER_CRT} is missing."
    with open(SERVER_CRT, 'rb') as f:
        cert_data = f.read()
    expected_hash = hashlib.sha256(cert_data).hexdigest()
    assert lines[1] == expected_hash, f"Line 2 (SHA-256) is incorrect. Expected {expected_hash}, got {lines[1]}."

    # Line 3: Inserted CSP line
    assert lines[2] == EXPECTED_CSP, f"Line 3 (CSP) is incorrect. Expected {EXPECTED_CSP}, got {lines[2]}."

    # Line 4: Octal permissions of config.json
    assert lines[3] in ["400", "0400"], f"Line 4 (permissions) is incorrect. Expected '400' or '0400', got {lines[3]}."